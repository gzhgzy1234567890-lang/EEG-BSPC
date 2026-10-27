# -*- coding: utf-8 -*-
"""v8 experiment E: why the damage depends on the classifier family.

The one-sided pipeline subtracts the target mean from the features, which
translates the decision function by w'mu_T.  For a binary problem this is a
threshold shift, so what matters is (i) how large that shift is in units of the
training score spread, rho = |w'mu_T| / sd(s_train), and (ii) where the
threshold already sits.  rho is measurable without target labels.

If the damage is a function of rho rather than of the classifier family, then a
sweep over the regularisation of three families should collapse onto one curve.

Output: results/exp5_<tag>.txt
"""
import os
import sys
import time
import numpy as np
from scipy import stats
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

TAG = sys.argv[1] if len(sys.argv) > 1 else "2b,seed,gal"
LOG = []
P = os.path.join(C.OUT, "exp5_%s.txt" % TAG)


def say(s=""):
    LOG.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")


def mk(kind, param):
    if kind == "lda":
        return LDA(solver="lsqr", shrinkage=param)
    if kind == "logit":
        return LogisticRegression(C=param, max_iter=4000, solver="lbfgs")
    return LinearSVC(C=param, max_iter=20000, dual=False, tol=1e-4)


def main():
    t0 = time.time()
    dss = TAG.split(",")
    say("v8 exp E: classifier family and the induced shift   %s" % time.strftime("%H:%M:%S"))
    say("  rho = |w'mu_T| / sd(s_train) ; damage = BA(one-sided) - BA(none)")
    say("")
    configs = ([("lda", s) for s in (0.1, 0.3, 0.6, 0.9, "auto")] +
               [("logit", c) for c in (0.01, 0.1, 1.0, 10.0)] +
               [("svm", c) for c in (0.001, 0.01, 0.1, 1.0, 10.0)])
    allrows = []
    for ds in dss:
        ps = C.all_pairs((ds,))
        if ds == "gal":
            ps = [p for p in ps
                  if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
        if len(ps) > 60:
            idx = np.linspace(0, len(ps) - 1, 60).astype(int)
            ps = [ps[i] for i in idx]
        say("=== %s : %d cells ===" % (ds, len(ps)))
        say("  %-6s %-6s %-9s %-9s %-9s %-9s"
            % ("clf", "param", "none", "zero", "damage", "rho"))
        for kind, param in configs:
            acc = {"none": [], "zero": [], "rho": []}
            for p in ps:
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                clf = mk(kind, param).fit(A, ya)
                if len(np.asarray(clf.classes_)) != 2:
                    continue
                classes = np.asarray(clf.classes_)
                sA = np.asarray(clf.decision_function(A), float).ravel()
                sB = np.asarray(clf.decision_function(Bt), float).ravel()
                w = np.asarray(clf.coef_, float).ravel()
                rho = abs(float(w @ Bt.mean(0))) / max(sA.std(), 1e-9)
                Pn = classes[np.argmax(C.score_matrix(clf, Bt), 1)]
                Pz = classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)]
                acc["none"].append(C.ba(yb, Pn))
                acc["zero"].append(C.ba(yb, Pz))
                acc["rho"].append(rho)
            if not acc["none"]:
                continue
            dm = np.mean(acc["zero"]) - np.mean(acc["none"])
            say("  %-6s %-6s %-9.4f %-9.4f %-+9.4f %-9.3f"
                % (kind, str(param), np.mean(acc["none"]), np.mean(acc["zero"]),
                   dm, np.median(acc["rho"])))
            allrows.append((ds, kind, str(param), dm,
                            np.median(acc["rho"]),
                            np.median(np.array(acc["zero"]) - np.array(acc["none"]))))
        say("")
    say("=" * 96)
    say("E2  across all configurations: is the damage a function of rho?")
    say("=" * 96)
    rho = np.array([r[4] for r in allrows])
    dm = np.array([r[3] for r in allrows])
    med = np.array([r[5] for r in allrows])
    say("  n=%d configurations" % len(rho))
    say("  spearman(rho, mean damage)   = %+.3f (p=%.2e)" % stats.spearmanr(rho, dm))
    say("  spearman(rho, median damage) = %+.3f (p=%.2e)" % stats.spearmanr(rho, med))
    say("")
    say("  %-5s %-6s %-6s %-9s %-9s" % ("ds", "clf", "param", "rho", "damage"))
    for r in allrows:
        say("  %-5s %-6s %-6s %-9.3f %-+9.4f" % r[:5])


if __name__ == "__main__":
    main()
