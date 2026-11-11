"""Generate compact, directly fetchable retrieval results for common RSE questions.

Uses the existing SQLite FTS5 index. No model API or paid service.
Each JSON file includes only ranked page excerpts and original page locations.
"""
import json
from retrieval import combined_search
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "search" / "pnap_fts.sqlite3"
DEST = ROOT / "search" / "topics"
QUERIES = {
    "scheduled-area-gi": "scheduled area GI",
    "approval-consent": "approval consent commencement",
    "consent-renewal": "consent renewal suspended months",
    "foundation": "foundation piling",
    "site-formation": "site formation submission",
}

def main():
    if not DB.exists():
        raise SystemExit("Build search/pnap_fts.sqlite3 first")
    DEST.mkdir(parents=True, exist_ok=True)
    for slug, query in QUERIES.items():
        results = combined_search(query, 15)
        for result in results:
            if result['kind'] == 'pdf':
                result['source'] = 'indexed_text/' + result['source']
        (DEST / (slug + '.json')).write_text(
            json.dumps({'query': query, 'results': results,
                        'note': 'Ranked evidence only. Read source, scope and amendments; XML has no PDF page.'},
                       ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'{slug}: {len(results)} document/provision results')
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
