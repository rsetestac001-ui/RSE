# GEO technical reference archive

`manifest.json` records official CEDD source URLs, catalogue row context (including cancellation/replacement notices), linked editions/amendments, PDF hashes and page counts. `search_audit.json` verifies hashes and per-file FTS page coverage.

Scope: Geoguides, GCO/GEO Publications and GEO Technical Guidance Notes, including the TGN master list. Other GEO publication series, including GEO Reports and Geospecs, are not included. Unavailable/cancelled entries remain visible in catalogue rows; inclusion never implies current applicability.

PDFs: `documents/GEO/`; text with physical PDF page markers: `indexed_text/GEO/`; shared FTS database: `search/pnap_fts.sqlite3`. Image-only/empty pages are flagged for visual review.

Run `python scripts/geo.py`, the existing index/search builders, then `python scripts/verify_geo.py`. The GEO workflow runs on relevant pushes, manually and weekly.
