# -*- coding: utf-8 -*-
"""Composition statistics: paired subject differences, two-sided sign tests, tie-corrected Spearman."""
import json, os, sys
import numpy as np
from scipy.stats import spearmanr
try:
    from scipy.stats import binomtest
    def sign_p(k, m):
        return binomtest(k, m, 0.5, alternative='two-sided').pvalue
except ImportError:
    from scipy.stats import binom_test
    def sign_p(k, m):
        return binom_test(k, m, 0.5, alternative='two-sided')
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, 'results')
al = json.load(open(os.path.join(RES, 'sleep_blocks_all.json')))
ba = json.load(open(os.path.join(RES, 'sleep_block_composition.json')))
n = len(al)
blk1 = sum(1 for r in al if r['ncls_block'] < 2)
hist1 = sum(1 for r in al if r['ncls_hist'] < 2)
both = sum(1 for r in al if r['ncls_block'] < 2 and r['ncls_hist'] < 2)
either = sum(1 for r in al if r['ncls_block'] < 2 or r['ncls_hist'] < 2)
print('blocks %d | scored-block single class %d | history single class %d | both %d | dropped %d | retained %d'
      % (n, blk1, hist1, both, either, n - either))

def paired(rows, key):
    subs = {}
    for r in rows:
        subs.setdefault(r['subj'], []).append(r)
    out = []
    for s, rs in subs.items():
        lo = [r[key] for r in rs if r['maxfrac'] < 0.6]
        hi = [r[key] for r in rs if r['maxfrac'] >= 0.8]
        if lo and hi:
            out.append(np.mean(hi) - np.mean(lo))
    return np.array(out)

d_ba = paired(ba, 'dba')
rng = np.random.default_rng(20261101)
b = [rng.choice(d_ba, len(d_ba), replace=True).mean() for _ in range(10000)]
print('BA: n=%d mean %+0.4f [%+0.4f, %+0.4f] positive %d/%d two-sided p=%.3g'
      % (len(d_ba), d_ba.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5), int((d_ba > 0).sum()), len(d_ba), sign_p(int((d_ba > 0).sum()), len(d_ba))))

subs = {}
for r in al:
    subs.setdefault(r['subj'], []).append(r)
def rate(rs):
    return np.sum([x['err1'] - x['err0'] for x in rs]) / np.sum([x['n'] for x in rs])
d_e = []
for s, rs in subs.items():
    lo = [r for r in rs if r['maxfrac'] < 0.6]
    hi = [r for r in rs if r['maxfrac'] >= 0.8]
    if lo and hi:
        d_e.append(rate(hi) - rate(lo))
d_e = np.array(d_e)
b2 = [rng.choice(d_e, len(d_e), replace=True).mean() for _ in range(10000)]
print('error rate: n=%d mean %+0.4f [%+0.4f, %+0.4f] positive %d/%d two-sided p=%.3g'
      % (len(d_e), d_e.mean(), np.percentile(b2, 2.5), np.percentile(b2, 97.5), int((d_e > 0).sum()), len(d_e), sign_p(int((d_e > 0).sum()), len(d_e))))

net = np.array([(r['err1'] - r['err0']) / float(r['n']) for r in al])
mf = np.array([r['maxfrac'] for r in al])
en = np.array([r['entropy'] for r in al])
print('spearman all blocks: maxfrac %+0.3f (p=%.2g) | entropy %+0.3f (p=%.2g)'
      % (spearmanr(mf, net).correlation, spearmanr(mf, net).pvalue, spearmanr(en, net).correlation, spearmanr(en, net).pvalue))