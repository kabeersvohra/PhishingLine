import json

from flask import Flask, request

from phishingline.src.Google import google_search
from phishingline.src.RankedDict import RankedDict
from phishingline.src.Util import *

corpus = load_word_corpus()
safe_browsing_cache = load_safe_browsing_cache()
app = Flask(__name__)
with open(GOOGLE_CACHE_LOCATION, 'r') as infile:
    google_cache = json.load(infile)


@app.route('/')
def online():
    return ''


@app.route('/%s/<path:url>' % SAFE_BROWSING)
def safe_browsing(url):
    return url in safe_browsing_cache


@app.route('/%s/<word>' % IDF)
def idf(word):
    return str(corpus.idf(word))


@app.route('/%s/<query>' % GOOGLE)
def google(query):
    if query not in google_cache.keys():
        google_cache[query] = google_search(query, num=GOOGLE_QUERY_LIMIT)
    return json.dumps(google_cache[query])


@app.route('/%s/<path:http>' % TF_IDF_GOOGLE)
def tf_idf_google(http):
    text = extract_text(BeautifulSoup(open(http, encoding="utf8"), 'html.parser'))
    tf_words = RankedDict(5)
    for word in text:
        tf_words[tf(text, word) * corpus.idf(word)] = word
    return google(str(tf_words))


@app.route('/shutdown')
def shutdown():
    with open(GOOGLE_CACHE_LOCATION, 'w', encoding="utf8") as outfile:
        json.dump(google_cache, outfile)
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Shutting down...'


app.run()
