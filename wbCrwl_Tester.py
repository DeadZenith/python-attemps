import unittest
from wbCrwl import validUrl, collectUrl, pullUrls

class CrawlingTesting(unittest.TestCase):

    def test_validLink(self):
        self.assertTrue(validUrl("https://www.rescale.com"))
    def test_doesPull(self):
        content = pullUrls("https://www.rescale.com")
        self.assertTrue(content)
    def test_outputUrls(self):
        self.assertIsNone(collectUrl("https://www.rescale.com"))

if __name__ == '__main__':
    unittest.main()