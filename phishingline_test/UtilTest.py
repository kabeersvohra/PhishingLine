import unittest

from phishingline.src.Util import *


class UtilTest(unittest.TestCase):

    def test_idf_common_word(self):
        corpus = load_word_corpus()
        self.assertTrue(corpus.idf('and') < 0.1)

    def test_idf_uncommon_word(self):
        corpus = load_word_corpus()
        self.assertTrue(corpus.idf('oxymoron') > 0.1)
