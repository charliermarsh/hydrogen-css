import unittest
from hydrogen import runHydrogen
import css
import os

pages = [('http://localhost:12345/page1.html', 'styles1.css'), ('http://localhost:12345/page2.html', 'styles2.css')]


class TestHydrogen(unittest.TestCase):

    def testSingle(self):
        url, stylesheet = pages[0]
        cleanStylesheet = css.cleanSheetForStylesheet(stylesheet)
        # run Hydrogen
        runHydrogen(url, False, False)
        # check that clean CSS was generated successfully
        self.assertTrue(os.path.exists(cleanStylesheet))
        sheetContent = open(cleanStylesheet, "r").read()
        # check proper removal
        self.assertTrue('h2' not in sheetContent)
        # check proper retention
        self.assertTrue('h1' in sheetContent)
        # check minify
        self.assertTrue(' ' not in sheetContent)
        os.remove(cleanStylesheet)

    def testDouble(self):
        # run with two URLs as arguments
        url1, stylesheet1 = pages[0]
        url2, stylesheet2 = pages[1]
        cleanStylesheet1 = css.cleanSheetForStylesheet(stylesheet1)
        cleanStylesheet2 = css.cleanSheetForStylesheet(stylesheet2)
        # run Hydrogen
        runHydrogen([url1, url2], False, False)
        # check that clean CSS was generated successfully for each sheet
        self.assertTrue(os.path.exists(cleanStylesheet1))
        os.remove(cleanStylesheet1)
        self.assertTrue(os.path.exists(cleanStylesheet2))
        os.remove(cleanStylesheet2)

    def testNoSelectors(self):
        ()

    def testIdempotent(self):
        ()

if __name__ == '__main__':
    unittest.main()
