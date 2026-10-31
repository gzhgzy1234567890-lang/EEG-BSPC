# -*- coding: utf-8 -*-
import json, sys
import numpy as np
from scipy.stats import spearmanr
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
R = lambda p: json.load(open(p))
ba = R(r'G:\Work_work\math\EEG\paper_v8\results\sleep_block_composition.json')
al = R(r'G:\Work_work\math\EEG\paper_v8\results\sleep_blocks_all.json')
print('BA rows %d | all-block rows %d' % (len(ba), len(al)))
def sign_p(k, m):
    from math import factorial as f
    return sum(f(m) / (f(i) * f(m - i)) for i in range(k, m + 1)) / 2.0 ** m
def paired(rows, key, lo_thr=0.6, hi_thr=0.8):
    subs = {}
    for r in rows:
        subs.setdefault(r['subj'], []).append(r)
    d = []
    for s, rs in subs.items():
        lo = [r[key] for r in rs if r['maxfrac'] < lo_thr]
        hi = [r[key] for r in rs if r['maxfrac'] >= hi_thr]
        if lo and hi:
            d.append(np.mean(hi) - np.mean(lo))
    return np.array(d)
d_ba = paired(ba, 'dba')
rng = np.random.default_rng(20261101)
b = [rng.choice(d_ba, len(d_ba), replace=True).mean() for _ in range(10000)]
lo_, hi_ = np.percentile(b, [2.5, 97.5])
print('BA paired: n=%d mean %+0.4f [%+0.4f, %+0.4f] positive %d/%d sign p=%.2g' % (len(d_ba), d_ba.mean(), lo_, hi_, int((d_ba > 0).sum()), len(d_ba), sign_p(int((d_ba > 0).sum()), len(d_ba))))
subs = {}
for r in al:
    subs.setdefault(r['subj'], []).append(r)
d_e = []
for s, rs in subs.items():
    lo = [r for r in rs if r['maxfrac'] < 0.6]
    hi = [r for r in rs if r['maxfrac'] >= 0.8]
    if lo and hi:
        f = lambda xs: np.sum([x['err1'] - x['err0'] for x in xs]) / np.sum([x['n'] for x in xs])
        d_e.append(f(hi) - f(lo))
d_e = np.array(d_e)
b2 = [rng.choice(d_e, len(d_e), replace=True).mean() for _ in range(10000)]
lo2, hi2 = np.percentile(b2, [2.5, 97.5])
print('error paired: n=%d mean %+0.4f [%+0.4f, %+0.4f] positive %d/%d sign p=%.2g' % (len(d_e), d_e.mean(), lo2, hi2, int((d_e > 0).sum()), len(d_e), sign_p(int((d_e > 0).sum()), len(d_e))))
ncl = np.array([r['ncls_block'] for r in al])
print('single-class scored blocks: %d of %d (%.1f%%)' % (int((ncl < 2).sum()), len(ncl), 100.0 * (ncl < 2).mean()))
print('multi-class retained: %d' % int((ncl >= 2).sum()))