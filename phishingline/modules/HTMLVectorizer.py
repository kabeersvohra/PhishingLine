from bs4 import BeautifulSoup
from sklearn.feature_extraction import DictVectorizer


def get_heuristics(html):
    if len(html) == 0:
        return {}

    try:
        soup = BeautifulSoup(html, 'html.parser', from_encoding='iso-8859-1')
        size_scripts = 0
        tags = soup.findAll()
        page_size = len(html)
        for script in soup.find_all('script'):
            size_scripts += len(script)
        return {
            'favicon': soup.find('link', rel='shortcut icon') is not None,
            'number_forms': len(soup.findAll('form')),
            'number_password_fields': len(soup.findAll('input', {'type': 'password'})),
            'number_iframes': len(soup.findAll('iframe')),
            'scripts_page_ratio': size_scripts / page_size,
            'number_tags': len(tags),
            'size_of_page': page_size,
        }
    except NotImplementedError:
        return {}


class HTMLVectorizer(DictVectorizer):

    def fit(self, x, y=None):
        x_html = [get_heuristics(v) for v in x]
        return super(HTMLVectorizer, self).fit(x_html)

    def fit_transform(self, x, y=None):
        x_html = [get_heuristics(v) for v in x]
        return super(HTMLVectorizer, self).fit_transform(x_html)

    def transform(self, x, y=None):
        x_html = [get_heuristics(v) for v in x]
        return super(HTMLVectorizer, self).transform(x_html)
