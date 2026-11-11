# RSE 100條新參考題：原文核對與搜尋結果

日期：2026-11-11。**已整理100條不同的原文參考題並逐題實跑搜尋；沒有100份歷史完整答案可供評分。以下不是100題答案準確率認證。**

原文及搜尋基準commit：`1192cc4299a4811a72be01456ffdf0aafe2c9da9`。本次保留主分支原有搜尋邏輯，沒有把未合併PR的改善成績當成現行結果。

| 實測項目 | 結果 |
|---|---:|
| 新的不同中文問題及AI原文核對參考答案 | 100 |
| 中文完整問題：前10頁找到指定文件 | 58/100 |
| 中文完整問題：前10頁找到指定參考頁 | 50/100 |
| 中文完整問題：零搜尋結果 | 4/100 |
| 英文關鍵字診斷：前10頁找到指定文件 | 90/100 |
| 英文關鍵字診斷：前10頁找到指定參考頁 | 90/100 |
| 搜尋執行錯誤（中文／英文） | 0/0 |
| 本次獨立官方PDF副本比對一致 | 10/10 |
| 本次DOJ官方英文XML比對一致 | 2/2 |
| 歷史完整答案評分／獨立專業審定 | 0／0 |
| 答案準確率 | 未評分（null） |

「指定參考頁命中」只比對文件路徑及實體頁地址。參考答案由同一AI依原文整理，沒有獨立專業評核。未命中不代表原文沒有規定；命中也不代表系統能正確解釋條件。

範圍：GI、Mid-levels、GBP assessment、新界SF豁免、ELS、bored/CFA piles、HKIE基礎手冊角色及consent。未涵蓋全庫GEO、wind、RC、steel與APSEC。

## 已定位的問題與改善次序

1. 中文完整問句與英文關鍵字的成績有差距。應改善中文同義詞與數值／條件語境，並用額外新題驗證，避免對100題直接硬編碼。
2. 主分支這個頁級搜尋函式沒有整合法例資料庫；5題consent法例均未能命中法例原文，不能把PNAP一般搜尋結果當作條文已找到。
3. 英文診斷另有5題未命中指定PNAP，見下列清單；應檢查排序、長文件多頁佔位及條件語句的選詞。
4. 文件找到與答案完整仍是兩層驗證；正式評分須先固定待測系統的完整答案，再對照原文及參考答案逐項評核。

英文診斷未命中：A013、A014、A015、A040、A045、A096、A097、A098、A099、A100。

## 逐題參考答案及結果

表內「文件／頁」分別表示指定文件、指定參考實體頁有否出現在中文完整問題的前10頁搜尋結果；不是答案正誤。所有頁碼均為PDF實體頁；法例XML沒有PDF頁碼。每題完整適用範圍及版次見題庫JSON。

| ID | 問題 | 原文核對參考答案 | Refer to | 中文文件／頁 |
|---|---|---|---|---|
| A001 | Scheduled Areas 做 GI，是否只要 consent、毋須 approval？ | 兩者都需要；ADM-16 第1段把 Scheduled Areas 的 GI 列為 building works，要求 approval 及 consent。 | [ADM-16](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/ADM/ADM-16.txt) para 1；PDF 1 | 有／有 |
| A002 | Scheduled Areas 新 GI 要並行處理 approval 同 consent，GI 圖則要連同甚麼提交？ | 須連同 site supervision plan 提交，並符合第3(b)段的信件及申請時間要求。 | [ADM-16](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/ADM/ADM-16.txt) para 3(a)-(b)；PDF 1 | 有／有 |
| A003 | GI approval 並行處理可以第32日便當作已獲 consent 開工嗎？ | 不可以。條文指在 approval 圖則提交第32日之後提出 consent 申請，並非第32日自動獲同意。 | [ADM-16](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/ADM/ADM-16.txt) para 3(b)；PDF 1 | 有／有 |
| A004 | 採用 Scheduled Areas GI 並行處理，covering letter 要寫甚麼？ | 須表明希望採用 concurrent processing option；另須提交 supervision plan，並在圖則提交第32日之後申請 consent。 | [ADM-16](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/ADM/ADM-16.txt) para 3(a)-(b)；PDF 1 | 有／有 |
| A005 | APP-30 可否當作所有 Scheduled Areas 都適用的備考？ | 不可；其範圍是 Mid-levels Scheduled Area No.1。其他地區應查各自適用文件。 | [APP-030](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-030.txt) para 1；PDF 1 | 無／無 |
| A006 | Mid-levels Scheduled Area No.1 GI 圖則是否包括 laboratory testing？ | 是。第3段指須按 B(A)R 8(1)(l)提交包括 laboratory testing 的 GI 圖則，並於開工前取得 approval 及 consent。 | [APP-030](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-030.txt) para 3；PDF 1 | 有／有 |
| A007 | Scheduled Area No.1 的岩土工作，甚麼階段要有 RGE input？ | 所有岩土方面工作均需要 RGE input，尤其工程早期規劃；並須委任 RGE 處理相關岩土工作。 | [APP-030](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-030.txt) para 2；PDF 1 | 有／有 |
| A008 | Mid-levels GI 須對照邊兩本 Geoguide 及邊份一般 GI PNAP？ | APP-30 第4段列 Geoguide 2、Geoguide 3 及 APP-49；這是交叉引用清單，詳細技術要求須再讀各文件。 | [APP-030](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-030.txt) para 4；PDF 1 | 有／有 |
| A009 | Mid-levels  provisional BEL 通常多久收到？ | GEO 收到要求後通常10個工作天提供 tentative BEL 圖；這是暫定資料，不能當作最終 BEL agreement。 | [APP-030](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-030.txt) para 7；PDF 2 | 有／有 |
| A010 | Mid-levels 是否每個重建項目都一定要求 performance review？ | 不是。第11段明確指並非打算對每個發展／重建地盤施加；可在 approval 或 consent 時附加。 | [APP-030](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-030.txt) para 11；PDF 2 | 有／有 |
| A011 | 新建築 GBP 地盤最大坡度剛好15°，是否已觸發 APP-25 第2(a)(i)項？ | 未單憑此項觸發；該項是大於15°，不是大於或等於15°。仍須核對第2段其他獨立條件。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(a)(i)；PDF 1 | 無／無 |
| A012 | 大型地盤的 APP-25 坡度檢查只看全地盤平均值嗎？ | 不是；條文包括 across any 50 m long strip 的最大坡度大於15°。亦須核對其他觸發項。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(a)(i)；PDF 1 | 無／無 |
| A013 | APP-25 的斜坡30°與7.5m高度是且還是或？ | 該項要求斜坡角度大於30°且高度大於7.5m，並位於地盤內或距地盤7.5m內；不能改成任一成立。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(a)(ii)；PDF 1 | 無／無 |
| A014 | APP-25 斜坡高度要否計埋坡腳或坡頂擋土牆？ | 要；第2(a)(ii)項明確包括坡腳或坡頂擋土牆高度，並保留該項角度、高度及位置條件。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(a)(ii)；PDF 1 | 無／無 |
| A015 | 斜坡在地盤外8m，能否只用 APP-25 第2(a)(ii) 的7.5m條件判定？ | 不能單憑此項；該項限地盤內或7.5m內，且另有角度與高度條件。其他觸發項或風險仍須查。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(a)(ii)；PDF 1 | 無／無 |
| A016 | APP-25 開挖深過7.5m就一定命中第2(a)(iii)嗎？ | 還要開挖面長度大於10m；長度條件須與三項替代情況之一同時成立。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(a)(iii)；PDF 1 | 無／無 |
| A017 | APP-25 開挖面剛好10m是否屬於 longer than 10m？ | 不是；該項是嚴格大於10m。但不能據此排除其他 assessment 要求。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(a)(iii)；PDF 1 | 無／無 |
| A018 | APP-25 開挖面長過10m，三個深度／位置條件要全部成立嗎？ | 不用；長度大於10m，且深過7.5m、低於擋土牆牆趾向下45°平面、或填海岸地低於HKPD −1m，三者任一。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(a)(iii)(1)-(3)；PDF 1 | 無／無 |
| A019 | APP-25 深過7.5m的測量是否只看最終開挖狀態？ | 不是；條文是任何位置、任何階段深於7.5m，並須符合開挖面長過10m的前提。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(a)(iii)(1)；PDF 1 | 無／無 |
| A020 | APP-25 擋土牆相關45°面由牆頂還是牆趾投射？ | 由擋土牆牆趾向下45°投射；並須符合開挖面長過10m等該項條件。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(a)(iii)(2)；PDF 1 | 無／無 |
| A021 | APP-25 的 HKPD −1m 適用所有地盤嗎？ | 不是；該分項是 reclaimed coastal land，並須符合開挖面長過10m前提。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(a)(iii)(3)；PDF 1 | 有／有 |
| A022 | APP-25 地盤內擋土牆 retained height 剛好6m是否已滿足大於6m條件？ | 沒有；第2(a)(iv)的牆高是大於6m。其他觸發項仍須核對。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(a)(iv)；PDF 1 | 有／有 |
| A023 | APP-25 地盤外擋土牆的長度及距離條件是甚麼？ | 對高度大於6m的牆，若有長度6m或以上的一段位於地盤6m內，屬該項情況；高度、長度、距離不能互換。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(a)(iv)；PDF 1 | 無／無 |
| A024 | A&A 沒有變成新建築，是否一定毋須 GBP 岩土評估？ | 不是；如對現有岩土設施及鄰近基礎可能有重大影響，或涉及第2(a)(iii)開挖，仍屬第2(b)情況。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 2(b)；PDF 2 | 無／無 |
| A025 | APP-25 要求 assessment 而 GBP 沒附上，文件有何後果提示？ | 第4段指可能按 Cap.123 s16(1)(a) 拒絕該 GBP submission；不是把此條當作所有SF工程的判定。 | [APP-025](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-025.txt) para 4；PDF 3 | 無／無 |
| A026 | APP-56 四項豁免準則滿足任何一項就得？ | 不是；第3段要求所有準則均符合，才會由相關 District Lands Officer 考慮發出 SF 豁免證明。 | [APP-056](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-056.txt) para 3；PDF 1 | 無／無 |
| A027 | 新界豁免 SF 地段內界至界最大坡度可以剛好15°嗎？ | 就第3(a)項而言可以，因為是不超過15°；但所有其他準則及證書條件亦須符合。 | [APP-056](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-056.txt) para 3(a)；PDF 1 | 無／無 |
| A028 | APP-56 地段外10m整體坡度可否剛好15°？ | 不符合第3(b)項，該項要求少於15°；與地段內不超過15°不同。 | [APP-056](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-056.txt) para 3(b)；PDF 1 | 無／無 |
| A029 | APP-56 地段外10m內斜坡高1.6m但只有20°，是否符合第3(c)項？ | 不符合；不得有斜坡陡於30°或高於1.5m，任何一項超限均不符。 | [APP-056](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-056.txt) para 3(c)；PDF 1 | 無／無 |
| A030 | APP-56 第3(d)擋土牆限制只適用地段外嗎？ | 不是；地段內或地段外10m範圍內的 retaining wall／terrace wall，均不得高於1.5m。 | [APP-056](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-056.txt) para 3(d)；PDF 1 | 無／無 |
| A031 | 新界豁免 SF 新造1m牆上加1m斜坡，可以分開各自計1.5m嗎？ | 不可以；第4(a)規定新建牆及斜坡的合計高度也不得超過1.5m。 | [APP-056](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-056.txt) para 4(a)；PDF 2 | 無／無 |
| A032 | APP-56 新建擋土牆 retained height 與 breadth 的比值上限是多少？ | 不大於2，且新建擋土牆須以 masonry 或 concrete 建造；仍受其他證書條件約束。 | [APP-056](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-056.txt) para 4(b)；PDF 2 | 有／有 |
| A033 | APP-56 新建斜坡剛好30°兼高1.5m可否單憑第4(c)判作超限？ | 不能；第4(c)禁止陡於30°或高於1.5m。惟仍須符合全部豁免準則及其他條件。 | [APP-056](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-056.txt) para 4(c)；PDF 2 | 無／無 |
| A034 | APP-56 豁免準則或附帶條件做不到應點處理？ | 第5段要求按正常程序向 BD 提交規定的 site formation 圖則；不是擅自忽略超限。 | [APP-056](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-056.txt) para 5；PDF 2 | 無／無 |
| A035 | 可否將 APP-56 的15°及1.5m當成全香港所有SF入則通用門檻？ | 不可；文件限與新界豁免建築工程相關的SF豁免制度，須與GBP岩土評估、ELS及一般法定要求分開。 | [APP-056](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-056.txt) paras 1-5；PDF 1, 2 | 無／無 |
| A036 | APP-57 第3段要求 ELS 圖則，深度、長度、影響條件是且還是或？ | 深度大於2.5m且長度大於5m，並且可能影響列明設施／斜坡；影響範圍按由開挖底向上45°至地面界定。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 3；PDF 1 | 有／有 |
| A037 | 開挖深度剛好2.5m是否已滿足 APP-57 第3(a)深度門檻？ | 未滿足嚴格大於2.5m這個分項；但不能據此作無須任何圖則或安全措施的總結。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 3(a)；PDF 1 | 無／無 |
| A038 | 開挖長度剛好5m是否已滿足 APP-57 第3(a)長度門檻？ | 未滿足嚴格大於5m這個分項；須另查其他適用要求及風險。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 3(a)；PDF 1 | 無／無 |
| A039 | APP-57 受影響斜坡角度是30°或以上嗎？ | 該段列的是陡於30°；並須結合開挖尺寸、可能影響及45°範圍等條件。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 3(b)；PDF 1 | 無／無 |
| A040 | APP-57 水管直徑剛好75mm是否在列明類別內？ | 是，條文是75mm或以上；但仍須同時評估開挖深度、長度及可能影響等條件。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 3(b)；PDF 1 | 無／無 |
| A041 | APP-57 影響範圍45°線由邊個位置起？ | 由開挖底部向上45°至地面；不是由地面向下任意畫線。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 3(b)；PDF 1 | 無／無 |
| A042 | 已觸發 APP-57 第3段但 ELS 圖未批，可否只申請 consent 開工？ | 第4段指未提交並批准規定的 ELS 圖則，不會發出 ELS 開工 consent。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 4；PDF 1 | 有／有 |
| A043 | 需要入則的 ELS，圖則及結構設計由誰準備簽署？ | 須由 RSE 準備及簽署圖則、結構設計，以及開挖／降水對鄰近結構影響的結構評估報告。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 5；PDF 1 | 有／有 |
| A044 | ELS 深度剛好4.5m是否已命中 APP-57 第5段 deeper than 4.5m？ | 未單憑深度命中該項，因為條文是大於4.5m；不能用來排除其他RGE要求。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 5；PDF 1 | 有／有 |
| A045 | ELS 深過4.5m，RGE 應簽甚麼？ | 當屬須提交的ELS圖則，RGE須準備及簽署隨圖則提交的岩土支持文件，例如評估、詳情、計算及相關報告。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 5；PDF 1 | 有／有 |
| A046 | ELS 可分兩階段入則，第一階段要否證明整個方案可行？ | 要；兩階段安排以第一階段展示整個方案可行為前提。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 6；PDF 2 | 有／無 |
| A047 | ELS 第一階段是否可延後全部岩土支持文件？ | 不可；第6段要求第一階段亦提供支持岩土文件，並有整體真實地面變形估算。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 6；PDF 2 | 有／有 |
| A048 | ELS 第一階段圖則應顯示哪些主要內容？ | 擋土樁牆系統、支撐佈置及施工次序；並須展示全方案可行及提供所需支持文件。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 6；PDF 2 | 有／有 |
| A049 | APP-57 initial-stage ELS 可以直接挖到第二層支撐嗎？ | 不能按該定義這樣做；限挖至第一層支撐底而不超過現有地面以下1.5m，並安裝首層圍檁及支撐，依批准圖則。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 6 footnote 1；PDF 2 | 有／有 |
| A050 | APP-57 GFM 有效應力排水分析抗傾覆／牆趾穩定最低 global FOS？ | 1.5；這是GFM有效應力排水分析的要求，不能混同PFM或其他破壞模式。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 7；PDF 2 | 有／有 |
| A051 | APP-57 GFM 總應力不排水分析抗傾覆／牆趾穩定最低 global FOS？ | 2.0；其註腳指埋置牆失去力矩平衡的安全系數作用於被動土壓力，水壓不加系數。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 7 footnote 2；PDF 2 | 有／有 |
| A052 | ELS 可否同一設計混用 GFM 同 PFM？ | 第9段明確不允許兩種方法混合；圖則及計算須列明採用方法。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 9；PDF 2 | 有／有 |
| A053 | ELS 採 GFM 或 PFM，submission procedures 是否不同？ | 第9段說提交程序相同；但須在圖則及計算列明設計方法，亦不可混用。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 9；PDF 2 | 有／有 |
| A054 | 同一程式支援 GFM/PFM，一次 prior acceptance 是否自動涵蓋兩者？ | 不是；第10段要求每種方法分別申請程式 prior acceptance，並參閱ADM-6的一般要求。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) para 10；PDF 3 | 有／有 |
| A055 | APP-57 base heave 及 hydraulic failure 最低 FOS 是多少？ | Appendix A §2.3.1要求最低1.5，並按GEO Publication 1/2023 §§6.2.3、6.2.4；不可用此數代替其他穩定驗算。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) Appendix A 2.3.1；PDF 4 | 有／有 |
| A056 | ELS design report 要否 RSE 同 RGE certification？ | Appendix A §2.4.1要求由RSE及RGE認證，並作關於倒塌安全裕度及在假設驗證／施工按要求下無不可接受影響的聲明。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) Appendix A 2.4.1；PDF 4, 5 | 有／無 |
| A057 | APP-57 最低限度監測是否只有 pile wall deflection？ | 不是；Appendix A §2.4.4最少要監測地面沉降／隆起及地下水壓讀數；重大生命財產風險時另須更多監測。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) Appendix A 2.4.4；PDF 5 | 有／無 |
| A058 | APP-57 PFM surcharge partial load factor 可以直接用 GEO 的1.3？ | 不可以；Appendix A §3.2.1要求用1.5取代GEO Publication 1/2023的1.3。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) Appendix A 3.2.1；PDF 5 | 有／有 |
| A059 | APP-57 PFM 結構設計的 SLS forces 及 bending moments 要乘多少？ | Appendix A §3.3.1要求乘1.4；§3.3.2仍可能要求按相關結構規範partial factors補充驗算。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) Appendix A 3.3.1-3.3.2；PDF 5 | 有／有 |
| A060 | PFM ULS 已按 APP-57 Appendix A 驗算，還須重做 GFM 力矩不穩定1.5／2.0嗎？ | §3.4.2說按該Appendix建議完成ULS驗算時，毋須另做GFM所需的1.5／2.0力矩不穩定驗算；其他要求仍適用。 | [APP-057](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-057.txt) Appendix A 3.4.2；PDF 6 | 有／有 |
| A061 | 小直徑 bored pile 直徑剛好750mm屬哪一邊？ | §5.4.6(1)為不超過750mm；大直徑§5.4.7為大於750mm，兩者邊界不可寫反。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.6(1);5.4.7；PDF 76, 77 | 無／無 |
| A062 | CFA 在 Code 中屬哪種 bored pile？ | §5.4.6(2)把CFA列為small diameter bored pile的一種；不能只因名稱就忽略對該樁型的限制。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.6(2)；PDF 76 | 有／有 |
| A063 | CFA 土層 N 大過40是否一律不可作設計？ | 該節不是全面排除N>40的土；公式中的樁身平均Nav取值不得超過40。實際可行性仍須地層、施工、試樁等證據判定。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.6(2)；PDF 76 | 有／有 |
| A064 | CFA 公式的樁端 Nb 上限是否也是40？ | 不是；樁身平均Nav上限40，樁端Nb上限200。兩個參數不可混淆。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.6(2)；PDF 76 | 有／有 |
| A065 | CFA 公式 Nav 是樁端值還是沿樁身平均值？ | Nav是沿樁身的平均SPT N值，取值不超過40；Nb才是樁端SPT N值，取值不超過200。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.6(2)；PDF 76 | 有／有 |
| A066 | CFA 冇做 trial pile，公式 friction factor 可以直接用1.6嗎？ | 不能；未做trial pile可用1.0，有trial pile充分證明才可將friction factor上限提高至1.6。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.6(2)；PDF 77 | 有／有 |
| A067 | CFA 每段 grout factor 是每1m還是1.5m記錄？ | 試樁須記總grout factor及每1.5m增量的grout factor，用於檢查working piles。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.6(2)；PDF 77 | 有／有 |
| A068 | CFA working pile 每1.5m grout factor 最低只要1.15就得？ | 還不得低於試樁最小1.5m增量grout factor；兩項同時滿足，且任何情況不小於1.15。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.6(2)(a)；PDF 77 | 有／有 |
| A069 | CFA working pile total grout factor 最低只要1.4就得？ | 還不得低於試樁total grout factor；兩項同時滿足，且任何情況不小於1.4。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.6(2)(b)；PDF 77 | 有／有 |
| A070 | CFA 深處 drilling refusal 在此節用甚麼 penetration rate界定？ | 少於300mm/min；這是該段深處鑽進拒進的定義，不能改成小於或等於。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.6(2)；PDF 77 | 有／有 |
| A071 | CFA 深處拒進且距已完成CFA小於6D，Code列甚麼可考慮處理？ | 該段列鑽孔用水泥漿回填並搬樁；適用於深處拒進、距已完成CFA小於6個樁徑的情況。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.6(2)(a)；PDF 77 | 有／有 |
| A072 | CFA 深處拒進且不小於6D，可清障後原位重裝便照計上部摩擦嗎？ | 不可照計；可按該段以合適方法清障、砂回填再重裝，但須重估樁長並忽略障礙以上土層樁身摩擦貢獻。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.6(2)(b)；PDF 77 | 有／有 |
| A073 | 大直徑 bored pile 的直徑以甚麼作準？ | §5.4.7指樁身直徑大於750mm，並以臨時鋼套管外徑作樁身直徑。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.7；PDF 77 | 無／無 |
| A074 | 大直徑 bored pile 成孔時可否抽乾孔內水？ | 該節要求在水或合適流體如bentonite下鑽進，不允許為孔內開挖降水；支護及其他條件亦須符合。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.7；PDF 77 | 無／無 |
| A075 | Bored pile bell-out 最大直徑係幾多？ | 在准許bell-out的情況，其直徑不得超過樁身直徑1.65倍；並受由垂直量起不超過30°的斜度限制。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.7；PDF 78 | 無／無 |
| A076 | Bored pile bell-out 30°係由水平量起嗎？ | 不是；條文是from vertical，即由垂直方向量起，且不超過30°。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.7；PDF 78 | 無／無 |
| A077 | Bell-out end bearing 加 rock socket摩擦一起計，socket有效長度上限？ | 不得超過1倍rock socket直徑或3m，取較短者；並須忽略bell-out正上方750mm一段的socket阻力。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.7；PDF 78 | 有／有 |
| A078 | 冇bell-out，端承加socket阻力一起計，可計socket多長？ | 該組合的socket計算長度不得超過2倍rock socket直徑或6m，取較短者；不要套用有bell-out的1D／3m。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.7；PDF 78 | 無／無 |
| A079 | 小直徑 bored pile 在 fill／marine deposit 的摩擦一定可計嗎？ | 通常應忽略，除非證明未來不可能再固結；並須按§5.2考慮negative skin friction。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.6(1)；PDF 76 | 有／有 |
| A080 | 陡峭bedrock下相鄰bored pile founding level差值可以任意大？ | 一般不得大於樁基底間淨距；例外需按認可工程原理核證樁下岩石穩定並考慮不利節理。 | [FoundationCode2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/BD_CODES/foundations/FoundationCode2017.txt) 5.4.7；PDF 78 | 有／無 |
| A081 | Site investigation 同 ground investigation 是否完全同義？ | 不是；SI範圍較廣，包含文獻、地盤測量及GI；GI是實際地表／地下勘測，如鑽孔、試坑及現場／實驗室試驗。 | [APP-049](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-049.txt) paras 1-2；PDF 1 | 有／有 |
| A082 | 一般 GI 可否只靠 ADM-16 作唯一規範來源？ | 不可；一般SI/GI應讀APP-49，另按問題讀Geoguide2／3、TGN1及基礎Code；ADM-16限Scheduled Areas。 | [APP-049](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-049.txt) paras 1-3；PDF 1 | 有／有 |
| A083 | APP-49 2025版指基礎SI應配合哪個 Foundations Code版次？ | Code of Practice for Foundations 2017 (2024 Edition)，並按TGN1所列相關岩土技術指引；亦須另查適用修訂。 | [APP-049](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-049.txt) para 3；PDF 1 | 無／無 |
| A084 | GIFW 包唔包括 laboratory testing 同 field density tests？ | 在APP-49的GIFW定義中不包括兩者；這兩類試驗須由就有關試驗獲認可的實驗室進行。 | [APP-049](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-049.txt) para 4；PDF 1 | 有／有 |
| A085 | 一般 GIFW 可以由任何鑽探公司做嗎？ | 第4段要求所有GIFW由RSC(GIFW)進行；詳細工作範圍及註冊要求另見APP-96。 | [APP-049](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-049.txt) para 4；PDF 1 | 有／有 |
| A086 | GI 某些operation分判畀人，RSC是否就不用負責報告資料？ | 不是；第6段要求RSC(GIFW)確保提交BA的GI報告全部資料正確，即使部分作業由其他人做。 | [APP-049](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-049.txt) para 6；PDF 2 | 有／無 |
| A087 | GI岩芯是否鑽完即可以丟棄？ | 不是；除被選作試驗樣本外，岩芯與樣本須妥善保存，直至相關SF、基礎或其他工程獲滿意完成的acknowledgement。 | [APP-049](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-049.txt) para 6；PDF 2 | 有／無 |
| A088 | GI/LT digital submission 只交PDF夠嗎？ | 不夠；第8段要求PDF及AGS data format兩者，包括本地Geoguide2／3描述及工程性質所需增修。 | [APP-049](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-049.txt) para 8；PDF 2 | 無／無 |
| A089 | GI各站報告檔名可以同一project內重複嗎？ | 第8(a)段要求各GI站PDF連同相片，且每站檔名在該項目內須唯一。 | [APP-049](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-049.txt) para 8(a)；PDF 2 | 有／無 |
| A090 | AGS data 可以分拆數個檔案，或用非ASCII文字格式嗎？ | 第8(b)段要求ASCII文字格式，而且不可分拆成部分。 | [APP-049](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/PNAP/APP/APP-049.txt) para 8(b)；PDF 3 | 有／有 |
| A091 | HKIE Foundations 2017 explanatory handbook 是哪個機構出版？ | HKIE Structural Division（香港工程師學會結構分部），不是BD發出的法例或PNAP。 | [HKIE-foundations-2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/HKIE/HKIE-foundations-2017.txt) publication page；PDF 2 | 有／有 |
| A092 | HKIE Foundations 2017 手冊的本版出版月份係甚麼？ | 出版頁列June 2019；不能因repo近日下載便當成2026年新版。 | [HKIE-foundations-2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/HKIE/HKIE-foundations-2017.txt) publication page；PDF 2 | 有／有 |
| A093 | HKIE Foundations handbook 自己有否聲明內容效力？ | 第3實體頁說明內容為意見，並不提供任何明示或默示保證；應按個案事實審視。 | [HKIE-foundations-2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/HKIE/HKIE-foundations-2017.txt) disclaimer；PDF 3 | 有／無 |
| A094 | HKIE 2019 Foundations handbook 可以自動當成已包含2024 Edition同2025 amendments嗎？ | 不可作此假設；出版頁為2019年。須另外讀現行BD Code及其2025修訂、APP-18，不能以手冊取代。 | [HKIE-foundations-2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/HKIE/HKIE-foundations-2017.txt) publication page; disclaimer；PDF 2, 3 | 有／有 |
| A095 | HKIE手冊建議是否可以不理個案事實直接套用？ | 手冊聲明要求使用者按個案事實審視指引及建議；引用它不等於已證明個案符合法例或Code。 | [HKIE-foundations-2017](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/indexed_text/HKIE/HKIE-foundations-2017.txt) disclaimer；PDF 3 | 無／無 |
| A096 | 取得 consent 後幾耐唔開工會被視為撤銷？ | Cap.123 s20(1)：取得consent後3個月內未開工，該consent視為撤銷；s20(2)容許向BA申請續期，並可附條件。 | [s20](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/legislation/provisions/cap123/en/s20.json) s20(1)-(2)；XML，無PDF頁碼 | 無／無 |
| A097 | 已開工便一定毋須再理 consent 的3個月規則？ | 不是；Cap.123 s20(1)亦涵蓋已開工但停工達該段所指3個月的情況，consent視為撤銷；可按s20(2)申請續期。 | [s20](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/legislation/provisions/cap123/en/s20.json) s20(1)-(2)；XML，無PDF頁碼 | 無／無 |
| A098 | Cap.123 s20 consent 續期是否BA只能無條件批？ | 不是；s20(2)指BA可在指定表格申請後續期，並以書面命令施加其認為因延遲或停工而需要的條件。 | [s20](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/legislation/provisions/cap123/en/s20.json) s20(2)；XML，無PDF頁碼 | 無／無 |
| A099 | 有 approved plans 是否即等於有 commencement consent？ | 不是；除另有規定，Cap.123 s14(1)分別要求圖則文件書面approval，以及就批准圖則工程的書面開工consent。 | [s14](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/legislation/provisions/cap123/en/s14.json) s14(1)；XML，無PDF頁碼 | 無／無 |
| A100 | BA 可否只同意已批圖則工程的一部分開工？ | 可以；B(A)R reg32(2)容許就已批圖則工程任何部分發出開工consent；書面通知要求見reg32(1)。 | [s32](https://github.com/rsetestac001-ui/RSE/blob/1192cc4299a4811a72be01456ffdf0aafe2c9da9/legislation/provisions/cap123A/en/s32.json) reg32(1)-(2)；XML，無PDF頁碼 | 無／無 |

## 官方補充查核

所用10份PDF由BD／HKIE官方URL重新下載，與repo副本逐位元相同；Cap.123及123A英文XML亦與本次DOJ官方資料包逐位元相同。完整URL、SHA-256及時間見[副本比對](answer_official_sources_v1.json)。

官方目錄另核對[BD Codes](https://www.bd.gov.hk/en/resources/codes-and-references/codes-and-design-manuals/)、[BD PNAP](https://www.bd.gov.hk/en/resources/codes-and-references/practice-notes-and-circular-letters/index_pnap.html)與[HKIE publications](https://hkie.org.hk/st/resources/technical-publications/)。官方資料作補充；題目證據以固定commit的repo原文為核心。

歷史100列題庫已保留於[legacy_search_cases.json](../tests/legacy_search_cases.json)，原有分支報告見[PR #1](https://github.com/rsetestac001-ui/RSE/pull/1)。本次沒有把舊分支的搜尋指標誤當答案準確率。
