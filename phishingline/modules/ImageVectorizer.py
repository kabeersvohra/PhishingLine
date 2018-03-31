from PIL import Image
from sklearn.feature_extraction import DictVectorizer


def get_heuristics(file):
    if file is None or file == '':
        return {}

    with Image.open(file) as image:
        height, width = image.size
        return {
            'height': height,
            'width': width,
        }


class ImageVectorizer(DictVectorizer):

    def fit(self, x, y=None):
        x_html = [get_heuristics(v) for v in x]
        return super(ImageVectorizer, self).fit(x_html)

    def fit_transform(self, x, y=None):
        x_html = [get_heuristics(v) for v in x]
        return super(ImageVectorizer, self).fit_transform(x_html)

    def transform(self, x, y=None):
        x_html = [get_heuristics(v) for v in x]
        return super(ImageVectorizer, self).transform(x_html)
