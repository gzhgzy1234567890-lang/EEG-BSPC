# -*- coding: utf-8 -*-
"""Regression tests for the corrected propositions (revision 2)."""
import sys
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
rng = np.random.default_rng(20261101)
ok = True


def ba(a, s, t):
    return 0.5 * (norm.cdf((a - t) / s) + norm.cdf((a + t) / s))


# 1. second-order coefficient, tested where a != sigma
for a, s in ((2.0, 1.0), (0.5, 2.0), (2.0, 0.7)):
    d = 1e-3
    loss = ba(a, s, 0) - ba(a, s, d)
    pred = a * d ** 2 / (2 * s ** 3) * norm.pdf(a / s)
    err = abs(loss - pred) / pred
    print('second order a=%.2f s=%.2f  loss %.3e  prediction %.3e  rel err %.2e' % (a, s, loss, pred, err))
    ok &= err < 1e-4

# 2. BA''(0) formula and sign
for a, s in ((2.0, 1.0), (1.0, 1.0), (0.5, 2.0)):
    h = 1e-4
    num = (ba(a, s, h) - 2 * ba(a, s, 0) + ba(a, s, -h)) / h ** 2
    formula = -a * norm.pdf(a / s) / s ** 3
    print('BA\'\'(0) a=%.2f s=%.2f  numeric %.6f  formula %.6f' % (a, s, num, formula))
    ok &= abs(num - formula) < 1e-4 and formula < 0

# 3. threshold dimension: score threshold tau equals feature threshold tau/w
a, s, w, tau = 2.0, 1.0, 4.0, 1.0
feat = ba(a, s, tau / w)
wrong = ba(a, s, tau)
print('threshold: feature %.4f  misinterpreted %.4f  difference %.4f' % (feat, wrong, abs(feat - wrong)))
ok &= abs(feat - wrong) > 0.05

# 4. constrained optimal weight
for b, c, expect in ((0.5, -0.4, 1.0), (0.8, 0.2, 0.8), (0.0, 0.5, 0.0), (0.5, -0.5, None)):
    if b + c != 0:
        lam = min(max(b / (b + c), 0.0), 1.0)
    else:
        lam = None
    ok &= (lam == expect) if expect is not None else (lam is None)
    print('lambda* b=%+0.2f c=%+0.2f -> %s (expected %s)' % (b, c, ('%.2f' % lam) if lam is not None else 'undefined', expect))

# 5. residual convention
b, c = 0.8, 0.3
for lam in (0.0, 0.5, 1.0):
    r = b - lam * (b + c)
    doc = (1 - lam) * b - lam * c
    ok &= abs(r - doc) < 1e-12
    print('residual lambda=%.1f  %.3f vs %.3f' % (lam, r, doc))

# 6. numerical optimum of lambda agrees with the clipped formula
b, c = 0.8, 0.7
lam_grid = np.linspace(0, 1, 2001)
ba_grid = [ba(1.0, 1.0, b - lam * (b + c)) for lam in lam_grid]
lam_num = lam_grid[int(np.argmax(ba_grid))]
lam_form = min(max(b / (b + c), 0.0), 1.0)
print('lambda numerical %.3f  formula %.3f' % (lam_num, lam_form))
ok &= abs(lam_num - lam_form) < 0.01

# 7. finite-sample sign flip at fixed features
xs = np.array([0.4, 1.2, -1.2, -1.2])
d = 0.5
changes = []
for y in (np.array([1, 1, -1, -1]), np.array([-1, 1, -1, -1])):
    p0 = np.where(xs > 0, 1, -1)
    p1 = np.where(xs - d > 0, 1, -1)
    b0 = 0.5 * (np.mean(p0[y == 1] == 1) + np.mean(p0[y == -1] == -1))
    b1 = 0.5 * (np.mean(p1[y == 1] == 1) + np.mean(p1[y == -1] == -1))
    changes.append(b1 - b0)
print('finite-sample changes', ['%+.3f' % c for c in changes])
ok &= changes[0] < 0 < changes[1]

# 8. certificate with and without ties
K = 3
S = np.array([[2.0, 1.0, 0.0]])
dd = np.array([0.5, 0.0, 0.0])
k = int(np.argmax(S[0]))
strict = all((S[0, k] - S[0, j]) > (dd[k] - dd[j]) for j in range(K) if j != k)
print('certificate strict condition holds:', strict, ' (a tie can only make it non-strict)')

print('THEORY TEST', 'PASS' if ok else 'FAIL')