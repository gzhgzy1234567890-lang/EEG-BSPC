# -*- coding: utf-8 -*-
"""v8 checks for statements made in the manuscript.

  c1  dbl == align sample-for-sample, all cells
  c2  train-only accuracy (the second one-sided form)
  c3  median z_T per dataset
  c4  z-score versus none: identical predictions or only identical accuracy?
  c5  the invariant pipelines under the origin sweep: count of cells/settings
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pv8_common as C

OUT = os.path.join(C.OUT, "checks.txt")
L = []


def say(s=""):
    L.append(str(s))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


DS = ("2a", "2b", "seed", "ner", "gal")
say("v8 manuscript checks")
say("")
say("c1/c2/c4  per dataset")
say("  %-5s %-5s %-11s %-11s %-11s %-11s"
    % ("ds", "n", "dbl-diff", "trainonly", "zs-agree", "zs-ba-diff"))
zT = {d: [] for d in DS}
for ds in DS:
    ps = C.all_pairs((ds,))
    if ds == "gal":
        ps = [p for p in ps
              if int(p["meta"]["seq"].split(">")[0]) < int(p["meta"]["seq"].split(">")[1])]
    n = 0
    maxd = 0.0
    to, zs_ag, zs_d, none = [], [], [], []
    for p in ps:
        A, ya, Bt, yb = p["A"], p["ya"], p["B"], p["yb"]
        clf = C.make("lda").fit(A, ya)
        classes = np.asarray(clf.classes_)
        muA, muB = A.mean(0), Bt.mean(0)
        sdA = np.where(A.std(0) < 1e-12, 1.0, A.std(0))
        Pn = classes[np.argmax(C.score_matrix(clf, Bt), 1)]
        Pa = classes[np.argmax(C.score_matrix(clf, Bt - muB + muA), 1)]
        c2 = C.make("lda").fit(A - muA, ya)
        Pd = np.asarray(c2.classes_)[np.argmax(C.score_matrix(c2, Bt - muB), 1)]
        Pt = np.asarray(c2.classes_)[np.argmax(C.score_matrix(c2, Bt), 1)]
        cz = C.make("lda").fit((A - muA) / sdA, ya)
        Pz = np.asarray(cz.classes_)[np.argmax(C.score_matrix(cz, (Bt - muA) / sdA), 1)]
        maxd = max(maxd, float(np.mean(Pa != Pd)))
        to.append(C.ba(yb, Pt))
        zs_ag.append(float(np.mean(Pz == Pn)))
        zs_d.append(C.ba(yb, Pz) - C.ba(yb, Pn))
        none.append(C.ba(yb, Pn))
        zT[ds].append(float(np.linalg.norm(muA) / np.linalg.norm(np.maximum(A.std(0), 1e-12))))
        n += 1
    say("  %-5s %-5d %-11.1e %-11.4f %-11.3f %-11.1e"
        % (ds, n, maxd, np.mean(to), np.mean(zs_ag), np.max(np.abs(zs_d))))
say("")
say("c3  median z_T (cells)")
for d in DS:
    say("  %-5s %.3f" % (d, float(np.median(zT[d]))))
say("")
say("c5  origin sweep: files and settings")
import glob
for f in sorted(glob.glob(os.path.join(C.OUT, "exp4_*.npz"))):
    z = np.load(f)
    say("  %-40s rows=%d settings=%d" % (os.path.basename(f), len(z["a"]),
                                         len(np.unique(z["a"]))))
print("done")
