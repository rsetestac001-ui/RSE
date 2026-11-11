# RSE 原100條搜尋測試：核對及改善報告

核對日期：2026-11-11。原100列已逐列執行搜尋與來源對照；官方搜尋按十個重複主題進行，並非100次獨立官方搜尋。原列未包含待評答案，因此不能宣稱完成100條獨立工程答案準確率核證。

## 實際結果

| 項目 | 結果 |
|---|---|
| 原列逐列測試 | 100/100 |
| 不同搜尋字串 | 60 |
| 完全重複列 | 40 |
| 原先沒有預期文件的列 | 60 |
| 舊候選文件命中比例 | 23.3% |
| 修正後同一批舊候選文件命中比例 | 98.3% |
| 審閱相關文件：頭十份文件覆蓋 | 83.1% |
| 按60個不同搜尋字串計算的文件覆蓋 | 82.2% |
| 加上明列交叉引用／修訂連結的覆蓋 | 92.8% |
| Consent主題列出的5條法例參考：頭十條覆蓋 | 100.0% |
| 獨立下載官方PDF與repo逐位元一致 | 37/37 |
| 獨立官方DOJ資料包英文XML逐位元一致 | 5/5 |
| 引用頁碼在索引中的地址錯誤 | 0 |
| 答案準確率／Precision@10／語義頁碼正確率 | 未評分；沒有適用的完整答案及完整相關性判定 |

以上不是「答對98.3%」。舊候選標籤仍有範圍不足，改善後的文件覆蓋也未達原定95%目標。交叉引用／修訂連結覆蓋不能冒充頭十份文件覆蓋。前後比較包括新增斜坡手冊，不是只改排序的隔離實驗。頁碼地址存在不能證明該頁實質支持答案。來源檔案一致也不表示已窮盡所有更新或完成專業判讀。

## 發現的問題與已實作修正

| 問題 | 修正及驗證 |
|---|---|
| 長文件多頁佔滿前十位，重要短PNAP被擠走 | 每份文件保留一個最佳頁面，增加標題及查詢詞覆蓋排序；Scheduled Area GI、ELS、一般GI回歸測試通過。 |
| 簡單OR搜尋及縮寫處理不完整 | 以同一搜尋函式供CLI、直接讀取的topic JSON及QA使用；GI/ELS/SF及選定中文用語擴展，英文縮寫只按完整詞替換。 |
| 法例是另一資料庫，原QA沒有查 | CLI及topic同時回傳法例條文，XML頁碼固定為null並註明沒有PDF頁碼；Consent可找到Cap.123 s14/s20及Cap.123A regs31/32/34。 |
| 舊版手冊及主文／修訂的角色不清 | 回傳Code修訂URL、PNAP交叉引用及舊版提示；保留歷史版次，不能把APP-63接受的完整第一版設計誤稱一律禁止。 |
| 斜坡穩定缺少GMS主文 | 已加入官方《Geotechnical Manual for Slopes》原PDF、303個實體頁及287頁hash綁定OCR，保存官方頁面的TGN更新連結；OCR仍須原PDF核證。 |
| 題庫重複、分類輪換、標籤有漏 | 保留原100列供前後比較；逐列標註duplicate_of、原標籤評語、補充相關文件、適用範圍及未評答案狀態，另報不同查詢的覆蓋率。 |
| 只見Actions成功容易誤當答案準確 | 新增8個回歸測試、來源hash檢查、逐列QA及報告artifact；strict只檢查退步／證據完整性，不認證答案。 |

## 必須保留的適用範圍

- APP-30只針對Scheduled Area No.1；一般GI不能只用ADM-16回答。Refer to：ADM-16第1–3段PDF1；APP-30第2–4段PDF1；APP-49第1–8段PDF1–3。
- SF入則、GBP階段岩土評估、ELS及新界豁免制度不能共用一套門檻。Refer to：ADM-15第2–7段PDF1–2；APP-15第2段PDF1及Appendix A PDF3；APP-25第2段PDF1–2；APP-56第1–5段PDF1–2。
- ELS須讀2026年7月版及BD對GEO方法的特定要求。Refer to：APP-57第3–10段PDF1–3及Appendix A PDF4–6。
- 基礎Code、PNAP及HKIE解說的版次與效力不同。Refer to：Foundations2017(2024Edition)§§5.4.6–5.4.7 PDF76–78、September2025amendments；APP-18 February2026版；HKIE2017手冊出版／聲明PDF2–3。

每題詳細文件編號、原文來源路徑、段落、PDF實體頁碼、GitHub連結、官方URL及hash核對狀態見[`qa_report.json`](qa_report.json)與[`topic_reviews.json`](../tests/topic_reviews.json)。

## 未解決事項

1. 原題庫不是100條獨立真實問題，也沒有待評的完整答案。正式答案評核需要100條有不同實際情況的問題及逐題答案，核對數值、觸發邏輯、範圍、豁免、版本與證據頁面。
2. 目前相關文件目標並非完整相關性清單；不能計算可信Precision@10。對較廣問題，背景文件與特定制度文件仍可能佔用結果。
3. 補入GMS解決來源缺漏，未解決所有OCR數字／公式／表格的人工核證。APSEC歷史缺漏及舊HKIE手冊的個別掃描頁亦未被本次審閱宣稱解決。
4. 檢查37份PDF及5份英文XML，是這次測試所用來源的副本一致性核對，不是全庫每份文件的最新版本認證。

## 原100列逐列結果

表中「補充文件」是本次審閱列出的相關文件目標；不是完整工程答案的判定。

| ID | 原搜尋字串 | 重複於 | 原標籤評語 | 補充文件頭十份命中 | 含交叉引用命中 |
|---|---|---|---|---:|---:|
| Q001 | scheduled area ground investigation | — | 相關，須保留範圍 | 2/2 | 2/2 |
| Q002 | site formation submission | — | 只部分相關 | 4/4 | 4/4 |
| Q003 | excavation lateral support | — | 相關，須保留範圍 | 2/2 | 2/2 |
| Q004 | foundation bored pile | — | 原先無預期文件 | 3/3 | 3/3 |
| Q005 | wind effects | — | 原先無預期文件 | 4/4 | 4/4 |
| Q006 | retaining wall | — | 原先無預期文件 | 3/3 | 3/3 |
| Q007 | ground investigation | — | 只部分相關 | 2/2 | 2/2 |
| Q008 | consent commencement | — | 原先無預期文件 | 0/1 | 1/1 |
| Q009 | slope stability | — | 原先無預期文件 | 1/3 | 1/3 |
| Q010 | concrete design | — | 原先無預期文件 | 3/5 | 5/5 |
| Q011 | scheduled area ground investigation design | — | 相關，須保留範圍 | 2/2 | 2/2 |
| Q012 | site formation submission design | — | 只部分相關 | 4/4 | 4/4 |
| Q013 | excavation lateral support design | — | 相關，須保留範圍 | 2/2 | 2/2 |
| Q014 | foundation bored pile design | — | 原先無預期文件 | 3/3 | 3/3 |
| Q015 | wind effects design | — | 原先無預期文件 | 4/4 | 4/4 |
| Q016 | retaining wall design | — | 原先無預期文件 | 3/3 | 3/3 |
| Q017 | ground investigation design | — | 只部分相關 | 2/2 | 2/2 |
| Q018 | consent commencement design | — | 原先無預期文件 | 0/1 | 1/1 |
| Q019 | slope stability design | — | 原先無預期文件 | 1/3 | 1/3 |
| Q020 | concrete design design | — | 原先無預期文件 | 3/5 | 5/5 |
| Q021 | scheduled area ground investigation guidance | — | 相關，須保留範圍 | 2/2 | 2/2 |
| Q022 | site formation submission guidance | — | 只部分相關 | 4/4 | 4/4 |
| Q023 | excavation lateral support guidance | — | 相關，須保留範圍 | 2/2 | 2/2 |
| Q024 | foundation bored pile guidance | — | 原先無預期文件 | 3/3 | 3/3 |
| Q025 | wind effects guidance | — | 原先無預期文件 | 4/4 | 4/4 |
| Q026 | retaining wall guidance | — | 原先無預期文件 | 3/3 | 3/3 |
| Q027 | ground investigation guidance | — | 只部分相關 | 2/2 | 2/2 |
| Q028 | consent commencement guidance | — | 原先無預期文件 | 0/1 | 1/1 |
| Q029 | slope stability guidance | — | 原先無預期文件 | 1/3 | 1/3 |
| Q030 | concrete design guidance | — | 原先無預期文件 | 3/5 | 5/5 |
| Q031 | scheduled area ground investigation code | — | 相關，須保留範圍 | 2/2 | 2/2 |
| Q032 | site formation submission code | — | 只部分相關 | 4/4 | 4/4 |
| Q033 | excavation lateral support code | — | 相關，須保留範圍 | 2/2 | 2/2 |
| Q034 | foundation bored pile code | — | 原先無預期文件 | 3/3 | 3/3 |
| Q035 | wind effects code | — | 原先無預期文件 | 4/4 | 4/4 |
| Q036 | retaining wall code | — | 原先無預期文件 | 3/3 | 3/3 |
| Q037 | ground investigation code | — | 只部分相關 | 2/2 | 2/2 |
| Q038 | consent commencement code | — | 原先無預期文件 | 0/1 | 1/1 |
| Q039 | slope stability code | — | 原先無預期文件 | 1/3 | 1/3 |
| Q040 | concrete design code | — | 原先無預期文件 | 5/5 | 5/5 |
| Q041 | scheduled area ground investigation technical | — | 相關，須保留範圍 | 2/2 | 2/2 |
| Q042 | site formation submission technical | — | 只部分相關 | 3/4 | 3/4 |
| Q043 | excavation lateral support technical | — | 相關，須保留範圍 | 2/2 | 2/2 |
| Q044 | foundation bored pile technical | — | 原先無預期文件 | 3/3 | 3/3 |
| Q045 | wind effects technical | — | 原先無預期文件 | 4/4 | 4/4 |
| Q046 | retaining wall technical | — | 原先無預期文件 | 3/3 | 3/3 |
| Q047 | ground investigation technical | — | 只部分相關 | 2/2 | 2/2 |
| Q048 | consent commencement technical | — | 原先無預期文件 | 0/1 | 1/1 |
| Q049 | slope stability technical | — | 原先無預期文件 | 1/3 | 1/3 |
| Q050 | concrete design technical | — | 原先無預期文件 | 2/5 | 5/5 |
| Q051 | scheduled area ground investigation | Q001 | 相關，須保留範圍 | 2/2 | 2/2 |
| Q052 | site formation submission | Q002 | 只部分相關 | 4/4 | 4/4 |
| Q053 | excavation lateral support | Q003 | 相關，須保留範圍 | 2/2 | 2/2 |
| Q054 | foundation bored pile | Q004 | 原先無預期文件 | 3/3 | 3/3 |
| Q055 | wind effects | Q005 | 原先無預期文件 | 4/4 | 4/4 |
| Q056 | retaining wall | Q006 | 原先無預期文件 | 3/3 | 3/3 |
| Q057 | ground investigation | Q007 | 只部分相關 | 2/2 | 2/2 |
| Q058 | consent commencement | Q008 | 原先無預期文件 | 0/1 | 1/1 |
| Q059 | slope stability | Q009 | 原先無預期文件 | 1/3 | 1/3 |
| Q060 | concrete design | Q010 | 原先無預期文件 | 3/5 | 5/5 |
| Q061 | scheduled area ground investigation requirements | — | 相關，須保留範圍 | 2/2 | 2/2 |
| Q062 | site formation submission requirements | — | 只部分相關 | 4/4 | 4/4 |
| Q063 | excavation lateral support requirements | — | 相關，須保留範圍 | 2/2 | 2/2 |
| Q064 | foundation bored pile requirements | — | 原先無預期文件 | 3/3 | 3/3 |
| Q065 | wind effects requirements | — | 原先無預期文件 | 4/4 | 4/4 |
| Q066 | retaining wall requirements | — | 原先無預期文件 | 3/3 | 3/3 |
| Q067 | ground investigation requirements | — | 只部分相關 | 2/2 | 2/2 |
| Q068 | consent commencement requirements | — | 原先無預期文件 | 0/1 | 1/1 |
| Q069 | slope stability requirements | — | 原先無預期文件 | 1/3 | 1/3 |
| Q070 | concrete design requirements | — | 原先無預期文件 | 2/5 | 5/5 |
| Q071 | scheduled area ground investigation design | Q011 | 相關，須保留範圍 | 2/2 | 2/2 |
| Q072 | site formation submission design | Q012 | 只部分相關 | 4/4 | 4/4 |
| Q073 | excavation lateral support design | Q013 | 相關，須保留範圍 | 2/2 | 2/2 |
| Q074 | foundation bored pile design | Q014 | 原先無預期文件 | 3/3 | 3/3 |
| Q075 | wind effects design | Q015 | 原先無預期文件 | 4/4 | 4/4 |
| Q076 | retaining wall design | Q016 | 原先無預期文件 | 3/3 | 3/3 |
| Q077 | ground investigation design | Q017 | 只部分相關 | 2/2 | 2/2 |
| Q078 | consent commencement design | Q018 | 原先無預期文件 | 0/1 | 1/1 |
| Q079 | slope stability design | Q019 | 原先無預期文件 | 1/3 | 1/3 |
| Q080 | concrete design design | Q020 | 原先無預期文件 | 3/5 | 5/5 |
| Q081 | scheduled area ground investigation guidance | Q021 | 相關，須保留範圍 | 2/2 | 2/2 |
| Q082 | site formation submission guidance | Q022 | 只部分相關 | 4/4 | 4/4 |
| Q083 | excavation lateral support guidance | Q023 | 相關，須保留範圍 | 2/2 | 2/2 |
| Q084 | foundation bored pile guidance | Q024 | 原先無預期文件 | 3/3 | 3/3 |
| Q085 | wind effects guidance | Q025 | 原先無預期文件 | 4/4 | 4/4 |
| Q086 | retaining wall guidance | Q026 | 原先無預期文件 | 3/3 | 3/3 |
| Q087 | ground investigation guidance | Q027 | 只部分相關 | 2/2 | 2/2 |
| Q088 | consent commencement guidance | Q028 | 原先無預期文件 | 0/1 | 1/1 |
| Q089 | slope stability guidance | Q029 | 原先無預期文件 | 1/3 | 1/3 |
| Q090 | concrete design guidance | Q030 | 原先無預期文件 | 3/5 | 5/5 |
| Q091 | scheduled area ground investigation code | Q031 | 相關，須保留範圍 | 2/2 | 2/2 |
| Q092 | site formation submission code | Q032 | 只部分相關 | 4/4 | 4/4 |
| Q093 | excavation lateral support code | Q033 | 相關，須保留範圍 | 2/2 | 2/2 |
| Q094 | foundation bored pile code | Q034 | 原先無預期文件 | 3/3 | 3/3 |
| Q095 | wind effects code | Q035 | 原先無預期文件 | 4/4 | 4/4 |
| Q096 | retaining wall code | Q036 | 原先無預期文件 | 3/3 | 3/3 |
| Q097 | ground investigation code | Q037 | 只部分相關 | 2/2 | 2/2 |
| Q098 | consent commencement code | Q038 | 原先無預期文件 | 0/1 | 1/1 |
| Q099 | slope stability code | Q039 | 原先無預期文件 | 1/3 | 1/3 |
| Q100 | concrete design code | Q040 | 原先無預期文件 | 5/5 | 5/5 |

來源發現過程見[`official_web_review.json`](../tests/official_web_review.json)，可重現方法及評分限制見[`tests/README.md`](../tests/README.md)。
