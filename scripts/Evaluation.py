import collections
import os
import shutil

from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import MaxAbsScaler

from scripts.EmergingThreats import get_rules
from phishingline.src.Pipeline import get_default_pipeline
from phishingline.src.Util import rooted, load_safe_browsing_cache, load_model, load_warc_directory, check_emerging_threats

_RULE_FIELDS = [
    "name",
    "engine",
    "cond",
    "clauses",
]
Rule = collections.namedtuple("Rule", _RULE_FIELDS)
rules = get_rules(rooted('data/etphish.ldb.txt'))

malicious_urls = set()
benign_urls = set()

input_x = []
y_true = []
y_pred_emergingthreats = []

input_x, y_true, appends_per_file = load_warc_directory(True, 'test', input_x, y_true)
check_emerging_threats(True, 'test', rules, appends_per_file, y_pred_emergingthreats)

input_x, y_true, appends_per_file = load_warc_directory(False, 'test', input_x, y_true)
check_emerging_threats(False, 'test', rules, appends_per_file, y_pred_emergingthreats)

print('emerging threats')
print(confusion_matrix(y_true, y_pred_emergingthreats))
print('\n')

x, y = load_model()

pipeline = get_default_pipeline(word_frequency_vectorizer=joblib.load(rooted('data/word_frequency_vectorizer.pkl')))

scaler = MaxAbsScaler()
reg = RandomForestClassifier()
reg.fit(scaler.fit_transform(x), y)

pipeline.fit(input_x)
y_pred = reg.predict(scaler.transform(pipeline.transform(input_x)))

shutil.rmtree(rooted('data/misclassified'))
os.mkdir(rooted('data/misclassified'))
misclassified_data = []
with open(rooted('data/misclassified/urls.txt'), 'w+') as urls:
    for i, x in enumerate(y_pred):
        if x != y_true[i]:
            if x == 1:
                classification = 'malicious'
            else:
                classification = 'benign'

            misclassified_data.append((input_x[i], classification))
            urls.write(str(input_x[i][0]) + ' ' + classification + '\n')

for i, data in enumerate(misclassified_data):
    with open(rooted('data/misclassified/{classification}{index}.html'.format(classification=data[1], index=i)),
              'wb+') as html:
        html.write(data[0][1])
    if data[0][3] is not None:
        shutil.copy(data[0][3], rooted('data/misclassified/{classification}{index}.png'
                                       .format(classification=data[1], index=i)))

print('ours')
print(confusion_matrix(y_true, y_pred))
print('\n')

safe_browsing_cache = load_safe_browsing_cache()

y_pred_safebrowsing = [e[0] + '\n' in safe_browsing_cache for e in input_x]

print('safe browsing')
print(confusion_matrix(y_true, y_pred_safebrowsing))
print('\n')
