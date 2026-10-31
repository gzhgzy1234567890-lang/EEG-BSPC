# -*- coding: utf-8 -*-
"""C2: decision-stability certificate and flip rate on real BCI-2b data (csp representation)."""
import json, os, sys
import numpy as np
sys.path.insert(0, r'G:\Work_work\math\EEG\paper_v8')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import causal_2b as C
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
root = r'E:\data\BCICIV-2b'
rows = []
for subj in (1, 2, 3):
    fT = os.path.join(root, 'B%02d01T.gdf' % subj)
    fE = os.path.join(root, 'B%02d02T.gdf' % subj)
    if not (os.path.exists(fT) and os.path.exists(fE)):
        continue
    XT, yT = C.load(fT, True)
    XE, yE = C.load(fE, True)
    cT, cE = C.csp_feat(XT, yT, XE, 3)
    clf = LDA(solver='lsqr', shrinkage='auto').fit(cT, yT)
    K = len(clf.classes_)
    S = clf.decision_function(cE)
    SA = clf.decision_function(cT)
    if S.ndim == 1:
        S = np.column_stack([-S, S])
    if SA.ndim == 1:
        SA = np.column_stack([-SA, SA])
    Fm = np.eye(K) - np.ones((K, K)) / K
    n = len(yE)
    blocks = [(a, min(a + 15, n)) for a in range(0, n, 15)]
    flip = []; cert = []; exposure = []; crit = []
    for k, (a, b) in enumerate(blocks):
        if k == 0:
            continue
        d = Fm @ (np.concatenate([S[x:y] for x, y in blocks[:k]]).mean(0) - SA.mean(0))
        for i in range(a, b):
            s = S[i]
            kstar = int(np.argmax(s))
            ratios = [s[kstar] - s[j] - (d[kstar] - d[j]) for j in range(K) if j != kstar]
            margin = min(s[kstar] - s[j] for j in range(K) if j != kstar)
            ratios = np.array(ratios)
            cert.append(bool(np.all(ratios > 0)))
            flip.append(int(np.argmax(s - d)) != kstar)
            exposure.append(float(margin))
            crit.append(float(np.min([(s[kstar] - s[j]) / max(d[kstar] - d[j], 1e-12) for j in range(K) if j != kstar and d[kstar] - d[j] > 0] or [np.inf])))
    cert = np.array(cert); flip = np.array(flip)
    print('subject %d: n=%d  flip rate %.3f  certificate predicts stability %.3f' % (subj, len(flip), flip.mean(), cert.mean()))
    print('   certificate vs observed: agreement %.3f  (cert=1, flip=1 cases: %d)' % (np.mean(cert == ~flip), int(np.sum(cert & flip))))
    print('   median margin %.3f  median critical strength %.3f' % (np.median(exposure), np.median([c for c in crit if np.isfinite(c)])))
    rows.append(dict(subj=subj, n=int(len(flip)), flip=float(flip.mean()), cert=float(cert.mean()), agree=float(np.mean(cert == ~flip)), med_margin=float(np.median(exposure))))
json.dump(rows, open(r'G:\Work_work\math\EEG\paper_v8\results\c2_certificate.json', 'w'), indent=1)
print('C2 done')