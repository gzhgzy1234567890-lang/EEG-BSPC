# -*- coding: utf-8 -*-
"""v8 experiment G: two additions requested by the internal referee.

G1  composition with alignment.  Within each of three representations that do
    or do not already use a second-order correction (euc: none; euc_ea:
    Euclidean alignment; tan: Riemannian tangent space), compare none with the
    mean correction.  If the first-order correction still helps inside the
    aligned representations, the two corrections compose rather than substitute.

G2  the classifier sweep on a second exposed dataset.  BCI-2a restricted to the
    two motor-imagery classes of the first two classes (left vs right hand),
    fourteen regularisation settings, damage against rho.

Output: results/exp7_<tag>.txt
"""
import os
import sys
import time
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "exp7.txt")
L = []


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    t0 = time.time()
    say("v8 exp G   %s" % time.strftime("%H:%M:%S"))
    say("")
    say("=" * 96)
    say("G1  does the first-order correction still help after a second-order one?")
    say("=" * 96)
    say("  %-5s %-7s %-5s %-9s %-9s %-9s" % ("ds", "rep", "n", "none", "mean", "gain"))
    for ds in ("2a", "2b"):
        for repname in ("euc", "euc_ea", "tan", "csp"):
            ps = [p for p in C.all_pairs((ds,)) if p["rep"] == repname]
            if not ps:
                continue
            a, b = [], []
            for p in ps:
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                clf = C.make("lda").fit(A, ya)
                classes = np.asarray(clf.classes_)
                g = Bt.mean(0) - A.mean(0)
                a.append(C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
                b.append(C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - g), 1)]))
            say("  %-5s %-7s %-5d %-9.4f %-9.4f %-+9.4f"
                % (ds, repname, len(ps), np.mean(a), np.mean(b), np.mean(b) - np.mean(a)))
    say("")
    say("=" * 96)
    say("G2  classifier sweep on BCI-2a, classes 1 and 2 only")
    say("=" * 96)
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import LinearSVC

    def mk(kind, param):
        if kind == "lda":
            return LDA(solver="lsqr", shrinkage=param)
        if kind == "logit":
            return LogisticRegression(C=param, max_iter=4000, solver="lbfgs")
        return LinearSVC(C=param, max_iter=20000, dual=False, tol=1e-4)

    configs = ([("lda", s) for s in (0.1, 0.5, 0.9, "auto")] +
               [("logit", c) for c in (0.01, 0.1, 1.0, 10.0)] +
               [("svm", c) for c in (0.001, 0.01, 0.1, 1.0, 10.0)])
    rows = []
    ps = [p for p in C.all_pairs(("2a",)) if p["rep"] == "euc"]
    say("  cells = %d (rep euc, classes 1/2)" % len(ps))
    say("  %-6s %-6s %-9s %-9s %-9s %-9s" % ("clf", "param", "none", "zero", "damage", "rho"))
    for kind, param in configs:
        a, z, rr = [], [], []
        for p in ps:
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            ma = np.isin(ya, [1, 2])
            mb = np.isin(yb, [1, 2])
            A2, ya2, B2, yb2 = A[ma], ya[ma], Bt[mb], yb[mb]
            if len(np.unique(ya2)) < 2 or len(np.unique(yb2)) < 2:
                continue
            clf = mk(kind, param).fit(A2, ya2)
            if len(np.asarray(clf.classes_)) != 2:
                continue
            sA = np.asarray(clf.decision_function(A2), float).ravel()
            w = np.asarray(clf.coef_, float).ravel()
            rr.append(abs(float(w @ B2.mean(0))) / max(sA.std(), 1e-9))
            classes = np.asarray(clf.classes_)
            a.append(C.ba(yb2, classes[np.argmax(C.score_matrix(clf, B2), 1)]))
            z.append(C.ba(yb2, classes[np.argmax(C.score_matrix(clf, B2 - B2.mean(0)), 1)]))
        if not a:
            continue
        dm = np.mean(z) - np.mean(a)
        rows.append((kind, str(param), np.mean(a), np.mean(z), dm, np.median(rr)))
        say("  %-6s %-6s %-9.4f %-9.4f %-+9.4f %-9.3f" % rows[-1])
    if rows:
        rho = np.array([r[5] for r in rows])
        dm = np.array([r[4] for r in rows])
        say("")
        say("  spearman(rho, median damage) = %+.3f (p=%.2e, n=%d)"
            % (stats.spearmanr(rho, dm)[0], stats.spearmanr(rho, dm)[1], len(rows)))
    say("")
    say("total %.1f min" % ((time.time() - t0) / 60.0))
    print("done", P)


if __name__ == "__main__":
    main()
