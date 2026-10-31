# -*- coding: utf-8 -*-
import json, sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
rows = json.load(open(r'G:\Work_work\math\EEG\paper_v8\results\seed_memory_scale_coldstart.json'))
W = (5, 10, 25, 50, 100, 200, 400)
A = ('0.20', '0.10', '0.05', '0.02', '0.01')
def subj(k):
    d = {}
    for r in rows:
        d.setdefault(r['subj'], []).append(r[k])
    return np.array([np.mean(v) for v in d.values()])
rng = np.random.default_rng(20261101)
def ci(v):
    b = [rng.choice(v, len(v), replace=True).mean() for _ in range(5000)]
    return np.percentile(b, [2.5, 97.5])
print('window | subject mean [95% CI] | positive subjects')
for w in W:
    v = subj('w%d' % w); lo, hi = ci(v)
    print('%4d   %+0.4f [%+0.4f, %+0.4f]   %d/%d' % (w, v.mean(), lo, hi, int((v > 0).sum()), len(v)))
print('alpha | subject mean [95% CI] | positive subjects')
for a in A:
    v = subj('a%s' % a); lo, hi = ci(v)
    print('%5s  %+0.4f [%+0.4f, %+0.4f]   %d/%d' % (a, v.mean(), lo, hi, int((v > 0).sum()), len(v)))
# within-subject slope of delta against log window
subs = {}
for r in rows:
    subs.setdefault(r['subj'], []).append(r)
slopes = []
for s, rs in subs.items():
    x = np.log([w for w in W for _ in rs])
    y = np.array([r['w%d' % w] for w in W for r in rs])
    slopes.append(np.polyfit(x, y, 1)[0])
slopes = np.array(slopes)
print('within-subject slope per log unit: mean %+0.4f  positive %d/%d' % (slopes.mean(), int((slopes > 0).sum()), len(slopes)))