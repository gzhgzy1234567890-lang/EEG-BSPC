# -*- coding: utf-8 -*-
"""v8 experiment B: what is left after a correct centring, and what predicts it?

For each cell we measure the residual gap to the within-session reference and
relate it to four label-free quantities:

    z_T     ||g|| / ||sd_source||          how far the origin sits from the
                                           data centre (source only)
    t       |W g| / sigma_score            the displacement in decision space
    h       |W (class-conditional offset)|  the part of the offset that a
                                           label-free correction cannot remove
                                           (orthogonal to the class-balanced
                                           mean; validated with labels)
    dcov    ||Sigma_T - Sigma_S||_F / ||Sigma_S||_F   geometry change

Output: results/exp2_<tag>.txt
"""
import os
import sys
import time
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

TAG = sys.argv[1] if len(sys.argv) > 1 else "2b,gal"
LOG = []
P = os.path.join(C.OUT, "exp2_%s.txt" % TAG)


def say(s=""):
    LOG.append(str(s))
    with open(P, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")


def rho(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 5 or a[ok].std() == 0 or b[ok].std() == 0:
        return np.nan, np.nan
    r = stats.spearmanr(a[ok], b[ok])
    return r[0], r[1]


def main():
    t0 = time.time()
    dss = tuple(TAG.split(","))
    say("v8 exp B: the residual after centring   datasets=%s  %s"
        % (TAG, time.strftime("%H:%M:%S")))
    rows = []
    for ds in dss:
        pairs = C.all_pairs((ds,))
        if ds == "gal":
            pairs = [p for p in pairs
                     if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
        say("=== %s : %d cells ===" % (ds, len(pairs)))
        for k, p in enumerate(pairs):
            A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
            clf = C.make("lda").fit(A, ya)
            classes = np.asarray(clf.classes_)
            K = len(classes)
            gm = C.class_means(A, ya, classes)
            gt = C.class_means(Bt, yb, classes)
            g = Bt.mean(0) - A.mean(0)
            sdA = np.maximum(A.std(0), 1e-12)
            zT = float(np.linalg.norm(g) / np.linalg.norm(sdA))
            dcov = float(np.linalg.norm(np.cov(Bt, rowvar=False) - np.cov(A, rowvar=False))
                         / max(np.linalg.norm(np.cov(A, rowvar=False)), 1e-12))
            W = C.linear_weights(clf, A.shape[1], K)
            SAl = C.score_matrix(clf, A)
            sdS = np.maximum(SAl.std(0), 1e-12)
            dlt = W @ g
            dlt = dlt - dlt.mean()
            tval = float(np.linalg.norm(dlt / sdS) / np.sqrt(K))
            # class-conditional offset h_k = (m_kB - m_kA) - mean_c(m_cB - m_cA)
            hk = (gt - gm)
            hk = hk - hk.mean(0)
            hproj = W @ hk.T                      # (K classes) x (K scores)
            hnorm = float(np.linalg.norm(hproj) / np.sqrt(K) / np.linalg.norm(sdS) * np.sqrt(K))
            # energy share of the class-conditional part
            hE = float(np.linalg.norm(hk) / max(np.linalg.norm(g), 1e-12))
            ref = C.cv_ref_cached(Bt, yb, ("ref", ds, p["sid_b"]), p["groups_b"])
            src = C.cv_ref_cached(A, ya, ("src", ds, p["sid_a"]))
            ba_none = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt), 1)])
            ba_align = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - g), 1)])
            go, _ = C.balanced_offset_oracle(A, ya, Bt, yb, classes)
            ba_or = C.ba(yb, classes[np.argmax(C.score_matrix(clf, Bt - go), 1)])
            rows.append(dict(ds=ds, rep=p["rep"], subj=p["subj"], pid=p["pid"],
                             zT=zT, t=tval, h=hnorm, hE=hE, dcov=dcov,
                             ref=ref, src=src, none=ba_none, align=ba_align,
                             oracle=ba_or,
                             gap=ref - ba_none, recover=ba_align - ba_none,
                             resid=ref - ba_align))
            if (k + 1) % 100 == 0:
                say("    %d/%d %.0fs" % (k + 1, len(pairs), time.time() - t0))

    say("")
    say("=" * 104)
    say("C1  levels by dataset")
    say("=" * 104)
    say("  %-5s %-5s %-8s %-8s %-8s %-8s %-8s %-8s %-8s"
        % ("ds", "n", "none", "align", "oracle", "ref", "gap", "recov", "resid"))
    for ds in dss:
        q = [r for r in rows if r["ds"] == ds]
        f = lambda k: np.mean([r[k] for r in q])
        say("  %-5s %-5d %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f"
            % (ds, len(q), f("none"), f("align"), f("oracle"), f("ref"),
               f("gap"), f("recover"), f("resid")))

    say("")
    say("=" * 104)
    say("C2  what predicts the gap, the recovery and the residual?  (Spearman over cells)")
    say("=" * 104)
    say("  %-22s %-9s %-9s %-9s %-9s" % ("target", "vs gap", "vs recover", "vs resid", "n"))
    for key in ("zT", "t", "h", "hE", "dcov"):
        out = []
        for tgt in ("gap", "recover", "resid"):
            r, pv = rho([r[key] for r in rows], [r[tgt] for r in rows])
            out.append("%+.3f%s" % (r, "*" if pv < 0.05 else " "))
        say("  %-22s %-9s %-9s %-9s %-9d" % (key, out[0], out[1], out[2], len(rows)))

    say("")
    say("=" * 104)
    say("C3  per-dataset residual vs h")
    say("=" * 104)
    for ds in dss:
        q = [r for r in rows if r["ds"] == ds]
        if len(q) < 10:
            continue
        r1, p1 = rho([r["h"] for r in q], [r["resid"] for r in q])
        r2, p2 = rho([r["h"] for r in q], [r["recover"] for r in q])
        say("  %-5s n=%-4d  h vs resid rho=%+.3f (p=%.2e) | h vs recover rho=%+.3f (p=%.2e)"
            % (ds, len(q), r1, p1, r2, p2))

    say("")
    say("=" * 104)
    say("C4  the recoverable fraction (recover/gap) and the size of the gap")
    say("=" * 104)
    q = [r for r in rows if r["gap"] > 0.02]
    if len(q) > 10:
        fr = np.array([min(r["recover"] / r["gap"], 2.0) for r in q])
        say("  cells with gap>0.02: n=%d  median recovered fraction %.3f  IQR [%.3f, %.3f]"
            % (len(q), np.median(fr), np.percentile(fr, 25), np.percentile(fr, 75)))
        for lo, hi in ((0, 0.5), (0.5, 1.5), (1.5, 100)):
            m = (np.array([r["zT"] for r in q]) >= lo) & (np.array([r["zT"] for r in q]) < hi)
            if m.sum() > 2:
                say("   zT in [%.1f,%.1f): n=%-4d median recovered %.3f"
                    % (lo, hi, int(m.sum()), np.median(fr[m])))

    np.savez(os.path.join(C.OUT, "exp2_%s.npz" % TAG),
             **{k: np.array([r[k] for r in rows], float)
                for k in ("zT", "t", "h", "hE", "dcov", "ref", "src", "none",
                          "align", "oracle", "gap", "recover", "resid")})
    say("")
    say("total %.1f min" % ((time.time() - t0) / 60.0))
    print("done", P)


if __name__ == "__main__":
    main()
