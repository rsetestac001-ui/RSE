# RSE retrieval guide for ChatGPT

## Repository retrieval status (2026-11-11)
- `search/pnap_fts.sqlite3` and `search/search_audit.json` exist on `main`.
- Audit: 366 indexed documents, 11,575 PDF pages, 0 indexing errors (QA branch after adding GMS; see current audit for review flags).
- GitHub connector reports `is_code_search_indexed=false`; GitHub code search returning no results **does not mean the source PDF is absent**.
- SQLite FTS5 is a database file, **not** an HTTP search API. The ChatGPT GitHub connector cannot execute SQL against it directly.

## Reliable document retrieval via GitHub connector
1. Fetch `index_manifest.json` from `main`.
2. Find the document's `source` or `text_file` using normalized identifiers: e.g. APP-30 may be `APP-030`.
3. Fetch the exact `text_file` path with GitHub's `fetch_file` operation; do **not** depend on code search.
4. Cite the document identifier, paragraph, and explicit `===== PDF PAGE N =====` marker. Clearly distinguish evidence from interpretation.
5. If the source is absent from the manifest, report that it is absent; do not guess paths or page numbers.

## Verified examples
- ADM-16: `indexed_text/PNAP/ADM/ADM-16.txt` — page 1, paragraph 1 (GI in Scheduled Areas requires approval and consent).
- APP-30: `indexed_text/PNAP/APP/APP-030.txt` — page 1, paragraph 3 (GI in Scheduled Area No. 1).

## Full-text search
For BD Codes of Practice, fetch `codes/manifest.json` and `codes/catalog.json`
first. These group foundations, concrete (RC), steel, dead/imposed loads and wind
with the official listed amendments and explanatory PDFs. Read the amendments as
well as the main code and relevant PNAP. Text is under `indexed_text/BD_CODES/`;
original PDFs are under `documents/BD_CODES/`. PDF markers are file pages, not
printed page labels. Check formulae/figures/tables against the original PDF.
The historical `pnap_fts.sqlite3` filename is retained for the combined PDF index.

The existing GitHub Actions workflow `.github/workflows/build-search.yml` runs:
`python scripts/build_search.py search "scheduled area GI" --limit 10`
The SQLite index can be queried on a machine running the repository, but it is **not remotely callable by ChatGPT**. A separate authenticated or public read-only HTTP service is needed for arbitrary live queries. Do not claim such a service exists until deployed and tested.

## Official legislation (separate provision index)
Fetch `legislation/manifest.json` for snapshot/version metadata and `legislation/catalog.json` for exact provision paths. The five chapters are 123, 123A, 123C, 123F and 123Q; languages are `en` and `zh-Hant`. For example, `legislation/provisions/cap123/en/s20.json` contains the whole section and its numbered subsections. Read the complete provision, not only a search excerpt, before stating conditions or deadlines.

Full original XML and statutory image assets are under `legislation/raw/`; complete extracted text is under `legislation/text/`. `search/legislation_fts.sqlite3` and `search/legislation_audit.json` are maintained by the official legislation workflow. Compact results live under `search/legislation_topics/`. See `legislation/SOURCES.md` for source attribution, update cadence, CLI usage and limitations.

## Cross-source QA and amended search
The search CLI now returns `documents` (one best page per document) and
`legislation` separately. It expands GI/ELS/SF and selected Chinese terms, ranks
titles, identifies earlier members of known handbook/Geoguide series, and returns
PNAP cross-reference paths and code amendment URLs. Earlier editions are retained;
their acceptability must be checked against the applicable PNAP.

`search/topics/` includes eleven directly fetchable topics. Their `results` field
retains the indexed text path; `legislation` includes provision paths and null PDF
page numbers. These compact files use the same ranking code as the QA test.

See `tests/README.md` and `search/qa_review.md` for the actual 100-row audit and
limitations. The old rows are not 100 distinct engineering questions. Search recall,
byte-identical source copies, and a passing CI job do not prove answer accuracy.
The GEO collection now also includes the Geotechnical Manual for Slopes, with
its original PDF, hash-bound OCR and saved links to later TGN updates.
