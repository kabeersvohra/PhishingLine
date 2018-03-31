import time

from google_images_download import google_images_download

from phishingline.src.Google import google_search
from phishingline.src.Util import rooted

with open(rooted('data/targets.txt'), 'r') as targets:
    for target in targets:
        target = ''.join(ch for ch in target if ch.isalnum() or ch == ' ')
        response = google_images_download.googleimagesdownload()
        response.download({'keywords': target, 'limit': 10, 'output_directory': rooted('data/logos')})
        with open(rooted('data/logos/%s/urls.txt' % target), 'w+') as urls:
            for result in google_search(target):
                urls.write(result['link'] + '\n')
        time.sleep(5)
