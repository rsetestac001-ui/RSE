"""Document-diverse retrieval. Ranking never reads the QA labels or expected answers."""
import json
import math
import re
import sqlite3
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'search/pnap_fts.sqlite3'
GENERIC = {'design', 'guidance', 'technical', 'code', 'requirement', 'submission'}
STOP = {'a', 'an', 'the', 'of', 'for', 'and', 'in', 'to', 'on', 'is', 'are', 'with'}
ALIASES = {
    'gi': 'ground investigation', 'els': 'excavation lateral support',
    'sf': 'site formation', 'gbp': 'general building plan', 'rc': 'reinforced concrete',
    '指定地區': 'scheduled area', '土地勘測': 'ground investigation',
    '地盤勘測': 'site investigation', '入則': 'submission approval',
    '地盤平整': 'site formation', '擋土牆': 'retaining wall',
    '風荷載': 'wind effects', '鑽孔樁': 'bored pile', '開工': 'commencement consent',
    '續期': 'renewal consent', '斜坡穩定': 'slope stability',
}


@lru_cache(maxsize=24000)
def tokens(text):
    # Conservative inflection handling, with no document-specific routing.
    result = []
    for word in re.findall(r'[a-z0-9]+', text.lower()):
        if word in STOP:
            continue
        if word.endswith('ies') and len(word) > 4:
            word = word[:-3] + 'y'
        elif word.endswith('s') and len(word) > 3 and not word.endswith(('ss', 'us')):
            word = word[:-1]
        result.append(word)
    return result


def expand(query):
    value = query.lower()
    for key, replacement in ALIASES.items():
        if re.search(r'[a-z]', key):
            value = re.sub(r'\b' + re.escape(key) + r'\b', replacement, value)
        else:
            value = value.replace(key, replacement)
    return value


@lru_cache(maxsize=1)
def metadata():
    result = {}
    for name in ('codes/manifest.json', 'geo/manifest.json', 'explanatory/manifest.json'):
        path = ROOT / name
        if not path.exists():
            continue
        for doc in json.loads(path.read_text())['documents']:
            source = doc['text_file'].removeprefix('indexed_text/')
            refs = doc.get('references', [])
            result[source] = {
                'title': doc.get('title') or ' '.join(x['label'] for x in refs[:1]),
                'official_url': doc.get('url'), 'must_read_with': doc.get('must_read_with') or [],
                'code_basis': doc.get('code_basis'),
                'catalogue_context': ' '.join(x.get('context', '') for x in refs),
                'kind': doc.get('kind', 'technical_guidance'),
            }
    with sqlite3.connect(DB) as con:
        for source, text in con.execute('SELECT source,content FROM page WHERE page_no=1'):
            info = result.setdefault(source, {})
            if not info.get('title'):
                # PNAP page headers contain the human-readable title before paragraphs.
                title = re.split(r'\n\s*(?:Introduction|General|1\.|2\.)\s', text, maxsplit=1)[0]
                info['title'] = title[:1800]
    for source, info in result.items():
        if source.startswith('PNAP/'):
            raw = (ROOT/'indexed_text'/source).read_text(encoding='utf-8')
            references = []
            for family, number in re.findall(r'\b(APP|ADM|ADV)\s*-\s*(\d+)\b', raw):
                code = f'{family}-{int(number):03d}' if family != 'ADM' else f'{family}-{int(number):02d}'
                ref = f'PNAP/{family}/{code}.txt'
                if ref != source and (ROOT/'indexed_text'/ref).exists() and ref not in references:
                    references.append(ref)
            info['cross_references'] = references
    # Preserve old editions, but identify the earlier member of each known series.
    groups = {}
    for source, info in result.items():
        match = re.search(r'(HKIE-[a-z]+)-(\d{4})|/(GEOGUIDES-[^/]*-)?(eg\d)_(\d{4})', source)
        if match:
            group = match[1] or match[4]
            year = int(match[2] or match[5])
            groups.setdefault(group, []).append((year, source))
    for group in groups.values():
        newest = max(year for year, _ in group)
        for year, source in group:
            result[source]['earlier_edition_in_series'] = year < newest
    return result


def search(query, limit=10, db=None):
    path = db or DB
    words = list(dict.fromkeys(tokens(expand(query))))
    if not words:
        return []
    expr = ' OR '.join('"' + w + '"*' for w in words)
    meta = metadata()
    with sqlite3.connect(path) as con:
        total = con.execute('SELECT count(*) FROM page').fetchone()[0]
        weights = {}
        for w in words:
            df = con.execute('SELECT count(*) FROM page_fts WHERE page_fts MATCH ?', ('"'+w+'"*',)).fetchone()[0]
            weights[w] = math.log(1 + total / (1 + df)) * (0.2 if w in GENERIC else 1)
        # Include all matching pages: truncating before document diversity hides short PNAPs.
        rows = con.execute('''SELECT p.code,p.source,p.page_no,p.content,bm25(page_fts)
            FROM page_fts JOIN page p ON p.id=page_fts.rowid
            WHERE page_fts MATCH ?''', (expr,)).fetchall()
    norm = sum(weights.values()) or 1
    best = {}
    for code, source, page, content, bm25 in rows:
        info = meta.get(source, {})
        body = set(tokens(content))
        title = set(tokens(info.get('title', '')))
        coverage = sum(v for w, v in weights.items() if w in body) / norm
        title_coverage = sum(v for w, v in weights.items() if w in title) / norm
        explicit_year = bool(re.search(r'\b(?:19|20)\d{2}\b', query))
        historical_penalty = 0.8 if info.get('earlier_edition_in_series') and not explicit_year else 0
        authority = 0.5 if info.get('kind') == 'code' else 0
        score = 4 * coverage + 5 * title_coverage + min(-bm25, 50) / 50 + authority - historical_penalty
        result = {'code': code, 'source': source, 'pdf_page': page,
                  'score': round(score, 6), 'excerpt': content[:350], **info}
        # Edition is a warning, never a claim that an old code is prohibited.
        result['version_note'] = 'Verify edition, amendments and scope before using this passage.'
        if source not in best or score > best[source]['score']:
            best[source] = result
    return sorted(best.values(), key=lambda x: (-x['score'], x['source']))[:limit]


def search_legislation(query, limit=5):
    path = ROOT / 'search/legislation_fts.sqlite3'
    if not path.exists():
        return []
    words = list(dict.fromkeys(tokens(expand(query))))
    if not words:
        return []
    expr = ' OR '.join('"'+w+'"*' for w in words)
    with sqlite3.connect(path) as con:
        rows = con.execute('''SELECT p.chapter,p.provision,p.heading,p.path,p.version_date,
            p.official_url,snippet(provision_fts,1,'[',']',' … ',48),bm25(provision_fts)
            FROM provision_fts JOIN provision p ON p.id=provision_fts.rowid
            WHERE provision_fts MATCH ? AND p.language='en'
            ORDER BY bm25(provision_fts) LIMIT ?''', (expr, limit)).fetchall()
    return [dict(zip(('chapter','provision','heading','source','version_date','official_url','excerpt','score'), r),
                 pdf_page=None, page_note='XML has no PDF page number') for r in rows]
