# -*- coding: utf-8 -*-
"""Model robustness: feature-space mean correction with LDA, RBF-SVM and a small MLP on sleep-EDF."""
import glob, json, os, re, sys, warnings
import numpy as np
import mne
warnings.filterwarnings('ignore')
mne.set_log_level('ERROR')
sys.path.insert(0, r'G:\Work_work\math\EEG\paper_v8')
import sleep_edf_frozen as F
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import balanced_accuracy_score as bas
OUT = r'G:\Work_work\math\EEG\paper_v8\results\sleep_models2.json'
BLOCK = F.BLOCK


def models():
    return {
        'lda': lambda: LDA(solver='lsqr', shrinkage='auto'),
        'svm': lambda: SVC(kernel='rbf', C=1.0, gamma='scale'),
        'mlp': lambda: MLPClassifier(hidden_layer_sizes=(16,), max_iter=150, random_state=0),
    }


def cell(Fa, ya, Fb, yb):
    out = {}
    sc = StandardScaler().fit(Fa)
    A = sc.transform(Fa); B = sc.transform(Fb)
    muA = A.mean(0)
    for name, make in models().items():
        clf = make().fit(A, ya)
        n = len(yb)
        blocks = [(x, min(x + BLOCK, n)) for x in range(0, n, BLOCK)]
        D = [B[x:y].mean(0) - muA for x, y in blocks]
        Bc = B.copy()
        for k, (x, y) in enumerate(blocks):
            if k > 0:
                Bc[x:y] = B[x:y] - np.mean(D[:k], axis=0)
        p0 = clf.predict(B)
        p1 = clf.predict(Bc)
        out[name] = float(bas(yb[BLOCK:], p1[BLOCK:]) - bas(yb[BLOCK:], p0[BLOCK:]))
    return out


def main():
    psg = sorted(glob.glob(os.path.join(F.ROOT, '*PSG.edf')))
    rows = []
    for f in psg:
        base = os.path.basename(f)
        hypo = os.path.join(F.ROOT, re.sub(r'E\d-PSG\.edf$', 'EC-Hypnogram.edf', base))
        if not os.path.exists(hypo):
            continue
        raw = mne.io.read_raw_edf(f, preload=True, verbose='ERROR')
        ann = mne.read_annotations(hypo)
        sf = raw.info['sfreq']
        y = F.night_labels(ann, int(raw.n_times // int(F.EPOCH * sf)))
        if len(np.unique(y[y >= 0])) < 2:
            continue
        idx = [raw.ch_names.index(c) for c in ('EEG Fpz-Cz', 'EEG Pz-Oz')]
        F_list, y_list = [], []
        for (a, b) in F.contiguous_runs(y):
            for s in range((b - a) // F.SERIES_EPOCHS):
                e0 = a + s * F.SERIES_EPOCHS
                seg = raw.get_data(picks=idx, start=int(e0 * F.EPOCH * sf),
                                   stop=int((e0 + F.SERIES_EPOCHS) * F.EPOCH * sf))
                if seg.shape[1] < int(F.SERIES_EPOCHS * F.EPOCH * sf):
                    continue
                F_list.append(F.series_features(seg, sf))
                y_list.append(y[e0:e0 + F.SERIES_EPOCHS])
        for i in range(len(F_list)):
            for j in range(i + 1, len(F_list)):
                if (i * 7 + j) % 3:
                    continue
                if len(np.unique(y_list[i])) < 2 or len(np.unique(y_list[j])) < 2:
                    continue
                r = cell(F_list[i], y_list[i], F_list[j], y_list[j])
                r['night'] = base; r['subj'] = base[:5]
                rows.append(r)
        print(base, len(rows), flush=True)
        json.dump(rows, open(OUT, 'w'))
    print('cells', len(rows))


if __name__ == '__main__':
    main()