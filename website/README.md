# RSE 項目總覽網站

呢個係項目進度同資料原理嘅圖像化總覽。來源係本 repository，唔將「文件入庫」當成「答案已核實」。

## 放喺 GitHub 嘅內容

| 檔案 | 用途 | 幾時更新 |
| --- | --- | --- |
| `website/index.html` | 完整網站介面，可獨立靜態託管 | 改設計、圖解或介面內容 |
| `website/project.json` | 小型進度摘要，首頁直接讀取 | 由 Python／Actions 產生 |
| `website/status-notes.json` | 目前重點、已知限制、下一步 | 人工確認進度後修改 |
| `scripts/build_project_overview.py` | 由文件目錄、manifest、audit 計算摘要 | 指標／來源範圍有改變 |
| `.github/workflows/update-project-overview.yml` | 監察資料／索引更新後重算摘要 | 改觸發條件或更新流程 |

PDF 留喺 `documents/`，抽取文字喺 `indexed_text/`，法例喺 `legislation/`，搜尋產物喺 `search/`。網站唔重複儲存呢啲大型檔案。官方文件唔齊、版本未核對同準確率未知都會保留標記。

## 更新方法

1. 更新文件來源／下載或放入原始文件，再執行對應下載、PDF 抽字同搜尋索引工作流程。
2. 更新 `website/status-notes.json` 交代目前重點同下一步。只有可核實嘅進度先寫成已完成。
3. `Update project overview` 工作流程會按 push 路徑設定，或兩個主要索引 workflow 完成後，重算 `website/project.json`。亦可以喺 Actions 手動執行。GitHub bot 寫入其他 workflow 所產生嘅 commit 未必會再次觸發 push 工作流程，因此 `workflow_run` 只列兩個現有主要索引流程；其他系列更新後可手動重跑 overview。
4. 開網站或按「更新狀態」讀最新摘要。數量來自實際檔案同檢查報告，唔係手填整體完成百分比。

本機重算：`python scripts/build_project_overview.py`（Python 3.11 標準庫，無其他依賴）。靜態預覽可由 HTTP server 提供 `website/`。GitHub 本身嘅檔案頁唔會執行 HTML；要用 Sites 或另外啟用靜態網站託管。

## Sites 部署

正式網址：https://rse-engineering-workbench.effervescentpatio2.chatgpt.site

Sites 首頁使用本 HTML，`/api/project` 由 server 讀 GitHub `main/website/project.json`；失敗時顯示隨發佈保存嘅快照並明確標示。打開首頁只需小份摘要，唔下載全文搜尋庫。改 `project.json`／進度備註後可重新讀取資料；改 `website/index.html` 則要同步 HTML 到 Sites 原始碼並重新發佈，GitHub commit 本身唔會自動部署 Sites。舊搜尋／核對工具保留於 `/workbench`。

## 解讀限制

365 份 PDF 同 678 個法例條文檔案係唔同單位。頁數／段落數從各 audit 讀取，可能對應上一輪索引；缺少報告顯示未知。PDF 掃描、圖表、公式、修訂及法律效力仍須回看原文件。`stage_overrides` 可以喺 status-notes.json 按 stage id（collect / extract / search / verify）提供 state、label、detail、evidence；只應按可核實依據修改。
