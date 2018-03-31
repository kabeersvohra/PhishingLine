import unittest

from phishingline.src.RankedDict import RankedDict


class RankedDictTest(unittest.TestCase):

    def test_normal_put(self):
        ranked_dict = RankedDict(5)
        ranked_dict[1.0] = 'hello'
        self.assertEqual(ranked_dict[1.0], 'hello')

    def test_max_size(self):
        ranked_dict = RankedDict(5)
        ranked_dict[1.0] = 'hello'
        ranked_dict[2.0] = 'hello'
        ranked_dict[3.0] = 'hello'
        ranked_dict[4.0] = 'hello'
        ranked_dict[5.0] = 'hello'
        ranked_dict[6.0] = 'hello'
        ranked_dict[7.0] = 'hello'
        ranked_dict[8.0] = 'hello'
        self.assertEqual(len(ranked_dict), 5)

    def test_small_put(self):
        ranked_dict = RankedDict(5)
        ranked_dict[1.0] = 'hello'
        ranked_dict[2.0] = 'hello'
        ranked_dict[3.0] = 'hello'
        ranked_dict[4.0] = 'hello'
        ranked_dict[5.0] = 'hello'
        ranked_dict[0.5] = 'hello'
        self.assertEqual(ranked_dict[0.5], None)

    def test_large_put(self):
        ranked_dict = RankedDict(5)
        ranked_dict[1.0] = 'hello'
        ranked_dict[2.0] = 'hello'
        ranked_dict[3.0] = 'hello'
        ranked_dict[4.0] = 'hello'
        ranked_dict[5.0] = 'hello'
        ranked_dict[6.0] = 'hello'
        self.assertEqual(ranked_dict[1.0], None)
        self.assertEqual(ranked_dict[6.0], 'hello')

    def test_medium_put(self):
        ranked_dict = RankedDict(5)
        ranked_dict[1.0] = 'hello'
        ranked_dict[2.0] = 'hello'
        ranked_dict[3.0] = 'hello'
        ranked_dict[4.0] = 'hello'
        ranked_dict[5.0] = 'hello'
        ranked_dict[3.5] = 'hello'
        self.assertEqual(ranked_dict[1.0], None)
        self.assertEqual(ranked_dict[3.5], 'hello')

    def test_str(self):
        ranked_dict = RankedDict(5)
        ranked_dict[1.0] = 'hello'
        ranked_dict[2.0] = 'hello'
        ranked_dict[3.0] = 'hello'
        ranked_dict[4.0] = 'hello'
        ranked_dict[5.0] = 'hello'
        self.assertEqual(str(ranked_dict), 'hello hello hello hello hello')

