"""Render the saved reference and retrieval diagnostics into a readable report."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    data = json.loads((ROOT / 'tests/answer_cases_v1.json').read_text())
    report = json.loads((ROOT / 'search/answer_retrieval_v1.json').read_text())
    official = json.loads((ROOT / 'search/answer_official_sources_v1.json').read_text())
    by_id = {r['id']: r for r in report['results']}
    natural = report['summary']['natural_question']
    english = report['summary']['english_diagnostic']
    lines = [
        '# RSE 100條新參考題：原文核對與搜尋結果', '',
        '日期：2026-11-11。**已整理100條不同的原文參考題並逐題實跑搜尋；沒有100份歷史完整答案可供評分。以下不是100題答案準確率認證。**', '',
        f"原文及搜尋基準commit：`{report['tested_commit']}`。本次保留主分支原有搜尋邏輯，沒有把未合併PR的改善成績當成現行結果。", '',
        '| 實測項目 | 結果 |', '|---|---:|',
        '| 新的不同中文問題及AI原文核對參考答案 | 100 |',
        f"| 中文完整問題：前10頁找到指定文件 | {natural['document_hits']}/100 |",
        f"| 中文完整問題：前10頁找到指定參考頁 | {natural['reference_page_hits']}/100 |",
        f"| 中文完整問題：零搜尋結果 | {natural['empty_results']}/100 |",
        f"| 英文關鍵字診斷：前10頁找到指定文件 | {english['document_hits']}/100 |",
        f"| 英文關鍵字診斷：前10頁找到指定參考頁 | {english['reference_page_hits']}/100 |",
        f"| 搜尋執行錯誤（中文／英文） | {natural['execution_errors']}/{english['execution_errors']} |",
        f"| 本次獨立官方PDF副本比對一致 | {sum(x.get('match') is True for x in official['pdf_results'])}/{len(official['pdf_results'])} |",
        f"| 本次DOJ官方英文XML比對一致 | {sum(x.get('match') is True for x in official['legislation_results'])}/{len(official['legislation_results'])} |",
        '| 歷史完整答案評分／獨立專業審定 | 0／0 |',
        '| 答案準確率 | 未評分（null） |', '',
        '「指定參考頁命中」只比對文件路徑及實體頁地址。參考答案由同一AI依原文整理，沒有獨立專業評核。未命中不代表原文沒有規定；命中也不代表系統能正確解釋條件。', '',
        '範圍：GI、Mid-levels、GBP assessment、新界SF豁免、ELS、bored/CFA piles、HKIE基礎手冊角色及consent。未涵蓋全庫GEO、wind、RC、steel與APSEC。', '',
        '## 已定位的問題與改善次序', '',
        '1. 中文完整問句與英文關鍵字的成績有差距。應改善中文同義詞與數值／條件語境，並用額外新題驗證，避免對100題直接硬編碼。',
        '2. 主分支這個頁級搜尋函式沒有整合法例資料庫；5題consent法例均未能命中法例原文，不能把PNAP一般搜尋結果當作條文已找到。',
        '3. 英文診斷另有5題未命中指定PNAP，見下列清單；應檢查排序、長文件多頁佔位及條件語句的選詞。',
        '4. 文件找到與答案完整仍是兩層驗證；正式評分須先固定待測系統的完整答案，再對照原文及參考答案逐項評核。', '',
        '英文診斷未命中：' + '、'.join(x['id'] for x in report['results'] if not x['english_diagnostic']['document_hit']) + '。', '',
        '## 逐題參考答案及結果', '',
        '表內「文件／頁」分別表示指定文件、指定參考實體頁有否出現在中文完整問題的前10頁搜尋結果；不是答案正誤。所有頁碼均為PDF實體頁；法例XML沒有PDF頁碼。每題完整適用範圍及版次見題庫JSON。', '',
        '| ID | 問題 | 原文核對參考答案 | Refer to | 中文文件／頁 |', '|---|---|---|---|---|',
    ]
    for c in data['cases']:
        e = c['evidence'][0]
        page = 'XML，無PDF頁碼' if e['pdf_pages'] is None else 'PDF ' + ', '.join(map(str, e['pdf_pages']))
        title = Path(e['path']).stem
        ref = f"[{title}]({e['github_url']}) {e['section']}；{page}"
        r = by_id[c['id']]['natural_question']
        hit = ('有' if r['document_hit'] else '無') + '／' + ('有' if r['reference_page_hit'] else '無')
        lines.append('| ' + ' | '.join([c['id'], c['question'], c['reference_answer'], ref, hit]) + ' |')
    lines += ['', '## 官方補充查核', '',
              '所用10份PDF由BD／HKIE官方URL重新下載，與repo副本逐位元相同；Cap.123及123A英文XML亦與本次DOJ官方資料包逐位元相同。完整URL、SHA-256及時間見[副本比對](answer_official_sources_v1.json)。', '',
              '官方目錄另核對[BD Codes](https://www.bd.gov.hk/en/resources/codes-and-references/codes-and-design-manuals/)、[BD PNAP](https://www.bd.gov.hk/en/resources/codes-and-references/practice-notes-and-circular-letters/index_pnap.html)與[HKIE publications](https://hkie.org.hk/st/resources/technical-publications/)。官方資料作補充；題目證據以固定commit的repo原文為核心。', '',
              '歷史100列題庫已保留於[legacy_search_cases.json](../tests/legacy_search_cases.json)，原有分支報告見[PR #1](https://github.com/rsetestac001-ui/RSE/pull/1)。本次沒有把舊分支的搜尋指標誤當答案準確率。', '']
    (ROOT / 'search/answer_review_v1.md').write_text('\n'.join(lines))
    print('Wrote 100-row readable review')


if __name__ == '__main__':
    main()
