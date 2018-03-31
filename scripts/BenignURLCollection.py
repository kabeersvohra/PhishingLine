import json
import urllib.request
from urllib.error import HTTPError

from phishingline.src.Util import rooted

output = set()
with open(rooted('data/alexa.txt'), 'r') as alexa:
    for i, url in enumerate(alexa):
        if i % 10 == 0:
            if len(output) > 200000:
                break
            try:
                request = 'http://index.commoncrawl.org/CC-MAIN-2018-13-index?url={search}*&output=json' \
                    .format(search=url.rstrip())
                page = urllib.request.urlopen(request)
                for line in page:
                    output.add(json.loads(line)['url'])
            except HTTPError:
                pass

with open(rooted('data/legitimate_urls.txt'), 'w') as file:
    for out in output:
        file.write(out)
        file.write('\n')
