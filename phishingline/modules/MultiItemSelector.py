import numpy as np
from sklearn.base import TransformerMixin, BaseEstimator


class MultiItemSelector(BaseEstimator, TransformerMixin):
    def __init__(self, keys):
        self.keys = keys

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        result = []
        for key in self.keys.split(' '):
            result.append(x[key])
        return np.column_stack(result)
