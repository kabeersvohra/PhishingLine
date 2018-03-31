from sklearn.feature_extraction.text import TfidfVectorizer


class WordFrequencyVectorizer(TfidfVectorizer):

    def fit(self, x, y=None):
        return None

    def fit_transform(self, x, y=None):
        return super(WordFrequencyVectorizer, self).fit_transform(x)

    def transform(self, x, y=None):
        return super(WordFrequencyVectorizer, self).transform(x)
