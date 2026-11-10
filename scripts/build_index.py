"""Extract text from PDFs with page markers and an auditable manifest. No API calls."""
from pathlib import Path
import hashlib, json, re
import fitz

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "documents"
OUT = ROOT / "indexed_text"
MANIFEST = ROOT / "index_manifest.json"

def main():
    OUT.mkdir(exist_ok=True)
    records = []
    expected = set()
    for pdf in sorted(SOURCE.rglob("*")) if SOURCE.exists() else []:
        if not pdf.is_file() or pdf.suffix.lower() != ".pdf":
            continue
        rel = pdf.relative_to(SOURCE)
        dest = (OUT / rel).with_suffix(".txt")
        expected.add(dest.resolve())
        entry = {"source": rel.as_posix(), "text_file": dest.relative_to(ROOT).as_posix(),
                 "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), "status": "ok"}
        try:
            doc = fitz.open(pdf)
            entry["pages"] = len(doc)
            parts = []
            empty = []
            for i, page in enumerate(doc, 1):
                content = page.get_text(sort=True).strip()
                if not content:
                    empty.append(i)
                parts.append(f"\n\n===== PDF PAGE {i} =====\n{content}\n")
            entry["empty_pages"] = empty
            entry["characters"] = sum(len(x) for x in parts)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text("".join(parts), encoding="utf-8")
            doc.close()
            if empty:
                entry["status"] = "review_empty_pages"
        except Exception as exc:
            entry["status"] = "error"
            entry["error"] = str(exc)
            dest.unlink(missing_ok=True)
        records.append(entry)
    for old in OUT.rglob("*.txt"):
        if old.resolve() not in expected:
            old.unlink()
    summary = {"total_pdfs": len(records),
               "indexed": sum(r["status"] != "error" for r in records),
               "failed": sum(r["status"] == "error" for r in records),
               "needs_review": sum(r["status"] == "review_empty_pages" for r in records),
               "documents": records}
    MANIFEST.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k != "documents"}))
    if summary["failed"]:
        raise SystemExit("Some PDFs could not be indexed; check index_manifest.json")

if __name__ == "__main__":
    main()
