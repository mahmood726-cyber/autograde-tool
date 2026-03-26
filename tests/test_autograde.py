"""
Selenium tests for AutoGRADE — GRADE Certainty of Evidence Calculator.
Usage: python -m pytest tests/test_autograde.py -v --timeout=60
"""
import sys, os, time, unittest
if __name__ == '__main__' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

HTML_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'autograde.html'))
FILE_URL = 'file:///' + HTML_PATH.replace('\\', '/')

_WDM = os.path.expanduser('~/.wdm/drivers/chromedriver/win64')
_CACHED = []
if os.path.isdir(_WDM):
    for v in sorted(os.listdir(_WDM), reverse=True):
        for sub in ('chromedriver-win32', ''):
            c = os.path.join(_WDM, v, sub, 'chromedriver.exe').rstrip(os.sep)
            if os.path.isfile(c): _CACHED.append(c); break

def _driver():
    opts = ChromeOptions()
    opts.add_argument('--headless=new'); opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-gpu'); opts.add_argument('--incognito'); opts.add_argument('--window-size=1280,900')
    opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    for p in _CACHED:
        try: return webdriver.Chrome(service=ChromeService(executable_path=p), options=opts)
        except WebDriverException: continue
    try: return webdriver.Chrome(options=opts)
    except: pass
    try:
        from selenium.webdriver.edge.options import Options as EO
        eo = EO(); eo.add_argument('--headless=new'); eo.add_argument('--no-sandbox')
        eo.add_argument('--disable-gpu'); eo.add_argument('--inprivate'); eo.add_argument('--window-size=1280,900')
        return webdriver.Edge(options=eo)
    except: pass
    raise WebDriverException('No driver')

class TestAutoGRADE(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = _driver(); cls.d.set_page_load_timeout(30)
        cls.d.get(FILE_URL); time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        if cls.d:
            try:
                import threading; done = threading.Event()
                def q():
                    try: cls.d.quit()
                    except: pass
                    finally: done.set()
                threading.Thread(target=q, daemon=True).start()
                if not done.wait(10):
                    try: cls.d.service.process.kill()
                    except: pass
            except: pass

    def js(self, s): return self.d.execute_script(s)

    # 01: Title
    def test_01_title(self):
        self.assertIn('AutoGRADE', self.d.title)

    # 02: Auto-compute on load (SGLT2i default)
    def test_02_auto_compute(self):
        badge = self.d.find_element(By.ID, 'gradeResult').text
        self.assertNotEqual(badge.strip(), '—')

    # 03: SGLT2i should be HIGH certainty (RCTs, no downgrades)
    def test_03_sglt2i_high(self):
        r = self.js("return window._lastGrade;")
        self.assertIsNotNone(r)
        self.assertEqual(r['gradeLabel'], 'HIGH', f'SGLT2i should be HIGH, got {r["gradeLabel"]}')

    # 04: SSRIs should be LOW (RoB + inconsistency + pub bias)
    def test_04_ssri_low(self):
        self.js("""
            document.getElementById('exSel').value = 'ssri';
            document.getElementById('exSel').dispatchEvent(new Event('change'));
        """)
        time.sleep(0.3)
        r = self.js("return window._lastGrade;")
        self.assertIn(r['gradeLabel'], ['LOW', 'VERY LOW'],
            f'SSRIs should be LOW or VERY LOW, got {r["gradeLabel"]}')

    # 05: Vitamin D should have imprecision downgrade (CI crosses null)
    def test_05_vitd_imprecision(self):
        self.js("""
            document.getElementById('exSel').value = 'vitd';
            document.getElementById('exSel').dispatchEvent(new Event('change'));
        """)
        time.sleep(0.3)
        r = self.js("return window._lastGrade;")
        imprecision = [d for d in r['domains'] if d['name'] == 'Imprecision'][0]
        self.assertGreater(imprecision['down'], 0, 'Vitamin D should have imprecision downgrade (CI crosses null)')

    # 06: 5 domains always present
    def test_06_five_domains(self):
        r = self.js("return window._lastGrade;")
        self.assertEqual(len(r['domains']), 5, f'Should have 5 domains, got {len(r["domains"])}')
        names = [d['name'] for d in r['domains']]
        for expected in ['Risk of Bias', 'Inconsistency', 'Indirectness', 'Imprecision', 'Publication Bias']:
            self.assertIn(expected, names)

    # 07: RCT starts at HIGH (4), OBS at LOW (2)
    def test_07_starting_certainty(self):
        # RCT — reload SGLT2i
        self.js("""
            document.getElementById('exSel').value = 'sglt2i';
            document.getElementById('exSel').dispatchEvent(new Event('change'));
        """)
        time.sleep(0.3)
        summary = self.d.find_element(By.ID, 'gradeSummary').text
        self.assertIn('Starting: HIGH', summary)

    # 08: High RoB → serious downgrade
    def test_08_rob_downgrade(self):
        self.js("""
            document.getElementById('exSel').value = 'sglt2i';
            document.getElementById('exSel').dispatchEvent(new Event('change'));
            document.getElementById('robHigh').value = '40';
            computeGrade();
        """)
        time.sleep(0.3)
        r = self.js("return window._lastGrade;")
        rob = [d for d in r['domains'] if d['name'] == 'Risk of Bias'][0]
        self.assertEqual(rob['down'], 1, f'40% high RoB should give -1, got {rob["down"]}')

    # 09: Very high I² → very serious inconsistency
    def test_09_high_i2(self):
        self.js("""
            document.getElementById('exSel').value = 'sglt2i';
            document.getElementById('exSel').dispatchEvent(new Event('change'));
            document.getElementById('i2').value = '80';
            computeGrade();
        """)
        time.sleep(0.3)
        r = self.js("return window._lastGrade;")
        incon = [d for d in r['domains'] if d['name'] == 'Inconsistency'][0]
        self.assertEqual(incon['down'], 2, f'I²=80% should give -2, got {incon["down"]}')

    # 10: CI crossing null → imprecision
    def test_10_ci_crosses_null(self):
        self.js("""
            document.getElementById('effectMeasure').value = 'RR';
            document.getElementById('effectEst').value = '0.90';
            document.getElementById('ciLo').value = '0.70';
            document.getElementById('ciHi').value = '1.15';
            document.getElementById('oisMet').value = 'no';
            computeGrade();
        """)
        time.sleep(0.3)
        r = self.js("return window._lastGrade;")
        imp = [d for d in r['domains'] if d['name'] == 'Imprecision'][0]
        self.assertEqual(imp['down'], 2, 'CI crosses null + OIS not met → very serious (-2)')

    # 11: Egger p < 0.10 → serious pub bias; p < 0.01 → very serious
    def test_11_pub_bias(self):
        self.js("""
            document.getElementById('exSel').value = 'sglt2i';
            document.getElementById('exSel').dispatchEvent(new Event('change'));
            document.getElementById('eggerP').value = '0.03';
            computeGrade();
        """)
        time.sleep(0.3)
        r = self.js("return window._lastGrade;")
        pub = [d for d in r['domains'] if d['name'] == 'Publication Bias'][0]
        self.assertEqual(pub['down'], 1, f'Egger p=0.03 should be -1 (serious), got {pub["down"]}')

    # 12: Observational + large effect → upgrade
    def test_12_obs_upgrade(self):
        self.js("""
            document.getElementById('studyDesign').value = 'OBS';
            document.getElementById('effectMeasure').value = 'OR';
            document.getElementById('effectEst').value = '3.5';
            document.getElementById('ciLo').value = '2.5';
            document.getElementById('ciHi').value = '5.0';
            document.getElementById('i2').value = '10';
            document.getElementById('robHigh').value = '5';
            document.getElementById('robUnclear').value = '10';
            document.getElementById('indirectness').value = '0';
            document.getElementById('oisMet').value = 'yes';
            document.getElementById('eggerP').value = '0.50';
            document.getElementById('largeEffect').value = 'yes';
            document.getElementById('doseResponse').value = 'yes';
            computeGrade();
        """)
        time.sleep(0.3)
        r = self.js("return window._lastGrade;")
        self.assertGreater(len(r['upgrades']), 0, 'Should have upgrades for OBS with large effect')
        self.assertIn(r['gradeLabel'], ['MODERATE', 'HIGH'],
            f'OBS with large effect + dose-response should upgrade, got {r["gradeLabel"]}')

    # 13: Score clamped between 1 and 4
    def test_13_score_bounds(self):
        # Force maximum downgrades on OBS (starting at 2)
        self.js("""
            document.getElementById('studyDesign').value = 'OBS';
            document.getElementById('robHigh').value = '60';
            document.getElementById('i2').value = '90';
            document.getElementById('indirectness').value = '2';
            document.getElementById('ciLo').value = '0.5';
            document.getElementById('ciHi').value = '2.0';
            document.getElementById('oisMet').value = 'no';
            document.getElementById('eggerP').value = '0.01';
            document.getElementById('largeEffect').value = 'no';
            document.getElementById('doseResponse').value = 'no';
            document.getElementById('plausibleConf').value = 'no';
            computeGrade();
        """)
        time.sleep(0.3)
        r = self.js("return window._lastGrade;")
        self.assertEqual(r['gradeLabel'], 'VERY LOW')
        self.assertGreaterEqual(r['score'], 1, 'Score should not go below 1')

    # 14: SoF table rendered
    def test_14_sof_table(self):
        self.js("""
            document.getElementById('exSel').value = 'sglt2i';
            document.getElementById('exSel').dispatchEvent(new Event('change'));
        """)
        time.sleep(0.3)
        rows = self.d.find_elements(By.CSS_SELECTOR, '#sofBody tr')
        self.assertGreater(len(rows), 0, 'SoF table should have rows')

    # 15: NNT computed for ratio measures
    def test_15_nnt(self):
        r = self.js("return window._lastGrade;")
        self.assertIsNotNone(r['nnt'], 'NNT should be computed for ratio measures')
        self.assertGreater(r['nnt'], 0)

    # 16: Dark mode
    def test_16_dark_mode(self):
        self.d.find_element(By.ID, 'themeBtn').click()
        time.sleep(0.3)
        self.assertEqual(self.d.find_element(By.TAG_NAME, 'html').get_attribute('data-theme'), 'dark')
        self.d.find_element(By.ID, 'themeBtn').click()
        time.sleep(0.3)

    # 17: About modal
    def test_17_about(self):
        self.d.find_element(By.ID, 'aboutBtn').click()
        time.sleep(0.3)
        m = self.d.find_element(By.ID, 'aboutModal')
        self.assertNotIn('hidden', m.get_attribute('class'))
        self.assertIn('GRADE', m.text)
        self.d.find_element(By.ID, 'aboutX').click()
        time.sleep(0.3)

    # 18: No console errors
    def test_18_no_errors(self):
        try: logs = self.d.get_log('browser')
        except: self.skipTest('No log support')
        severe = [e for e in logs if e.get('level') == 'SEVERE' and 'favicon' not in e.get('message','').lower()]
        if severe: self.fail(f'Errors: {[e["message"] for e in severe]}')

    # 19: Skip-nav + CSP + aria-live
    def test_19_accessibility(self):
        self.assertEqual(len(self.d.find_elements(By.CSS_SELECTOR, 'a[href="#main"]')), 1)
        csp = self.js("var m=document.querySelector('meta[http-equiv=\"Content-Security-Policy\"]'); return m?m.content:null;")
        self.assertIsNotNone(csp)
        self.assertEqual(self.d.find_element(By.ID, 'resultsCard').get_attribute('aria-live'), 'polite')

    # 20: Export function exists
    def test_20_export(self):
        self.assertTrue(self.js("return typeof exportJSON === 'function'"))
        self.assertTrue(self.js("return typeof copySoF === 'function'"))

if __name__ == '__main__':
    unittest.main(verbosity=2)
