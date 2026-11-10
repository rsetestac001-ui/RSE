# Hong Kong building legislation — authoritative source register

Checked: 2026-11-11

This directory registers **official sources**, not a copy of the legislation. The existing `index_manifest.json` indexes PNAP PDFs only. Do not claim Cap. 123 or subsidiary regulations have been indexed until full texts are downloaded, parsed and audited.

| Chapter | Title | Official legislation |
|---|---|---|
| Cap. 123 | Buildings Ordinance | https://www.elegislation.gov.hk/hk/cap123 |
| Cap. 123A | Building (Administration) Regulations | https://www.elegislation.gov.hk/hk/cap123A |
| Cap. 123C | Building (Demolition Works) Regulations | https://www.elegislation.gov.hk/hk/cap123C |
| Cap. 123F | Building (Planning) Regulations | https://www.elegislation.gov.hk/hk/cap123F |
| Cap. 123Q | Building (Construction) Regulation | https://www.elegislation.gov.hk/hk/cap123Q |

Buildings Department's official legislation directory:
https://www.bd.gov.hk/en/resources/legal-matters/index.html

Department of Justice's open data feed (current legislation, updated weekly):
https://data.gov.hk/en-data/dataset/hk-doj-hkel-legislation-current

## Required ingestion steps
1. Retrieve current official text from Hong Kong e-Legislation / the Department of Justice open-data distribution, recording language, version date, URL and checksum.
2. Parse sections and subsections (not PDF pages unless an actual PDF is stored).
3. Index legal provisions alongside, but separately from, PNAP page-level FTS.
4. Add automated checks for Cap.123 s.20 and Cap.123A, and report missing/changed versions.
5. Never treat this source register as proof of a particular statutory wording.

## Immediate lookup rule
For a question about statutory deadlines (e.g. consent to commence), first look for the relevant provision in Cap.123 itself; do not infer the law from PNAP text alone. Verify the current statutory wording from the official source before answering.
