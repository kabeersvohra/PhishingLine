from sklearn.externals import joblib

from modules.WordFrequencyVectorizer import WordFrequencyVectorizer
from phishingline.src.Pipeline import get_default_pipeline
from phishingline.src.Util import save_model, load_warc_directories, rooted

x, y = load_warc_directories('train')

with open(rooted('data/urls.txt'), 'w+') as file:
    for i, xs in enumerate(x):
        file.write(xs[0] + ' ' + str(y[i]) + '\n')

word_frequency_vectorizer = WordFrequencyVectorizer()
pipeline = get_default_pipeline(word_frequency_vectorizer=word_frequency_vectorizer)

x = pipeline.fit_transform(x)

save_model(x, y)
joblib.dump(word_frequency_vectorizer, rooted('data/word_frequency_vectorizer.pkl'))
