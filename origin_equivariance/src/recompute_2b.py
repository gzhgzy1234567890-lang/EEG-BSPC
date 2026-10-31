# -*- coding: utf-8 -*-
"""Independent recomputation of the BCI-2b factor table from the raw JSON (A5).
Reads only results/causal_2b.json; does not import any analysis module."""
import json, os, sys
import numpy as np
from scipy.stats import wilcoxon
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'results', 'causal_2b.json')))
MODES = {'cs': 'causal_so', 'ca': 'causal_arch', 'ns': 'noncausal_so', 'na': 'noncausal'}
REPS = ['csp', 'euc', 'euc_ea', 'tan']
def per_subject(mode, rep):
    d = {}
    for r in rows:
        k0 = '%s|%s|none' % (MODE(mode), rep); k1 = '%s|%s|lam1' % (MODE(mode), rep)
        d.setdefault(r['subj'], []).append(r[k1] - r[k0])
    return {s: float(np.mean(v)) for s, v in d.items()}
def MODE(m):
    return MODES[m]
rng = np.random.default_rng(20261101)
def boot_ci(v, n=10000):
    b = [rng.choice(v, len(v), replace=True).mean() for _ in range(n)]
    return float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
print('%-8s %-22s %-22s %-8s %-8s' % ('rep', 'delta_causal (mean [CI])', 'filter effect', 'p_w', 'p_f'))
out = []
for rep in REPS:
    cs = np.array([v for _, v in sorted(per_subject('cs', rep).items())])
    ca = np.array([v for _, v in sorted(per_subject('ca', rep).items())])
    ns = np.array([v for _, v in sorted(per_subject('ns', rep).items())])
    na = np.array([v for _, v in sorted(per_subject('na', rep).items())])
    lo, hi = boot_ci(cs)
    pw = wilcoxon(cs).pvalue if np.any(cs != 0) else float('nan')
    fe = (cs - ns + ca - na) / 2.0
    pf = wilcoxon(fe).pvalue if np.any(fe != 0) else float('nan')
    print('%-8s %+0.4f [%+0.4f, %+0.4f]    %+0.4f              %-8.3g %-8.3g' % (rep, cs.mean(), lo, hi, fe.mean(), pw, pf))
    out.append(dict(rep=rep, delta=float(cs.mean()), lo=lo, hi=hi, p_wilcoxon=float(pw), filter_effect=float(fe.mean()), p_filter=float(pf), n_subjects=int(len(cs))))
json.dump(out, open(os.path.join(HERE, 'results', 'statistics_recomputed_2b.json'), 'w'), indent=1)
print('wrote results/statistics_recomputed_2b.json')