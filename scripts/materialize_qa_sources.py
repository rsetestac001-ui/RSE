"""Restore absent QA source PDFs from their verified official URLs.

Required because API-authored source changes cannot upload the large PDF/index
through the text interface. Existing PDFs are checked against the review snapshot.
"""
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse, quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'www.bd.gov.hk','www.cedd.gov.hk','hkie.org.hk','www.hkie.org.hk'}


def main():
    snapshot = json.loads((ROOT/'search/official_source_check.json').read_text())
    for item in snapshot['results']:
        if item['status'] != 'byte_identical':
            raise ValueError('Unverified source in snapshot: '+item['source_pdf'])
        path = (ROOT/item['source_pdf']).resolve()
        if not path.is_relative_to(ROOT/'documents'):
            raise ValueError('Expected a source under documents/')
        if not path.exists():
            url = item['official_url']
            if urlparse(url).hostname not in ALLOWED or urlparse(url).scheme!='https':
                raise ValueError('Expected an official HTTPS source')
            with urlopen(Request(quote(url,safe=':/%?=&'),headers={'User-Agent':'RSE-QA/1.0'}),timeout=120) as response:
                if urlparse(response.url).hostname not in ALLOWED:
                    raise ValueError('Unexpected redirect')
                data = response.read(100*1024*1024+1)
            if len(data)>100*1024*1024 or not data.startswith(b'%PDF-'):
                raise ValueError('Unexpected PDF response')
            if hashlib.sha256(data).hexdigest()!=item['official_sha256']:
                raise ValueError('Official source changed since review; re-review required')
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(data)
            print('Restored '+item['source_pdf'])
        if hashlib.sha256(path.read_bytes()).hexdigest()!=item['repository_sha256']:
            raise ValueError('Source differs from QA review snapshot: '+item['source_pdf'])
    print(f"Verified {len(snapshot['results'])} PDF snapshot hashes")


if __name__=='__main__':
    main()
