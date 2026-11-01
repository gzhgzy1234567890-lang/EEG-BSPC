# -*- coding: utf-8 -*-
"""Shared-class subset analysis from the per-block records (class-aligned)."""
import json, os, sys
import numpy as np
from scipy.stats import wilcoxon
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'results', 'online_decomposition_blocks.json')))
rng = np.random.default_rng(20261101)
K = 5
print('blocks', len(rows), '| subjects', len({r['subj'] for r in rows}))
masses = np.array([r['unmatched_mass'] for r in rows])
print('unmatched mass: frac 0 = %.3f, >0.5 = %.3f, max %.2f' % (np.mean(masses == 0), np.mean(masses > 0.5), masses.max()))


def pooled_ba(recs, cond):
    tp = np.zeros(K); n = np.zeros(K)
    for r in recs:
        for j, c in enumerate(r['classes']):
            tp[c] += r[cond + '_tp'][j]
            n[c] += r[cond + '_n'][j]
    m = n > 0
    return float(np.mean(tp[m] / n[m]))


by_subj = {}
for r in rows:
    by_subj.setdefault(r['subj'], []).append(r)

for label, keep in (('all blocks', lambda r: True),
                    ('shared-only blocks (unmatched mass = 0)', lambda r: r['unmatched_mass'] == 0),
                    ('blocks with unmatched mass > 0', lambda r: r['unmatched_mass'] > 0)):
    sub = {s: [r for r in v if keep(r)] for s, v in by_subj.items()}
    sub = {s: v for s, v in sub.items() if v}
    if len(sub) < 5:
        print(label, '-> too few subjects', len(sub)); continue
    vals = {cond: np.array([pooled_ba(v, cond) for v in sub.values()])
            for cond in ('none', 'full', 'mix', 'within', 'unmatched')}
    d = vals['full'] - vals['none']
    dm = vals['mix'] - vals['none']
    dw = vals['within'] - vals['none']
    b = [rng.choice(d, len(d), replace=True).mean() for _ in range(10000)]
    print('%-42s subjects %2d  none %.4f  full %+0.4f [%+0.4f, %+0.4f]  mix %+0.4f  within %+0.4f  negative %d/%d'
          % (label, len(sub), vals['none'].mean(), d.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5),
             dm.mean(), dw.mean(), int((d < 0).sum()), len(d)))
