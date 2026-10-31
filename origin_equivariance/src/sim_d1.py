# -*- coding: utf-8 -*-
"""D1: controlled generator - baseline drift x prior shift x autocorrelation x estimator memory."""
import itertools, json, os, sys
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import balanced_accuracy_score as bas
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
OUT = os.environ.get('BSPC_RESULTS', r'G:\Work_work\math\EEG\paper_v8\results')
BLOCK = 15


def session(rng, n, a, pi, drift, rho, cond_shift=0.0, noise=0.0):
    y = (rng.random(n) < pi).astype(int)
    eps = np.zeros((n, 2))
    eps[0] = rng.normal(size=2)
    for t in range(1, n):
        eps[t] = rho * eps[t - 1] + np.sqrt(1 - rho ** 2) * rng.normal(size=2)
    mu = np.where(y[:, None] == 1, a, -a) + drift + noise * eps
    mu[:, 0] += cond_shift * y
    X = mu + rng.normal(size=(n, 2))
    return X, y


def run_cell(XA, yA, XB, yB, block):
    clf = LDA(solver='lsqr', shrinkage='auto').fit(XA, yA)
    K = len(clf.classes_)
    S = clf.decision_function(XB)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    SA = clf.decision_function(XA)
    if SA.ndim == 1:
        SA = np.column_stack([-SA, SA])
    Fm = np.eye(K) - np.ones((K, K)) / K
    n = len(yB)
    blocks = [(a, min(a + block, n)) for a in range(0, n, block)]
    d = np.array([Fm @ (S[a:b].mean(0) - SA.mean(0)) for a, b in blocks])
    corr = np.zeros_like(S)
    for k, (a, b) in enumerate(blocks):
        if k > 0:
            corr[a:b] = d[:k].mean(0)
    keep = slice(block, n)
    p0 = clf.classes_[np.argmax(S, 1)]
    p1 = clf.classes_[np.argmax(S - corr, 1)]
    return bas(yB[keep], p0[keep]), bas(yB[keep], p1[keep])


def main():
    rng = np.random.default_rng(20261101)
    a = 1.0
    rows = []
    grid_b = [0.0, 0.25, 0.5, 0.75, 1.0]
    grid_pi = [0.2, 0.35, 0.5, 0.65, 0.8]
    grid_rho = [0.0, 0.9]
    noise_level = 0.5
    n_seeds = 20
    for b, pi, rho in itertools.product(grid_b, grid_pi, grid_rho):
        deltas = []
        for s in range(n_seeds):
            XA, yA = session(rng, 600, a, 0.5, 0.0, 0.0)
            XB, yB = session(rng, 600, a, pi, b, rho, noise=noise_level)
            b0, b1 = run_cell(XA, yA, XB, yB, BLOCK)
            deltas.append(b1 - b0)
        d = np.array(deltas)
        theo = b / (b + (2 * pi - 1) * a) if (b + (2 * pi - 1) * a) > 0 else float('nan')
        rows.append(dict(b=b, pi=pi, rho=rho, delta=float(d.mean()), sd=float(d.std()),
                         pos=int((d > 0).sum()), theo_lambda=float(theo)))
        print('b=%.2f pi=%.2f rho=%.1f  deltaBA=%+0.4f (sd %.3f)  positive %2d/%d  theory lambda*=%.2f'
              % (b, pi, rho, d.mean(), d.std(), int((d > 0).sum()), n_seeds, theo), flush=True)
    json.dump(rows, open(os.path.join(OUT, 'd1_grid.json'), 'w'), indent=1)
    # agreement of the observed sign with the theory prediction: correction helps iff b > (2pi-1)a
    agree = 0
    for r in rows:
        pred_pos = abs(r['b']) > abs((2 * r['pi'] - 1) * a)
        if (r['delta'] > 0) == pred_pos:
            agree += 1
    print('sign agreement with theory (help iff |b| > |(2pi-1)a|): %d/%d' % (agree, len(rows)))


if __name__ == '__main__':
    main()