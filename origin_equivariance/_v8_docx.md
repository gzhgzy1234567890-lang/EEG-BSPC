# Origin equivariance in cross-session EEG decoding: what a mean correction repairs and how to screen for the risk

Zihao Gong ^a,†^, Jiran Li ^b,†^, Ke Huo ^a^, Yubin Han ^c^, Guangyu Shi ^a^, Yongqiang Xie ^a,*^

^a^ School of Mechano-Electronic Engineering, Xidian University, Xi'an 710071, China

^b^ School of Humanities and Social Sciences, Beijing Forestry University, Beijing 100083, China

^c^ School of Life Science and Technology, Xidian University, Xi'an 710071, China

† These authors contributed equally to this work.

E-mail addresses: andy.zihao.gong@gmail.com (Z. Gong), dsx54188dsx@163.com (J. Li), huoke@stu.xidian.edu.cn (K. Huo), 2044037857@qq.com (Y. Han), 2793218576@qq.com (G. Shi), yqxie@xidian.edu.cn (Y. Xie, corresponding author).

## Abstract

Removing a session mean is the first step in cross-session EEG decoding, and two operations circulate under that description: centring both sessions, or centring one. We settle what the choice is. The two-sided form is equivariant to a change of the coordinate origin, and we characterize when two corrections are prediction-equivalent: exactly when they differ by a vector in the null space of the classifier's weights. Any other correction makes the result depend on a convention the pipeline does not report; five elaborations, including one that uses target labels, do not improve on the mean correction.

We then measure when it matters, separating risk from benefit. The one-sided form displaces the decision function by the projection of the target mean onto the fitted weights, so its damage is governed by two measurable quantities: the distance of the feature origin from the data centre, computable from the source session alone, and the displacement in units of the classifier's score spread. On 845 session pairs from five public datasets (BCI-IV-2a, 2b, SEED, NER2015, grasp-and-lift; 11 feature units) an origin sweep leaves the equivariant pipelines unchanged by 0.000 in balanced accuracy and drives the one-sided one to exact chance. The source-only statistic orders the damage across units (Spearman -0.76, permutation p = 0.009), and the displacement orders it across classifier settings (-0.78). The benefit of the correction is not ordered by the same statistic (negative result). A label-free certificate identifies collapse exactly (124 of 124 cells) and separates it from chance-level accuracy, which on an imbalanced target is usually not collapse.

**Keywords:** cross-session EEG decoding; feature centring; origin equivariance; calibration; decision threshold; reproducibility


## 1. Introduction

A classifier trained on one recording session and applied to another usually loses accuracy, and the first step in almost every cross-session pipeline is to remove a mean. The step is described as re-centring, mean removal, per-session normalisation or baseline correction, and it appears in pipelines that are otherwise unlike each other and inside calibration protocols [1-3]. It is also the step whose description is most often ambiguous, because two operations share the name.

*Two-sided centring.* Centre the training session on its own mean, fit the classifier on the centred data, and centre the target session on its own mean before predicting.

*One-sided centring.* Centre one session and not the other. There are two forms — centring only the target or only the training session — and they fail in opposite directions.

The two forms are not equally common in practice, and the reason is instructive: a framework that fits every transform inside the training fold never has to choose, because the reference is the fold; a custom pipeline that patches a normalisation step at prediction time does have to choose, and usually does so without saying which one it chose (Section 6.4).

A reader may reasonably ask why the algebra of two conventions deserves a paper. Our answer is that the ambiguity is a missing invariance, that the invariance is screenable before a target session is recorded, and that the size of the failure is predictable from quantities the source session already contains. Each of those three statements can fail, and the paper tests all three.

**What we establish.** (i) A characterization. The two-sided form is equivariant to a translation of the coordinate origin; the one-sided forms are not. We characterize when two corrections are prediction-equivalent — exactly when they differ by a vector in the null space of the classifier's weights — and show that this class contains the projected correction used in practice as well as any correction that differs from the mean by a class-constant. The characterization explains the empirical result that follows: seven elaborations of the correction, including two that use target labels, do not beat the mean correction, and the one that lies in the null space reproduces it to the last sample.

(ii) A measurement of when the convention matters, with the risk separated from the benefit. The failure of the one-sided form is a displacement of the decision function, whose size is the projection of the target mean onto the fitted weights. That displacement is governed, at the feature level, by the distance of the feature origin from the data centre, a statistic computable from the source session alone. Across eleven dataset-by-representation units the statistic orders the damage of the one-sided form (−0.755, p = 0.007), and a controlled origin sweep confirms the relation causally within cells. The *benefit* of the correction over doing nothing is a different quantity, and it is not ordered by the same statistic; we report that as a negative result rather than a screen.

(iii) A label-free certificate. The one-sided form collapses the classifier when a closed-form inequality on the fitted weights, the target mean and the target scores holds. The certificate is exact on all 845 cells and lets us separate collapse from chance-level accuracy, which on an imbalanced target is usually not collapse.

**What we do not claim.** We do not claim that one-sided centring is common; we have no audit of released code and put no number on its frequency (Section 6.4). We do not claim that the two-sided form is always more accurate: on a hinge-loss support-vector machine the sign reverses, and Section 4.4 shows that the reversal is predicted by the induced displacement rather than by the classifier family. We do not claim a decomposition of cross-session loss into calibration and discriminability; we report what the convention costs in accuracy and in probability calibration (Section 4.5) and what remains after correction (Section 4.8).

**Relation to prior work.** Apicella et al. [4] compared normalisation schemes with dedicated domain-adaptation methods on three EEG datasets and found that an appropriate normalisation often outperforms the adaptation algorithm. Our results are compatible and add a criterion: the normalisation whose output does not depend on the coordinate origin. The nearest formal relatives are the Euclidean and Riemannian alignment families [5-8]. He and Wu's Euclidean alignment whitens each trial's covariance by the inverse square root of an average reference covariance [6]; Zanini et al. centre covariance matrices with respect to a reference [8]. Both act on second-order structure. Neither is a translation of feature vectors, and the two are not reducible to one another: a whitening matrix that happens to be a multiple of the identity performs no alignment at all, so describing mean subtraction as a degenerate case of Euclidean alignment would run the degeneration in the wrong direction. What the families share is a question — against which reference is the new session expressed? — and what we add is that for the first-order version of that question the equivariant answer is unique in effect, and that its absence is detectable and its cost predictable.

Methods that remove session-specific directions before classification [9,10] estimate a subspace in which the two sessions agree rather than relocating a boundary by a constant; they operate on second-order structure and are complementary. Calibrating a classifier to a new session by re-estimating an intercept from a few labelled trials [1,2] is the procedure onto which our analysis of label use maps: we show that on balanced designs it changes no prediction relative to the label-free form.

## 2. Theory

### 2.1 Notation and the pipelines

Let A denote the training session with features X_A and labels y_A, and B the target session with features X_B and labels y_B, the latter used only for evaluation. Write μA = mean(X_A), μB = mean(X_B), and s_A for the elementwise standard deviation of X_A. A linear classifier fitted on A gives score functions

    s_k(x) = w_k'x + b_k ,   k = 1 ... K ,                                   (1)

with prediction argmax_k s_k(x). Linear discriminant analysis with a pooled within-class covariance and Ledoit-Wolf shrinkage [11] is the primary instance; Section 4.4 repeats the analysis with logistic regression and a linear support-vector machine.

**Table 1.** The pipelines compared in this paper. `zero` and `train-only` are the two one-sided forms; `mean` and `dbl` are the two descriptions of two-sided centring.

| name | fitted on | applied to | equivariant |
|---|---|---|---|
| none | X_A | X_B | yes |
| zero | X_A | X_B − μB | no |
| mean | X_A | X_B − μB + μA | yes |
| dbl (refit) | X_A − μA | X_B − μB | yes |
| train-only | X_A − μA | X_B | no |
| z-score | (X_A − μA)/s_A | (X_B − μA)/s_A | yes |

The last row is a per-feature affine re-expression applied to both sessions, and it returns the same predictions as `none` in all five datasets (Table 3). It matters because it is what many pipelines do before centring: in the space standardised by training statistics the two centrings coincide, which is part of why the distinction has escaped notice.

### 2.2 The correction, and what "the same correction" means

Consider the translation T_c : x -> x + c applied to all data, training and target alike, with the classifier refitted.

**Proposition 1 (equivariance).** Under T_c the `mean` and `dbl` pipelines return predictions identical to those they returned before the translation, for every c, provided the fitting procedure has an unpenalised intercept.

*Proof for `mean`.* The fit receives X_A + c. With an unpenalised intercept the fitted weights are unchanged and the intercepts become b_k − w_k'c. The candidate features become (x + c) − (μB + c) + (μA + c) = (x − μB + μA) + c. Their scores are

    w_k'[(x − μB + μA) + c] + b_k − w_k'c = w_k'(x − μB + μA) + b_k ,

the scores the candidates received before the translation, so the argmax is unchanged for every sample. *For `dbl`* both the training and the candidate features are unchanged, so no assumption on the fit is needed. For `none` the same cancellation occurs on both sides. QED

**Proposition 2 (prediction equivalence).** Two corrections x -> x − γ and x -> x − γ' return identical predictions for every target sample if and only if W(γ − γ') is a class-constant vector, where W is the matrix whose rows are w_k. In particular (i) a correction differing from another by a vector in the null space of W is prediction-equivalent, and (ii) among corrections whose reference is a function of the target sample mean alone, exactly one is equivariant, namely γ = μB, up to a class-constant.

*Proof.* The score of sample x under reference γ is s_k(x − γ) = s_k(x) − w_k'γ. The difference between the two corrections is (w_k'γ − w_k'γ'), which is independent of x but may vary with k. The argmax of a set of scores is unchanged by adding a constant that is the same for all k, and can change when the constants differ; hence the condition is exactly that w_k'(γ − γ') takes one value for all k. For (ii), equivariance requires γ(X_B + c·1) = γ(X_B) + c for every c; the only function of the mean satisfying this is the mean plus a constant, and a constant is class-constant. QED

Proposition 2 is why the paper does not propose a new estimator. The prediction-relevant content of a correction is the vector of K numbers Wγ; two corrections that agree there are the same pipeline, and a correction that disagrees there has moved the decision function, which is either a deliberate relocation of the boundary or a dependence on an unreported convention. Section 4.5 verifies the null-space corollary to the last sample and shows what happens to the three corrections that leave the null space.

**Proposition 3 (the one-sided forms).** Under T_c the `zero` pipeline assigns to x + c the score it previously assigned to x, shifted by −w_k'c; the `train-only` pipeline shifts by +w_k'c.

Proposition 3 follows from the same computation. The two one-sided forms differ only in the sign of the shift; they are the same kind of failure.

**Corollary (decision-space form).** For an affine model the correction can be applied to the K scores instead of to the D features: subtracting δ_k = w_k'(μB − μA) from score k returns the same predictions as the feature-space correction, and requires neither the features nor a refit. The two forms are related by Proposition 2, since they differ by exactly W(μB − μA).

**Proposition 4 (rank preservation).** For any two samples x, x' and any two classes j, k, the comparison s_j(x) − s_k(x) versus s_j(x') − s_k(x') is unchanged by any of the six pipelines. Consequently every threshold-free measure of ranking quality is unchanged: the binary AUC for K = 2 and the pairwise AUC for K > 2.

This is the sense in which centring cannot "improve the representation": it moves a threshold. We therefore report accuracy and calibration, not AUC, as the quantities of interest, and we do not read a change in AUC as a change in discriminability.

### 2.3 What governs the damage

*The origin distance.* Define

    z_T = || μ_A || / || sd_A || ,                                            (2)

the distance of the feature origin from the data centre, measured in within-session standard deviations of the source session. z_T uses no target data. When a feature is a logarithm of power the origin is the logarithm of an arbitrary reference — amplifier gain, a floor added before the logarithm, the reference electrode — and z_T is large; when a feature is a difference of two conditions measured close in time the origin is near the data centre and z_T is small.

*The induced displacement.* Project the target mean onto the classifier's own scale,

    ρ = || W μ_B − mean_k(w_k'μ_B) || / sqrt(K) / sd(s) ,                      (3)

the size of the threshold shift that the one-sided form applies, in units of the score spread. ρ needs the target features but no target labels. For K = 2 it reduces to |w'μB| / sd(s).

*The damage law.* For a two-class problem whose class-conditional scores are Gaussian with equal variance, the balanced accuracy of a pipeline whose threshold is displaced by t score-standard-deviations from the optimal position is

    BA(t) = ½ [ Φ(c + t) + Φ(c − t) ] ,   c = Φ⁻¹(BA_aligned) ,                (4)

which is maximal at t = 0 and, for small t, falls as ½ φ(c) c t². Two consequences are counter-intuitive and both are tested below. The damage is second order in the shift, so a pipeline can survive a moderate displacement and then collapse abruptly; and the damage grows with c, so a *better* decoder is more exposed to a threshold error, not less, until the displacement is large enough to collapse it to chance.

**Proposition 5 (collapse certificate).** After `zero` centring the classifier returns the single class c for every target sample if and only if, for every k ≠ c,

    w_k'μB − w_c'μB  >  max_x [ s_k(x) − s_c(x) ] .                            (5)

The criterion uses the fitted weights, the target mean and the target scores, and no target labels. When it holds, balanced accuracy equals 1/K exactly.

Proposition 5 is a retrospective, label-free check on the target session whose scores it explains; it is not a forecast of collapse in a session not yet recorded. Its practical value is diagnostic: it separates a pipeline that has collapsed from one that is merely inaccurate, and Section 4.8 shows that the two are different events even when both report chance-level accuracy.

### 2.4 What cannot be repaired

Write the target class-conditional means as m_k^B = m_k^A + ḡ + h_k, with ḡ the class-balanced mean offset and Σ_k h_k = 0. The `mean` pipeline removes the sample mean, which equals ḡ plus the prior-weighted average of the h_k; on a balanced design the two agree. The residual h_k is confounded with a change of class prior: a target whose classes are re-weighted has class-conditional means that move in opposite directions while the design matrix is unchanged. No label-free method can separate a prior change from a class-conditional offset, because both act on the first two moments in the same way; separating them requires labels or an assumption about the prior. This is the standard label-shift identification problem [12], and it bounds what any correction of the form studied here can achieve. Section 4.9 measures how much of the residual is associated with the class-conditional offset and reports where that association fails.

## 3. Data and protocol

**Datasets.** Five public datasets, chosen to differ in class count, channel count, feature type, session structure and — crucially — in whether the electrode cap was removed between sessions.

*BCI Competition IV 2a* [13]: four motor-imagery classes, 22 channels, 250 Hz, nine subjects, two sessions recorded on different days; features from the 2.0–6.0 s window after trial onset, band-passed 8–30 Hz, in four representations.

*BCI Competition IV 2b* [13]: two classes, three channels (C3, Cz, C4), nine subjects, three retained sessions per subject on different days; every chronologically ordered pair among the retained sessions contributes one cell, 27 pairs over nine subjects.

*SEED* [14,15]: three emotion classes, 62 channels, 15 subjects, three sessions on different days; the features are the distributed 1 s differential-entropy series, 3394 segments per session in 15 film-defined blocks. The target-session reference uses `StratifiedGroupKFold` with the film as group, because adjacent segments of one film are not independent.

*NER2015*: sixteen subjects, five sessions on different days with the cap re-applied, two classes (correct versus error feedback) whose priors vary strongly across sessions (0.17 to 0.73 in the retained cells); 56 channels, eight windows, time-domain mean features.

*Grasp-and-lift*: twelve subjects, eight series recorded within a single session with the cap left in place, two classes (hand movement versus rest), 32 channels, eight windows of log power. This is the negative control: series differ by minutes rather than days and no electrode was replaced.

A *cell* is one (dataset, representation, subject, session-pair) combination: 36 + 108 + 45 + 320 + 336 = 845 cells from 61 subject-session units and 11 dataset-by-representation units.

**Table 2.** The datasets. The last column is the origin distance of Equation (2), computed on the source session only, median over the cells of the dataset.

| dataset | classes | subjects | session structure | representations | cells | median z_T |
|---|---|---|---|---|---|---|
| BCI-IV-2a | 4 | 9 | two days, cap replaced | 4 | 36 | 0.50 |
| BCI-IV-2b | 2 | 9 | three days, cap replaced | 4 | 108 | 16.1 |
| SEED | 3 | 15 | three days, cap replaced | 1 | 45 | 34.2 |
| NER2015 | 2 | 16 | five days, cap replaced | 1 | 320 | 0.20 |
| grasp-and-lift | 2 | 12 | one session, cap in place | 1 | 336 | 0.25 |

The median hides a wide within-dataset spread that is itself the subject of Section 4.3: in BCI-IV-2b the CSP representation has z_T = 0.22 and the log-power representation 57.1, and in BCI-IV-2a the tangent representation has 0.37 and the log-power representation 7.9.

**Representations.** For 2a and 2b: Euclidean log-power (`euc`), Euclidean alignment followed by log-power (`euc_ea`), Riemannian tangent space (`tan`) and CSP log-variance (`csp`). For SEED the distributed feature is used as is; for NER2015 the time-domain mean over eight windows; for grasp-and-lift the log power over eight windows. A representation is fitted on the training session unless its definition requires statistics from both (Section 5).

**Classifiers.** Linear discriminant analysis with Ledoit-Wolf shrinkage [11] is the primary classifier; logistic regression and a linear support-vector machine are used in Section 4.4.

**Reference.** The within-session reference is cross-validation inside the target session using its own labels: stratified 5-fold for 2a, 2b, NER2015 and grasp-and-lift, `StratifiedGroupKFold` over films for SEED. It is not a ceiling and it differs from the cross-session classifier in training-set size as well as in session; on 2a it falls below the cross-session accuracy for two of the four representations, and on the 253-dimensional tangent representation it is not usable. We report it as a descriptive quantity and do not use it as a denominator anywhere in this paper.

**Statistics.** Cells are aggregated per subject first, then tested across subjects with a two-sided Wilcoxon signed-rank test, with a subject-level bootstrap of the median (10,000 resamples) and Cohen's dz. We do not treat the 845 cells as independent observations. The screen of Section 4.3 is reported at the level of dataset-by-representation units, n = 11, with per-unit medians as observations, and at the cell level with the cell as observation for description only.

## 4. Results

### 4.1 The two descriptions of two-sided centring are one pipeline

Fitting on X_A − μA and applying to X_B − μB, versus fitting on X_A and applying to X_B − μB + μA, gave identical predictions sample for sample in all 845 cells, with a maximum difference in balanced accuracy of 0.0e+00.

The same comparison identifies why the distinction has escaped notice. A pipeline that standardises with training statistics and then centres *either* way obtains the same result, and standardisation alone returns exactly the predictions of `none`: the balanced accuracy of the z-score pipeline equals that of `none` to four decimals in all five datasets (Table 3), and its predictions agree with `none` in 100 per cent of samples in every dataset. The distinction is inert in that space, not eliminated by it; a pipeline that passes log-power features to a classifier without standardising is fully exposed.

**Table 3.** Balanced accuracy of the pipelines, per dataset. `dbl` coincides with `mean` in every cell. `train-only` is the other one-sided form. The reference is the within-session cross-validation of Section 3.

| dataset | n | none | zero | mean | dbl | train-only | z-score | reference |
|---|---|---|---|---|---|---|---|---|
| BCI-2a (K=4) | 36 | 0.5656 | 0.5254 | 0.6119 | 0.6119 | 0.5141 | 0.5656 | 0.5355 |
| BCI-2b (K=2) | 108 | 0.7046 | 0.5831 | 0.7375 | 0.7375 | 0.5722 | 0.7046 | 0.7571 |
| SEED (K=3) | 45 | 0.4591 | 0.3377 | 0.7094 | 0.7094 | 0.3456 | 0.4591 | 0.7738 |
| NER2015 (K=2) | 320 | 0.5886 | 0.5865 | 0.5909 | 0.5909 | 0.5845 | 0.5886 | 0.6167 |
| grasp-and-lift (K=2) | 336 | 0.7770 | 0.7484 | 0.7815 | 0.7815 | 0.7521 | 0.7770 | 0.8350 |
| all | 845 | 0.6705 | 0.6346 | 0.6926 | 0.6926 | 0.6338 | 0.6705 | 0.7264 |

![Figure 3](figs/fig3.png)
**Fig. 3.** (a) Balanced accuracy of the three pipelines by dataset; (b) the gain of the two-sided over the uncorrected pipeline, one point per subject, with the box showing the median and quartiles. The two datasets with an origin offset are the two in which the correction recovers most of the gap; the two without one are the two in which it recovers least.

The gain of `mean` over `none` is +0.0463 on 2a, +0.0329 on 2b and +0.2503 on SEED, and small in the two datasets without an origin offset: +0.0023 on NER2015 and +0.0045 on grasp-and-lift. Per subject, the gain is positive in 9 of 9 subjects on 2a (median +0.0356, bootstrap 95% CI [+0.0287, +0.0659], dz = 1.52, p = 3.9 × 10⁻³), 9 of 9 on 2b (+0.0321, [+0.0187, +0.0477], dz = 1.39, p = 3.9 × 10⁻³), 15 of 15 on SEED (+0.2452, [+0.2038, +0.2958], dz = 2.71, p = 6.1 × 10⁻⁵), 10 of 16 on NER2015 (+0.0050, [−0.0018, +0.0062], p = 0.32) and 8 of 12 on grasp-and-lift (+0.0031, [+0.0007, +0.0090], p = 0.052).

The one-sided form is worse than no correction wherever there is an origin offset: −0.0402 on 2a, −0.1215 on 2b, −0.1214 on SEED. On the two datasets without one it is also worse, but by less (−0.0021 on NER2015, −0.0286 on grasp-and-lift), and Section 4.4 shows that the sign there depends on the classifier.

### 4.2 An origin sweep: the equivariant pipelines are exactly flat

To measure the effect of the origin with the cells held fixed, we added a common constant to every feature, in both sessions alike, so that the data are unchanged up to an unreported convention, and swept its size over ten settings, which moves z_T over a 250-fold range; the sweep was run on all 845 cells.

![Figure 1](figs/fig1.png)
**Fig. 1.** (a) Change in balanced accuracy of the one-sided pipeline as a function of z_T, one curve per dataset; (b) the fraction of cells that land on exactly 1/K; (c) the largest change of the two equivariant pipelines over the whole sweep. The equivariant pipelines change by 0.0e+00 in every cell at every setting; the one-sided pipeline slides and stops.

Three results. First, `none` and `mean` are exactly invariant: across 845 cells and ten settings the largest absolute change in balanced accuracy was 0.0e+00 for both, in every dataset (Fig. 1c). This is Proposition 1 verified as an identity rather than as an empirical regularity, and it holds because the injected constant is exactly the class of transformations the proposition covers.

Second, the one-sided pipeline decays towards 1/K as z_T grows and stops there (Fig. 1a,b). On grasp-and-lift the decay is complete within the sweep, the fraction of cells at chance rising from 0.00 to 1.00 as z_T goes from 0.26 to 54.9. On BCI-2a it rises from 0.08 to 0.97; on NER2015 from 0.05 to 0.93; on BCI-2b the sweep starts at z_T = 26, where 0.60 of the cells are already at chance, and rises to 0.78; on SEED it starts at z_T = 34, where 0.90 are already at chance, and ends at 1.00.

Third, this is the only place in the paper where a causal claim is made about the origin: the constant changes nothing but the reported origin, the equivariant pipelines are unaffected to the last sample, and the one-sided pipeline's accuracy is a monotone function of the size of the change. Section 4.3 asks the complementary question, which requires real sessions.

### 4.3 The screen: the distance of the origin orders the damage

The sweep can create an origin offset; it cannot tell us which of the real representations are exposed to one. That is what the source-only statistic of Equation (2) does.

**Table 4.** The screen at the level of dataset-by-representation units, medians within a unit. `z_T` is the origin distance of the source session; `ρ` is the induced displacement of Equation (3); `penalty` = zero − none; `gain` = mean − none. Units are sorted by z_T.

| dataset | representation | n | z_T | ρ | penalty | gain |
|---|---|---|---|---|---|---|
| NER2015 | time mean | 320 | 0.20 | 0.21 | 0.000 | 0.000 |
| BCI-2b | csp | 27 | 0.22 | 0.50 | +0.018 | +0.026 |
| grasp-and-lift | log power | 336 | 0.25 | 0.25 | −0.015 | 0.000 |
| BCI-2a | tan | 9 | 0.37 | 0.41 | +0.014 | +0.031 |
| BCI-2a | csp | 9 | 0.40 | 0.40 | +0.024 | +0.059 |
| BCI-2a | euc_ea | 9 | 0.64 | 0.22 | −0.014 | +0.059 |
| BCI-2a | euc | 9 | 7.87 | 0.34 | −0.184 | +0.017 |
| BCI-2b | euc_ea | 27 | 14.2 | 5.27 | −0.137 | +0.018 |
| BCI-2b | tan | 27 | 21.2 | 5.15 | −0.160 | +0.020 |
| SEED | differential entropy | 45 | 34.2 | 0.98 | −0.029 | +0.211 |
| BCI-2b | euc | 27 | 57.1 | 23.2 | −0.186 | +0.021 |

Across the eleven units the rank correlation between z_T and the penalty is −0.755 (permutation over units, p = 0.009); across the 845 cells it is −0.382, which we report descriptively because cells within a unit are not independent. The units below z_T = 0.5 have penalties between +0.024 and −0.015, of either sign; the units above z_T = 7 have penalties between −0.029 and −0.186, all negative. The screen orders the damage; it does not produce a threshold that separates every unit, and SEED is the exception that keeps the correlation at −0.76 rather than higher: its origin is distant but its classifier is so poorly separated that the displacement buys little.

The feature-level statistic is a proxy for the decision-level one: z_T and ρ are correlated at +0.718 across units (p = 0.013) and +0.525 across cells (descriptive). Of the two, the feature-level statistic orders the penalty better (−0.755 against −0.464 for ρ), which is what one expects when the decision-level quantity saturates: beyond ρ ≈ 5 the classifier has already collapsed and further displacement adds nothing.

![Figure 2](figs/fig2.png)
**Fig. 2.** (a) The screen at unit level: origin distance of the source session against the penalty of the one-sided pipeline, one point per dataset-by-representation unit, area proportional to the number of cells; (b) the same relation per cell; (c) the origin distance against the induced displacement, which it proxies.

**What the screen does not do.** It does not order the *benefit* of the correction. Across the eleven units the rank correlation between z_T and the gain is +0.19 (p = 0.57), and between z_T and the fraction of the within-session gap that the correction recovers it is +0.27 (p = 0.49). The benefit is a property of the particular session pair — how large the class-mean offset is relative to the residual gap — and not of the feature family. We report this as a negative result: a laboratory can screen the risk of the wrong convention from the source session, and cannot screen the benefit of the right one without a target session.

### 4.4 The damage is a threshold shift, and the classifier family is not the variable

Table 3 showed that the sign of the one-sided effect depends on the classifier: on BCI-2b it is −0.098 for LDA and +0.030 for a linear support-vector machine with C = 0.01, and on SEED it is −0.121 for LDA and +0.197 for logistic regression. A reader who stops there concludes that the effect is a classifier artefact. It is not: it is a threshold shift, and ρ of Equation (3) measures it.

We swept the regularisation of three classifier families on BCI-2b, grasp-and-lift and NER2015, fourteen settings in total, and computed the mean damage of the one-sided pipeline and the median ρ.

**Table 5.** The damage of the one-sided pipeline against the induced displacement, for one dataset that is exposed and two that are not. Each row aggregates 60 cells.

| dataset | classifier | setting | none | zero | damage | ρ |
|---|---|---|---|---|---|---|
| BCI-2b | LDA | shrinkage 0.1 | 0.7065 | 0.6073 | −0.0992 | 3.41 |
| BCI-2b | LDA | shrinkage auto | 0.7018 | 0.6038 | −0.0980 | 4.93 |
| BCI-2b | LDA | shrinkage 0.9 | 0.6737 | 0.5820 | −0.0917 | 10.17 |
| BCI-2b | logistic | C = 0.01 | 0.6112 | 0.5685 | −0.0427 | 5.50 |
| BCI-2b | logistic | C = 10 | 0.7092 | 0.6094 | −0.0998 | 2.57 |
| BCI-2b | SVM | C = 0.001 | 0.6217 | 0.7133 | +0.0915 | 1.00 |
| BCI-2b | SVM | C = 0.01 | 0.6950 | 0.7251 | +0.0301 | 0.47 |
| BCI-2b | SVM | C = 10 | 0.7144 | 0.6258 | −0.0886 | 1.30 |
| grasp-and-lift | LDA | auto | 0.7897 | 0.7629 | −0.0268 | 0.24 |
| grasp-and-lift | SVM | C = 0.01 | 0.7464 | 0.7563 | +0.0099 | 0.17 |
| NER2015 | LDA | auto | 0.5873 | 0.5874 | +0.0002 | 0.26 |
| NER2015 | SVM | C = 0.01 | 0.5787 | 0.5850 | +0.0063 | 0.37 |
| BCI-2a (1 vs 2) | LDA | auto | 0.6759 | 0.5679 | −0.1080 | 2.27 |
| BCI-2a (1 vs 2) | SVM | C = 0.01 | 0.6427 | 0.6373 | −0.0054 | 0.33 |
| BCI-2a (1 vs 2) | SVM | C = 10 | 0.6574 | 0.6196 | −0.0378 | 1.10 |

The same sweep on a second exposed dataset, BCI-2a restricted to the two motor-imagery classes and the log-power representation (nine cells, thirteen settings), gives a rank correlation of −0.654 (p = 0.015) between ρ and the damage, with the same sign reversal: the LDA and logistic settings, at ρ between 1.5 and 6.6, lose 0.10 to 0.12, and the SVM settings, at ρ between 0.33 and 1.10, lose at most 0.038 and gain up to 0.010.

Across the fourteen BCI-2b settings the rank correlation between ρ and the damage is −0.78 (p = 1.0 × 10⁻³), and the sign reverses exactly where ρ falls below about 1: the strongly regularised support-vector machine, whose decision function is anchored by its support vectors rather than by the class means, has ρ = 0.47 and is *helped* by the one-sided centring, while the same family at C = 10 has ρ = 1.30 and is damaged by −0.089. The two datasets with no origin offset have ρ below 0.4 in every setting and damage no larger than 0.033 in absolute value, of either sign.

The practical reading is that the classifier family is a proxy for ρ, and ρ is computable before deployment from the target mean and the fitted weights. It also explains the one place where the one-sided form is not the worst of the three: when ρ is small the pipelines are within 0.03 of each other and the choice does not matter.

### 4.5 The correction is exact for its own component

Proposition 2 says that the prediction-relevant content of a correction is Wγ. We tested the corollary by building five alternatives and evaluating each on all 845 cells.

**Table 6.** Alternatives to the mean correction. `proj` subtracts only the component of the offset in the row space of the fitted weights; `shrink` subtracts half the offset; `low5` subtracts its projection onto the five leading source principal directions; `bal` subtracts the class-balanced offset and uses the target labels.

| dataset | none | zero | mean | proj | shrink | low5 | bal |
|---|---|---|---|---|---|---|---|
| BCI-2a | 0.5656 | 0.5254 | 0.6119 | 0.6119 | 0.5965 | 0.5873 | 0.6119 |
| BCI-2b | 0.7046 | 0.5831 | 0.7375 | 0.7375 | 0.7260 | 0.7318 | 0.7373 |
| SEED | 0.4591 | 0.3377 | 0.7094 | 0.7094 | 0.5551 | 0.4460 | 0.7092 |
| NER2015 | 0.5886 | 0.5865 | 0.5909 | 0.5909 | 0.5887 | 0.5873 | 0.6039 |
| grasp-and-lift | 0.7770 | 0.7484 | 0.7815 | 0.7815 | 0.7817 | 0.7793 | 0.7815 |

The projected correction returns predictions identical to `mean` in 100.0 per cent of samples in every dataset, as Proposition 2 requires: it differs from the mean correction by a vector in the null space of the weights. Halving the correction loses accuracy everywhere it matters, by 0.015 on 2a, 0.012 on 2b and 0.154 on SEED. Projecting onto the five leading principal directions is the worst of the alternatives on SEED, 0.446 against 0.709, because the offset's leading directions need not be the informative ones. Re-estimating the correction with the target labels changes nothing on the two balanced BCI datasets and on grasp-and-lift, gains 0.013 on NER2015 — the one dataset with a large change of class priors — and loses 0.0002 on SEED.

**The correction composes with second-order alignment.** The representations that already use a second-order correction are the natural test of whether the first-order correction is redundant after alignment. It is not. Within the Euclidean-aligned representation the mean correction still gains +0.0725 on BCI-2a and +0.0236 on BCI-2b; within the Riemannian tangent representation +0.0417 and +0.0452; within CSP +0.0575 and +0.0384; and within plain log power +0.0135 and +0.0245. The two corrections act on different moments and are not substitutes: alignment does not remove an origin offset, and centring does not remove a covariance change.

The last column is the empirical form of Section 2.4: where the class priors do not change, labels add nothing to the correction; where they do, the class-balanced offset recovers a further 0.013, and it does so by using the labels. An estimator that recovers it without labels would have to identify the prior change, which is the identification problem of Section 2.4 and which we do not solve.

### 4.6 Applying the correction without the features

The corollary of Proposition 2 has a practical consequence for deployed systems: a model that is frozen, wrapped behind an interface, or stored without its feature pipeline can still be corrected, because the correction needs only the K numbers δ_k = w_k'(μB − μA). We verified the equivalence on three linear families and three datasets. For LDA, logistic regression and a linear support-vector machine, on BCI-2b (60 cells), BCI-2a (36 cells) and grasp-and-lift (60 cells), the decision-space form returned predictions identical to the feature-space form in 100 per cent of samples, with a maximum discrepancy of 0.0e+00 and equal balanced accuracy to four decimals (for example 0.7365 and 0.7365 for LDA on 2b, 0.7188 and 0.7188 for the support-vector machine).

The practical difference between the forms is what they require. The feature-space form needs the target features, which in a deployed system means storing them; the decision-space form needs the target scores, which the system already computes, and K numbers rather than D. For the three linear families the two are interchangeable; for a non-linear model the decision-space form is an approximation, and we have not tested it.

### 4.7 Probability calibration

Accuracy is not the only quantity that moves. Under the one-sided form the decision function is displaced, so the confidence attached to each prediction is displaced with it.

**Table 7.** Calibration on three datasets, 60 cells each, LDA. ECE uses ten equal-width bins.

| dataset | pipeline | BA | ECE (median per subject) | 95% CI of the mean | Brier | log loss |
|---|---|---|---|---|---|---|
| BCI-2b | none | 0.7018 | 0.1041 | [0.0822, 0.1418] | 0.3842 | 0.5690 |
| BCI-2b | zero | 0.6038 | 0.3557 | [0.3033, 0.3774] | 0.7224 | 4.7724 |
| BCI-2b | mean | 0.7365 | 0.0900 | [0.0710, 0.1075] | 0.3437 | 0.5084 |
| SEED | none | 0.4591 | 0.5467 | [0.5086, 0.5692] | 1.0781 | 14.8384 |
| SEED | zero | 0.3377 | 0.6716 | [0.6617, 0.6725] | 1.3355 | 18.4447 |
| SEED | mean | 0.7094 | 0.2404 | [0.2335, 0.3504] | 0.5769 | 7.8051 |
| grasp-and-lift | none | 0.7897 | 0.1484 | [0.1416, 0.2176] | 0.3641 | 1.1935 |
| grasp-and-lift | zero | 0.7629 | 0.1909 | [0.1791, 0.2391] | 0.4187 | 1.4418 |
| grasp-and-lift | mean | 0.7938 | 0.1466 | [0.1358, 0.2153] | 0.3545 | 1.1277 |

The table reports, for each pipeline, the median of the per-subject expected calibration error and a bootstrap interval for its mean over subjects, so that the comparison is not carried by a pooled average over cells that are not independent. On BCI-2b the one-sided form raises the median expected calibration error from 0.104 to 0.356 and log loss from 0.569 to 4.772, with intervals that do not overlap; the two-sided pipeline returns 0.090 against 0.104, a difference whose intervals overlap and which we therefore do not claim as an improvement. On SEED every pipeline is poorly calibrated because the features are not probabilities of anything, but the ordering is the same and the magnitude larger, 0.547 to 0.672 to 0.240, again with non-overlapping intervals. On grasp-and-lift the differences are small and the intervals overlap, consistent with the small z_T of that dataset.

The calibration result matters for two reasons that are worth separating. A pipeline whose balanced accuracy falls from 0.70 to 0.58 and whose log loss rises from 0.57 to 4.77 is not merely less accurate; it is confidently wrong, which is the failure that matters when a probability is used downstream, for example to reject low-confidence trials. And the correction recovers calibration without any label, because it acts on the location of the decision function and not on its shape.

### 4.8 The collapse certificate, and the difference between chance and collapse

Proposition 5 identifies collapse from the target features and the fitted weights. On all 845 cells it agrees with the observed collapse — every prediction equal — in 124 of 124 collapsing cells and 721 of 721 non-collapsing cells, with no false positive and no false negative.

The certificate also separates two events that a balanced-accuracy threshold conflates. Of the 845 cells, 180 report balanced accuracy exactly 1/K after the one-sided pipeline. Only 124 of them have collapsed. The difference is concentrated in the imbalanced dataset: on NER2015, 66 cells are at chance and 16 have collapsed; on grasp-and-lift, 3 are at chance and none has collapsed. A target whose class priors are 0.17 and 0.83 can reach a balanced accuracy of 0.5 without returning a single class, because the classifier has scrambled both recalls. An audit that checks for chance accuracy therefore either stops too early — it calls a scrambled classifier "at chance" — or reports the wrong reason. The certificate supplies the reason.

**Table 8.** Collapse under the one-sided pipeline and its label-free prediction. The last column counts cells whose balanced accuracy is exactly 1/K, whether collapsed or not.

| dataset | K | collapsed | predicted | TP | FP | FN | TN | at chance |
|---|---|---|---|---|---|---|---|---|
| BCI-2a | 4 | 1 | 1 | 1 | 0 | 0 | 35 | 3 |
| BCI-2b | 2 | 67 | 67 | 67 | 0 | 0 | 41 | 67 |
| SEED | 3 | 40 | 40 | 40 | 0 | 0 | 5 | 41 |
| NER2015 | 2 | 16 | 16 | 16 | 0 | 0 | 304 | 66 |
| grasp-and-lift | 2 | 0 | 0 | 0 | 0 | 0 | 336 | 3 |

### 4.9 What is left

After the correction a residual gap to the within-session reference remains: 0.0198 on BCI-2b, 0.0770 on SEED, 0.0257 on NER2015 and 0.0294 on grasp-and-lift. It is not an origin effect: across all 845 cells the correlation between z_T and the residual is +0.06, and within datasets it has no consistent sign (BCI-2a −0.55, BCI-2b −0.37, SEED +0.41, NER2015 +0.11, grasp-and-lift +0.27). We therefore report it as a bound rather than as a second mechanism, and do not use it to support any claim in the abstract.

The residual is weakly associated with the class-conditional offset h_k of Section 2.4, measured as the component of the class-conditional mean shift orthogonal to the class-balanced mean, in units of the score spread: +0.21 on BCI-2a, −0.36 on BCI-2b, +0.33 on SEED, +0.30 on NER2015 and +0.55 on grasp-and-lift (pooled +0.26, four of five datasets in the same direction). A change of the within-session covariance explains less (pooled +0.10) and inconsistently. The correction removes what it can identify; what it cannot identify is the class-conditional part, and our measurement of that part is a weak and partly inconsistent predictor of the residual. We report it as the boundary of the account rather than as its confirmation.

## 5. The procedure

The results reduce to a procedure with three steps and one test.

**Step 1 — measure the origin distance from the source session.** z_T of Equation (2) requires nothing but the training features. Below 0.5 the penalty of the one-sided form is within ±0.024 across the units we studied, and the choice between the pipelines is not worth a figure; above 7 it is between −0.03 and −0.19, and the pipeline must be checked.

**Step 2 — use the equivariant form.** Centre both sessions and fit on the centred training data, or standardise with training statistics, which is equivalent. A pipeline that does this is invariant to the origin by Proposition 1, and Proposition 2 says nothing else needs to be done. If the model is frozen or the features are unavailable, subtract w_k'(μB − μA) from score k instead: Section 4.6 shows that this is exact for affine models and needs K numbers rather than D.

**Step 3 — apply the certificate before believing an accuracy.** Compute w_k'μB and the target scores; if (5) holds for some c, the classifier has collapsed and its balanced accuracy is 1/K by identity. If the accuracy is at chance but the certificate does not fire, the pipeline is not collapsed and the cause is elsewhere.

**The unit test.** Translate every feature by a constant, refit, and check that the predictions are unchanged. The test is one line of code, it is satisfied by construction by any equivariant pipeline and violated by any one-sided one, and it requires no labels and no reference result. It is the cheapest check we know of that would have caught the failure mode this paper is about.

**Deployment, and why the trial order matters.** For an online system the target mean is not available at the first trial, and the natural substitute is a running mean warm-started at the source mean. Whether that works depends on the order in which the trials arrive, and the two orders give different answers. With the trials drawn in a random order, the running reference is close to the batch correction after five trials: 0.7334 at k = 5 against a batch value of 0.7365 on BCI-2b, 0.7086 against 0.7094 on SEED, 0.7911 against 0.7938 on grasp-and-lift, and 0.6105 against 0.6119 on BCI-2a. With the trials in their recorded order the same pipeline is exact on BCI-2b (0.7409 against 0.7365) and clearly worse on the two datasets whose sessions are organised in blocks: 0.6724 against 0.7094 on SEED and 0.6781 against 0.7938 on grasp-and-lift, because the first trials of those sessions belong to one film or one series and are not a sample of the session. A running reference therefore does not remove the need for a calibration block; it moves the requirement to one of two conditions, either an exchangeable trial order or a warm-up that spans the blocks. We report both orders because the random-order result alone would have overstated the method.

## 6. Discussion

### 6.1 What the characterization buys

The practical content of Propositions 1 and 2 is that the question "which centring?" has an answer that is unique in effect, and that the answer is not a modelling choice. That is stronger than "the two-sided form is better", and it changes what a negative result means: if an elaborate correction does not beat the mean correction, the reason is not that the mean correction is a good heuristic but that there is nothing in the null space to find. Section 4.5 is an illustration of the characterization rather than a tournament of methods.

The characterization also explains why the ambiguity survives. Half the pipelines in use standardise their features with training statistics, and in that space the two centrings are the same expression; the other half do not, and in that half the two differ by the full offset. The two populations can report contradictory experience with the same nominal operation, and neither is mistaken about its own results.

### 6.2 Why some features are exposed and others are not

The statistic that orders the risk, z_T, is the distance of the feature origin from the data centre in within-session standard deviations. It is large when the feature carries a free additive constant. Log power has three: the logarithm of a reference power, any floor added before the logarithm, and any change of the reference electrode that adds an offset to the potential before a non-linear transform. Differential entropy, the log of a variance, inherits all three. A difference of two conditions measured within the same trial has none, which is why the time-domain contrast features of NER2015 have z_T = 0.20 and a penalty of 0.000.

This is a statement about measurement conventions, not about neurophysiology. The origin is set by the amplifier, the montage and the code, and none of the three is reported in a typical methods section. The invariance test of Section 5 makes the dependence visible without knowing which of the three changed.

### 6.3 Relation to alignment methods

Euclidean and Riemannian alignment [5-8] act on the second-order structure of the signal, and our result is orthogonal to them: an alignment matrix that happens to be a multiple of the identity performs no alignment, so the first-order correction is not a special case of the second-order one. The two corrections compose, and in our cells the second-order correction is not what recovers the gap: the representations that already use alignment statistics (`euc_ea`, `tan`) are not the ones with the largest gain, and the same-cap control shows that a gap can exist without an origin offset.

Riemannian geometry supplies the natural language for the second-order statement of the same question [16], and the linear classifier families we sweep are the standard ones for BCI [17]. Where the two intersect is the label-shift problem. Aligning a covariance implicitly assumes that the class mixture is unchanged, and re-weighting the classes changes the average covariance in a way that alignment cannot distinguish from a change of state. Section 2.4 shows the same ambiguity for the first-order correction, in a form that is easier to state: a prior change and a class-conditional offset are indistinguishable from unlabelled data. The consequence is the same for both families, and we state it as a bound rather than as a defect of a particular method.

### 6.4 Limitations

**Prevalence is measured only anecdotally.** We inspected one published cross-session example in detail — the MOABB cross-session motor-imagery script, which evaluates CSP+LDA and Riemannian tangent space + logistic regression with leave-one-session-out [18]. Neither pipeline centres the target at prediction time, and every transform is fitted inside the training fold. The example is therefore equivariant by construction and cannot exhibit the failure this paper is about. That is the correct way to build a cross-session pipeline, and it is also the reason the ambiguity is invisible in framework code: the framework fixes the reference to the training fold. The exposure is in pipelines that add a normalisation step at prediction time, outside the fold, which is what Section 1 describes and what the unit test of Section 5 detects. We have not surveyed that population, and we put no number on its size. A reader who believes the one-sided form is rare should read the paper as a statement about origin dependence rather than about prevalence; the recommendation survives that reading, and the unit test is the cheap way to settle the question for any particular codebase.

**The screen orders risk, not benefit.** z_T orders the penalty of the one-sided form across units (−0.755) and cells (−0.382), and does not order the gain of the correction (+0.19 across units, p = 0.57). The screen is a risk screen and nothing more.

**The classifier dependence is explained only to first order.** ρ orders the damage across regularisation settings on one dataset (−0.78 across fourteen settings) and separates the exposed from the unexposed datasets, but the scatter around that relation is large, and the two datasets with small ρ have damage of either sign.

**The reference is not a ceiling.** On 2a the within-session reference falls below the cross-session accuracy for two of four representations, and on the 253-dimensional tangent representation it is not usable. This is a property of the reference, not of the correction, but it limits what the reference can be used for.

**The residual is only partly explained.** The class-conditional offset predicts the sign of the residual in four of five datasets and fails on BCI-2b; the covariance change explains less. We report the boundary rather than closing it.

**The decision-space form is proved for affine models only.** Section 4.6 verifies the corollary for LDA, logistic regression and a linear support-vector machine. For a non-linear model the same shift is an approximation whose accuracy we did not measure, and a reader who deploys a non-linear decoder should check it on their own data before relying on the K-number form.

**No streaming protocol of the kind used online.** The running-mean experiment of Section 5 is a simulation on offline data with a random trial order. It shows that the correction does not need a calibration block, not that it performs as well under the trial order of a real session.

## 7. Conclusion

Two centrings circulate under one name, and only one of them is equivariant to the coordinate origin. The prediction-relevant content of a correction is the projection of its reference onto the classifier's weights; corrections that agree there are the same pipeline, and among references that are functions of the mean only one is equivariant. We prove this, verify the null-space corollary to the last sample, and show that five elaborations — projected, halved, low-ranked, standardised and one that uses the target labels — are no better than the mean correction, and are sometimes much worse.

The size of the failure is not a property of the dataset but of the feature's origin and of the classifier's anchoring. On 845 session pairs from five datasets, an origin sweep leaves the equivariant pipelines unchanged by 0.000 in balanced accuracy and drives the one-sided pipeline to exact chance; a statistic computed from the source session alone orders the damage across eleven dataset-by-representation units (Spearman −0.76) and across cells (−0.38); and the induced displacement orders the damage across classifier families and regularisation strengths (−0.78), which dissolves the appearance of a classifier artefact. The benefit of the correction over doing nothing is not ordered by the same statistic, and we say so. After correction the remaining gap is uncorrelated with the origin and weakly associated with the class-conditional offset, which is the part that labels carry and that no label-free correction can supply.

## CRediT authorship contribution statement

**Zihao Gong:** Conceptualization, Methodology, Software, Formal analysis, Investigation, Writing – original draft, Visualization. **Jiran Li:** Conceptualization, Methodology, Validation, Writing – review & editing. **Ke Huo:** Software, Data curation, Investigation. **Yubin Han:** Formal analysis, Validation, Visualization. **Guangyu Shi:** Data curation, Resources, Validation. **Yongqiang Xie:** Conceptualization, Supervision, Writing – review & editing, Project administration.

## Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Data availability

BCI Competition IV datasets 2a and 2b are available from the competition organisers. SEED is available from the BCMI Laboratory, Shanghai Jiao Tong University, on request for academic use; the present study used the differential-entropy features distributed with that release, unmodified. NER2015 and grasp-and-lift are Kaggle competition datasets and are publicly available. The analysis code, the feature-cache schema and the plain-text output of every number reported in this paper are archived at https://github.com/gzhgzy1234567890-lang/EEG-BSPC/tree/main/origin_equivariance (folder `origin_equivariance`), which is the version of record for the code.

## Acknowledgements

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

## References

[1] M. Krauledat, M. Tangermann, B. Blankertz, K.-R. Müller, Towards zero training for brain-computer interfacing, PLoS ONE 3 (2008) e2967.

[2] F. Lotte, Signal processing approaches to minimize or suppress calibration time in oscillatory activity-based brain-computer interfaces, Proc. IEEE 103 (2015) 871–890.

[3] C. Vidaurre, C. Sannelli, K.-R. Müller, B. Blankertz, Machine-learning-based coadaptive calibration for brain-computer interfaces, Neural Comput. 23 (2011) 791–816.

[4] R. Apicella, F. Isgrò, A. Pollastro, R. Prevete, On the effects of data normalisation on EEG-based BCI classification, IEEE Trans. Neural Syst. Rehabil. Eng. 31 (2023) 4591–4601.

[5] A. Barachant, S. Bonnet, M. Congedo, C. Jutten, Riemannian geometry for EEG-based brain-computer interfaces: a primer and a review, Brain-Comput. Interfaces 4 (2017) 155–174.

[6] H. He, D. Wu, Transfer learning for brain-computer interfaces: a Euclidean space data alignment approach, IEEE Trans. Biomed. Eng. 67 (2020) 399–410.

[7] F. Yger, M. Berar, F. Lotte, Riemannian approaches in brain-computer interfaces: a review, IEEE Trans. Neural Syst. Rehabil. Eng. 25 (2017) 1753–1762.

[8] P. Zanini, M. Congedo, C. Jutten, S. Said, Y. Berthoumieu, Transfer learning: a Riemannian geometry framework with applications to brain-computer interfaces, IEEE Trans. Biomed. Eng. 65 (2018) 1107–1116.

[9] W. Samek, K.-R. Müller, T. Kawanabe, M. Kawanabe, Brain-computer interfacing in discriminative and stationary subspaces, in: Proc. IEEE EMBS, 2012, pp. 2873–2876.

[10] B. Blankertz, M. Kawanabe, R. Tomioka, F. U. Hohlefeld, V. V. Nikulin, K.-R. Müller, Invariant common spatial patterns: alleviating nonstationarities in brain-computer interfacing, in: Adv. Neural Inf. Process. Syst. 20, 2008, pp. 113–120.

[11] O. Ledoit, M. Wolf, A well-conditioned estimator for large-dimensional covariance matrices, J. Multivar. Anal. 88 (2004) 365–411.

[12] M. Saerens, P. Latinne, C. Decaestecker, Adjusting the outputs of a classifier to new a priori probabilities: a simple procedure, Neural Comput. 14 (2002) 21–41.

[13] M. Tangermann, K.-R. Müller, A. Aertsen, et al., Review of the BCI competition IV, Front. Neurosci. 6 (2012) 55.

[14] W.-L. Zheng, B.-L. Lu, Investigating critical frequency bands and channels for EEG-based emotion recognition with deep neural networks, IEEE Trans. Auton. Ment. Dev. 7 (2015) 162–175.

[15] R.-N. Duan, J.-Y. Zhu, B.-L. Lu, Differential entropy feature for EEG-based emotion classification, in: Proc. 6th Int. IEEE/EMBS Conf. Neural Eng., 2013, pp. 81–84.

[16] M. Congedo, A. Barachant, A. Andreev, A Riemannian Gauss–Laplace distribution on the manifold of symmetric positive definite matrices, with application to anomaly detection and clustering, arXiv:2306.10543 (2023).

[17] F. Lotte, L. Bougrain, A. Cichocki, M. Clerc, M. Congedo, A. Rakotomamonjy, F. Yger, A review of classification algorithms for EEG-based brain-computer interfaces: a 10 year update, J. Neural Eng. 15 (2018) 031005.

[18] MOABB developers, Cross-session motor imagery example (CSP+LDA and Riemannian geometry + logistic regression, leave-one-session-out), NeuroTechX/moabb, 2024. https://github.com/NeuroTechX/moabb

