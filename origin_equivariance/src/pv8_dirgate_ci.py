# -*- coding: utf-8 -*-
"""v25b: paired intervals for the direction gate, and its held-out test."""
import glob
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_dirgate import run, pairs, K0

P = os.path.join(C.OUT, "dirgate_ci.txt")
CACHE4 = r"G:\Work_work\math\EEG\local_analysis\cache_seed4_iv"
L = []


def say(s=""):
    L.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def ci(vals):
    rs = np.random.RandomState(0)
    bs = np.array([np.mean(rs.choice(vals, len(vals))) for _ in range(4000)])
    return vals.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)


def main():
    say("v25b: direction gate, subject-level paired differences against none")
    for ds in ("2b", "2a", "seed", "gal", "ner"):
        k0 = K0[ds]
        by = {}
        for p in pairs(ds):
            r = run(p["A"], p["ya"], p["B"], p["yb"], k0)
            by.setdefault(p["subj"], []).append(
                (r["dirgate"] - r["none"], r["shrunk"] - r["none"], r["cum"] - r["none"]))
        keys = ("dirgate", "shrunk", "cum")
        say("  %-5s (%2d subjects)" % (ds, len(by)))
        for j, k in enumerate(keys):
            d = np.array([np.mean([v[j] for v in vs]) for vs in by.values()])
            m, lo, hi = ci(d)
            say("    %-8s %+.4f  95%% CI [%+.4f, %+.4f]  %s"
                % (k, m, lo, hi, "better" if lo > 0 else ("worse" if hi < 0 else "tie")))

    # held out
    say("")
    subs = sorted(set(int(os.path.basename(f).split("_")[0])
                      for f in glob.glob(os.path.join(CACHE4, "*.npz"))))
    rows = []
    for sub in subs:
        S = {}
        for sess in (1, 2, 3):
            f = os.path.join(CACHE4, "%02d_%d.npz" % (sub, sess))
            if os.path.exists(f):
                d = np.load(f)
                S[sess] = (d["X"].astype(np.float64), d["y"].astype(int))
        for i in sorted(S):
            for j in sorted(S):
                if i != j:
                    r = run(S[i][0], S[i][1], S[j][0], S[j][1], 50)
                    rows.append((sub, r))
    say("  SEED-IV held out (%d cells, %d subjects)" % (len(rows), len(set(s for s, _ in rows))))
    for k in ("dirgate", "shrunk", "cum", "oracle"):
        by = {}
        for s, r in rows:
            by.setdefault(s, []).append(r[k] - r["none"])
        d = np.array([np.mean(v) for v in by.values()])
        m, lo, hi = ci(d)
        say("    %-8s %+.4f  95%% CI [%+.4f, %+.4f]  %s"
            % (k, m, lo, hi, "better" if lo > 0 else ("worse" if hi < 0 else "tie")))
    say("    mean kappa %.2f" % np.mean([r["kappa"] for _, r in rows]))
    print("done", P)


if __name__ == "__main__":
    main()
