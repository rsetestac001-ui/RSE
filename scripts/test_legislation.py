"""Structural regression tests: schedules, nested clauses, mixed inline text and images."""
import tempfile
import unittest
from pathlib import Path
import legislation as law

class ExtractionTests(unittest.TestCase):
    def test_sections_and_schedule_keep_context_and_inline_words(self):
        raw=b'''<ordinance xmlns="http://www.xml.gov.hk/schemas/hklm/1.0"><main>
        <part><heading>Administration</heading>
        <section id="a" temporalId="s20"><num>20.</num><heading>Consent</heading>
        <subsection temporalId="s20_1"><num>(1)</num><content>The <term>Building Authority</term> may act.</content>
        <paragraph temporalId="s20_1_a"><num>(a)</num><content>within time</content></paragraph></subsection>
        <subsection temporalId="s20_2"><num>(2)</num><content>Second clause.</content></subsection></section></part>
        <schedule id="b" temporalId="sch1"><heading>Forms</heading>
        <section temporalId="sch1_s1"><content><table><tr><td>Entry A</td><td>Entry B</td></tr></table>
        <img src="images/form.jpg" alt="Form diagram"/></content></section></schedule></main></ordinance>'''
        old=law.ROOT
        with tempfile.TemporaryDirectory() as td:
            law.ROOT=Path(td)
            try:
                (law.ROOT/'source.xml').write_bytes(raw)
                rows,full=law.parse({'chapter':'123','language':'en','version_date':'2026-01-01',
                    'xml_path':'source.xml','sha256':law.sha(raw),'files':[],
                    'official_url':'https://www.elegislation.gov.hk/hk/cap123'})
                self.assertEqual([r['provision'] for r in rows],['s20','sch1'])
                self.assertEqual(rows[0]['context'],['Administration'])
                self.assertEqual(len(rows[0]['subsections']),2)
                self.assertIn('The Building Authority may act.',rows[0]['content'])
                self.assertIn('within time',rows[0]['subsections'][0]['content'])
                self.assertIn('Entry A\nEntry B',rows[1]['content'])
                self.assertIn('[Image: Form diagram]',full)
                self.assertEqual(rows[1]['images'][0]['src'],'images/form.jpg')
            finally: law.ROOT=old

if __name__=='__main__': unittest.main()
