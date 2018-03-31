import pandas as pd

from phishingline.src.RankedDict import RankedDict
from phishingline.src.Util import rooted

number_of_targets = 20
url = 'http://data.phishtank.com/data/online-valid.csv'
reader = pd.read_csv(url)

ranked_targets = RankedDict(number_of_targets)
targets = dict()
for index, row in reader.iterrows():
    if row.values[7] in targets.keys():
        targets[row.values[7]] += 1
    else:
        targets[row.values[7]] = 1

del targets['Other']

for target in targets:
    ranked_targets[targets[target]] = target

with open(rooted('data/targets.txt'), 'w+') as output:
    for target in ranked_targets:
        output.write(ranked_targets[target])
        output.write('\n')
