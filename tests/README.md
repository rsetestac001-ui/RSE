# Cross-source search QA

The original 100 rows are preserved in `search_cases.json`, including their IDs.
They contain **60 distinct query strings, 40 duplicate rows and 60 rows without
candidate labels**. They are keyword searches, not 100 independent engineering
questions with proposed answers. Their rotating `category` field is not reliable
source classification. Do not treat this dataset as a validated answer benchmark.

## What was actually checked

- Every original row has an individual result in `search/qa_report.json`.
- `topic_reviews.json` documents source reading, scope corrections, physical PDF
  pages and statutory references for the ten repeated topic families.
- `official_web_review.json` records twelve actual topic-level official search
  queries and resulting BD/CEDD/HKIE URLs. Repeated cases share that evidence;
  there were not 100 independent official web searches.
- `official_sources.json` identifies independently downloaded PDFs.
  `search/official_source_check.json` records live SHA-256 comparisons.
- `search/official_legislation_check.json` compares the five English XML files
  with the current official DOJ archive, normalizing ZIP path separators.
- The originally missing Geotechnical Manual for Slopes was added with 303
  physical PDF pages and 287 hash-bound OCR transcriptions. OCR remains
  unverified transcription; figures, tables and numerical rules need PDF review.

## Metrics and limits

`candidate_recall_at_10` retains the original unverified labels for a comparable
before/after diagnostic. `reviewed_reference_recall_at_10` uses explicitly listed
related document targets, without claiming that the relevance list is exhaustive.
One best page per document is returned by the new search, whereas the old search
returned pages and could fill many slots from one document. The baseline predates
addition of the slope manual, so this is a system before/after comparison, not an
isolated ranking experiment. Unique-query metrics are reported separately.

`reviewed_reference_bundle_coverage` also counts returned amendment URLs and PNAP
cross-reference paths; it must not be presented as top-ten recall.

**Precision, correctness of a generated answer, correctness of its supporting
passage and professional/legal applicability are not scored.** Those metrics are
null. A page address existing in the index is not proof that the page answers the
question. No submitted answers exist in the original dataset to grade.

## Reproduce

```sh
python scripts/materialize_qa_sources.py
python scripts/build_search.py build
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/test_cross_references.py --strict
python scripts/build_retrieval.py
python scripts/verify_geo.py
python scripts/verify_bd_codes.py
```

These local steps use no model API. Snapshot materialization only downloads missing
sources and checks their saved review hashes; it does not claim a fresh web check.
For an independent live refresh, run `check_official_sources.py` and
`check_official_legislation.py` deliberately; the latter downloads the official
English legislation ZIP (about 236 MB at this check).

The QA workflow runs on relevant pushes and can be dispatched manually. It checks
sources, runs regression checks, rebuilds indexes and directly fetchable topics,
retains a report artifact and commits generated results back to the triggering
branch. It never labels a passing job as validated answer accuracy.

## Work required for answer-level validation

Replace keyword variations with independent real questions, supply complete
reference answers, and adjudicate each numerical condition, comparison operator,
AND/OR relationship, scope, exception, source version and supporting PDF page.
Keep errors as regression cases and review all ten ranked results before claiming
Precision@10. A successful workflow cannot substitute for this review.
