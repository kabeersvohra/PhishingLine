import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError

from phishingline.src.Util import rooted

jobs = []
output = dict()
with ThreadPoolExecutor(max_workers=100) as executor:
    with open(rooted('data/alexa.txt'), 'r') as alexa:
        for i, url in enumerate(alexa):
            if i % 60 == 0:
                try:
                    request = 'http://index.commoncrawl.org/CC-MAIN-2018-13-index?url={search}*&output=json' \
                        .format(search=url.rstrip())
                    page = urllib.request.urlopen(request)
                    for line in page:
                        result = json.loads(line)
                        if 'crawldiagnostics' in result['filename'] and int(result['length']) < 700:
                            output[result['url']] = result['filename']
                except HTTPError:
                    pass

    for k in output:
        future = executor.submit(urllib.request.urlretrieve,
                                 'https://commoncrawl.s3.amazonaws.com/%s' % output[k],
                                 rooted('data/benign/%s.warc.gz' % ''.join(c for c in output[k] if c.isalnum())))
        jobs.append(future)

    for f in jobs:
        print(f.result())
