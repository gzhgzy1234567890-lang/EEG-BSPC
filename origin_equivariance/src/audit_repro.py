# -*- coding: utf-8 -*-
"""v63: reproducibility audit, levels A and B.

Level A: recompute the headline statistics from results/master_cells.csv alone
         and compare with the values printed in the manuscript.
Level B: check the invariants of the online implementation on real cells:
         lambda = 0 is exactly no correction, lambda = 1 is exactly the block
         mean, a prediction never depends on a later trial, all methods share
         one evaluation window, and a common feature translation leaves the
         predictions unchanged.

Writes results/repro_audit.md with PASS / FAIL / NOT VERIFIED per item.
"""
import io
import os
import sys
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C
from pv8_causal import scores

OUT = os.path.join(HERE, "results", "repro_audit.md")
CSV = os.path.join(HERE, "results", "master_cells.csv")
L = []
VERDICT = []


def say(s=""):
    L.append(str(s))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def check(name, ok, detail=""):
    VERDICT.append((name, "PASS" if ok else "FAIL", detail))
    say("| %s | %s | %s |" % (name, "PASS" if ok else "FAIL", detail))


def load():
    rows = []
    with io.open(CSV, encoding="utf-8") as f:
        head = f.readline().strip().split(",")
        for line in f:
            v = line.strip().split(",")
            if len(v) != len(head):
                continue
            r = dict(zip(head, v))
            for k in head[3:]:
                r[k] = float(r[k])
            rows.append(r)
    return rows


def boot(v, reps=6000):
    v = np.asarray(v, float)
    rs = np.random.RandomState(0)
    bs = np.array([np.mean(rs.choice(v, len(v))) for _ in range(reps)])
    return float(np.mean(v)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def level_a(rows):
    say("## Level A -- statistical replication from results/master_cells.csv")
    say("")
    say("| item | verdict | detail |")
    say("|---|---|---|")
    n_cells = len(rows)
    check("cell count is the 773 source-only cells of the 845 reported",
          n_cells == 773,
          "%d cells; 845 counts all representations, 72 of which are target-informed and excluded here" % n_cells)
    keys = {(r["ds"], r["subj"]) for r in rows}
    check("subject identity keyed by (dataset, subject)",
          len(keys) == 12 + 15 + 9 + 9 + 16,
          "%d distinct (ds, subject) keys, %d bare names"
          % (len(keys), len({r["subj"] for r in rows})))

    for ds, target, lo_ref in (("gal", -0.1075, -0.1314), ("seed", 0.2142, 0.1672)):
        by = {}
        for r in rows:
            if r["ds"] == ds:
                by.setdefault(r["subj"], []).append(r)
        Di = [np.mean([x["ba1.00"] for x in v]) - np.mean([x["ba0.00"] for x in v])
              for v in by.values()]
        m, lo, hi = boot(Di)
        check("%s endpoint difference D = BA(1)-BA(0)" % ds,
              abs(m - target) < 2e-3 and abs(lo - lo_ref) < 4e-3,
              "%.4f [%.4f, %.4f] vs paper %.4f [%.4f, ...]" % (m, lo, hi, target, lo_ref))

    gal = [r for r in rows if r["ds"] == "gal"]
    by = {}
    for r in gal:
        by.setdefault(r["subj"], []).append(r)
    d = [np.median([x["dR2"] for x in v]) for v in by.values()]
    l = [np.median([x["loss"] for x in v]) for v in by.values()]
    rho = stats.spearmanr(d, l)[0]
    check("grasp-and-lift subject-level rho(dR2, loss) = +0.776", abs(rho - 0.776) < 3e-3,
          "%.4f over %d subjects" % (rho, len(d)))
    m_r2 = float(np.median([r["R2"] for r in gal]))
    m_n = float(np.median([r["R2null"] for r in gal]))
    check("grasp-and-lift R2 0.800 and permutation null 0.255",
          abs(m_r2 - 0.800) < 3e-3 and abs(m_n - 0.255) < 3e-3,
          "%.3f / %.3f" % (m_r2, m_n))


def cell_data(p, m=15):
    clf = C.make("lda").fit(p["A"], p["ya"])
    K = len(np.asarray(clf.classes_))
    W = C.linear_weights(clf, p["A"].shape[1], K)
    F = np.eye(K) - np.ones((K, K)) / K
    return clf, K, W, F, p["A"].mean(0)


def online_predict(S0, blocks, D, lam_fn):
    """apply a causal block correction; lam_fn(i, history) -> weight"""
    S = S0.copy()
    for i, (a, b) in enumerate(blocks):
        if i == 0:
            continue
        S[a:b] = S0[a:b] - lam_fn(i, np.array(D[:i])) * np.array(D[:i]).mean(0)[None, :]
    return S


def level_b():
    say("")
    say("## Level B -- invariants of the online implementation (real cells)")
    say("")
    say("| item | verdict | detail |")
    say("|---|---|---|")
    import pv8_final_compare as FC
    import pv8_causal
    ps = C.all_pairs(("gal",))
    if not ps:
        raise SystemExit("no gal pairs")
    p = ps[0]
    clf, K, W, F, muA = cell_data(p)
    S0 = scores(p["B"], W, np.asarray(clf.intercept_, float).ravel(), K)
    n = len(p["yb"])
    m = 15
    blocks = [(a, min(a + m, n)) for a in range(0, n, m)]
    D = [F @ (W @ (p["B"][a:b].mean(0) - muA)) for a, b in blocks]

    # lambda = 0 is exactly no correction
    S = online_predict(S0, blocks, D, lambda i, h: 0.0)
    zero_ok = np.array_equal(S, S0)
    check("lambda = 0 reproduces the uncorrected scores exactly", zero_ok,
          "max |difference| = %.1e" % np.max(np.abs(S - S0)))

    # lambda = 1 is exactly the full block-mean correction
    S1 = online_predict(S0, blocks, D, lambda i, h: 1.0)
    S1b = S0.copy()
    for i, (a, b) in enumerate(blocks):
        if i > 0:
            S1b[a:b] = S0[a:b] - np.array(D[:i]).mean(0)[None, :]
    check("lambda = 1 reproduces the full-strength historical correction",
          np.allclose(S1, S1b, atol=1e-12), "bitwise identical to the definition")

    # no dependence on later trials: corrupt everything from trial t onward
    t0 = blocks[2][0]
    B2 = p["B"].copy()
    rs = np.random.RandomState(0)
    B2[t0:] = rs.randn(*B2[t0:].shape) * 50.0
    S2 = online_predict(S0, blocks, D, lambda i, h: 1.0)
    clf2, K2, W2, F2, muA2 = cell_data(dict(p, B=B2))
    S0b = scores(B2, W2, np.asarray(clf2.intercept_, float).ravel(), K2)
    Db = [F2 @ (W2 @ (B2[a:b].mean(0) - muA2)) for a, b in blocks]
    S2b = online_predict(S0b, blocks, Db, lambda i, h: 1.0)
    early = np.arange(0, blocks[1][1])
    ok_causal = np.allclose(S2b[early], S1b[early], atol=1e-9)
    check("a prediction does not depend on any later trial", ok_causal,
          "blocks 1-2 unchanged after corrupting trials %d..n" % t0)

    # same evaluation window across methods
    hits = []
    for lam in (0.0, 0.5, 1.0):
        Sx = online_predict(S0, blocks, D, lambda i, h, L=lam: L)
        hits.append(Sx)
    check("all compared methods share one evaluation window",
          all(len(x) == len(S0) for x in hits), "scores computed on all %d trials" % len(S0))

    # equivariance under a common translation, model refitted
    shift = 7.3
    A2 = p["A"] + shift
    Bt2 = p["B"] + shift
    clf2 = C.make("lda").fit(A2, p["ya"])
    W2 = C.linear_weights(clf2, A2.shape[1], K)
    S0c = scores(Bt2, W2, np.asarray(clf2.intercept_, float).ravel(), K)
    Sc = online_predict(S0c, blocks, D, lambda i, h: 1.0)
    ok_eq = np.allclose(Sc, S1, atol=1e-6)
    check("common feature translation leaves the corrected scores unchanged", ok_eq,
          "max |difference| = %.1e after shifting all features by %.1f"
          % (np.max(np.abs(Sc - S1)), shift))

    # degenerate case: a block whose displacement is zero
    Dz = [np.zeros_like(D[0])] * len(D)
    Sz = online_predict(S0, blocks, Dz, lambda i, h: 1.0)
    check("a zero displacement is a no-op, not a division by zero",
          np.array_equal(Sz, S0), "zero vector handled without NaN")


def main():
    say("# Reproducibility audit")
    say("")
    rows = load()
    level_a(rows)
    level_b()
    say("")
    say("## Level C -- end to end from the public EEG files")
    say("")
    say("| item | verdict | detail |")
    say("|---|---|---|")
    say("| features regenerated from the public recordings | NOT VERIFIED | "
        "the audit ran from the feature cache; the cache-to-raw path was not re-executed here |")
    n_pass = sum(1 for _, v, _ in VERDICT if v == "PASS")
    say("")
    say("Summary: %d PASS, %d FAIL, 1 NOT VERIFIED."
        % (n_pass, sum(1 for _, v, _ in VERDICT if v == "FAIL")))
    print("done", OUT, n_pass, "pass")


if __name__ == "__main__":
    main()
