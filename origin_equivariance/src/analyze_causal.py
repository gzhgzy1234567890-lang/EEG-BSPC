# -*- coding: utf-8 -*-
"""Delta_causal, Delta_noncausal and Delta_protocol for BCI-2a, subject level."""
import json, os, sys
import numpy as np
from scipy.stats import wilcoxon
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'results', 'causal_2a.json')))
REPS = ('euc', 'euc_ea', 'tan', 'csp')
MODES = ('causal_so', 'causal_arch', 'noncausal')
rng = np.random.default_rng(20261101)
def ci(v):
    b = [rng.choice(v, len(v), replace=True).mean() for _ in range(10000)]
    return np.percentile(b, [2.5, 97.5])
print('subjects:', len(rows))
for rep in REPS:
    print()
    print('representation', rep)
    deltas = {}
    for mode in MODES:
        d = np.array([r['%s|%s|lam1' % (mode, rep)] - r['%s|%s|none' % (mode, rep)] for r in rows])
        deltas[mode] = d
        lo, hi = ci(d)
        p = wilcoxon(d).pvalue if np.any(d != 0) else float('nan')
        print('  %-12s delta %+0.4f [%+0.4f, %+0.4f]  positive %d/%d  wilcoxon p=%.3g'
              % (mode, d.mean(), lo, hi, int((d > 0).sum()), len(d), p))
    dp = deltas['causal_so'] - deltas['noncausal']
    lo, hi = ci(dp)
    print('  delta_protocol (causal_so - noncausal) %+0.4f [%+0.4f, %+0.4f]' % (dp.mean(), lo, hi))
    df = deltas['causal_so'] - deltas['causal_arch']
  
    lo2, hi2 = ci(df)
    print('  filter effect within source-only EA (causal_so - causal_arch) %+0.4f [%+0.4f, %+0.4f]' % (df.mean(), lo2, hi2))