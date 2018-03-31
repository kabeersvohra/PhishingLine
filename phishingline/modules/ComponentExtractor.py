import numpy as np

from sklearn.base import TransformerMixin, BaseEstimator


# noinspection PyMethodMayBeStatic
class ComponentExtractor(BaseEstimator, TransformerMixin):

    def fit(self, x):
        return self

    def transform(self, x):
        features = np.recarray(shape=(len(x),),
                               dtype=[('url', object), ('html', object), ('text', object), ('img', object), ('status', object)])

        for i, train in enumerate(x):
            url = train[0]
            html = train[1]
            text = train[2]
            img = train[3]
            status = train[4]

            features['url'][i] = url
            features['html'][i] = html
            features['text'][i] = text
            features['img'][i] = img
            features['status'][i] = status

        return features
