# -*- coding: utf-8 -*-
"""Within-subject, within-stratum matched comparison of the concentration effect."""
import json, os, sys
import numpy as np
from scipy.stats import binomtest
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'results', 'sleep_blocks_all.json')))
for r in rows:
    r['net'] = (r['err1'] - r['err0']) / float(r['n'])
    r['arm'] = 'hi' if r['maxfrac'] >= 0.8 else ('lo' if r['maxfrac'] < 0.6 else None)
MIN_CELLS = 2
cells = {}
for r in rows:
    if r['arm'] is None:
        continue
    key = (r['subj'], r['ncls_block'], r['ncls_hist'], r['hist_len'])
    cells.setdefault(key, {'lo': [], 'hi': []})[r['arm']].append(r['net'])
complete = {k: v for k, v in cells.items() if len(v['lo']) >= MIN_CELLS and len(v['hi']) >= MIN_CELLS}
print('subject x stratum cells with both arms (>= %d blocks each): %d of %d' % (MIN_CELLS, len(complete), len(cells)))
per_subj = {}
for (subj, a, b, c), v in complete.items():
    per_subj.setdefault(subj, []).append(np.mean(v['hi']) - np.mean(v['lo']))
d = np.array([np.mean(x) for x in per_subj.values()])
k = int((d > 0).sum())
print('subjects with at least one complete cell: %d' % len(d))
print('subject-level matched difference: mean %+0.4f median %+0.4f positive %d/%d two-sided p=%.3g'
      % (d.mean(), np.median(d), k, len(d), binomtest(k, len(d), 0.5).pvalue))
rng = np.random.default_rng(20261101)
boot = [rng.choice(d, len(d), replace=True).mean() for _ in range(10000)]
print('95%% interval [%+0.4f, %+0.4f]' % tuple(np.percentile(boot, [2.5, 97.5])))
# stratum-level balanced aggregation: weight each subject equally over its cells
print('cells used per subject: median %d range %d-%d' % (int(np.median([len(v) for v in per_subj.values()])), min(len(v) for v in per_subj.values()), max(len(v) for v in per_subj.values())))