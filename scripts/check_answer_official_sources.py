import concurrent.futures, datetime, hashlib, io, json, re, zipfile
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parents[1]
base='https://www.bd.gov.hk/doc/en/resources/codes-and-references/practice-notes-and-circular-letters/pnap/'
items=[]
for kind,number in [('ADM',16),('APP',30),('APP',25),('APP',56),('APP',57),('APP',49),('APP',18)]:
 stem=f'{kind}-{number:02}' if kind=='ADM' else f'{kind}-{number:03}'
 items.append(dict(path=f'documents/PNAP/{kind}/{stem}.pdf',url=f'{base}{kind}/{kind}{number:03}.pdf'))
for x in json.loads((ROOT/'codes/catalog.json').read_text())['foundations']:
 items.append(dict(path=x['source_pdf'],url=x['url']))
for x in json.loads((ROOT/'explanatory/catalog.json').read_text()):
 if x.get('id')=='HKIE-foundations-2017': items.append(dict(path=x['source_pdf'],url=x['url']))
def fetch(x):
 out=dict(x,checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  r=requests.get(x['url'],timeout=45);out['http_status']=r.status_code;r.raise_for_status()
  if not r.content.startswith(b'%PDF'):raise ValueError('Response is not PDF')
  out['repository_sha256']=hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()
  out['official_sha256']=hashlib.sha256(r.content).hexdigest()
  out['match']=out['repository_sha256']==out['official_sha256'];out['bytes']=len(r.content)
 except Exception as e:out['match']=None;out['error']=str(e)
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(fetch,items))
report=dict(method='Fresh official downloads compared byte-for-byte with pinned repository files. Hash match verifies copied bytes, not semantic correctness or completeness of version discovery.',pdf_results=results,legislation_results=[])
dest=ROOT/'search/answer_official_sources_v1.json'
dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps([(x['path'],x['match'],x.get('error')) for x in results]),flush=True)
manifest=json.loads((ROOT/'legislation/manifest.json').read_text())['documents']
selected=[x for x in manifest if x['language']=='en' and x['chapter'] in ['123','123A']]
url=selected[0]['download_url']
try:
 r=requests.get(url,timeout=(20,90));r.raise_for_status()
 z=zipfile.ZipFile(io.BytesIO(r.content));names={n.replace('\\','/'):n for n in z.namelist()}
 for item in selected:
  expected=item['archive_member'].replace('\\','/')
  matches=[n for n in names if n.endswith(expected)]
  if len(matches)!=1:
   report['legislation_results'].append(dict(chapter=item['chapter'],match=None,error='Pinned version not uniquely found in current official archive; inspect newer version.',url=url));continue
  raw=z.read(names[matches[0]])
  official=hashlib.sha256(raw).hexdigest();local=hashlib.sha256((ROOT/item['xml_path']).read_bytes()).hexdigest()
  report['legislation_results'].append(dict(chapter=item['chapter'],path=item['xml_path'],url=url,version_date=item['version_date'],checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),official_sha256=official,repository_sha256=local,match=official==local))
except Exception as e:report['legislation_results'].append(dict(url=url,match=None,error=str(e)))
dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report['legislation_results']),flush=True)
