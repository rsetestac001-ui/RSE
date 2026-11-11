"""Build a page-level SQLite FTS5 index from extracted PNAP text.

Usage:
  python scripts/build_search.py build
  python scripts/build_search.py search "scheduled area GI" --limit 20
  python scripts/build_search.py audit
No external packages or AI API required.
"""
import argparse
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = ROOT / "indexed_text"
DB = ROOT / "search" / "pnap_fts.sqlite3"
REPORT = ROOT / "search" / "search_audit.json"
PAGE = re.compile(r"===== PDF PAGE (\d+) =====")
def pages(raw):
    pieces = PAGE.split(raw)
    for i in range(1, len(pieces), 2):
        body = pieces[i+1].strip()
        yield int(pieces[i]), body

def build():
    DB.parent.mkdir(parents=True, exist_ok=True)
    tmp = DB.with_suffix(".tmp")
    tmp.unlink(missing_ok=True)
    conn = sqlite3.connect(tmp)
    conn.execute("CREATE TABLE page (id INTEGER PRIMARY KEY, code TEXT NOT NULL, source TEXT NOT NULL, page_no INTEGER NOT NULL, content TEXT NOT NULL)")
    conn.execute("CREATE VIRTUAL TABLE page_fts USING fts5(code, content, content='page', content_rowid='id', tokenize='unicode61')")
    counts = {"documents":0,"pages":0,"empty_pages":[],"errors":[]}
    for path in sorted(TEXT.rglob("*.txt")):
        rel = path.relative_to(TEXT)
        try:
            data = path.read_text(encoding="utf-8")
            found = list(pages(data))
            if not found:
                counts["errors"].append({"file":str(rel),"reason":"No PDF page markers"})
                continue
            counts["documents"] += 1
            for number, content in found:
                code = path.stem
                conn.execute("INSERT INTO page(code,source,page_no,content) VALUES(?,?,?,?)",
                             (code,rel.as_posix(),number,content))
                counts["pages"] += 1
                if not content:
                    counts["empty_pages"].append({"file":str(rel),"page":number})
        except Exception as exc:
            counts["errors"].append({"file":str(rel),"reason":str(exc)})
    conn.execute("INSERT INTO page_fts(page_fts) VALUES('rebuild')")
    conn.commit()
    conn.close()
    manifest = ROOT / "index_manifest.json"
    if manifest.exists():
        m = json.loads(manifest.read_text(encoding="utf-8"))
        counts["manifest_documents"] = m.get("total_pdfs")
        counts["manifest_failed"] = m.get("failed")
        counts["manifest_needs_review"] = m.get("needs_review")
        if counts["documents"] != m.get("indexed"):
            counts["errors"].append({"reason":"Indexed document count does not match manifest",
                                     "expected":m.get("indexed"),"actual":counts["documents"]})
    REPORT.write_text(json.dumps(counts,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    if counts["errors"]:
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"Search index validation failed: {counts['errors'][:5]}")
    tmp.replace(DB)
    print(json.dumps(counts,ensure_ascii=False))

def search(q, limit):
    if not DB.exists():
        raise SystemExit("Missing database. Run build first.")
    from retrieval import combined_search
    print(json.dumps(combined_search(q, limit), indent=2, ensure_ascii=False))

def audit():
    if not REPORT.exists():
        raise SystemExit("Missing audit report. Run build first.")
    print(REPORT.read_text(encoding="utf-8"))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("command",choices=["build","search","audit"])
    ap.add_argument("query",nargs="?")
    ap.add_argument("--limit",type=int,default=20)
    args=ap.parse_args()
    if args.command=="build": build()
    elif args.command=="audit": audit()
    elif args.query: search(args.query,max(1,min(args.limit,100)))
    else: ap.error("Search requires a query")
