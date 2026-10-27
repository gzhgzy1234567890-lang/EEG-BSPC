# -*- coding: utf-8 -*-
"""v11: SEED-IV held-out test, bound caveat, rigorous z_w, operating points."""
import io
import re

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)
R = []

# ---------- abstract ----------
new_ab = """Removing a session mean is the first step in cross-session EEG decoding, and two operations circulate under that description: centring both sessions, or centring one. We separate three questions. Equivariance: a correction is invariant to the coordinate origin if it translates by a translation-equivariant estimate of the target mean; this family contains more than the sample mean, and we do not claim uniqueness. Score-difference equivalence: two corrections shift every class score by the same amount exactly when their references differ by a vector whose projection onto the centred classifier weights vanishes; for a finite sample that is sufficient but not necessary for identical predictions. Performance: a signed threshold-displacement law predicts the per-cell change of balanced accuracy for mean-calibrated linear classifiers (r = 0.99, MAE 0.013 on the BCI data), and we report where it fails.

On 935 session pairs from six public datasets an origin sweep leaves the equivariant pipelines unchanged by 0.000 and drives the one-sided one to exact chance. A direction-controlled sweep shows that a norm-based statistic is direction-blind; a projected source-only statistic orders the damage across the six datasets (rho = −0.94, exact permutation p = 0.017) and detects a severe loss with AUC 0.84, but does not resolve representations within a dataset, and the transferable operating point fails on two of five held-out datasets. The signed law's bound holds for its predictions but is exceeded by 23 per cent of observed changes, because empirical balanced accuracy moves in steps.
"""
ab_old = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(0)
s = s.replace(ab_old, "## Abstract\n\n" + new_ab + "\n**Keywords")

# ---------- z_w rigorous definition ----------
R.append((
"""Four quantities are used below, and they differ in what they need. The *origin distance* z_T = ‖μ_A‖/‖sd_A‖ uses the source features only and is direction-blind (Section 4.3). The *projected screen* z_w = ‖P W μ_A‖/(√K σ_s) uses the source features and the fitted weights. The *displacement* ρ = ‖P W μ_B‖/(√K σ_s) uses the target features and carries the mechanism, and its signed binary counterpart is s = w'μ_A/σ_s. All three are scale-invariant in the features, since numerator and denominator scale together.""",
"""Four quantities are used below, and they differ in what they need. The *origin distance* z_T = ‖μ_A‖/‖sd_A‖ uses the source features only and is direction-blind (Section 4.3). The *projected screen*

    z_w = ‖ D_σ^{-1} P W μ_A ‖ / √K ,   D_σ = diag(σ_1, …, σ_K),             (2c)

uses the source features and the fitted weights, and the *displacement* ρ is the same expression with μ_B in place of μ_A, i.e. it uses the target features and carries the mechanism; its signed binary counterpart is s = w'μ_A/σ_s.

Equation (2c) is a matrix definition and needs two comments. First, σ_k is the standard deviation of the k-th column of the *source* score matrix S — computed before any centring, which is the convention the code implements and the one we verified. Centring the scores first and then taking the standard deviations gives a different quantity, by as much as 24 in our data (Section 4.10), so the two conventions are not interchangeable; we use the uncentred one throughout and say so. Second, the statistic has the two invariances it is supposed to have: an offset applied to all class scores changes every σ_k not at all and cancels in P W μ_A, and a feature translation in the null space of P W leaves the numerator unchanged, so z_w is invariant to both. We checked both numerically: the largest change over 60 cells is 1.4 × 10⁻¹⁴ for the score offset and 2.5 × 10⁻¹³ for the null-space translation (Section 4.10). The binary reduction is exact: with W = [w'; −w'], P W μ = [w'μ; −w'μ], ‖P W μ‖ = √2|w'μ| and σ_1 = σ_2 = sd(s), so √K = √2 gives z_w = |w'μ_A|/sd(s)."""))

# ---------- dataset table: add SEED-IV ----------
R.append((
"""| NER2015 | 2 | 16 | 80 | 1 | 320 | 0.20 |
| grasp-and-lift | 2 | 12 | 12 | 1 | 336 | 0.25 |""",
"""| NER2015 | 2 | 16 | 80 | 1 | 320 | 0.20 |
| grasp-and-lift | 2 | 12 | 12 | 1 | 336 | 0.25 |
| SEED-IV (held out) | 4 | 15 | 45 | 1 | 90 | 1.00 |"""))

R.append((
"""A *cell* is one (dataset, representation, subject, ordered session pair) combination. There are 36 + 108 + 45 + 320 + 336 = 845 cells, from 61 subject units (9 + 9 + 15 + 16 + 12) and 182 session units (18 + 27 + 45 + 80 + 12).""",
"""*SEED-IV* [19] is used **only as a held-out test**: the statistic, its thresholds and the classifier were fixed in earlier rounds, and SEED-IV was opened after them. It contributes 15 subjects, 4 classes, three sessions and 6 ordered pairs per subject, 90 cells, from the distributed 1 s differential-entropy features (62 channels × 5 bands).

A *cell* is one (dataset, representation, subject, ordered session pair) combination. There are 36 + 108 + 45 + 320 + 336 + 90 = 935 cells, from 76 subject units (9 + 9 + 15 + 16 + 12 + 15) and 227 session units (18 + 27 + 45 + 80 + 12 + 45)."""))

for a, b in R:
    if a not in s:
        print("MISS:", a[:60].replace("\n", " "))
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
print("written", n0, "->", len(s), "| abstract:", len(re.findall(r"[A-Za-z][A-Za-z\-']*", ab)))
