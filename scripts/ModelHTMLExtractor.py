from phishingline.src.Util import rooted, load_warc_directory

x_malicious, _, _ = load_warc_directory(True, 'test', [], [])
x_benign, _, _ = load_warc_directory(False, 'test', [], [])

with open(rooted('data/extracted_malicious.html'), 'wb+') as extracted:
    extracted.write(x_malicious[0][1])

with open(rooted('data/extracted_benign.html'), 'wb+') as extracted:
    extracted.write(x_benign[0][1])
