# -*- coding: utf-8 -*-
"""v12: external threshold test on the held-out dataset, scope accounting,
one unambiguous z_w definition, repositioning of the screen."""
import io
import re

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)

T1 = "# Origin equivariance in cross-session EEG decoding: what mean correction repairs, when it fails, and how to detect the failure"
T2 = "# Origin equivariance in cross-session EEG decoding: what mean correction repairs, and an exploratory screen for feature families"

A1 = "On 935 session pairs from six public datasets an origin sweep leaves the equivariant pipelines unchanged by 0.000 and drives the one-sided one to exact chance."
A2 = "The main experiments use 845 session pairs from five datasets; a further 90 pairs from SEED-IV, opened only after the statistic was fixed, are used for a held-out test and for nothing else. On the 845, an origin sweep leaves the equivariant pipelines unchanged by 0.000 and drives the one-sided one to exact chance."

B1 = "and detects a severe loss with AUC 0.84, but does not resolve representations within a dataset, and the transferable operating point fails on two of five held-out datasets."
B2 = "and detects a severe loss with AUC 0.84 on the development cells. It does not survive as an operational rule: a threshold fixed on the five datasets flags every cell of the held-out dataset (specificity 0.000), cannot resolve the representations of one development dataset, and fails on two of five leave-one-dataset-out folds. We therefore present it as an exploratory screen for feature families, not as a detector of risky sessions."

C1 = "    z_w = ‖ D_σ⁻¹ P W μ_A ‖ / √K ,   D_σ = diag(σ_1, …, σ_K),             (2c)"
C2 = "    z_w = ‖ D_σ⁻¹ P W μ_A ‖ / √K ,   D_σ = diag(σ_1, …, σ_K),             (2)"

D1 = "Equation (2c) is a matrix definition and needs two comments."
D2 = "Equation (2) is the definition; the scalar form |w'μ_A|/σ_s used later is its binary special case, valid when K = 2 or when all σ_k are equal, and it is not used elsewhere. The definition needs three comments."

E1 = "Second, the statistic has the two invariances it is supposed to have: an offset applied to all class scores changes every σ_k not at all and cancels in P W μ_A, and a feature translation in the null space of P W leaves the numerator unchanged, so z_w is invariant to both. We checked both numerically: the largest change over 60 cells is 1.4 × 10⁻¹⁴ for the score offset and 2.5 × 10⁻¹³ for the null-space translation (Section 4.10). The binary reduction is exact:"
E2 = "Second, the statistic has the invariances it is supposed to have and *not* the one it is not: an offset applied to all class scores changes no σ_k and cancels in P W μ_A, and a feature translation in the null space of P W leaves the numerator unchanged, so z_w is insensitive to decision-null translations; it is *not* invariant to a translation along the discriminating directions, which is the point of the statistic. We checked both numerically: the largest change over 60 cells is 1.4 × 10⁻¹⁴ for the score offset and 2.5 × 10⁻¹³ for the null-space translation (Section 4.10). The binary reduction is exact:"

F1 = "A *cell* is one (dataset, representation, subject, ordered session pair) combination."
F2 = """**Table 3.** What each analysis covers, so that no claim borrows the sample size of another.

| analysis | datasets | cells |
|---|---|---|
| main levels, origin sweep, direction control | five development | 845 |
| signed law, per cell | four development (binary cells) | 800 |
| screening AUC, leave-one-dataset-out operating points | five development | 845 |
| six-dataset association, exact permutation test | five development + SEED-IV | six dataset observations |
| external screening test | five development (threshold) → SEED-IV (test) | 845 → 90 |

A *cell* is one (dataset, representation, subject, ordered session pair) combination."""

G1 = "The transferable operating point works on three of the five held-out datasets and fails on two: on SEED it flags everything (specificity 0.000), and on NER2015 it misses most of the severe cases (sensitivity 0.273, precision 0.188). A laboratory that used this rule would therefore be roughly right on three datasets and wrong on two, which is not yet a screening instrument."
G2 = """The transferable operating point works on three of the five held-out datasets and fails on two: on SEED it flags everything (specificity 0.000), and on NER2015 it misses most of the severe cases (sensitivity 0.273, precision 0.188).

**The held-out test.** Fixing the threshold on *all five* development datasets by Youden's J gives t = 0.354, with sensitivity 0.811, specificity 0.749 and precision 0.544 on the development cells it was chosen on. Applied unchanged to SEED-IV it gives sensitivity 1.000, specificity 0.000, precision 0.544 and accuracy 0.544: every one of the 90 cells is flagged, because SEED-IV's z_w sits at 1.00 and the threshold is 0.354. The dataset-level prediction is therefore right — SEED-IV is an exposed feature family, and its median penalty of −0.070 says so — while the cell-level rule has no specificity at all. That is the clearest statement of what the statistic does and does not do."""

H1 = "**Step 1 — project the source mean onto the classifier's direction.**"
H2 = "**Step 1 (exploratory) — project the source mean onto the classifier's direction.**"

I1 = "These are descriptive operating characteristics of the eleven units studied, not validated thresholds: use the statistic to triage a feature family, not to certify that a particular representation is safe"
I2 = "These are descriptive operating characteristics of the twelve units studied, not validated thresholds, and the held-out test of Section 4.4 shows that a threshold fixed this way does not transfer to cells: use the statistic to say whether a *feature family* is likely to be exposed, and not to certify that a particular representation, session or subject is safe"

J1 = "Three kinds of statement are mixed in a paper of this shape,"
J2 = """The paper's claim is about a *mechanism* and an *exploratory* screen, and it is worth saying so in one place because the title of an earlier version promised a detector. What we can say is: a first-order correction has a unique effect on score differences; its absence or misapplication displaces the decision function by an amount that is computable and whose sign is predictable for mean-calibrated linear classifiers; and the exposure of a feature family can be ranked before any target label. What we cannot say, and do not, is that a threshold on the resulting statistic decides whether a given session will fail — the held-out test in Section 4.4 shows the opposite.

Three kinds of statement are mixed in a paper of this shape,"""

for a, b in [(T1, T2), (A1, A2), (B1, B2), (C1, C2), (D1, D2), (E1, E2), (F1, F2), (G1, G2), (H1, H2), (I1, I2), (J1, J2)]:
    if a not in s:
        print("MISS:", a[:60])
    s = s.replace(a, b, 1)

io.open(P, "w", encoding="utf-8").write(s)
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
print("written", n0, "->", len(s), "| abstract:", len(re.findall(r"[A-Za-z][A-Za-z\-']*", ab)))
