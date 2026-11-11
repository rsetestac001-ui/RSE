"""Additional retrieval-only examples; never imported by the search engine."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import subprocess
import types

import retrieval

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    ('H01', '指定地區鑽探要 approval 同 consent', 'PNAP/ADM/ADM-16.txt'),
    ('H02', '我想搵 retaining wall 用嘅 Geoguide 1', 'GEO/GEOGUIDES/GEOGUIDES-8f0263d7-eg1_20200601.txt'),
    ('H03', '風荷載 2019 規範', 'BD_CODES/wind/WindEffects2019e.txt'),
    ('H04', 'concrete 2013 2020 code', 'BD_CODES/concrete/CoP_SUC2013e.txt'),
    ('H05', 'steel 2011 2023 code', 'BD_CODES/steel/SUOS2011.txt'),
    ('H06', 'dead imposed loads 2011 code', 'BD_CODES/dead-imposed-loads/DIL2011e.txt'),
    ('H07', '地盤勘測 Geoguide 2', 'GEO/GEOGUIDES/GEOGUIDES-efdaa5a4-eg2_20171218.txt'),
    ('H08', 'Deep Excavation Design Construction 2023', 'GEO/GEO_PUBLICATIONS/GEO_PUBLICATIONS-1145bf9c-ep1_2023.txt'),
    ('H09', '地盤平整 part A part B', 'PNAP/ADM/ADM-15.txt'),
    ('H10', 'concrete handbook HKIE 2013', 'HKIE/HKIE-concrete-2013.txt'),
    ('H11', '停工後 renewal consent', 'legislation/provisions/cap123/en/s20.json'),
    ('H12', 'Cap.123A reg32', 'legislation/provisions/cap123A/en/s32.json'),
]
BASELINE = 'd5ae0737a5eccd45dd08ac6247d8e7878d215ccc'


def main():
    old_source = subprocess.check_output(['git', 'show', BASELINE + ':scripts/build_search.py'], cwd=ROOT, text=True)
    old = types.ModuleType('legacy_build_search')
    old.__file__ = str(ROOT / 'scripts/build_search.py')
    exec(compile(old_source, old.__file__, 'exec'), old.__dict__)
    results = []
    for ident, query, expected in CASES:
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            old.search(query, 10)
        before = json.loads(buf.getvalue())
        after = retrieval.combined_search(query, 10)
        results.append(dict(id=ident, query=query, expected_source=expected,
                            baseline_hit=any(r['source'] == expected for r in before),
                            improved_hit=any(r['source'] == expected for r in after),
                            baseline=[dict(source=r['source'], pdf_page=r['pdf_page']) for r in before],
                            improved=[dict(source=r['source'], pdf_page=r['pdf_page']) for r in after]))
    report = dict(method='12 supplemental document-retrieval examples authored after the engine change, including GEO/wind/concrete/steel. Not independent answer evaluation; do not tune on these results. Exact source match in top 10 results; old returns pages, new returns diverse documents/provisions.',
                  baseline_commit=BASELINE,
                  engine_sha256=hashlib.sha256((ROOT/'scripts/retrieval.py').read_bytes()).hexdigest(),
                  baseline_hits=sum(r['baseline_hit'] for r in results),
                  improved_hits=sum(r['improved_hit'] for r in results), cases=12, results=results)
    (ROOT/'search/retrieval_examples_v2.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k:report[k] for k in ['cases','baseline_hits','improved_hits']}))


if __name__ == '__main__':
    main()
