"""Re-fetch official PDFs and compare bytes with the repository, without AI calls."""
import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'www.bd.gov.hk', 'www.cedd.gov.hk', 'hkie.org.hk', 'www.hkie.org.hk'}


def check(item):
    result = dict(item, checked_at=datetime.now(timezone.utc).isoformat())
    try:
        url = item['official_url']
        if urlparse(url).hostname not in ALLOWED or urlparse(url).scheme != 'https':
            raise ValueError('Expected an allowlisted official HTTPS source')
        local = ROOT / item['source_pdf']
        result['repository_sha256'] = hashlib.sha256(local.read_bytes()).hexdigest()
        request = Request(quote(url, safe=':/%?=&'), headers={'User-Agent': 'RSE-source-verification/1.0'})
        with urlopen(request, timeout=45) as response:
            if urlparse(response.url).hostname not in ALLOWED:
                raise ValueError('Unexpected redirect host')
            digest = hashlib.sha256()
            length = 0
            prefix = b''
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                if not prefix:
                    prefix = block[:5]
                digest.update(block)
                length += len(block)
                if length > 100 * 1024 * 1024:
                    raise ValueError('Unexpectedly large source')
            if prefix != b'%PDF-':
                raise ValueError('Official response is not a PDF')
            result.update(official_sha256=digest.hexdigest(), bytes=length,
                          final_url=response.url, last_modified=response.headers.get('Last-Modified'))
        result['status'] = 'byte_identical' if result['official_sha256'] == result['repository_sha256'] else 'different_bytes_review_required'
    except Exception as exc:
        result.update(status='unconfirmed', error=str(exc))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    items = json.loads((ROOT / 'tests/official_sources.json').read_text())
    with ThreadPoolExecutor(max_workers=max(1,min(args.workers,6))) as pool:
        results = list(pool.map(check, items))
    report = {'method': 'Independent live HTTPS download and SHA-256 byte comparison; not semantic answer validation or proof of exhaustive catalogue currency.',
              'results': results,
              'summary': {s: sum(x['status']==s for x in results) for s in sorted({x['status'] for x in results})}}
    (ROOT / 'search/official_source_check.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(report['summary']))
    if any(item['status'] != 'byte_identical' for item in results):
        raise SystemExit('At least one official PDF source needs review')


if __name__ == '__main__':
    main()
