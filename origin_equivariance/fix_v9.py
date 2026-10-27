# -*- coding: utf-8 -*-
"""v9 fixes: abstract length, Fig. 3 reference, cite [16]."""
import io
import re

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()

new_ab = """Removing a session mean is the first step in cross-session EEG decoding, and two operations circulate under that description: centring both sessions, or centring one. We separate three questions that are often conflated. Equivariance: a correction is invariant to the coordinate origin if it translates by a translation-equivariant estimate of the target mean; this family contains more than the sample mean, and we state the family rather than claiming uniqueness. Prediction equivalence: two corrections return the same predictions, for every input, exactly when their references differ by a vector whose projection onto the centred classifier weights vanishes; for a finite sample the condition is sufficient but not necessary. Performance: no equivariant correction is optimal in general; the damage of the wrong one depends on where the training threshold already sits, and a signed law predicts its sign in 80–97 per cent of cells.

On 845 session pairs from five public datasets (BCI-IV-2a, 2b, SEED, NER2015, grasp-and-lift; 11 dataset-by-representation units) an origin sweep leaves the equivariant pipelines unchanged by 0.000 in balanced accuracy and drives the one-sided one to exact chance. A direction-controlled sweep shows that the source-only statistic we propose is direction-blind: equal-norm origins parallel and orthogonal to the classifier weights give the same statistic and penalties of −0.21 and 0.000. We therefore present it as an empirical proxy: across the five datasets the rank correlation with the damage is −0.80 (p = 0.10), and a cluster bootstrap over datasets puts the unit-level correlation at −0.755 [−1.00, −0.28]. What the correction cannot repair is a change of class priors, confounded with a class-conditional offset unless the label-shift assumption is granted.
"""

ab_old = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(0)
s = s.replace(ab_old, "## Abstract\n\n" + new_ab + "\n**Keywords")

s = s.replace(
    "The gain of `mean` over `none` is +0.0463 on 2a",
    "The gain of `mean` over `none` is +0.0463 on 2a", 1)
# figure 3 reference
s = s.replace(
    "Per subject it is positive in 9 of 9 on 2a",
    "Fig. 3 shows the levels by dataset and the gain per subject. Per subject the gain is positive in 9 of 9 on 2a")
# cite [16]
s = s.replace(
    "Euclidean and Riemannian alignment [5-8] act on second-order structure.",
    "Euclidean and Riemannian alignment [5-8] act on second-order structure, and the Riemannian Gaussian–Laplace framework of [16] is a recent example of the same second-order programme.")

io.open(P, "w", encoding="utf-8").write(s)
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
print("abstract words:", len(re.findall(r"[A-Za-z][A-Za-z\-']*", ab)))
