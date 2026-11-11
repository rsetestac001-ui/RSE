#!/usr/bin/env python3
"""Build a small, evidence-based project overview. Python standard library only."""
import argparse,datetime,json,pathlib,subprocess

def build(root,tree=None):
 def read(p):
  try:return json.loads((root/p).read_text())
  except (OSError,ValueError):return {}
 if tree:
  entries=tree['tree'];sha=tree['sha']
 else:
  entries=[{'path':p.relative_to(root).as_posix(),'type':'blob','size':p.stat().st_size} for p in root.rglob('*') if p.is_file() and '.git' not in p.parts]
  try:sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
  except (OSError,subprocess.CalledProcessError):sha=None
 files=[e for e in entries if e.get('type')=='blob']; paths={e['path'] for e in files}
 def count(prefix,suffix):return sum(e['path'].startswith(prefix) and e['path'].lower().endswith(suffix) for e in files)
 audit=read('search/search_audit.json');para=read('search/pnap_paragraph_audit.json');law=read('search/legislation_audit.json');manifest=read('index_manifest.json')
 specs=[('PNAP','PNAP 實務作業備考','documents/PNAP/','indexed_text/PNAP/','ADM、APP、ADV；按段落及 PDF 頁碼檢索。','search/pnap_paragraph_audit.json'),('BD_CODES','BD 規範與解說','documents/BD_CODES/','indexed_text/BD_CODES/','Foundation、RC、steel、wind、dead and imposed loads；主文、修訂同解說須一齊核對。','codes/search_audit.json'),('GEOGUIDES','GEO Geoguides','documents/GEO/GEOGUIDES/','indexed_text/GEO/GEOGUIDES/','岩土工程指南及可取得嘅修訂文件。','geo/search_audit.json'),('GEO_PUBLICATIONS','GEO Publications','documents/GEO/GEO_PUBLICATIONS/','indexed_text/GEO/GEO_PUBLICATIONS/','已收錄公開出版物；唔代表所有 GEO 系列或歷史版本已齊。','geo/search_audit.json'),('TGN','GEO 技術指引 TGN','documents/GEO/TGN/','indexed_text/GEO/TGN/','須核對 master list、版本及取消／取代狀態。','geo/search_audit.json'),('HKIE','HKIE 解說手冊','documents/HKIE/','indexed_text/HKIE/','解釋 Code 同設計例子；唔應當成法例或取代 BD Code。','explanatory/search_audit.json'),('APSEC','APSEC 討論摘要','documents/APSEC/','indexed_text/APSEC/','公開 Discussion Forum 收藏；問題同 BD 回應要分清，歷年覆蓋仍須核實。','apsec/search_audit.json')]
 sources=[]
 for id,title,pdf,text,description,evidence in specs:
  sources.append(dict(id=id,title=title,pdfs=count(pdf,'.pdf'),texts=count(text,'.txt'),path=pdf,description=description,evidence=evidence,granularity='段落 + PDF 頁碼' if id=='PNAP' else 'PDF 頁面',status='有檔案' if count(pdf,'.pdf') else '尚未收錄'))
 lm=read('legislation/manifest.json');chapters=sorted({d.get('chapter') for d in lm.get('documents',[]) if d.get('chapter')})
 sources.append(dict(id='LAW',title='Cap.123 系列法例',pdfs=None,texts=count('legislation/provisions/','.json'),path='legislation/',description='Cap.123、123A、123C、123F、123Q 中英文 XML；分拆成條文，沒有 PDF 頁碼。',evidence='search/legislation_audit.json',granularity='法例條文',status='有檔案',chapters=chapters))
 stages=[dict(id='collect',title='收集官方文件',state='built' if any(s.get('pdfs') for s in sources) else 'unknown',label='入庫流程已建立',detail='多個來源已有 PDF／XML、manifest 同原始來源紀錄。收藏完整性及現行版本仍須檢查。',evidence=['documents/','legislation/manifest.json','pnap_app_adv_sources.json']),dict(id='extract',title='轉成可搜尋文字',state='review' if manifest.get('needs_review') else ('built' if manifest.get('indexed') else 'unknown'),label='已抽字，仍有待覆核',detail='原生 PDF 直接抽字；掃描頁由 repo 工作流程做 OCR；XML 直接拆條文。空白頁、公式及表格要回看原文。',evidence=['scripts/build_index.py','index_manifest.json','geo/search_audit.json']),dict(id='search',title='建立搜尋索引',state='built' if 'search/pnap_fts.sqlite3' in paths else 'unknown',label='全文及部分條文索引已建立',detail='SQLite FTS5 做頁級全文搜尋，PNAP 有段落 JSON，法例有條文 JSON。其他技術文件目前主要按 PDF 頁搜尋。',evidence=['search/search_audit.json','search/pnap_paragraph_audit.json','search/legislation_audit.json']),dict(id='verify',title='核對答案與修正問題',state='pending',label='未完成完整準確性驗證',detail='索引建好唔代表答案一定準確。完整測試原題／原答案同逐題官方核對紀錄尚未能證實；準確率保留未知。',evidence=['website/status-notes.json'])]
 notes=read('website/status-notes.json')
 for stage in stages:
  override=notes.get('stage_overrides',{}).get(stage['id'],{})
  for key in ['state','label','detail','evidence']:
   if key in override:stage[key]=override[key]
 return dict(schema=1,repository='rsetestac001-ui/RSE',source_commit=sha,generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),stage_summary='資料已入庫並建立搜尋；下一步係補資料覆蓋同驗證答案。',counts={'pdf_files':count('documents/','.pdf'),'text_files':count('indexed_text/','.txt'),'indexed_documents':audit.get('documents'),'indexed_pages':audit.get('pages'),'pnap_sections':para.get('sections'),'law_provisions':law.get('provisions'),'needs_review':manifest.get('needs_review'),'empty_pages':len(audit['empty_pages']) if isinstance(audit.get('empty_pages'),list) else None,'accuracy':None},stages=stages,sources=sources,workflows=[e['path'] for e in files if e['path'].startswith('.github/workflows/') and e['path'].endswith(('.yml','.yaml'))],notes=read('website/status-notes.json'),method='檔案數量由 repository 目錄計算；索引數據由 audit／manifest 讀取；階段係依據現有產物嘅判讀，唔係整體完成百分比。')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',default='.');p.add_argument('--tree-json');p.add_argument('--output',default='website/project.json');a=p.parse_args();root=pathlib.Path(a.root).resolve();tree=json.loads(pathlib.Path(a.tree_json).read_text()) if a.tree_json else None;data=build(root,tree);out=pathlib.Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');print(f'Overview: {data["counts"]["pdf_files"]} PDFs, {data["counts"]["law_provisions"]} provisions → {out}')
