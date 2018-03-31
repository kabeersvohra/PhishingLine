import os
import urllib.request

from phishingline.src.Util import rooted

with open(rooted('data/legitimate_urls_small.txt'), 'r') as f:
    for i, line in enumerate(f):
        try:
            if not os.path.isfile(rooted('data/legit/%s.html' % ''.join(c for c in line if c.isalnum()))):
                opener = urllib.request.urlopen(line)
                with open(rooted('data/legit/%s.html' % ''.join(c for c in line if c.isalnum())), 'wb+') as root:
                    root.write(opener.read().encode('utf8'))
        except IOError:
            pass

with open(rooted('data/phishing_urls_small.txt'), 'r') as f:
    for i, line in enumerate(f):
        try:
            if not os.path.isfile(rooted('data/phish/%s.html' % ''.join(c for c in line if c.isalnum()))):
                opener = urllib.request.urlopen(line)
                with open(rooted('data/phish/%s.html' % ''.join(c for c in line if c.isalnum())), 'wb+') as root:
                    root.write(opener.read().encode('utf8'))
        except IOError:
            pass
