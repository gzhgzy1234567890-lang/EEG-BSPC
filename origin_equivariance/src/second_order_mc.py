# -*- coding: utf-8 -*-
"""Monte Carlo validation of the corrected second-order coefficient (revision 2)."""
import json, sys
import numpy as np
from scipy.stats import norm
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
rng = np.random.default_rng(20261101)
OUT = r'G:\Work_work\math\EEG\paper_v8\results\second_order_mc.json'


def exact_loss(a, s, d):
    return 0.5 * (2 * norm.cdf(a / s) - norm.cdf((a - d) / s) - norm.cdf((a + d) / s))


def predict2(a, s, d):
    return a * d ** 2 / (2 * s ** 3) * norm.pdf(a / s)


rows = []
for a in (0.5, 1.0, 2.0):
    for s in (0.7, 1.0, 1.5):
        for d in (0.1, 0.2, 0.4):
            n = 400000
            y = rng.integers(0, 2, n)
            x = rng.normal(np.where(y == 1, a, -a), s)
            pred0 = x > 0
            pred1 = (x - d) > 0
            acc0 = 0.5 * (pred0[y == 1].mean() + (~pred0[y == 0]).mean())
            acc1 = 0.5 * (pred1[y == 1].mean() + (~pred1[y == 0]).mean())
            mc = acc0 - acc1
            ex = exact_loss(a, s, d)
            pr = predict2(a, s, d)
            rows.append(dict(a=a, s=s, d=d, mc=float(mc), exact=float(ex), pred2=float(pr)))
            print('a=%.1f s=%.1f d=%.1f  MC %+0.5f  exact %+0.5f  second-order %+0.5f  ratio %.3f'
                  % (a, s, d, mc, ex, pr, pr / ex))
err = max(abs(r['pred2'] - r['exact']) / r['exact'] for r in rows if r['d'] == 0.1)
err2 = max(abs(r['pred2'] - r['exact']) / r['exact'] for r in rows if r['d'] == 0.2)
print('max relative error of the second-order formula at d=0.1: %.4f; at d=0.2: %.4f' % (err, err2))
print('max |MC - exact| over the grid: %.5f' % max(abs(r['mc'] - r['exact']) for r in rows))
json.dump(rows, open(OUT, 'w'), indent=1)
print('wrote', OUT)