"""Verify archive hashes, exact page coverage and FTS retrieval for every GEO PDF."""
import hashlib,json,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    m=json.loads((ROOT/'geo/manifest.json').read_text())
    assert not m['errors'],m['errors']
    results={}
    entries={d['source']:d for d in json.loads((ROOT/'index_manifest.json').read_text())['documents']}
    ocr_pages=0
    content_documents=0
    with sqlite3.connect(ROOT/'search/pnap_fts.sqlite3') as db:
        for d in m['documents']:
            path=ROOT/d['source_pdf']
            assert hashlib.sha256(path.read_bytes()).hexdigest()==d['sha256'],str(path)
            source=str(Path(d['source_pdf']).relative_to('documents').with_suffix('.txt'))
            pages=[r[0] for r in db.execute('select page_no from page where source=? order by page_no',(source,))]
            assert pages==list(range(1,d['pages']+1)),source
            n=db.execute('select count(*) from page_fts join page p on p.id=page_fts.rowid where page_fts match ? and p.source=?',('"'+path.stem+'"',source)).fetchone()[0]
            assert n==d['pages'],source
            entry=entries[d['source_pdf'].removeprefix('documents/')]
            ocr_pages+=len(entry.get('ocr_pages',[]))
            if db.execute('select count(*) from page where source=? and length(trim(content))>0',(source,)).fetchone()[0]: content_documents+=1
            results[d['family']]=results.get(d['family'],0)+1
    audit={'content_documents':content_documents,'ocr_pages':ocr_pages,'families':results,'verified_pdfs':len(m['documents']),'errors':[],'image_or_empty_pages':[{ 'source_pdf':d['source_pdf'],'pages':d['empty_pages']} for d in m['documents'] if d['empty_pages']]}
    (ROOT/'geo/search_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps({k:v for k,v in audit.items() if k!='image_or_empty_pages'}))
if __name__=='__main__':main()
