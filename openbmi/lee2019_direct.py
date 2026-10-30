# -*- coding: utf-8 -*-
"""Lee2019-MI loader bypassing the MOABB paradigm.

Official definitions (MOABB Lee2019.py): events at sample indices t, MI epoch [0, 4] s,
labels left_hand = 2, right_hand = 1, signal scaled by 1e-6 to volts.
"""
import numpy as np
import scipy.io as sio
from scipy.signal import butter, filtfilt

BANDS = ((8, 12), (12, 16), (16, 20), (20, 30))
M = 15
LAMS = (0.0, 0.25, 0.5, 0.75, 1.0)


def load_epochs(path):
    m = sio.loadmat(path, squeeze_me=True, struct_as_record=False)
    tr = m["EEG_MI_train"]
    x = np.asarray(tr.x, float) * 1e-6
    t = np.asarray(tr.t).astype(int).ravel() - 1        # MATLAB 1-based
    y = np.asarray(tr.y_dec).astype(int).ravel()
    fs = float(np.asarray(tr.fs).ravel()[0])
    n = int(4 * fs)
    keep = (t + n) <= x.shape[0]
    X = np.stack([x[t[i]:t[i] + n].T for i in range(len(t)) if keep[i]])
    y = y[keep]
    return X, y, fs


def features(X, fs):
    out = np.zeros((X.shape[0], X.shape[1], len(BANDS)))
    for bi, (lo, hi) in enumerate(BANDS):
        b, a = butter(4, [lo / (fs / 2), hi / (fs / 2)], btype="band")
        F = filtfilt(b, a, X, axis=2)
        out[:, :, bi] = np.log(np.var(F, axis=2) + 1e-30)
    return out.reshape(X.shape[0], -1)


def run(src, tgt, name):
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
    from sklearn.metrics import balanced_accuracy_score as bas
    Xa, ya, fs = load_epochs(src)
    Xb, yb, fs2 = load_epochs(tgt)
    Fa, Fb = features(Xa, fs), features(Xb, fs2)
    clf = LDA(solver="lsqr", shrinkage="auto").fit(Fa, ya)
    K = len(clf.classes_)
    W = clf.coef_ if K > 2 else np.vstack([-clf.coef_, clf.coef_])
    Fm = np.eye(K) - np.ones((K, K)) / K
    muA = Fa.mean(0)
    S = clf.decision_function(Fb)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    n = len(yb)
    blocks = [(a, min(a + M, n)) for a in range(0, n, M)]
    D = [Fm @ (W @ (Fb[a:b].mean(0) - muA)) for a, b in blocks]
    bm = np.zeros((n, K))
    for i, (a, b) in enumerate(blocks):
        if i > 0:
            bm[a:b] = np.mean(D[:i], axis=0)
    res = {}
    for lam in LAMS:
        pred = clf.classes_[np.argmax(S - lam * bm, 1)]
        res[lam] = bas(yb[M:], pred[M:])
    print("source trials", len(ya), "target trials", len(yb), "fs", fs, "features", Fa.shape[1])
    print("classes source", np.unique(ya), "target", np.unique(yb))
    for lam in LAMS:
        print("  block lambda=%.2f  BA=%.4f" % (lam, res[lam]))
    print("  primary (lambda=1 - lambda=0) = %+.4f" % (res[1.0] - res[0.0]))
    return res


if __name__ == "__main__":
    root = r"D:\data\mne_data\MNE-lee2019-mi-data\gigadb\pub\10.5524\100001_101000\100542"
    run(root + r"\session1\s1\sess01_subj01_EEG_MI.mat",
        root + r"\session2\s1\sess02_subj01_EEG_MI.mat", "subj01")
