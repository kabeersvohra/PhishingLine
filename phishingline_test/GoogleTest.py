import unittest

from phishingline.src.Google import google_search


class GoogleTest(unittest.TestCase):

    def test_google_search(self):
        results = google_search('gmail', num=10)
        self.assertEqual(results[0]['link'], 'https://www.google.com/gmail/')
