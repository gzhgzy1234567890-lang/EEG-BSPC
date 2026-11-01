# -*- coding: utf-8 -*-
"""Post-hoc conditional analysis: does the correction do anything where decoding works?"""
import json, sys
import numpy as np
from scipy.stats import spearmanr
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
rng = np.random.default_rng(20261101)
HERE = r'G:\Work_work\math\EEG\paper_v8\results'


def ci(v, n=20000):
    b = [rng.choice(v, len(v), replace=True).mean() for _ in range(n)]
    return float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


print('=== ERRp ===')
rows = json.load(open(HERE + r'\errp_external.json'))
d = np.array([r['delta'] for r in rows])
ba = np.array([np.mean([p[3] for p in r['pairs']]) for r in rows])
print('all subjects: n=%d  mean %+0.4f  [%+0.4f, %+0.4f]' % (len(d), d.mean(), *ci(d)))
print('BA range %.3f-%.3f' % (ba.min(), ba.max()))
for thr in (0.52, 0.55):
    m = ba >= thr
    if m.sum() >= 3:
        print('BA >= %.2f: n=%d  mean %+0.4f  [%+0.4f, %+0.4f]  positive %d'
              % (thr, m.sum(), d[m].mean(), *ci(d[m]), int((d[m] > 0).sum())))
rho, p = spearmanr(ba, d)
print('Spearman(BA, delta) rho=%+0.3f p=%.2f' % (rho, p))

print()
print('=== P300 exploratory ===')
rows = json.load(open(HERE + r'\p300_external_meanamp.json'))
d = np.array([r['delta'] for r in rows])
ba = np.array([r['ba_none'] for r in rows])
print('all subjects: mean %+0.4f  [%+0.4f, %+0.4f]' % (d.mean(), *ci(d)))
m = ba >= 0.55
print('BA >= 0.55: n=%d  mean %+0.4f  [%+0.4f, %+0.4f]  positive %d'
      % (m.sum(), d[m].mean(), *ci(d[m]), int((d[m] > 0).sum())))
rho, p = spearmanr(ba, d)
print('Spearman(BA, delta) rho=%+0.3f p=%.2f' % (rho, p))