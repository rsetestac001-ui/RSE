"""Archive publicly listed HKIE APSEC Discussion Forum summaries, with provenance.

These are discussion summaries, not legislation, PNAP or a complete APSEC record.
No guessed PDF URLs or authenticated/member-only material are downloaded.
"""
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

import fitz

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = 'https://hkie.org.hk/st/resources/summary-of-items-discussed-in-apsec/'
SCOPE_NOTE = ('Publicly listed HKIE Structural Division APSEC Discussion Forum summaries only. '
              'Not a complete historical APSEC meeting/paper archive. Pre-2017 and unlisted meetings '
              'remain unconfirmed. Summaries record discussions at the meeting date; check current '
              'legislation, PNAP and codes before applying them. Do not equate these summaries '
              'with formal APSEC minutes or binding statutory requirements.')


def session():
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    s = requests.Session()
    s.headers['User-Agent'] = 'RSE-public-APSEC-archive/1.0'
    s.mount('https://', HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1,
                  status_forcelist=[429, 500, 502, 503, 504])))
    return s


def meeting_date(title):
    m = re.search(r'(\d{1,2})/(\d{1,2})/(20\d{2})', title)
    if m:
        return datetime.strptime(m.group(), '%d/%m/%Y').date().isoformat()
    m = re.search(r'(\d{1,2} [A-Za-z]+ 20\d{2})', title)
    if m:
        for fmt in ('%d %B %Y', '%d %b %Y'):
            try:
                return datetime.strptime(m.group(), fmt).date().isoformat()
            except ValueError:
                pass
    raise ValueError(f'Cannot verify meeting date from catalogue: {title}')


def discover(html):
    from bs4 import BeautifulSoup
    records = {}
    for a in BeautifulSoup(html, 'html.parser').select('a[href]'):
        title = a.get_text(' ', strip=True)
        u = urlsplit(urljoin(CATALOGUE, a['href']))
        if 'apsec' not in title.lower() or not u.path.lower().endswith('.pdf'):
            continue
        if u.hostname != 'hkie.org.hk':
            raise ValueError(f'Unexpected publisher: {u.hostname}')
        date = meeting_date(title)
        # Cache-busting query strings do not identify different documents.
        url = urlunsplit((u.scheme, u.netloc, u.path, '', ''))
        code = f'APSEC-DF-{date}'
        item = {'code': code, 'meeting_date': date, 'title': title,
                'publisher': 'HKIE Structural Division', 'document_type': 'discussion_forum_summary',
                'catalogue_url': CATALOGUE, 'url': url,
                'source_pdf': f'documents/APSEC/{date[:4]}/{code}.pdf',
                'text_file': f'indexed_text/APSEC/{date[:4]}/{code}.txt'}
        if date in records and records[date]['url'] != url:
            raise ValueError(f'Multiple listed versions for {date}; review before overwriting')
        records[date] = item
    if len(records) < 39:
        raise ValueError(f'Catalogue unexpectedly shrank below the initial 39 summaries: {len(records)}')
    return sorted(records.values(), key=lambda x: x['meeting_date'])


def download(item):
    r = session().get(item['url'], timeout=(15, 90))
    r.raise_for_status()
    if not r.content.startswith(b'%PDF-'):
        raise ValueError(f'Not a PDF: {item["url"]}')
    with fitz.open(stream=r.content, filetype='pdf') as doc:
        if not len(doc) or doc.needs_pass:
            raise ValueError(f'Empty/encrypted: {item["url"]}')
        empty = [i for i, p in enumerate(doc, 1) if not p.get_text().strip()]
        text = '\n'.join(p.get_text() for p in doc)
        if 'apsec' not in text.lower():
            raise ValueError(f'APSEC identity not extractable: {item["url"]}')
        item.update(pages=len(doc), empty_pages=empty)
    item.update(sha256=hashlib.sha256(r.content).hexdigest(), bytes=len(r.content),
                last_modified=r.headers.get('Last-Modified'))
    print(f'Validated {item["code"]}: {item["pages"]} pages', flush=True)
    return item, r.content


def refresh():
    response = session().get(CATALOGUE, timeout=(15, 90))
    response.raise_for_status()
    records = discover(response.content)
    with ThreadPoolExecutor(max_workers=4) as pool:
        staged = list(pool.map(download, records))
    out = ROOT / 'apsec'
    old = out / 'manifest.json'
    previous = json.loads(old.read_text())['documents'] if old.exists() else []
    removed = {x['meeting_date'] for x in previous} - {x['meeting_date'] for x in records}
    if removed:
        raise ValueError(f'Previously listed meetings disappeared; review catalogue: {removed}')
    for item, data in staged:
        dest = ROOT / item['source_pdf']
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists() or dest.read_bytes() != data:
            dest.write_bytes(data)
    out.mkdir(exist_ok=True)
    (out / 'source_catalogue.html').write_bytes(response.content)
    coverage = {}
    for item in records:
        coverage.setdefault(item['meeting_date'][:4], []).append(item['meeting_date'])
    manifest = {'catalogue_url': CATALOGUE, 'checked_at': datetime.now(timezone.utc).isoformat(),
                'catalogue_sha256': hashlib.sha256(response.content).hexdigest(),
                'scope_note': SCOPE_NOTE, 'document_count': len(records),
                'earliest_meeting': records[0]['meeting_date'], 'latest_meeting': records[-1]['meeting_date'],
                'complete_history_verified': False, 'coverage_by_year': coverage,
                'unconfirmed': ['Pre-2017 APSEC summaries, formal minutes and papers',
                                'Any meeting not listed in the public HKIE catalogue'],
                'documents': records}
    (out / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'Saved {len(records)} public summaries; history completeness NOT verified', flush=True)



def page_text(page, pdf_sha):
    """Preserve PDF reading order; OCR image-only pages with a hash-bound cache."""
    text = page.get_text(sort=False).strip()
    if text:
        return text, False
    cache = ROOT / 'apsec/ocr' / pdf_sha / f'page-{page.number + 1:04d}.json'
    if cache.exists():
        record = json.loads(cache.read_text())
        if record['pdf_sha256'] != pdf_sha or record['pdf_page'] != page.number + 1:
            raise ValueError(f'OCR cache provenance mismatch: {cache}')
        text = record['text']
    else:
        import shutil
        import subprocess
        import tempfile
        if not shutil.which('tesseract'):
            raise RuntimeError('Image-only APSEC page requires tesseract-ocr or its hash-bound OCR cache')
        with tempfile.TemporaryDirectory() as temp:
            image = Path(temp) / 'page.png'
            page.get_pixmap(dpi=300).save(image)
            result = subprocess.run(['tesseract', str(image), 'stdout', '-l', 'eng', '--psm', '3'],
                                    check=True, capture_output=True, text=True, timeout=120)
            text = result.stdout.strip()
        if not text:
            raise ValueError(f'OCR produced no text on PDF page {page.number + 1}')
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps({'pdf_sha256': pdf_sha, 'pdf_page': page.number + 1,
                         'method': 'Tesseract English OCR at 300 dpi; unverified transcription',
                         'text': text}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return '[OCR transcription: verify wording, numbers and tables against the original PDF.]\n' + text, True


def verify():
    manifest = json.loads((ROOT / 'apsec/manifest.json').read_text())
    docs = json.loads((ROOT / 'index_manifest.json').read_text())['documents']
    indexed = {x['source']: x for x in docs}
    import sqlite3
    audit = {'documents': len(manifest['documents']), 'pages': 0, 'ocr_pages': [], 'searchable_documents': 0}
    with sqlite3.connect(ROOT / 'search/pnap_fts.sqlite3') as db:
        for item in manifest['documents']:
            path = ROOT / item['source_pdf']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], item['code']
            entry = indexed[item['source_pdf'].removeprefix('documents/')]
            assert entry['status'] != 'error' and entry['pages'] == item['pages'], item['code']
            text = (ROOT / item['text_file']).read_text()
            assert '===== PDF PAGE 1 =====' in text and 'apsec' in text.lower(), item['code']
            source = item['text_file'].removeprefix('indexed_text/')
            count = db.execute('SELECT COUNT(*) FROM page WHERE source=?', (source,)).fetchone()[0]
            assert count == item['pages'], (item['code'], count)
            hits = db.execute('SELECT count(*) FROM page_fts JOIN page p ON p.id=page_fts.rowid '
                              'WHERE page_fts MATCH ? AND p.source=?', ('APSEC', source)).fetchone()[0]
            assert hits, item['code']
            audit['pages'] += count
            audit['searchable_documents'] += 1
            audit['ocr_pages'].extend({'code': item['code'], 'pdf_page': n} for n in entry.get('ocr_pages', []))
    (ROOT / 'apsec/search_audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'Verified PDF hashes, page text and FTS retrieval for all {len(manifest["documents"])} APSEC summaries')


if __name__ == '__main__':
    import sys
    verify() if sys.argv[1:] == ['verify'] else refresh()
