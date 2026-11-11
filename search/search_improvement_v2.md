# 搜尋改善 v2：固定100題重測

2026-11-11。本次改搜尋程式；100題題目、參考答案、PDF索引及證據原文維持相同，舊報告未覆寫。這是搜尋結果比較，答案準確率仍未評分。

| 項目 | v1 | v2 |
|---|---:|---:|
| 中文：指定文件／條文在前10結果 | 58/100 | 97/100 |
| 中文：主要PDF頁／XML條文定位 | 50/100 | 72/100 |
| 英文關鍵字：指定文件／條文在前10結果 | 90/100 | 96/100 |
| 英文關鍵字：主要PDF頁／XML條文定位 | 90/100 | 87/100 |
| 中文：零結果 | 4/100 | 0/100 |
| 另12條補充題：指定文件／條文命中 | 8/12 | 12/12 |

加入相鄰頁補讀後，中文參考位置覆蓋為84/100；這個數字獨立報告，不當成主要頁定位。

**比較限制：v1為前10頁；v2為前10個不同PDF文件／法例條文，每份PDF只有一個主要頁。結果單位改變，因此是整體搜尋行為比較，不能稱為固定頁數下的隔離排序實驗。XML結果沒有PDF頁碼，以條文路徑核對。**

## 改了甚麼

- 單一搜尋引擎供CLI及常用topic JSON使用；不讀題庫、預期答案或測試標籤。
- 通用中文工程詞彙與英文縮寫擴展；長中文詞優先，GI接中文可識別，不會誤改digital等英文單字。
- APP25／APP-025等編號正規化並可直接定位文件；不是依題目ID分派答案。
- 以查詢詞覆蓋、標題、FTS分數及文件版次資料排序；每份PDF一個主要頁，另附相鄰頁及交叉引用／修訂資訊。
- PDF與法例條文一併搜尋；明確Cap.123 s20等查詢直接定位條文。XML頁碼固定null。
- 加入8個搜尋合約回歸測試，連既有法例測試共9個通過；Actions更新時自動重跑100題並保存結果。

## 未解決及退步

文件命中不代表已找到最有力的支持段落。原始文件覆蓋並非完整相關性判定，也不代表答案內容正確。HKIE／GEO版次提示不等於禁用歷史版本或完成所有修訂核證。

英文主要位置由90降至87，不能只報文件命中的改善。以下保留所有主要位置由命中轉為未命中的題目；部分可能在補讀頁找到，仍屬主要定位退步。

中文指定文件／條文仍未命中：A087、A097、A100。

中文主要位置退步：A032、A054、A066、A067、A068、A069、A070、A071、A091、A092、A094。

英文指定文件／條文仍未命中：A008、A015、A018、A056。

英文主要位置退步：A008、A018、A026、A027、A028、A029、A030、A033、A056、A091、A094。

補充12題在程式修改後編寫，未因其測試結果調整排序；包含GEO、wind、RC、steel等文件查找，但不是這些專題的答案核證。

下一步優先改善同一文件內段落／頁定位，處理英文退步及餘下3條中文未命中問題；正式答案評核仍須固定待評系統完整輸出，再逐項核對數值、範圍、例外及引用。

## 逐題比較

「文件」包括指定法例條文；「主位置」只算主要頁／條文；「含補讀」另算相鄰PDF頁。完整參考答案及原文位置見[固定題庫](../tests/answer_cases_v1.json)，原始結果見[舊結果](answer_retrieval_v1.json)、[新結果](answer_retrieval_v2.json)。

| ID | 問題 | 中文文件 v1→v2 | 中文主位置 v1→v2 | v2含補讀 |
|---|---|---|---|---|
| A001 | Scheduled Areas 做 GI，是否只要 consent、毋須 approval？ | 有→有 | 有→有 | 有 |
| A002 | Scheduled Areas 新 GI 要並行處理 approval 同 consent，GI 圖則要連同甚麼提交？ | 有→有 | 有→有 | 有 |
| A003 | GI approval 並行處理可以第32日便當作已獲 consent 開工嗎？ | 有→有 | 有→有 | 有 |
| A004 | 採用 Scheduled Areas GI 並行處理，covering letter 要寫甚麼？ | 有→有 | 有→有 | 有 |
| A005 | APP-30 可否當作所有 Scheduled Areas 都適用的備考？ | 無→有 | 無→有 | 有 |
| A006 | Mid-levels Scheduled Area No.1 GI 圖則是否包括 laboratory testing？ | 有→有 | 有→有 | 有 |
| A007 | Scheduled Area No.1 的岩土工作，甚麼階段要有 RGE input？ | 有→有 | 有→有 | 有 |
| A008 | Mid-levels GI 須對照邊兩本 Geoguide 及邊份一般 GI PNAP？ | 有→有 | 有→有 | 有 |
| A009 | Mid-levels  provisional BEL 通常多久收到？ | 有→有 | 有→有 | 有 |
| A010 | Mid-levels 是否每個重建項目都一定要求 performance review？ | 有→有 | 有→有 | 有 |
| A011 | 新建築 GBP 地盤最大坡度剛好15°，是否已觸發 APP-25 第2(a)(i)項？ | 無→有 | 無→有 | 有 |
| A012 | 大型地盤的 APP-25 坡度檢查只看全地盤平均值嗎？ | 無→有 | 無→有 | 有 |
| A013 | APP-25 的斜坡30°與7.5m高度是且還是或？ | 無→有 | 無→有 | 有 |
| A014 | APP-25 斜坡高度要否計埋坡腳或坡頂擋土牆？ | 無→有 | 無→有 | 有 |
| A015 | 斜坡在地盤外8m，能否只用 APP-25 第2(a)(ii) 的7.5m條件判定？ | 無→有 | 無→有 | 有 |
| A016 | APP-25 開挖深過7.5m就一定命中第2(a)(iii)嗎？ | 無→有 | 無→有 | 有 |
| A017 | APP-25 開挖面剛好10m是否屬於 longer than 10m？ | 無→有 | 無→有 | 有 |
| A018 | APP-25 開挖面長過10m，三個深度／位置條件要全部成立嗎？ | 無→有 | 無→有 | 有 |
| A019 | APP-25 深過7.5m的測量是否只看最終開挖狀態？ | 無→有 | 無→有 | 有 |
| A020 | APP-25 擋土牆相關45°面由牆頂還是牆趾投射？ | 無→有 | 無→有 | 有 |
| A021 | APP-25 的 HKPD −1m 適用所有地盤嗎？ | 有→有 | 有→有 | 有 |
| A022 | APP-25 地盤內擋土牆 retained height 剛好6m是否已滿足大於6m條件？ | 有→有 | 有→有 | 有 |
| A023 | APP-25 地盤外擋土牆的長度及距離條件是甚麼？ | 無→有 | 無→無 | 有 |
| A024 | A&A 沒有變成新建築，是否一定毋須 GBP 岩土評估？ | 無→有 | 無→無 | 有 |
| A025 | APP-25 要求 assessment 而 GBP 沒附上，文件有何後果提示？ | 無→有 | 無→無 | 無 |
| A026 | APP-56 四項豁免準則滿足任何一項就得？ | 無→有 | 無→有 | 有 |
| A027 | 新界豁免 SF 地段內界至界最大坡度可以剛好15°嗎？ | 無→有 | 無→有 | 有 |
| A028 | APP-56 地段外10m整體坡度可否剛好15°？ | 無→有 | 無→無 | 無 |
| A029 | APP-56 地段外10m內斜坡高1.6m但只有20°，是否符合第3(c)項？ | 無→有 | 無→無 | 無 |
| A030 | APP-56 第3(d)擋土牆限制只適用地段外嗎？ | 無→有 | 無→無 | 無 |
| A031 | 新界豁免 SF 新造1m牆上加1m斜坡，可以分開各自計1.5m嗎？ | 無→有 | 無→有 | 有 |
| A032 | APP-56 新建擋土牆 retained height 與 breadth 的比值上限是多少？ | 有→有 | 有→無 | 有 |
| A033 | APP-56 新建斜坡剛好30°兼高1.5m可否單憑第4(c)判作超限？ | 無→有 | 無→無 | 有 |
| A034 | APP-56 豁免準則或附帶條件做不到應點處理？ | 無→有 | 無→無 | 有 |
| A035 | 可否將 APP-56 的15°及1.5m當成全香港所有SF入則通用門檻？ | 無→有 | 無→有 | 有 |
| A036 | APP-57 第3段要求 ELS 圖則，深度、長度、影響條件是且還是或？ | 有→有 | 有→有 | 有 |
| A037 | 開挖深度剛好2.5m是否已滿足 APP-57 第3(a)深度門檻？ | 無→有 | 無→有 | 有 |
| A038 | 開挖長度剛好5m是否已滿足 APP-57 第3(a)長度門檻？ | 無→有 | 無→有 | 有 |
| A039 | APP-57 受影響斜坡角度是30°或以上嗎？ | 無→有 | 無→有 | 有 |
| A040 | APP-57 水管直徑剛好75mm是否在列明類別內？ | 無→有 | 無→有 | 有 |
| A041 | APP-57 影響範圍45°線由邊個位置起？ | 無→有 | 無→有 | 有 |
| A042 | 已觸發 APP-57 第3段但 ELS 圖未批，可否只申請 consent 開工？ | 有→有 | 有→有 | 有 |
| A043 | 需要入則的 ELS，圖則及結構設計由誰準備簽署？ | 有→有 | 有→有 | 有 |
| A044 | ELS 深度剛好4.5m是否已命中 APP-57 第5段 deeper than 4.5m？ | 有→有 | 有→有 | 有 |
| A045 | ELS 深過4.5m，RGE 應簽甚麼？ | 有→有 | 有→有 | 有 |
| A046 | ELS 可分兩階段入則，第一階段要否證明整個方案可行？ | 有→有 | 無→有 | 有 |
| A047 | ELS 第一階段是否可延後全部岩土支持文件？ | 有→有 | 有→有 | 有 |
| A048 | ELS 第一階段圖則應顯示哪些主要內容？ | 有→有 | 有→有 | 有 |
| A049 | APP-57 initial-stage ELS 可以直接挖到第二層支撐嗎？ | 有→有 | 有→有 | 有 |
| A050 | APP-57 GFM 有效應力排水分析抗傾覆／牆趾穩定最低 global FOS？ | 有→有 | 有→有 | 有 |
| A051 | APP-57 GFM 總應力不排水分析抗傾覆／牆趾穩定最低 global FOS？ | 有→有 | 有→有 | 有 |
| A052 | ELS 可否同一設計混用 GFM 同 PFM？ | 有→有 | 有→有 | 有 |
| A053 | ELS 採 GFM 或 PFM，submission procedures 是否不同？ | 有→有 | 有→有 | 有 |
| A054 | 同一程式支援 GFM/PFM，一次 prior acceptance 是否自動涵蓋兩者？ | 有→有 | 有→無 | 有 |
| A055 | APP-57 base heave 及 hydraulic failure 最低 FOS 是多少？ | 有→有 | 有→有 | 有 |
| A056 | ELS design report 要否 RSE 同 RGE certification？ | 有→有 | 無→無 | 無 |
| A057 | APP-57 最低限度監測是否只有 pile wall deflection？ | 有→有 | 無→有 | 有 |
| A058 | APP-57 PFM surcharge partial load factor 可以直接用 GEO 的1.3？ | 有→有 | 有→有 | 有 |
| A059 | APP-57 PFM 結構設計的 SLS forces 及 bending moments 要乘多少？ | 有→有 | 有→有 | 有 |
| A060 | PFM ULS 已按 APP-57 Appendix A 驗算，還須重做 GFM 力矩不穩定1.5／2.0嗎？ | 有→有 | 有→有 | 有 |
| A061 | 小直徑 bored pile 直徑剛好750mm屬哪一邊？ | 無→有 | 無→有 | 有 |
| A062 | CFA 在 Code 中屬哪種 bored pile？ | 有→有 | 有→有 | 有 |
| A063 | CFA 土層 N 大過40是否一律不可作設計？ | 有→有 | 有→有 | 有 |
| A064 | CFA 公式的樁端 Nb 上限是否也是40？ | 有→有 | 有→有 | 有 |
| A065 | CFA 公式 Nav 是樁端值還是沿樁身平均值？ | 有→有 | 有→有 | 有 |
| A066 | CFA 冇做 trial pile，公式 friction factor 可以直接用1.6嗎？ | 有→有 | 有→無 | 有 |
| A067 | CFA 每段 grout factor 是每1m還是1.5m記錄？ | 有→有 | 有→無 | 有 |
| A068 | CFA working pile 每1.5m grout factor 最低只要1.15就得？ | 有→有 | 有→無 | 有 |
| A069 | CFA working pile total grout factor 最低只要1.4就得？ | 有→有 | 有→無 | 有 |
| A070 | CFA 深處 drilling refusal 在此節用甚麼 penetration rate界定？ | 有→有 | 有→無 | 有 |
| A071 | CFA 深處拒進且距已完成CFA小於6D，Code列甚麼可考慮處理？ | 有→有 | 有→無 | 有 |
| A072 | CFA 深處拒進且不小於6D，可清障後原位重裝便照計上部摩擦嗎？ | 有→有 | 有→有 | 有 |
| A073 | 大直徑 bored pile 的直徑以甚麼作準？ | 無→有 | 無→無 | 無 |
| A074 | 大直徑 bored pile 成孔時可否抽乾孔內水？ | 無→有 | 無→無 | 無 |
| A075 | Bored pile bell-out 最大直徑係幾多？ | 無→有 | 無→有 | 有 |
| A076 | Bored pile bell-out 30°係由水平量起嗎？ | 無→有 | 無→無 | 無 |
| A077 | Bell-out end bearing 加 rock socket摩擦一起計，socket有效長度上限？ | 有→有 | 有→有 | 有 |
| A078 | 冇bell-out，端承加socket阻力一起計，可計socket多長？ | 無→有 | 無→有 | 有 |
| A079 | 小直徑 bored pile 在 fill／marine deposit 的摩擦一定可計嗎？ | 有→有 | 有→有 | 有 |
| A080 | 陡峭bedrock下相鄰bored pile founding level差值可以任意大？ | 有→有 | 無→無 | 無 |
| A081 | Site investigation 同 ground investigation 是否完全同義？ | 有→有 | 有→有 | 有 |
| A082 | 一般 GI 可否只靠 ADM-16 作唯一規範來源？ | 有→有 | 有→有 | 有 |
| A083 | APP-49 2025版指基礎SI應配合哪個 Foundations Code版次？ | 無→有 | 無→有 | 有 |
| A084 | GIFW 包唔包括 laboratory testing 同 field density tests？ | 有→有 | 有→有 | 有 |
| A085 | 一般 GIFW 可以由任何鑽探公司做嗎？ | 有→有 | 有→有 | 有 |
| A086 | GI 某些operation分判畀人，RSC是否就不用負責報告資料？ | 有→有 | 無→有 | 有 |
| A087 | GI岩芯是否鑽完即可以丟棄？ | 有→無 | 無→無 | 無 |
| A088 | GI/LT digital submission 只交PDF夠嗎？ | 無→有 | 無→有 | 有 |
| A089 | GI各站報告檔名可以同一project內重複嗎？ | 有→有 | 無→有 | 有 |
| A090 | AGS data 可以分拆數個檔案，或用非ASCII文字格式嗎？ | 有→有 | 有→有 | 有 |
| A091 | HKIE Foundations 2017 explanatory handbook 是哪個機構出版？ | 有→有 | 有→無 | 無 |
| A092 | HKIE Foundations 2017 手冊的本版出版月份係甚麼？ | 有→有 | 有→無 | 無 |
| A093 | HKIE Foundations handbook 自己有否聲明內容效力？ | 有→有 | 無→無 | 無 |
| A094 | HKIE 2019 Foundations handbook 可以自動當成已包含2024 Edition同2025 amendments嗎？ | 有→有 | 有→無 | 無 |
| A095 | HKIE手冊建議是否可以不理個案事實直接套用？ | 無→有 | 無→有 | 有 |
| A096 | 取得 consent 後幾耐唔開工會被視為撤銷？ | 無→有 | 無→有 | 有 |
| A097 | 已開工便一定毋須再理 consent 的3個月規則？ | 無→無 | 無→無 | 無 |
| A098 | Cap.123 s20 consent 續期是否BA只能無條件批？ | 無→有 | 無→有 | 有 |
| A099 | 有 approved plans 是否即等於有 commencement consent？ | 無→有 | 無→有 | 有 |
| A100 | BA 可否只同意已批圖則工程的一部分開工？ | 無→無 | 無→無 | 無 |

## 重現

```sh
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/review_answer_cases.py
python scripts/check_retrieval_examples.py
python scripts/build_search_improvement_report.py
python scripts/build_retrieval.py
```

12題補充測試需本機git含基準commit d5ae073；一般Actions重跑100題不依賴此舊git物件。所有搜尋、排序及測試只用本地SQLite／Python，不呼叫模型API。
