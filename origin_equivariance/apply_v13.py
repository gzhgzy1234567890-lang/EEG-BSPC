# -*- coding: utf-8 -*-
"""v13: remove the meta-language and the duplicate table, restate the law with
both parameterisations, and align the abstract with what survives."""
import io
import re

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)

REPL = [
# title
("# Origin equivariance in cross-session EEG decoding: what mean correction repairs, and an exploratory screen for feature families",
 "# Mean correction in cross-session EEG decoding: equivariance, failure mechanism, and boundaries"),
# abstract
("""Removing a session mean is the first step in cross-session EEG decoding, and two operations circulate under that description: centring both sessions, or centring one. We separate three questions. Equivariance: a correction is invariant to the coordinate origin if it translates by a translation-equivariant estimate of the target mean; this family contains more than the sample mean, and we do not claim uniqueness. Score-difference equivalence: two corrections shift every class score by the same amount exactly when their references differ by a vector whose projection onto the centred classifier weights vanishes; for a finite sample this is sufficient, not necessary, for identical predictions. Performance: a signed threshold-displacement law predicts the per-cell change of balanced accuracy for mean-calibrated linear classifiers (r = 0.99, MAE 0.013 on the BCI data), and we report where it fails.

The main experiments use 845 session pairs from five datasets; 90 further pairs from SEED-IV, opened only after the statistic was fixed, are used for one held-out test. An origin sweep on the 845 leaves the equivariant pipelines unchanged by 0.000 and drives the one-sided one to exact chance. A direction-controlled sweep shows that a norm-based statistic is direction-blind; a projected source-only statistic orders the damage across the six datasets (rho = −0.94, exact p = 0.017) and separates a severe loss with AUC 0.84 on the development cells. It does not survive as an operational rule: the threshold flags every held-out cell (specificity 0.000). We present it as an exploratory screen for feature families, not as a detector of risky sessions.""",
 """Removing a session mean is the first step in cross-session EEG decoding, and two operations circulate under that description: centring both sessions, or centring one. We ask what the choice is, and what it can and cannot buy. Equivariance: a correction is invariant to the coordinate origin if it translates by a translation-equivariant estimate of the target mean; this family contains more than the sample mean, and we do not claim uniqueness. Score-difference equivalence: two corrections shift every class score by the same amount exactly when their references differ by a vector whose projection onto the centred classifier weights vanishes. Performance: the failure of the one-sided form is a threshold displacement, so its sign is set by the threshold error the training session already carries, not by the size of the displacement.

On 845 session pairs from five datasets, an origin sweep leaves the equivariant pipelines unchanged by 0.000 in balanced accuracy and drives the one-sided one to exact chance; 90 further pairs from SEED-IV, opened after all choices were fixed, serve as a held-out test. A Gaussian model of the displacement explains the *sign* of the change for mean-calibrated linear classifiers under one parameterisation but not the magnitude under the parameterisation the model itself requires, and we report both rather than the better one. An exploratory source-only statistic orders the damage across the six datasets (rho = −0.94, exact p = 0.017) and fails as an operational rule (specificity 0.000 on the held-out data). The paper's claim is a mechanism and its boundaries, not a detector and not a predictive law."""),
# remove meta language
("Two comments, because earlier versions of this work got them wrong.", "Two comments."),
("Two caveats, both of which the referee of an earlier version asked for. First,", "Two caveats. First,"),
("The identifiability statement must be made under assumptions, and earlier versions of this work stated it too broadly.", "The identifiability statement must be made under assumptions."),
("The sweep of Section 4.2 injects the origin along one direction. The referee of an earlier version pointed out that this is not enough: §2.3 says the damage is governed by the projection of the origin onto the weights, so an origin orthogonal to the weights should do nothing while raising any norm-based statistic, including z_T. We ran that experiment.",
 "The sweep of Section 4.2 injects the origin along one direction, which is not enough: §2.3 says the damage is governed by the projection of the origin onto the weights, so an origin orthogonal to the weights should do nothing while raising any norm-based statistic. We ran that experiment."),
# equations
("Equation (2b)", "Equation (2)"),
("Equation (2c)", "Equation (2)"),
("of Equation (2b)", "of Equation (2)"),
# table 3 duplicate -> list
("""**Table 3.** What each analysis covers, so that no claim borrows the sample size of another.

| analysis | datasets | cells |
|---|---|---|
| main levels, origin sweep, direction control | five development | 845 |
| signed law, per cell | four development (binary cells) | 800 |
| screening AUC, leave-one-dataset-out operating points | five development | 845 |
| six-dataset association, exact permutation test | five development + SEED-IV | six dataset observations |
| external screening test | five development (threshold) → SEED-IV (test) | 845 → 90 |

A *cell* is one (dataset, representation, subject, ordered session pair) combination.""",
 """The analyses do not all cover the same cells, and no claim borrows the sample size of another: the main levels, the origin sweep and the direction control use the 845 development cells; the per-cell displacement analysis uses the 800 binary cells of the four binary datasets (for BCI-2a, the two-class subproblem of classes 1 and 2, not the four-class problem); the screening analysis uses the 845 development cells and the six dataset observations; and the external test fixes its threshold on the 845 and evaluates on the 90 held-out cells.

A *cell* is one (dataset, representation, subject, ordered session pair) combination."""),
# figure 2 caption: two panels
("""**Fig. 2.** (a) The screen at unit level: origin distance of the source session against the penalty of the one-sided pipeline, one point per dataset-by-representation unit, area proportional to the number of cells; (b) the same relation per cell; (c) the origin distance against the induced displacement, which it proxies.""",
 """**Fig. 2.** (a) Unit medians of the source-only statistic against the penalty of the one-sided pipeline, one point per dataset-by-representation unit, with the held-out SEED-IV point shown as a star; (b) the same relation over the development cells."""),
]

for a, b in REPL:
    if a not in s:
        print("MISS:", a[:60].replace("\n", " "))
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
print("written", n0, "->", len(s), "| abstract:", len(re.findall(r"[A-Za-z][A-Za-z\-']*", ab)))
