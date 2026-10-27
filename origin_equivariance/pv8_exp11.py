# -*- coding: utf-8 -*-
"""v8 experiment J: the two experiments the reject report demands.

J1  Direction control.  The report's counter-example is that z_T can be made
    arbitrarily large by translating along a direction orthogonal to the
    classifier's weights, while the decision function does not move.  We
    therefore inject origins of equal norm along three directions:
      parallel   c || w        -> w'c = a * sigma
      orthogonal c perp w      -> w'c = 0
      random     c ~ N(0, I)   -> w'c small but not zero
    and report z_T and the penalty for each.  z_T must rise in all three; the
    penalty must rise only in the parallel case.

J2  Sign law.  rho measures the magnitude of the induced threshold shift, so it
    cannot determine the sign of the damage (the report's point 4).  The sign
    is set by where the aligned threshold already sits.  For each cell we
    measure the threshold displacement t* that maximises balanced accuracy on
    the aligned target scores, and the induced shift of the one-sided pipeline,
    s = w'mu_A / sigma.  The law predicts
        damage = D(c, t* - s) - D(c, t*),  D(c,u) = mean[cdf(c+u), cdf(c-u)]
    and in particular the sign of the damage.  We compare the predicted sign
    with the observed one.

Output: results/exp11.txt
"""
import os
import sys
import time
import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "exp11.txt")
L = []
DS = ("2b", "2a", "gal", "ner")


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def ba_at(S, y, classes, thr):
    pred = classes[(S > thr).astype(int)] if S.ndim == 1 else None
    return C.ba(y, pred)


def best_threshold(s, y, classes):
    """Exact search for the threshold maximising balanced accuracy (K = 2)."""
    o = np.argsort(s)
    ss, yy = s[o], y[o]
    pos = (yy == classes[1]).astype(float)
    n = len(ss)
    csum = np.concatenate([[0.0], np.cumsum(pos)])
    npos, nneg = pos.sum(), n - pos.sum()
    if npos == 0 or nneg == 0:
        return 0.0
    k = np.arange(n + 1)
    tp = npos - csum[k]
    fp = (n - k) - tp
    b = 0.5 * (tp / npos + (nneg - fp) / nneg)
    i = int(np.argmax(b))
    if i == 0:
        return float(ss[0] - 1.0)
    if i >= n:
        return float(ss[-1] + 1.0)
    return float(0.5 * (ss[i - 1] + ss[i]))


def D(c, u):
    return float(0.5 * (norm.cdf(c + u) + norm.cdf(c - u)))


def pairs(ds, cap=60):
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    if cap and len(ps) > cap:
        idx = np.linspace(0, len(ps) - 1, cap).astype(int)
        ps = [ps[i] for i in idx]
    return ps


def main():
    t0 = time.time()
    rng = np.random.RandomState(13)
    say("v8 exp J   %s" % time.strftime("%H:%M:%S"))

    # ---------------- J1 direction control ----------------
    say("")
    say("=" * 92)
    say("J1  equal-norm origins, three directions   (LDA, balanced accuracy)")
    say("=" * 92)
    say("  %-5s %-12s %-5s %-9s %-10s %-10s"
        % ("ds", "direction", "n", "a", "z_T", "penalty"))
    for ds in ("2b", "gal"):
        ps = pairs(ds)
        for tag in ("parallel", "orthogonal", "random"):
            for a in (2.0, 8.0):
                zt, pen = [], []
                for p in ps:
                    A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                    clf = C.make("lda").fit(A, ya)
                    classes = np.asarray(clf.classes_)
                    if len(classes) != 2:
                        continue
                    w = np.asarray(clf.coef_, float).ravel()
                    sd = A.std(0).mean()
                    if tag == "parallel":
                        cdir = w / max(np.linalg.norm(w), 1e-12)
                    elif tag == "orthogonal":
                        u = rng.normal(size=A.shape[1])
                        u = u - (u @ w) / max(w @ w, 1e-12) * w
                        cdir = u / max(np.linalg.norm(u), 1e-12)
                    else:
                        u = rng.normal(size=A.shape[1])
                        cdir = u / max(np.linalg.norm(u), 1e-12)
                    # scale so that the induced score shift is a * sigma in the
                    # parallel case, and |c| = a * sigma in every case
                    if tag == "parallel":
                        c = cdir * (a * sd * np.linalg.norm(w)) / max(abs(float(w @ cdir)), 1e-12)
                        c = cdir * (a * sd)
                        c = cdir * (a * sd * float(np.linalg.norm(w)) / max(abs(float(w @ cdir)), 1e-12))
                        c = c / max(np.linalg.norm(c), 1e-12) * (a * sd)
                    else:
                        c = cdir * (a * sd)
                    A2, B2 = A + c, Bt + c
                    clf2 = C.make("lda").fit(A2, ya)
                    cls2 = np.asarray(clf2.classes_)
                    base = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)])
                    zero = C.ba(yb, cls2[np.argmax(
                        C.score_matrix(clf2, B2 - B2.mean(0)), 1)])
                    zt.append(float(np.linalg.norm(A2.mean(0)) / np.linalg.norm(np.maximum(A2.std(0), 1e-12))))
                    pen.append(zero - base)
                say("  %-5s %-12s %-5d %-9.1f %-10.2f %-10.4f"
                    % (ds, tag, len(zt), a, np.median(zt), np.median(pen)))

    # ---------------- J2 sign law ----------------
    say("")
    say("=" * 92)
    say("J2  sign of the damage: predicted from the pre-existing threshold error")
    say("=" * 92)
    say("  %-5s %-6s %-5s %-9s %-10s %-10s %-9s"
        % ("ds", "clf", "n", "median t*", "median shift", "damage", "sign ok"))
    for ds in ("2b", "2a", "gal"):
        for kind in ("lda", "logit", "svm"):
            tstar, shift, dmg, ok = [], [], [], 0
            for p in pairs(ds):
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                ma = np.isin(ya, [1, 2]) if ds == "2a" else np.ones(len(ya), bool)
                mb = np.isin(yb, [1, 2]) if ds == "2a" else np.ones(len(yb), bool)
                A2, ya2, B2, yb2 = A[ma], ya[ma], Bt[mb], yb[mb]
                if len(np.unique(ya2)) < 2 or len(np.unique(yb2)) < 2:
                    continue
                clf = C.make(kind).fit(A2, ya2)
                if len(np.asarray(clf.classes_)) != 2:
                    continue
                classes = np.asarray(clf.classes_)
                w = np.asarray(clf.coef_, float).ravel()
                sA = np.asarray(clf.decision_function(A2), float).ravel()
                sig = max(sA.std(), 1e-9)
                muA, muB = A2.mean(0), B2.mean(0)
                s_al = np.asarray(clf.decision_function(B2 - muB + muA), float).ravel()
                s_ze = np.asarray(clf.decision_function(B2 - muB), float).ravel()
                ts = best_threshold(s_al, yb2, classes) / sig
                sh = float(w @ muA) / sig
                c = norm.ppf(np.clip(C.ba(yb2, classes[(s_al > 0).astype(int)]), 0.01, 0.99))
                pred = D(c, ts - sh) - D(c, ts)
                obs = (C.ba(yb2, classes[(s_ze > 0).astype(int)])
                       - C.ba(yb2, classes[(s_al > 0).astype(int)]))
                tstar.append(ts)
                shift.append(sh)
                dmg.append(obs)
                if abs(obs) < 1e-6:
                    ok += 1
                elif np.sign(pred) == np.sign(obs):
                    ok += 1
            if tstar:
                say("  %-5s %-6s %-5d %-9.3f %-10.3f %-10.4f %-9.2f"
                    % (ds, kind, len(tstar), np.median(tstar), np.median(shift),
                       np.mean(dmg), ok / float(len(tstar))))
    say("")
    say("  t* = threshold that maximises BA on the aligned target scores, in source")
    say("  score SD; shift = w'mu_A / sigma, the extra displacement that the")
    say("  one-sided pipeline applies relative to the two-sided one; sign ok =")
    say("  fraction of cells whose damage sign the law predicts.")
    say("")
    say("total %.1f min" % ((time.time() - t0) / 60.0))
    print("done", P)


if __name__ == "__main__":
    main()
