"""Compare fixed retrieval runs, preserving the old report and its result units."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    def read(path):
        return json.loads((ROOT / path).read_text())
    before = read('search/answer_retrieval_v1.json')
    after = read('search/answer_retrieval_v2.json')
    cases = read('tests/answer_cases_v1.json')['cases']
    extra = read('search/retrieval_examples_v2.json')
    for field in ['question_dataset_sha256', 'index_sha256', 'source_text_sha256']:
        if before[field] != after[field]:
            raise ValueError('Comparison inputs changed: ' + field)
    old = {r['id']:r for r in before['results']}
    new = {r['id']:r for r in after['results']}
    lines = ['# 搜尋改善 v2：固定100題重測', '',
             '2026-11-11。本次改搜尋程式；100題題目、參考答案、PDF索引及證據原文維持相同，舊報告未覆寫。這是搜尋結果比較，答案準確率仍未評分。', '',
             '| 項目 | v1 | v2 |', '|---|---:|---:|']
    for label, key, metric in [
        ('中文：指定文件／條文在前10結果', 'natural_question', 'document_hits'),
        ('中文：主要PDF頁／XML條文定位', 'natural_question', 'reference_page_hits'),
        ('英文關鍵字：指定文件／條文在前10結果', 'english_diagnostic', 'document_hits'),
        ('英文關鍵字：主要PDF頁／XML條文定位', 'english_diagnostic', 'reference_page_hits'),
        ('中文：零結果', 'natural_question', 'empty_results'),
    ]:
        lines.append(f"| {label} | {before['summary'][key][metric]}/100 | {after['summary'][key][metric]}/100 |")
    lines += [f"| 另12條補充題：指定文件／條文命中 | {extra['baseline_hits']}/12 | {extra['improved_hits']}/12 |", '',
              f"加入相鄰頁補讀後，中文參考位置覆蓋為{after['summary']['natural_question']['reference_context_hits']}/100；這個數字獨立報告，不當成主要頁定位。", '',
              '**比較限制：v1為前10頁；v2為前10個不同PDF文件／法例條文，每份PDF只有一個主要頁。結果單位改變，因此是整體搜尋行為比較，不能稱為固定頁數下的隔離排序實驗。XML結果沒有PDF頁碼，以條文路徑核對。**', '',
              '## 改了甚麼', '',
              '- 單一搜尋引擎供CLI及常用topic JSON使用；不讀題庫、預期答案或測試標籤。',
              '- 通用中文工程詞彙與英文縮寫擴展；長中文詞優先，GI接中文可識別，不會誤改digital等英文單字。',
              '- APP25／APP-025等編號正規化並可直接定位文件；不是依題目ID分派答案。',
              '- 以查詢詞覆蓋、標題、FTS分數及文件版次資料排序；每份PDF一個主要頁，另附相鄰頁及交叉引用／修訂資訊。',
              '- PDF與法例條文一併搜尋；明確Cap.123 s20等查詢直接定位條文。XML頁碼固定null。',
              '- 加入8個搜尋合約回歸測試，連既有法例測試共9個通過；Actions更新時自動重跑100題並保存結果。', '',
              '## 未解決及退步', '',
              '文件命中不代表已找到最有力的支持段落。原始文件覆蓋並非完整相關性判定，也不代表答案內容正確。HKIE／GEO版次提示不等於禁用歷史版本或完成所有修訂核證。', '',
              '英文主要位置由90降至87，不能只報文件命中的改善。以下保留所有主要位置由命中轉為未命中的題目；部分可能在補讀頁找到，仍屬主要定位退步。', '']
    for key, label in [('natural_question', '中文'), ('english_diagnostic', '英文')]:
        regressions = [c for c in cases if old[c['id']][key]['reference_page_hit'] and not new[c['id']][key]['reference_page_hit']]
        misses = [c['id'] for c in cases if not new[c['id']][key]['document_hit']]
        lines += [label + '指定文件／條文仍未命中：' + '、'.join(misses) + '。', '',
                  label + '主要位置退步：' + '、'.join(c['id'] for c in regressions) + '。', '']
    lines += ['補充12題在程式修改後編寫，未因其測試結果調整排序；包含GEO、wind、RC、steel等文件查找，但不是這些專題的答案核證。', '',
              '下一步優先改善同一文件內段落／頁定位，處理英文退步及餘下3條中文未命中問題；正式答案評核仍須固定待評系統完整輸出，再逐項核對數值、範圍、例外及引用。', '',
              '## 逐題比較', '',
              '「文件」包括指定法例條文；「主位置」只算主要頁／條文；「含補讀」另算相鄰PDF頁。完整參考答案及原文位置見[固定題庫](../tests/answer_cases_v1.json)，原始結果見[舊結果](answer_retrieval_v1.json)、[新結果](answer_retrieval_v2.json)。', '',
              '| ID | 問題 | 中文文件 v1→v2 | 中文主位置 v1→v2 | v2含補讀 |', '|---|---|---|---|---|']
    mark = lambda x: '有' if x else '無'
    for c in cases:
        a, b = old[c['id']]['natural_question'], new[c['id']]['natural_question']
        lines.append(f"| {c['id']} | {c['question']} | {mark(a['document_hit'])}→{mark(b['document_hit'])} | {mark(a['reference_page_hit'])}→{mark(b['reference_page_hit'])} | {mark(b['reference_context_hit'])} |")
    lines += ['', '## 重現', '', '```sh',
              "python -m unittest discover -s scripts -p 'test_*.py' -v",
              'python scripts/review_answer_cases.py', 'python scripts/check_retrieval_examples.py',
              'python scripts/build_search_improvement_report.py', 'python scripts/build_retrieval.py', '```', '',
              '12題補充測試需本機git含基準commit d5ae073；一般Actions重跑100題不依賴此舊git物件。所有搜尋、排序及測試只用本地SQLite／Python，不呼叫模型API。', '']
    (ROOT / 'search/search_improvement_v2.md').write_text('\n'.join(lines))
    print('Wrote fixed-input before/after comparison with regressions')


if __name__ == '__main__':
    main()
