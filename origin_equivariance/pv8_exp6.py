# -*- coding: utf-8 -*-
"""v8 experiment F: deployment.

The correction needs the target session's mean.  A pipeline that references its
features *within the session it is computed on* has the correction built in and
therefore needs no post-hoc access to the target mean: the running mean of the
trials seen so far replaces the session mean.  This section measures how fast
that converges, and whether it lands on the batch correction.

Protocol per cell: draw the target trials in a random order, predict each trial
with the running reference from the trials already seen (warm start: the source
mean), accumulate balanced accuracy over the whole stream.

Output: results/exp6_<tag>.txt
"""
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

TAG = sys.argv[1] if len(sys.argv) > 1 else "2b,seed"
LOG = []
P = os.path.join(C.OUT, "exp6_%s.txt" % TAG)


def say(s=""):
    LOG.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")


def main():
    t0 = time.time()
    dss = TAG.split(",")
    say("v8 exp F: streaming reference   %s" % time.strftime("%H:%M:%S"))
    say("  running mean = mean of the first k target trials, warm-started at the source mean")
    say("")
    say("  %-5s %-6s %-8s %-8s %-8s %-8s %-8s %-8s"
        % ("ds", "n", "k=5", "k=10", "k=20", "k=50", "k=all", "batch"))
    rng = np.random.RandomState(3)
    for ds in dss:
        ps = C.all_pairs((ds,))
        if ds == "gal":
            ps = [p for p in ps
                  if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
        if len(ps) > 60:
            idx = np.linspace(0, len(ps) - 1, 60).astype(int)
            ps = [ps[i] for i in idx]
        res = {k: [] for k in (5, 10, 20, 50, "all", "batch")}
        for p in ps:
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            order = rng.permutation(len(yb))
            B2, y2 = Bt[order], yb[order]
            n = len(y2)
            # running mean of target features, warm start = source mean
            run = A.mean(0).copy()
            preds = np.empty(n, dtype=classes.dtype)
            for i in range(n):
                preds[i] = classes[np.argmax(C.score_matrix(clf, (B2[i] - run + A.mean(0))[None, :]), 1)[0]]
                run = run + (B2[i] - run) / (i + 2.0)
            for k in (5, 10, 20, 50, "all"):
                if k == "all":
                    m = np.ones(n, bool)
                elif n <= k:
                    continue
                else:
                    m = np.zeros(n, bool)
                    m[k:] = True
                # evaluate only on trials after the warm-up
                if m.sum() < 5:
                    continue
                res[k].append(C.ba(y2[m], preds[m]))
            g = Bt.mean(0) - A.mean(0)
            res["batch"].append(C.ba(yb, classes[np.argmax(
                C.score_matrix(clf, Bt - g), 1)]))
        f = lambda k: np.mean(res[k]) if res[k] else np.nan
        say("  %-5s %-6d %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f"
            % (ds, len(ps), f(5), f(10), f(20), f(50), f("all"), f("batch")))
    say("")
    say("total %.1f min" % ((time.time() - t0) / 60.0))
    print("done", P)


if __name__ == "__main__":
    main()
