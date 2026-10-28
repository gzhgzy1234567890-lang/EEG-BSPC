# Causal mean correction in cross-session EEG decoding: a comparison of estimators and their failure modes

Zihao Gong ^a,†^, Jiran Li ^b,†^, Ke Huo ^a^, Yubin Han ^c^, Guangyu Shi ^a^, Yongqiang Xie ^a,*^

^a^ School of Mechano-Electronic Engineering, Xidian University, Xi'an 710071, China

^b^ School of Humanities and Social Sciences, Beijing Forestry University, Beijing 100083, China

^c^ School of Life Science and Technology, Xidian University, Xi'an 710071, China

† These authors contributed equally to this work.

E-mail addresses: andy.zihao.gong@gmail.com (Z. Gong), dsx54188dsx@163.com (J. Li), huoke@stu.xidian.edu.cn (K. Huo), 2044037857@qq.com (Y. Han), 2793218576@qq.com (G. Shi), yqxie@xidian.edu.cn (Y. Xie, corresponding author).

## Abstract

Removing a session mean is the first step of almost every cross-session EEG pipeline, and in deployment the mean has to be estimated from the trials that have already arrived. We compare four causal estimators of that mean on one protocol: a cumulative mean, a sliding window, an exponential average, and a shrunk estimator whose weight on the correction is n_eff/(n_eff + τ).

The experiments cover 845 cells from five datasets plus 90 held-out cells from SEED-IV. The comparison has a clear structure. Where the session mean is stable, every estimator recovers the transductive gain. Where the mean drifts between blocks, short-memory estimators are harmful. Where the mean drifts within a session, long-memory estimators are harmful, and the shrunk estimator reduces the loss from 0.115 to 0.024 without removing it — the loss remains significant (−0.024, 95% CI [−0.031, −0.016]) and we do not call the estimator safe. On SEED-IV, a related emotion paradigm rather than an independent one, it keeps four fifths of the transductive gain (+0.164 against +0.205). A label-free gate that tries to decide per block whether to correct, by matching the corrected score margins to the source session, does not work: it falls back to no correction on every dataset and loses the SEED gain. What the paper establishes is that the memory of the estimator, not the choice between one-sided and two-sided correction alone, determines whether a deployment gains or loses; what it does not establish is a rule that decides this in advance.

**Keywords:** cross-session EEG decoding; mean correction; origin equivariance; preprocessing audit; calibration; reproducibility

## Highlights

- The equivariant family of mean corrections is stated; uniqueness is not claimed.
- Score-difference equivalence follows from the centred classifier weights.
- Only the origin's projection on the weights damages the decoder, not its norm.
- A shrunk estimator cuts the worst-case loss from 0.115 to 0.024, not to zero.
- A badly estimated mean can cost more than not correcting at all.

## 1. Introduction

A classifier trained on one recording session and applied to another usually loses accuracy, and the first step of almost every cross-session pipeline is to remove a mean. The step appears under several names — re-centring, mean removal, per-session normalisation, baseline correction — and it appears in pipelines that are otherwise unlike each other and inside calibration protocols [1-3]. It is also the step that is most often described ambiguously, because two different operations are called by the same name.

*Two-sided centring.* Centre the training session on its own mean, fit the classifier on the centred data, and centre the target session on its own mean before predicting.

*One-sided centring.* Centre one session and not the other. There are two forms, centring only the target or only the training session, and they shift the decision function in opposite directions.

This paper compares the estimators a deployment can actually build from that choice, measures what the inconsistent variant costs, and reports where each estimator holds and where it fails. It asks three questions and answers each with the weakest statement the evidence supports.

**Equivariance.** Which corrections are invariant to a translation of the feature origin, and does the invariance single one out? Section 2.2 shows that the two-sided form is invariant and that the invariant family is larger than the sample mean, so the invariance cannot be used as a uniqueness argument. What it does establish is a requirement: a pipeline whose output depends on the unreported zero of the feature scale has a convention in it, and the convention is invisible.

**Equivalence.** When do two corrections give the same predictions? Section 2.3 gives the exact condition in terms of the centred classifier weights, and separates it from the finite-sample question of whether any particular set of trials crosses the boundary that moves.

**Performance.** Does the correction improve accuracy, and can the change be predicted? Sometimes it cannot, and the sign of the change is not governed by the size of the displacement: it is governed by where the training threshold already sits relative to the target optimum. Section 2.3 gives a Gaussian model of that mechanism, Section 4.5 tests it cell by cell under two parameterisations, and Section 6 states the boundaries.

**What the study covers.** Five public datasets, eleven dataset-by-representation units and 845 cells, chosen to span motor imagery, emotion, error-related potentials and movement, four feature families and three linear classifier families; a sixth dataset, SEED-IV, contributes 90 further cells and is used only as a held-out test of the one source-level statistic the paper defines. The measured quantities are not invented for the occasion: the origin distance of a feature family, the displacement it induces in the decision function, the sign of the resulting change, and the calibration of the resulting probabilities.

**What this paper does not claim.** We do not claim that one-sided centring is frequent. We inspected three released framework components (Section 4.11) and all three take their reference from the training fold or from a causal running mean, so none of them can exhibit the failure; we put no number on the frequency of the mistake in custom code, and the paper is written as an invariance verification rather than as a prevalence study. We do not claim that two-sided centring is optimal; Section 4.5 exhibits the settings in which it is not. We do not claim that the source-only statistic is a screening instrument; its held-out operating point has zero specificity and we say so in the abstract. We do not claim that the Gaussian model is a quantitative law; it is a mechanism with a measured range of validity.

**The operation is in current use.** A recent controlled benchmark makes the question concrete rather than academic: Rahimipour and Van Hulle [20] compare a tangent-space pipeline with unsupervised test-time recentering against deep sequence models on eight public motor-imagery datasets and conclude that the recentering, not the architecture, carries the cross-session advantage — the pipeline beats its recentering-free twin only across sessions, and is indistinguishable from it within a session. Their recentering is computed at test time, i.e. transductively, and it acts in the tangent space of the SPD manifold rather than on a Euclidean feature mean; the two operations share the word but not the object, and what we analyse here is the Euclidean one. That is also the operation a deployment can compute from a stream of feature vectors, which is why the causal question in Section 4.2 is worth asking of it. If the correction is the operative ingredient, then which correction it is, and whether it survives being computed online, are the questions worth answering.

**Relation to prior work.** Apicella et al. [4] compared normalisation schemes with domain-adaptation methods on three EEG datasets and found that an appropriate normalisation often outperforms the adaptation algorithm; our results are compatible and add a criterion, the invariance of the output to the coordinate origin. The nearest formal relatives are the Euclidean and Riemannian alignment families [5-8], which act on second-order structure; an alignment matrix that is a multiple of the identity performs no alignment, so the first-order correction audited here is not a special case of the second-order one, although the two compose (Section 4.6). Methods that remove session-specific directions [9,10] estimate a subspace in which the sessions agree rather than relocating a boundary by a constant. Calibrating a classifier to a new session by re-estimating an intercept from a few labelled trials [1,2] is the procedure onto which our analysis of label use maps; on four of five datasets it changes nothing relative to the label-free form, and on the fifth it gains 0.013 (Section 4.6).

## 2. Theory

### 2.1 Notation and the pipelines

Let A denote the training session with features X_A and labels y_A, and B the target session with features X_B and labels y_B, the latter used only for evaluation. Write μA = mean(X_A), μB = mean(X_B), and s_A for the elementwise standard deviation of X_A. A linear classifier fitted on A gives scores

    s_k(x) = w_k'x + b_k ,   k = 1 ... K ,                                   (1)

with prediction argmax_k s_k(x). Let W be the K × D matrix whose rows are w_k, S the N × K matrix whose rows are the score vectors of N samples, and P = I_K − 11'/K the K × K projector that removes the class mean from a K-vector. The centred scores are therefore S P, an N × K matrix, and σ_k is the standard deviation of its k-th column. Linear discriminant analysis with Ledoit-Wolf shrinkage [11] is the primary classifier; Section 4.5 also uses logistic regression and a linear support-vector machine [17].

**Table 1.** The pipelines compared in this paper.

| name | fitted on | applied to | origin-equivariant |
|---|---|---|---|
| none | X_A | X_B | yes |
| zero | X_A | X_B − μB | no |
| mean | X_A | X_B − μB + μA | yes |
| dbl (refit) | X_A − μA | X_B − μB | yes |
| train-only | X_A − μA | X_B | no |
| z-score | (X_A − μA)/s_A | (X_B − μA)/s_A | yes |

### 2.2 Equivariance, and what it does not determine

**Proposition 1 (equivariance).** Under the translation T_c : x ↦ x + c applied to all data with the classifier refitted, the `mean` and `dbl` pipelines return predictions identical to those they returned before the translation, for every c, provided the fit belongs to the class of linear models whose intercept is unpenalised and whose fitting objective is invariant to a common translation of the inputs — LDA with a pooled or shrunk covariance, logistic regression with an unpenalised intercept, and a linear support-vector machine with an unpenalised intercept all qualify; a model whose intercept is penalised, or whose regulariser acts on the intercept, does not.

*Proof for `mean`.* The fit receives X_A + c; by the assumption on the objective the weights are unchanged and the intercepts become b_k − w_k'c. The candidate features become (x + c) − (μB + c) + (μA + c) = (x − μB + μA) + c, whose scores are w_k'[(x − μB + μA) + c] + b_k − w_k'c, the scores the candidates received before the translation. The argmax is unchanged. For `dbl` both the training and the candidate features are unchanged, so no assumption on the fit is needed. For `none` the same cancellation occurs on both sides. QED

**Proposition 2 (the equivariant family).** Let c ∈ R^D and let γ : R^{N×D} → R^D. A correction x ↦ x − γ(X) is equivariant, i.e. γ(X + 1c') = γ(X) + c for every c ∈ R^D, if and only if γ(X) = μ(X) + h(X − 1μ(X)') for some h : R^{N×D} → R^D that is translation-invariant. The family therefore contains more than the sample mean.

*Proof.* Write γ(X) = μ(X) + [γ(X) − μ(X)] and note that μ(X + c1) = μ(X) + c. Equivariance holds iff the bracket is unchanged by translation, i.e. iff it is a function of the centred sample only. QED

Two remarks. A reference of the form μ + a with a fixed vector a is equivariant and is not the sample-mean correction; the two differ by a in score space, and unless Wa is class-constant they give different predictions. Equivariance therefore does not single out the sample mean, and no uniqueness is claimed. What can be said is that h = 0 is the member of the family that adds no offset at all beyond the sample mean; any other h must be justified by something other than invariance.

**Proposition 3 (score-difference equivalence).** The score differences s_j − s_k are identical for every input x and every class pair (j,k) if and only if W(γ − γ') is a class-constant vector, equivalently P W(γ − γ') = 0.

*Proof.* The score of x under reference γ is s_k(x − γ) = s_k(x) − w_k'γ. The difference between the two corrections is w_k'(γ − γ'), independent of x. Adding a vector v to all class scores leaves every score difference unchanged iff v is class-constant; hence the condition. QED

For a finite target sample the condition is sufficient but not necessary for identical predictions: if no trial crosses the boundary that the difference moves, the labels agree. A class whose score is dominated everywhere can also be shifted without changing a decision, so label equivalence is strictly weaker than score-difference equivalence.

**Proposition 4 (rank preservation, for score-based rankings).** For any two samples x, x' and any two classes j, k, the comparison s_j(x) − s_k(x) versus s_j(x') − s_k(x') is unchanged by any of the six pipelines, because the added constants are identical for x and x'. Per-class, cross-sample rankings of the raw scores and of pairwise margins are therefore unchanged, and so is a macro-averaged one-versus-rest AUC computed from those scores, since each class score is shifted by the same constant. A measure computed from softmax probabilities is not covered: the per-class constants change the normalisation even though every margin is fixed. The statement does not extend to rankings computed from *softmax probabilities*: a per-class constant changes the normalisation, so a one-versus-rest ROC-AUC computed from softmax outputs can move even though every margin is fixed. It also holds only for a fixed model; for a refitted or standardised pipeline the scores are recomputed.

### 2.3 What governs the damage

**The displacement.** For a sample mean μ and a classifier with scores S, define

    ρ(μ) = ‖ D_σ⁻¹ P W μ ‖ / √K ,   D_σ = diag(σ_1, …, σ_K),   σ_k = SD[(S P)_{:,k}] ,   (2)

The scale is taken from the **centred** scores S P, and this matters: with σ_k taken from the raw columns, adding a class-common linear term a'x to every score leaves all predictions unchanged but changes the per-class score spreads, so the statistic would depend on how a decision function is written rather than on what it decides. With the scale from S P both numerator and scale are invariant, because P(W + 1a') = PW and (S + 1a'x) P = S P; we verify this numerically in Section 4.10. Equation (2) is the definition throughout; the scalar form |w'μ_A|/σ_s used later is its binary special case, valid when K = 2 or when all σ_k are equal.

Two instances of Equation (2) are used. With μ = μ_A it is the *source-only* statistic z_w, computable before any target data; with μ = μ_B it is the displacement ρ that the one-sided pipeline induces, computable from the target features but not from its labels.

**The size.** If the class-conditional scores of the aligned target were Gaussian with equal variance and the training threshold were optimal, the balanced accuracy at a threshold displaced by u standard deviations would be

    BA(c, u) = ½ [ Φ(c + u) + Φ(c − u) ] ,                                     (3)

with c the standardised half-separation. At u = 0 this is Φ(c), and for small u it falls as ½ c φ(c) u². The coefficient c φ(c) is not monotone: it increases up to c = 1, i.e. aligned balanced accuracy 0.84, and decreases beyond. The most exposed decoder is therefore neither the worst nor the best one.

**The sign.** Equation (3) is written around the *optimal* threshold, and the one-sided pipeline does not start there. Let s be the extra displacement that the one-sided pipeline applies relative to the two-sided one, and t* the displacement of the aligned threshold from the target optimum, both signed and in units of the score scale. The change is

    Δ = BA(c, t* + s) − BA(c, t*) ,                                            (4)

which is negative when the displacement moves the threshold away from the optimum and positive when it moves it closer. The magnitude ρ is unsigned and cannot determine this sign; the sign is carried by t*. Note that s and ρ are different quantities: ρ uses μ_B and measures the zero-versus-none shift, while s uses μ_A and measures the zero-versus-mean shift.

### 2.4 What cannot be repaired

Write m_kB = m_kA + ḡ + h_k with ḡ = Σ_k π_kB (m_kB − m_kA) the prior-weighted class-conditional offset, so that Σ_k π_kB h_k = 0 by construction. Then

    μ_B − μ_A = ḡ + Σ_k (π_kB − π_kA) m_kA .                                    (5)

The second term is the change in the mixture of the source class means; it is present even when nothing about the class-conditional distributions changes. Under the constraint the h_k do not enter the mean at all — they enter the class-conditional placement, which is where the residual of Section 4.9 comes from. Subtracting μB − μA removes the class-conditional offset and the prior-induced mixture term together; on a balanced design the second term vanishes, and when the priors change it does not.

If the class-conditional distributions are unchanged, p_B(x | y) = p_A(x | y), and the classes are distinguishable in the score space (the mixture components are not degenerate), the target priors are identifiable from unlabelled target data and can be estimated by the EM procedure of Saerens et al. [12]. Without that assumption a prior change and a class-conditional offset are confounded, since both act on the first two moments of the mixture, and no label-free method separates them.

### 2.5 The collapse identity

After `zero` centring the classifier returns a single class c for every target sample of the finite target set X_B if and only if, for every k ≠ c,

    w_k'μB − w_c'μB  ≥  max_{x ∈ X_B} [ s_k(x) − s_c(x) ] ,                    (6)

with equality resolved by the argmax tie-breaking rule (the smallest class index wins in our implementation). This is an identity: it rewrites argmax_k s_k(x − μB) = c for all x in X_B. The maximum is taken over the finite target set, not over R^D; over R^D it need not be bounded when the two weight vectors differ. It is useful operationally, because it can be checked from the fitted weights, the target mean and the target scores before any label, and because it distinguishes collapse from chance-level accuracy. It is not a predictive method, and the simplest label-free check of collapse remains counting the distinct predicted classes.

## 3. Data and protocol

**Datasets.** Six public datasets, chosen to span tasks, feature families and session structures.

*BCI Competition IV 2a* [13]: four motor-imagery classes, 22 channels, 250 Hz, nine subjects, two sessions on different days; features from the 2.0–6.0 s window after trial onset, band-passed 8–30 Hz, in four representations.

*BCI Competition IV 2b* [13]: two classes, three channels (C3, Cz, C4), nine subjects. Three sessions are retained per subject — the screening sessions 01T and 02T and the feedback session 03T — and every chronologically ordered pair among them contributes one cell, 27 pairs over nine subjects. Levels and gains are reported by pair type so that the introduction of feedback can be seen: 1→2 0.6461 → 0.6769, 1→3 0.7430 → 0.7677, 2→3 0.7247 → 0.7680.

*SEED* [14,15]: three emotion classes, 62 channels, 15 subjects, three sessions on different days; the distributed 1 s differential-entropy features, 3394 segments per session in 15 film-defined blocks. The reference uses `StratifiedGroupKFold` with the film as group; the target mean uses all segments of the session, because it is a first moment and not an estimate of generalisation.

*NER2015*: sixteen subjects, five sessions on different days with the cap re-applied, two classes (correct versus error feedback) whose priors vary from 0.17 to 0.73; 56 channels, eight windows, time-domain mean features over the trial. Both directions of every pair are used, 16 × 20 = 320 cells, because the two directions differ in μB and are not equivalent under a translation.

*Grasp-and-lift*: twelve subjects, eight series recorded within one session with the cap left in place, two classes, 32 channels, eight windows of log power; 12 × 28 = 336 unordered pairs. This is the same-cap control.

*SEED-IV* [19]: 15 subjects, four classes, three sessions, distributed differential-entropy features (62 channels × 5 bands); six ordered pairs per subject, 90 cells. It is used **only as a held-out test**: the statistic, its thresholds and the classifier were fixed before it was opened, and no parameter was tuned on it.

**Table 2.** The datasets. The last column is z_T = ‖μ_A‖/‖sd_A‖, the norm-based origin distance, median over cells.

| dataset | classes | subjects | sessions | representations | cells | median z_T |
|---|---|---|---|---|---|---|
| BCI-IV-2a | 4 | 9 | 18 | 4 | 36 | 0.50 |
| BCI-IV-2b | 2 | 9 | 27 | 4 | 108 | 16.1 |
| SEED | 3 | 15 | 45 | 1 | 45 | 34.2 |
| NER2015 | 2 | 16 | 80 | 1 | 320 | 0.20 |
| grasp-and-lift | 2 | 12 | 12 | 1 | 336 | 0.25 |
| SEED-IV (held out) | 4 | 15 | 45 | 1 | 90 | 56.3 |

A *cell* is one dataset-representation-subject-ordered-pair combination: 845 development cells from 61 subjects and 182 sessions, plus 90 held-out cells from 15 further subjects (76 subjects and 227 sessions in total). SEED and SEED-IV are distributed as separate cohorts; the releases we used share no subject identifiers, and we treat them as different subjects while noting that we cannot verify that no individual took part in both. Because a subject contributes several representations of the same pair, 845 cells correspond to **737 distinct session pairs**; the paper says "cells" whenever it means cells. The analyses do not all cover the same cells: the per-cell displacement model uses the 800 binary cells of the four binary datasets (for BCI-2a, the two-class subproblem of classes 1 and 2), and the held-out test uses the 90 SEED-IV cells.

**Representations, and which of them are source-only.** `euc` (log power), `csp` (filters fitted on the training session) and the single representations of SEED, SEED-IV, NER2015 and grasp-and-lift are computed from the training session alone. `euc_ea` and `tan` are not: Euclidean alignment and tangent-space mapping use the session covariance, and in our pipeline both sessions contribute, so a classifier trained on them has already seen the target. The two groups are kept apart wherever the paper makes a *source-only* claim: Section 4.4 reports the statistic on the source-only representations (773 of the 845 development cells) and treats `euc_ea` and `tan` as target-informed, reporting them only where the claim does not depend on the source-only status (Tables 3 and 8).

**Classifiers.** Linear discriminant analysis with Ledoit-Wolf shrinkage [11] throughout, with logistic regression (C = 1, lbfgs) and a linear support-vector machine (C = 0.01, hinge loss) in Sections 4.5 and 4.10.

**Reference.** The within-session reference is cross-validation inside the target session using its own labels: stratified 5-fold, `StratifiedGroupKFold` over films for SEED and SEED-IV. It is not a ceiling and it differs from the cross-session classifier in training-set size as well as in session; on 2a it falls below the cross-session accuracy for two of four representations.

**Statistics.** Cells are aggregated per subject first, then tested across subjects with a two-sided Wilcoxon signed-rank test, a subject-level bootstrap of the median (10,000 resamples) and Cohen's dz. Cell-level correlations are descriptive; dataset-level tests use exact permutation distributions over the datasets; the unit-level analysis is reported with a cluster bootstrap that resamples datasets. No analysis treats the 845 cells as independent.

**Which tests are primary.** Five tests are confirmatory: the subject-level Wilcoxon signed-rank test of the gain of `mean` over `none`, run separately per dataset, with Holm control across the five. After Holm the p-values are 3.05 × 10⁻⁴ (SEED), 0.016 (BCI-2a), 0.016 (BCI-2b), 0.104 (grasp-and-lift) and 0.320 (NER2015), so the gain is established on three datasets, not on five; grasp-and-lift's raw p of 0.052 becomes 0.104 and its median gain of 0.003 is not claimed as an improvement. Everything else — the classifier family comparison, the calibration differences, the unit-level correlations and the operating points — is exploratory, and we report it without a multiplicity correction and say so. Because the cells are very unevenly distributed across datasets (NER2015 and grasp-and-lift contribute 656 of 845), the pooled cell mean is dominated by those two datasets; the per-dataset numbers are the ones to read, and the equal-weight mean of the five per-dataset gains is 0.067 against the cell-weighted 0.022.

**Preprocessing detail.** The 2a/2b features use a fourth-order Butterworth band-pass at 8–30 Hz applied to the continuous signal, epochs from 2.0 s to 6.0 s after cue onset, and a per-trial log-variance in each of the four bands for `euc`; `csp` uses four filters per class fitted on the training session; `tan` maps the session covariance to the tangent space at the identity of the training session; `euc_ea` divides by the session covariance before the log. SEED and SEED-IV use the distributed differential-entropy features unmodified (five bands). NER2015 and grasp-and-lift use the mean and the log power over eight windows respectively. Classifiers use scikit-learn defaults except where stated: LDA with `solver='lsqr'` and `shrinkage='auto'` (the `svd` solver does not support shrinkage), logistic regression with C = 1 and the lbfgs solver, linear SVM with C = 0.01 and `dual=False`, all with a fixed random state of 0; numpy 1.21, scipy 1.7, scikit-learn 1.0. A minimal reproduction of Table 3 from the cached features is `python src/pv8_final.py 1,2` followed by `python src/pv8_figs.py`; the archive's README lists the command for every table.

**Sub-sampling.** Two analyses use a uniform subsample of a dataset's cells to bound computation: the classifier sweep reported in Section 4.5's discussion of regularisation (60 cells per dataset on grasp-and-lift and NER2015, equally spaced) and the direction experiment (60 cells in each of two datasets). The per-cell model of Table 8 and everything else use all cells of the relevant dataset.

## 4. Results

### 4.1 The two descriptions are one pipeline; standardisation is a different question

Fitting on X_A − μA and applying to X_B − μB, versus fitting on X_A and applying to X_B − μB + μA, gave identical predictions sample for sample in all 845 cells, with a maximum difference in balanced accuracy of 0.0e+00.

Standardisation with training statistics is a related but different operation. Write X̃ = (X − μA)/s_A for both sessions. In that space the source mean is zero, so `zero` and `mean` coincide, and the pipeline is equivariant. But "standardise only" is not the same transformation as "centre both sessions": the two differ by (μ_B − μ_A)/s_A on the target, and applying the model fitted on X̃_A to X̃_B gives the predictions of `none`, not of `mean`. In our data the two agree in 100.0 per cent of samples for BCI-2a and BCI-2b, and this is an empirical fact about LDA with Ledoit-Wolf shrinkage rather than a theorem: without shrinkage the covariance estimate on grasp-and-lift is rank-deficient and the agreement drops to 51.8 per cent (Section 4.10). What Table 4 calls the *one-sided patch* is a different object: it standardises the target only (or subtracts its mean only) and leaves the training session raw, which is not `z-score` and does not inherit its agreement with `none`.

**Table 3.** Balanced accuracy per dataset. `dbl` coincides with `mean` in every cell. The reference is the within-session cross-validation of Section 3.

| dataset | n | none | zero | mean | dbl | train-only | reference |
|---|---|---|---|---|---|---|---|
| BCI-2a (K=4) | 36 | 0.5656 | 0.5254 | 0.6119 | 0.6119 | 0.5141 | 0.5355 |
| BCI-2b (K=2) | 108 | 0.7046 | 0.5831 | 0.7375 | 0.7375 | 0.5722 | 0.7571 |
| SEED (K=3) | 45 | 0.4591 | 0.3377 | 0.7094 | 0.7094 | 0.3456 | 0.7738 |
| NER2015 (K=2) | 320 | 0.5886 | 0.5865 | 0.5909 | 0.5909 | 0.5845 | 0.6167 |
| grasp-and-lift (K=2) | 336 | 0.7770 | 0.7484 | 0.7815 | 0.7815 | 0.7521 | 0.8350 |
| all development | 845 | 0.6705 | 0.6346 | 0.6926 | 0.6926 | 0.6338 | 0.7264 |

The gain of `mean` over `none` is +0.0463 on 2a, +0.0329 on 2b and +0.2503 on SEED, and small where the features have no origin offset: +0.0023 on NER2015 and +0.0045 on grasp-and-lift. Per subject it is positive in 9 of 9 on 2a (median +0.0356, 95% CI [+0.0287, +0.0659], dz = 1.52, p = 3.9 × 10⁻³), 9 of 9 on 2b (+0.0321, [+0.0187, +0.0477], dz = 1.39, p = 3.9 × 10⁻³), 15 of 15 on SEED (+0.2452, [+0.2038, +0.2958], dz = 2.71, p = 6.1 × 10⁻⁵), 10 of 16 on NER2015 (+0.0050, [−0.0018, +0.0062], p = 0.32) and 8 of 12 on grasp-and-lift (+0.0031, [+0.0007, +0.0090], p = 0.052).

![Figure 1](figs/fig3.png)
**Fig. 1.** (a) Balanced accuracy of the three pipelines by dataset; (b) the gain of the two-sided over the uncorrected pipeline, one point per subject, with the box showing the median and quartiles.

### 4.2 An origin sweep: the equivariant pipelines are exactly flat

To measure the effect of the origin with the cells held fixed, we added a common constant to every feature, in both sessions alike, and swept its size over ten settings; the sweep was run on all 845 cells.

![Figure 2](figs/fig1.png)
**Fig. 2.** (a) Change in balanced accuracy of the one-sided pipeline as a function of z_T, one curve per dataset; (b) the fraction of cells that land on exactly 1/K; (c) the largest change of the two equivariant pipelines over the whole sweep, on a logarithmic axis whose floor is 10⁻¹⁶, so that a zero is drawn at the floor rather than as a measured value. The equivariant pipelines change by 0.0e+00 in every cell at every setting; the one-sided pipeline decays toward 1/K without reaching it uniformly within the sweep.

`none` and `mean` are exactly invariant: across 845 cells and ten settings the largest absolute change in balanced accuracy was 0.0e+00 for both, in every dataset (Fig. 2c). This is the numerical confirmation of Proposition 1, not an independent discovery: the algebra says the number must be zero, and the experiment says the implementation behaves as the algebra says. The one-sided pipeline decays toward 1/K as z_T grows, but it does not reach it uniformly within the sweep: on grasp-and-lift the fraction of cells at chance rises from 0.00 to 1.00 as z_T goes from 0.26 to 54.9; on BCI-2a from 0.08 to 0.97; on NER2015 from 0.05 to 0.93; on BCI-2b the sweep starts at z_T = 26 where 0.60 of the cells are already at chance and ends at 0.78; on SEED it starts at z_T = 34 where 0.90 are already at chance and ends at 1.00.

**The mean has to be estimated online, and the estimator is a design choice.** Centring the target on its own mean uses the whole session; a deployment has only the trials that have arrived. Two different things can then be built, and they must not be confused.

*Two-sided online correction.* The model is fitted on the uncorrected training session, and trial t of the target is corrected by

    x̃_t = x_t − μ̂_{t−1} + μ_A ,                                                (7)

with μ̂_{t−1} an estimate from trials 1 … t−1. This is the online counterpart of the two-sided pipeline: as μ̂ → μ_B it converges to `mean`.

*One-sided patch.* The same but without the training mean,

    x̃_t = x_t − μ̂_{t−1} ,                                                      (8)

which is the `zero` pipeline of Section 2.1 and the failure mode this paper analyses. Equations (7) and (8) differ by μ_A, i.e. by exactly the quantity at issue.

**Table 4.** Balanced accuracy on one common post-prefix test set (trials k+1 … n), LDA, mean over cells; k = 20 except SEED, where k = 50. `batch` is the transductive correction scored on the same trials. The last column is the one-sided patch of Equation (8) with the cumulative estimate. The intervals are subject-level paired differences against `none` (4,000 bootstrap resamples); the fixed-λ and oracle-λ rows are reported in the text below rather than in the table.

| dataset | none | batch | cumulative | window (50) | exponential (0.05) | shrunk | one-sided patch |
|---|---|---|---|---|---|---|---|
| BCI-2b | 0.7063 | 0.7428 | 0.7417 | 0.7419 | 0.7420 | 0.7327 | 0.5839 |
| BCI-2a | 0.5640 | 0.6111 | 0.6077 | 0.6145 | 0.6138 | 0.6043 | 0.5169 |
| SEED | 0.4599 | 0.7094 | 0.6782 | 0.4194 | 0.4178 | 0.6845 | 0.3394 |
| grasp-and-lift | 0.7704 | 0.7764 | 0.6560 | 0.6488 | 0.6236 | 0.7465 | 0.5942 |
| NER2015 | 0.5878 | 0.5883 | 0.5840 | 0.5842 | 0.5822 | 0.5867 | 0.5857 |

Three regimes appear, and they are why the estimator is a design choice rather than an implementation detail. Where the session mean is stable (BCI-2b, BCI-2a) every estimator recovers the transductive gain within 0.01 and the choice does not matter. Where the mean drifts between blocks (SEED), a *short-memory* estimator is harmful — a 50-trial window and an exponential average with α = 0.05 both fall below no correction, because within one film block the window sees only that block — while a long-memory estimator keeps the gain. Where the mean drifts *within* a session (grasp-and-lift), the reverse happens: the cumulative mean loses 0.115 because it averages across drift, and the exponential average loses 0.147. No fixed-memory estimator is safe on both.

**A shrunk estimator that is less bad.** The estimator that loses least is a cumulative mean whose weight is set by the number of trials seen:

    x̃_t = x_t − λ_t μ̂_{t−1} + λ_t μ_A ,   λ_t = n_eff / (n_eff + τ) ,           (9)

with n_eff = t−1 for the cumulative mean and τ = 50 fixed before the experiments. n_eff is the number of trials seen, which is an upper bound on the effective sample size of a correlated series rather than the effective size itself; for a stationary series with autocorrelation ρ(k) the latter is n/(1 + 2Σρ(k)), and the difference matters most on SEED, whose segments come from continuous film blocks. We therefore call the rule sample-count shrinkage and treat τ as a policy constant, not as a calibrated uncertainty. The unit of k is trials, which is not a common unit of time across datasets: a BCI trial is about eight seconds, a SEED segment one second, so k = 20 is roughly 160 s of motor-imagery data and k = 50 is 50 s of film; we report trials because that is what the estimator consumes, and the time conversion is given so that the cost can be compared across paradigms. At the start λ ≈ 0 and the pipeline returns `none`; as trials accumulate λ → 1 and it returns the two-sided correction. The estimator therefore spends its uncertainty on the safe side: it cannot damage a session at the start, and it cannot hold on to a stale mean once the evidence accumulates. On the five datasets the subject-level paired difference against no correction is +0.026 [+0.012, +0.041], +0.040 [+0.025, +0.057], +0.225 [+0.178, +0.272], −0.024 [−0.031, −0.016] and −0.001 [−0.004, +0.002], in the order BCI-2b, BCI-2a, SEED, grasp-and-lift, NER2015. It keeps almost all of the SEED gain (0.225 against 0.218 for the plain cumulative mean) and cuts the grasp-and-lift loss from 0.115 to 0.024, but the interval on grasp-and-lift stays below zero: the estimator reduces the damage, it does not remove it. τ is the only parameter and it was set to 50 before the experiments; the sweep below shows how much it matters. It trades the two regimes against each other: τ = 20 gives +0.031, +0.044, +0.225, −0.052 and −0.003 on the five datasets, and τ = 200 gives +0.012, +0.028, +0.198, −0.006 and −0.001, so a ten-fold change moves the numbers by at most 0.03 and leaves the pattern intact — a larger τ trusts the correction later, which costs a little on the stable datasets and buys a little on the drifting one. We report the sweep rather than a tuned value because the choice is a policy decision about which failure one prefers, not a quantity to be optimised on the test data.

**The estimator on the held-out dataset.** SEED-IV was not used to design Equation (9). On its 90 cells with k = 50 the shrunk estimator gives +0.164 [+0.128, +0.201] against no correction, against +0.189 [+0.144, +0.236] for the cumulative mean and +0.205 [+0.161, +0.254] for the transductive correction; the one-sided patch gives −0.105 [−0.143, −0.067]. The causal correction therefore transfers to a related paradigm — SEED-IV uses the same emotion task and the same differential-entropy features as SEED, so this is external validation within a family, not across families — and the shrunk estimator keeps about four fifths of the transductive gain there — the price of the safety it buys on grasp-and-lift.

**The comparison is not specific to LDA.** The same protocol with logistic regression gives, on BCI-2b, 0.7065 uncorrected, 0.7430 fully corrected and 0.7337 with Equation (9); on grasp-and-lift, 0.7601, 0.6393 and 0.7347. The ordering of the estimators is the same, which is what "model-agnostic" should mean here: the transform is independent of the classifier, and the ranking of estimators survives a change of classifier, but we do not claim it for non-linear decoders, for which the threshold-displacement analysis does not apply.

**Why the classifier stays affine.** The mechanism is a property of an affine decision function: a shift of the feature origin moves the intercept by w'c, and a non-linear model has no such global intercept to move, so the analysis would not apply to it. That is a scope statement, not a claim that non-linear decoders are immune; it says that the quantity this paper measures — a threshold displacement of the class scores — exists for the models it studies and is not defined the same way for the others. The estimator of Equation (9), by contrast, is model-agnostic: it only needs the training mean and the target stream.

**Fixed shrinkage already does most of the work, and an oracle shows the remaining gap.** A constant λ on the same protocol gives, on BCI-2b, 0.7186 (λ = 0.25), 0.7316 (0.5), 0.7408 (0.75) and 0.7417 (1.0) against 0.7327 for Equation (9); on grasp-and-lift the same four are 0.7514, 0.7236, 0.6906 and 0.6560 against 0.7465; on SEED, 0.4939, 0.5460, 0.6204 and 0.6782 against 0.6845. A fixed λ = 0.75 is therefore close to the shrunk rule on BCI-2b and better on grasp-and-lift, and the time dependence buys its advantage on SEED. Choosing λ per cell on the target labels — an oracle, not a method — reaches 0.7538, 0.6156, 0.6979, 0.7813 and 0.6015, so the gap between the best fixed rule and the oracle is 0.01 to 0.05 and is not closed by any of the causal rules we tried.

**A label-free gate that decides does not work.** The obvious way to make the method decide is to compare, at the end of each block of 25 trials, the margin distribution of the corrected scores with that of the source session and to correct only when it is closer. On every dataset this gate selects *no correction* for almost every block: 0.7099 on BCI-2b (against 0.7063 uncorrected and 0.7417 fully corrected), 0.5631 on BCI-2a, 0.4565 on SEED, 0.7093 on grasp-and-lift. The reason is that correcting by the full shift makes the margins *wider* than the source's, so the gate reads a correct correction as a distributional mismatch. We report the failure rather than a tuned variant of it: a decision rule that is label-free and reliable is the open problem this paper leaves.

**The one-sided patch is the harmful variant, and its cost is measurable.** Subtracting the estimate without adding the training mean back (Equation 8) costs 0.122 on BCI-2b, 0.047 on BCI-2a, 0.121 on SEED and 0.176 on grasp-and-lift relative to not correcting at all. That is the quantity the theory of Section 2.3 predicts, and it is an order of magnitude larger than the difference between good estimators.

### 4.3 The direction control

The sweep injects the origin along one direction, which is not enough: Section 2.3 says the damage is governed by the projection of the origin onto the weights, so an origin orthogonal to the weights should do nothing while raising any norm-based statistic. We ran that experiment with equal-norm origins in two directions.

**Table 5.**  Equal-norm origins, two directions, LDA, 60 cells per dataset. `change` is the penalty relative to the no-injection baseline.

| dataset | direction | norm | z_T | penalty | change |
|---|---|---|---|---|---|
| BCI-2b | none | 0 | 16.0 | −0.0443 | — |
| BCI-2b | parallel to w | 2 σ̄ | 16.0 | −0.1755 | −0.1312 |
| BCI-2b | orthogonal to w | 2 σ̄ | 16.1 | −0.0443 | 0.0000 |
| BCI-2b | parallel to w | 8 σ̄ | 15.9 | −0.1637 | −0.1194 |
| BCI-2b | orthogonal to w | 8 σ̄ | 15.6 | −0.0443 | 0.0000 |
| grasp-and-lift | none | 0 | 0.27 | −0.0147 | — |
| grasp-and-lift | parallel to w | 2 σ̄ | 0.27 | −0.2279 | −0.2132 |
| grasp-and-lift | orthogonal to w | 2 σ̄ | 0.27 | −0.0147 | 0.0000 |
| grasp-and-lift | parallel to w | 8 σ̄ | 0.49 | −0.3225 | −0.3078 |
| grasp-and-lift | orthogonal to w | 8 σ̄ | 0.50 | −0.0147 | 0.0000 |

The two directions give z_T values within 0.3 of each other on BCI-2b and within 0.01 on grasp-and-lift, which is the point: an equal-norm origin leaves the norm-based statistic essentially unchanged while the penalty moves by 0.13 to 0.31, and the orthogonal one changes the penalty by exactly 0.0000 in every cell while the parallel one changes it by −0.13 and −0.21 to −0.31. A norm-based statistic is therefore blind to the direction. The projected statistic of Equation (2) is unchanged in the orthogonal arm by construction, and it is the statistic we use.

**The same decomposition on real session shifts.** The sweep injects an origin; a session shift is not one. We therefore took the observed shift d = μ_B − μ_A of each cell, set A = P W, and split d into the row space of A and its complement, d∥ = A⁺A d and d⊥ = (I − A⁺A) d, so that d = d∥ + d⊥ and A d⊥ = 0 exactly. The split has to use A and not W: ker(W) is contained in ker(P W) but is generally smaller, so a shift can move the raw scores and still leave every class-score difference untouched, and projecting on W would count it as relevant. By construction only the first can move a decision, and that is what Proposition 3 says; what the data add is that its *magnitude* does not order the damage: across the 845 cells the rank correlation between ‖A d‖ and the penalty is +0.03, and between ‖d⊥‖ and the penalty +0.08, with within-dataset values between −0.04 and +0.59. The reason is the one Equation (4) gives: the damage is a threshold-crossing function of the shift and of where the threshold sits, not a monotone function of the shift. A real shift therefore does not reproduce the clean sweep, and the paper does not claim that it does — the sweep is a controlled input, the model of Section 2.3 is what connects it to the damage, and the online comparison of Section 4.2 is what connects the model to a deployment.

### 4.4 A source-level statistic, and its boundaries

![Figure 3](figs/fig2.png)
**Fig. 3.** (a) Unit medians of the source-only statistic against the penalty of the one-sided pipeline, one point per dataset-by-representation unit, with the held-out SEED-IV point shown as a star; (b) the same relation over the development cells. The four `euc_ea` and `tan` units are target-informed (Section 3); the source-only correlations quoted in the text are computed without them.

**Table 6.**  The source-only statistic at the level of dataset-by-representation units, medians within a unit. z_T = ‖μ_A‖/‖sd_A‖; z_w is Equation (2) with the scale taken from the centred scores; penalty = zero − none; gain = mean − none. † uses both sessions' covariances, so the classifier has seen the target; the source-only correlations are computed without these four rows. Sorted by z_w.

| dataset | representation | n | z_T | z_w | penalty | gain |
|---|---|---|---|---|---|---|
| BCI-2b | csp | 27 | 0.22 | 0.068 | +0.018 | +0.026 |
| NER2015 | time mean | 320 | 0.20 | 0.230 | 0.000 | 0.000 |
| grasp-and-lift | log power | 336 | 0.25 | 0.289 | −0.015 | 0.000 |
| BCI-2a | csp | 9 | 0.40 | 0.287 | +0.024 | +0.059 |
| BCI-2a | tan † | 9 | 0.37 | 0.309 | +0.014 | +0.031 |
| BCI-2a | euc_ea † | 9 | 0.64 | 0.597 | −0.014 | +0.059 |
| BCI-2a | euc | 9 | 7.87 | 4.399 | −0.184 | +0.017 |
| BCI-2b | tan † | 27 | 21.2 | 5.117 | −0.160 | +0.020 |
| BCI-2b | euc_ea † | 27 | 14.2 | 5.405 | −0.137 | +0.018 |
| SEED | differential entropy | 45 | 34.2 | 12.36 | −0.029 | +0.211 |
| BCI-2b | euc | 27 | 57.1 | 23.31 | −0.186 | +0.021 |

On the source-only representations — 773 of the 845 development cells, seven units, since `euc_ea` and `tan` are target-informed — the rank correlation between z_w and the penalty is −0.857, with a cluster bootstrap over datasets of [−1.000, −0.585] (median −0.862, 4,993 resamples), and the direction is the same at the cell level (AUC 0.831 for a loss larger than 0.05). Including the two target-informed representations in the unit-level analysis changes the correlation only to −0.827, so the statistic is not being carried by the representations a source-only analysis should not use. The statistic also resolves the four representations of BCI-2a, which the norm-based z_T does not: `euc` has z_w = 4.40 and a penalty of −0.184, while `csp`, `tan` and `euc_ea` sit between 0.29 and 0.60 with penalties between +0.024 and −0.014.

**The statistic is defined relative to a feature origin.** z_w uses the absolute source mean, so it answers the question "how far is this family's origin from the classifier's reference, in units of the score spread", not "how exposed is this family in an absolute sense". Translating every feature by a vector c changes the numerator to ‖D_σ⁻¹PW(μ_A + c)‖; a translation in the null space of PW leaves it unchanged, and a translation along the weights moves it one-for-one. The numbers in Table 5 are therefore comparable within one convention — the convention in which each dataset's features are built — and not across conventions; a feature family that is shifted by a constant before the pipeline would receive a different z_w. This is one reason we do not offer an absolute threshold, and it is a limitation of the quantity rather than of the measurement.

**Where it fails.** At the dataset level the picture weakens: on the source-only representations the five development datasets give a rank correlation of −0.80, and adding SEED-IV (median z_w = 24.4, median penalty −0.070) gives −0.83 with an exact permutation p of 42/720 = 0.058; over all representations the six-dataset value is −0.77, p = 0.103. A threshold of 0.354 fixed by Youden's J on the five development datasets flags every one of the 90 held-out cells (sensitivity 1.000, specificity 0.000, precision 0.544), and within SEED-IV the statistic has an AUC of 0.515. The leave-one-dataset-out operating point fails on two of five development datasets (SEED: sensitivity 1.000, specificity 0.000; NER2015: 0.273, 0.864) and works on three (BCI-2a 0.714/0.864, BCI-2b 1.000/0.574, grasp-and-lift 0.704/0.828).

**Table 7.**  Leave-one-dataset-out operating point for the statistic. The threshold is chosen on four development datasets and evaluated on the fifth.

| held out | n | threshold | sensitivity | specificity | precision |
|---|---|---|---|---|---|
| BCI-2a | 36 | 0.354 | 0.714 | 0.864 | 0.769 |
| BCI-2b | 108 | 0.354 | 1.000 | 0.574 | 0.753 |
| SEED | 45 | 0.354 | 1.000 | 0.000 | 0.489 |
| NER2015 | 320 | 0.475 | 0.273 | 0.864 | 0.188 |
| grasp-and-lift | 336 | 0.369 | 0.704 | 0.828 | 0.627 |

The conclusion we draw is that a source-level statistic can rank *feature families* within a set of datasets and cannot decide which session, subject or representation will fail. We report it because it is the natural quantity to compute before a target session exists, and because its three failures are as informative as its success.

### 4.5 A displacement model of the change, and its two parameterisations

Equations (3) and (4) make a prediction for the per-cell change once c, t* and s are fixed. They can be fixed in two ways, and the two are not the same. The *oracle* choice takes c = Φ⁻¹(BA_aligned) and normalises by the pooled score standard deviation; it is oracle-assisted because c is read from the target's own accuracy. The *model* choice takes c = (m₁ − m₀)/(2σ_w) from the source class means and the within-class standard deviation, which is what an equal-variance Gaussian model implies.

**Table 8.**  Per-cell prediction of Equation (4) under the two parameterisations. For BCI-2a the cells are the two-class subproblem of classes 1 and 2. `MAE` is the mean absolute difference between prediction and observation on the same cell; `r` is Pearson; `sign` and `base` are the sign accuracy and the majority-class rate under the oracle parameterisation; `BA gap` is the mean absolute difference between the model's implied accuracy Φ(c) and the observed aligned accuracy under the model parameterisation.

| dataset | classifier | n | oracle r | oracle MAE | oracle sign (base) | model r | model MAE | BA gap |
|---|---|---|---|---|---|---|---|---|
| BCI-2b | LDA | 108 | 0.989 | 0.0130 | 0.917 (0.815) | 0.861 | 0.0567 | 0.096 |
| BCI-2b | logistic | 108 | 0.990 | 0.0127 | 0.889 (0.769) | 0.852 | 0.0578 | 0.098 |
| BCI-2b | SVM | 108 | 0.381 | 0.0224 | 0.676 (0.528) | 0.655 | 0.0203 | 0.107 |
| BCI-2a | LDA | 36 | 0.902 | 0.0320 | 0.889 (0.833) | 0.874 | 0.0414 | 0.149 |
| BCI-2a | logistic | 36 | 0.885 | 0.0330 | 0.750 (0.750) | 0.824 | 0.0563 | 0.128 |
| BCI-2a | SVM | 36 | 0.610 | 0.0161 | 0.611 (0.528) | 0.711 | 0.0217 | 0.095 |
| grasp-and-lift | LDA | 336 | 0.649 | 0.0360 | 0.693 (0.604) | 0.271 | 0.0420 | 0.213 |
| grasp-and-lift | logistic | 336 | 0.592 | 0.0364 | 0.649 (0.607) | 0.531 | 0.0355 | 0.212 |
| grasp-and-lift | SVM | 336 | 0.353 | 0.0115 | 0.420 (0.292) | 0.191 | 0.0127 | 0.248 |
| NER2015 | LDA | 320 | 0.385 | 0.0285 | 0.556 (0.406) | not estimable (282 of 320 cells have a degenerate within-class spread) | — | — |
| NER2015 | logistic | 320 | 0.371 | 0.0258 | 0.509 (0.425) | not estimable | — | — |
| NER2015 | SVM | 320 | 0.458 | 0.0434 | 0.666 (0.503) | not estimable | — | — |

The oracle parameterisation fits well on the BCI data (r = 0.99, MAE 0.013) and the model parameterisation fits less well (r = 0.86, MAE 0.057); the model's implied accuracy is 0.10 to 0.21 away from the observed aligned accuracy, which is a direct statement that the equal-variance assumption does not hold on these scores. Part of the oracle fit is built in, because c is read from BA_aligned and BA_aligned also enters the observed change. Equation (4) is the standard threshold-shift formula of a two-class Gaussian model; what it adds here is not a new phenomenon but the statement that the sign of the effect is carried by t* and that t* is a property of the training session's own calibration, which is why the same correction helps a well-calibrated LDA and hurts a margin-anchored SVM. We therefore treat it as a mechanism with a measured range of validity, not as a predictive law. The label-free check above is the evidence for the second half of that sentence.

**The bound applies to the model, not to the data.** The inequality |Δ| ≤ 0.1995|s| follows from the derivative of Equation (3). Over the 800 binary cells the prediction violates it in 0 of 800 cases and the observation violates it in 185, i.e. 23.1 per cent, with a median ratio |Δ_obs|/|s| of 0.29 among the violations and a maximum of 4.1: empirical balanced accuracy is a step function of the scores and can jump.

**The sign, with and without a held-out half.** With t* estimated on one half of the target and the sign evaluated on the other half, the sign-discrimination AUC is 0.914 [0.853, 0.958] (BCI-2b, LDA), 0.848 [0.767, 0.917] (BCI-2b, logistic), 0.848 [0.705, 0.955] (BCI-2a, LDA), 0.786 [0.618, 0.924] (BCI-2a, logistic), 0.667 [0.606, 0.725] and 0.662 [0.599, 0.721] on grasp-and-lift. The support-vector machine is unstable across settings (0.571, 0.328, 0.478) and we do not claim the model for it. Raw sign accuracy is close to the majority rate, which is why we report the AUC.

**A source-only version of the same model does not work.** Replacing the target-optimal threshold t* by the source-optimal one — the threshold that maximises balanced accuracy on the training scores of the fitted model, in within-class units — makes the model fully source-only. The sign accuracy it reaches is at the majority baseline: 0.815 against 0.815 on BCI-2b, 0.613 against 0.604 on grasp-and-lift, and 0.750 against 0.833 on BCI-2a, with mean absolute errors of 0.06, 0.04 and 0.05. The mechanism is therefore explanatory only, as Section 6.4 states.

![Figure 4](figs/fig4.png)
**Fig. 4.** (a) Predicted change of Equation (4) against the observed change, one point per cell, LDA, the 800 binary cells; the dotted line is the identity. (b) Distribution of the prediction error.

### 4.6 Variants, labels, and the decision-space form

**Table 9.**  Alternatives to the mean correction. `proj` subtracts the component of the offset in the row space of W; `shrink` half the offset; `low5` the projection onto the five leading source principal directions; `bal` the class-balanced offset, using the target labels.

| dataset | none | zero | mean | proj | shrink | low5 | bal |
|---|---|---|---|---|---|---|---|
| BCI-2a | 0.5656 | 0.5254 | 0.6119 | 0.6119 | 0.5965 | 0.5873 | 0.6119 |
| BCI-2b | 0.7046 | 0.5831 | 0.7375 | 0.7375 | 0.7260 | 0.7318 | 0.7373 |
| SEED | 0.4591 | 0.3377 | 0.7094 | 0.7094 | 0.5551 | 0.4460 | 0.7092 |
| NER2015 | 0.5886 | 0.5865 | 0.5909 | 0.5909 | 0.5887 | 0.5873 | 0.6039 |
| grasp-and-lift | 0.7770 | 0.7484 | 0.7815 | 0.7815 | 0.7817 | 0.7793 | 0.7815 |

The projected correction returns predictions identical to `mean` in 100.0 per cent of samples, as Proposition 3 requires. Halving the correction loses accuracy where it matters (0.015 on 2a, 0.012 on 2b, 0.154 on SEED), and the low-rank variant is the worst on SEED (0.446 against 0.709). The label-based correction changes nothing on the four balanced datasets (0.0000 on 2a and grasp-and-lift, −0.0002 on 2b and SEED) and gains 0.013 on NER2015, the dataset whose priors change substantially, which is what Section 2.4 predicts.

The correction composes with second-order alignment: within the Euclidean-aligned representation the mean correction still gains +0.0725 on BCI-2a and +0.0236 on BCI-2b, within the tangent representation +0.0417 and +0.0452, within CSP +0.0575 and +0.0384, and within plain log power +0.0135 and +0.0245.

For an affine model the correction can also be applied to the K scores instead of the D features, by subtracting δ_k = w_k'(μB − μA) from score k. We verified the equivalence on three linear families and three datasets: identical predictions in 100 per cent of samples, maximum discrepancy 0.0e+00, equal balanced accuracy to four decimals (0.7365 against 0.7365 for LDA on 2b; 0.7188 against 0.7188 for the SVM). The decision-space form needs the target scores and K numbers rather than the target features.

### 4.7 Probability calibration

**Table 10.**  Calibration, LDA, every development cell. ECE is the expected calibration error of the predicted-class probability, computed with ten equal-width confidence bins and averaged within subject; the interval is a bootstrap over subjects of the *mean*, and the median is reported beside the mean, not inside that interval. The Brier score is the mean squared error of the predicted probability vector, and log loss clips probabilities at 10⁻¹². The paired differences are given in the text.

| dataset | n | pipeline | BA | median ECE | 95% CI | Brier | log loss |
|---|---|---|---|---|---|---|---|
| BCI-2b | 108 | none | 0.7046 | 0.0989 | [0.0786, 0.1330] | 0.3842 | 0.5690 |
| BCI-2b | 108 | zero | 0.5831 | 0.3468 | [0.3391, 0.3815] | 0.7224 | 4.7724 |
| BCI-2b | 108 | mean | 0.7375 | 0.0987 | [0.0710, 0.1086] | 0.3437 | 0.5084 |
| SEED | 45 | none | 0.4591 | 0.5467 | [0.5086, 0.5692] | 1.0781 | 14.8384 |
| SEED | 45 | zero | 0.3377 | 0.6716 | [0.6617, 0.6725] | 1.3355 | 18.4447 |
| SEED | 45 | mean | 0.7094 | 0.2404 | [0.2335, 0.3504] | 0.5769 | 7.8051 |
| grasp-and-lift | 336 | none | 0.7770 | 0.1802 | [0.1552, 0.2259] | 0.3641 | 1.1935 |
| grasp-and-lift | 336 | zero | 0.7484 | 0.2408 | [0.1941, 0.2476] | 0.4187 | 1.4418 |
| grasp-and-lift | 336 | mean | 0.7815 | 0.1671 | [0.1494, 0.2201] | 0.3545 | 1.1277 |

Because the pipelines are evaluated on the same subjects we also report the paired difference per subject. The one-sided minus uncorrected difference is +0.254 [+0.229, +0.282] on BCI-2b, +0.129 [+0.098, +0.160] on SEED and +0.030 [+0.013, +0.047] on grasp-and-lift: the one-sided pipeline is worse on all three. The two-sided minus uncorrected difference is −0.014 [−0.036, +0.006] on BCI-2b, which is a tie, −0.251 [−0.296, −0.205] on SEED and −0.006 [−0.010, −0.002] on grasp-and-lift. The correction therefore restores the calibration that the one-sided pipeline destroys on BCI-2b, improves on doing nothing on SEED, and does little on grasp-and-lift.

### 4.8 Collapse, and the difference between chance and collapse

The identity of Section 2.5 is exact by construction: on all 845 cells it agrees with the observed collapse — every prediction equal — in 124 of 124 collapsing cells and 721 of 721 non-collapsing cells. Its substantive use is that it separates collapse from chance-level accuracy. Of the 845 cells, 180 report balanced accuracy exactly 1/K after the one-sided pipeline and only 124 have collapsed; the difference is concentrated in the imbalanced dataset (NER2015: 66 cells at chance, 16 collapsed). A target whose class priors are 0.17 and 0.83 can reach a balanced accuracy of 0.5 without returning a single class.

### 4.9 What is left

After the correction a difference from the within-session reference remains. We call it the *observed cross-protocol difference*: the reference differs from the cross-session model in training-set size and in evaluation protocol, and it is not a ceiling — on BCI-2a the corrected pipeline (0.6119) is above it (0.5355), so the difference cannot be read as an information gap nor as a bound on what a label-free method could recover: 0.0198 on BCI-2b, 0.0770 on SEED, 0.0257 on NER2015 and 0.0294 on grasp-and-lift. It is not an origin effect: across all 845 cells the correlation between z_T and the residual is +0.06, and within datasets it has no consistent sign. The residual is weakly associated with the class-conditional offset h_k of Equation (5) in units of the score spread: +0.21 on BCI-2a, −0.36 on BCI-2b, +0.33 on SEED, +0.30 on NER2015, +0.55 on grasp-and-lift (pooled +0.26, four of five in the same direction). The correlation is descriptive: the class-conditional offset is computed with the target labels and so is the residual, and we do not read it as a causal decomposition. A change of the within-session covariance explains less (pooled +0.10).

### 4.10 Implementation details and the invariance checks

**The invariances of the statistic.** With the scale taken from the centred scores, z_w is invariant to (i) adding a class-common linear term to all scores, (ii) adding a constant to all scores, and (iii) translating the features in the null space of P W. We verified (i) to 4.4 × 10⁻¹⁶, and (ii) and (iii) to 1.4 × 10⁻¹⁴ and 2.5 × 10⁻¹³ over 60 cells. Taking the scale from the uncentred scores instead breaks (i) and can change the statistic on a decision-equivalent classifier; that convention is not used anywhere in the paper.

**The mean/dbl identity.** Exact for every fit with an unpenalised intercept; verified on all 845 cells.

**The z-score/none agreement.** 100.0 per cent on BCI-2a, BCI-2b and grasp-and-lift with Ledoit-Wolf shrinkage, 51.8 per cent with shrinkage set to zero on grasp-and-lift, where the 256-dimensional covariance is rank-deficient. The agreement is empirical; a pipeline that relies on standardisation for equivariance should verify it.

**Six properties are checked by an executable test.** `tests_properties.py` asserts, on a real cell of BCI-2b, that `mean` and `dbl` give identical predictions sample by sample; that `z-score` and `none` do; that the feature-space and score-space corrections agree to 1e-10; that z_w is invariant to a class-common score term to 1e-12; that the collapse identity is consistent with the observed collapse; and that the causal mean at trial t is unchanged when every later trial is replaced by noise. All six pass, and the script prints one line per property.

**The held-out dataset.** SEED-IV was converted from the distributed features with the session labels in its ReadMe, cached per session, and evaluated with the models and thresholds fixed beforehand. No parameter was tuned on it.

### 4.11 A small audit of released preprocessing components

The paper's practical premise is that a pipeline can be built with a reference
that is fixed at prediction time. We inspected the components of three widely
used frameworks that a cross-session pipeline actually uses, and recorded which
data each one takes its reference from.

**Table 11.**  What the inspected components centre on. Quoted lines are from the
public sources; the audit is small and reported as such (`results/code_audit.txt`
in the archive).

| component | what it does | reference taken from | exposed at prediction time? |
|---|---|---|---|
| MOABB cross-session example [18] | `CrossSessionEvaluation` with CSP+LDA and tangent-space+logistic pipelines | every transform is fitted inside the training fold | no |
| MNE `Scaler` [mne/decoding/transformer.py] | stores a scaling estimated on the data given to `fit` (a fixed per-channel-type scaling by default, a fitted `StandardScaler` in the `scalings='mean'` mode) and applies it in `transform` | the data passed to `fit`, i.e. the training fold | no |
| Braindecode `exponential_moving_demean` [braindecode/preprocessing/preprocess.py] | causal exponential moving average, initialised from the first block of each trial | the signal up to the current sample | no, if the running window covers the session offset |

None of the three centres the target session at prediction time, and all three
therefore satisfy the invariance of Proposition 1 by construction: the reference
is the training fold, or a causal running mean that sees the session offset as
part of the signal. The failure mode audited in this paper is consequently not
present in the framework components we inspected; it belongs to code that
patches a normalisation step onto features at prediction time, outside the fold.
We did not audit that population, and the audit above is too small to estimate
its size.

## 5. The verification procedure

The results reduce to a procedure with three measurements, one correction and one test.

**Measure the origin distance of the feature family.** z_w of Equation (2) needs only the training session: the fitted weights, the source mean and the centred score spread. In our units, below z_w = 0.35 the penalty of the one-sided form is between +0.024 and −0.015; above z_w = 4 it is between −0.03 and −0.19. These are the ranges observed on the eleven development units, not thresholds; the held-out test shows that a value computed this way does not transfer as an operating rule.

**Correct both sides and fit on the centred training data.** This makes the pipeline equivariant (Proposition 1). Standardising with training statistics also makes it equivariant but does not implement the two-sided correction; a pipeline that standardises and then centres either way obtains the two-sided result. If the model is frozen, subtract w_k'(μB − μA) from score k instead.

**Check the collapse identity before believing an accuracy.** If all target predictions are equal the classifier has collapsed, and its balanced accuracy is 1/K by identity.

**The invariance test.** Translate every feature by a constant, refit, and check that the predictions are unchanged. The test is one line of code and needs no labels. It has two blind spots that follow from Proposition 3: a translation in the null space of P W changes nothing, and a target sample that does not cross the moved boundary changes no label. The test is therefore a sufficient but not a necessary detector, and it should be run with a translation large relative to the score range; we use ten within-session standard deviations in the sweep of Section 4.2.

**Report the residual separately.** The correction recovers the origin component; the rest is an observed difference from the within-session reference, not an identified information gap, and reporting the two separately prevents a corrected pipeline from being credited with the whole difference.

## 6. Discussion

### 6.1 What the verification establishes, and what it does not

Three kinds of statement are mixed in a paper of this shape, and only the second is specific to EEG. The first is a corollary of linear discriminant theory: a constant added to a feature vector moves the intercept, the prediction-relevant content of a reference is its projection onto the weights, and score differences are unchanged by class-constant shifts. We prove these and do not claim them as discoveries. The second is an empirical regularity of cross-session EEG features: which feature families carry a free origin, how large the resulting damage is on six public datasets, how the damage depends on the classifier's threshold error, and in what ways a source-level statistic fails. The third is a change in practice: centre both sides, run the invariance test, and do not use a norm-based origin statistic. The paper's contribution is the second and the third; the first is the scaffolding, and we say so because a reader who expects a new algorithm should know what this is not.

### 6.2 Why some features are exposed and others are not

z_T is large when the feature carries a free additive constant. Log power has three: the logarithm of a reference power, a floor added before the logarithm, and a change of the reference electrode that adds an offset to the potential before a non-linear transform. Differential entropy inherits all three. A difference of two conditions measured within the same trial has none, which is why the time-domain contrast features of NER2015 have z_T = 0.20 and a penalty of 0.000. This is a statement about measurement conventions, not about neurophysiology: the origin is set by the amplifier, the montage and the code, and none of the three is reported in a typical methods section.

The electrical reading should not be pushed far. An amplifier gain change and a reference-electrode change both alter the covariance of the raw signal, and a reference change is not a pure translation of the feature vector; what is additive after a log transform is the magnitude of a gain change, not every consequence of a montage change.

### 6.3 Relation to alignment methods

A recent benchmark attributes the cross-session advantage of a tangent-space pipeline to its test-time recentering [20]. Our results accept the mechanism and qualify its availability: the recentering in that pipeline is transductive, and Section 4.2 shows that a causal version reproduces the gain from the fifth trial on BCI-2b and BCI-2a, only approaches it on SEED as the window grows, and on grasp-and-lift falls below not correcting at all. The mechanism is real; whether a deployment can have it is a separate question with a measured answer.

Euclidean and Riemannian alignment [5-8] act on second-order structure, and the Riemannian Gaussian–Laplace framework of [16] is a recent example of the same programme. An alignment matrix that is a multiple of the identity performs no alignment, so the first-order correction is not a special case of the second-order one, and Section 4.6 shows that the two compose in all four BCI representations. Where the two intersect is the label-shift problem of Section 2.4: aligning a covariance implicitly assumes that the class mixture is unchanged, and re-weighting the classes changes the average covariance in a way that alignment cannot distinguish from a change of state. Under the label-shift assumption the prior is estimable [12]; without it the same ambiguity applies to both families.

### 6.4 Limitations

**Prevalence is measured on three components, not on the field.** Section 4.11 audits the MOABB cross-session example, the MNE `Scaler` and the Braindecode causal demean; all three take their reference from the training fold or from a causal running mean, so none of them can exhibit the failure, and we put no number on the frequency of the mistake in custom code. The audit is small by design: it establishes that the failure is an implementation choice and not a property of the frameworks, and the invariance test of Section 5 is the instrument that would settle any particular codebase.

**The source-level statistic is not a screen.** It ranks feature families within the development data and fails at the dataset level (rho = −0.77, exact p = 0.103), on the held-out dataset (specificity 0.000) and within SEED (AUC 0.332). We report it because the quantity is the right first thing to compute, not because it decides.

**The displacement model has a measured range.** It is quantitative for mean-calibrated linear classifiers under the oracle parameterisation, less so under the parameterisation the Gaussian assumption implies, and not applicable to the margin-based classifier. We do not have a label-free estimator of t*, and the sign analysis therefore remains descriptive.

**The protocol is transductive.** Both forms of the correction use the whole target session to estimate μB. That is legitimate under a protocol that allows unlabelled target data and is not available in a strictly inductive deployment. The causal experiment of Section 4.2 maps the limit: a cumulative estimate recovers the transductive gain on BCI-2b, BCI-2a and SEED, loses 0.115 on grasp-and-lift because the mean drifts within the session, and the shrunk estimator of Equation (9) is the only one that stays non-negative on all five datasets. A causal reference does not remove the need for calibration; it changes what a calibration failure looks like.

**The statistics are hierarchical.** The 845 cells come from 61 subjects and 737 distinct session pairs; subject-level aggregation and the cluster bootstrap are used where they matter, and cell-level correlations are labelled descriptive. The dataset-level tests rest on five or six observations and have little power.

## 7. Conclusion

The two centrings are different operations. The two-sided form is invariant to the coordinate origin, the invariant family is wider than the sample mean, and two corrections leave every score difference unchanged exactly when their projections onto the centred weights agree. The failure of the one-sided form is a threshold displacement; its sign is set by the threshold error the training session already carries, and across five development datasets the resulting damage ranges from nothing on time-domain contrast features to a collapse to chance on log-power and differential-entropy features with a large free origin; a sixth dataset, held out, behaves as the family it belongs to.

What the comparison adds to a textbook statement is a measured boundary. The correction is exact for its own component, it composes with second-order alignment, it can be transported to the decision space of a frozen model, and it restores neither the observed cross-protocol difference nor a calibration that the wrong convention destroyed. A source-only statistic computed before the target session exists ranks feature families but does not screen sessions, and we report that as the open problem this audit leaves.

## CRediT authorship contribution statement

**Zihao Gong:** Conceptualization, Methodology, Software, Formal analysis, Investigation, Writing – original draft, Visualization. **Jiran Li:** Conceptualization, Methodology, Validation, Writing – review & editing. **Ke Huo:** Software, Data curation, Investigation. **Yubin Han:** Formal analysis, Validation, Visualization. **Guangyu Shi:** Data curation, Resources, Validation. **Yongqiang Xie:** Conceptualization, Supervision, Writing – review & editing, Project administration.

## Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Data availability

BCI Competition IV datasets 2a and 2b are available from the competition organisers. SEED and SEED-IV are available from the BCMI Laboratory, Shanghai Jiao Tong University, on request for academic use; the present study used the differential-entropy features distributed with those releases, unmodified. NER2015 and grasp-and-lift are Kaggle competition datasets and are publicly available. The analysis code, the feature-cache schema and the plain-text output of every number reported in this paper are archived at https://github.com/gzhgzy1234567890-lang/EEG-BSPC/tree/main/origin_equivariance (analysis commit b588c1c4b6), which is the version of record for the code.

## Acknowledgements

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

## References

[1] M. Krauledat, M. Tangermann, B. Blankertz, K.-R. Müller, Towards zero training for brain-computer interfacing, PLoS ONE 3 (2008) e2967.

[2] F. Lotte, Signal processing approaches to minimize or suppress calibration time in oscillatory activity-based brain-computer interfaces, Proc. IEEE 103 (2015) 871–890.

[3] C. Vidaurre, C. Sannelli, K.-R. Müller, B. Blankertz, Machine-learning-based coadaptive calibration for brain-computer interfaces, Neural Comput. 23 (2011) 791–816.

[4] R. Apicella, F. Isgrò, A. Pollastro, R. Prevete, On the effects of data normalization on EEG-based BCI classification, Eng. Appl. Artif. Intell. 123 (2023) 106205.

[5] M. Congedo, A. Barachant, R. Bhatia, Riemannian geometry for EEG-based brain-computer interfaces: a primer and a review, Brain-Comput. Interfaces 4 (2017) 155–174.

[6] H. He, D. Wu, Transfer learning for brain-computer interfaces: a Euclidean space data alignment approach, IEEE Trans. Biomed. Eng. 67 (2020) 399–410.

[7] F. Yger, M. Berar, F. Lotte, Riemannian approaches in brain-computer interfaces: a review, IEEE Trans. Neural Syst. Rehabil. Eng. 25 (2017) 1753–1762.

[8] P. Zanini, M. Congedo, C. Jutten, S. Said, Y. Berthoumieu, Transfer learning: a Riemannian geometry framework with applications to brain-computer interfaces, IEEE Trans. Biomed. Eng. 65 (2018) 1107–1116.

[9] W. Samek, K.-R. Müller, M. Kawanabe, C. Vidaurre, Brain-computer interfacing in discriminative and stationary subspaces, in: Proc. IEEE EMBS, 2012, pp. 2873–2876.

[10] B. Blankertz, M. Kawanabe, R. Tomioka, F. U. Hohlefeld, V. V. Nikulin, K.-R. Müller, Invariant common spatial patterns: alleviating nonstationarities in brain-computer interfacing, in: Adv. Neural Inf. Process. Syst. 20, 2008, pp. 113–120.

[11] O. Ledoit, M. Wolf, A well-conditioned estimator for large-dimensional covariance matrices, J. Multivar. Anal. 88 (2004) 365–411.

[12] M. Saerens, P. Latinne, C. Decaestecker, Adjusting the outputs of a classifier to new a priori probabilities: a simple procedure, Neural Comput. 14 (2002) 21–41.

[13] M. Tangermann, K.-R. Müller, A. Aertsen, et al., Review of the BCI competition IV, Front. Neurosci. 6 (2012) 55.

[14] W.-L. Zheng, B.-L. Lu, Investigating critical frequency bands and channels for EEG-based emotion recognition with deep neural networks, IEEE Trans. Auton. Ment. Dev. 7 (2015) 162–175.

[15] R.-N. Duan, J.-Y. Zhu, B.-L. Lu, Differential entropy feature for EEG-based emotion classification, in: Proc. 6th Int. IEEE/EMBS Conf. Neural Eng., 2013, pp. 81–84.

[16] M. Congedo, A. Barachant, A. Andreev, A Riemannian Gauss–Laplace distribution on the manifold of symmetric positive definite matrices, with application to anomaly detection and clustering, arXiv:2306.10543 (2023).

[17] F. Lotte, L. Bougrain, A. Cichocki, M. Clerc, M. Congedo, A. Rakotomamonjy, F. Yger, A review of classification algorithms for EEG-based brain-computer interfaces: a 10 year update, J. Neural Eng. 15 (2018) 031005.

[18] MOABB developers, Cross-session motor imagery example (CSP+LDA and Riemannian geometry + logistic regression, leave-one-session-out), NeuroTechX/moabb, 2024. https://github.com/NeuroTechX/moabb

[19] W.-L. Zheng, W. Liu, Y. Lu, B.-L. Lu, A. Cichocki, EmotionMeter: a multimodal framework for recognizing human emotions, IEEE Trans. Cybern. 49 (2019) 1110–1122.

[20] M. Rahimipour, M. M. Van Hulle, Simple geometric recentering rivals deep sequence models for cross-session EEG motor-imagery decoding, bioRxiv (2026) 2026.07.07.736991, version 1, posted 11 July 2026, accessed 28 October 2026. https://doi.org/10.64898/2026.07.07.736991

## Figure captions

**Fig. 1.** (a) Change in balanced accuracy of the one-sided pipeline as a function of z_T, one curve per dataset; (b) the fraction of cells that land on exactly 1/K; (c) the largest change of the two equivariant pipelines over the whole sweep, on a logarithmic axis whose floor is 10⁻¹⁶, so that a zero is drawn at the floor rather than as a measured value.

**Fig. 2.** (a) Unit medians of the source-only statistic against the penalty of the one-sided pipeline, with the held-out SEED-IV point shown as a star; (b) the same relation over the development cells. The four `euc_ea` and `tan` units are target-informed (Section 3); the source-only correlations quoted in the text are computed without them.

**Fig. 3.** (a) Balanced accuracy of the three pipelines by dataset; (b) the gain of the two-sided over the uncorrected pipeline, one point per subject.

**Fig. 4.** (a) Predicted change of Equation (4) against the observed change, one cell per point, LDA, the 800 binary cells; (b) distribution of the prediction error.
