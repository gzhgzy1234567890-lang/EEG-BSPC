# -*- coding: utf-8 -*-
"""v8 analysis: representation-level structure of the screen.

Rebuilds the (dataset, representation) labels in the same order as exp2 and
asks the questions that decide how the screen can be used:

  * is z_T a representation-level or a cell-level quantity?
  * within a representation, does z_T still order the recoverable fraction?
  * what does a cross-validated threshold buy?

Output: results/analyze_<tag>.txt
"""
import os
import sys
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

TAG = sys.argv[1] if len(sys.argv) > 1 else "2a,2b,seed,ner,gal"
LOG = []
P = os.path.join(C.OUT, "analyze_%s.txt" % TAG)


def say(s=""):
    LOG.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")


def load_rows(tag):
    z = np.load(os.path.join(C.OUT, "exp2_%s.npz" % tag))
    return {k: z[k] for k in z.files}


def main():
    dss = tuple(TAG.split(","))
    z = load_rows(TAG)
    meta = []
    for ds in dss:
        pairs = C.all_pairs((ds,))
        if ds == "gal":
            pairs = [p for p in pairs
                     if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
        for p in pairs:
            zt = float(np.linalg.norm(p["B"].mean(0) - p["A"].mean(0))
                       / np.linalg.norm(np.maximum(p["A"].std(0), 1e-12)))
            meta.append((ds, p["rep"], p["subj"], zt))
    assert len(meta) == len(z["zT"]), (len(meta), len(z["zT"]))
    err = max(abs(meta[i][3] - z["zT"][i]) for i in range(len(meta)))
    say("rebuild check: max |z_T rebuild - saved| = %.2e" % err)

    ds = np.array([m[0] for m in meta])
    rep = np.array([m[1] for m in meta])
    subj = np.array([m[2] for m in meta])
    zT = z["zT"]
    gap = z["gap"]
    rec = z["recover"]
    resid = z["resid"]
    h = z["h"]
    ok = gap > 0.02
    frac = np.where(ok, rec / np.maximum(gap, 1e-9), np.nan)

    say("")
    say("=" * 100)
    say("E1  z_T by representation (this is a representation-level quantity)")
    say("=" * 100)
    say("  %-5s %-7s %-5s %-9s %-9s %-9s %-9s"
        % ("ds", "rep", "n", "median zT", "median gap", "median rec", "median frac"))
    units = sorted(set(zip(ds, rep)))
    for u in units:
        m = (ds == u[0]) & (rep == u[1])
        if m.sum() == 0:
            continue
        say("  %-5s %-7s %-5d %-9.2f %-9.4f %-9.4f %-9.3f"
            % (u[0], u[1], int(m.sum()), np.median(zT[m]), np.median(gap[m]),
               np.median(rec[m]), np.nanmedian(frac[m])))

    say("")
    say("=" * 100)
    say("E2  within-representation: does z_T still order the recoverable fraction?")
    say("=" * 100)
    say("  %-5s %-7s %-5s %-9s %-9s" % ("ds", "rep", "n", "rho(zT,frac)", "p"))
    pooled = []
    for u in units:
        m = (ds == u[0]) & (rep == u[1]) & ok
        if m.sum() < 8 or np.nanstd(frac[m]) == 0 or np.std(zT[m]) == 0:
            continue
        r = stats.spearmanr(zT[m], frac[m])
        say("  %-5s %-7s %-5d %-9.3f %-9.3f" % (u[0], u[1], int(m.sum()), r[0], r[1]))
        pooled.append((zT[m] - np.median(zT[m]), frac[m] - np.nanmedian(frac[m])))
    if pooled:
        a = np.concatenate([p[0] for p in pooled])
        b = np.concatenate([p[1] for p in pooled])
        rr = stats.spearmanr(a, b)
        say("  pooled within-representation: n=%d  rho=%+.3f  p=%.2e" % (len(a), rr[0], rr[1]))

    say("")
    say("=" * 100)
    say("E3  the screen, fit as a monotone relation (fraction recovered vs log z_T)")
    say("=" * 100)
    m = ok & np.isfinite(frac) & (zT > 0)
    lz = np.log(zT[m])
    fr = np.clip(frac[m], -0.5, 1.5)
    say("  n=%d  spearman(log zT, frac)=%.3f (p=%.1e)"
        % (len(lz), stats.spearmanr(lz, fr)[0], stats.spearmanr(lz, fr)[1]))
    # logistic regression of "recovered at least half the gap"
    yb = (fr >= 0.5).astype(float)
    if yb.sum() > 5 and (1 - yb).sum() > 5:
        X = np.column_stack([np.ones(len(lz)), lz])
        b = np.zeros(2)
        for _ in range(200):
            p = 1.0 / (1.0 + np.exp(-X @ b))
            W = np.diag(np.maximum(p * (1 - p), 1e-6))
            b = b + np.linalg.solve(X.T @ W @ X + 1e-6 * np.eye(2), X.T @ (yb - p))
        pred = 1.0 / (1.0 + np.exp(-X @ b))
        auc = stats.spearmanr(pred, yb)[0]
        say("  logistic: P(frac>=0.5) = sigma(%.3f + %.3f log zT) ; rank corr %.3f"
            % (b[0], b[1], auc))
        say("  implied 50%% point: zT = %.3f" % np.exp(-b[0] / b[1]))

    say("")
    say("=" * 100)
    say("E4  the residual is a different quantity: does h explain it?")
    say("=" * 100)
    say("  %-5s %-5s %-12s %-12s" % ("ds", "n", "rho(h,resid)", "rho(h,gap)"))
    for d in dss:
        m = (ds == d)
        if m.sum() < 10:
            continue
        r1 = stats.spearmanr(h[m], resid[m])
        r2 = stats.spearmanr(h[m], gap[m])
        say("  %-5s %-5d %-12.3f %-12.3f   (p=%.1e / %.1e)"
            % (d, int(m.sum()), r1[0], r2[0], r1[1], r2[1]))

    say("")
    say("=" * 100)
    say("E5  subject-level summary (each subject contributes one number per dataset)")
    say("=" * 100)
    say("  %-5s %-12s %-12s %-12s %-8s" % ("ds", "gap", "recover", "frac", "n_sub"))
    for d in dss:
        m = (ds == d)
        subs = sorted(set(subj[m]))
        g = np.array([np.nanmean(gap[m & (subj == s)]) for s in subs])
        r = np.array([np.nanmean(rec[m & (subj == s)]) for s in subs])
        fr = r / np.maximum(g, 1e-9)
        say("  %-5s %-12.4f %-12.4f %-12.3f %-8d"
            % (d, np.mean(g), np.mean(r), np.nanmedian(fr), len(subs)))

    print("done", P)


if __name__ == "__main__":
    main()
