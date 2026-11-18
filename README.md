# RSE PDF Knowledge Base

Private PDF library for ChatGPT-assisted research.

## BD Codes of Practice
See [codes/README.md](codes/README.md) for foundations, RC, steel, dead and imposed
loads, wind effects, listed amendments and official explanatory material. The
[code catalogue](codes/catalog.json) records exact original PDF and page-marked
text paths; the existing full-text database includes these codes alongside PNAP.
Minor works guidelines are indexed only by official link in
[codes/minor-works/SOURCES.md](codes/minor-works/SOURCES.md); the PDFs are not in this repository.

## APSEC Discussion Forum summaries
See [APSEC archive and coverage notes](apsec/README.md) and
[provenance manifest](apsec/manifest.json) for the public HKIE collection.
Original PDFs and page-marked text share the existing full-text search index.
Historical completeness is not verified; unlisted/pre-2017 records remain gaps.

## Phone-only usage
1. Open the [documents folder](https://github.com/rsetestac001-ui/RSE/tree/main/documents).
2. Select **Add file > Upload files**, choose a text-based PDF, and commit.
3. Open the [Actions tab](https://github.com/rsetestac001-ui/RSE/actions/workflows/index-pdfs.yml) and wait for **Index PDF documents** to complete.
4. Check [index_manifest.json](https://github.com/rsetestac001-ui/RSE/blob/main/index_manifest.json) for failed or empty pages.
5. Search the extracted text in [indexed_text](https://github.com/rsetestac001-ui/RSE/tree/main/indexed_text).

## Important limitations
- This is a first-stage text extraction and audit pipeline, not yet a full hybrid semantic RAG service.
- ChatGPT's GitHub connector may not reliably search every extracted file or PDF page. Verify retrieval coverage before relying on answers.
- Extraction of tables and unusual layouts may be imperfect; blank pages are flagged.
- GitHub file size, Actions quota, and repository limits apply. Large PDFs may need an alternative storage approach.
- Keep the repository private and avoid uploading confidential material unless GitHub and connected apps meet your security requirements.
