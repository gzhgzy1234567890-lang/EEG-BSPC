# -*- coding: utf-8 -*-
"""Secondary analysis on Lee2019-MI: four estimators x five strengths, 54 subjects.

Same loader, features, classifier and warm-up as the primary endpoint; only the estimator of
the target mean varies. Everything is past-only across trials.
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

ROOT = r"D:\data\mne_data\MNE-lee2019-mi-data\gigadb\pub\10.5524\100001_101000\100542"
OUT = os.path.join(HERE, "results", "lee2019_secondary.json")
M = 15
LAMS = (0.0, 0.25, 0.5, 0.75, 1.0)
SUBJECTS = list(range(1, 55))


def path_of(s, k):
    return os.path.join(ROOT, "session%d" % k, "s%d" % s, "sess0%d_subj%02d_EEG_MI.mat" % (k, s))


def estimates(D, n):
    """Return a dict estimator -> array (n, K) of past-only estimates."""
    out = {}
    K = D.shape[1]
    cum = np.zeros((n, K))
    win = np.zeros((n, K))
    expo = np.zeros((n, K))
    blk = np.zeros((n, K))
    run_sum = np.zeros(K)
    e = np.zeros(K)
    alpha = 0.05
    for t in range(n):
        cum[t] = run_sum / t if t > 0 else 0.0
        lo = max(0, t - 50)
        win[t] = D[lo:t].mean(0) if t > 0 else 0.0
        expo[t] = e
        blocks = [(a, min(a + M, t)) for a in range(0, t, M) if min(a + M, t) > a]
        done = [(a, b) for a, b in blocks if b - a == M]
        blk[t] = np.mean([D[a:b].mean(0) for a, b in done], axis=0) if done else np.zeros(K)
        run_sum = run_sum + D[t]
        e = (1 - alpha) * e + alpha * D[t]
    out["cumulative"] = cum
    out["window50"] = win
    out["exponential"] = expo
    out["block"] = blk
    return out


def evaluate(subject):
    import lee2019_direct as L
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
    from sklearn.metrics import balanced_accuracy_score as bas
    try:
        Xa, ya, fs = L.load_epochs(path_of(subject, 1))
        Xb, yb, _ = L.load_epochs(path_of(subject, 2))
        Fa, Fb = L.features(Xa, fs), L.features(Xb, fs)
        clf = LDA(solver="lsqr", shrinkage="auto").fit(Fa, ya)
        K = len(clf.classes_)
        W = clf.coef_ if K > 2 else np.vstack([-clf.coef_, clf.coef_])
        Fm = np.eye(K) - np.ones((K, K)) / K
        muA = Fa.mean(0)
        S = clf.decision_function(Fb)
        if S.ndim == 1:
            S = np.column_stack([-S, S])
        D = np.stack([Fm @ (W @ (Fb[i] - muA)) for i in range(len(yb))])
        est = estimates(D, len(yb))
        res = {}
        for name, E in est.items():
            for lam in LAMS:
                pred = clf.classes_[np.argmax(S - lam * E, 1)]
                res["%s|%.2f" % (name, lam)] = float(bas(yb[M:], pred[M:]))
        return {"subject": subject, "ba": res}
    except Exception as exc:
        return {"subject": subject, "error": repr(exc)[:160]}


def main():
    rows = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(evaluate, SUBJECTS):
            rows.append(r)
            print("subject", r["subject"], "ok" if "ba" in r else r.get("error", ""), flush=True)
            json.dump({"rows": rows}, open(OUT, "w"), indent=1)
    ok = [r for r in rows if "ba" in r]
    keys = [k for k in ok[0]["ba"]]
    print("\n%-16s %8s %8s %8s" % ("estimator|lambda", "meanBA", "dBA", "neg"))
    base = {}
    for k in keys:
        if k.endswith("|0.00"):
            base[k.split("|")[0]] = np.array([r["ba"][k] for r in ok]).mean()
    for k in keys:
        v = np.array([r["ba"][k] for r in ok])
        name = k.split("|")[0]
        d = v.mean() - base[name]
        print("%-16s %8.4f %+8.4f %8d" % (k, v.mean(), d, int((v - base[name] < 0).sum())))
    print("n subjects", len(ok))


if __name__ == "__main__":
    main()
