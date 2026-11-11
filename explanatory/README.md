# Explanatory handbooks and notes

Official public sources: HKIE Structural Division technical publications and BD codes catalogue. `catalog.json` is a compact inventory; `manifest.json` includes provenance, code basis, hashes and physical PDF page counts. HKIE original PDFs are in `documents/HKIE/`; existing BD explanations remain under `documents/BD_CODES/` to avoid duplication. Text in `indexed_text/` retains physical PDF page markers; `search_audit.json` verifies coverage and retrieval.

Scope: nine publicly linked HKIE handbooks (concrete 2004/2013, foundations 2004/2017, steel 2011, wind 2004/2019, demolition 2004, precast based on the 2003 code) and BD steel explanatory materials, wind explanatory notes and amendments. Catalogue presence does not establish current applicability. Match the handbook's code basis to the actual code edition, amendments and PNAP; handbook opinions and examples do not replace statutory or BD requirements.

Scanned HKIE pages use hash-bound Tesseract OCR at 200 dpi, clearly labelled as unverified transcription. Numbers, equations, drawings and tables must be checked against the PDF. Blank pages may remain empty.

The workflow saves originals and OCR results, then rebuilds the shared FTS index and verifies every document, page coverage and existing ADM-16/APP-30 GI retrieval. It runs weekly and on relevant changes, without model API calls.
