# -*- coding: utf-8 -*-
import json, sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
rows = json.load(open(r'G:\Work_work\math\EEG\paper_v8\results\sleep_block_composition.json'))
print('block rows', len(rows), '| cells', len({(r['subj'], r['night'], r['hist_len']) for r in rows}))
d = np.array([r['dba'] for r in rows])
mf = np.array([r['maxfrac'] for r in rows])
en = np.array([r['entropy'] for r in rows])
print('block-level dBA mean %+0.4f  median %+0.4f  harmful fraction %.2f' % (d.mean(), np.median(d), np.mean(d < 0)))
print('maxfrac median %.2f | entropy median %.2f' % (np.median(mf), np.median(en)))
def rank(a):
    return np.argsort(np.argsort(a)).astype(float)
print('rank corr(maxfrac, dba) %+0.3f | rank corr(entropy, dba) %+0.3f' % (np.corrcoef(rank(mf), rank(d))[0,1], np.corrcoef(rank(en), rank(d))[0,1]))
for lo, hi in ((0, 0.5), (0.5, 0.7), (0.7, 0.85), (0.85, 1.01)):
    m = (mf >= lo) & (mf < hi)
    if m.sum():
        print('maxfrac %.2f-%.2f: n=%4d  mean dBA %+0.4f  harmful %.2f' % (lo, hi, m.sum(), d[m].mean(), np.mean(d[m] < 0)))
# subject-level: mean dBA in the two extreme strata
subs = {}
for r in rows:
    subs.setdefault(r['subj'], []).append(r)
lo_s, hi_s = [], []
for s, rs in subs.items():
    l = [r['dba'] for r in rs if r['maxfrac'] < 0.6]
    h = [r['dba'] for r in rs if r['maxfrac'] >= 0.8]
    if l: lo_s.append(np.mean(l))
    if h: hi_s.append(np.mean(h))
print('subjects with both strata: %d | low-concentration %+0.4f | high-concentration %+0.4f' % (min(len(lo_s), len(hi_s)), np.mean(lo_s), np.mean(hi_s)))