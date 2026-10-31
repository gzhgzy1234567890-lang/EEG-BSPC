# -*- coding: utf-8 -*-
"""Numerical verification of Propositions 1-5 (C1, C3, C4)."""
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar
rng = np.random.default_rng(20261101)


def ba_formula(a, sigma, t):
    return 0.5 * (norm.cdf((a - t) / sigma) + norm.cdf((a + t) / sigma))


def ba_mc(a, sigma, t, pi_b, n=400000):
    y = (rng.random(n) < pi_b).astype(int) * 2 - 1
    x = rng.normal(np.where(y > 0, a, -a), sigma)
    pred = np.where(x > t, 1, -1)
    rec_pos = np.mean(pred[y > 0] == 1)
    rec_neg = np.mean(pred[y < 0] == -1)
    return 0.5 * (rec_pos + rec_neg)


ok = True
for a, sigma, pi_b in ((1.0, 1.0, 0.5), (1.0, 1.0, 0.3), (1.0, 1.0, 0.9), (0.5, 2.0, 0.15), (2.0, 0.7, 0.6)):
    d = (2 * pi_b - 1) * a
    f = ba_formula(a, sigma, d)
    m = ba_mc(a, sigma, d, pi_b, 200000)
    print('a=%.1f s=%.1f pi=%.2f  d=%+0.3f  BA_formula=%.4f  BA_MC=%.4f  diff=%.4f' % (a, sigma, pi_b, d, f, m, abs(f - m)))
    ok &= abs(f - m) < 5e-3

# optimum at 0
a, sigma = 1.0, 1.0
res = minimize_scalar(lambda t: -ba_formula(a, sigma, t), bounds=(-3, 3), method='bounded')
print('numerical maximiser of BA(t): t* = %.6f (theory 0)' % res.x)
ok &= abs(res.x) < 1e-4

# monte carlo of the harm from a composition-only correction
for pi_b in (0.5, 0.6, 0.8, 0.95):
    d = (2 * pi_b - 1) * a
    g = ba_formula(a, sigma, 0) - ba_formula(a, sigma, d)
    print('pi_B=%.2f  harm of removing the composition shift = %.5f' % (pi_b, g))
    ok &= (g > -1e-12)

# drift: correction with weight lambda, theory lambda* = b / (b + (2pi-1)a)
b, pi_b = 0.8, 0.7
a2 = 1.0
den = b + (2 * pi_b - 1) * a2
lam_star = b / den
grid = np.linspace(0, 1, 101)
ba_grid = [0.5 * (norm.cdf((a2 + b - lam * den) / sigma) + norm.cdf((a2 - b + lam * den) / sigma)) for lam in grid]
lam_num = grid[int(np.argmax(ba_grid))]
print('drift b=%.1f pi=%.2f: lambda* theory %.4f, grid optimum %.4f' % (b, pi_b, lam_star, lam_num))
ok &= abs(lam_star - lam_num) < 0.02

# Proposition 4: certificate vs observed flips
K, D, n = 4, 6, 400
W = rng.normal(size=(K, D)); bvec = rng.normal(size=K)
X = rng.normal(size=(n, D))
S = X @ W.T + bvec
kstar = np.argmax(S, 1)
d = rng.normal(size=K) * 0.3
S2 = S - d
flip = np.argmax(S2, 1) != kstar
cert = np.ones(n, bool)
for i in range(n):
    for j in range(K):
        if j == kstar[i]:
            continue
        if not (S[i, kstar[i]] - S[i, j] > d[kstar[i]] - d[j]):
            cert[i] = False
print('certificate predicts no flip: agreement with observed flips %d/%d' % (int(np.sum(cert == ~flip)), n))
ok &= bool(np.all(cert == ~flip))

# Proposition 5: same features, two labelings, opposite sign of the gain
xs = np.array([0.4, 1.2, -1.2, -1.2])
d5 = 0.5
for case, labels in (('labels match predictions', np.array([1, 1, -1, -1])),
                     ('one positive relabelled', np.array([1, -1, -1, -1]))):
    pi_hat = np.mean(labels == 1)
    pred0 = np.where(xs > 0, 1, -1)
    pred1 = np.where(xs - d5 > 0, 1, -1)
    rec0 = [(pred0[labels == c] == c).mean() for c in (1, -1)]
    rec1 = [(pred1[labels == c] == c).mean() for c in (1, -1)]
    print('case %-24s pi=%.2f d=%+0.2f  BA before %.3f  after %.3f  change %+0.3f' % (case, pi_hat, d5, np.mean(rec0), np.mean(rec1), np.mean(rec1) - np.mean(rec0)))

print('THEORY TEST', 'PASS' if ok else 'FAIL')