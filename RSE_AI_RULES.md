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
