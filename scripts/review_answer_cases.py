"""Run answer-reference retrieval diagnostics, without calling a model API.

This does not grade answer semantics. Chinese natural questions and manually
authored English keyword diagnostics are always reported separately.
"""
import contextlib
import argparse
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
    targets = [(e['path'].removeprefix('indexed_text/'), e['pdf_pages']) for e in evidence]
    rows = run['results']
    doc_hit = any(r['source'] == p for r in rows for p, _ in targets)
    page_hit = any(r['source'] == p and ((pages is None and r.get('kind') == 'legislation' and r['pdf_page'] is None)
                                       or (pages is not None and r['pdf_page'] in pages))
                   for r in rows for p, pages in targets)
    context_hit = page_hit or any(r['source'] == p and pages is not None
                                  and any(c['pdf_page'] in pages for c in r.get('context_pages', []))
                                  for r in rows for p, pages in targets)
    return dict(document_hit=doc_hit, reference_page_hit=page_hit,
                reference_context_hit=context_hit, results=[compact(r) for r in rows], error=run['error'])


def compact(row):
    fields = ['code', 'source', 'pdf_page', 'score', 'kind', 'chapter', 'provision']
    result = {k: row[k] for k in fields if k in row}
    if 'context_pages' in row:
        result['context_pages'] = [{'pdf_page': p['pdf_page']} for p in row['context_pages']]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='search/answer_retrieval_v2.json')
    args = parser.parse_args()
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
            reference_context_hits=sum(r[key]['reference_context_hit'] for r in results),
            empty_results=sum(not r[key]['results'] for r in results),
            execution_errors=sum(r[key]['error'] is not None for r in results),
        )
    report = dict(
        generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        tested_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        engine_worktree_changes=bool(subprocess.check_output(
            ['git', 'status', '--porcelain', '--', 'scripts/build_search.py', 'scripts/retrieval.py'],
            cwd=ROOT, text=True).strip()),
        index_sha256=hashlib.sha256(build_search.DB.read_bytes()).hexdigest(),
        question_dataset_sha256=hashlib.sha256((ROOT / 'tests/answer_cases_v1.json').read_bytes()).hexdigest(),
        engine_source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                              for p in ['scripts/build_search.py', 'scripts/retrieval.py']},
        method='Top 10 mixed results: one primary page per PDF document or one statutory provision. Primary location counts exact PDF page or XML provision separately by type; context coverage adds adjacent PDF pages and is not primary page accuracy. No semantic answer grading. Baseline v1 returned pages without diversity or laws, so the result units differ.',
        answer_accuracy=None, summary=summary, source_text_sha256=sources, results=results,
    )
    dest = ROOT / args.output
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
