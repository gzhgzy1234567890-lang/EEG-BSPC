# -*- coding: utf-8 -*-
"""v19: one protocol, one test set. Batch, frozen prefix, causal running mean,
source standardisation and no correction, all scored on the same post-prefix
trials, with subject-level intervals. Includes SEED, whose block structure is
the hardest case for a running estimate.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

P = os.path.join(C.OUT, "online2.txt")
L = []
KS = {"2b": (5, 20, 50), "2a": (5, 20, 50), "gal": (5, 20, 50),
      "ner": (5, 20, 50), "seed": (5, 20, 50, 100, 200)}


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


def run_cell(A, ya, Bt, yb, ks):
    clf = C.make("lda").fit(A, ya)
    classes = np.asarray(clf.classes_)
    W = C.linear_weights(clf, A.shape[1], len(classes))
    b = np.asarray(clf.intercept_, float).ravel()
    if len(classes) == 2:
        raw = (Bt @ W[1][None, :].T).ravel() + b[0]
        S0 = np.column_stack([-raw, raw])
    else:
        S0 = Bt @ W.T + b[None, :]
    muA = A.mean(0)
    n = len(yb)
    sc = np.maximum(A.std(0), 1e-12)
    Sz = (Bt / sc) @ W.T + b               # source standardisation only
    out = {}
    for k in ks:
        if k + 20 >= n:
            continue
        T = np.arange(k, n)
        mu_batch = Bt.mean(0)
        mu_pre = Bt[:k].mean(0)
        cs = np.cumsum(Bt, axis=0)
        cnt = np.arange(1, n + 1)[:, None]
        mu_run = cs / cnt                   # mean of trials 1..i (inclusive)
        # for trial i use the mean of trials 1..i-1
        mu_run = np.vstack([np.zeros((1, Bt.shape[1])), mu_run[:-1]])
        mu_run[:1] = Bt[:1]
        methods = {
            "batch": mu_batch,
            "prefix": mu_pre,
            "run": mu_run[T],
            "std": None,
            "none": None,
        }
        for name, mu in methods.items():
            if name == "batch":
                S = S0[T] - (W @ mu)[None, :] + (W @ muA)[None, :]
            elif name == "prefix":
                S = S0[T] - (W @ mu)[None, :] + (W @ muA)[None, :]
            elif name == "run":
                S = S0[T] - mu @ W.T + (W @ muA)[None, :]
            elif name == "std":
                S = Sz[T]
            else:
                S = S0[T]
            out[(name, k)] = C.ba(yb[T], classes[np.argmax(S, 1)])
    return out


def main():
    say("v19: identical post-prefix test trials for every method (LDA)")
    say("")
    for ds in ("2b", "2a", "gal", "ner", "seed"):
        ks = KS[ds]
        rows = []
        for p in pairs(ds):
            r = run_cell(p["A"], p["ya"], p["B"], p["yb"], ks)
            if r:
                rows.append((p["subj"], r))
        if not rows:
            continue
        say("=" * 74)
        say("%s  (%d cells, %d subjects)" % (ds, len(rows), len(set(s for s, _ in rows))))
        say("=" * 74)
        say("  %-8s %-6s %-8s %-8s %-8s %-8s %-8s"
            % ("k", "n", "batch", "prefix", "run", "std", "none"))
        for k in ks:
            vals = {m: np.array([r[(m, k)] for _, r in rows if (m, k) in r])
                    for m in ("batch", "prefix", "run", "std", "none")}
            if len(vals["batch"]) == 0:
                continue
            say("  %-8d %-6d %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f"
                % (k, len(vals["batch"]), vals["batch"].mean(), vals["prefix"].mean(),
                   vals["run"].mean(), vals["std"].mean(), vals["none"].mean()))
        # subject-level paired difference: prefix - batch at the middle k
        k = ks[min(2, len(ks) - 1)]
        by = {}
        for s, r in rows:
            if ("prefix", k) in r:
                by.setdefault(s, []).append(r[("prefix", k)] - r[("batch", k)])
        d = np.array([np.mean(v) for v in by.values()])
        rs = np.random.RandomState(0)
        bs = np.array([np.mean(rs.choice(d, len(d))) for _ in range(4000)])
        say("  prefix - batch at k=%d: %+.4f  95%% CI [%+.4f, %+.4f]  (n=%d subjects)"
            % (k, d.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5), len(d)))
        say("")
    print("done", P)


if __name__ == "__main__":
    main()
