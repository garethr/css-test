"""

CSS is hard to test automatically. Their appear to be two potential approaches 
which might have merit in solving this problem and and this sample code 
represents one of them.

The basic idea resolves around programatic comparison of images, some based on 
screen shots and others generated dynamically from URLs. The capability to 
analyse only a segment of a page has also been included.

The overhead introduced by the need to take screenshots of a site makes this
technique more useful for spotting regression issues in a live site than for
a test driven approach to writing CSS. Tools will be provided to make this 
easier at a later date.

As this is currently a proof of concept in that it only supports testing in 
webkit, and even then only on OS X. Support for other browsers relies on 
other screen grab tools being integrated into the code.

The sample code is written in Python but other implementations would be
straightforward. All of the actual work is done via other commands; namely 
webkit2png by Paul Hammond and the Imagemagik suite of tools.

This is not intended as a tool to check whether a finished website looks
identical to a set of photoshop images. It's intended to spot changes in
unexpected areas of a sites layout or design.

"""

#!/usr/bin/env python

import re
import commands
import unittest

class CSSTests(unittest.TestCase):
    """
    This is a base class containing a set of custom assertions. Inherit 
    from this when creating your test suite.
    """

    def assert_image_same(self, expected, actual):
        "Check that two images specified by a path are identical"
        output = commands.getoutput("compare -metric PSNR %s %s diff.png" 
            % (expected, actual))
        if output == "inf":
            self.assert_(True)
        else:
            self.assert_(False, "%s and %s are not identical" 
                % (expected, actual))
        #commands.getoutput("rm diff.png")

    def assert_image_and_url_same(self, image, url):
        """
        Check that a specified image is identical to what is currently shown
        on a given URL
        """
        commands.getoutput("webkit2png -F %s" % url)
        filename = re.sub('\W', '', url)
        filename = re.sub('^http', '', filename)
        actual = "%s-full.png" % filename
        output = commands.getoutput("compare -metric PSNR %s %s diff.png" 
            % (image, actual))
        if output == "inf":
            self.assert_(True)
        else:
            self.assert_(False, "the page found at %s does not look like %s" 
                % (url, image))
        commands.getoutput("rm %s-full.png" % filename)
        #commands.getoutput("rm diff.png")
        
    def assert_urls_same(self, expected, actual):
        """
        Check that two specified urls are visualy identical
        """
        commands.getoutput("webkit2png -F %s" % expected)
        expected_filename = re.sub('\W', '', expected)
        expected_filename = re.sub('^http', '', expected_filename)
        expected_filename = "%s-full.png" % expected_filename


        commands.getoutput("webkit2png -F %s" % actual)
        actual_filename = re.sub('\W', '', actual)
        actual_filename = re.sub('^http', '', actual_filename)
        actual_filename = "%s-full.png" % actual_filename

        output = commands.getoutput("compare -metric PSNR %s %s diff.png" 
            % (expected_filename, actual_filename))
        if output == "inf":
            self.assert_(True)
        else:
            self.assert_(False, "the page found at %s does not look like %s" 
                % (actual, expected))
        commands.getoutput("rm %s-full.png" % expected_filename)
        commands.getoutput("rm %s-full.png" % actual_filename)
        #commands.getoutput("rm diff.png")
        
    def assert_image_and_url_segment_same(self, image, url, segment):
        """
        Check that a specified image is identical to what is currently shown
        on a given portion of a URL. The syntax for the segment parameter is
        the same as the Imagemagick convert -crop command.
        """
        commands.getoutput("webkit2png -F %s" % url)
        filename = re.sub('\W', '', url)
        filename = re.sub('^http', '', filename)
        commands.getoutput("convert -crop %s %s-full.png %s-segment.png" 
            % (segment, filename, filename))
        actual = "%s-segment.png" % filename
        output = commands.getoutput("compare -metric PSNR %s %s diff.png" 
            % (image, actual))
        if output == "inf":
            self.assert_(True)
        else:
            self.assert_(False, 
                "the segment of the page found at %s does not look like %s"
                    % (url, image))
        commands.getoutput("rm %s-full.png" % filename)
        commands.getoutput("rm %s-segment.png" % filename)
        #commands.getoutput("rm diff.png")
        
class SampleCSSTests(CSSTests):
    """
    A reference implementation of CSSTests demonstration usage
    """
        
    def test_assert_image_same(self):
        expected = "sample/localhost8000-full.png"
        commands.getoutput("webkit2png -F http://localhost:8000")
        actual = "localhost8000-full.png"
        self.assert_image_same(expected, actual)
        commands.getoutput("rm localhost8000-full.png")
        
    def test_assert_image_and_url_same(self):
        image = "sample/localhost8000-full.png"
        url = "http://localhost:8000"
        self.assert_image_and_url_same(image, url)
        
    def test_assert_image_and_url_segment_same(self):
        image = "sample/localhost8000-segment.png"
        url = "http://localhost:8000"
        segment = "500x500+200+200"
        self.assert_image_and_url_segment_same(image, url, segment)

    def test_assert_urls_same(self):
        expected = "http://localhost:8000"
        actual = "http://localhost:8000"
        self.assert_urls_same(expected, actual)

if __name__ == "__main__":
    unittest.main()