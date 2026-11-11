# Cross-source search QA
100 exploratory queries are stored in search_cases.json. Expected codes are **unverified candidate labels**, not manually adjudicated gold truth. The automated run measures candidate recall only; it cannot legitimately claim Precision@10 or correctness of paragraphs, PDF pages, statutory interpretations, or version currency.

## External web comparison protocol
For each query, independently search official BD, CEDD/GEO and HKIE websites. Record the official URL, document version/date, applicable section and physical PDF page, plus date checked. Compare these against RSE results, verify original PDF and amendments, and have a reviewer adjudicate relevance. Only then mark a case gold_verified and calculate validated Recall@10 / Precision@10. Do not automatically treat web ranking as truth. Web searching is **not implemented** in the offline workflow, so no claim of independent web verification is made.

Run: python scripts/build_search.py build && python scripts/test_cross_references.py
