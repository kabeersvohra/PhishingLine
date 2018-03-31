import random
import string

from warcio import ArchiveIterator, WARCWriter

from phishingline.src.Util import rooted

used_names = set()
with open(rooted('data/legitimate1.warc'), 'rb') as file:
    for record in ArchiveIterator(file):
        try:
            content_type_http = record.http_headers.get_header('Content-Type')
            if content_type_http is not None and 'text/html' in content_type_http:
                name = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(32)])
                while name in used_names:
                    name = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(32)])
                used_names.add(name)
                with open(rooted('data/benign/%s.warc' % name), 'wb+') as file2:
                    writer = WARCWriter(file2)
                    writer.write_record(record)
        except:
            pass
