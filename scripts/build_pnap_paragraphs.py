"""Build auditable paragraph-level PNAP JSON without guessing missing paragraph numbers.

Original PDF and page-level text remain authoritative. Every paragraph carries
a verbatim excerpt and source PDF page. Unnumbered text is preserved separately.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "indexed_text" / "PNAP"
DEST = ROOT / "search" / "pnap_paragraphs"
PAGE_RE = re.compile(r"===== PDF PAGE (\d+) =====")
# Match numbered paragraphs only at the beginning of a line; avoid dates and refs.
PARA_RE = re.compile(r"(?m)^\s{0,12}(\d{1,3})\.\s+(?=[A-Za-z(])")
SUB_RE = re.compile(r"(?m)^\s{2,16}\(([a-z])\)\s+")

def extract(path):
    raw = path.read_text(encoding="utf-8")
    chunks = PAGE_RE.split(raw)
    sections = []
    for i in range(1, len(chunks), 2):
        page = int(chunks[i])
        content = chunks[i + 1].strip()
        matches = list(PARA_RE.finditer(content))
        if not matches:
            sections.append({"id":f"page-{page}", "type":"unstructured_page",
                             "pdf_pages":[page], "text":content})
            continue
        preamble = content[:matches[0].start()].strip()
        if preamble:
            sections.append({"id":f"page-{page}-intro","type":"unstructured",
                             "pdf_pages":[page],"text":preamble})
        for j, match in enumerate(matches):
            end = matches[j+1].start() if j+1<len(matches) else len(content)
            body = content[match.start():end].strip()
            subparas = [{"label":m.group(1),"offset":m.start()}
                        for m in SUB_RE.finditer(body)]
            sections.append({"id":f"p{match.group(1)}-page-{page}",
                             "type":"numbered_paragraph",
                             "paragraph":match.group(1),
                             "pdf_pages":[page],
                             "subparagraph_markers":subparas,
                             "text":body})
    return sections

def main():
    DEST.mkdir(parents=True, exist_ok=True)
    audit = {"documents":0,"sections":0,"numbered_paragraphs":0,
             "unstructured_sections":0,"warnings":[]}
    for path in sorted(SOURCE.rglob("*.txt")):
        rel = path.relative_to(SOURCE)
        sections = extract(path)
        if not sections:
            raise ValueError(f"No PDF page markers: {path}")
        out = DEST / rel.with_suffix(".json")
        out.parent.mkdir(parents=True, exist_ok=True)
        record = {"code":path.stem,"source_text":str(path.relative_to(ROOT)),
                  "source_pdf":f"documents/PNAP/{rel.with_suffix('.pdf').as_posix()}",
                  "extraction":"heuristic; verify against PDF",
                  "sections":sections}
        out.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        audit["documents"]+=1
        audit["sections"]+=len(sections)
        audit["numbered_paragraphs"]+=sum(s["type"]=="numbered_paragraph" for s in sections)
        audit["unstructured_sections"]+=sum(s["type"]!="numbered_paragraph" for s in sections)
    (ROOT/"search"/"pnap_paragraph_audit.json").write_text(
        json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    assert audit["documents"]>=200, "Unexpected PNAP coverage drop"
    print(json.dumps(audit))

if __name__=="__main__":
    main()
