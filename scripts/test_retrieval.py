"""Regression checks for failures found by the cross-source audit."""
import unittest
from retrieval import ROOT, expand, metadata, search, search_legislation


class RetrievalRegression(unittest.TestCase):
    def test_aliases_do_not_expand_inside_english_words(self):
        self.assertEqual(expand('design guidance'), 'design guidance')
        self.assertEqual(expand('GI in 指定地區'), 'ground investigation in scheduled area')

    def test_scheduled_gi_finds_both_primary_notes_and_unique_documents(self):
        rows = search('scheduled area GI',10)
        self.assertTrue({'ADM-16','APP-030'} <= {r['code'] for r in rows})
        self.assertEqual(len(rows),len({r['source'] for r in rows}))

    def test_els_primary_pnap_is_visible_and_cross_references_preserved(self):
        rows = search('ELS',10)
        self.assertEqual(rows[0]['code'],'APP-057')
        self.assertIn('PNAP/APP/APP-018.txt',rows[0]['cross_references'])
        self.assertIn('PNAP/APP/APP-137.txt',rows[0]['cross_references'])

    def test_general_gi_is_not_routed_only_to_scheduled_area_note(self):
        rows = search('ground investigation',10)
        self.assertEqual(rows[0]['code'],'APP-049')
        self.assertTrue(any('eg2_20171218' in r['source'] for r in rows))

    def test_statutory_deadline_source_is_returned_without_fake_pdf_page(self):
        rows = search_legislation('consent commencement',10)
        section = next(r for r in rows if r['chapter']=='123' and r['provision']=='s20')
        self.assertIsNone(section['pdf_page'])
        self.assertIn('3 months',(ROOT/section['source']).read_text())

    def test_main_code_result_carries_amendment_links(self):
        rows = search('wind effects',10)
        code = next(r for r in rows if r['code']=='WindEffects2019e')
        self.assertTrue(any('Amend2023' in u for u in code['must_read_with']))

    def test_historical_editions_are_identified_and_retained(self):
        meta = metadata()
        self.assertTrue(meta['HKIE/HKIE-wind-2004.txt']['earlier_edition_in_series'])
        self.assertFalse(meta['HKIE/HKIE-wind-2019.txt']['earlier_edition_in_series'])
        self.assertTrue(any(r['code']=='HKIE-wind-2004' for r in search('wind effects 2004',10)))


if __name__=='__main__':
    unittest.main()
