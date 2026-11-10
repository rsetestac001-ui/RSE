# Official Hong Kong building legislation

The repository stores the Department of Justice's **current-version open-data XML**, in English and Traditional Chinese, for Cap. 123, 123A, 123C, 123F and 123Q. This is a downloaded official source snapshot; its retrieval date is not its legislative version date and the weekly feed may lag a newly published change.

| Chapter | Title | Official source |
|---|---|---|
| 123 | Buildings Ordinance | https://www.elegislation.gov.hk/hk/cap123 |
| 123A | Building (Administration) Regulations | https://www.elegislation.gov.hk/hk/cap123A |
| 123C | Building (Demolition Works) Regulations | https://www.elegislation.gov.hk/hk/cap123C |
| 123F | Building (Planning) Regulations | https://www.elegislation.gov.hk/hk/cap123F |
| 123Q | Building (Construction) Regulation | https://www.elegislation.gov.hk/hk/cap123Q |

Publisher: Department of Justice, HKSAR Government. Original statutory text and images: © Government of the Hong Kong Special Administrative Region.
Dataset and reuse terms: https://data.gov.hk/en-data/dataset/hk-doj-hkel-legislation-current and https://data.gov.hk/en/terms-and-conditions

## Stored evidence and retrieval

- `legislation/manifest.json`: exact official ZIP URLs, archive members, retrieval timestamp, language, legislative version dates, and SHA-256 of every saved source file.
- `legislation/raw/cap123/en/` (and corresponding chapters/languages): original XML bytes and all associated assets, including statutory diagrams. Open the source XML/images when layout matters. Extracted text does not reproduce table layout or diagrams.
- `legislation/text/cap123/en.txt`: full extracted law, including introductory text, notes and schedules. These are not PDF pages.
- `legislation/catalog.json`: direct provision lookup for all ten chapter/language combinations.
- `legislation/provisions/cap123/en/s20.json`: a whole section with numbered subsections and paragraphs, heading, part context, source path/checksum, version date and official link. Schedules are indexed as whole units with their internal sections retained.
- `search/legislation_fts.sqlite3`: separate section/schedule FTS5 database. Chinese queries use literal substring matching because unicode61 does not segment Chinese words.
- `search/legislation_audit.json`: coverage and regression check results.
- `search/legislation_topics/`: compact excerpts for common questions. Always read the full provision and related conditions before drawing a legal conclusion.

GitHub connector retrieval: fetch the catalog, select chapter/language/provision, then fetch the exact provision path. Do not rely on GitHub code search indexing the repository. SQLite is a local database, not a hosted search API.

## Automation

`.github/workflows/update-legislation.yml` downloads both official archives, selects only the five requested chapters and their assets, validates all ten XML files and asset checksums, extracts provisions, tests Cap.123 s.20 / Cap.123A consent / Chinese retrieval, and commits the validated result to `main`. It runs on relevant code pushes, manually via Actions, and weekly on Monday at 06:00 Hong Kong time. Failed runs do not commit a partial snapshot; check Actions before assuming a refresh succeeded.

```
python scripts/legislation.py refresh
python scripts/legislation.py build
python scripts/legislation.py search 'consent commencement' --chapter 123
python scripts/legislation.py search '同意' --chapter 123 --language zh-Hant
```

No model API or paid search service is used. Cite chapter, section/regulation, subsection and snapshot version date. The open-data snapshot is not represented here as a verified copy under Cap.614. For newly changed law, confirm against Hong Kong e-Legislation and identify any difference separately.
