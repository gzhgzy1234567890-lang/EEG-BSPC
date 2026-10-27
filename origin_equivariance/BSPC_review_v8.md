# Referee report — BSPC submission

**Manuscript:** "Origin equivariance in cross-session EEG decoding: what a mean correction repairs and how to screen for the risk"

**Recommendation:** Major revision (not minor). The paper is careful, honest and well written; the problem is that its contribution is a characterization of a one-line operation plus a validation study, and the validation contains three soft spots that a second referee will find. I list what would have to change for me to move to minor.

---

## Summary of what the paper does

1. Defines six centring pipelines and proves that only the two-sided forms are equivariant to a translation of the feature origin (Prop. 1).
2. Proves a prediction-equivalence: two corrections give identical predictions iff their references differ by a vector in the null space of W (Prop. 2).
3. Proposes a source-only statistic z_T (distance of the feature origin from the data centre) and an induced displacement ρ, and shows that (a) z_T orders the damage of the one-sided form across 11 dataset-by-representation units (Spearman −0.755) and 845 cells (−0.382); (b) ρ orders the damage across 14 classifier/regularisation settings on BCI-2b (−0.78).
4. Reports a label-free collapse certificate that is exact on 845 cells and distinguishes collapse from chance-level accuracy.
5. Reports calibration, a streaming-reference test, and an inconclusive residual analysis.

## Major comments

**M1. The paper has no method.** It explicitly declines to propose one (Section 2.2), and the operation it defends is a subtraction of two means. BSPC's readership expects either a signal-processing method with demonstrated benefit or a clinical/engineering application. The manuscript's own defence — "the characterization is the contribution" — is a legitimate genre, but then the empirical part has to be strong enough to carry it. At present the empirical part is a validation of a convention, and the largest gains (+0.25 on SEED, +0.033 on 2b) come from datasets where the features are log-power or differential entropy, i.e. from the fact that these features carry a large DC term. I can summarize the paper in one sentence: "if your log-power features have a large arbitrary offset, centre them on the training mean". That sentence is already in every textbook on preprocessing, and the manuscript does not demonstrate that the mistake is made in practice.

**M2. The prevalence question is not answered and cannot be waved away.** The manuscript concedes (Section 6.4) that no code audit was performed. A referee at BSPC will ask: who does the one-sided form? Without at least a small audited sample of public pipelines (MOABB, Braindecode, pyRiemann examples, the BCI-IV baseline code), the practical relevance is unestablished and the paper reads as a straw man. The unit test is a good idea, but a good idea is not evidence.

**M3. The screen is fitted on 11 points.** The headline "screen" is a Spearman correlation over 11 units, and those units are a mixture of five datasets and four feature families; the two clusters (low z_T, high z_T) are essentially "features without an offset" versus "log-power/DE features". The correlation is therefore close to a restatement of the definition of z_T. The cell-level correlation (−0.382) is quoted with a p-value of 10⁻³⁰, but cells within a unit are not independent, and the manuscript's own statistics section says so. This must be reported as a descriptive statistic, not as inference, and the abstract must not quote the cell-level p-value.

**M4. The benefit of the correction is not screenable, and the paper's own framing depends on the risk being screenable.** Section 4.3 reports that z_T does not order the gain (p = 0.57). This is honest, but it means the practical message is "avoid a catastrophe you cannot predict the size of". That is a weaker claim than the abstract suggests. Either (i) find a statistic that orders the gain (the offset displacement t, which the manuscript measures but does not use for the screen, is the obvious candidate — it is +0.25 at cell level, which is weak but positive), or (ii) reframe the abstract around risk only.

**M5. The classifier analysis rests on one dataset.** The ρ story is convincing on BCI-2b, but 14 settings from a single dataset and a single subject pool cannot support the sentence "the classifier family is a proxy for ρ". On grasp-and-lift and NER2015 the ρ values are all below 0.4 and the damage is within ±0.033, so the relation is not tested where it would matter. Either extend to a second exposed dataset (SEED with a binary split, or 2a with a one-vs-rest decomposition) or downgrade the claim to "on BCI-2b".

**M6. The collapse certificate is exact by construction.** Proposition 5 restates the definition of "argmax is constant"; the empirical "124 of 124" is a tautology given the implementation. The only non-trivial content is the observation that chance-level balanced accuracy is not the same as collapse (66 versus 16 on NER2015). That is a good observation, but it belongs in a short subsection, not in a proposition with a table.

**M7. Calibration numbers are under-powered.** ECE with ten bins on ~60 trials per session and nine subjects is noisy; the SEED ECE of 0.539 for the uncorrected pipeline indicates that the probability model is meaningless there, which undermines the claim that the correction "recovers calibration". Report the ECE per subject with a CI, or restrict the calibration claim to BCI-2b.

**M8. The residual analysis is inconclusive and should be shortened.** A correlation that is +0.21, −0.36, +0.33, +0.30, +0.55 across datasets is not a finding; the manuscript says so, but it still occupies a full subsection and a paragraph of the abstract. Cut it, or replace it with a quantitative statement of what the label-information gap is (e.g., the target-session accuracy of the source-trained model as a function of the number of target labels), which would be useful.

**M9. Streaming experiment is not a streaming protocol.** A random trial order with a warm start from the source mean is not how an online BCI session unfolds, and the 5-trial warm-up is asserted rather than justified. If the claim is "no calibration block is needed", it must be tested with the real trial order and with a convergence criterion (e.g. the number of trials until the running reference is within 10 per cent of the session mean, as a function of z_T).

**M10. Novelty relative to the alignment literature is asserted rather than demonstrated.** The manuscript argues that first-order and second-order corrections are orthogonal, but it does not run the obvious experiment: apply Euclidean or Riemannian alignment *both* with and without the mean correction, on the same cells, and show that the two compose rather than substitute. The `euc_ea` and `tan` representations are not that experiment because they differ in more than the alignment step.

## Minor comments

1. Fig. 2a: labels overlap and the two clusters are not annotated; the panel does not communicate the screen.
2. Fig. 2c: a single point (2b-euc, ρ = 23.2) dominates; use a log axis.
3. Table 3: `train-only` is missing for `dbl`-style refits; the `dbl` column repeats `mean` and could be dropped.
4. The phrase "250-fold range" is used for z_T and for the injected constant in different places; be consistent.
5. Abstract is 260 words; BSPC allows 250. Highlights: five bullets, all within 85 characters — fine.
6. Section 2.2, Prop. 2: the statement "among corrections whose reference is a function of the target sample mean alone, exactly one is equivariant" is correct but should note that a translation-invariant functional of the centred sample (e.g. a function of the third moment) is also equivariant and is *not* prediction-equivalent; as written the reader may think the equivalence class is larger than it is.
7. The claim that z-score standardisation "returns the same predictions as none" needs a statement of why (LDA is equivariant under invertible affine maps; the shrinkage estimator is not, in general), and a check that the Ledoit–Wolf estimator does not break it. It is empirically exact in the five datasets; say so explicitly.
8. Reference 16 is cited nowhere; reference 17 is cited nowhere. Clean the reference list.
9. The Data availability statement refers to a repository URL placeholder.
10. "six elaborations" in the conclusion versus five in the introduction — fix.

## What would move this to minor

1. **A prevalence audit** (even a small one: 10–15 public pipelines, with the exact lines quoted) — this is the single highest-value addition.
2. **A screen for the benefit**, not only for the risk, even if it is weak; or an abstract reframed around risk.
3. **The classifier result replicated on a second exposed dataset**, or the claim restricted to BCI-2b.
4. **Statistics corrected**: unit-level exact tests (permutation over units), cell-level correlations labelled descriptive, abstract p-values removed or replaced with unit-level values.
5. **A composition experiment** with one alignment method (EA), showing the first-order correction still helps after alignment, and that alignment still helps after the correction.
6. **The residual subsection cut or made quantitative**, and the streaming experiment either done properly or removed.
7. Figures fixed (Fig. 2).
8. The reference list and placeholders cleaned.

I would then be willing to consider minor revision, because the core algebra is correct, the origin sweep is a clean and convincing demonstration, and the certificate is a genuinely useful diagnostic even if it is exact by construction.
