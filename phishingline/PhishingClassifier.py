import sys
import time
import urllib.request
from urllib.error import URLError

from PIL import Image
from sklearn.linear_model import LinearRegression

from phishingline.src.Classification import Classification
from phishingline.src.Pipeline import get_default_pipeline
from phishingline.src.Util import first, SERVER_BASE_URL, load_model


# noinspection PyArgumentList,PyShadowingNames
def classify(url, html, img):
    x, y = load_model()

    pipeline = get_default_pipeline()

    reg = LinearRegression()
    reg.fit(x, y)

    try:
        return Classification(probability=first(reg.predict(pipeline.fit_transform([[url, html, img]], ))))
    except ValueError:
        exit('model dimension error, please re-train')


if len(sys.argv) <= 3:
    exit('insufficient arguments')

try:
    urllib.request.urlopen(SERVER_BASE_URL)
except URLError:
    exit('server offline')

start = time.time()
url = sys.argv[1]
with Image.open(sys.argv[2], 'r') as img:
    with open(sys.argv[3], 'r', encoding='utf8') as html:
        print('%s%%' % (classify(url, html.read(), img).likelihood() * 100))
print('--- %s seconds ---' % (time.time() - start))
