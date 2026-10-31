# -*- coding: utf-8 -*-
import json, os, sys
import numpy as np
from scipy.stats import wilcoxon
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'results', 'causal_2b.json')))
print('cells', len(rows), 'subjects', sorted({r['subj'] for r in rows}))
M = {'cs': 'causal_so', 'ca': 'causal_arch', 'ns': 'noncausal_so', 'na': 'noncausal'}
rng = np.random.default_rng(20261101)
def ci(v):
    b = [rng.choice(v, len(v), replace=True).mean() for _ in range(10000)]
    return np.percentile(b, [2.5, 97.5])
def subj_mean(vals_by_cell, key_fn):
    d = {}
    for r in rows:
        d.setdefault(r['subj'], []).append(key_fn(r))
    return np.array([np.mean(v) for v in d.values()])
for rep in ('csp', 'euc', 'euc_ea', 'tan'):
    if not all(('%s|%s|none' % (M[m], rep)) in rows[0] for m in M):
        continue
    print()
    print('representation', rep)
    def dl(mode):
        return subj_mean(None, lambda r: r['%s|%s|lam1' % (M[mode], rep)] - r['%s|%s|none' % (M[mode], rep)])
    cs, ca, ns, na = dl('cs'), dl('ca'), dl('ns'), dl('na')
    k = int((cs > 0).sum())
    p = wilcoxon(cs).pvalue if np.any(cs != 0) else float('nan')
    lo, hi = ci(cs)
    print('  primary (causal, source EA): %+0.4f [%+0.4f, %+0.4f] positive %d/%d wilcoxon p=%.3g' % (cs.mean(), lo, hi, k, len(cs), p))
    print('  causal+both %+0.4f | noncausal+source %+0.4f | noncausal+both %+0.4f' % (ca.mean(), ns.mean(), na.mean()))
    fe = (cs - ns + ca - na) / 2
    ae = (cs - ca + ns - na) / 2
    l1, h1 = ci(fe); l2, h2 = ci(ae)
    print('  filter effect %+0.4f [%+0.4f, %+0.4f] wilcoxon p=%.3g' % (fe.mean(), l1, h1, wilcoxon(fe).pvalue))
    pw = wilcoxon(ae).pvalue if np.any(ae != 0) else float('nan')
    print('  alignment effect %+0.4f [%+0.4f, %+0.4f] wilcoxon p=%.3g' % (ae.mean(), l2, h2, pw))