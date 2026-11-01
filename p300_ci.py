# -*- coding: utf-8 -*-
import json, sys
import numpy as np
from scipy.stats import binomtest
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
rng = np.random.default_rng(20261101)
HERE = r'G:\Work_work\math\EEG\paper_v8\results'
def ci(v, n=20000):
    b = [rng.choice(v, len(v), replace=True).mean() for _ in range(n)]
    return float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
for name, path in (('P300 prereg (variance)', 'p300_external.json'), ('P300 exploratory (mean amp)', 'p300_external_meanamp.json')):
    rows = json.load(open(path if path.startswith('G') else HERE + '\\' + path))
    v = np.array([r['delta'] for r in rows])
    lo, hi = ci(v)
    print('%s: n=%d mean %+0.4f [%+0.4f, %+0.4f] positive %d/%d' % (name, len(v), v.mean(), lo, hi, int((v > 0).sum()), len(v)))
rows = json.load(open(HERE + '\\errp_external.json'))
v = np.array([r['delta'] for r in rows])
lo, hi = ci(v)
print('ERRp: n=%d mean %+0.4f [%+0.4f, %+0.4f] positive %d/%d' % (len(v), v.mean(), lo, hi, int((v > 0).sum()), len(v)))
print('both inside +/-0.02:', lo > -0.02 and hi < 0.02)