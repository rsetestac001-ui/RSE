"""Hash-bound OCR cache for scanned GEO pages; all transcription is unverified."""
import concurrent.futures
import json
import os
import subprocess
import tempfile
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
WARNING='[OCR transcription: verify wording, numbers and tables against the original PDF.]\n'
def cached_text(sha,number):
    cache=ROOT/'geo/ocr'/sha/f'page-{number:04d}.json'
    if not cache.exists():return None
    r=json.loads(cache.read_text())
    if r['pdf_sha256']!=sha or r['pdf_page']!=number:raise ValueError('OCR provenance mismatch: '+str(cache))
    return r['text']
def page_text(page,sha):
    native=page.get_text(sort=True).strip()
    if native:return native,False
    text=cached_text(sha,page.number+1)
    return (WARNING+text,True) if text else ('',False)
def recognize(job):
    source,sha,number=job
    with fitz.open(ROOT/source) as doc, tempfile.TemporaryDirectory() as temp:
        image=Path(temp)/'page.png'
        doc[number-1].get_pixmap(dpi=200).save(image)
        lang='eng+chi_tra' if '/tc/' in source or 'cg5' in source else 'eng'
        result=subprocess.run(['tesseract',str(image),'stdout','-l',lang,'--psm','3'],env={**os.environ,'OMP_THREAD_LIMIT':'1'},check=True,capture_output=True,text=True,timeout=180)
    text=result.stdout.strip()
    cache=ROOT/'geo/ocr'/sha/f'page-{number:04d}.json'
    cache.parent.mkdir(parents=True,exist_ok=True)
    cache.write_text(json.dumps({'pdf_sha256':sha,'pdf_page':number,'text':text,'method':'Tesseract at 200 dpi; unverified transcription','language':lang},ensure_ascii=False)+'\n')
    return bool(text)
def main():
    m=json.loads((ROOT/'geo/manifest.json').read_text())
    jobs=[]
    for d in m['documents']:
        for n in d['empty_pages']:
            if cached_text(d['sha256'],n) is None:jobs.append((d['source_pdf'],d['sha256'],n))
    print(f'OCR: {len(jobs)} uncached pages',flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for i,result in enumerate(pool.map(recognize,jobs),1):
            if i%50==0 or i==len(jobs):print(f'OCR: {i}/{len(jobs)} pages processed',flush=True)
if __name__=='__main__':main()
