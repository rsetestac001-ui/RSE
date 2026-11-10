"""Download official DoJ XML and build section-level bilingual retrieval. No AI API.

python scripts/legislation.py refresh [--archive-en ZIP --archive-zh ZIP]
python scripts/legislation.py build
python scripts/legislation.py search 'consent commencement' --chapter 123
"""
import argparse
import hashlib
import json
import re
import shutil
import sqlite3
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'legislation'
DB = ROOT / 'search/legislation_fts.sqlite3'
CAPS = ('123', '123A', '123C', '123F', '123Q')
LANGS = ('en', 'zh-Hant')
NS = {'l': 'http://www.xml.gov.hk/schemas/hklm/1.0', 'dc': 'http://purl.org/dc/elements/1.1/'}
FEED = 'https://resource.data.one.gov.hk/doj/data/hkel_c_leg_cap_1_cap_300_{}.zip'

def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def tag(e):
    return e.tag.rsplit('}', 1)[-1]

def text(e):
    # Retain paragraph/table boundaries and image descriptions without breaking inline words.
    blocks = {'section','subsection','paragraph','subparagraph','content','heading',
              'num','leadIn','continued','sourceNote','tr','td','p','schedule','part','def'}
    def render(n):
        s = n.text or ''
        if tag(n) == 'img':
            s += '[Image: '+n.get('alt', n.get('src', ''))+']'
        for c in n:
            s += render(c) + (c.tail or '')
        return ('\n'+s+'\n') if tag(n) in blocks else s
    lines = [re.sub(r'\s+', ' ', line).strip() for line in render(e).splitlines()]
    return '\n'.join(line for line in lines if line)

def refresh(archives):
    BASE.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        stage = Path(td)
        manifest = {'publisher':'Department of Justice, HKSAR Government',
                    'dataset':'https://data.gov.hk/en-data/dataset/hk-doj-hkel-legislation-current',
                    'retrieved_at':datetime.now(timezone.utc).isoformat(), 'documents':[]}
        for lang in LANGS:
            archive = archives.get(lang)
            if not archive:
                archive = stage / (lang+'.zip')
                print('Downloading', FEED.format(lang), flush=True)
                with urllib.request.urlopen(FEED.format(lang), timeout=180) as response, open(archive,'wb') as out:
                    shutil.copyfileobj(response, out)
            with zipfile.ZipFile(archive) as z:
                names = {n.replace('\\','/'):n for n in z.namelist()}
                for cap in CAPS:
                    folder = f'cap_{cap}_{lang}_c/'
                    matches = [n for n in names if n.startswith(folder) and n.endswith('.xml')]
                    if len(matches) != 1:
                        raise ValueError(f'{cap}/{lang}: expected exactly one XML, got {matches}')
                    member = matches[0]
                    raw = z.read(names[member]); xml = ET.fromstring(raw)
                    if xml.findtext('l:meta/l:docNumber', namespaces=NS) != cap:
                        raise ValueError('Chapter metadata mismatch')
                    if xml.get('{http://www.w3.org/XML/1998/namespace}lang') != {'en':'en','zh-Hant':'zh-Hant-HK'}[lang]:
                        raise ValueError('Language metadata mismatch')
                    main = xml.find('l:main', NS)
                    if main is None or not main.findall('.//l:section', NS):
                        raise ValueError('Empty law')
                    files=[]
                    for normalized, original in names.items():
                        if not normalized.startswith(folder) or normalized.endswith('/'):
                            continue
                        relative = PurePosixPath(normalized[len(folder):])
                        if relative.is_absolute() or '..' in relative.parts:
                            raise ValueError('Unsafe archive path')
                        dest = Path('raw') / f'cap{cap}' / lang / str(relative)
                        data=z.read(original)
                        target=stage/dest; target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
                        files.append({'path':(Path('legislation')/dest).as_posix(),'sha256':sha(data),'bytes':len(data)})
                    for img in main.iter():
                        if tag(img)=='img' and not (stage/'raw'/f'cap{cap}'/lang/img.get('src','')).is_file():
                            raise ValueError('Missing statutory image')
                    manifest['documents'].append({'chapter':cap,'language':lang,
                        'version_date':xml.findtext('l:meta/dc:date', namespaces=NS),
                        'status':xml.findtext('l:meta/l:docStatus',namespaces=NS),
                        'official_url':f'https://www.elegislation.gov.hk/hk/cap{cap}',
                        'download_url':FEED.format(lang),'archive_member':member,
                        'xml_path':f'legislation/raw/cap{cap}/{lang}/{PurePosixPath(member).name}',
                        'sha256':sha(raw),'files':files})
        # Do not touch the previous snapshot until every chapter/language has validated.
        shutil.rmtree(BASE/'raw',ignore_errors=True)
        shutil.copytree(stage/'raw', BASE/'raw')
        dump(BASE/'manifest.json', manifest)
    build()

def parse(doc):
    raw=(ROOT/doc['xml_path']).read_bytes()
    if sha(raw) != doc['sha256']: raise ValueError('XML checksum mismatch')
    for f in doc['files']:
        if sha((ROOT/f['path']).read_bytes()) != f['sha256']: raise ValueError('Source checksum mismatch')
    root=ET.fromstring(raw); main=root.find('l:main',NS)
    cap,lang=doc['chapter'],doc['language']
    rows=[]
    def walk(e, context):
        kind=tag(e)
        if kind in ('section','schedule'):
            ident=e.get('temporalId') or e.get('name')
            if not ident or not re.fullmatch(r'[A-Za-z0-9_-]+',ident): raise ValueError('Invalid provision identifier')
            heading=e.find('l:heading', NS)
            row={**{k:doc[k] for k in ('chapter','language','version_date','xml_path','sha256')},
                 'provision':ident,'kind':kind,'role':e.get('role',kind),
                 'heading':text(heading) if heading is not None else '', 'context':context,
                 'status':e.get('status'),'start_period':e.get('startPeriod'),
                 'official_url':doc['official_url']+'?xpid='+e.get('id',''),
                 'content':text(e), 'images':[x.attrib for x in e.iter() if tag(x)=='img'],
                 'subsections':[{'identifier':s.get('temporalId'),'content':text(s)} for s in e.findall('l:subsection',NS)],
                 'path':f'legislation/provisions/cap{cap}/{lang}/{ident}.json'}
            rows.append(row)
            return  # A schedule remains whole, including its own numbered paragraphs.
        heading=e.find('l:heading',NS)
        if kind=='part' and heading is not None: context=context+[text(heading)]
        for child in e: walk(child,context)
    walk(main,[])
    keys=[r['provision'] for r in rows]
    if len(keys)!=len(set(keys)): raise ValueError('Duplicate provision identifier')
    return rows, text(main)

def build():
    manifest=json.loads((BASE/'manifest.json').read_text())
    docs=manifest['documents']
    if {(d['chapter'],d['language']) for d in docs} != {(c,l) for c in CAPS for l in LANGS} or len(docs)!=10:
        raise ValueError('Incomplete bilingual chapter set')
    rows=[]; catalog=[]
    with tempfile.TemporaryDirectory() as td:
        stage=Path(td)
        for doc in docs:
            units,full=parse(doc); rows.extend(units)
            fullpath=f"legislation/text/cap{doc['chapter']}/{doc['language']}.txt"
            p=stage/fullpath;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(full+'\n',encoding='utf-8')
            for row in units: dump(stage/row['path'],row)
            catalog.append({**doc,'full_text_path':fullpath,'provisions':[{'id':u['provision'],'heading':u['heading'],'path':u['path']} for u in units]})
        for folder in ('provisions','text'):
            shutil.rmtree(BASE/folder,ignore_errors=True)
            shutil.copytree(stage/'legislation'/folder,BASE/folder)
    DB.parent.mkdir(exist_ok=True); tmp=DB.with_suffix('.tmp');tmp.unlink(missing_ok=True)
    with sqlite3.connect(tmp) as con:
        con.execute('CREATE TABLE provision(id INTEGER PRIMARY KEY,chapter,language,provision,heading,content,path,version_date,official_url)')
        con.execute("CREATE VIRTUAL TABLE provision_fts USING fts5(heading,content,content='provision',content_rowid='id')")
        for r in rows:
            con.execute('INSERT INTO provision(chapter,language,provision,heading,content,path,version_date,official_url) VALUES(?,?,?,?,?,?,?,?)',tuple(r[k] for k in ('chapter','language','provision','heading','content','path','version_date','official_url')))
        con.execute("INSERT INTO provision_fts(provision_fts) VALUES('rebuild')")
        con.execute("INSERT INTO provision_fts(provision_fts) VALUES('integrity-check')")
    tmp.replace(DB)
    dump(BASE/'catalog.json',{'documents':catalog})
    audit={'documents':len(docs),'provisions':len(rows),'errors':[],
           'chapters':[{'chapter':d['chapter'],'language':d['language'],'version_date':d['version_date'],
                        'provisions':sum(r['chapter']==d['chapter'] and r['language']==d['language'] for r in rows)} for d in docs]}
    s20=next(r for r in rows if r['chapter']=='123' and r['language']=='en' and r['provision']=='s20')
    if 'consent' not in s20['content'].lower(): raise ValueError('Cap123 s20 regression')
    if not search('consent',chapter='123A'): raise ValueError('Cap123A retrieval failed')
    if not search('同意',chapter='123',language='zh-Hant'): raise ValueError('Chinese retrieval failed')
    dump(ROOT/'search/legislation_audit.json',audit)
    for slug,query in {'consent-commencement':'consent commencement','scheduled-area-gi':'scheduled area ground investigation'}.items():
        dump(ROOT/f'search/legislation_topics/{slug}.json', {'query':query,'results':search(query,limit=15)})
    print(json.dumps(audit,ensure_ascii=False))

def search(query,chapter=None,language='en',limit=20):
    if not query.strip(): raise ValueError('Query is empty')
    with sqlite3.connect(DB) as con:
        con.row_factory=sqlite3.Row
        filters='p.language=?'; args=[language]
        if chapter: filters+=' AND p.chapter=?';args.append(chapter)
        if re.search(r'[\u3400-\u9fff]',query):
            # unicode61 does not segment Chinese words. Literal substring retrieval supports even two-character queries.
            sql=f'SELECT p.* FROM provision p WHERE {filters} AND p.content LIKE ? ORDER BY p.id LIMIT ?'
            args += ['%'+query.replace('%','\\%').replace('_','\\_')+'%',limit]
            sql=sql.replace('LIKE ?', "LIKE ? ESCAPE '\\'")
        else:
            expr=' OR '.join('"'+w+'"' for w in re.findall(r'\w+',query))
            if not expr: return []
            sql=f'''SELECT p.* FROM provision_fts JOIN provision p ON p.id=provision_fts.rowid
                    WHERE {filters} AND provision_fts MATCH ? ORDER BY bm25(provision_fts) LIMIT ?'''
            args += [expr,limit]
        hits=[]
        for row in con.execute(sql,args):
            r=dict(row);r.pop('id');content=r.pop('content')
            terms=re.findall(r'\w+',query.lower());pos=min([content.lower().find(t) for t in terms if t in content.lower()] or [0])
            r['excerpt']=content[max(0,pos-120):pos+650];hits.append(r)
        return hits

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('command',choices=['refresh','build','search'])
    ap.add_argument('query',nargs='?');ap.add_argument('--archive-en');ap.add_argument('--archive-zh');ap.add_argument('--chapter',choices=CAPS)
    ap.add_argument('--language',choices=LANGS,default='en');ap.add_argument('--limit',type=int,default=20)
    a=ap.parse_args()
    if a.command=='refresh':refresh({k:v for k,v in [('en',a.archive_en),('zh-Hant',a.archive_zh)] if v})
    elif a.command=='build':build()
    elif a.query:print(json.dumps(search(a.query,a.chapter,a.language,max(1,min(a.limit,100))),ensure_ascii=False,indent=2))
    else:ap.error('Search requires a query')
