"""Archive public HKIE code handbooks; catalogue BD explanations without duplication."""
import argparse, hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import fitz
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT=Path(__file__).resolve().parents[1]
CATALOGUE='https://hkie.org.hk/st/resources/technical-publications/'
BASES={
 'concrete-2013':('concrete 2013','Code of Practice for Structural Use of Concrete 2013; handbook foreword refers to 2020 edition'),
 'concrete-2004':('concrete 2004','Code of Practice for Structural Use of Concrete 2004'),
 'foundations-2017':('foundations 2017','Code of Practice for Foundations 2017'),
 'foundations-2004':('foundations 2004','Code of Practice for Foundations 2004'),
 'steel-2011':('steel 2011','Code of Practice for Structural Use of Steel 2011'),
 'wind-2019':('wind effects in hong kong 2019','Code of Practice on Wind Effects in Hong Kong 2019'),
 'wind-2004':('wind effects in hong kong 2004','Code of Practice on Wind Effects in Hong Kong 2004'),
 'demolition-2004':('demolition of buildings year 2004','Code of Practice for Demolition of Buildings 2004'),
 'precast-2003':('precast concrete construction handbook','Code of Practice for Precast Concrete Construction 2003; handbook published June 2015'),
}

def session():
 s=requests.Session()
 s.mount('https://',HTTPAdapter(max_retries=Retry(total=4,backoff_factor=1,status_forcelist=[429,500,502,503,504])))
 s.headers['User-Agent']='RSE-public-technical-reference-archive/1.0'
 return s

def download():
 s=session()
 r=s.get(CATALOGUE,timeout=(20,120));r.raise_for_status()
 soup=BeautifulSoup(r.content,'html.parser')
 records={}
 for a in soup.select('a[href]'):
  title=' '.join(a.get_text(' ',strip=True).split())
  url=urljoin(CATALOGUE,a['href'])
  if not urlparse(url).path.lower().endswith('.pdf'):continue
  key=next((k for k,(phrase,basis) in BASES.items() if phrase in title.lower()),None)
  if not key:continue
  if urlparse(url).hostname not in ['hkie.org.hk','www.hkie.org.hk']:raise ValueError(url)
  # Remove transient cache-buster query parameters; retain the published PDF path.
  url=urlparse(url)._replace(query='',fragment='').geturl()
  records[key]={'id':'HKIE-'+key,'publisher':'HKIE Structural Division','kind':'explanatory_handbook',
   'title':title,'url':url,'catalogue_url':CATALOGUE,'code_basis':BASES[key][1],
   'source_pdf':f'documents/HKIE/HKIE-{key}.pdf','text_file':f'indexed_text/HKIE/HKIE-{key}.txt',
   'applicability':'Read with the applicable BD code edition, later amendments and PNAP. Catalogue presence does not establish currency.'}
 if set(records)!=set(BASES):raise ValueError(f'Missing catalogue handbooks: {set(BASES)-set(records)}')
 checked=datetime.now(timezone.utc).isoformat()
 for key,item in records.items():
  response=s.get(item['url'],timeout=(20,240));response.raise_for_status()
  data=response.content
  if not data.startswith(b'%PDF-'):raise ValueError('Not a PDF: '+item['url'])
  if len(data)>=100*1024*1024:raise ValueError('PDF exceeds ordinary Git file limit: '+item['url'])
  with fitz.open(stream=data,filetype='pdf') as doc:
   if not len(doc) or doc.needs_pass:raise ValueError('Empty/encrypted PDF: '+item['url'])
   item.update(pages=len(doc),native_empty_pages=[n for n,p in enumerate(doc,1) if not p.get_text().strip()])
  item.update(sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),checked_at=checked,last_modified=response.headers.get('Last-Modified'))
  path=ROOT/item['source_pdf'];path.parent.mkdir(parents=True,exist_ok=True)
  if not path.exists() or path.read_bytes()!=data:path.write_bytes(data)
  print(f"Saved {item['id']}: {item['pages']} pages",flush=True)
 bd=json.loads((ROOT/'codes/manifest.json').read_text())['documents']
 explanations=[dict(d,publisher='Buildings Department') for d in bd if d['kind']=='explanatory' or 'explanatory' in d['title'].lower()]
 if len(explanations)<3:raise ValueError('Missing BD steel/wind explanation or its amendment')
 out=ROOT/'explanatory';out.mkdir(exist_ok=True)
 (out/'hkie_catalogue.html').write_bytes(r.content)
 manifest={'checked_at':checked,'hkie_catalogue_url':CATALOGUE,'documents':list(records.values())+explanations,
  'scope':'Nine publicly linked HKIE code handbooks and BD steel/wind explanatory publications with amendments. Historical handbooks are labelled by their code basis; explanations do not replace codes or PNAP. Original official PDFs are preserved. No claim of complete coverage of every HKIE/BD publication.'}
 (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 catalog=[{k:d.get(k) for k in ['id','publisher','kind','title','code_basis','source_pdf','text_file','pages','url','must_read_with']} for d in manifest['documents']]
 (out/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
 print(f'Catalogued {len(records)} HKIE and {len(explanations)} BD PDFs',flush=True)

def verify():
 import sqlite3
 m=json.loads((ROOT/'explanatory/manifest.json').read_text())
 entries={d['text_file']:d for d in json.loads((ROOT/'index_manifest.json').read_text())['documents']}
 result=[]
 with sqlite3.connect(ROOT/'search/pnap_fts.sqlite3') as db:
  assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
  db.execute("CREATE VIRTUAL TABLE temp.hkie_tokens USING fts5vocab(main,page_fts,instance)")
  tokens=dict(db.execute("SELECT doc,min(term) FROM temp.hkie_tokens GROUP BY doc"))
  for d in m['documents']:
   assert hashlib.sha256((ROOT/d['source_pdf']).read_bytes()).hexdigest()==d['sha256'],d['source_pdf']
   entry=entries[d['text_file']];assert entry['status']!='error',d['text_file']
   if d['source_pdf'].startswith('documents/HKIE/'):
    from explanatory_ocr import cached_text
    for n in d['native_empty_pages']:assert cached_text(d['sha256'],n) is not None,(d['source_pdf'],n)
   source=d['text_file'].removeprefix('indexed_text/')
   rows=db.execute('select id,page_no,content from page where source=? order by page_no',(source,)).fetchall()
   assert [r[1] for r in rows]==list(range(1,d['pages']+1)),source
   nonempty=0
   for row_id,page_no,content in rows:
    if not content.strip():continue
    token=tokens.get(row_id)
    if token:
     assert db.execute('select rowid from page_fts where page_fts match ? and rowid=?',('"'+token.replace('"','""')+'"',row_id)).fetchone(),(source,page_no)
     nonempty+=1
   assert nonempty>0,source
   result.append({'source_pdf':d['source_pdf'],'pages':d['pages'],'searchable_pages':nonempty,'ocr_pages':entry.get('ocr_pages',[]),'empty_pages':entry.get('empty_pages',[]),'verified':True})
  for code in ['ADM-16','APP-030']:
   assert db.execute('select p.id from page_fts join page p on p.id=page_fts.rowid where page_fts match ? and p.code=?',('"ground investigation"',code)).fetchone(),code
 report={'documents':len(result),'pages':sum(d['pages'] for d in result),'errors':[],'results':result}
 (ROOT/'explanatory/search_audit.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='results'}))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('command',choices=['download','verify']);a=ap.parse_args()
 download() if a.command=='download' else verify()
