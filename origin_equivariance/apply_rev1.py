# -*- coding: utf-8 -*-
"""Apply the internal-referee fixes to BSPC_draft_v8.md."""
import io

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v8.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)

REPL = [
# ---- abstract: statistics and framing
("and the source-only statistic orders the damage across units (Spearman −0.76, p = 0.007) and cells (−0.38, p = 10⁻³⁰).",
 "and the source-only statistic orders the damage across the eleven feature units (Spearman −0.76, permutation p = 0.009); the cell-level association (−0.38) is reported descriptively, because cells within a unit are not independent."),
("The benefit of the correction over doing nothing is not screenable at unit level, and we report that as a negative result.",
 "The benefit of the correction over doing nothing is not ordered by the same statistic, and we report that as a negative result rather than a screen."),
# ---- 4.3 statistics
("Across the eleven units the rank correlation between z_T and the penalty is −0.755 (p = 0.007), and across the 845 cells it is −0.382 (p = 1.0 × 10⁻³⁰).",
 "Across the eleven units the rank correlation between z_T and the penalty is −0.755 (permutation over units, p = 0.009); across the 845 cells it is −0.382, which we report descriptively because cells within a unit are not independent."),
("The feature-level statistic is a proxy for the decision-level one: z_T and ρ are correlated at +0.718 across units (p = 0.013) and +0.525 across cells (p = 4.2 × 10⁻⁶¹).",
 "The feature-level statistic is a proxy for the decision-level one: z_T and ρ are correlated at +0.718 across units (p = 0.013) and +0.525 across cells (descriptive)."),
# ---- 4.4 second exposed dataset
("Across the fourteen BCI-2b settings the rank correlation between ρ and the damage is −0.78 (p = 1.0 × 10⁻³), and the sign reverses exactly where ρ falls below about 1:",
 "The same sweep on a second exposed dataset, BCI-2a restricted to the two motor-imagery classes and the log-power representation (nine cells, thirteen settings), gives a rank correlation of −0.654 (p = 0.015) between ρ and the damage, with the same sign reversal: the LDA and logistic settings, at ρ between 1.5 and 6.6, lose 0.10 to 0.12, and the SVM settings, at ρ between 0.33 and 1.10, lose at most 0.038 and gain up to 0.010.\n\nAcross the fourteen BCI-2b settings the rank correlation between ρ and the damage is −0.78 (p = 1.0 × 10⁻³), and the sign reverses exactly where ρ falls below about 1:"),
("| NER2015 | SVM | C = 0.01 | 0.5787 | 0.5850 | +0.0063 | 0.37 |",
 "| NER2015 | SVM | C = 0.01 | 0.5787 | 0.5850 | +0.0063 | 0.37 |\n| BCI-2a (1 vs 2) | LDA | auto | 0.6759 | 0.5679 | −0.1080 | 2.27 |\n| BCI-2a (1 vs 2) | SVM | C = 0.01 | 0.6427 | 0.6373 | −0.0054 | 0.33 |\n| BCI-2a (1 vs 2) | SVM | C = 10 | 0.6574 | 0.6196 | −0.0378 | 1.10 |"),
# ---- 4.5 composition with alignment
("The last column is the empirical form of Section 2.4:",
 "**The correction composes with second-order alignment.** The representations that already use a second-order correction are the natural test of whether the first-order correction is redundant after alignment. It is not. Within the Euclidean-aligned representation the mean correction still gains +0.0725 on BCI-2a and +0.0236 on BCI-2b; within the Riemannian tangent representation +0.0417 and +0.0452; within CSP +0.0575 and +0.0384; and within plain log power +0.0135 and +0.0245. The two corrections act on different moments and are not substitutes: alignment does not remove an origin offset, and centring does not remove a covariance change.\n\nThe last column is the empirical form of Section 2.4:"),
# ---- 4.8 shorten
("""After the correction a residual gap to the within-session reference remains: 0.0198 on BCI-2b, 0.0770 on SEED, 0.0257 on NER2015 and 0.0294 on grasp-and-lift. It is not an origin effect. Across all 845 cells the correlation between z_T and the residual is +0.06, and within datasets it has no consistent sign (BCI-2a −0.55, BCI-2b −0.37, SEED +0.41, NER2015 +0.11, grasp-and-lift +0.27).""",
 """After the correction a residual gap to the within-session reference remains: 0.0198 on BCI-2b, 0.0770 on SEED, 0.0257 on NER2015 and 0.0294 on grasp-and-lift. It is not an origin effect: across all 845 cells the correlation between z_T and the residual is +0.06, and within datasets it has no consistent sign (BCI-2a −0.55, BCI-2b −0.37, SEED +0.41, NER2015 +0.11, grasp-and-lift +0.27). We therefore report it as a bound rather than as a second mechanism, and do not use it to support any claim in the abstract."""),
("""The residual is weakly associated with the class-conditional offset h_k of Section 2.4, measured as the component of the class-conditional mean shift orthogonal to the class-balanced mean, in units of the score spread: +0.21 on BCI-2a, −0.36 on BCI-2b, +0.33 on SEED, +0.30 on NER2015 and +0.55 on grasp-and-lift, pooled +0.26. Four of five datasets agree in sign; BCI-2b does not, and we do not have an account of why. A change of the within-session covariance explains less (pooled +0.10) and inconsistently.

The honest summary is that the correction removes what it can identify, that what it cannot identify is the class-conditional part, and that our measurement of that part is a weak and partly inconsistent predictor of the residual. We report it as the boundary of the account rather than as its confirmation.""",
 """The residual is weakly associated with the class-conditional offset h_k of Section 2.4, measured as the component of the class-conditional mean shift orthogonal to the class-balanced mean, in units of the score spread: +0.21 on BCI-2a, −0.36 on BCI-2b, +0.33 on SEED, +0.30 on NER2015 and +0.55 on grasp-and-lift (pooled +0.26, four of five datasets in the same direction). A change of the within-session covariance explains less (pooled +0.10) and inconsistently. The correction removes what it can identify; what it cannot identify is the class-conditional part, and our measurement of that part is a weak and partly inconsistent predictor of the residual. We report it as the boundary of the account rather than as its confirmation."""),
# ---- references used
("Where the two intersect is the label-shift problem",
 "Riemannian geometry supplies the natural language for the second-order statement of the same question [16], and the linear classifier families we sweep are the standard ones for BCI [17]. Where the two intersect is the label-shift problem"),
# ---- data availability placeholder
("archived at [repository URL], pinned to this manuscript.",
 "archived at the repository associated with this manuscript, with a commit hash pinned to the reported numbers."),
]

for a, b in REPL:
    if a not in s:
        print("MISS:", a[:70].replace("\n", " "))
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
print("written", n0, "->", len(s))
