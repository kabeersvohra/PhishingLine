import os

import PIL
from PIL import Image

from phishingline.src.Util import rooted

for root, dirs, files in os.walk(rooted('data/logos')):
    for fname in files:
        path = os.path.join(root, fname)
        base_fname, extension = os.path.splitext(fname)
        if extension == '.png':
            basewidth = 300
            img = Image.open(path)
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
            img.save(path)
