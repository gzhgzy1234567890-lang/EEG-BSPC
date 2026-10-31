# -*- coding: utf-8 -*-
"""Reproduce the supplement concentration contrast under several arm definitions."""
import json, os, sys
from collections import defaultdict
import numpy as np
from scipy.stats import binomtest, wilcoxon
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
recs = json.load(open(os.path.join(HERE, 'results', 'd3_concentration.json')))
print('blocks', len(recs), '| subjects', len({r['subj'] for r in recs}))
print('concentration range %.2f-%.2f' % (min(r['conc'] for r in recs), max(r['conc'] for r in recs)))


def run(name, split):
    strata = defaultdict(list)
    for r in recs:
        strata[(r['subj'], r['k_block'], r['k_hist'], r['hist_len'])].append(r)
    used, subj = 0, defaultdict(list)
    for (s, *_), rs in strata.items():
        hi, lo = split(rs)
        if len(hi) >= 2 and len(lo) >= 2:
            subj[s].append(float(np.mean([r['delta'] for r in hi]) - np.mean([r['delta'] for r in lo])))
            used += 1
    if len(subj) < 3:
        print('%-30s unusable' % name); return
    vals = np.array([np.mean(v) for v in subj.values()])
    pos = int((vals > 0).sum())
    p_sign = binomtest(pos, len(vals), 0.5).pvalue
    print('%-30s subjects %2d  cells %3d  mean %+0.4f  positive %2d  sign p=%.3f  wilcoxon p=%.3f'
          % (name, len(vals), used, vals.mean(), pos, p_sign, wilcoxon(vals).pvalue))
    return vals


def med(rs):
    c = np.median([r['conc'] for r in rs])
    return [r for r in rs if r['conc'] > c], [r for r in rs if r['conc'] <= c]


def above_uniform(rs):
    return [r for r in rs if r['conc'] > 1.0 / r['k_block']], [r for r in rs if r['conc'] <= 1.0 / r['k_block']]


def thresh(t):
    def f(rs):
        return [r for r in rs if r['conc'] >= t], [r for r in rs if r['conc'] < t]
    return f


def terciles(rs):
    cs = sorted(r['conc'] for r in rs)
    lo, hi = cs[len(cs) // 3], cs[(2 * len(cs)) // 3]
    return [r for r in rs if r['conc'] >= hi], [r for r in rs if r['conc'] <= lo]


run('median split within stratum', med)
run('above uniform share', above_uniform)
run('concentration >= 0.6', thresh(0.6))
run('concentration >= 0.7', thresh(0.7))
run('tercile top vs bottom', terciles)