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
STOP = {'a', 'an', 'the', 'of', 'for', 'and', 'in', 'to', 'on', 'is', 'are', 'with',
        'can', 'does', 'do', 'not', 'be', 'it', 'this', 'that', 'by', 'or', 'as',
        'any', 'all', 'only', 'what', 'which', 'how', 'than', 'from', 'into',
        'should', 'must', 'may', 'have', 'has', 'under', 'app', 'adm', 'pnap', 'cap'}
ALIASES = {
    'gi': 'ground investigation', 'els': 'excavation lateral support',
    'sf': 'site formation', 'gbp': 'general building plan', 'rc': 'reinforced concrete',
    '指定地區': 'scheduled area', '土地勘測': 'ground investigation',
    '地盤勘測': 'site investigation', '入則': 'submission approval',
    '地盤平整': 'site formation', '擋土牆': 'retaining wall',
    '風荷載': 'wind effects', '鑽孔樁': 'bored pile', '開工': 'commencement consent',
    '續期': 'renewal consent', '斜坡穩定': 'slope stability',
    'cfa': 'continuous flight auger', 'rge': 'registered geotechnical engineer',
    'rse': 'registered structural engineer', 'gifw': 'ground investigation field works',
    'si': 'site investigation', 'hkpd': 'hong kong principal datum',
    '附表所列地區': 'scheduled areas', '半山': 'mid levels',
    '岩土評估': 'geotechnical assessment', '岩土': 'geotechnical',
    '斜坡': 'slope', '坡度': 'gradient', '牆趾': 'toe', '牆頂': 'crest',
    '坡腳': 'toe', '坡頂': 'crest', '開挖面': 'excavation face', '開挖': 'excavation',
    '地段': 'lot', '地盤': 'site', '界至界': 'boundary to boundary',
    '擋土': 'retaining', '豁免': 'exemption', '新界': 'new territories',
    '證書': 'certificate', '證明': 'demonstrate', '填海': 'reclaimed',
    '基礎': 'foundations', '鑽探': 'ground investigation', '鑽孔': 'borehole',
    '土層': 'soil', '樁身': 'pile shaft', '樁端': 'pile base',
    '小直徑': 'small diameter', '大直徑': 'large diameter',
    '樁徑': 'pile diameter', '直徑': 'diameter', '摩擦': 'friction',
    '岩芯': 'cores', '樣本': 'samples', '試驗': 'testing', '試樁': 'trial pile',
    '鋼套管': 'steel casing', '清障': 'obstruction', '搬樁': 'relocated pile',
    '回填': 'backfilled', '重裝': 'reinstalling', '拒進': 'drilling refusal',
    '降水': 'dewatering', '滲流': 'seepage', '水管': 'water main',
    '支撐': 'struts', '圍檁': 'waling', '牆趾穩定': 'toe stability',
    '安全系數': 'factor of safety', '排水分析': 'drained analysis',
    '不排水': 'undrained', '有效應力': 'effective stress', '總應力': 'total stress',
    '傾覆': 'overturning', '監測': 'monitoring', '地下水': 'groundwater',
    '沉降': 'settlement', '隆起': 'heave', '兩階段': 'two stages',
    '第一階段': 'first stage', '次序': 'sequence', '可行': 'feasibility',
    '程式': 'computer program', '混用': 'mixture', '混合': 'mixture',
    '上限': 'maximum limit', '最大': 'maximum', '最低': 'minimum',
    '高度': 'height', '深度': 'depth', '深過': 'deeper', '深於': 'deeper',
    '長度': 'length', '距離': 'distance', '淨距': 'clear distance',
    '垂直': 'vertical', '水平': 'horizontal', '倍': 'times',
    '平均': 'average', '每段': 'increment', '合計': 'combined',
    '出版': 'published', '手冊': 'handbook', '機構': 'institution',
    '月份': 'month', '版次': 'edition', '新版': 'edition',
    '建議': 'recommendations', '意見': 'opinion', '保證': 'warranty',
    '效力': 'disclaimer', '個案': 'particular case', '事實': 'facts',
    '分判': 'others operations', '資料': 'information', '檔名': 'filename',
    '格式': 'format', '報告': 'report', '相片': 'photographs',
    '簽署': 'sign', '認證': 'certified', '結構設計': 'structural design',
    '圖則': 'plans', '提交': 'submission', '批准': 'approval',
    '撤銷': 'revoked', '停工': 'suspended', '延遲': 'delay',
    '通知': 'notice', '書面': 'writing', '部分': 'part',
    '幾耐': 'period', '個月': 'months', '工作天': 'working days',
}


@lru_cache(maxsize=24000)
def tokens(text):
    # Conservative inflection handling, with no document-specific routing.
    result = []
    for word in re.findall(r'[a-z0-9]+', text.lower()):
        if word in STOP or word.isdigit():
            continue
        if word.endswith('ies') and len(word) > 4:
            word = word[:-3] + 'y'
        elif word.endswith('s') and len(word) > 3 and not word.endswith(('ss', 'us')):
            word = word[:-1]
        result.append(word)
    return result


def expand(query):
    value = query.lower()
    # Match longer Chinese phrases first (e.g. 不排水 before 排水).
    chinese = sorted((k for k in ALIASES if not re.search(r'[a-z]', k)), key=len, reverse=True)
    if chinese:
        value = re.sub('|'.join(map(re.escape, chinese)),
                       lambda m: ' ' + ALIASES[m[0]] + ' ', value)
    for key, replacement in ALIASES.items():
        if re.search(r'[a-z]', key):
            # ASCII boundaries permit GI做乜 without matching 'gi' inside digital.
            value = re.sub(r'(?<![a-z0-9])' + re.escape(key) + r'(?![a-z0-9])', replacement, value)
    return value


def explicit_codes(query):
    return {f'{family.upper()}-{int(number)}' for family, number in
            re.findall(r'(?i)(?<![a-z0-9])(APP|ADM|ADV)[ -]*0*(\d+)(?![0-9])', query)}


def canonical_code(code):
    match = re.fullmatch(r'(APP|ADM|ADV)-0*(\d+)', code.upper())
    return f'{match[1]}-{int(match[2])}' if match else code.upper()


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
    codes = explicit_codes(query)
    if not words and not codes:
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
            WHERE page_fts MATCH ?''', (expr,)).fetchall() if expr else []
        seen = {(r[1], r[2]) for r in rows}
        # Exact document lookup must work even with an otherwise unknown phrase.
        if codes:
            for r in con.execute('SELECT code,source,page_no,content,0 FROM page'):
                if canonical_code(r[0]) in codes and (r[1], r[2]) not in seen:
                    rows.append(r)
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
        code_bonus = 15 if canonical_code(code) in codes else 0
        score = 5 * coverage + 3 * title_coverage + min(-bm25, 50) / 50 + authority - historical_penalty + code_bonus
        result = {'code': code, 'source': source, 'pdf_page': page,
                  'score': round(score, 6), 'excerpt': content[:350], **info}
        # Edition is a warning, never a claim that an old code is prohibited.
        result['version_note'] = 'Verify edition, amendments and scope before using this passage.'
        if source not in best or score > best[source]['score']:
            best[source] = result
    ranked = sorted(best.values(), key=lambda x: (-x['score'], x['source']))[:max(0, limit)]
    # Context is separate from the ranked page and must not inflate primary hits.
    with sqlite3.connect(path) as con:
        for result in ranked:
            result['kind'] = 'pdf'
            result['context_pages'] = [dict(pdf_page=p, excerpt=t[:700]) for p, t in con.execute(
                'SELECT page_no,content FROM page WHERE source=? AND page_no BETWEEN ? AND ? AND page_no != ? ORDER BY page_no',
                (result['source'], max(1, result['pdf_page'] - 1), result['pdf_page'] + 1, result['pdf_page']))]
    return ranked


def search_legislation(query, limit=5):
    path = ROOT / 'search/legislation_fts.sqlite3'
    if not path.exists():
        return []
    expanded = expand(query)
    words = [w for w in dict.fromkeys(tokens(expanded))
             if not re.fullmatch(r'(?:cap\d+[a-z]?|s\d+|reg\d+)', w)]
    chapter_match = re.search(r'(?i)\bcap\.?\s*(\d+[a-z]?)\b', query)
    chapter = chapter_match[1].upper() if chapter_match else None
    provision_match = re.search(r'(?i)(?:\bs(?:ection)?\.?|\breg(?:ulation)?\.?)\s*(\d+)\b', query)
    provision = 's' + provision_match[1] if provision_match else None
    if not words and not chapter:
        return []
    expr = ' OR '.join('"'+w+'"*' for w in words)
    with sqlite3.connect(path) as con:
        filters = ["p.language='en'"]
        args = []
        if chapter:
            filters.append('upper(p.chapter)=?'); args.append(chapter)
        if provision:
            filters.append('p.provision=?'); args.append(provision)
        direct = bool(chapter and (provision or not words))
        if not direct:
            if not expr:
                return []
            filters.append('provision_fts MATCH ?'); args.append(expr)
        join = '' if direct else 'JOIN provision_fts ON p.id=provision_fts.rowid'
        rows = con.execute(f'''SELECT p.chapter,p.provision,p.heading,p.path,p.version_date,
            p.official_url,p.content FROM provision p {join}
            WHERE {' AND '.join(filters)}''', args).fetchall()
    ranked = []
    for cap, section, heading, source, version, url, content in rows:
        body = set(tokens(content)); title = set(tokens(heading))
        n = len(words) or 1
        score = 5 * sum(w in body for w in words) / n + 3 * sum(w in title for w in words) / n
        if chapter:
            score += 10
        if provision:
            score += 5
        ranked.append(dict(code=f'Cap.{cap} {section}', chapter=cap, provision=section,
                           heading=heading, source=source, version_date=version, official_url=url,
                           excerpt=content[:1000], score=round(score, 6), pdf_page=None,
                           kind='legislation', page_note='XML has no PDF page number'))
    return sorted(ranked, key=lambda x: (-x['score'], x['source']))[:max(0, limit)]


def combined_search(query, limit=10):
    """One result list for existing CLI consumers; types and page semantics stay explicit."""
    if not query.strip() or limit <= 0:
        return []
    bare_law = re.fullmatch(r'\s*cap\.?\s*\d+[a-z]?\s+(?:s(?:ection)?\.?|reg(?:ulation)?\.?)\s*\d+\s*', query, re.I)
    if bare_law:
        return search_legislation(query, limit)
    docs = search(query, limit)
    laws = search_legislation(query, limit)
    # Always expose statutory candidates; do not equate a law hit with a PDF page.
    return sorted(docs + laws, key=lambda x: (-x['score'], x['source']))[:limit]
