# 屋宇署小型工程刊物來源索引

檢索日期：2026-11-11T08:12:56Z。資料來自屋宇署網站當時的公開目錄及下載檔，不是本庫所存 PDF。本庫沒有存入任何小型工程 PDF。

官方目錄：

- 英文：<https://www.bd.gov.hk/en/resources/codes-and-references/codes-and-design-manuals/index.html>
- 中文：<https://www.bd.gov.hk/tc/resources/codes-and-references/codes-and-design-manuals/index.html>

## 目錄上的正式名稱

現行「守則、設計手冊及指引」目錄沒有名為 *Code of Practice for the Minor Works Control System* 的作業守則，也沒有名為 *Explanatory Notes* 的小型工程說明資料。

目錄上與小型工程監管制度直接對應、並標為現行的技術刊物是：

| 目錄用語 | 正式名稱 |
|---|---|
| 英文 | Technical Guidelines on Minor Works Control System (2024 edition) (Only the Chinese version is available) |
| 中文 | 小型工程監管制度之技術指引（2024年修訂版） |

英文目錄及英文分章頁 <https://www.bd.gov.hk/en/resources/codes-and-references/codes-and-design-manuals/MWTG.html> 都寫明只有中文版本。該英文頁的章節連結指向 `doc/tc/.../TG_c/` 中文 PDF。`TGe_ch01.pdf` 回傳 HTTP 404。

合訂本前言寫明初版為 2010 年 10 月，本修訂版為 2025 年 2 月，並收錄至 2025 年 2 月的修訂。2025 年 10 月及 2026 年 8 月兩份修訂是目錄另列的 PDF，沒有併入這份合訂本。閱讀現行技術內容時，三份檔案要一併看。

## 為何沒有存入 PDF

屋宇署 [Important Notices](https://www.bd.gov.hk/en/important-notices/index.html) 寫明，網站內容的版權屬香港特別行政區政府。未經屋宇署事先書面授權，不得複製、分發、散布或向公眾提供；下載許可限於單一電腦上的個人、非商業內部使用，不得把材料轉移給另一人，亦不得在未得政府書面許可下上載、張貼、傳送或分發。機構內部可複製未經改動的文本，其餘權利保留。同一頁寫明英、中文本如有不一致，以英文為準。

`gh repo view` 顯示本倉庫 `rsetestac001-ui/RSE` 的 visibility 為 PUBLIC。把 PDF 提交到這個倉庫屬於向公眾提供。因此下面只記錄官方連結，以及是次下載核對得到的 SHA-256；倉庫內沒有這些 PDF。

合訂本 `MWTGc.pdf` 為 146,132,641 bytes（約 139.4 MiB），超過 GitHub 單一檔案 100 MB 上限。28 個分章 PDF 個別都低於 100 MB（最大為附錄 VII 第 II 級別，49,964,187 bytes），但公開再分發的限制同樣適用，所以沒有改以分章方式存入。

## 現行技術指引（已開啟 PDF 核對）

出版者（PDF metadata）：香港特別行政區政府屋宇署。語言：繁體中文。本庫路徑：無。

| 文件 | 版本日期（PDF 內文／metadata） | HTTP Last-Modified | 頁數 | bytes | SHA-256 |
|---|---|---|---|---|---|
| [合訂本 MWTGc.pdf](https://www.bd.gov.hk/doc/tc/resources/codes-and-references/code-and-design-manuals/MW/MWTGc.pdf) | 封面及 metadata 標題「小型工程監管制度之技術指引（2024年修訂版）」；前言：初版 2010 年 10 月，本修訂版 2025 年 2 月。CreationDate 2025-02-23 | Fri, 28 Feb 2025 01:00:39 GMT | 660 | 146132641 | `2a712ecaa1606f57a42d82975b8e157d3c3e2ae324bb58e0a53cdef1675ab5fd` |
| [2025 年 10 月修訂](https://www.bd.gov.hk/doc/tc/resources/codes-and-references/code-and-design-manuals/MW/MWTGc_amendment_oct2025.pdf) | metadata 標題「《小型工程監管制度之技術指引》（2024年修訂版）的修訂(2025年10月)」。目錄標題：修訂加入遮蓋建築物外牆的保護網、保護幕、防水油布或塑膠帆布的阻燃效能認可標準（2025年10月） | Tue, 23 Dec 2025 09:06:10 GMT | 2 | 292656 | `73444e54dead07dfe7b9459cc7f27b565f003cb83fcebb9430ba465ba2578294` |
| [2026 年 8 月修訂](https://www.bd.gov.hk/doc/tc/resources/codes-and-references/code-and-design-manuals/MW/MWTGc_amendment_aug2026.pdf) | metadata 標題「《小型工程監管制度之技術指引》（2024年修訂版）(2026年8月修訂)」。目錄標題：修訂加入長者友善樓宇設計的強制性規定（2026年8月） | Tue, 18 Aug 2026 13:38:44 GMT | 12 | 669793 | `527f4d7dabe8702fd7fdb4bf2e83f22aae659e5e0c756c1bb05303412e1e6a00` |

落地頁：

- 中文分章：<https://www.bd.gov.hk/tc/resources/codes-and-references/codes-and-design-manuals/MWTG.html>
- 英文分章（連結為中文 PDF）：<https://www.bd.gov.hk/en/resources/codes-and-references/codes-and-design-manuals/MWTG.html>

核對：`file` 認三份都是 PDF。`pdfinfo` 讀到上表頁數。`pdftotext` 抽出合訂本封面、前言，以及兩份修訂的標題及修訂欄。合訂本抽出的全文沒有「阻燃」「長者友善」「GB 5725」「2025 年 10 月」「2026 年 8 月」；前言所列修訂止於 2025 年 2 月。抽出文字不是 OCR，圖則頁可以沒有文字，所以上述關鍵詞缺失要與前言的修訂清單一併看。Poppler 讀合訂本時出現 “Expected the optional content group list” 語法提示，仍讀到 660 頁並抽出封面。2026 年 8 月修訂的 PDF 以 AES-256 加密（允許列印及複製文字、不允許修改），文字仍可抽出。

## 同一 2024 年修訂版的分章連結

分章頁與合訂本是同一版的兩種官方提供方式，不是另兩份修訂。下表只做 HTTP HEAD（2026-11-11）：全部 `200`、`application/pdf`，Last-Modified 同為 2025-02-28。除目錄及第 1 章外，沒有下載全文，所以沒有逐章 SHA-256。目錄 SHA-256 `c1e2931a7a8593cbb52d9e0166e7a89214501b0596ec7b7198a99137a45d648b`（286,293 bytes，6 頁，metadata 標題與合訂本相同）。第 1 章 SHA-256 `1ca4b269ea74e212c74e3935787402e2f0de5bc63ab77557e47c50d0f308b496`（786,209 bytes，10 頁）。28 個檔案合計 144,056,402 bytes。

基址：`https://www.bd.gov.hk/doc/tc/resources/codes-and-references/code-and-design-manuals/MW/TG_c/`

| 檔名 | 分章頁標示 | bytes |
|---|---|---|
| `TGc_toc.pdf` | 目錄 | 286293 |
| `TGc_ch01.pdf` | 第1章 引言 | 786209 |
| `TGc_ch02.pdf` | 第2章 小型工程 | 538791 |
| `TGc_ch03.pdf` | 第3章 「小型工程」的範疇 | 16286182 |
| `TGc_ch04.pdf` | 第4章 進行「小型工程」的法定程序 | 1202512 |
| `TGc_ch05.pdf` | 第5章 豁免建築工程 | 166682 |
| `TGc_ch06.pdf` | 第6章 指定豁免工程 | 1579382 |
| `TGc_ch07.pdf` | 第7章 「訂明建築物或建築工程」的檢查及核證 | 3236947 |
| `TGc_ch08.pdf` | 第8章 「訂明註冊承建商」的法律責任 | 206950 |
| `TGc_ch09.pdf` | 第9章 對「訂明建築專業人士」及「訂明註冊承建商」的刑罰 | 258545 |
| `TGc_ch10.pdf` | 第10章 其他法律條文 | 397332 |
| `TGc_ch11.pdf` | 第11章 預防及安全措施 | 915101 |
| `TGc_ch12.pdf` | 第12章 保險事宜 | 170051 |
| `TGc_ch13.pdf` | 第13章 其他須留意的事項 | 243721 |
| `TGc_ch14.pdf` | 第14章 常見問題 | 280764 |
| `TGc_ch15.pdf` | 第15章 查詢 | 142218 |
| `TGc_appI.pdf` | 附錄I 「小型工程」的類型 | 225049 |
| `TGc_appII.pdf` | 附錄II 「小型工程」項目 | 467566 |
| `TGc_appIII.pdf` | 附錄III 須委任的「訂明註冊承建商」 | 110026 |
| `TGc_appIV.pdf` | 附錄IV 指明表格及標準表格一覽表 | 210098 |
| `TGc_appV.pdf` | 附錄V 指明表格的樣本 | 19885559 |
| `TGc_appVI.pdf` | 附錄VI 可用於圖則着色的顏色 | 127439 |
| `TGc_appVII.pdf` | 附錄VII 建議設計及詳圖 | 562348 |
| `TGc_appVII_classII.pdf` | 附錄VII 第II級別 | 49964187 |
| `TGc_appVII_classIII.pdf` | 附錄VII 第III級別 | 43788773 |
| `TGc_appVIII.pdf` | 附錄VIII 職業安全及健康 | 395623 |
| `TGc_appIX.pdf` | 附錄IX 給承建商的建議步驟 | 89421 |
| `TGc_appX.pdf` | 附錄X 窗或玻璃外牆用作防護欄障 | 1532633 |

## 沒有當作現行英文版或說明資料的其他連結

這些檔案不是現行《技術指引》的英文版，也不是作業守則的 Explanatory Notes。本庫沒有存入。

- 英文舊版壓縮檔（目錄標為 Obsolete versions）：<https://www.bd.gov.hk/doc/en/resources/codes-and-references/code-and-design-manuals/MW/TG_e/obsolete/MWTGeov.zip>。HEAD：105,789,904 bytes，`application/zip`，Last-Modified Fri, 28 Feb 2025 01:00:35 GMT。沒有解壓，沒有 SHA-256。
- 中文舊版壓縮檔（目錄標為舊有版本）：<https://www.bd.gov.hk/doc/tc/resources/codes-and-references/code-and-design-manuals/MW/TG_c/obsolete/MWTGcov.zip>。只見於目錄連結，是次沒有下載。
- 較早的英文合訂路徑 <https://www.bd.gov.hk/doc/en/building-works/minor-works/MWTGe.pdf>：HEAD 34,213,148 bytes，Last-Modified Wed, 19 Dec 2018 04:24:18 GMT。現行守則目錄沒有把它列為 2024 年修訂版。

## 一般指引：相關，但不是所找的守則或說明資料

目錄另有 *General Guidelines on Minor Works Control System*／小型工程監管制度之一般指引，並註明「The 2021 edition will be issued soon」／「2021年版本即將公布」。這是給公眾的一般指引；其英文前言寫明技術內容要另看 *Technical Guidelines on Minor Works Control System*。它不是作業守則，也不是該守則的 Explanatory Notes，所以沒有用來代替上面兩項缺漏。

是次打開的連結檔仍是 2010 年 10 月文本，不是目錄預告的 2021 年版：

| 文件 | PDF 所見 | 頁數 | bytes | SHA-256 |
|---|---|---|---|---|
| [英文合訂本](https://www.bd.gov.hk/doc/en/resources/codes-and-references/code-and-design-manuals/MW/MWGGe.pdf) | metadata 標題 “General Guidelines on Minor Works Control System”；免責聲明頁印 2010/10；CreationDate 2010-12-24。Last-Modified Wed, 13 Sep 2023 07:59:15 GMT | 65 | 38737976 | `dcc94a97f54edf29d92c4763a223918ccbec97137abe13ff7501485293252199` |
| [中文合訂本](https://www.bd.gov.hk/doc/tc/resources/codes-and-references/code-and-design-manuals/MW/MWGGc.pdf) | 封面「小型工程監管制度之一般指引」；metadata 標題少了「之」，作「小型工程監管制度一般指引」；免責聲明頁印 2010/10；CreationDate 2013-03-27。Last-Modified Wed, 13 Sep 2023 07:59:58 GMT | 65 | 38716876 | `9486c40b406ab76294528604803a13f9b0c57a87648a6298e76b048a30e42fef` |
| [英文附錄 (11/2014)](https://www.bd.gov.hk/doc/en/resources/codes-and-references/code-and-design-manuals/MW/VSFUSGGe.pdf) | metadata 標題 “Addendum: General Guidelines on Validation Scheme for Unauthorised Signboards”；內文實施日期 2013-09-02。CreationDate 2013-09-06 | 9 | 145458 | `3dab8001805769cfdbe03716929b51e7d89b2ef0b043e11dafb5772829c2fd25` |
| [中文附錄 (11/2014)](https://www.bd.gov.hk/doc/tc/resources/codes-and-references/code-and-design-manuals/MW/VSFUSGGc.pdf) | metadata 標題「附錄: 違例招牌檢核計劃之一般指引」。CreationDate 2013-09-06 | 8 | 388680 | `28ee5c306cac50e3f3589f468145ae54e4c6cf10980518758ffeb0b518cc18de` |

分章落地頁：<https://www.bd.gov.hk/en/resources/codes-and-references/codes-and-design-manuals/MWGG.html> 及 <https://www.bd.gov.hk/tc/resources/codes-and-references/codes-and-design-manuals/MWGG.html>。分章沒有全部下載。英文第 1 章 metadata 標題只是 “Introduction”，CreationDate 2010-12-24。

## 與本庫其他守則的分別

`documents/BD_CODES/` 及 `codes/manifest.json` 的五個系列（基礎、混凝土、鋼、恆載及外加荷載、風）沒有這些小型工程檔案，是次沒有重複加入。五個系列的下載及索引流程沒有改動。小型工程技術指引在取得屋宇署書面授權之前，不應按該流程把 PDF 提交到這個公開倉庫。
