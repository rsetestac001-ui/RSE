"""Compare repository English XML with the current DOJ official data archive."""
import hashlib
import json
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def main():
    docs = [d for d in json.loads((ROOT/'legislation/manifest.json').read_text())['documents'] if d['language']=='en']
    urls = {d['download_url'] for d in docs}
    if len(urls) != 1:
        raise SystemExit('Expected one English archive; review changed manifest')
    url = urls.pop()
    if not url.startswith('https://resource.data.one.gov.hk/doj/data/'):
        raise SystemExit('Expected official DOJ data archive')
    report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'official_url':url,
              'method':'Compare exact XML member SHA-256 with official archive; no PDF page numbers.', 'results':[]}
    try:
        with tempfile.TemporaryFile() as archive:
            with urlopen(Request(url,headers={'User-Agent':'RSE-source-verification/1.0'}),timeout=120) as response:
                if not response.url.startswith('https://resource.data.one.gov.hk/doj/data/'):
                    raise ValueError('Unexpected archive redirect')
                report['last_modified'] = response.headers.get('Last-Modified')
                total = 0
                while True:
                    chunk = response.read(1024*1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > 700*1024*1024:
                        raise ValueError('Unexpected archive size')
                    archive.write(chunk)
            archive.seek(0)
            with zipfile.ZipFile(archive) as z:
                members = {name.replace('\\', '/'): name for name in z.namelist()}
                for doc in docs:
                    member = doc['archive_member']
                    entry = {'chapter':doc['chapter'],'language':'en','version_date':doc['version_date'],
                             'source':doc['xml_path'],'archive_member':member,'pdf_page':None}
                    if member not in members:
                        entry.update(status='version_or_path_changed_review_required', candidates=[m for m in members if m.startswith(f"cap_{doc['chapter']}_en_c/") and m.endswith('.xml')])
                    else:
                        current = hashlib.sha256(z.read(members[member])).hexdigest()
                        local = hashlib.sha256((ROOT/doc['xml_path']).read_bytes()).hexdigest()
                        entry.update(status='byte_identical' if current==local else 'different_bytes_review_required',
                                     official_sha256=current,repository_sha256=local)
                    report['results'].append(entry)
    except Exception as exc:
        report['error'] = str(exc)
    report['summary'] = {s:sum(x['status']==s for x in report['results']) for s in sorted({x['status'] for x in report['results']})}
    (ROOT/'search/official_legislation_check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('summary','error') if k in report}))
    if report.get('error') or any(x['status']!='byte_identical' for x in report['results']):
        raise SystemExit(1)


if __name__=='__main__':
    main()
