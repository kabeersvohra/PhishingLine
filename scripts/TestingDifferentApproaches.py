import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import MaxAbsScaler

from modules.HTMLVectorizer import HTMLVectorizer
from modules.ImageVectorizer import ImageVectorizer
from modules.ResourceVectorizer import ResourceVectorizer
from modules.URLVectorizer import URLVectorizer
from modules.WordFrequencyVectorizer import WordFrequencyVectorizer
from phishingline.src.Pipeline import get_default_pipeline, initialise_pipeline
from phishingline.src.Util import rooted, load_warc_directories

with open(rooted('data/evaluation.txt'), 'w+') as output:
    pipelines = [
        (initialise_pipeline(url_vectorizer=URLVectorizer(sparse=False),
                             url_n_vectorizer=HashingVectorizer(n_features=2)), 'url with 2-gram'),
        (initialise_pipeline(url_vectorizer=URLVectorizer(sparse=False),
                             url_n_vectorizer=HashingVectorizer(n_features=3)), 'url with 3-gram'),
        (initialise_pipeline(url_vectorizer=URLVectorizer(sparse=False)), 'url only'),
        (initialise_pipeline(html_vectorizer=HTMLVectorizer(sparse=False),
                             body_n_vectorizer=HashingVectorizer(n_features=3),
                             status_n_vectorizer=HashingVectorizer(n_features=3)), 'html with 3-gram'),
        (initialise_pipeline(html_vectorizer=HTMLVectorizer(sparse=False),
                             body_n_vectorizer=HashingVectorizer(n_features=2),
                             status_n_vectorizer=HashingVectorizer(n_features=2)), 'html with 2-gram'),
        (initialise_pipeline(html_vectorizer=HTMLVectorizer(sparse=False),
                             body_n_vectorizer=HashingVectorizer(n_features=2),
                             word_frequency_vectorizer=WordFrequencyVectorizer(),
                             status_n_vectorizer=HashingVectorizer(n_features=2)), 'html with 2-gram and word freq'),
        (initialise_pipeline(html_vectorizer=HTMLVectorizer(sparse=False)), 'html only'),
        (initialise_pipeline(resource_vectorizer=ResourceVectorizer(),
                             status_n_vectorizer=HashingVectorizer(n_features=3)), 'resources and status 3-gram'),
        (initialise_pipeline(resource_vectorizer=ResourceVectorizer(),
                             status_n_vectorizer=HashingVectorizer(n_features=2)), 'resources and status 2-gram'),
        (initialise_pipeline(image_vectorizer=ImageVectorizer(sparse=False)), 'resources and status 2-gram'),
        (get_default_pipeline(url_n_vectorizer=HashingVectorizer(n_features=2),
                              body_n_vectorizer=HashingVectorizer(n_features=2),
                              status_n_vectorizer=HashingVectorizer(n_features=2)), 'full with 2-gram'),
        (get_default_pipeline(url_n_vectorizer=HashingVectorizer(n_features=3),
                              body_n_vectorizer=HashingVectorizer(n_features=3),
                              status_n_vectorizer=HashingVectorizer(n_features=3)), 'full with 3-gram'),
    ]

    methods = [
        (LogisticRegression(), 'Logistic regression'),
        (LogisticRegression(C=0.5), 'Logistic regression with strong regularisation'),
        (LogisticRegression(C=0.2), 'Logistic regression with very strong regularisation'),
        (SGDClassifier(), 'Stochastic gradient descent'),
        (RandomForestClassifier(), 'Random forest classifier'),
    ]

    x_train, y_train = load_warc_directories('train')
    for entry in pipelines:
        pipeline = entry[0]
        config = entry[1]
        output.write(config + '\n')
        x = pipeline.fit_transform(x_train)
        input_x, y_true = load_warc_directories('test')

        for method in methods:
            reg = method[0]
            reg.fit(x, y_train)
            pipeline.fit(input_x)
            y_pred = reg.predict(pipeline.transform(input_x))
            output.write('%s\n' % method[1])
            output.write(np.array_str(confusion_matrix(y_pred, y_true)))
            output.write('\n')

            output.write('with normalisation\n')

            scaler = MaxAbsScaler()
            reg = method[0]
            reg.fit(scaler.fit_transform(x), y_train)
            pipeline.fit(input_x)
            y_pred = reg.predict(scaler.transform(pipeline.transform(input_x)))
            output.write('%s\n' % method[1])
            output.write(np.array_str(confusion_matrix(y_pred, y_true)))
            output.write('\n')
