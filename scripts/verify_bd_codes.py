"""Verify every discovered PDF is archived and every nonempty page searchable."""
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / "codes/manifest.json").read_text())
    indexed = json.loads((ROOT / "index_manifest.json").read_text())
    by_source = {r["text_file"]: r for r in indexed["documents"]}
    results = []
    with sqlite3.connect(ROOT / "search/pnap_fts.sqlite3") as db:
        assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        for item in manifest["documents"]:
            pdf = ROOT / item["source_pdf"]
            assert hashlib.sha256(pdf.read_bytes()).hexdigest() == item["sha256"], pdf
            entry = by_source[item["text_file"]]
            assert entry["status"] != "error" and entry["pages"] == item["pages"], pdf
            source = item["text_file"].removeprefix("indexed_text/")
            rows = db.execute("SELECT id,content FROM page WHERE source=? ORDER BY page_no", (source,)).fetchall()
            assert len(rows) == item["pages"], source
            for row_id, content in rows:
                import re
                words = re.findall(r"[A-Za-z]{3,}", content)
                if words:
                    assert db.execute("SELECT rowid FROM page_fts WHERE page_fts MATCH ? AND rowid=?", ('"'+words[0]+'"', row_id)).fetchone(), (source, row_id)
            results.append({"source_pdf":item["source_pdf"], "indexed_pages":len(rows), "verified":True})
        # Retain the pre-existing PNAP retrieval guarantees after adding codes.
        for code in ["ADM-16", "APP-030"]:
            assert db.execute("SELECT p.id FROM page_fts JOIN page p ON p.id=page_fts.rowid WHERE page_fts MATCH '\"ground investigation\"' AND p.code=?", (code,)).fetchone(), code
    report = {"documents":len(results), "pages":sum(r["indexed_pages"] for r in results), "errors":[], "results":results}
    (ROOT / "codes/search_audit.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k != "results"}))


if __name__ == "__main__":
    main()
