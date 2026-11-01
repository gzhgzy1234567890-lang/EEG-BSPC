# -*- coding: utf-8 -*-
"""Subject-level statistics for the online decomposition."""
import json, os, sys
import numpy as np
from scipy.stats import wilcoxon
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'results', 'online_decomposition.json')))
rng = np.random.default_rng(20261101)
print('cells', len(rows), '| subjects', len({r['subj'] for r in rows}))
err = max(r['err'] for r in rows)
print('max reconstruction error over all blocks: %.3e' % err)
unm = max(r['unmatched_mass_max'] for r in rows)
print('max unmatched class mass in a history: %.3f' % unm)

def subj(key):
    d = {}
    for r in rows:
        d.setdefault(r['subj'], {}).setdefault(r['night'], []).append(r[key])
    return np.array([np.mean([np.mean(v) for v in n.values()]) for n in d.values()])

def ci(v, n=10000):
    b = [rng.choice(v, len(v), replace=True).mean() for _ in range(n)]
    return float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))

for cond in ('none', 'full', 'mix', 'within', 'shared', 'unmatched'):
    v = subj(cond)
    lo, hi = ci(v)
    print('%-10s BA %.4f  [%.4f, %.4f]' % (cond, v.mean(), lo, hi))

base = subj('none')
print()
for cond in ('full', 'mix', 'within', 'shared', 'unmatched'):
    d = subj(cond) - base
    lo, hi = ci(d)
    p = wilcoxon(d).pvalue if np.any(d != 0) else float('nan')
    print('%-10s delta %+0.4f [%+0.4f, %+0.4f]  negative %d/%d  p=%.3g'
          % (cond, d.mean(), lo, hi, int((d < 0).sum()), len(d), p))

for cond in ('full', 'mix', 'within', 'shared'):
    v = subj(cond + '_flip')
    print('flip rate %-8s %.3f' % (cond, v.mean()))
