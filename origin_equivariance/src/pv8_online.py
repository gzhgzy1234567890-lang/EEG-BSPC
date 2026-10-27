# -*- coding: utf-8 -*-
"""v18 experiment B: prefix-calibration online protocol, and a source-only
estimate of the threshold error."""
import os
import sys
import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_exp14 import best_thr, ba_thr

P = os.path.join(C.OUT, "online_labelfree.txt")
L = []
KS = (5, 10, 20, 50, 100)


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


def online(ds, seeds=5):
    """Prefix calibration: freeze the mean from the first k trials, test later."""
    out = {k: [] for k in KS}
    rng = np.random.RandomState(0)
    for p in pairs(ds):
        A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
        clf = C.make("lda").fit(A, ya)
        classes = np.asarray(clf.classes_)
        muA = A.mean(0)
        n = len(yb)
        for s in range(seeds):
            order = rng.permutation(n) if s > 0 else np.arange(n)
            X, y = Bt[order], yb[order]
            cs = np.cumsum(X, axis=0)
            for k in KS:
                if k + 10 >= n:
                    continue
                mu = cs[k - 1] / k
                S = C.score_matrix(clf, X[k:] - mu + muA)
                out[k].append(C.ba(y[k:], classes[np.argmax(S, 1)]))
    return out


def labelfree(ds):
    """Source-only threshold error: the source-optimal threshold vs the model's 0."""
    rows = []
    for p in pairs(ds):
        A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
        if ds == "2a":
            ma, mb = np.isin(ya, [1, 2]), np.isin(yb, [1, 2])
            A, ya, Bt, yb = A[ma], ya[ma], Bt[mb], yb[mb]
        if len(np.unique(ya)) < 2 or len(np.unique(yb)) < 2:
            continue
        clf = C.make("lda").fit(A, ya)
        classes = np.asarray(clf.classes_)
        w = np.asarray(clf.coef_, float).ravel()
        sA = np.asarray(clf.decision_function(A), float).ravel()
        m0 = sA[ya == classes[0]].mean()
        m1 = sA[ya == classes[1]].mean()
        sig_w = max(np.sqrt(0.5 * (sA[ya == classes[0]].var(ddof=1)
                                   + sA[ya == classes[1]].var(ddof=1))), 1e-9)
        c = (m1 - m0) / (2 * sig_w)
        t_src = best_thr(sA, ya, classes) / sig_w      # source optimal threshold
        muA, muB = A.mean(0), Bt.mean(0)
        s_al = np.asarray(clf.decision_function(Bt - muB + muA), float).ravel()
        s_ze = np.asarray(clf.decision_function(Bt - muB), float).ravel()
        sh = float(w @ muA) / sig_w
        obs = ba_thr(s_ze, yb, classes, 0.0) - ba_thr(s_al, yb, classes, 0.0)
        d0 = 0.5 * (norm.cdf(c) + norm.cdf(c)) - 0.5 * (norm.cdf(c) + norm.cdf(c))
        pred_lf = (0.5 * (norm.cdf(c + t_src + sh) + norm.cdf(c - t_src - sh))
                   - 0.5 * (norm.cdf(c + t_src) + norm.cdf(c - t_src)))
        rows.append((obs, pred_lf, c, t_src, sh))
    return np.array(rows)


def main():
    say("v18 B1: prefix-calibration online protocol (LDA, mean over seeds and cells)")
    say("  %-5s %-8s %-9s %-9s %-9s %-9s" % ("ds", "batch", "k=5", "k=20", "k=50", "k=100"))
    for ds in ("2b", "2a", "gal", "ner"):
        out = online(ds)
        batch = []
        for p in pairs(ds):
            clf = C.make("lda").fit(p["A"], p["ya"])
            cl = np.asarray(clf.classes_)
            g = p["B"].mean(0) - p["A"].mean(0)
            batch.append(C.ba(p["yb"], cl[np.argmax(C.score_matrix(clf, p["B"] - g), 1)]))
        say("  %-5s %-8.4f %-9.4f %-9.4f %-9.4f %-9.4f"
            % (ds, np.mean(batch),
               np.mean(out[5]) if out[5] else np.nan,
               np.mean(out[20]) if out[20] else np.nan,
               np.mean(out[50]) if out[50] else np.nan,
               np.mean(out[100]) if out[100] else np.nan))

    say("")
    say("v18 B2: source-only threshold error")
    say("  %-5s %-6s %-5s %-9s %-9s %-9s" % ("ds", "clf", "n", "MAE", "sign", "base"))
    for ds in ("2b", "gal", "2a"):
        r = labelfree(ds)
        if len(r) == 0:
            continue
        obs, pred = r[:, 0], r[:, 1]
        base = max(np.mean(obs > 0), np.mean(obs < 0))
        say("  %-5s %-6s %-5d %-9.4f %-9.3f %-9.3f"
            % (ds, "lda", len(obs), np.mean(np.abs(pred - obs)),
               np.mean(np.sign(pred) == np.sign(obs)), base))
    say("")
    say("  the source-only threshold t* is the source-optimal threshold of the")
    say("  fitted model, in within-class SD units; the prediction uses it in")
    say("  place of the target-optimal threshold.")
    print("done", P)


if __name__ == "__main__":
    main()
