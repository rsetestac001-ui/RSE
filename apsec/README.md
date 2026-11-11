# APSEC public archive

Original APSEC Discussion Forum summaries published publicly by the
[HKIE Structural Division](https://hkie.org.hk/st/resources/summary-of-items-discussed-in-apsec/).

- Originals: `documents/APSEC/<year>/APSEC-DF-<meeting-date>.pdf`.
- Page-marked text: `indexed_text/APSEC/<year>/APSEC-DF-<meeting-date>.txt`.
- `manifest.json`: verified PDF hashes, source URLs, page counts and meeting dates by year.
- `source_catalogue.html`: publisher catalogue snapshot for auditing discovery coverage.
- Every PDF is included in `search/pnap_fts.sqlite3` and `search/document_catalog.json`.
- Run `python scripts/apsec.py verify` after building the index to check every PDF and its FTS retrieval.

The initial public catalogue lists 39 summaries from 17 November 2017 to
14 August 2026. This is **not verified as a complete history of APSEC**.
Pre-2017 summaries, formal APSEC minutes/papers and any unlisted meetings
remain unconfirmed. No missing meetings are inferred from an assumed frequency.
HKIS archive access returned HTTP 403 during initial discovery; HKIA's
published instructions direct members to its member area. No restricted archive
was imported. BD's public committee page describes the committee but was not
found to provide a historical PDF collection.

Discussion summaries must be read as dated discussions, separating the questions
raised by convenors from **BD's responses**. They do not replace legislation,
PNAP or codes. Follow cross-references and check current provisions before use.
Cite meeting date, item number, column and 1-based PDF file page; printed page
labels may differ. Where an APSEC summary refers to an older meeting that is
absent here, disclose that gap rather than reconstructing the missing response.

The GitHub workflow checks the public catalogue weekly, retains original PDFs,
and rejects invalid downloads or disappearing catalogue records before updating
the archive. It uses Python text extraction and SQLite, with no AI API calls.
