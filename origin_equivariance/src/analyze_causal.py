# -*- coding: utf-8 -*-
"""2x2 factorial on BCI-2a: filter (causal/non-causal) x alignment (source-only / both sessions)."""
import json, os, sys
import numpy as np
from scipy.stats import wilcoxon
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'results', 'causal_2a.json')))
M = {'cs': 'causal_so', 'ca': 'causal_arch', 'ns': 'noncausal_so', 'na': 'noncausal'}
def d(mode, rep):
    return np.array([r['%s|%s|lam1' % (M[mode], rep)] - r['%s|%s|none' % (M[mode], rep)] for r in rows])
rng = np.random.default_rng(20261101)
def ci(v):
    b = [rng.choice(v, len(v), replace=True).mean() for _ in range(10000)]
    return np.percentile(b, [2.5, 97.5])
for rep in ('euc', 'euc_ea', 'tan', 'csp'):
    cs, ca, ns, na = d('cs', rep), d('ca', rep), d('ns', rep), d('na', rep)
    print()
    print('representation', rep)
    print('  causal  + source EA %+0.4f | causal + both-session EA %+0.4f' % (cs.mean(), ca.mean()))
    print('  noncaus + source EA %+0.4f | noncaus + both-session EA %+0.4f' % (ns.mean(), na.mean()))
    ea_effect = ((cs - ca).mean() + (ns - na).mean()) / 2
    filt_effect = ((cs - ns).mean() + (ca - na).mean()) / 2
    lo1, hi1 = ci((cs - ca + ns - na) / 2)
    lo2, hi2 = ci((cs - ns + ca - na) / 2)
    print('  alignment effect (averaged over filters) %+0.4f [%+0.4f, %+0.4f]' % (ea_effect, lo1, hi1))
    print('  filter effect    (averaged over alignments) %+0.4f [%+0.4f, %+0.4f]' % (filt_effect, lo2, hi2))
    inter = (cs - ca) - (ns - na)
    lo3, hi3 = ci(inter)
    print('  interaction (filter x alignment) %+0.4f [%+0.4f, %+0.4f]' % (inter.mean(), lo3, hi3))
    p = wilcoxon(cs).pvalue
    print('  causal + source EA: positive %d/%d, wilcoxon p=%.3g' % (int((cs > 0).sum()), len(cs), p))