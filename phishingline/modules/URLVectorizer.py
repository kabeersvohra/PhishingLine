import ipaddr
from fuzzywuzzy import fuzz
from sklearn.feature_extraction import DictVectorizer

from phishingline.src.Util import *


def get_heuristics(url):
    hostname = get_host(url)
    path = get_path(url)
    subdomain = get_subdomain(hostname)
    scheme = get_scheme(url)
    query = get_query(url)
    TLD = load_tld()

    try:
        ipaddr.IPAddress(hostname)
        ip_address = True
    except ValueError:
        ip_address = False

    return {
        'contains_at': url.find('@') >= 0,
        'hostname_contains_dash': hostname.find('-') >= 0,
        'percent_encoding': url.find('%') >= 0,
        'contains_brackets': url.find('(') >= 0,
        'number_subdomains': subdomain.count('.'),
        'path_contains_tld': any(e in path for e in TLD),
        'subdomain_contains_tld': any(e in subdomain for e in TLD),
        'path_contains_equal': path.find('=') >= 0,
        'hostname_contains_digit': any(char.isdigit() for char in hostname),
        'has_cyrillic': bool(re.search(CYRILLIC_REGEX, url)),  # https://www.xudongz.com/blog/2017/idn-phishing/
        'target_in_path': any(e in path for e in TARGETS),
        'ip_address': ip_address,
        'shortened_url': hostname in URL_SHORTENING_SERVICES,
        'target_in_subdomain': any(e in subdomain for e in TARGETS),
        'trigger_in_path': any(e in path for e in TRIGGER),
        'changed_port': hostname.find(':') >= 0,
        'misspelled_target_in_url': any(fuzz.partial_ratio(e, url) > 80 for e in TARGETS),
        'length': len(url),
        'uses_https': scheme.find('https'),
        'size_of_query': len(query),
    }


class URLVectorizer(DictVectorizer):

    def fit(self, x, y=None):
        x_urls = [get_heuristics(v) for v in x]
        return super(URLVectorizer, self).fit(x_urls)

    def fit_transform(self, x, y=None):
        x_urls = [get_heuristics(v) for v in x]
        return super(URLVectorizer, self).fit_transform(x_urls)

    def transform(self, x, y=None):
        x_urls = [get_heuristics(v) for v in x]
        return super(URLVectorizer, self).transform(x_urls)
