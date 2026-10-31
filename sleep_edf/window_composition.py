# -*- coding: utf-8 -*-
import json, sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
rows = json.load(open(r'G:\Work_work\math\EEG\paper_v8\results\sleep_blockwise2.json'))
d = np.array([r['full'] - r['none'] for r in rows])
mf = np.array([r['hist_maxfrac'] for r in rows])
en = np.array([r['hist_entropy'] for r in rows])
k = np.array([r['hist_k'] for r in rows])
print('cells', len(rows), '| maxfrac median %.2f | entropy median %.2f | classes median %d' % (np.median(mf), np.median(en), np.median(k)))
def spearman(a, b):
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    return float(np.corrcoef(ra, rb)[0, 1]), 0.0
print('spearman(maxfrac, delta) rho %+.3f' % spearman(mf, d)[0])
print('spearman(entropy, delta) rho %+.3f' % spearman(en, d)[0])
for lo, hi in ((0, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.01)):
    m = (mf >= lo) & (mf < hi)
    if m.sum():
        print('maxfrac %.1f-%.1f: n=%4d  mean delta %+0.4f  fraction harmful %.2f' % (lo, hi, m.sum(), d[m].mean(), np.mean(d[m] < 0)))