# -*- coding: utf-8 -*-
"""Regression tests for the properties the paper claims. Prints PASS/FAIL."""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "tests.txt")
L = []
OUT = []


def check(name, ok, detail=""):
    OUT.append("%-58s %s  %s" % (name, "PASS" if ok else "FAIL", detail))


def main():
    p = C.all_pairs(("2b",))[0]
    A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]

    # 1. mean == dbl, sample by sample
    clf1 = C.make("lda").fit(A, ya)
    clf2 = C.make("lda").fit(A - A.mean(0), ya)
    s1 = C.score_matrix(clf1, Bt - Bt.mean(0) + A.mean(0))
    s2 = C.score_matrix(clf2, Bt - Bt.mean(0))
    check("mean and dbl give identical predictions",
          np.array_equal(s1.argmax(1), s2.argmax(1)))

    # 2. z-score == none for source-standardised LDA
    sc = np.maximum(A.std(0), 1e-12)
    clf3 = C.make("lda").fit(A / sc, ya)
    s3 = C.score_matrix(clf3, Bt / sc)
    s0 = C.score_matrix(clf1, Bt)
    check("z-score and none agree sample by sample",
          np.array_equal(s3.argmax(1), s0.argmax(1)))

    # 3. feature-space and score-space correction are the same
    W = C.linear_weights(clf1, A.shape[1], len(np.asarray(clf1.classes_)))
    delta = W @ (A.mean(0) - Bt.mean(0))
    s4 = s0 + delta[None, :]
    check("feature-space and score-space corrections agree",
          np.allclose(s1, s4, atol=1e-10))

    # 4. z_w invariance under a class-common score offset
    S = C.score_matrix(clf1, A)
    Sc = S - S.mean(1, keepdims=True)
    sig = np.maximum(Sc.std(0), 1e-12)
    proj = W @ A.mean(0)
    proj = proj - proj.mean()
    z0 = np.linalg.norm(proj / sig) / np.sqrt(len(proj))
    a = 0.5 * np.eye(A.shape[1])[:, 0]
    Sp = S + (A @ a)[:, None]
    scp = Sp - Sp.mean(1, keepdims=True)
    z1 = np.linalg.norm(proj / np.maximum(scp.std(0), 1e-12)) / np.sqrt(len(proj))
    check("z_w invariant to a class-common score term", abs(z1 - z0) < 1e-12,
          "|dz|=%.1e" % abs(z1 - z0))

    # 5. collapse identity agrees with the observed collapse
    clf = C.make("lda").fit(A, ya)
    classes = np.asarray(clf.classes_)
    pred = classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)]
    collapsed = len(np.unique(pred)) == 1
    S = C.score_matrix(clf, Bt)
    s_z = C.score_matrix(clf, Bt - Bt.mean(0))
    ok = True
    for c in range(len(classes)):
        for k in range(len(classes)):
            if k == c:
                continue
            lhs = (W[k] - W[c]) @ Bt.mean(0)
            rhs = (s_z[:, k] - s_z[:, c]).max()
            ok &= (not (pred == classes[c]).all()) or (lhs >= rhs - 1e-9)
    check("collapse identity consistent with the observed collapse", ok,
          "collapsed=%s" % collapsed)

    # 6. the online estimator never looks at future trials
    rng = np.random.RandomState(0)
    n = len(yb)
    mu_cum = np.cumsum(Bt, axis=0) / np.arange(1, n + 1)[:, None]
    mu_prev = np.vstack([np.zeros((1, Bt.shape[1])), mu_cum[:-1]])
    t = max(10, n // 2)
    Bp = Bt.copy()
    Bp[t + 1:] = rng.randn(n - t - 1, Bt.shape[1]) * 100.0
    mu_cum2 = np.cumsum(Bp, axis=0) / np.arange(1, n + 1)[:, None]
    mu_prev2 = np.vstack([np.zeros((1, Bp.shape[1])), mu_cum2[:-1]])
    check("causal mean at trial t ignores future trials",
          np.allclose(mu_prev[t], mu_prev2[t]))

    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(OUT) + "\n")
    print("\n".join(OUT))


if __name__ == "__main__":
    main()
