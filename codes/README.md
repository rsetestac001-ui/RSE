# Official BD Codes of Practice

Five requested families: foundations, structural concrete (RC), structural steel,
dead and imposed loads, and wind effects. Original English PDFs, all PDF amendments
listed alongside them on the official BD catalogue, and the official steel/wind
explanatory publications are archived separately under `documents/BD_CODES/`.

`manifest.json` records the official title/edition, source URL, SHA-256, retrieval
date, PDF page count, empty pages and documents to read together. `catalog.json`
groups exact PDF and extracted-text paths by family. Check this manifest for the
current discovered set; older retained files are not proof of current applicability.
The PDFs remain unmodified. Amendments are **not** silently merged into the main code.

`indexed_text/BD_CODES/` contains the full extracted text with 1-based PDF file page
markers. These differ from printed page numbers. Figures, equations and tables must
be checked against the original PDF before relying on a design conclusion. Text
extraction is not OCR and cannot guarantee every diagram or formula is searchable.

The existing `search/pnap_fts.sqlite3` indexes both PNAP and BD codes (its historical
filename is retained). `search/document_catalog.json` supports direct document lookup.
For code-only SQL results filter `page.source LIKE 'BD_CODES/%'`. The database is
local, not a remotely hosted search API. `codes/search_audit.json` verifies PDF hashes,
page coverage, per-page FTS retrieval and retention of the ADM-16/APP-30 GI matches.

The **Download and index official BD codes** workflow refreshes on Sunday at 22:30 UTC
(Monday 06:30 Hong Kong), on relevant code changes, or manual dispatch. It runs the
download, PDF extraction and search build in one job, since bot commits do not trigger
other workflows automatically. Discovery fails if any of the five families disappears.

Before a technical answer, read the code, its amendments and relevant PNAP original
text/cross-references. Explanatory material has a different role from the code itself.
The source catalogue is https://www.bd.gov.hk/en/resources/codes-and-references/codes-and-design-manuals/index.html.
