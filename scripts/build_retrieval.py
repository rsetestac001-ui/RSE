"""Generate compact, directly fetchable retrieval results for common RSE questions.

Uses the existing SQLite FTS5 index. No model API or paid service.
Each JSON file includes only ranked page excerpts and original page locations.
"""
import json
from pathlib import Path
from retrieval import search, search_legislation

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "search" / "pnap_fts.sqlite3"
DEST = ROOT / "search" / "topics"
QUERIES = {
    "scheduled-area-gi": 'scheduled area ground investigation',
    "approval-consent": 'approval consent commencement',
    "consent-renewal": 'consent renewal suspended commencement',
    "foundation": 'foundation bored pile',
    "site-formation": 'site formation submission',
    "excavation-lateral-support": 'excavation lateral support',
    "wind-effects": 'wind effects',
    "retaining-wall": 'retaining wall',
    "ground-investigation": 'ground investigation',
    "slope-stability": 'slope stability',
    "concrete-design": 'concrete design',
}

def main():
    if not DB.exists():
        raise SystemExit("Build search/pnap_fts.sqlite3 first")
    DEST.mkdir(parents=True, exist_ok=True)
    for slug, query in QUERIES.items():
        results = [dict(row, source='indexed_text/'+row['source']) for row in search(query,15)]
        (DEST / (slug+'.json')).write_text(json.dumps({
            'query':query,'results':results,'legislation':search_legislation(query,10),
            'note':'One best page per document. XML results have no PDF page number. Follow the original text, PNAP cross-references and amendment links; rankings are not answers.',
        },ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(f'{slug}: {len(results)} documents')
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
