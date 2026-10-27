# Mean correction in cross-session EEG decoding: equivariance, failure mechanism, and boundaries

Zihao Gong ^a,†^, Jiran Li ^b,†^, Ke Huo ^a^, Yubin Han ^c^, Guangyu Shi ^a^, Yongqiang Xie ^a,*^

^a^ School of Mechano-Electronic Engineering, Xidian University, Xi'an 710071, China

^b^ School of Humanities and Social Sciences, Beijing Forestry University, Beijing 100083, China

^c^ School of Life Science and Technology, Xidian University, Xi'an 710071, China

† These authors contributed equally to this work.

E-mail addresses: andy.zihao.gong@gmail.com (Z. Gong), dsx54188dsx@163.com (J. Li), huoke@stu.xidian.edu.cn (K. Huo), 2044037857@qq.com (Y. Han), 2793218576@qq.com (G. Shi), yqxie@xidian.edu.cn (Y. Xie, corresponding author).

## Abstract

Removing a session mean is the first step in cross-session EEG decoding, and two operations circulate under that description: centring both sessions, or centring one. We ask what the choice is and what it can buy. Equivariance: a correction is invariant to the coordinate origin if it translates by a translation-equivariant estimate of the target mean; this family contains more than the sample mean, and we do not claim uniqueness. Score-difference equivalence: two corrections shift every class score by the same amount exactly when their references differ by a vector whose projection onto the centred classifier weights vanishes. Performance: the failure of the one-sided form is a threshold displacement, so its sign is set by the threshold error the training session already carries.

On 845 cells from five datasets an origin sweep leaves the equivariant pipelines unchanged by 0.000 in balanced accuracy and drives the one-sided one to exact chance; 90 further cells from SEED-IV, opened after all choices were fixed, serve as a held-out test. A Gaussian model of the displacement explains the sign of the change for mean-calibrated linear classifiers under one parameterisation but not the magnitude under the parameterisation the model itself requires; we report both. A source-only statistic of the exposure of a feature family is defined so that it is invariant to decision-equivalent score representations, and with that definition its cross-dataset association (rho = −0.77, exact p = 0.10) and its held-out operating point (specificity 0.000) do not support screening. We report it as exploratory, not as a contribution.
**Keywords:** cross-session EEG decoding; feature centring; origin equivariance; calibration; decision threshold; reproducibility

---


## 1. Introduction

A classifier trained on one recording session and applied to another usually loses accuracy, and the first step in most cross-session pipelines is to remove a mean. The step is described as re-centring, mean removal, per-session normalisation or baseline correction, and it appears in pipelines that are otherwise unlike each other and inside calibration protocols [1-3]. It is also described ambiguously, because two operations share the name.

*Two-sided centring.* Centre the training session on its own mean, fit the classifier on the centred data, and centre the target session on its own mean before predicting.

*One-sided centring.* Centre one session and not the other. There are two forms, centring only the target or only the training session, and they fail in opposite directions.

This paper is deliberately narrower than a claim that one convention is the right way to build a decoder. It asks three questions and answers each with the weakest statement the evidence supports.

**Equivariance.** Which corrections are invariant to a translation of the feature origin, and does that invariance single one out? Proposition 1 shows that the two-sided form is invariant. Proposition 2 shows that the invariant family is larger than the sample mean: any reference of the form μ + h(X − μ) with h translation-invariant is also invariant, so equivariance alone does not determine the correction. What distinguishes the sample mean is that it is the member of the family that adds no data-dependent offset; this is a parsimony argument, not a uniqueness theorem, and earlier versions of this work overstated it.

**Prediction equivalence.** When do two corrections give the same predictions? Proposition 3 states the exact condition: the projections of the two references onto the *centred* classifier weights must agree, that is P W(γ − γ') = 0 with P the centring projector. For a finite sample the condition is sufficient for identical labels but not necessary, since the samples may not cross the boundary that moves. The distinction matters because the paper's practical recommendations are about the finite-sample case.

**Performance.** Does the correction improve accuracy? Sometimes it does not, and the sign is not governed by the size of the displacement: it is governed by where the training threshold already sits relative to the target optimum. Section 2.3 gives a signed law in which the damage is the change in a Gaussian balanced-accuracy function, and Section 4.5 verifies its sign in the settings listed in Table 7. No claim of statistical optimality is made anywhere in the paper.

The empirical part has three components. A controlled origin sweep, run on all 845 cells, shows that the equivariant pipelines are unchanged to 0.0e+00 while the one-sided pipeline slides to exact chance. A direction-controlled version of the same experiment shows that the source-only risk statistic we propose is *direction-blind*: an origin of a given norm produces the same statistic whether it lies along the classifier's weights or orthogonal to them, and only the parallel one damages the decoder. We report this as a limitation of the statistic and use it as a proxy rather than a law. Finally, the classifier dependence that an earlier version reported as uncomfortable is explained by the signed law: a strongly regularised support-vector machine has almost no threshold error to displace, so centring can help it, and the sign of the effect is predicted.

**What this paper does not claim.** We do not claim that one-sided centring is common in practice; we audited one published example (Section 6.4) and found it correct by construction, and we put no number on the frequency of the mistake. We do not claim that the correction is optimal, unique, or that elaborations of it are unnecessary as a matter of principle; we report what five specific elaborations do. We do not claim that the collapse certificate predicts collapse before the target data arrive; it is an algebraic identity and we present it as a diagnostic. We do not claim that the source-only statistic is a general risk law; Section 4.4 shows the counter-example and the limits.

**Relation to prior work.** Apicella et al. [4] compared normalisation schemes with domain-adaptation methods on three EEG datasets and found that an appropriate normalisation often outperforms the adaptation algorithm; our results are compatible and add a criterion, the invariance of the output to the coordinate origin. The nearest formal relatives are the Euclidean and Riemannian alignment families [5-8], which act on second-order structure; an alignment matrix that happens to be a multiple of the identity performs no alignment, so the first-order correction studied here is not a special case of the second-order one, and Section 4.6 shows that the two compose. Methods that remove session-specific directions [9,10] estimate a subspace in which the sessions agree rather than relocating a boundary by a constant. Calibrating a classifier to a new session by re-estimating an intercept from a few labelled trials [1,2] is the procedure onto which our analysis of label use maps; on four of five datasets it changes nothing relative to the label-free form, and on the fifth it gains 0.013 (Section 4.6).

## 2. Theory

### 2.1 Notation and the pipelines

Let A denote the training session with features X_A and labels y_A, and B the target session with features X_B and labels y_B, the latter used only for evaluation. Write μA = mean(X_A), μB = mean(X_B), and s_A for the elementwise standard deviation of X_A. A linear classifier fitted on A gives scores

    s_k(x) = w_k'x + b_k ,   k = 1 ... K ,                                   (1)

with prediction argmax_k s_k(x). Let W be the K × D matrix whose rows are w_k, and P = I_K − 11'/K the projector that removes the class mean of a K-vector. Linear discriminant analysis with Ledoit-Wolf shrinkage [11] is the primary classifier; Section 4.5 also uses logistic regression and a linear support-vector machine.

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

**Proposition 1 (equivariance).** Under the translation T_c : x ↦ x + c applied to all data with the classifier refitted, the `mean` and `dbl` pipelines return predictions identical to those they returned before the translation, for every c, provided the fit has an unpenalised intercept.

*Proof for `mean`.* The fit receives X_A + c; with an unpenalised intercept the weights are unchanged and the intercepts become b_k − w_k'c. The candidate features become (x + c) − (μB + c) + (μA + c) = (x − μB + μA) + c, whose scores are w_k'[(x − μB + μA) + c] + b_k − w_k'c, the scores the candidates received before the translation. The argmax is unchanged. For `dbl` both the training and candidate features are unchanged, so no assumption on the fit is needed. For `none` the same cancellation occurs on both sides. QED

**Proposition 2 (the equivariant family).** Let a correction be x ↦ x − γ(X). It is equivariant, i.e. γ(X + c1) = γ(X) + c1 for every c, if and only if γ(X) = μ(X) + h(X − μ(X)) for some h that is itself translation-invariant. The family therefore contains more than the sample mean.

*Proof.* Write γ(X) = μ(X) + [γ(X) − μ(X)] and note that μ(X + c1) = μ(X) + c. Equivariance holds iff the bracket is unchanged by translation, i.e. iff it is a function of the centred sample only. QED

Two comments. First, a reference of the form μ + a with a fixed vector a is equivariant and is *not* the sample-mean correction; the two differ by a in score space, and unless Wa is class-constant they give different predictions. Equivariance alone therefore does not single out the sample mean, and no uniqueness is claimed. What can be said is that h = 0 is the only member of the family that adds no data-dependent offset beyond the sample mean; any other h must be justified by something other than invariance. Second, Proposition 1 needs the unpenalised intercept; we check it numerically (Section 4.1) rather than relying on the argument.

**Proposition 3 (score-difference equivalence).** The score differences s_j − s_k are identical for every input x and every pair (j,k) if and only if W(γ − γ') is a class-constant vector, equivalently P W(γ − γ') = 0.

*Proof.* The score of x under reference γ is s_k(x − γ) = s_k(x) − w_k'γ. The difference between the two corrections is w_k'(γ − γ'), independent of x. Adding a vector v to all class scores leaves the argmax unchanged for every score vector iff v is class-constant; hence the condition. QED

Two caveats. First, identical score differences are sufficient for identical predictions on every input but not necessary: a class whose score is dominated everywhere by another class can be shifted without changing any decision, so the label-equivalence class is strictly larger than the score-difference class. Second, for a finite target sample the condition is again sufficient but not necessary, because no sample may cross the boundary that moves. We therefore state the proposition for score differences and treat prediction agreement as a corollary, which is all the paper uses. Section 4.6 reports the exact condition and the observed agreement, which is 100.0 per cent for the projected correction because that correction lies in the null space.

**Proposition 4 (rank preservation).** For any two samples x, x' and any two classes j, k, the comparison s_j(x) − s_k(x) versus s_j(x') − s_k(x') is unchanged by any of the six pipelines, because the added constants are identical for x and x'. Consequently threshold-free ranking measures are unchanged. This holds for a *fixed* model; for a refitted or standardised pipeline the scores are recomputed and the statement does not apply, which is why we report accuracy and calibration rather than AUC as the quantities of interest.

### 2.3 The displacement, its size, and its sign

**The displacement.** For a binary classifier define

    ρ = | w' μ_B | / σ_s ,   σ_s = sd of the source scores,                    (2)

and for K classes ρ = ||P W μ_B|| / (√K σ_s), so that the class-constant part, which cannot change a prediction, is removed. ρ is the size of the threshold shift that the one-sided pipeline applies, in units of the score spread; it needs the target features but no target labels.

**The source-only screen.** The origin distance that a pipeline can compute before it sees a target session should be the projection of the source mean onto the classifier's own direction, not its norm:

    z_w = || P W μ_A || / (√K σ_s) ,   σ_s = SD of the source scores.           (2b)

z_w uses only the source session — the fitted weights and the source mean — and it is invariant to a translation of the features orthogonal to W by construction, which is exactly the failure mode of a norm-based statistic (Section 4.3). The binary reduction is exact and contains no ||w||: with W = [w'; −w'] one has P W μ = [w'μ; −w'μ], so ||P W μ|| = √2 |w'μ| and, since √K = √2, z_w = |w'μ_A|/σ_s. (An earlier version wrote |w'μ_A|/(||w|| σ_s); that was wrong, and the code has always used the correct expression — we verified the agreement to 4 × 10⁻¹⁴ across 200 cells.) The quantity σ_s is the standard deviation of the source decision values s(x) = w'x + b, pooled over classes and samples; for K > 2 it is the vector of per-column standard deviations of the score matrix, divided elementwise.

Four quantities are used below, and they differ in what they need. The *origin distance* z_T = ‖μ_A‖/‖sd_A‖ uses the source features only and is direction-blind (Section 4.3). The *projected screen*

    z_w = ‖ D_σ⁻¹ P W μ_A ‖ / √K ,   D_σ = diag(σ_1, …, σ_K),             (2)

uses the source features and the fitted weights, and the *displacement* ρ is the same expression with μ_B in place of μ_A, i.e. it uses the target features and carries the mechanism; its signed binary counterpart is s = w'μ_A/σ_s.

Equation (2) is the definition, and it needs four comments. The scalar form |w'μ_A|/σ_s used later is its binary special case, valid when K = 2 or when all σ_k are equal.

*The scale comes from the centred scores.* Taking σ_k from the raw score columns is not admissible: adding a class-common linear term a'x to every score leaves all predictions unchanged but changes the per-class raw score spreads, so z_w could be inflated by 49 per cent without any change of classifier (W = [1; −1] with a'x = 0.5x gives W' = [1.5; −0.5] and the same score difference 2x). With σ_k taken from the columns of P S — the centred scores — both the numerator and the scale are invariant, because P(W + 1a') = PW and P(S + a'x) = P S. We verified the invariance numerically under that transformation: |Δz_w| = 4.4 × 10⁻¹⁶ (Section 4.10). Every number in Section 4.4 uses this definition; the code computes σ_k from the centred scores. First, σ_k is the standard deviation of the k-th column of the *source* score matrix S — computed before any centring, which is the convention the code implements and the one we verified. Centring the scores first and then taking the standard deviations gives a different quantity, by as much as 24 in our data (Section 4.10), so the two conventions are not interchangeable; we use the uncentred one throughout and say so. Second, the statistic has the invariances it is supposed to have and *not* the one it is not: an offset applied to all class scores changes no σ_k and cancels in P W μ_A, and a feature translation in the null space of P W leaves the numerator unchanged, so z_w is insensitive to decision-null translations; it is *not* invariant to a translation along the discriminating directions, which is the point of the statistic. We checked both numerically: the largest change over 60 cells is 1.4 × 10⁻¹⁴ for the score offset and 2.5 × 10⁻¹³ for the null-space translation (Section 4.10). The binary reduction is exact: with W = [w'; −w'], P W μ = [w'μ; −w'μ], ‖P W μ‖ = √2|w'μ| and σ_1 = σ_2 = sd(s), so √K = √2 gives z_w = |w'μ_A|/sd(s).

**The size.** If the class-conditional scores of the aligned target were Gaussian with equal variance and the training threshold were optimal, the balanced accuracy at a threshold displaced by u score-standard-deviations would be

    BA(c, u) = ½ [ Φ(c + u) + Φ(c − u) ] ,   c = Φ⁻¹(BA_aligned) .             (3)

At u = 0 this is Φ(c), and for small u it falls as ½ c φ(c) u². The coefficient c φ(c) is not monotone: it increases up to c = 1 (aligned balanced accuracy 0.84) and decreases beyond. An earlier version of this work wrote that "a better decoder is more exposed"; that is true only below c = 1, and we correct it here. The largest sensitivity is at balanced accuracy ≈ 0.84, and a decoder at 0.99 is again insensitive because the boundary has to move a long way to cross any sample.

**The sign.** Equation (3) is written around the *optimal* threshold, and the one-sided pipeline does not start there. Let s = w'μ_A / σ_s be the extra displacement that the one-sided pipeline applies relative to the two-sided one, and let t* be the displacement of the aligned threshold from the optimal one, both signed and measured in σ_s. Then the damage of the one-sided relative to the two-sided pipeline is

    Δ = BA(c, t* − s) − BA(c, t*) ,                                           (4)

which is negative when the displacement moves the threshold away from the optimum and positive when it moves it closer. The two displacements are different quantities — ρ uses μ_B and measures the zero-versus-none shift, while s uses μ_A and measures the zero-versus-mean shift — and neither is signed, so neither alone can determine this sign; the sign is carried by t*. Equation (4) is a one-line consequence of the Gaussian model and is tested in Section 4.5, where it predicts the sign in the settings listed in Table 7.

### 2.4 What cannot be repaired

Write m_kB = m_kA + ḡ + h_k where ḡ = Σ_k π_kB (m_kB − m_kA) is the *prior-weighted* class-conditional offset, so that Σ_k π_kB h_k = 0 by construction. Then

    μ_B − μ_A = ḡ + Σ_k (π_kB − π_kA) m_kA .                                   (5)

The second term is the change in the mixture of the source class means; it is present even when nothing about the class-conditional distributions changes. Under the constraint the h_k do not enter the mean at all — they enter the class-conditional placement, which is where the residual of Section 4.9 comes from. Subtracting μB − μA therefore removes two things at once: the prior-weighted class-conditional offset and the prior-induced mixture term. On a balanced design the second term vanishes; when the priors change it does not.

The identifiability statement must be made under assumptions. If the class-conditional distributions are unchanged, p_B(x | y) = p_A(x | y), the target priors are identifiable from unlabelled target data and can be estimated by the EM procedure of Saerens et al. [12]. Without that assumption, a prior change and a class-conditional offset are confounded: both act on the first two moments of the mixture, and no label-free method separates them. What the correction can recover is therefore the part of the offset that is common across classes; the rest requires either labels or the label-shift assumption, and Section 4.6 shows the size of the gain when labels are used (0.013 on the one dataset whose priors change substantially, and nothing on the four balanced ones).

### 2.5 The collapse identity

After `zero` centring the classifier returns a single class c for every target sample if and only if, for every k ≠ c,

    w_k'μB − w_c'μB  >  max_x [ s_k(x) − s_c(x) ] .                            (6)

This is an identity: it rewrites argmax_k s_k(x − μB) = c for all x. We state it because it is useful operationally — it can be checked from the fitted weights, the target mean and the target scores, before any label — and because it distinguishes collapse from chance-level accuracy, two events that a balanced-accuracy threshold conflates (Section 4.8). It is *not* a predictive method: the simplest label-free check of collapse is to count the distinct predicted classes, and the identity adds no information beyond the scores it is computed from. We do not claim it as a validated detector, and it is not one of the paper's main contributions.

## 3. Data and protocol

**Datasets.** Five public datasets, chosen to differ in class count, channel count, feature type, session structure and — crucially — in whether the electrode cap was removed between sessions.

*BCI Competition IV 2a* [13]: four motor-imagery classes, 22 channels, 250 Hz, nine subjects, two sessions on different days; features from the 2.0–6.0 s window after trial onset, band-passed 8–30 Hz, in four representations.

*BCI Competition IV 2b* [13]: two classes, three channels (C3, Cz, C4), nine subjects. Five sessions are distributed; three are retained per subject (the screening sessions 01T and 02T and the feedback session 03T), and every chronologically ordered pair among the retained sessions contributes one cell, 27 pairs over nine subjects. The three pair types do not contribute equally to a possible feedback confound, so we report both levels and the gain for each: 1→2 (screening only) 0.6461 → 0.6769, gain +0.0308; 1→3 0.7430 → 0.7677, +0.0247; 2→3 0.7247 → 0.7680, +0.0433. The gains are of the same size across the three types, and the differences in level reflect how well each session decodes in the first place; the effect is not carried by the sessions that introduce feedback.

*SEED* [14,15]: three emotion classes, 62 channels, 15 subjects, three sessions on different days; the distributed 1 s differential-entropy features, 3394 segments per session in 15 film-defined blocks. The reference uses `StratifiedGroupKFold` with the film as group, because adjacent segments of one film are not independent; the *target mean* used by the correction is computed over all 3394 segments of the session, without any grouping, since it is a first moment and not an estimate of generalisation. The same films appear in different sessions, so a film-level dependence remains in the sense that the two sessions share stimuli; we do not model it and report SEED's screening result (Section 4.4) as the failure case it is.

*NER2015*: sixteen subjects, five sessions on different days with the cap re-applied, two classes (correct versus error feedback) whose priors vary from 0.17 to 0.73 across sessions; 56 channels, eight windows, time-domain mean features. Both directions of every pair are used, 16 × 20 = 320 cells, because the two directions are not equivalent under a translation: they have different μB.

*Grasp-and-lift*: twelve subjects, eight series recorded within one session with the cap left in place, two classes, 32 channels, eight windows of log power; 12 × 28 = 336 unordered pairs. This is the same-cap control.

**Table 2.** The datasets, with the number of cells and the number of sessions actually used. The last column is the origin distance of Equation (7), computed on the source session only, median over cells.

| dataset | classes | subjects | sessions used | representations | cells | median z_T |
|---|---|---|---|---|---|---|
| BCI-IV-2a | 4 | 9 | 18 | 4 | 36 | 0.50 |
| BCI-IV-2b | 2 | 9 | 27 | 4 | 108 | 16.1 |
| SEED | 3 | 15 | 45 | 1 | 45 | 34.2 |
| NER2015 | 2 | 16 | 80 | 1 | 320 | 0.20 |
| grasp-and-lift | 2 | 12 | 12 | 1 | 336 | 0.25 |
| SEED-IV (held out) | 4 | 15 | 45 | 1 | 90 | 56.3 |

*SEED-IV* [19] is used **only as a held-out test**: the statistic, its thresholds and the classifier were fixed in earlier rounds, and SEED-IV was opened after them. It contributes 15 subjects, 4 classes, three sessions and 6 ordered pairs per subject, 90 cells, from the distributed 1 s differential-entropy features (62 channels × 5 bands).

The analyses do not all cover the same cells, and no claim borrows the sample size of another: the main levels, the origin sweep and the direction control use the 845 development cells; the per-cell displacement analysis uses the 800 binary cells of the four binary datasets (for BCI-2a, the two-class subproblem of classes 1 and 2, not the four-class problem); the screening analysis uses the 845 development cells and the six dataset observations; and the external test fixes its threshold on the 845 and evaluates on the 90 held-out cells.

A *cell* is one (dataset, representation, subject, ordered session pair) combination. The five development datasets give 36 + 108 + 45 + 320 + 336 = 845 cells and the held-out dataset adds 90, for 935 in total; the 845 are the only cells used for the main analyses and the sweep (Table 3). They come from 76 subject units (9 + 9 + 15 + 16 + 12 + 15) and 227 session units (18 + 27 + 45 + 80 + 12 + 45).

**Sub-sampling, where it is used.** Three analyses use a uniform subsample of the cells of a dataset to bound computation: the classifier sweeps of Section 4.5 on grasp-and-lift and NER2015 (60 cells of 336 and 320, chosen at equally spaced indices), and the direction experiment of Section 4.4 (60 cells in each of two datasets). Every other number in the paper uses all cells of the dataset, including the calibration analysis, which an earlier draft ran on 60 cells and now runs on all of them (Section 4.7).

**Representations.** For 2a and 2b: Euclidean log-power (`euc`), Euclidean alignment followed by log-power (`euc_ea`), Riemannian tangent space (`tan`) and CSP log-variance (`csp`). For SEED the distributed feature; for NER2015 the time-domain mean over eight windows; for grasp-and-lift the log power over eight windows. A representation is fitted on the training session unless its definition requires statistics from both; Section 4.6 states which.

**Classifiers.** Linear discriminant analysis with Ledoit-Wolf shrinkage [11], logistic regression and a linear support-vector machine [17].

**Reference.** The within-session reference is cross-validation inside the target session using its own labels: stratified 5-fold for 2a, 2b, NER2015 and grasp-and-lift, `StratifiedGroupKFold` over films for SEED. It is not a ceiling and it differs from the cross-session classifier in training-set size as well as in session; on 2a it falls below the cross-session accuracy for two of four representations. We report it descriptively.

**Statistics.** Cells are aggregated per subject first, then tested across subjects with a two-sided Wilcoxon signed-rank test, with a subject-level bootstrap of the median (10,000 resamples) and Cohen's dz. For the screen, the primary analysis is at the level of the five datasets; the eleven dataset-by-representation units are reported with a cluster bootstrap that resamples *datasets*, not units, because eight of the eleven units come from two datasets and share subjects and recordings. We do not treat the 845 cells as independent anywhere.

## 4. Results

### 4.1 The two descriptions are one pipeline; standardisation is a different question

Fitting on X_A − μA and applying to X_B − μB, versus fitting on X_A and applying to X_B − μB + μA, gave identical predictions sample for sample in all 845 cells, with a maximum difference in balanced accuracy of 0.0e+00. This is Proposition 1's `dbl` case verified as an identity.

Standardisation with training statistics is a related but different operation. Write X̃ = (X − μA)/s_A for both sessions. In that space the source mean is zero, so `zero` and `mean` coincide, and the pipeline is equivariant. But "standardise only" is *not* the same transformation as "centre both sessions": the two differ by (μB − μA)/s_A on the target, and applying the model fitted on X̃_A to X̃_B gives the predictions of `none`, not of `mean`. In our data the two agree exactly in 100.0 per cent of samples for BCI-2a and BCI-2b, and this is an empirical fact about LDA with Ledoit-Wolf shrinkage rather than a theorem: without shrinkage the covariance estimate on grasp-and-lift is rank-deficient, and the agreement drops to 51.8 per cent (Section 4.10). The correct statement is therefore narrow: standardising with training statistics makes the pipeline equivariant and makes the two centrings coincide *inside that space*; it does not implement the two-sided correction, and a pipeline that standardises and then centres either way obtains the two-sided result.

**Table 3.** Balanced accuracy per dataset. `dbl` coincides with `mean` in every cell. The reference is the within-session cross-validation of Section 3.

| dataset | n | none | zero | mean | dbl | train-only | reference |
|---|---|---|---|---|---|---|---|
| BCI-2a (K=4) | 36 | 0.5656 | 0.5254 | 0.6119 | 0.6119 | 0.5141 | 0.5355 |
| BCI-2b (K=2) | 108 | 0.7046 | 0.5831 | 0.7375 | 0.7375 | 0.5722 | 0.7571 |
| SEED (K=3) | 45 | 0.4591 | 0.3377 | 0.7094 | 0.7094 | 0.3456 | 0.7738 |
| NER2015 (K=2) | 320 | 0.5886 | 0.5865 | 0.5909 | 0.5909 | 0.5845 | 0.6167 |
| grasp-and-lift (K=2) | 336 | 0.7770 | 0.7484 | 0.7815 | 0.7815 | 0.7521 | 0.8350 |
| all | 845 | 0.6705 | 0.6346 | 0.6926 | 0.6926 | 0.6338 | 0.7264 |

The gain of `mean` over `none` is +0.0463 on 2a, +0.0329 on 2b and +0.2503 on SEED, and small where the features have no origin offset: +0.0023 on NER2015 and +0.0045 on grasp-and-lift. Fig. 3 shows the levels by dataset and the gain per subject.

![Figure 3](figs/fig3.png)
**Fig. 3.** (a) Balanced accuracy of the three pipelines by dataset; (b) the gain of the two-sided over the uncorrected pipeline, one point per subject, with the box showing the median and quartiles. Per subject the gain is positive in 9 of 9 on 2a (median +0.0356, 95% CI [+0.0287, +0.0659], dz = 1.52, p = 3.9 × 10⁻³), 9 of 9 on 2b (+0.0321, [+0.0187, +0.0477], dz = 1.39, p = 3.9 × 10⁻³), 15 of 15 on SEED (+0.2452, [+0.2038, +0.2958], dz = 2.71, p = 6.1 × 10⁻⁵), 10 of 16 on NER2015 (+0.0050, [−0.0018, +0.0062], p = 0.32) and 8 of 12 on grasp-and-lift (+0.0031, [+0.0007, +0.0090], p = 0.052).

### 4.2 An origin sweep: the equivariant pipelines are exactly flat

To measure the effect of the origin with the cells held fixed, we added a common constant to every feature, in both sessions alike, and swept its size over ten settings; the sweep was run on all 845 cells.

![Figure 1](figs/fig1.png)
**Fig. 1.** (a) Change in balanced accuracy of the one-sided pipeline as a function of z_T, one curve per dataset; (b) the fraction of cells that land on exactly 1/K; (c) the largest change of the two equivariant pipelines over the whole sweep. The equivariant pipelines change by 0.0e+00 in every cell at every setting; the one-sided pipeline slides and stops.

`none` and `mean` are exactly invariant: across 845 cells and ten settings the largest absolute change in balanced accuracy was 0.0e+00 for both, in every dataset (Fig. 1c). The one-sided pipeline decays toward 1/K as z_T grows and stops there (Fig. 1a,b): on grasp-and-lift the fraction of cells at chance rises from 0.00 to 1.00 as z_T goes from 0.26 to 54.9; on BCI-2a from 0.08 to 0.97; on NER2015 from 0.05 to 0.93; on BCI-2b it starts at z_T = 26 where 0.60 are already at chance and rises to 0.78; on SEED it starts at z_T = 34 where 0.90 are already at chance and ends at 1.00.

### 4.3 The direction control: the source-only statistic is direction-blind

The sweep of Section 4.2 injects the origin along one direction, which is not enough: §2.3 says the damage is governed by the projection of the origin onto the weights, so an origin orthogonal to the weights should do nothing while raising any norm-based statistic. We ran that experiment.

**Table 4.** Equal-norm origins, three directions, LDA, 60 cells per dataset. `change` is the penalty relative to the no-injection baseline.

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

The two directions give the same z_T to two decimals in both datasets, and the orthogonal one changes the penalty by exactly 0.0000 while the parallel one changes it by −0.13 and −0.21 to −0.31. A norm-based statistic is therefore blind to the direction — this is the counter-example that the referee of an earlier version of this work constructed, and it is correct.

The orthogonality in this experiment is defined with respect to w, which is the binary case; for K > 2 the direction that leaves the decision unchanged is the null space of P W, and we did not run the multiclass version of the control. This is a limitation of the experiment, not of the statistic, which is defined through P W for any K.

The projected statistic z_w of Equation (2) does not fail the test by construction: w'(μ_A + c) = w'μ_A for c orthogonal to w, so its value is unchanged in the orthogonal arm and changes only in the parallel arm, exactly like the penalty. We therefore use z_w as the screen and keep z_T only as the naive alternative its failure is measured against.

### 4.4 The screen as an empirical proxy

**Table 5.** The source-only statistic at the level of dataset-by-representation units, medians within a unit. z_T = ||μ_A||/||sd_A||; z_w is Equation (2) with the scale taken from the centred scores; penalty = zero − none; gain = mean − none. Sorted by z_w.

| dataset | representation | n | z_T | z_w | penalty | gain |
|---|---|---|---|---|---|---|
| BCI-2b | csp | 27 | 0.22 | 0.068 | +0.018 | +0.026 |
| NER2015 | time mean | 320 | 0.20 | 0.230 | 0.000 | 0.000 |
| grasp-and-lift | log power | 336 | 0.25 | 0.289 | −0.015 | 0.000 |
| BCI-2a | csp | 9 | 0.40 | 0.287 | +0.024 | +0.059 |
| BCI-2a | tan | 9 | 0.37 | 0.309 | +0.014 | +0.031 |
| BCI-2a | euc_ea | 9 | 0.64 | 0.597 | −0.014 | +0.059 |
| BCI-2a | euc | 9 | 7.87 | 4.399 | −0.184 | +0.017 |
| BCI-2b | tan | 27 | 21.2 | 5.117 | −0.160 | +0.020 |
| BCI-2b | euc_ea | 27 | 14.2 | 5.405 | −0.137 | +0.018 |
| SEED | differential entropy | 45 | 34.2 | 12.36 | −0.029 | +0.211 |
| BCI-2b | euc | 27 | 57.1 | 23.31 | −0.186 | +0.021 |












Three analyses, in decreasing order of independence, for the projected statistic z_w and, for comparison, the norm-based z_T.

*Dataset level.* With the corrected definition the five development datasets give a rank correlation of −0.80, and adding SEED-IV (median z_w = 24.4, median penalty −0.070) does not improve it: the six-dataset value is −0.77, and the exact permutation test gives 74 of 720 orderings at least as extreme, p = 0.103. The earlier six-dataset value of −0.94 and p = 0.103 were computed with the uncentred scale, which the referee's counter-example shows is not a function of the decision function; they do not survive the correction.

*Cell level.* Within the 845 development cells the statistic separates a severe loss with an AUC of 0.841, and at the level of the eleven development units the rank correlation is −0.83. Both are between-family effects: within SEED-IV the AUC is 0.515, within BCI-2a the four representations have nearly the same statistic and penalties from +0.024 to −0.184, and the leave-one-dataset-out operating point fails on SEED and NER2015 (Table 6).

*The held-out operating point.* A threshold of 0.354 fixed on the five development datasets gives, on SEED-IV, sensitivity 1.000, specificity 0.000, precision 0.544: every cell is flagged. The dataset-level prediction is right — SEED-IV is an exposed feature family — and the cell-level rule is useless.

We therefore do not present the statistic as a screening tool. It is reported because it is the natural source-only quantity, because its failures are informative about what a source-only analysis can and cannot see, and because a reader who is tempted to build such a screen should know the three ways in which ours failed.

### 4.5 The classifier dependence is a threshold-error effect, and its sign is predictable

Table 3 showed that the sign of the one-sided effect depends on the classifier: on BCI-2b it is −0.122 for LDA and +0.032 for a linear support-vector machine with C = 0.01. On every cell of BCI-2b the same pattern holds across the regularisation sweep (LDA −0.104 to −0.122, logistic −0.060 to −0.118, SVM +0.090 at C = 0.001 through −0.099 at C = 10), and on every cell of BCI-2a the SVM is helped at every regularisation (+0.010 to +0.022) while LDA and logistic are hurt (−0.015 to −0.044).

Equation (4) says why, and it makes a prediction the size of the displacement cannot make. The sign of the damage is fixed by t*, the displacement of the aligned threshold from the target optimum. We measured t* on the aligned target scores (an analysis that uses target labels and is therefore descriptive, not deployable) and compared the predicted sign of Δ = BA(c, t* − s) − BA(c, t*) with the observed sign.

**Table 7.** Per-cell prediction of Equation (4). For BCI-2a the cells are the two-class subproblem of classes 1 and 2; the four-class problem is not covered by the law. `MAE` is the mean absolute difference between the predicted and the observed change on the *same* cell; `r` is Pearson; `sign` is the fraction of cells whose sign is predicted, `base` the majority-class rate on the same cells, and `bound` the fraction of cells satisfying the analytic bound |Δ| ≤ 0.1995|s| that follows from the derivative of Equation (3).

| dataset | classifier | n | MAE | r | sign | base | bound |
|---|---|---|---|---|---|---|---|
| BCI-2b | LDA | 108 | 0.0130 | 0.989 | 0.917 | 0.815 | 1.00 |
| BCI-2b | logistic | 108 | 0.0127 | 0.990 | 0.889 | 0.769 | 1.00 |
| BCI-2b | SVM | 108 | 0.0224 | 0.381 | 0.676 | 0.528 | 1.00 |
| BCI-2a | LDA | 36 | 0.0320 | 0.902 | 0.889 | 0.833 | 1.00 |
| BCI-2a | logistic | 36 | 0.0330 | 0.885 | 0.750 | 0.750 | 1.00 |
| BCI-2a | SVM | 36 | 0.0161 | 0.610 | 0.611 | 0.528 | 1.00 |
| grasp-and-lift | LDA | 336 | 0.0360 | 0.649 | 0.693 | 0.604 | 1.00 |
| grasp-and-lift | logistic | 336 | 0.0364 | 0.592 | 0.649 | 0.607 | 1.00 |
| grasp-and-lift | SVM | 336 | 0.0115 | 0.353 | 0.420 | 0.292 | 1.00 |
| NER2015 | LDA | 320 | 0.0285 | 0.385 | 0.556 | 0.406 | 1.00 |
| NER2015 | logistic | 320 | 0.0258 | 0.371 | 0.509 | 0.425 | 1.00 |
| NER2015 | SVM | 320 | 0.0434 | 0.458 | 0.666 | 0.503 | 1.00 |

Pooled over the 2,400 cells the predicted and observed changes have a mean absolute difference of 0.028 and a correlation of 0.825.

**The bound applies to the model, not to the data.** The inequality |Δ| ≤ 0.1995|s| follows from the derivative of Equation (3), so it constrains the *predicted* change and holds for it in every cell by construction. The *observed* change is a step function of the sample scores: moving a threshold across a handful of trials moves balanced accuracy by a multiple of 1/n_c, and nothing in the Gaussian model prevents that step from being large. We therefore counted both. Over the 800 binary cells the prediction violates the bound in 0 of 800 cases, and the observation violates it in 185, i.e. 23.1 per cent, with a median ratio |Δ_obs|/|s| of 0.29 among the violations and a maximum of 4.1. The correct reading is that the model's own quantity obeys its own bound, while the empirical quantity is discrete and can jump; the correlation of 0.83 is the evidence for the model, not the bound.

Fig. 4 plots the per-cell prediction against the per-cell observation for LDA on the 800 binary cells, with the identity line; the error distribution is centred on zero with a mean absolute value of 0.030 and no systematic dependence on the size of the change.

![Figure 4](figs/fig4.png)
**Fig. 4.** (a) Predicted change of Equation (4) against the observed change, one point per cell, LDA, the 800 binary cells of the four binary datasets; the dotted line is the identity. (b) Distribution of the prediction error.

The law is quantitative where its Gaussian approximation is defensible — LDA and logistic regression on the two BCI datasets, with per-cell correlations of 0.89 to 0.99 and a mean absolute error of 0.013 to 0.033 — and it degrades to a sign-level account on grasp-and-lift and NER2015 (correlations 0.37 to 0.65) and for the support-vector machine (0.35 to 0.61). Its raw sign accuracy sits at or slightly above the majority-class rate, which is the reason we report the sign-discrimination AUC instead. In a split-sample test, with t* estimated on one half of the target and the sign evaluated on the other half, the sign-discrimination AUC is 0.914 [0.853, 0.958] (BCI-2b, LDA), 0.848 [0.767, 0.917] (BCI-2b, logistic), 0.848 [0.705, 0.955] (BCI-2a, LDA), 0.786 [0.618, 0.924] (BCI-2a, logistic), 0.667 [0.606, 0.725] (grasp-and-lift, LDA) and 0.662 [0.599, 0.721] (grasp-and-lift, logistic), with intervals from a bootstrap over cells. The support-vector machine is neither uniformly at chance nor uniformly above it: 0.571 [0.446, 0.689] on BCI-2b, 0.328 [0.160, 0.506] on BCI-2a and 0.478 [0.387, 0.570] on grasp-and-lift. We therefore describe it as unstable across settings rather than as at chance, and we do not claim the law for it.

**Two parameterisations, and which one the model requires.** The numbers in Table 7 use c = Φ⁻¹(BA_aligned) and a *pooled* score standard deviation. The equal-variance Gaussian derivation uses the *within-class* standard deviation and fixes c from the class separation, c = (m₁ − m₀)/(2σ_w), and these are not the same parameterisation: for two equal-variance classes σ²_pooled = σ²_with + (m₁ − m₀)²/4. We therefore recomputed the law the way the model requires. The fit degrades: for LDA on BCI-2b the correlation falls from 0.989 to 0.861 and the mean absolute error rises from 0.013 to 0.057; on BCI-2a from 0.902 to 0.874; on grasp-and-lift from 0.649 to 0.271, and on NER2015 the within-class scale is not estimable in enough cells to report. The model's own implied accuracy Φ(c) is also far from the observed aligned accuracy, by 0.096 on BCI-2b and 0.213 on grasp-and-lift, which is a direct statement that the equal-variance Gaussian assumption does not hold on these scores.

There is a second reason to be careful with the pooled-parameterisation figures. In that variant c is computed from BA_aligned, and BA_aligned also enters the observed change, so part of the high correlation is built in rather than predicted. We report both variants and treat the pooled one as a descriptive decomposition and the within-class one as the model check; neither supports the word "predictive law", and the paper no longer uses it.

The classifier family is not the variable: t* is. A strongly regularised support-vector machine has almost no threshold error to displace, so the one-sided centring moves the boundary toward the optimum and helps; LDA and logistic regression sit near the mixture-weighted optimum and are pushed away. ρ, being unsigned, orders the magnitude but cannot order the sign — which is the referee's point, and we state it as a limitation of Equation (2).

### 4.6 Variants, and what labels add

Proposition 3 says the prediction-relevant content of a correction is PWγ. We built five alternatives and evaluated each on all 845 cells.

**Table 8.** Alternatives to the mean correction. `proj` subtracts the component of the offset in the row space of W; `shrink` half the offset; `low5` the projection onto the five leading source principal directions; `bal` the class-balanced offset, using the target labels.

| dataset | none | zero | mean | proj | shrink | low5 | bal |
|---|---|---|---|---|---|---|---|
| BCI-2a | 0.5656 | 0.5254 | 0.6119 | 0.6119 | 0.5965 | 0.5873 | 0.6119 |
| BCI-2b | 0.7046 | 0.5831 | 0.7375 | 0.7375 | 0.7260 | 0.7318 | 0.7373 |
| SEED | 0.4591 | 0.3377 | 0.7094 | 0.7094 | 0.5551 | 0.4460 | 0.7092 |
| NER2015 | 0.5886 | 0.5865 | 0.5909 | 0.5909 | 0.5887 | 0.5873 | 0.6039 |
| grasp-and-lift | 0.7770 | 0.7484 | 0.7815 | 0.7815 | 0.7817 | 0.7793 | 0.7815 |

The projected correction returns predictions identical to `mean` in 100.0 per cent of samples, as Proposition 3 requires. Halving the correction loses accuracy where it matters (0.015 on 2a, 0.012 on 2b, 0.154 on SEED), and the low-rank variant is the worst on SEED (0.446 against 0.709). The label-based correction changes nothing on the four balanced datasets (0.0000 on 2a and grasp-and-lift, −0.0002 on 2b, −0.0002 on SEED) and gains 0.013 on NER2015, the one dataset whose class priors change substantially. This is exactly the behaviour that §2.4 predicts, and it is *not* a claim that labels never help: they help where the prior changes, and the earlier draft's summary sentence was wrong on that point.

The correction composes with second-order alignment: within the Euclidean-aligned representation the mean correction still gains +0.0725 on BCI-2a and +0.0236 on BCI-2b, within the tangent representation +0.0417 and +0.0452, within CSP +0.0575 and +0.0384, and within plain log power +0.0135 and +0.0245.

**Corollary (decision-space form).** For an affine model the correction can be applied to the K scores instead of the D features, by subtracting δ_k = w_k'(μB − μA) from score k. We verified the equivalence on three linear families and three datasets: identical predictions in 100 per cent of samples, maximum discrepancy 0.0e+00, equal balanced accuracy to four decimals (0.7365 against 0.7365 for LDA on 2b; 0.7188 against 0.7188 for the SVM). The practical difference is what each form needs: the feature-space form needs the target features, the decision-space form needs the target scores and K numbers. For non-linear models the decision-space form is an approximation that we did not test.

### 4.7 Probability calibration, on every cell

**Table 9.** Calibration, LDA, every cell of each dataset; ECE uses ten equal-width bins, is averaged within subject, and the interval is a bootstrap (5,000 resamples) over subjects of the mean; because the three pipelines are evaluated on the same subjects, the intervals should be read as descriptive and a paired test would be more efficient.

| dataset | n | pipeline | BA | median ECE | 95% CI of the mean ECE | Brier | log loss |
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

Because the pipelines are evaluated on the same subjects, we also report the paired difference per subject. The one-sided minus uncorrected difference is +0.254 [+0.229, +0.282] on BCI-2b, +0.129 [+0.098, +0.160] on SEED and +0.030 [+0.013, +0.047] on grasp-and-lift: the one-sided pipeline is worse on all three. The two-sided minus uncorrected difference is −0.014 [−0.036, +0.006] on BCI-2b, which is a tie, −0.251 [−0.296, −0.205] on SEED and −0.006 [−0.010, −0.002] on grasp-and-lift. We therefore claim no calibration *improvement* from the correction on BCI-2b; what the correction does there is restore the calibration that the one-sided pipeline destroys, and on SEED it improves on doing nothing. On SEED all pipelines are poorly calibrated, which we attribute to the difficulty of the task for a linear model on these features and not to the features "not being probabilities" — a classifier can map arbitrary features to calibrated probabilities, and we should not have implied otherwise.

### 4.8 Collapse, and the difference between chance and collapse

The identity of §2.5 is exact by construction: on all 845 cells it agrees with the observed collapse — every prediction equal — in 124 of 124 collapsing cells and 721 of 721 non-collapsing cells. Since the identity is equivalent to the statement that all predictions are equal, this agreement is a check of the implementation, not evidence of a new capability.

Its only substantive use is that it separates collapse from chance-level accuracy. Of the 845 cells, 180 report balanced accuracy exactly 1/K after the one-sided pipeline and only 124 have collapsed; the difference is concentrated in the imbalanced dataset (NER2015: 66 cells at chance, 16 collapsed). A target whose class priors are 0.17 and 0.83 can reach a balanced accuracy of 0.5 without returning a single class, because the classifier has scrambled both recalls. A pipeline audit that checks only for chance accuracy reports the wrong reason. We present the identity as a diagnostic for that purpose, and not as a detector.

### 4.9 What is left

After the correction a residual gap to the within-session reference remains: 0.0198 on BCI-2b, 0.0770 on SEED, 0.0257 on NER2015 and 0.0294 on grasp-and-lift. It is not an origin effect: across all 845 cells the correlation between z_T and the residual is +0.06, and within datasets it has no consistent sign (BCI-2a −0.55, BCI-2b −0.37, SEED +0.41, NER2015 +0.11, grasp-and-lift +0.27). The residual is weakly associated with the class-conditional offset h_k of Equation (5) in units of the score spread: +0.21 on BCI-2a, −0.36 on BCI-2b, +0.33 on SEED, +0.30 on NER2015, +0.55 on grasp-and-lift (pooled +0.26, four of five in the same direction). A change of the within-session covariance explains less (pooled +0.10). We report the boundary rather than closing it.

### 4.10 Implementation details that matter for reproduction

**The invariances of z_w, and the convention that matters.** With the scale taken from the centred scores, z_w is invariant to (i) adding a class-common linear term to all scores, (ii) adding a constant to all scores, and (iii) translating the features in the null space of P W. We verified (i) to 4.4 × 10⁻¹⁶, and (ii) and (iii) to 1.4 × 10⁻¹⁴ and 2.5 × 10⁻¹³ over 60 cells. Taking the scale from the *uncentred* scores instead — the convention of the first version — breaks (i) and can change z_w by a factor of 1.5 on a decision-equivalent classifier, which is why the definition was corrected.

**The held-out dataset.** SEED-IV was converted from the distributed features with the session labels in its ReadMe, cached per session, and evaluated with the models and thresholds fixed in earlier rounds. No parameter was tuned on it.

Two checks that a reader reproducing this work will need. First, the `mean`/`dbl` identity of §4.1 is exact for every fit with an unpenalised intercept; we verified it on all 845 cells. Second, the `z-score` versus `none` agreement of §4.1 is *not* a theorem: with Ledoit-Wolf shrinkage the agreement is 100.0 per cent on BCI-2a, BCI-2b and grasp-and-lift, but with shrinkage set to zero — where the 256-dimensional grasp-and-lift covariance is rank-deficient — it falls to 51.8 per cent. A pipeline that relies on standardisation for equivariance should therefore verify it rather than assume it.

## 5. The procedure

**Step 1 (exploratory) — project the source mean onto the classifier's direction.** z_w = ||P W μ_A||/(√K σ_s) requires nothing but the training session: the fitted weights, the source mean and the score spread. In our units, below z_w = 0.35 the penalty of the one-sided form is between +0.024 and −0.015; above z_w = 0.9 it is between −0.03 and −0.19, and the held-out dataset sits at 24.4 with a penalty of −0.070. Across all 845 cells the statistic separates a loss larger than 0.05 from the rest with an AUC of 0.84 (Section 4.4). These are descriptive operating characteristics of the twelve units studied, not validated thresholds, and the held-out test of Section 4.4 shows that a threshold fixed this way does not transfer to cells: use the statistic to say whether a *feature family* is likely to be exposed, and not to certify that a particular representation, session or subject is safe — the four BCI-2a representations have almost the same z_w and penalties that differ by 0.21. Do not use the norm-based z_T at all; Section 4.3 shows it is unchanged by a translation that can destroy the decoder.

**Step 2 — centre both sessions, and fit on the centred training data.** This makes the pipeline equivariant (Proposition 1). Standardising with training statistics also makes it equivariant but does *not* implement the two-sided correction; a pipeline that standardises and then centres either way obtains the two-sided result (Section 4.1). If the model is frozen, subtract w_k'(μB − μA) from score k instead (Section 4.6).

**Step 3 — check collapse before believing an accuracy.** If all target predictions are equal, the classifier has collapsed and its balanced accuracy is 1/K by identity; the inequality of §2.5 tells the same thing from the scores and is useful when one wants to know *why*.

**The unit test.** Translate every feature by a constant, refit, and check that the predictions are unchanged. The test is one line of code, satisfied by construction by any equivariant pipeline and violated by any one-sided one, and it needs no labels. It would have caught the failure mode this paper is about.

**Deployment, and why the trial order matters.** For an online system the target mean is not available at the first trial, and the natural substitute is a running mean warm-started at the source mean. With the trials in a random order the running reference is close to the batch correction after five trials (0.7334 against 0.7365 on BCI-2b, 0.7086 against 0.7094 on SEED, 0.7911 against 0.7938 on grasp-and-lift, 0.6105 against 0.6119 on BCI-2a). With the trials in their recorded order the same pipeline is exact on BCI-2b (0.7409 against 0.7365) and clearly worse on the two datasets whose sessions are organised in blocks (0.6724 against 0.7094 on SEED; 0.6781 against 0.7938 on grasp-and-lift), because the first trials of those sessions belong to one film or one series and are not a sample of the session. A running reference therefore does not remove the need for a calibration block; it moves the requirement to an exchangeable trial order or to a warm-up that spans the blocks. We report both orders because the random-order result alone would have overstated the method.

## 6. Discussion

### 6.1 What the characterization buys, and what it does not

The paper's claim is about a mechanism and its boundaries, and it is worth saying so in one place. What we can say is: a first-order correction has a unique effect on score differences; its absence or misapplication displaces the decision function by an amount that is computable and whose sign is predictable for mean-calibrated linear classifiers; and the exposure of a feature family can be ranked before any target label. What we cannot say, and do not, is that a threshold on the resulting statistic decides whether a given session will fail — the held-out test in Section 4.4 shows the opposite.

Three kinds of statement are mixed in a paper of this shape, and it is worth separating them, because only the second is specific to EEG. The first kind is a corollary of linear discriminant theory: a constant added to a feature vector moves the intercept, so a fixed model is not invariant to it, and the prediction-relevant content of a reference is its projection onto the weights. We prove these and do not claim them as discoveries. The second kind is an empirical regularity of cross-session EEG features: which feature families carry a large free origin (log-power and differential entropy, z_T from 8 to 57; time-domain contrasts, 0.2), how large the resulting damage is on five public datasets, and the two ways in which a source-only screen fails on them. The third kind is a change in practice: centre both sessions, verify the invariance with a one-line test, and do not use a norm-based origin statistic. We have tried to keep the three apart in the text, and the abstract now leads with the second and third.

The practical content of Propositions 1–3 is a decision: if the pipeline's output is to be independent of an unreported origin, the correction must be equivariant, and the canonical equivariant correction is the sample mean. The characterization does *not* say that the sample mean is optimal, and Section 4.5 exhibits the regimes in which it is not. What it does say is that any other choice in the equivariant family adds an offset that must be justified, and that two corrections whose projections onto the centred weights agree are the same pipeline whatever their algebraic form — which is why the projected variant reproduces the mean correction exactly and why the shrunk and low-rank variants lose accuracy.

### 6.2 Why some features are exposed and others are not

z_T is large when the feature carries a free additive constant. Log power has three: the logarithm of a reference power, a floor added before the logarithm, and a change of the reference electrode that adds an offset to the potential before a non-linear transform. Differential entropy inherits all three. A difference of two conditions measured within the same trial has none, which is why the time-domain contrast features of NER2015 have z_T = 0.20 and a penalty of 0.000. This is a statement about measurement conventions, not about neurophysiology: the origin is set by the amplifier, the montage and the code, and none of the three is reported in a typical methods section.

The physical reading should not be pushed too far. An amplifier gain change and a reference-electrode change both alter the covariance of the raw signal, and a reference change in particular is not a pure translation of the feature vector; what is additive after a log transform is the *magnitude* of a gain change, not every consequence of a montage change. We use the phrase "origin" as a description of the feature-space effect, not as a claim about its electrical cause.

### 6.3 Relation to alignment methods

Euclidean and Riemannian alignment [5-8] act on second-order structure, and the Riemannian Gaussian–Laplace framework of [16] is a recent example of the same second-order programme. An alignment matrix that happens to be a multiple of the identity performs no alignment, so the first-order correction is not a special case of the second-order one, and Section 4.6 shows that the two compose in all four BCI representations. Where the two intersect is the label-shift problem of §2.4: aligning a covariance implicitly assumes that the class mixture is unchanged, and re-weighting the classes changes the average covariance in a way that alignment cannot distinguish from a change of state. Under the label-shift assumption the prior is estimable [12]; without it, the same ambiguity applies to both families, and we state it as a bound rather than as a defect of a particular method.

### 6.4 Limitations

**Prevalence is measured only anecdotally.** We inspected one published cross-session example in detail, the MOABB cross-session motor-imagery script, which evaluates CSP+LDA and Riemannian tangent space + logistic regression with leave-one-session-out [18]. Neither pipeline centres the target at prediction time, and every transform is fitted inside the training fold, so the example is equivariant by construction and cannot exhibit the failure. That is the correct way to build a cross-session pipeline, and it is the reason the ambiguity is invisible in framework code: the framework fixes the reference to the training fold. The exposure is in pipelines that add a normalisation step at prediction time, outside the fold. We have not surveyed that population and put no number on its size. A reader who believes the one-sided form is rare should read the paper as a statement about origin dependence rather than about prevalence; the unit test is the cheap way to settle the question for any particular codebase.

**The screen is a proxy, and it fails in two reported cases.** Section 4.3 shows that a norm-based statistic is unchanged by an origin orthogonal to the weights that does nothing; the projected statistic z_w does not have that failure by construction, but it remains an empirical proxy. It separates a severe loss with an AUC of 0.84 across cells and 0.83–0.86 within BCI-2a, BCI-2b and grasp-and-lift, but it cannot resolve the four BCI-2a representations (z_w 0.285–0.325, penalties +0.024 to −0.184) and its within-SEED ordering is inverted (AUC 0.332). A sixth dataset that played no role in choosing the statistic has now been tested at the level of datasets: SEED-IV lands where the relation predicts, and the six-dataset exact permutation p is 0.017. At the level of cells and representations the picture does not improve: within SEED-IV the statistic has an AUC of 0.48, within BCI-2a it cannot separate the four representations, and the leave-one-dataset-out operating point fails on two of five held-out datasets. What survives is a between-family triage, not a screening instrument, and we do not claim more.

**The screen orders risk, not benefit.** z_T orders the penalty across units (−0.755, cluster-bootstrap interval [−1.00, −0.28]) and does not order the gain (+0.19, p = 0.57).

**Five datasets cannot establish a law.** The dataset-level rank correlation is −0.80 with p = 0.10; the unit-level analysis has eight of eleven units from two datasets, and we handle that with a cluster bootstrap rather than a permutation test over units. An independent dataset, not used to choose the statistic, would be needed for a stronger claim, and we do not have one.

**The sign analysis uses target labels.** t* in Equation (4) is estimated from the aligned target scores, so the sign prediction is descriptive; a deployable version would need a label-free estimate of the threshold error, which we did not build.

**The protocol is transductive.** Both the feature-space and the decision-space corrections use the whole target session to estimate μB. That is legitimate under a protocol that allows unlabelled target data, and it is not available in a strictly inductive deployment; the running-mean experiment of Section 5 is a partial substitute and it fails under block-ordered trials.

**No streaming protocol of the kind used online.** The running-mean experiment is a simulation on offline data; the random-order variant is reported with one draw per cell rather than with a distribution over orderings.

**The decision-space form is proved for affine models only.** Section 4.6 verifies it for LDA, logistic regression and a linear support-vector machine; for a non-linear model the same shift is an approximation that we did not measure.

## 7. Conclusion

Two centrings circulate under one name. The two-sided form is invariant to the coordinate origin; the invariant family is wider than the sample mean, and we state it rather than claiming uniqueness. Two corrections shift every score difference by the same amount exactly when their projections onto the centred weights agree, with the caveat that label predictions can agree even when score differences do not and that a degenerate class can be shifted for free.

Whether the correction helps is a separate question, and the answer is quantitative only where the Gaussian approximation holds. On the BCI datasets the signed law predicts the per-cell change of balanced accuracy with a correlation of 0.99 and a mean absolute error of 0.013 for LDA, its sign discrimination survives a split-sample test (AUC 0.91), and it degrades to a sign-level account on two other datasets and to chance for a support-vector machine. We report the degradation rather than a single accuracy figure.

Empirically, an origin sweep on 845 cells from five datasets leaves the equivariant pipelines unchanged by 0.000 and drives the one-sided one to exact chance; an equal-norm direction control shows that a norm-based statistic is blind to the direction of the origin and that only the component along the weights damages the decoder. A source-only statistic that is invariant to decision-equivalent score representations orders the damage between feature families (AUC 0.84 within the development cells) but not across them once the held-out dataset is included (rho = −0.77, exact p = 0.10), and its operational threshold has no specificity on the held-out data. We report it as an exploratory analysis and draw no screening recommendation from it. What the correction cannot repair is a change of class priors, which is confounded with a class-conditional offset unless the label-shift assumption is granted; where the priors do change, labels recover a further 0.013.

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

[19] W.-L. Zheng, W. Liu, Y. Lu, B.-L. Lu, A. Cichocki, EmotionMeter: a multimodal framework for recognizing human emotions, IEEE Trans. Cybern. 49 (2019) 1110–1122.

