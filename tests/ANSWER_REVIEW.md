# 100條條文核對參考題：方法與限制

本批於2026-11-11建立。`answer_cases_v1.json`包含100條不同的中文問題、AI依repo原文整理的參考答案、適用範圍、文件版次、段落及PDF實體頁碼。它是一批新建立的條文核對題，**不是找回的100份歷史答案**。

原測試位於[未合併PR #1](https://github.com/rsetestac001-ui/RSE/pull/1)的`tests/search_cases.json`。本目錄以`legacy_search_cases.json`保留其100列：60個不同字串、40列重複，沒有待評完整答案。舊資料的輪換category不能視為可靠分類；其搜尋命中率不能稱為答案準確率。

## 本次做到的事

- 按原文整理100條有明確範圍的參考答案，包含嚴格大於／不超過、且／或、版次及例外。核對由AI執行，沒有獨立工程師審定。
- 每題用完整中文問題執行目前`main`的頁級搜尋，保存前10個結果。
- 另以人工整理的英文關鍵字作診斷，獨立保存結果。英文成績不能代替中文成績。
- 對照指定參考文件及頁碼是否出現在結果；頁碼命中是地址比對，並非該段能完整支持答案的自動語義判定。
- 重新下載所用官方PDF及DOJ官方英文XML資料包，比較repo副本的SHA-256。副本一致不代表已證明所有指引均完整或所有適用條件已窮盡。
- 公式與樁型數值另回看Foundation Code的PDF實體第76、77、78頁，並讀2025修訂與APP-18。

範圍集中於Scheduled Area GI、Mid-levels、GBP岩土評估、新界SF豁免、ELS、bored/CFA piles、一般GI、HKIE基礎手冊角色及consent。**尚不構成全庫GEO、wind、RC、steel或APSEC的完整答案測試。**

## 重跑

```sh
python scripts/review_answer_cases.py
python scripts/build_answer_review_report.py
```

搜尋重跑只用本地SQLite，沒有模型API。首次或索引缺失時先用既有`build_search.py build`建立索引。獨立官方副本檢查可用`python scripts/check_answer_official_sources.py`，會下載官方PDF及大型DOJ資料包；這不屬每次搜尋的必要動作。

## 如何完成真正的答案評分

目前保存的是原文核對參考答案；歷史答案評分數為0，答案準確率維持null。正式評分須先固定欲測系統輸出的答案，再獨立核對每項數值、條件、例外及引文。不得把本批參考答案自動與自己比對而報100%答對。

依據實跑結果，優先改善中文用語／數值語境處理、獨立法例索引整合、同一長文件多頁佔位及鄰近段落補讀。需保留本批原結果，在獨立的新問題上評估改善，避免只為這100題硬編碼答案或文件編號。

逐題結果見[`../search/answer_review_v1.md`](../search/answer_review_v1.md)；機器結果在`../search/answer_retrieval_v1.json`，官方副本比對在`../search/answer_official_sources_v1.json`。
