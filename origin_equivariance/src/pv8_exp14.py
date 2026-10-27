# -*- coding: utf-8 -*-
"""v9 experiment M: per-cell validation of the signed damage law.

For every cell and every classifier we compute the predicted change
    dhat = BA(c, t* - s) - BA(c, t*)
with c = Phi^{-1}(BA_aligned), t* the threshold displacement that maximises
balanced accuracy on the aligned target scores, and s = w'mu_A / sigma, and
compare it with the observed change
    dobs = BA(zero) - BA(mean).
We report the paired MAE, the correlation, the sign accuracy against the
majority-class baseline, and the per-cell inequality |d| <= 0.1995 |s|.

We also run the split-sample version: t* estimated on a random half of the
target trials, the sign evaluated on the other half (labels used for t* only on
the fitting half).

Output: results/exp14.txt and results/exp14.npz
"""
import os
import sys
import time
import numpy as np
from scipy.stats import norm, pearsonr, spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "exp14.txt")
L = []
DS = ("2b", "2a", "gal", "ner")


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def pairs(ds, cap=None):
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    if cap and len(ps) > cap:
        idx = np.linspace(0, len(ps) - 1, cap).astype(int)
        ps = [ps[i] for i in idx]
    return ps


def ba_thr(s, y, classes, thr):
    return C.ba(y, classes[(s > thr).astype(int)])


def best_thr(s, y, classes):
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


def main():
    t0 = time.time()
    rng = np.random.RandomState(21)
    rows = []
    say("v9 exp M: per-cell signed law   %s" % time.strftime("%H:%M:%S"))
    say("")
    say("  %-5s %-6s %-5s %-9s %-9s %-9s %-9s %-9s %-9s"
        % ("ds", "clf", "n", "MAE", "r", "rho", "sign", "base", "bound ok"))
    for ds in DS:
        for kind in ("lda", "logit", "svm"):
            dh, do, ss, tt, ok = [], [], [], [], 0
            for p in pairs(ds):
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
                if ds == "2a":
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
                ts = best_thr(s_al, yb, classes) / sig
                sh = float(w @ muA) / sig
                ba_al = ba_thr(s_al, yb, classes, 0.0)
                c = norm.ppf(np.clip(ba_al, 0.01, 0.99))
                dpred = D(c, ts - sh) - D(c, ts)
                dobs = ba_thr(s_ze, yb, classes, 0.0) - ba_al
                dh.append(dpred)
                do.append(dobs)
                ss.append(sh)
                tt.append(ts)
                ok += int(abs(dpred) <= 0.1995 * abs(sh) + 1e-9)
            if not dh:
                continue
            dh, do = np.array(dh), np.array(do)
            base = max(np.mean(do > 0), np.mean(do < 0))
            say("  %-5s %-6s %-5d %-9.4f %-9.3f %-9.3f %-9.3f %-9.3f %-9.2f"
                % (ds, kind, len(dh), np.mean(np.abs(dh - do)), pearsonr(dh, do)[0],
                   spearmanr(dh, do)[0], np.mean(np.sign(dh) == np.sign(do)),
                   base, ok / float(len(dh))))
            rows.append(dict(ds=ds, clf=kind, dhat=dh, dobs=do, t=tt, s=ss))

    say("")
    say("  bound: per-cell |dhat| <= 0.1995 |s| must hold by construction; the")
    say("  column reports the fraction of cells where it does.")
    allh = np.concatenate([r["dhat"] for r in rows])
    allo = np.concatenate([r["dobs"] for r in rows])
    say("")
    say("  pooled n=%d  MAE %.4f  r %.3f  sign %.3f  majority baseline %.3f"
        % (len(allh), np.mean(np.abs(allh - allo)), pearsonr(allh, allo)[0],
           np.mean(np.sign(allh) == np.sign(allo)),
           max(np.mean(allo > 0), np.mean(allo < 0))))

    # ---------------- split-sample sign prediction ----------------
    say("")
    say("=" * 84)
    say("M2  split-sample sign prediction: t* from half the target, sign on the other half")
    say("=" * 84)
    say("  %-5s %-6s %-5s %-9s %-9s %-9s" % ("ds", "clf", "n", "sign", "baseline", "gain"))
    for ds in ("2b", "gal"):
        for kind in ("lda", "logit", "svm"):
            hit, base = [], []
            for p in pairs(ds):
                A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
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
                ba1 = ba_thr(s_al[h1], yb[h1], classes, 0.0)
                c = norm.ppf(np.clip(ba1, 0.01, 0.99))
                pred = np.sign(D(c, ts - sh) - D(c, ts))
                obs = ba_thr(s_ze[h2], yb[h2], classes, 0.0) - ba_thr(s_al[h2], yb[h2], classes, 0.0)
                if abs(obs) < 1e-9:
                    continue
                hit.append(np.sign(pred) == np.sign(obs))
            if hit:
                say("  %-5s %-6s %-5d %-9.3f %-9.3f %-+9.3f"
                    % (ds, kind, len(hit), np.mean(hit), np.nan, np.nan))
    np.savez(os.path.join(C.OUT, "exp14.npz"),
             dhat=allh, dobs=allo,
             **{k: np.array([r[k] for r in rows]) for k in ()})
    say("")
    say("total %.1f min" % ((time.time() - t0) / 60.0))
    print("done", P)


if __name__ == "__main__":
    main()
