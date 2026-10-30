# -*- coding: utf-8 -*-
"""Is the grasp-and-lift trend separable from class composition?

Per series, the cached per-trial labels give the class of every trial; blocks of 15 trials give
the composition of each block. If block composition is a monotone function of block index, then
"temporal drift" and "class composition change" are the same variable in this dataset and no
analysis of these cells can separate them.
"""
import glob
import os
import re

import numpy as np
from scipy import stats

CACHE = r"G:\Work_work\math\EEG\local_analysis\cache_gal"
M = 15


def series_labels():
    out = {}
    for f in sorted(glob.glob(os.path.join(CACHE, "*.npz"))):
        m = re.match(r"(subj\d+)_series(\d+)", os.path.basename(f))
        out[(m.group(1), int(m.group(2)))] = np.load(f)["y"]
    return out


def main():
    labels = series_labels()
    rhos, runs, comps = [], [], []
    for (sub, ser), y in labels.items():
        blocks = [y[i:i + M] for i in range(0, len(y), M) if len(y[i:i + M]) == M]
        comp = np.array([float(b.mean()) for b in blocks])
        comps.append(comp)
        if len(comp) >= 3 and comp.std() > 0:
            rhos.append(stats.spearmanr(np.arange(len(comp)), comp)[0])
        best = cur = 1
        for i in range(1, len(y)):
            cur = cur + 1 if y[i] == y[i - 1] else 1
            best = max(best, cur)
        runs.append(best)

    rhos = np.array(rhos)
    runs = np.array(runs)
    allb = np.concatenate(comps)
    print("series:", len(labels), "| blocks:", len(allb))
    print("single-class blocks: %d of %d (%.0f%%)"
          % (int(((allb == 0) | (allb == 1)).sum()), len(allb),
             100 * ((allb == 0) | (allb == 1)).mean()))
    print("|rho(block index, composition)| median %.2f, min %.2f, share > 0.8 %.2f"
          % (np.median(np.abs(rhos)), np.abs(rhos).min(), (np.abs(rhos) > 0.8).mean()))
    print("longest identical-label run: median %d, max %d" % (np.median(runs), runs.max()))


if __name__ == "__main__":
    main()
