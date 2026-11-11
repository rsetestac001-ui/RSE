# RSE AI Answering Rules

## Mandatory source priority

For every question asked within the RSE project concerning Hong Kong buildings, structural engineering, geotechnical investigation (GI), statutory submissions, PNAP, or related technical/regulatory matters:

1. **Search the RSE GitHub repository first**: https://github.com/rsetestac001-ui/RSE
2. Prefer repository documents, indexed text, and index_manifest.json as the primary evidence.
3. Provide the exact document identifier, relevant passage/section, and PDF page number whenever verifiable.
4. Clearly distinguish quoted or verified document facts from the assistant's interpretation.
5. If repository evidence is unavailable, incomplete, or not yet checked, state this explicitly. Never claim to have checked the RSE repository when it has not been accessed.
6. If official Buildings Department websites or other external sources are used to check updates or gaps, identify them separately; never silently substitute web/general knowledge for the RSE repository.
7. For statutory submission or safety-critical conclusions, identify uncertainties and relevant conditions; do not overstate legal or professional certainty.

**Core rule: RSE repository first; verifiable citations before conclusions.**

## BD Codes of Practice retrieval

結構設計問題亦須查閱 `codes/manifest.json` 及 `codes/catalog.json`，按適用範圍讀取 foundation、RC、steel、dead and imposed loads、wind code 的原文，以及目錄所列修訂及相關 PNAP。官方解說與主文須分清；不可只讀舊主文而漏掉修訂。PDF 在 `documents/BD_CODES/`，附 PDF 頁碼標記的全文在 `indexed_text/BD_CODES/`。公式、圖表及表格須回看原 PDF；PDF 實體頁數與印刷頁碼須區分。

This file records the user's standing preference for RSE project responses. It does not itself modify ChatGPT Project Instructions.

## 回答前防漏檢查（2026-11-11 新增）

適用於所有香港建築、結構工程、GI、PNAP、屋宇署法規及入則問題。回答前須完成以下檢查，不能等使用者逐項追問：

1. **明確交代 GitHub 查閱結果**：回答開首先說明在 RSE GitHub「找到」、「部分找到」或「未找到」，並列出實際讀過且支持答案的文件。未讀取不得聲稱已核實。
2. **查法例亦查相關 PNAP**：先用索引找候選文件，再讀相關原文及交叉引用。索引摘要或搜尋無結果不足以支持「沒有規定」；若資料不足，指出已查範圍及未能確認之處。
3. **主動提供相關數值及完整條件**：對「何時需要入則／是否需要／豁免／期限」等問題，一併核對坡度、深度、高度、長度、距離、面積、體積、期限等相關數值，以及觸發條件、適用範圍、豁免及例外；只列與問題有實質關係的準則，不要求使用者先知道數值再追問。
4. **保留條件邏輯**：準確區分「大於／不小於／小於／不超過」及「且／或」，說明各條件是否須同時成立。不得將特定地區、工程類別或豁免制度的數值當成通用門檻。
5. **區分不同程序**：例如 SF 圖則、ELS 圖則、GBP 階段 Geotechnical Assessment、GI 入則、approval、consent 及續期，應分別說明；不得互相替代或混用門檻。
6. **逐項提供出處**：列文件編號、段落／條文及可核對的 PDF 頁碼，並附 RSE GitHub 連結。若法例來自 XML，明確說明沒有 PDF 頁碼，不得猜測。
7. **區分證據與分析**：標示文件明文要求與 AI 的實務判讀。外部官方資料只作補充並另行標明。未確認個案條件前，避免對個案給出無條件結論。
8. **檢查否定結論**：「已查文件未見通用門檻」不等於「PNAP 沒有相關數值」。提出否定結論時，須同時交代找到的相關特定準則及其用途，並限制結論於已查文件。
9. **保存及驗證**：聲稱規則或檔案已更新前，必須成功寫入並重新讀取核對。repo 規則不等於已修改 ChatGPT Project Instructions，也不能保證每個新對話自動載入。

### SF 問題的防漏例子（非獨立法規依據）

回答 SF 入則觸發條件時，應核對當時版本的 Cap.123 第2、14及41條、Cap.123A 第8(1)(bb)條，以及適用的 PNAP，例如 APP-15、APP-25、APP-56、APP-57、ADM-15。
APP-56 的新界豁免建築相關 SF 豁免條件、APP-25 的 GBP 階段岩土評估條件及 APP-57 的 ELS 入則條件用途不同。必須讀取現行文件後再引用數字，不能把其中任何一套直接視為所有 SF 工程的通用入則門檻。

## APSEC Discussion Forum retrieval

相關問題亦須查閱 `apsec/manifest.json` 的年份覆蓋及來源，再讀取 `documents/APSEC/` 或 `indexed_text/APSEC/` 原文。必須區分左欄提出的問題與右欄 BD 回應，並引用會議日期、item 編號、欄位及 PDF 實體頁碼。APSEC Discussion Forum 摘要並非法例、PNAP 或完整 APSEC 正式會議紀錄；須核對現行法例、PNAP、codes 及原文交叉引用。公開收藏未核實為完整歷史檔案；較早或未列出的會議缺漏必須如實交代，不可把未下載當成沒有相關討論。

## GEO guidance retrieval

岩土問題須查閱 `geo/manifest.json`、`geo/search_audit.json` 及官方目錄保存的狀態註記，再讀 `documents/GEO/` 或 `indexed_text/GEO/` 原文。涵蓋 Geoguides、GCO/GEO Publications 及 TGN；GEO Reports、Geospecs 等其他系列不在此下載範圍。目錄可能同時提供原版、整合修訂版及 amendments，必須核對版本、取代／取消及交叉引用（包括 TGN master list、TGN 1 及相關 PNAP）；不可把歷史版本或已取消 TGN 當作現行指引。須區分技術指引與法例，列文件編號／版本、段落及 PDF 實體頁碼。空白或掃描頁、公式及圖表須回看 PDF，全文未抽出不代表沒有規定。

## HKIE and BD explanatory publications

結構設計問題須按主題查 `explanatory/catalog.json`、`explanatory/manifest.json` 及 `explanatory/search_audit.json`，讀 HKIE 手冊（`documents/HKIE/`、`indexed_text/HKIE/`）及 BD 解說（沿用 `documents/BD_CODES/`）原文。必須標明出版者、手冊對應的 Code 年份／版次及 PDF 實體頁碼；舊手冊不能自動視為適用於現行 Code。HKIE 手冊中的分析、設計例子與 BD Code／法例／PNAP 要求須分清，不能互相替代；同時核對 Code 修訂。掃描頁 OCR 是未經人工核證的轉錄，數值、公式、表格及圖須回看 PDF。此目錄涵蓋已核對的公開手冊及 BD steel/wind 解說，並非聲稱 HKIE／BD 所有解說文件已齊全。

## 搜尋測試結果的解讀（2026-11-11）
`search/qa_review.md`、`search/qa_report.json` 及 `tests/README.md` 記錄原100條搜尋列的逐列審閱。原題庫只有60個不同搜尋字串，並非100條有完整答案的獨立工程問題。不得把候選文件命中、文件覆蓋、官方檔案SHA一致、頁碼地址存在或Actions成功，稱為答案準確率、條件判讀正確率或頁面證據正確率。新搜尋使用文件去重，分開回傳法例條文及PDF結果，並列PNAP交叉引用和Code修訂；回答仍須讀取原文及適用範圍。另已加入《Geotechnical Manual for Slopes》及原官方頁面的TGN更新連結；新增OCR亦屬未經人工核證的轉錄，數值、表格及圖仍須回看PDF。
