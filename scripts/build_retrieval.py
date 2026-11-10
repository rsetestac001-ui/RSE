"""Generate compact, directly fetchable retrieval results for common RSE questions.

Uses the existing SQLite FTS5 index. No model API or paid service.
Each JSON file includes only ranked page excerpts and original page locations.
"""
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "search" / "pnap_fts.sqlite3"
DEST = ROOT / "search" / "topics"
QUERIES = {
    "scheduled-area-gi": '"ground investigation" OR "scheduled area" OR "scheduled areas"',
    "approval-consent": '"approval and consent" OR "consent to commence" OR "commencement of works"',
    "consent-renewal": '"renewal of consent" OR "consent" OR "validity"',
    "foundation": '"foundation" OR "piling"',
    "site-formation": '"site formation" OR "excavation"',
}

def main():
    if not DB.exists():
        raise SystemExit("Build search/pnap_fts.sqlite3 first")
    DEST.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB) as db:
        for slug, expression in QUERIES.items():
            hits = db.execute(
                """SELECT p.code,p.source,p.page_no,
                          snippet(page_fts,1,'[',']',' … ',22),
                          bm25(page_fts)
                   FROM page_fts JOIN page p ON p.id=page_fts.rowid
                   WHERE page_fts MATCH ? ORDER BY bm25(page_fts) LIMIT 15""",
                (expression,),
            ).fetchall()
            results = [{"code":code, "source":"indexed_text/"+source,
                        "pdf_page":page, "excerpt":excerpt}
                       for code,source,page,excerpt,_ in hits]
            (DEST / (slug+".json")).write_text(
                json.dumps({"query":expression, "results":results},
                           ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
            print(f"{slug}: {len(results)} pages")
    # Direct document lookup is more reliable than GitHub code search.
    manifest = json.loads((ROOT/"index_manifest.json").read_text(encoding="utf-8"))
    catalog = {}
    for doc in manifest["documents"]:
        name = Path(doc["source"]).stem.upper()
        catalog[name] = {"path":doc["text_file"], "pages":doc.get("pages"),
                         "source_pdf":doc["source"]}
        # Normalize APP-030 and APP-30 to the same file.
        import re
        match = re.fullmatch(r"([A-Z]+)-0*(\d+)", name)
        if match:
            catalog[f"{match.group(1)}-{int(match.group(2))}"] = catalog[name]
    (ROOT/"search"/"document_catalog.json").write_text(
        json.dumps(catalog,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    assert catalog["ADM-16"]["path"].endswith("ADM-16.txt")
    assert catalog["APP-30"]["path"].endswith("APP-030.txt")

if __name__ == "__main__":
    main()
