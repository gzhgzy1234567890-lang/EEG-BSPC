# -*- coding: utf-8 -*-
"""Structure-matched analysis: compare error change across concentration strata, holding the number of
classes, block size and history length fixed (exact matching on the discrete factors)."""
import json, os, sys
import numpy as np
from scipy.stats import binomtest
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'results', 'sleep_blocks_all.json')))
for r in rows:
    r['net'] = (r['err1'] - r['err0']) / float(r['n'])
    r['stratum'] = 'hi' if r['maxfrac'] >= 0.8 else ('lo' if r['maxfrac'] < 0.6 else 'mid')
keys = {}
for r in rows:
    k = (r['ncls_block'], r['ncls_hist'], r['hist_len'])
    keys.setdefault(k, {'lo': [], 'hi': []})
    if r['stratum'] in ('lo', 'hi'):
        keys[k][r['stratum']].append(r['net'])
usable = {k: v for k, v in keys.items() if v['lo'] and v['hi']}
print('strata with both arms:', len(usable), 'of', len(keys))
tot_lo = sum(len(v['lo']) for v in usable.values())
tot_hi = sum(len(v['hi']) for v in usable.values())
print('blocks in matched strata: lo %d hi %d' % (tot_lo, tot_hi))
diffs = []
subs = {}
for r in rows:
    k = (r['ncls_block'], r['ncls_hist'], r['hist_len'])
    if k in usable:
        subs.setdefault(r['subj'], []).append(r)
for s, rs in subs.items():
    lo = [r['net'] for r in rs if r['stratum'] == 'lo']
    hi = [r['net'] for r in rs if r['stratum'] == 'hi']
    if lo and hi:
        diffs.append(np.mean(hi) - np.mean(lo))
d = np.array(diffs)
k_pos = int((d > 0).sum())
print('subject-level matched difference: n=%d mean %+0.4f positive %d/%d two-sided p=%.3g'
      % (len(d), d.mean(), k_pos, len(d), binomtest(k_pos, len(d), 0.5).pvalue))
rng = np.random.default_rng(20261101)
boot = [rng.choice(d, len(d), replace=True).mean() for _ in range(10000)]
print('95%% interval [%+0.4f, %+0.4f]' % tuple(np.percentile(boot, [2.5, 97.5])))