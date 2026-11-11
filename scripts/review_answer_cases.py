"""Run answer-reference retrieval diagnostics, without calling a model API.

This does not grade answer semantics. Chinese natural questions and manually
authored English keyword diagnostics are always reported separately.
"""
import contextlib
import datetime
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_search


def retrieve(query):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            build_search.search(query, 10)
        return {'results': json.loads(buf.getvalue()), 'error': None}
    except (Exception, SystemExit) as exc:
        return {'results': [], 'error': str(exc)}


def score(run, evidence):
    # A target page existing/matching is an address diagnostic, not entailment.
    targets = [(e['path'].removeprefix('indexed_text/'), e['pdf_pages'])
               for e in evidence if e['path'].startswith('indexed_text/')]
    rows = run['results']
    doc_hit = any(r['source'] == p for r in rows for p, _ in targets)
    page_hit = any(r['source'] == p and r['pdf_page'] in pages
                   for r in rows for p, pages in targets)
    for r in rows:
        r.pop('excerpt', None)
    return dict(document_hit=doc_hit, reference_page_hit=page_hit,
                results=rows, error=run['error'])


def main():
    data = json.loads((ROOT / 'tests/answer_cases_v1.json').read_text())
    cases = data['cases']
    if len(cases) != 100 or len({c['id'] for c in cases}) != 100:
        raise SystemExit('Expected exactly 100 distinct IDs')
    if len({c['question'] for c in cases}) != 100:
        raise SystemExit('Duplicate natural questions')
    results = []
    sources = {}
    for c in cases:
        for e in c['evidence']:
            path = ROOT / e['path']
            raw = path.read_bytes()
            sources[e['path']] = hashlib.sha256(raw).hexdigest()
            if e['pdf_pages'] is not None:
                available = {int(x) for x in re.findall(
                    r'===== PDF PAGE (\d+) =====', raw.decode())}
                if not set(e['pdf_pages']) <= available:
                    raise SystemExit('Missing reference page: ' + c['id'])
        results.append(dict(
            id=c['id'], question=c['question'],
            natural_question=score(retrieve(c['question']), c['evidence']),
            english_diagnostic=score(retrieve(c['diagnostic_english_query']), c['evidence']),
            answer_correctness=None,
        ))
    summary = {}
    for key in ['natural_question', 'english_diagnostic']:
        summary[key] = dict(
            cases=100,
            document_hits=sum(r[key]['document_hit'] for r in results),
            reference_page_hits=sum(r[key]['reference_page_hit'] for r in results),
            empty_results=sum(not r[key]['results'] for r in results),
            execution_errors=sum(r[key]['error'] is not None for r in results),
        )
    report = dict(
        generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        tested_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        index_sha256=hashlib.sha256(build_search.DB.read_bytes()).hexdigest(),
        question_dataset_sha256=hashlib.sha256((ROOT / 'tests/answer_cases_v1.json').read_bytes()).hexdigest(),
        method='Current page-level main search, top 10 pages. Exact reference-path and page-address diagnostic only. Chinese natural questions and English keyword diagnostics are separate; no semantic grading, no law index in this search function.',
        answer_accuracy=None, summary=summary, source_text_sha256=sources, results=results,
    )
    dest = ROOT / 'search/answer_retrieval_v1.json'
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
