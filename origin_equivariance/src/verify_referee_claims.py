# -*- coding: utf-8 -*-
"""Independent check of the referee's MC1, MC2, MC3, MC4 claims."""
import sys
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar
sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def ba(a, s, t):
    return 0.5 * (norm.cdf((a - t) / s) + norm.cdf((a + t) / s))


print('--- MC1: second-order coefficient ---')
for a, s, d in ((2.0, 1.0, 0.2), (1.0, 1.0, 0.2), (0.5, 2.0, 0.3), (2.0, 0.7, 0.15)):
    loss = ba(a, s, 0) - ba(a, s, d)
    old = d ** 2 / (2 * s ** 2) * norm.pdf(a / s)
    new = a * d ** 2 / (2 * s ** 3) * norm.pdf(a / s)
    print('a=%.2f s=%.2f d=%.2f  loss=%.6f  old=%.6f  new=%.6f' % (a, s, d, loss, old, new))

print()
print('--- MC1: BA\'\'(0) numeric vs formula ---')
for a, s in ((2.0, 1.0), (1.0, 1.0), (0.5, 2.0)):
    h = 1e-4
    num = (ba(a, s, h) - 2 * ba(a, s, 0) + ba(a, s, -h)) / h ** 2
    print('a=%.2f s=%.2f  numeric %.6f  formula -a*phi/s^3 %.6f' % (a, s, num, -a * norm.pdf(a / s) / s ** 3))

print()
print('--- MC3: threshold in feature space vs score space ---')
a, s, w, t = 2.0, 1.0, 4.0, 1.0
print('BA with feature threshold t=%.2f: %.4f' % (t, ba(a, s, t)))
print('BA with feature threshold t/w=%.4f: %.4f  (score-space threshold t)' % (t / w, ba(a, s, t / w)))

print()
print('--- MC2: constrained lambda ---')
for b, c in ((0.5, -0.4), (0.8, 0.2), (0.0, 0.5), (0.5, -0.5)):
    if b + c != 0:
        lam = b / (b + c)
        clip = min(max(lam, 0.0), 1.0)
    else:
        lam, clip = float('nan'), float('nan')
    print('b=%+0.2f c=%+0.2f  lambda*=%.3f  clipped=%.3f' % (b, c, lam, clip))

print()
print('--- MC2: residual convention check ---')
b, c = 0.8, 0.3
for lam in (0.0, 0.5, 1.0):
    r_correct = b - lam * (b + c)
    r_doc = (1 - lam) * b + lam * c
    print('lambda=%.1f  correct residual %.3f   document formula %.3f' % (lam, r_correct, r_doc))

print()
print('--- MC4: same features, two labelings ---')
xs = np.array([0.4, 1.2, -1.2, -1.2])
d = 0.5
for name, y in (('(+,+,-,-)', np.array([1, 1, -1, -1])), ('(-,+,-,-)', np.array([-1, 1, -1, -1]))):
    p0 = np.where(xs > 0, 1, -1)
    p1 = np.where(xs - d > 0, 1, -1)
    def bacc(p):
        rp = np.mean(p[y == 1] == 1)
        rn = np.mean(p[y == -1] == -1)
        return 0.5 * (rp + rn)
    print('%s  before %.3f  after %.3f  change %+0.3f' % (name, bacc(p0), bacc(p1), bacc(p1) - bacc(p0)))