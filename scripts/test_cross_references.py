"""Cross-source retrieval smoke tests. Candidate labels are NOT verified gold answers."""
import json,sqlite3,re,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument("--strict",action="store_true");a=p.parse_args()
 db=ROOT/"search/pnap_fts.sqlite3"
 cases=json.loads((ROOT/"tests/search_cases.json").read_text())
 if not db.exists():raise SystemExit("Build search index first")
 out=[];positive=0;found=0
 with sqlite3.connect(db) as con:
  for c in cases:
   words=re.findall(r"[\w]+",c["query"].lower())
   expr=" OR ".join('"'+w+'"' for w in words if len(w)>2)
   rows=con.execute("""SELECT p.code,p.source,p.page_no,bm25(page_fts) FROM page_fts JOIN page p ON p.id=page_fts.rowid WHERE page_fts MATCH ? ORDER BY bm25(page_fts) LIMIT 10""",(expr,)).fetchall() if expr else []
   codes={r[0].upper() for r in rows}
   expected=c["expected_codes"];hits=[x for x in expected if x.upper() in codes]
   positive+=len(expected);found+=len(hits)
   out.append({"id":c["id"],"query":c["query"],"review_status":c["review_status"],"candidate_hits":hits,"candidate_misses":[x for x in expected if x not in hits],"top10":[{"code":r[0],"source":r[1],"pdf_page":r[2]} for r in rows]})
 report={"warning":"Candidate labels are unverified. Candidate recall is diagnostic, NOT validated search accuracy. Web comparison requires independent evidence review.","cases":len(cases),"candidate_recall_at_10":round(found/positive,4) if positive else None,"candidate_labels":positive,"results":out}
 dest=ROOT/"search/qa_report.json";dest.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
 print(json.dumps({"cases":len(cases),"candidate_recall_at_10":report["candidate_recall_at_10"]}))
 if a.strict and any(x["candidate_misses"] for x in out):raise SystemExit("Candidate misses detected")
if __name__=="__main__":main()
