# -*- coding: utf-8 -*-
"""v10 experiment P: the four checks the second report asks for.

P1  the bound |d| <= 0.1995 |s|: violation rate for the theoretical prediction
    and for the observed change, separately
P2  z_w as a matrix definition: invariance to a class-common score offset and
    to a feature translation in the null space of P W; centred versus
    uncentred sigma
P3  operating points: threshold chosen by leave-one-dataset-out, then
    sensitivity, specificity and precision on the held-out dataset
P4  split-sample sign AUC with bootstrap intervals, and the SVM wording
"""
import os
import sys
import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_exp14 import best_thr, ba_thr, D

P = os.path.join(C.OUT, "exp17.txt")
L = []
DS = ("2a", "2b", "seed", "ner", "gal")


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def pairs(ds):
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    return ps


def auc(y, s):
    y = np.asarray(y, int)
    s = np.asarray(s, float)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    allv = np.concatenate([pos, neg])
    r = np.argsort(np.argsort(allv)) + 1.0
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg)))


def main():
    say("v10 exp P")

    # ---------------- P1 bound ----------------
    say("")
    say("=" * 80)
    say("P1  the theoretical bound, applied to the prediction and to the observation")
    say("=" * 80)
    vt = vo = n = 0
    ratios = []
    for ds in ("2b", "2a", "gal", "ner"):
        for p in pairs(ds):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            if ds == "2a":
                ma, mb = np.isin(ya, [1, 2]), np.isin(yb, [1, 2])
                A, ya, Bt, yb = A[ma], ya[ma], Bt[mb], yb[mb]
            if len(np.unique(ya)) < 2 or len(np.unique(yb)) < 2:
                continue
            clf = C.make("lda").fit(A, ya)
            if len(np.asarray(clf.classes_)) != 2:
                continue
            classes = np.asarray(clf.classes_)
            w = np.asarray(clf.coef_, float).ravel()
            sA = np.asarray(clf.decision_function(A), float).ravel()
            sig = max(sA.std(), 1e-9)
            muA, muB = A.mean(0), Bt.mean(0)
            s_al = np.asarray(clf.decision_function(Bt - muB + muA), float).ravel()
            s_ze = np.asarray(clf.decision_function(Bt - muB), float).ravel()
            ts = best_thr(s_al, yb, classes) / sig
            sh = float(w @ muA) / sig
            ba = ba_thr(s_al, yb, classes, 0.0)
            c = norm.ppf(np.clip(ba, 0.01, 0.99))
            dp = D(c, ts - sh) - D(c, ts)
            do = ba_thr(s_ze, yb, classes, 0.0) - ba
            n += 1
            if abs(dp) > 0.1995 * abs(sh) + 1e-9:
                vt += 1
            if abs(do) > 0.1995 * abs(sh) + 1e-9:
                vo += 1
                ratios.append(abs(do) / max(abs(sh), 1e-9))
    say("  cells %d" % n)
    say("  theoretical prediction violating the bound: %d (%.3f%%)" % (vt, 100.0 * vt / n))
    say("  observed change violating the bound    : %d (%.3f%%)" % (vo, 100.0 * vo / n))
    if ratios:
        say("  when the observation violates, |do|/|s| median %.2f, max %.2f"
            % (np.median(ratios), np.max(ratios)))

    # ---------------- P2 z_w invariances ----------------
    say("")
    say("=" * 80)
    say("P2  z_w: two invariances and the centred/uncentred scale")
    say("=" * 80)
    dev_common = dev_null = dev_scale = 0.0
    for ds in ("2b", "seed", "2a"):
        for p in pairs(ds)[:20]:
            A, ya = p["A"], p["ya"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            K = len(classes)
            S = C.score_matrix(clf, A)
            W = C.linear_weights(clf, A.shape[1], K)

            def zw_of(mu, S):
                proj = W @ mu
                proj = proj - proj.mean()
                sig = np.maximum(S.std(0), 1e-12)
                return float(np.linalg.norm(proj / sig) / np.sqrt(K))

            z0 = zw_of(A.mean(0), S)
            # class-common score offset: add the same constant to every column
            z1 = zw_of(A.mean(0), S + 3.0)
            dev_common = max(dev_common, abs(z1 - z0))
            # feature translation in the null space of P W
            U, sv, Vt = np.linalg.svd(W)
            ns = Vt.T[:, W.shape[0]:]
            if ns.shape[1] > 0:
                u = ns[:, 0]
                z2 = zw_of(A.mean(0) + 5.0 * u, S)
                dev_null = max(dev_null, abs(z2 - z0))
            # centred versus uncentred sigma
            Sc = S - S.mean(1, keepdims=True)
            sig_c = np.maximum(Sc.std(0), 1e-12)
            zc = float(np.linalg.norm(((W @ A.mean(0)) - (W @ A.mean(0)).mean()) / sig_c) / np.sqrt(K))
            dev_scale = max(dev_scale, abs(zc - z0))
    say("  max |z_w(common score offset) - z_w|      = %.2e" % dev_common)
    say("  max |z_w(feature shift in null(PW)) - z_w| = %.2e" % dev_null)
    say("  max |z_w(centred sigma) - z_w(uncentred)|  = %.3f  (definition matters)" % dev_scale)

    # ---------------- P3 operating points ----------------
    say("")
    say("=" * 80)
    say("P3  threshold from four datasets, applied to the fifth")
    say("=" * 80)
    rows = []
    for ds in DS:
        for p in pairs(ds):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            K = len(classes)
            muA = A.mean(0)
            S = C.score_matrix(clf, A)
            sig = np.maximum(S.std(0), 1e-12)
            W = C.linear_weights(clf, A.shape[1], K)
            proj = W @ muA
            proj = proj - proj.mean()
            zw = float(np.linalg.norm(proj / sig) / np.sqrt(K))
            pen = (C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - Bt.mean(0)), 1)])
                   - C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)]))
            rows.append((ds, zw, pen))
    ds = np.array([r[0] for r in rows])
    zw = np.array([r[1] for r in rows])
    pen = np.array([r[2] for r in rows])
    y = (pen < -0.05).astype(int)
    say("  %-7s %-5s %-8s %-8s %-8s %-8s" % ("held", "n", "thresh", "sens", "spec", "prec"))
    for held in DS:
        tr, te = ds != held, ds == held
        # pick the threshold that maximises Youden's J on the training datasets
        cand = np.unique(zw[tr])
        best, thr = -1, cand[0]
        for t in cand:
            se = np.mean(zw[tr][y[tr] == 1] > t) if (y[tr] == 1).sum() else np.nan
            sp = np.mean(zw[tr][y[tr] == 0] <= t) if (y[tr] == 0).sum() else np.nan
            if np.isfinite(se) and np.isfinite(sp) and se + sp - 1 > best:
                best, thr = se + sp - 1, t
        tp = np.sum((zw[te] > thr) & (y[te] == 1))
        fp = np.sum((zw[te] > thr) & (y[te] == 0))
        fn = np.sum((zw[te] <= thr) & (y[te] == 1))
        tn = np.sum((zw[te] <= thr) & (y[te] == 0))
        se = tp / max(tp + fn, 1)
        sp = tn / max(tn + fp, 1)
        pr = tp / max(tp + fp, 1)
        say("  %-7s %-5d %-8.3f %-8.3f %-8.3f %-8.3f" % (held, te.sum(), thr, se, sp, pr))

    # ---------------- P4 split-sample AUC with CI ----------------
    say("")
    say("=" * 80)
    say("P4  split-sample sign AUC with bootstrap intervals")
    say("=" * 80)
    rng = np.random.RandomState(21)
    say("  %-5s %-6s %-5s %-8s %-18s" % ("ds", "clf", "n", "AUC", "95% CI"))
    for dsx in ("2b", "gal", "2a"):
        for kind in ("lda", "logit", "svm"):
            sp, so = [], []
            for p in pairs(dsx):
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                if dsx == "2a":
                    ma, mb = np.isin(ya, [1, 2]), np.isin(yb, [1, 2])
                    A, ya, Bt, yb = A[ma], ya[ma], Bt[mb], yb[mb]
                if len(np.unique(ya)) < 2 or len(np.unique(yb)) < 2:
                    continue
                clf = C.make(kind).fit(A, ya)
                if len(np.asarray(clf.classes_)) != 2:
                    continue
                classes = np.asarray(clf.classes_)
                w = np.asarray(clf.coef_, float).ravel()
                sA = np.asarray(clf.decision_function(A), float).ravel()
                sig = max(sA.std(), 1e-9)
                muA, muB = A.mean(0), Bt.mean(0)
                s_al = np.asarray(clf.decision_function(Bt - muB + muA), float).ravel()
                s_ze = np.asarray(clf.decision_function(Bt - muB), float).ravel()
                idx = rng.permutation(len(yb))
                h1, h2 = idx[:len(idx) // 2], idx[len(idx) // 2:]
                if len(np.unique(yb[h1])) < 2:
                    continue
                ts = best_thr(s_al[h1], yb[h1], classes) / sig
                sh = float(w @ muA) / sig
                c = norm.ppf(np.clip(ba_thr(s_al[h1], yb[h1], classes, 0.0), 0.01, 0.99))
                sp.append(D(c, ts - sh) - D(c, ts))
                so.append(ba_thr(s_ze[h2], yb[h2], classes, 0.0)
                          - ba_thr(s_al[h2], yb[h2], classes, 0.0))
            if len(sp) < 10:
                continue
            sp, so = np.array(sp), np.array(so)
            yk = (so < 0).astype(int)
            a = auc(yk, -sp)
            bs = []
            for _ in range(2000):
                i = rng.randint(0, len(sp), len(sp))
                if len(np.unique(yk[i])) < 2:
                    continue
                bs.append(auc(yk[i], -sp[i]))
            bs = np.array(bs)
            say("  %-5s %-6s %-5d %-8.3f [%.3f, %.3f]"
                % (dsx, kind, len(sp), a, np.percentile(bs, 2.5), np.percentile(bs, 97.5)))
    print("done", P)


if __name__ == "__main__":
    main()
