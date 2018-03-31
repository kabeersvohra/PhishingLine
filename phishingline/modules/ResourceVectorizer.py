from bs4 import BeautifulSoup
from sklearn.feature_extraction import DictVectorizer

from phishingline.src.Util import get_host, get_scheme


def get_heuristics(pair):
    url = pair[0]
    html = pair[1]
    domain = get_host(url)
    if len(html) == 0:
        return {}

    try:
        soup = BeautifulSoup(html, 'html.parser', from_encoding='iso-8859-1')
        forms = soup.findAll('form')
        resources = soup.findAll(src=True)
        empty_form_action = external_form_action = relative_path_form_action = same_domain_form_action = False
        empty_resources = external_resources = relative_path_resources = same_domain_resources = False
        https_upgrade = False
        redirect = False

        if soup.title is not None and soup.title.string is not None and '301' in soup.title.string:
            redirect = True
            for a in soup.find_all('a', href=True):
                if get_host(a['href']) == domain and get_scheme(a['href']) == 'https':
                    https_upgrade = True

        for form in forms:
            empty_form_action, external_form_action, relative_path_form_action, same_domain_form_action = \
                check_url_source(empty_form_action, external_form_action, relative_path_form_action,
                                 same_domain_form_action, domain, form.get('action'))

        for resource in resources:
            empty_resources, external_resources, relative_path_resources, same_domain_resources = \
                check_url_source(empty_resources, external_resources, relative_path_resources,
                                 same_domain_resources, domain, resource['src'])

        return {
            'empty_form_action': empty_form_action,
            'relative_path_form_action': relative_path_form_action,
            'same_domain_form_action': same_domain_form_action,
            'external_form_action': external_form_action,
            'empty_resources': empty_resources,
            'relative_path_resources': relative_path_resources,
            'same_domain_resources': same_domain_resources,
            'external_resources': external_resources,
            'redirect': redirect,
            'https_upgrade': https_upgrade,
        }
    except NotImplementedError:
        return {}


def check_url_source(empty, external, relative_path, same_domain, base, query):
    if query == '':
        return True, external, relative_path, same_domain
    action_host = get_host(query)
    if action_host == '':
        relative_path = True
    elif action_host == base:
        same_domain = True
    else:
        external = True
    return empty, external, relative_path, same_domain


class ResourceVectorizer(DictVectorizer):

    def fit(self, x, y=None):
        x_html = [get_heuristics(v) for v in x]
        return super(ResourceVectorizer, self).fit(x_html)

    def fit_transform(self, x, y=None):
        x_html = [get_heuristics(v) for v in x]
        return super(ResourceVectorizer, self).fit_transform(x_html)

    def transform(self, x, y=None):
        x_html = [get_heuristics(v) for v in x]
        return super(ResourceVectorizer, self).transform(x_html)
