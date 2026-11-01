# -*- coding: utf-8 -*-
"""Block-length sensitivity of the pre-specified 2b endpoint."""
import json, os, sys
import numpy as np
from scipy.stats import wilcoxon
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = r'G:\Work_work\math\EEG\paper_v8'
rng = np.random.default_rng(20261101)


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def subject_values(rows, mode, rep):
    d = {}
    for r in rows:
        k0 = '%s|%s|none' % (mode, rep); k1 = '%s|%s|lam1' % (mode, rep)
        d.setdefault(r['subj'], []).append(r[k1] - r[k0])
    return np.array([np.mean(v) for _, v in sorted(d.items())])


print('%-10s %-6s %-8s %-26s %-8s %s' % ('block', 'rep', 'n', 'mean [95% CI]', 'p', 'positive'))
out = []
for block, fn in ((10, 'causal_2b_block10.json'), (15, 'origin_equivariance/results/causal_2b.json'), (20, 'causal_2b_block20.json')):
    if fn.startswith('origin'):
        path = os.path.join(r'G:\Work_work\math\EEG\repo_bspc', fn)
    elif fn.startswith('causal_2b_block'):
        path = os.path.join(HERE, 'results', fn)
    else:
        path = os.path.join(HERE, fn)
    if not os.path.exists(path):
        continue
    rows = json.load(open(path))
    for rep in ('csp', 'euc'):
        v = subject_values(rows, 'causal_so', rep)
        b = [rng.choice(v, len(v), replace=True).mean() for _ in range(10000)]
        lo, hi = np.percentile(b, [2.5, 97.5])
        p = wilcoxon(v).pvalue if np.any(v != 0) else float('nan')
        print('%-10d %-6s %-8d %+0.4f [%+0.4f, %+0.4f]   %-8.3g %d/%d'
              % (block, rep, len(v), v.mean(), lo, hi, p, int((v > 0).sum()), len(v)))
        out.append(dict(block=block, rep=rep, n=len(v), mean=float(v.mean()), lo=float(lo), hi=float(hi), p=float(p), positive=int((v > 0).sum())))
json.dump(out, open(os.path.join(HERE, 'results', 'block_sensitivity_2b.json'), 'w'), indent=1)
print('wrote results/block_sensitivity_2b.json')