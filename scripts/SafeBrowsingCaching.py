from phishingline.src.Google import safe_browsing
from phishingline.src.Util import rooted

search = set()
with open(rooted('data/safe_browsing.txt'), 'a') as safe_browsing_file:
    with open(rooted('data/phishing_urls_test.txt')) as file:
        for url in file:
            if len(search) == 500:
                result = safe_browsing(search)
                for match in result['matches']:
                    safe_browsing_file.write(match['threat']['url'])
                search = set()
            else:
                search.add(url)
        result = safe_browsing(search)
        for match in result['matches']:
            safe_browsing_file.write(match['threat']['url'])
