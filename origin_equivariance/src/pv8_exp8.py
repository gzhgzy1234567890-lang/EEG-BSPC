# -*- coding: utf-8 -*-
"""v8 experiment H: streaming reference under the real trial order.

The previous streaming test drew the target trials in a random order.  A real
session is not shuffled, and its first trials are not exchangeable with the
rest: block structure and time-on-task drift mean that a warm-up drawn from the
beginning of a session is a biased sample of it.

This script therefore runs the running-reference pipeline twice, once in the
recorded order and once in a random order, and additionally reports the number
of trials needed for the running mean to come within 10 per cent of the session
mean, as a function of z_T.

Output: results/exp8_<tag>.txt
"""
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

TAG = sys.argv[1] if len(sys.argv) > 1 else "2b,seed,gal,2a"
LOG = []
P = os.path.join(C.OUT, "exp8_%s.txt" % TAG)


def say(s=""):
    LOG.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")


def run_stream(A, ya, Bt, yb, clf, classes, order):
    B2, y2 = Bt[order], yb[order]
    muA = A.mean(0)
    run = muA.copy()
    n = len(y2)
    preds = np.empty(n, dtype=classes.dtype)
    conv = np.nan
    true_mu = Bt.mean(0)
    for i in range(n):
        preds[i] = classes[np.argmax(
            C.score_matrix(clf, (B2[i] - run + muA)[None, :]), 1)[0]]
        run = run + (B2[i] - run) / (i + 2.0)
        if np.isnan(conv) and np.linalg.norm(run - true_mu) <= 0.1 * np.linalg.norm(true_mu - muA):
            conv = i + 2
    out = {"conv": conv}
    for k in (5, 10, 20, 50):
        if n > k + 5:
            out[k] = C.ba(y2[k:], preds[k:])
    out["all"] = C.ba(y2, preds)
    return out


def main():
    t0 = time.time()
    dss = TAG.split(",")
    say("v8 exp H: streaming under the recorded trial order   %s" % time.strftime("%H:%M:%S"))
    say("")
    say("  %-5s %-6s %-8s %-8s %-8s %-8s %-9s %-9s"
        % ("ds", "order", "k=5", "k=10", "k=20", "k=50", "all", "batch"))
    rng = np.random.RandomState(5)
    for ds in dss:
        ps = C.all_pairs((ds,))
        if ds == "gal":
            ps = [p for p in ps
                  if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
        if len(ps) > 60:
            idx = np.linspace(0, len(ps) - 1, 60).astype(int)
            ps = [ps[i] for i in idx]
        res = {"natural": {5: [], 10: [], 20: [], 50: [], "all": [], "conv": []},
               "random": {5: [], 10: [], 20: [], 50: [], "all": [], "conv": []},
               "batch": []}
        zT, conv = [], []
        for p in ps:
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            muA = A.mean(0)
            zT.append(float(np.linalg.norm(muA) / np.linalg.norm(np.maximum(A.std(0), 1e-12))))
            for tag, order in (("natural", np.arange(len(yb))),
                               ("random", rng.permutation(len(yb)))):
                o = run_stream(A, ya, Bt, yb, clf, classes, order)
                for k in (5, 10, 20, 50, "all", "conv"):
                    if k in o and np.isfinite(o[k]):
                        res[tag][k].append(o[k])
            g = Bt.mean(0) - muA
            res["batch"].append(C.ba(yb, classes[np.argmax(
                C.score_matrix(clf, Bt - g), 1)]))
        for tag in ("natural", "random"):
            f = lambda k: np.nanmean(res[tag][k]) if res[tag][k] else np.nan
            say("  %-5s %-6s %-8.4f %-8.4f %-8.4f %-8.4f %-9.4f %-9.4f"
                % (ds, tag, f(5), f(10), f(20), f(50), f("all"), np.mean(res["batch"])))
        say("        median trials to converge (natural order): %.0f ; median z_T %.2f ; "
            "spearman(z_T, converge) %.3f"
            % (np.nanmedian(res["natural"]["conv"]), np.median(zT),
               __import__("scipy.stats", fromlist=["spearmanr"]).spearmanr(zT, res["natural"]["conv"])[0]))
        say("")
    say("total %.1f min" % ((time.time() - t0) / 60.0))
    print("done", P)


if __name__ == "__main__":
    main()
