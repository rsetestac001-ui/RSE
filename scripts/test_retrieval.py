"""Contract tests for safe, auditable retrieval, using small synthetic indexes."""
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import retrieval


class RetrievalContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'search').mkdir()
        self.pdf = self.root / 'search/pnap_fts.sqlite3'
        with sqlite3.connect(self.pdf) as db:
            db.execute('CREATE TABLE page(id INTEGER PRIMARY KEY,code,source,page_no,content)')
            db.execute("CREATE VIRTUAL TABLE page_fts USING fts5(code,content,content='page',content_rowid='id')")
            db.executemany('INSERT INTO page(code,source,page_no,content) VALUES(?,?,?,?)', [
                ('APP-025', 'PNAP/APP/APP-025.txt', 1, 'geotechnical assessment slope height'),
                ('APP-025', 'PNAP/APP/APP-025.txt', 2, 'geotechnical assessment neighbouring slope'),
                ('OTHER', 'OTHER.txt', 1, 'geotechnical assessment slope'),
            ])
            db.execute("INSERT INTO page_fts(page_fts) VALUES('rebuild')")
        with sqlite3.connect(self.root / 'search/legislation_fts.sqlite3') as db:
            db.execute('CREATE TABLE provision(id INTEGER PRIMARY KEY,chapter,language,provision,heading,content,path,version_date,official_url)')
            db.execute("CREATE VIRTUAL TABLE provision_fts USING fts5(heading,content,content='provision',content_rowid='id')")
            db.execute("INSERT INTO provision VALUES(1,'123','en','s20','Resumption','consent suspended months','legislation/provisions/cap123/en/s20.json','2026-03-01','https://example.invalid')")
            db.execute("INSERT INTO provision_fts(provision_fts) VALUES('rebuild')")

    def tearDown(self):
        self.temp.cleanup()

    def test_cantonese_adjacent_acronym_does_not_expand_inside_english_word(self):
        self.assertIn('ground investigation', retrieval.expand('GI做乜'))
        self.assertEqual(retrieval.expand('digital'), 'digital')

    def test_longest_chinese_phrase_keeps_undrained_distinct(self):
        self.assertIn('undrained', retrieval.expand('不排水'))
        self.assertNotIn('drained analysis', retrieval.expand('不排水'))

    def test_document_reference_with_chinese_suffix_is_normalized(self):
        self.assertEqual(retrieval.explicit_codes('APP25的要求及ADM-016'), {'APP-25', 'ADM-16'})
        with patch.object(retrieval, 'metadata', return_value={}):
            result = retrieval.search('APP25未知中文', db=self.pdf)
        self.assertEqual(result[0]['code'], 'APP-025')

    def test_one_primary_page_per_document_with_context_separate(self):
        with patch.object(retrieval, 'metadata', return_value={}):
            result = retrieval.search('geotechnical assessment', db=self.pdf)
        self.assertEqual(len({x['source'] for x in result}), len(result))
        doc = next(x for x in result if x['code'] == 'APP-025')
        self.assertEqual(len(doc['context_pages']), 1)
        self.assertNotEqual(doc['pdf_page'], doc['context_pages'][0]['pdf_page'])

    def test_xml_result_has_no_pdf_page(self):
        with patch.object(retrieval, 'ROOT', self.root):
            result = retrieval.search_legislation('Cap.123 s20')
        self.assertEqual(result[0]['provision'], 's20')
        self.assertIsNone(result[0]['pdf_page'])
        self.assertEqual(result[0]['kind'], 'legislation')

    def test_exact_law_reference_does_not_return_unrelated_pdf(self):
        with patch.object(retrieval, 'ROOT', self.root):
            result = retrieval.combined_search('Cap.123 s20')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['kind'], 'legislation')

    def test_blank_and_punctuation_queries(self):
        self.assertEqual(retrieval.combined_search(''), [])
        with patch.object(retrieval, 'metadata', return_value={}):
            self.assertEqual(retrieval.search('*** " OR ()', db=self.pdf), [])

    def test_missing_optional_law_index_is_not_created(self):
        with patch.object(retrieval, 'ROOT', self.root / 'missing'):
            self.assertEqual(retrieval.search_legislation('consent'), [])
        self.assertFalse((self.root / 'missing/search/legislation_fts.sqlite3').exists())


if __name__ == '__main__':
    unittest.main()
