"""Archive the three official CEDD GEO catalogues, linked editions and amendments.
Original PDFs, catalogue context and supersession notices are retained separately.
"""
import concurrent.futures
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import fitz
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://www.cedd.gov.hk'
FAMILIES = {'GEOGUIDES': 'geoguides', 'GEO_PUBLICATIONS': 'geo-gco', 'TGN': 'geo-technical-guidance-notes'}

def get(url):
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1, status_forcelist=[429,500,502,503,504])))
    r = session.get(url, timeout=(20,120))
    r.raise_for_status()
    if urlparse(r.url).hostname != 'www.cedd.gov.hk':
        raise ValueError('Unexpected redirect: '+r.url)
    return r

def discover(family, part):
    catalogue = f'{BASE}/eng/publications/geo/{part}/index.html'
    queue = [catalogue]
    visited, records, notices = set(), {}, []
    while queue:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        r = get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        content = soup.select_one('#content')
        if content is None:
            raise ValueError('Missing catalogue content: '+url)
        dest = ROOT/'geo'/'source_pages'/family/(hashlib.sha256(url.encode()).hexdigest()[:16]+'.html')
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(r.content)
        for row in content.select('tr'):
            context = row.get_text(' ', strip=True)
            if row.select('td'):
                notices.append({'page':url,'text':context})
        for a in content.select('a[href]'):
            target = urljoin(url,a['href'])
            parsed = urlparse(target)
            if parsed.hostname != 'www.cedd.gov.hk':
                continue
            if parsed.path.lower().endswith('.pdf'):
                row = a.find_parent('tr')
                label = a.get_text(' ',strip=True)
                context = row.get_text(' ',strip=True) if row else a.parent.get_text(' ',strip=True)
                if target not in records:
                    name = re.sub(r'[^A-Za-z0-9._-]+','-',unquote(Path(parsed.path).name))
                    prefix = hashlib.sha256(target.encode()).hexdigest()[:8]
                    path = f'documents/GEO/{family}/{family}-{prefix}-{name}'
                    records[target] = {'family':family,'url':target,'source_pdf':path,'text_file':str(Path(path.replace('documents/','indexed_text/',1)).with_suffix('.txt')),'references':[]}
                records[target]['references'].append({'page':url,'label':label,'context':context})
            elif parsed.path.endswith('.html') and any(parsed.path.startswith(f'/{lang}/publications/geo/{part}/') for lang in ['eng','tc']):
                if target not in visited:
                    queue.append(target)
        print(f'Discovered {family}: {len(visited)} pages, {len(records)} PDFs',flush=True)
    if not records:
        raise ValueError('No PDFs discovered: '+catalogue)
    return {'catalogue_url':catalogue,'pages':sorted(visited),'catalogue_rows':notices,'documents':list(records.values())}

def download(item):
    data = get(item['url']).content
    if not data.startswith(b'%PDF-'):
        raise ValueError('Not PDF: '+item['url'])
    with fitz.open(stream=data,filetype='pdf') as doc:
        if not len(doc) or doc.needs_pass:
            raise ValueError('Empty/encrypted PDF: '+item['url'])
        item.update(pages=len(doc),empty_pages=[i for i,p in enumerate(doc,1) if not p.get_text().strip()])
    item.update(sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
    dest=ROOT/item['source_pdf']
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(data)
    print('Saved '+item['source_pdf'],flush=True)
    return item

def main():
    families={key:discover(key,part) for key,part in FAMILIES.items()}
    records=[d for f in families.values() for d in f['documents']]
    errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        jobs={pool.submit(download,d):d for d in records}
        for job in concurrent.futures.as_completed(jobs):
            try: job.result()
            except Exception as exc: errors.append({'url':jobs[job]['url'],'error':str(exc)})
    manifest={'checked_at':datetime.now(timezone.utc).isoformat(),'families':families,'documents':records,'errors':errors,
              'scope':'PDFs linked within official Geoguides, GCO/GEO Publications and TGN catalogue trees, including linked original editions and amendments. GEO Reports, Geospecs and other GEO publication families are outside this scope. Cancelled TGN rows are preserved, even where no PDF is offered. Catalogue inclusion does not establish current applicability. Image-only pages require visual review; no unverified OCR is substituted.'}
    (ROOT/'geo'/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if errors: raise SystemExit(f'{len(errors)} downloads failed; see geo/manifest.json')
    print(f'Saved {len(records)} GEO PDFs',flush=True)

if __name__=='__main__': main()
