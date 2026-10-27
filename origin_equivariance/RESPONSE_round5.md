# Response to the second-round report (Major Revision)

Manuscript: v10 (`BSPC_draft_v9.md`, `BSPC_Manuscript_v10_with_figs.docx`).

The two items the report identified as potentially decisive were both genuine
errors of the previous draft, and we fixed them rather than qualified them: the
signed law had never been checked cell by cell, and the binary reduction of
`z_w` in the text did not match its own definition. The first now has a per-cell
validation and a figure; the second is corrected, derived, and verified against
the code. The dataset-level p-value is replaced by the exact permutation value.
A third finding is less comfortable and we state it as it is: once the sign
accuracy is compared with the majority-class rate, most of the "80–97 per cent"
figure is the majority class, and the real evidence for the law is its
quantitative per-cell accuracy and its sign-discrimination AUC.

---

## MC1 — the signed law had no per-cell validation (Critical)

**Fixed, and the test changes how the law is described.**

*Per-cell check.* For every cell we now compute the predicted change with
Equation (4) and compare it with the observed change **on the same cell**: 2,400
cells over four datasets and three classifiers. The pooled mean absolute error
is 0.028 and the correlation is 0.825. For LDA on BCI-2b the per-cell
correlation is 0.989 with MAE 0.013; for logistic regression on BCI-2b, 0.990
and 0.013. The analytic bound |Δ| ≤ 0.1995|s| holds in 100 per cent of cells, as
it must by construction — the apparent contradiction between the median
displacement and the median damage came from comparing medians of different
quantities, which the new table makes impossible. Fig. 4 is the scatter the
report asked for, with the identity line and the error distribution.

*Where it fails.* The law degrades to a sign-level account on grasp-and-lift and
NER2015 (per-cell correlation 0.37–0.65) and to chance for the support-vector
machine (0.35–0.61). We now say so in the table, in the text and in the
conclusion.

*The sign, and the majority-class problem.* The report is right that a raw sign
accuracy is uninformative when most cells share one sign. We report the majority
baseline next to the sign accuracy for every setting, and we add a split-sample
test in which t* is estimated on one half of the target and the sign is evaluated
on the other half. The result is honest and mixed: raw sign accuracy is 0.869 for
2b LDA against a baseline of 0.889 (no gain), but the sign-discrimination AUC is
0.914, and 0.846, 0.844 and 0.877 in three further LDA/logistic settings, against
0.50–0.53 for the SVM. The claim is now "the law discriminates the sign for
mean-calibrated classifiers, and its quantitative per-cell accuracy is the
stronger evidence", not "80–97 per cent sign accuracy".
(Section 2.3, Section 4.5 and Table 6; Fig. 4; Abstract; Section 7.)

## MC2 — `z_w` was mis-stated in the binary case (Critical)

**Fixed; the code was right and the text was wrong.** The definition
z_w = ‖P W μ_A‖/(√K σ_s) is the one the code implements. In the binary case
W = [w'; −w'], so P W μ = [w'μ; −w'μ], ‖P W μ‖ = √2|w'μ| and, with √K = √2,
z_w = |w'μ_A|/σ_s. There is no ‖w‖ in the denominator; the previous text was
wrong and the sentence is replaced by the derivation. We verified the agreement
between the closed form and the implementation over 200 cells: maximum
difference 4 × 10⁻¹⁴. σ_s is defined explicitly as the standard deviation of the
source decision values, pooled over classes and samples, with the per-column
generalisation to K > 2. A definitions paragraph now collects z_T, z_w, ρ and s,
their inputs and their roles, and states that all three are scale-invariant.
(Section 2.3.)

## MC3 — the dataset-level p-value was asymptotic (High)

**Corrected to the exact permutation value.** With five observations there are
120 orderings; ten are at least as extreme as ρ = −0.90, so the exact two-sided
p is 0.083, not 0.035. The exact value is now primary and the normal
approximation is reported as secondary, with the sentence "the result is
suggestive and does not reach 0.05". (Section 4.4; Abstract.)

## MC4 — Proposition 3 still over-claims for label predictions (High)

**Restated.** The proposition is now *score-difference equivalence*: identical
score differences for every input and every class pair iff P W(γ − γ') = 0.
Prediction (label) equivalence is a corollary, with two caveats stated in the
text: a class whose score is dominated everywhere can be shifted without
changing any decision, so label equivalence is strictly weaker; and for a finite
sample agreement of predictions can occur without the condition. (Section 2.2.)

## MC5 — the screen has not been shown to support a decision (High)

**We tested the decision, and we report the failures.** Defining a severe loss
as |penalty| > 0.05 (228 of 845 cells), z_w reaches an AUC of 0.839 and a
precision-recall AUC of 0.648, with a cluster-bootstrap interval over datasets
of [0.733, 0.881]. Within single datasets it reaches 0.834 (BCI-2a), 0.847
(BCI-2b) and 0.857 (grasp-and-lift), 0.693 on NER2015, and it *inverts* on SEED
(0.332). The BCI-2a representation anomaly the report identified is now reported
as the clearest failure: the four representations have z_w between 0.285 and
0.325 and penalties from +0.024 to −0.184, so the statistic cannot resolve which
representation of a given dataset is exposed. The abstract, Section 4.4, Section
5 and the limitations all say that the statistic triages a feature family, not
that it screens a representation. (Section 4.4; Section 5; Section 6.4.)

## MC6 — the sign prediction used target labels (High)

**Addressed with a split-sample test, and reported against the majority
baseline.** t* is estimated on one half of the target and the sign is evaluated
on the other half. Sign-discrimination AUC: 0.914 and 0.846 (BCI-2b, LDA and
logistic), 0.844 and 0.877 (BCI-2a), 0.670 and 0.646 (grasp-and-lift); 0.529,
0.503 for the SVM settings, i.e. chance. Raw sign accuracy is reported next to
the majority rate, and where the law does not beat that rate we say so. The
answer to the report's question 4 (stability across class counts) is that the
law is quantitative on the 2-class and 4-class (binary-reduced) BCI data and
degrades on the 2-class datasets with weaker decoding — which we attribute to
the equal-variance Gaussian approximation, not to the class count, and state as
an observation. (Section 4.5; Section 6.4.)

## MC7 — online value (Medium–High)

The transductive nature of the correction is stated in the limitations; the
running-mean experiment reports both trial orders; and the calibration-trial
curve is reported for k = 5, 10, 20, 50 with the recorded order failing on the
block-structured datasets. We have not run a full causal replay with a separated
calibration block, and we say so rather than implying otherwise. (Section 5;
Section 6.4.)

## MC8 — distinctiveness from known linear-discriminant facts (Medium–High)

A new paragraph in Section 6.1 separates three kinds of statement: corollaries of
linear discriminant theory (proved, not claimed as discoveries); empirical
regularities of cross-session EEG features (which feature families carry a free
origin, how large the damage is on five public datasets, and the two ways in
which a source-only screen fails); and changes in practice (centre both sessions,
run the one-line invariance test, do not use a norm-based origin statistic). The
abstract leads with the second and third. (Section 6.1; Section 1.)

## Minor comments

1. **Equation (5).** Corrected. With ḡ = Σ_k π_kB(m_kB − m_kA) and Σ_k π_kB h_k = 0
   by construction, the h_k indeed drop out of the mean, and Equation (5) is now
   written as μ_B − μ_A = ḡ + Σ_k(π_kB − π_kA)m_kA. The role of h_k in the
   class-conditional placement, and hence in the residual, is stated separately.
2. **Multiclass direction control.** Stated as a limitation: the orthogonality in
   Section 4.3 is defined with respect to w, i.e. the binary case; for K > 2 the
   invariant direction is the null space of P W and we did not run that version.
3. **SEED dependence.** The target mean uses all 3394 segments without grouping,
   because it is a first moment; the film grouping applies to the reference CV
   only; the shared-film dependence across sessions is stated and not modelled,
   and SEED's screening result is reported as the failure case.
4. **BCI-2b pair types.** Levels and gains are both reported for the three pair
   types (0.6461→0.6769, 0.7430→0.7677, 0.7247→0.7680).
5. **Calibration intervals.** Replaced by paired bootstrap differences of the
   per-subject ECE: one-sided minus uncorrected +0.254 [+0.229, +0.282] on
   BCI-2b, +0.129 [+0.098, +0.160] on SEED, +0.030 [+0.013, +0.047] on
   grasp-and-lift; two-sided minus uncorrected −0.014 [−0.036, +0.006],
   −0.251 [−0.296, −0.205] and −0.006 [−0.010, −0.002].
6. **Reproducibility.** The archive is at
   https://github.com/gzhgzy1234567890-lang/EEG-BSPC/tree/main/origin_equivariance
   (public). The scripts for the new analyses are `pv8_exp14.py` (per-cell law and
   split sample), `pv8_exp15.py` and `pv8_exp16.py` (definitions, exact
   permutation test, screening AUC, pair types, paired calibration), `pv8_fig4.py`
   (Fig. 4); their plain-text output is in `results/`. We would be glad to provide
   a zip if the reviewer's access failed for network reasons.

## What we have not done

A sixth dataset that played no role in choosing the statistic has not been
tested; the leave-one-dataset-out fit is compressed and we report it as a weak
check. The prevalence audit remains a single example. We do not claim to have
closed either.
