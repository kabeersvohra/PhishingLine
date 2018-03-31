import json
import unittest

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

from phishingline.src.Classification import Classification
from phishingline.src.Pipeline import get_default_pipeline
from phishingline.src.Util import *


# noinspection SpellCheckingInspection
class URLHeuristicsTest(unittest.TestCase):
    def setUp(self):
        with open(rooted('data/model.txt')) as model:
            data = json.loads(model.read())
            self.x = np.array(data['x'])
            self.y = np.array(data['y'])

        self.pipeline = get_default_pipeline()

        self.reg = LogisticRegression()
        self.reg.fit(self.x, self.y)

    def get_likelihood(self, url):
        return Classification(probability=first(self.reg.predict(
            self.pipeline.fit_transform([url, '', ''], )))).likelihood()

    def test_ip_address(self):
        url = 'http://192.168.0.1/index/archive.html'
        self.assertTrue(self.get_likelihood(url) == 1)

    def test_many_subdomains(self):
        url = 'http://www.bank.barclays.com.tinyinfo.org.uk/index/archive.html'
        self.assertTrue(self.get_likelihood(url) == 1)

    def test_legitimate_URL(self):
        url = 'http://www.google.com/index/archive.html'
        self.assertTrue(self.get_likelihood(url) == 0)

    def test_data_set(self):
        legit = []
        phish = []
        with open(rooted('data/legitimate_urls_test.txt')) as file:
            for line in file:
                legit.append(self.get_likelihood(line))
        with open(rooted('data/phishing_urls_test.txt')) as file:
            for line in file:
                phish.append(self.get_likelihood(line))

        y_true = [0] * len(legit) + [1] * len(phish)
        y_pred = legit + phish
        print(confusion_matrix(y_true, y_pred))
