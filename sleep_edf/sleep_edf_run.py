# -*- coding: utf-8 -*-
"""Run the frozen sleep-EDF protocol over all nights and aggregate at the subject level."""
import json
import os
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mne
import re
import glob
import sleep_edf_test as S

mne.set_log_level("ERROR")


def run_all():
    psg = sorted(glob.glob(os.path.join(S.ROOT, "*PSG.edf")))
    rows = []
    for f in psg:
        base = os.path.basename(f)
        hypo = os.path.join(S.ROOT, re.sub(r"E\d-PSG\.edf$", "EC-Hypnogram.edf", base))
        if not os.path.exists(hypo):
            continue
        try:
            raw = mne.io.read_raw_edf(f, preload=True, verbose="ERROR")
            ann = mne.read_annotations(hypo)
            F, y = S.feats_epochs(raw, ann)
            cells = S.analyse(F, y)
            for c in cells:
                c["night"] = base
                c["subj"] = base[:6]
            rows += cells
            print(base, len(cells), flush=True)
        except Exception as exc:
            print(base, "FAILED", repr(exc)[:100], flush=True)
    json.dump(rows, open(S.OUT, "w"), indent=1)
    return rows


def summarise(rows):
    from scipy import stats
    per_subj = {}
    for r in rows:
        # sleep-EDF file names are SC4<subject><recording>E0-PSG.edf: the subject is the first
        # five characters (SC4xx) and the sixth is the recording index, so 13 subjects with two
        # recordings collapse correctly to 32 units. A four-character key collapses ten subjects
        # into one and is wrong.
        per_subj.setdefault(r["subj"][:5], []).append(r["delta"])
    subj_means = {k: float(np.mean(v)) for k, v in per_subj.items()}
    d = np.array(list(subj_means.values()))
    pos, neg = int((d > 0).sum()), int((d < 0).sum())
    p = stats.binomtest(pos, pos + neg, 0.5).pvalue if pos + neg else 1.0
    rng = np.random.default_rng(20261030)
    boot = [rng.choice(d, len(d), replace=True).mean() for _ in range(10000)]
    lo, hi = np.percentile(boot, [2.5, 97.5])
    print("\nsubjects:", len(d), "cells:", len(rows))
    print("mean subject delta %+.4f, median %+.4f" % (d.mean(), np.median(d)))
    print("bootstrap 95%% interval [%+.4f, %+.4f]" % (lo, hi))
    print("sign test: %d negative / %d positive, p = %.5f" % (neg, pos, p))
    print("subject values:", {k: round(v, 3) for k, v in sorted(subj_means.items())})


if __name__ == "__main__":
    rows = run_all()
    summarise(rows)
