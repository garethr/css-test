"""
Part of my investigation of CSS Testing techniques, this time looking at
the possibility of using selenium to extract rendered DOM attribute values.

So far I have a simple text size example pointing at my personal site. But the
general pattern shown here should be general enough for all DOM properties.

You'll need a Selenium RC server running locally on port 4444 to use this.
"""

#!/usr/bin/env python

import unittest
from ext.selenium import selenium

class DOMTests(unittest.TestCase):
    """
    This is the start of a series of useful assertions for various DOM values
    """

    def setUp(self):
        "Instantiate a local Selenium RC instance"
        self.browser = selenium("localhost", 4444, "*chrome", "http://morethanseven.net/")
        self.browser.start()

    def tearDown(self):
        "Close the browser once we're done with each test"
        self.browser.stop()

    def assert_text_size(self, css, expected):
        """
        Assert that the element matching a given CSS expression has the given
        font size. Useful to avoid unintended changes to text sizes because of
        rogue CSS rules.
        """
        js = """
            element = this.browserbot.findElement("css=%s");
            document.defaultView.getComputedStyle(element,null).getPropertyValue("font-size");
        """ % (css)
        observed = self.browser.get_eval(js)
        self.assertEqual(observed, expected)        

class SampleDOMTests(DOMTests):
    "Examples demonstrating the above assertions"

    def test_assert_text_size_for_h1(self):
        browser = self.browser
        browser.open("http://morethanseven.net/")
        self.failUnless(browser.is_element_present("css=body"))        
        self.assert_text_size("h1", "20.8px")
        
if __name__ == "__main__":
    unittest.main()