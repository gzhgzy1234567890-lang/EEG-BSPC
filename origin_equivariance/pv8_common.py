# -*- coding: utf-8 -*-
"""v8 shared layer: pair loaders, decoders, score algebra, estimators.

Design notes (each corresponds to a bug that earlier versions of this project hit):

  * decision_function for binary LDA returns (n,), for K>2 (n, K).  We always
    return an (n, K) score matrix with column k belonging to classes_[k].
  * balanced accuracy is the mean of per-class recalls, never plain accuracy.
  * the within-session reference is cross-validation *inside the target
    session*; it differs from the cross-session number in both session and
    training-set size, so it is a reference and not a ceiling.
  * the offset field is g = mean(B) - mean(A).  It is only ever used through
    W g (the K decision-space displacements) or through its decomposition
    along / orthogonal to the source class-mean axis.
"""
import os
import glob
import re
import sys
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold, StratifiedGroupKFold
from scipy.stats import norm

D = r"G:\Work_work\math\EEG\local_analysis"
if D not in sys.path:
    sys.path.insert(0, D)
import bspc_feat as B  # noqa: E402

OUT = r"G:\Work_work\math\EEG\paper_v8\results"
if not os.path.isdir(OUT):
    os.makedirs(OUT)


# --------------------------------------------------------------------------
# decoders
# --------------------------------------------------------------------------
def make(kind="lda"):
    if kind == "lda":
        return LDA(solver="lsqr", shrinkage="auto")
    if kind == "logit":
        return LogisticRegression(C=1.0, max_iter=4000, solver="lbfgs",
                                  multi_class="auto")
    if kind == "svm":
        return LinearSVC(C=0.01, max_iter=8000, dual=False, tol=1e-3)
    raise ValueError(kind)


def score_matrix(clf, X):
    s = np.asarray(clf.decision_function(X), float)
    if s.ndim == 1:
        return np.column_stack([-s, s])
    if s.shape[1] == 1:
        return np.column_stack([-s[:, 0], s[:, 0]])
    return s


def ba(y, pred, classes=None):
    u = np.unique(y) if classes is None else np.asarray(classes)
    hit = []
    for c in u:
        m = (y == c)
        if m.sum() == 0:
            continue
        hit.append(float((pred[m] == c).mean()))
    return float(np.mean(hit)) if hit else np.nan


_CVCACHE = {}


def cv_ref(X, y, groups=None, kind="lda", n_splits=5):
    """Within-session balanced accuracy of the same classifier family."""
    y = np.asarray(y)
    pred = np.full(len(y), -1)
    if groups is None:
        sk = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=0)
        it = sk.split(X, y)
    else:
        sk = StratifiedGroupKFold(n_splits=n_splits)
        it = sk.split(X, y, groups=groups)
    for a, b in it:
        if len(np.unique(y[a])) < 2:
            pred[b] = y[a][0]
            continue
        clf = make(kind).fit(X[a], y[a])
        pred[b] = clf.predict(X[b])
    return ba(y, pred)


def cv_ref_cached(X, y, key, groups=None, kind="lda", n_splits=5):
    if key in _CVCACHE:
        return _CVCACHE[key]
    v = cv_ref(X, y, groups=groups, kind=kind, n_splits=n_splits)
    _CVCACHE[key] = v
    return v


# --------------------------------------------------------------------------
# pair construction
# --------------------------------------------------------------------------
def pairs_bci(ds, reps=("euc", "euc_ea", "tan", "csp")):
    fn = B.pairs_2a if ds == "2a" else B.pairs_2b
    out = []
    for p in fn():
        if p["rep"] not in reps:
            continue
        meta = {}
        if ds == "2b":
            meta["seq"] = p.get("seq", "")
            meta["gap"] = p.get("gap", np.nan)
        sub = B.subject_of(p["tag"])
        if ds == "2a":
            sid_a, sid_b = "%s:T" % sub, "%s:E" % sub
        else:
            seq = str(p.get("seq", "1>2"))
            sid_a, sid_b = "%s:%s" % (sub, seq.split(">")[0]), "%s:%s" % (sub, seq.split(">")[1])
        out.append(dict(ds=ds, rep=p["rep"], subj=sub, pid=str(p["tag"]),
                        sid_a=sid_a, sid_b=sid_b,
                        A=np.asarray(p["A"], float), ya=np.asarray(p["ya"], int),
                        B=np.asarray(p["B"], float), yb=np.asarray(p["yb"], int),
                        groups_b=None, meta=meta))
    return out


def pairs_seed():
    files = sorted(glob.glob(os.path.join(D, "cache_seed", "*.npz")))
    by = {}
    for f in files:
        m = re.match(r"(\d+)_(\d+)\.npz", os.path.basename(f))
        if not m:
            continue
        by.setdefault(int(m.group(1)), []).append((int(m.group(2)), f))
    out = []
    for sub in sorted(by):
        sess = sorted(by[sub])
        S = {}
        for si, f in sess:
            z = np.load(f, allow_pickle=True)
            S[si] = (z["X"].astype(np.float64), z["y"].astype(int), z["g"].astype(int))
        for i in range(1, len(sess) + 1):
            for j in range(i + 1, len(sess) + 1):
                XA, yA, _ = S[i]
                XB, yB, gB = S[j]
                gA = S[i][2]
                out.append(dict(ds="seed", rep="de", subj="S%02d" % sub,
                                sid_a="S%02d:%d" % (sub, i), sid_b="S%02d:%d" % (sub, j),
                                pid="S%02d:%d>%d" % (sub, i, j),
                                A=XA, ya=yA, B=XB, yb=yB, groups_b=gB, groups_a=gA,
                                meta=dict(seq="%d>%d" % (i, j))))
    return out


def pairs_ner(feature="Ftime"):
    files = sorted(glob.glob(os.path.join(D, "cache_ner_feat", "*.npz")))
    by = {}
    for f in files:
        m = re.match(r"S(\d+)_(\d+)\.npz", os.path.basename(f))
        if not m:
            continue
        by.setdefault(m.group(1), []).append((int(m.group(2)), f))
    out = []
    for sub in sorted(by):
        sess = sorted(by[sub])
        S = {}
        for si, f in sess:
            z = np.load(f, allow_pickle=True)
            S[si] = (np.asarray(z[feature], np.float64), np.asarray(z["y"], int))
        for i in range(1, len(sess) + 1):
            for j in range(1, len(sess) + 1):
                if i == j:
                    continue
                XA, yA = S[i]
                XB, yB = S[j]
                if len(np.unique(yA)) < 2 or len(np.unique(yB)) < 2:
                    continue
                out.append(dict(ds="ner", rep=feature, subj="S" + sub,
                                sid_a="S%s:%d" % (sub, i), sid_b="S%s:%d" % (sub, j),
                                pid="S%s:%d>%d" % (sub, i, j),
                                A=XA, ya=yA, B=XB, yb=yB, groups_b=None,
                                meta=dict(seq="%d>%d" % (i, j), dist=abs(i - j))))
    return out


def pairs_gal():
    """Grasp-and-lift: 12 subjects x 8 series recorded in one session, cap not
    removed -> the same-cap negative control."""
    files = sorted(glob.glob(os.path.join(D, "cache_gal", "*.npz")))
    by = {}
    for f in files:
        m = re.match(r"(subj\d+)_series(\d+)\.npz", os.path.basename(f))
        if not m:
            continue
        by.setdefault(m.group(1), []).append((int(m.group(2)), f))
    out = []
    for sub in sorted(by):
        s = sorted(by[sub])
        S = {}
        for si, f in s:
            z = np.load(f, allow_pickle=True)
            S[si] = (np.asarray(z["F"], np.float64), np.asarray(z["y"], int))
        for i in range(1, len(s) + 1):
            for j in range(1, len(s) + 1):
                if i == j:
                    continue
                XA, yA = S[i]
                XB, yB = S[j]
                if len(np.unique(yA)) < 2 or len(np.unique(yB)) < 2:
                    continue
                out.append(dict(ds="gal", rep="pow", subj=sub,
                                sid_a="%s:%d" % (sub, i), sid_b="%s:%d" % (sub, j),
                                pid="%s:%d>%d" % (sub, i, j),
                                A=XA, ya=yA, B=XB, yb=yB, groups_b=None,
                                meta=dict(seq="%d>%d" % (i, j), dist=abs(i - j))))
    return out


def all_pairs(datasets=("2a", "2b", "seed", "ner", "gal"), reps=None):
    out = []
    for d in datasets:
        if d in ("2a", "2b"):
            out += pairs_bci(d, reps) if reps else pairs_bci(d)
        elif d == "seed":
            out += pairs_seed()
        elif d == "ner":
            out += pairs_ner()
        elif d == "gal":
            out += pairs_gal()
        else:
            raise ValueError(d)
    return out


# --------------------------------------------------------------------------
# geometry of the offset
# --------------------------------------------------------------------------
def class_means(X, y, classes):
    return np.array([X[y == c].mean(0) for c in classes], float)


def pooled_cov(X, y, classes, shrink=1e-3):
    Dd = X.shape[1]
    Cs = []
    for c in classes:
        Z = X[y == c]
        Cs.append(np.cov(Z, rowvar=False))
    C = np.mean(Cs, 0)
    C = np.atleast_2d(C)
    C = (1 - shrink) * C + shrink * (np.trace(C) / Dd) * np.eye(Dd)
    return C


def offset_decomposition(A, ya, Bt, yb, classes):
    mA = class_means(A, ya, classes)
    g = Bt.mean(0) - A.mean(0)
    if len(classes) == 2:
        d = mA[1] - mA[0]
        nd = np.linalg.norm(d)
        d = d / max(nd, 1e-12)
        alpha = float(g @ d)
        alpha_n = alpha / max(nd, 1e-12)
        g_par = alpha * d
        g_ort = g - g_par
    else:
        M = mA - mA.mean(0)
        U, S, Vt = np.linalg.svd(M, full_matrices=False)
        d = Vt[0]
        alpha = float(g @ d)
        alpha_n = alpha
        g_par = alpha * d
        g_ort = g - g_par
    piA = np.array([(ya == c).mean() for c in classes], float)
    piB = np.array([(yb == c).mean() for c in classes], float)
    return dict(g=g, d=d, alpha=alpha, alpha_n=alpha_n, g_par=g_par, g_ort=g_ort,
                mA=mA, piA=piA, piB=piB,
                dpi=float(piB[1] - piA[1]) if len(classes) == 2 else np.nan)


def linear_weights(clf, n_features, n_classes):
    W = np.asarray(clf.coef_, float)
    if W.ndim == 1:
        W = W[None, :]
        if n_classes == 2:
            W = np.vstack([-W, W])
    elif W.shape[0] == 1 and n_classes == 2:
        W = np.vstack([-W, W])
    if W.shape[0] != n_classes and W.shape[0] == n_classes - 1:
        W = np.vstack([W, np.zeros((1, W.shape[1]))])
    return W


# --------------------------------------------------------------------------
# estimators of the correction
# --------------------------------------------------------------------------
def plain_centre(A, ya, Bt, classes):
    return Bt.mean(0) - A.mean(0), dict(pi=None)


def balanced_offset_oracle(A, ya, Bt, yb, classes):
    mA = class_means(A, ya, classes)
    mB = class_means(Bt, yb, classes)
    return (mB - mA).mean(0), dict(pi=np.array([(yb == c).mean() for c in classes]))


def cgm_recentre(A, ya, Bt, classes, n_iter=60, tol=1e-6, shrink=1e-3,
                 verbose=False):
    """Constrained Gaussian-mixture recentring (labelled source, unlabelled
    target): x ~ sum_k pi_k N(m_k + gamma, Sigma) with m_k, Sigma from the
    source.  Plain centring is the special case pi = pi_source."""
    mA = class_means(A, ya, classes)
    Cm = pooled_cov(A, ya, classes, shrink)
    piA = np.array([(ya == c).mean() for c in classes], float)
    muB = Bt.mean(0)
    w, V = np.linalg.eigh(Cm)
    w = np.maximum(w, 1e-10)
    Wh = V @ np.diag(w ** -0.5) @ V.T
    Bw = Bt @ Wh.T
    mw = mA @ Wh.T
    const = -0.5 * Bt.shape[1] * np.log(2 * np.pi) - 0.5 * np.sum(np.log(w))
    pi = piA.copy()
    gamma = muB - (pi[:, None] * mA).sum(0)
    prev = -np.inf
    ll = np.nan
    it = 0
    for it in range(n_iter):
        m = mw + (gamma @ Wh.T)[None, :]
        d2 = ((Bw[:, None, :] - m[None, :, :]) ** 2).sum(2)
        logp = -0.5 * d2 + const + np.log(np.maximum(pi, 1e-12))[None, :]
        mx = logp.max(1, keepdims=True)
        lse = mx[:, 0] + np.log(np.exp(logp - mx).sum(1))
        ll = float(lse.mean())
        r = np.exp(logp - lse[:, None])
        pi = r.mean(0)
        gamma = muB - (pi[:, None] * mA).sum(0)
        if abs(ll - prev) < tol:
            break
        prev = ll
    if verbose:
        print("    cgm it=%d ll=%.4f pi=%s" % (it, ll, np.round(pi, 3)))
    return gamma, dict(pi=pi, ll=ll, it=it)


# --------------------------------------------------------------------------
# predictions
# --------------------------------------------------------------------------
def damage_law(c, t):
    """Damage of a residual displacement t (within-class SD units) for a
    two-class decoder whose aligned accuracy is Phi(c)."""
    return float(norm.cdf(c) - 0.5 * (norm.cdf(c - t) + norm.cdf(c + t)))


def predict_ba(ba_ref, t):
    c = norm.ppf(np.clip(ba_ref, 1e-3, 1 - 1e-3))
    return float(0.5 * (norm.cdf(c - t) + norm.cdf(c + t)))
