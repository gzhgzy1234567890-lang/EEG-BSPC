# -*- coding: utf-8 -*-
"""v14: the corrected statistic, the removed screening claim, and the numbers."""
import io
import re

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v9.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)

NEW_AB = """Removing a session mean is the first step in cross-session EEG decoding, and two operations circulate under that description: centring both sessions, or centring one. We ask what the choice is and what it can buy. Equivariance: a correction is invariant to the coordinate origin if it translates by a translation-equivariant estimate of the target mean; this family contains more than the sample mean, and we do not claim uniqueness. Score-difference equivalence: two corrections shift every class score by the same amount exactly when their references differ by a vector whose projection onto the centred classifier weights vanishes. Performance: the failure of the one-sided form is a threshold displacement, so its sign is set by the threshold error the training session already carries.

On 845 cells from five datasets an origin sweep leaves the equivariant pipelines unchanged by 0.000 in balanced accuracy and drives the one-sided one to exact chance; 90 further cells from SEED-IV, opened after all choices were fixed, serve as a held-out test. A Gaussian model of the displacement explains the sign of the change for mean-calibrated linear classifiers under one parameterisation but not the magnitude under the parameterisation the model itself requires; we report both. A source-only statistic of the exposure of a feature family is defined so that it is invariant to decision-equivalent score representations, and with that definition its cross-dataset association (rho = −0.77, exact p = 0.10) and its held-out operating point (specificity 0.000) do not support it as a screening tool. We therefore report it as an exploratory analysis and not as a contribution. What the paper claims is a mechanism and its boundaries."""

ab_old = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.OCR if False else re.S)
ab_old = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(0)
s = s.replace(ab_old, "## Abstract\n\n" + NEW_AB + "\n**Keywords")

# --- z_w definition: centred scale, referee counter-example, invariance
old_def = """Equation (2) is the definition; the scalar form |w'μ_A|/σ_s used later is its binary special case, valid when K = 2 or when all σ_k are equal, and it is not used elsewhere. The definition needs three comments."""
new_def = """Equation (2) is the definition, and it needs four comments. The scalar form |w'μ_A|/σ_s used later is its binary special case, valid when K = 2 or when all σ_k are equal.

*The scale must come from the centred scores.* The first version of this analysis took σ_k from the raw score columns, and a referee's counter-example shows why that is wrong: adding a class-common linear term a'x to every score leaves all predictions unchanged but changes the per-class raw score spreads, so z_w could be inflated by 49 per cent without any change of classifier (W = [1; −1] with a'x = 0.5x gives W' = [1.5; −0.5] and the same score difference 2x). With σ_k taken from the columns of P S — the centred scores — both the numerator and the scale are invariant, because P(W + 1a') = PW and P(S + a'x) = P S. We verified the invariance numerically under that transformation: |Δz_w| = 4.4 × 10⁻¹⁶ (Section 4.10). Every number in Section 4.4 uses this definition."""
if old_def not in s:
    print("MISS def")
s = s.replace(old_def, new_def)

old_inv = """**The two invariances of z_w.** We verified both numerically over 60 cells spanning three datasets: an offset added to every class score changes z_w by at most 1.4 × 10⁻¹⁴, and a feature translation in the null space of P W changes it by at most 2.5 × 10⁻¹³. The choice of scale convention matters: taking the standard deviations of the *centred* scores instead of the uncentred ones changes z_w by as much as 24, so Equation (2) must be read with the uncentred convention, which is what the code implements."""
new_inv = """**The invariances of z_w, and the convention that matters.** With the scale taken from the centred scores, z_w is invariant to (i) adding a class-common linear term to all scores, (ii) adding a constant to all scores, and (iii) translating the features in the null space of P W. We verified (i) to 4.4 × 10⁻¹⁶, and (ii) and (iii) to 1.4 × 10⁻¹⁴ and 2.5 × 10⁻¹³ over 60 cells. Taking the scale from the *uncentred* scores instead — the convention of the first version — breaks (i) and can change z_w by a factor of 1.5 on a decision-equivalent classifier, which is why the definition was corrected."""
if old_inv not in s:
    print("MISS inv")
s = s.replace(old_inv, new_inv)

# --- 4.4: corrected numbers and the negative conclusion
start = s.find("*Dataset level (n = 6, including the held-out dataset).*")
end = s.find("### 4.5")
if start < 0 or end < 0:
    print("MISS 4.4 block")
else:
    new44 = """*Dataset level.* With the corrected definition the five development datasets give a rank correlation of −0.80, and adding SEED-IV (median z_w = 24.4, median penalty −0.070) does not improve it: the six-dataset value is −0.77, and the exact permutation test gives 74 of 720 orderings at least as extreme, p = 0.103. The earlier six-dataset value of −0.94 and p = 0.017 were computed with the uncentred scale, which the referee's counter-example shows is not a function of the decision function; they do not survive the correction.

*Cell level.* Within the 845 development cells the statistic separates a severe loss with an AUC of 0.841, and at the level of the eleven development units the rank correlation is −0.83. Both are between-family effects: within SEED-IV the AUC is 0.515, within BCI-2a the four representations have nearly the same statistic and penalties from +0.024 to −0.184, and the leave-one-dataset-out operating point fails on SEED and NER2015 (Table 6).

*The held-out operating point.* A threshold of 0.354 fixed on the five development datasets gives, on SEED-IV, sensitivity 1.000, specificity 0.000, precision 0.544: every cell is flagged. The dataset-level prediction is right — SEED-IV is an exposed feature family — and the cell-level rule is useless.

We therefore do not present the statistic as a screening tool. It is reported because it is the natural source-only quantity, because its failures are informative about what a source-only analysis can and cannot see, and because a reader who is tempted to build such a screen should know the three ways in which ours failed.

"""
    s = s[:start] + new44 + s[end:]

# --- conclusion paragraph on the screen
s = s.replace("""Empirically, an origin sweep on 845 session pairs from five datasets leaves the equivariant pipelines unchanged by 0.000 and drives the one-sided one to exact chance; an equal-norm direction control shows that a norm-based statistic is blind to the direction of the origin and that only the component along the weights damages the decoder; and a projected source-only statistic orders the damage across the five datasets (rho = −0.90, exact p = 0.083) and separates a severe loss with an AUC of 0.84, while failing to resolve the four representations of one dataset and inverting within another.""",
"""Empirically, an origin sweep on 845 cells from five datasets leaves the equivariant pipelines unchanged by 0.000 and drives the one-sided one to exact chance; an equal-norm direction control shows that a norm-based statistic is blind to the direction of the origin and that only the component along the weights damages the decoder. A source-only statistic that is invariant to decision-equivalent score representations orders the damage between feature families (AUC 0.84 within the development cells) but not across them once the held-out dataset is included (rho = −0.77, exact p = 0.10), and its operational threshold has no specificity on the held-out data. We report it as an exploratory analysis and draw no screening recommendation from it.""")

io.open(P, "w", encoding="utf-8").write(s)
ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
print("written", n0, "->", len(s), "| abstract:", len(re.findall(r"[A-Za-z][A-Za-z\-']*", ab)))
