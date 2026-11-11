"""Audit every original query; separate retrieval, evidence provenance and answer validity."""
import argparse
import hashlib
import json
import re
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from retrieval import search, search_legislation

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def legacy_search(con, query):
    words = re.findall(r'[\w]+', query.lower())
    expression = ' OR '.join('"'+w+'"' for w in words if len(w)>2)
    rows = con.execute('''SELECT p.code,p.source,p.page_no FROM page_fts
        JOIN page p ON p.id=page_fts.rowid WHERE page_fts MATCH ?
        ORDER BY bm25(page_fts) LIMIT 10''', (expression,)).fetchall() if expression else []
    return [dict(zip(('code','source','pdf_page'),r)) for r in rows]


def document_id(row):
    return row['source']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strict', action='store_true', help='Fail on retrieval regression or evidence integrity failures; never certify answer accuracy.')
    args = parser.parse_args()
    cases = json.loads((ROOT/'tests/search_cases.json').read_text())
    topics = json.loads((ROOT/'tests/topic_reviews.json').read_text())['topics']
    pdf_check = json.loads((ROOT/'search/official_source_check.json').read_text())
    parity = {x['source_pdf']:x for x in pdf_check['results']}
    legal_path = ROOT/'search/official_legislation_check.json'
    legal_check = json.loads(legal_path.read_text()) if legal_path.exists() else {'results':[]}
    legal_parity = {x['chapter']:x['status'] for x in legal_check['results']}
    original_baseline = ROOT/'search/qa_baseline.json'
    saved = json.loads(original_baseline.read_text()) if original_baseline.exists() else None
    saved_rows = {x['id']:x['top10'] for x in saved['results']} if saved else {}
    seen = {}
    cache = {}
    out = []
    integrity_errors = []
    baseline_hits = new_hits = labels = 0
    reference_found = reference_total = 0
    bundle_found = 0
    legal_found = legal_total = 0
    with sqlite3.connect(ROOT/'search/pnap_fts.sqlite3') as con:
        indexed_pages = {(s,n) for s,n in con.execute('SELECT source,page_no FROM page')}
        for position, case in enumerate(cases):
            topic = topics[position % 10]
            assert case['query'].startswith(topic['base_query']), (case['id'], topic['topic_id'])
            query = case['query']
            if query not in cache:
                cache[query] = (search(query,10),search_legislation(query,10))
            ranked, laws = cache[query]
            previous = saved_rows.get(case['id']) or legacy_search(con,query)
            old_codes = {r['code'].upper() for r in previous}
            new_codes = {r['code'].upper() for r in ranked}
            expected = case['expected_codes']
            old_hits = [x for x in expected if x.upper() in old_codes]
            hits = [x for x in expected if x.upper() in new_codes]
            labels += len(expected)
            baseline_hits += len(old_hits)
            new_hits += len(hits)
            refs = topic['evidence']
            targets = {x['source'] for x in refs}
            sources = {r['source'] for r in ranked}
            bundle = set(sources)
            url_sources = {x['official_url']:x['source_pdf'].removeprefix('documents/').removesuffix('.pdf')+'.txt' for x in parity.values()}
            for row in ranked:
                bundle.update(row.get('cross_references',[]))
                bundle.update(url_sources[u] for u in row.get('must_read_with',[]) if u in url_sources)
            reference_found += len(targets & sources)
            reference_total += len(targets)
            bundle_found += len(targets & bundle)
            statutory = topic.get('statutory_evidence',[])
            statutory_targets = {r['source'] for r in statutory}
            statutory_hits = statutory_targets & {r['source'] for r in laws}
            legal_found += len(statutory_hits)
            legal_total += len(statutory_targets)
            evidence = []
            for ref in refs:
                pdf = 'documents/'+ref['source'].removesuffix('.txt')+'.pdf'
                check = parity.get(pdf,{})
                for number in ref['pdf_pages']:
                    if (ref['source'],number) not in indexed_pages:
                        integrity_errors.append({'case':case['id'],'source':ref['source'],'pdf_page':number,'error':'Cited page missing from index'})
                evidence.append(dict(ref,official_url=check.get('official_url'),
                                     official_parity=check.get('status','not_checked'),
                                     github_url='https://github.com/rsetestac001-ui/RSE/blob/feature/cross-search-qa/'+pdf,
                                     checked_at=check.get('checked_at')))
            for row in ranked:
                if (row['source'],row['pdf_page']) not in indexed_pages:
                    integrity_errors.append({'case':case['id'],'error':'Result location missing from index'})
            duplicate_of = seen.get(query)
            seen.setdefault(query,case['id'])
            result = {
                'id':case['id'],'query':query,'duplicate_of':duplicate_of,
                'topic_id':topic['topic_id'],'original_category':case['category'],
                'review_status':'source_reviewed_not_answer_gold',
                'original_label_assessment':topic['original_label_assessment'],
                'review_note':topic['review_note'],
                'baseline_candidate_hits':old_hits,'candidate_hits':hits,
                'candidate_misses':[x for x in expected if x not in hits],
                'reference_targets':sorted(targets),'reference_hits':sorted(targets & sources),
                'reference_misses':sorted(targets-sources),
                'reference_bundle_hits':sorted(targets & bundle),
                'reference_bundle_misses':sorted(targets-bundle),
                'evidence':evidence,
                'statutory_evidence':[dict(r,official_parity=legal_parity.get(r['chapter'],'not_checked')) for r in statutory],
                'statutory_hits':sorted(statutory_hits),
                'baseline_top10':previous,'top10':ranked,'legislation_top10':laws,
                'answer_accuracy':None,
                'answer_validation_note':'The original row has no proposed answer, section-level gold answer or independent adjudication. Source review and retrieval testing cannot score an absent answer.',
            }
            out.append(result)
            if (position+1)%10==0:
                print(f"Audited {position+1}/{len(cases)}",flush=True)
    def ratio(n,d):
        return round(n/d,4) if d else None
    # Unique-query metrics prevent repeated rows from silently inflating the evidence count.
    unique = [r for r in out if r['duplicate_of'] is None]
    unique_targets = sum(len(r['reference_targets']) for r in unique)
    unique_hits = sum(len(r['reference_hits']) for r in unique)
    baseline_recall = ratio(baseline_hits,labels)
    new_recall = ratio(new_hits,labels)
    report = {
        'checked_at':datetime.now(timezone.utc).isoformat(),
        'status':'all_original_rows_retrieval_and_source_reviewed_answer_validation_unavailable',
        'method':'All 100 original rows evaluated individually. Ten repeated topic families share cited source review and independently fetched official documents. 60 unique query strings are not 100 independent engineering questions. Official web discovery is topic-level, not 100 independent web searches.',
        'corpus_note':'Baseline predates addition of the missing Geotechnical Manual for Slopes. Changes include ranking fixes and that source addition.',
        'cases':len(cases),'unique_queries':len(unique),'duplicate_rows':len(cases)-len(unique),
        'original_unlabelled_rows':sum(not c['expected_codes'] for c in cases),
        'original_label_review':dict(Counter(r['original_label_assessment'] for r in out)),
        'baseline_candidate_recall_at_10':baseline_recall,
        'candidate_recall_at_10':new_recall,'candidate_labels':labels,
        'reviewed_reference_recall_at_10':ratio(reference_found,reference_total),
        'reviewed_reference_bundle_coverage':ratio(bundle_found,reference_total),
        'unique_query_reviewed_reference_recall_at_10':ratio(unique_hits,unique_targets),
        'statutory_reference_recall_at_10':ratio(legal_found,legal_total),
        'metric_limits':'Reference targets are reviewed relevant documents, not an exhaustive gold relevance set. Bundle coverage includes explicitly returned PNAP cross-references and code amendment links and is not top10 recall. Candidate labels remain diagnostic. PDF location checks only prove index address existence, not that the returned page answers the question.',
        'precision_at_10':None,'answer_accuracy':None,'semantic_page_accuracy':None,
        'official_pdf_parity':pdf_check['summary'],'official_xml_parity':legal_check.get('summary'),
        'evidence_location_errors':integrity_errors,
        'inputs_sha256':{p:digest(ROOT/p) for p in ['tests/search_cases.json','tests/topic_reviews.json','search/pnap_fts.sqlite3','search/legislation_fts.sqlite3']},
        'results':out,
    }
    (ROOT/'search/qa_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('results','inputs_sha256')},ensure_ascii=False))
    if args.strict and (integrity_errors or new_recall is None or new_recall<baseline_recall or any(x['status']!='byte_identical' for x in parity.values()) or legal_check.get('error') or len(legal_parity)!=5 or any(status!='byte_identical' for status in legal_parity.values())):
        raise SystemExit('QA regression or evidence integrity failure')


if __name__=='__main__':
    main()
