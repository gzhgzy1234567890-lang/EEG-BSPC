# Response to the referee report (Reject)

Manuscript: *Origin equivariance in cross-session EEG decoding: what mean
correction repairs, when it fails, and how to detect the failure*
(manuscript file `BSPC_draft_v9.md` / `BSPC_Manuscript_v9_with_figs.docx`)

We thank the referee for a report that identified two genuine errors in the
theoretical section. We have rewritten the theory rather than defended it, run
the experiments the report asks for, and removed every claim that the evidence
does not support. The main changes are: the uniqueness claim is gone, the
prediction-equivalence condition is corrected to involve the centred weights,
the source-only statistic is demoted to an empirical proxy after we reproduced
the referee's counter-example experimentally, the damage law is replaced by a
signed law that predicts the sign, the standardisation sentence is corrected
and quantified, the cell counts are reconciled, the collapse certificate is
demoted to a diagnostic, and the label-shift statement is restricted to its
assumption. The title, abstract, highlights and conclusion were rewritten to
match.

---

## Major comments

### MC1 — the uniqueness theorem is false (Critical)

**Referee.** γ = μ_B + a with fixed a is equivariant but not prediction-equivalent
to γ = μ_B. Uniqueness does not follow.

**Accepted; the claim is withdrawn.** The referee's counter-example is correct:
γ(X + c1) = μ_B + c + a = γ(X) + c for every c, so the family of equivariant
corrections contains μ + a. Proposition 2 is rewritten as a *characterization of
the family*: γ is equivariant iff γ(X) = μ(X) + h(X − μ(X)) with h
translation-invariant. The text states explicitly that this family is larger than
the sample mean, that μ + a is a member, and that no uniqueness is claimed. The
only statement retained about the sample mean is a parsimony one — it is the
member of the family that adds no data-dependent offset — and it is labelled as
such. The abstract, the introduction's contribution list, Section 6.1 and the
conclusion were rewritten. (Section 2.2, Proposition 2 and the two paragraphs
that follow it; Abstract; Section 1 "Equivariance"; Section 6.1; Section 7.)

### MC2 — the prediction-equivalence condition is imprecise (Critical)

**Referee.** The correct condition is P W(γ − γ') = 0 with P = I − 11'/K, not
γ − γ' ∈ ker(W); and for a finite sample the condition is sufficient but not
necessary.

**Accepted and corrected.** Proposition 3 now states the exact condition,
P W(γ − γ') = 0, with the projector defined in Section 2.1, and proves it by the
class-constancy argument. A paragraph immediately after the proof separates the
two notions: for all inputs the condition is necessary and sufficient; for a
finite target sample, agreement of predictions can occur without it when no
sample crosses the moved boundary. The abstract says "exactly when their
references differ by a vector whose projection onto the centred classifier
weights vanishes; for a finite sample the condition is sufficient but not
necessary". Section 4.6 reports both the exact condition and the observed
agreement (100.0 per cent for the projected correction, because it lies in the
null space). (Section 2.2, Proposition 3 and the following paragraph; Section
2.1 for P; Section 4.6; Section 6.1.)

### MC3 — the source-only statistic has no theoretical standing, and the
### evidence is not independent (Critical)

**Referee.** z_T can be made arbitrarily large by a translation orthogonal to w
while the decision is unchanged; the 11 units are not independent (8 of 11 from
two datasets); there is no leave-one-dataset-out validation.

**Accepted; we ran the counter-example and reframed the statistic.** Section 4.3
is a new experiment: origins of equal norm are injected parallel and orthogonal
to the classifier weights. The statistic is identical in both directions to two
decimals (16.0 against 16.1 on BCI-2b; 0.27 against 0.27 on grasp-and-lift),
while the penalty changes by −0.131 and −0.213 to −0.308 in the parallel
direction and by exactly 0.0000 in the orthogonal one. We state that this is a
counter-example to z_T as a law and not to the mechanism, and we now present z_T
as an *empirical proxy* for the exposure of a feature family, with ρ as the
quantity that carries the mechanism.

We also did what the referee asked in the last paragraph of MC3: a fair
comparison with a source-only indicator related to the decision direction.
Define

  z_w = ||P W μ_A|| / (√K σ_s),

which uses only the source session — the fitted weights, the source mean and
the score spread. It is invariant to a translation orthogonal to W *by
construction*, so it passes the test that the norm-based z_T fails. It is also
better at every level: dataset level −0.90 (p = 0.035) against −0.80
(p = 0.10); unit level −0.855 (p = 0.001) against −0.755; cluster-bootstrap
interval [−1.00, −0.60] against [−1.00, −0.28]; cell level −0.502 against
−0.382. **z_w is now the screen the paper recommends; z_T is retained only as
the naive alternative whose failure the direction experiment measures.**

The independence problem is addressed by changing the level of inference. The
primary analysis is at the dataset level (n = 5), where the projected statistic
is significant. The unit-level analysis is retained but its uncertainty is
estimated by a **cluster bootstrap that resamples datasets**, not units. The
permutation test over the eleven units that the earlier draft reported is
removed, and the 845-cell correlation is labelled descriptive. The operational
ranges of Section 5 are labelled "descriptive of the eleven units studied, not
validated thresholds".

A **leave-one-dataset-out** evaluation is now reported: fitting log z_w against
the penalty on four datasets and predicting the fifth gives median absolute
errors of 0.021, 0.027 and 0.075 on grasp-and-lift, NER2015 and SEED, and
underestimates on the two BCI datasets (BCI-2b: predicted −0.074 against
observed −0.149). We report the failures as well as the successes and say that
four datasets are not a training set. (Section 4.3 new; Section 4.4 rewritten;
Section 2.3 Equation (2b); Section 5; Section 6.4.)

### MC4 — the damage law is misread and cannot explain the sign (High)

**Referee.** The coefficient cφ(c) peaks at c = 1 and decreases beyond, so
"a better decoder is more exposed" is not general; and ρ is unsigned, so it
cannot determine the sign, which explains the SVM result.

**Accepted; both points are incorporated.** Section 2.3 now states the
expansion with the correct coefficient, says explicitly that the sensitivity
peaks at aligned balanced accuracy ≈ 0.84 and declines beyond, and withdraws the
sentence the referee quotes. The signed law is new: with s = w'μ_A/σ_s the extra
displacement of the one-sided pipeline and t* the displacement of the aligned
threshold from the target optimum,

  Δ = BA(c, t* − s) − BA(c, t*),

which is negative when the displacement moves the threshold away from the
optimum and positive when it moves it closer. Section 4.5 measures t* (using
target labels, for analysis only) and compares the predicted sign with the
observed one: 0.97/0.93/0.83 on BCI-2b, 0.92/0.89/0.83 on BCI-2a,
0.90/0.80/0.83 on grasp-and-lift for LDA/logistic/SVM. The text says explicitly
that ρ cannot determine the sign and that this is a limitation of Equation (2),
not of the mechanism. (Section 2.3 rewritten; Equation (4) new; Section 4.5 and
Table 6 new.)

### MC5 — standardisation is not equivalent to two-sided centring (High)

**Referee.** (X_B − μ_A)/s_A ≠ (X_B − μ_B)/s_A; the 100 per cent agreement
cannot be a general identity, and Ledoit-Wolf shrinkage breaks the affine
equivariance that would make it one.

**Accepted; the sentence is withdrawn and replaced by a quantified statement.**
Section 4.1 now separates three operations: (i) standardising with source
statistics, (ii) centring each session, (iii) centring inside the standardised
space. It states that (i) makes the pipeline equivariant and makes the two
centrings coincide *inside that space*, but is not the same transformation as
(ii), differing on the target by (μ_B − μ_A)/s_A. The 100 per cent agreement
between `z-score` and `none` is reported as an empirical fact about LDA with
Ledoit-Wolf shrinkage, and a new Section 4.10 gives the control: with shrinkage
set to zero, where the 256-dimensional grasp-and-lift covariance is
rank-deficient, the agreement falls to 51.8 per cent. (Section 4.1 rewritten;
Section 4.10 new; Section 5 Step 2 corrected.)

### MC6 — cell counts and statistical units are inconsistent (High)

**Referee.** NER2015 uses 320 ordered pairs while others use chronological
pairs; Table 5 claims 60 cells but BCI-2a has 9; Table 7 gives SEED 60 cells but
the total is 45; "61 subject-session units" is 61 subjects; hyper-parameter
settings are treated as independent observations.

**Accepted; the counts are reconciled and the protocol is stated in one place.**
Table 2 now reports the number of sessions used (18, 27, 45, 80, 12; total 182)
alongside the cells, and Section 3 defines a cell as an ordered session pair.
NER2015 uses both directions of each pair, and the text explains why: the two
directions are not equivalent under a translation because they have different
μ_B. The BCI-2b session choice is explained (the two screening sessions and the
feedback session), and the feedback confound is measured rather than assumed:
the gain is +0.0308 for 1→2, +0.0247 for 1→3 and +0.0433 for 2→3, so the
effect is not carried by the sessions that introduce feedback. A new paragraph
"Sub-sampling, where it is used" lists every analysis that does not use all
cells and why (classifier sweeps on grasp-and-lift and NER2015: 60 of 336 and
320; direction experiment: 60 cells in each of two datasets). The calibration
analysis now uses every cell (108, 45, 336) instead of a 60-cell subsample, and
the classifier sweep uses every cell of BCI-2b (108) and BCI-2a (9). Table
captions give the exact n of each row. The statement "61 subject-session units"
is replaced by "61 subject units and 182 session units". The hyper-parameter
settings of Section 4.5 are in a different table (Table 6) and are described as
settings of one classifier family on one dataset, not as independent
replicates. (Section 3 rewritten, including Table 2 and the sub-sampling
paragraph; Section 4.5 and Table 6; Section 4.7 and Table 8.)

### MC7 — the collapse certificate is algebra, not a discovery (High)

**Referee.** Proposition 5 restates the definition; `len(set(pred)) == 1`
already detects collapse; the contribution should be downgraded or strengthened.

**Accepted; downgraded.** Section 2.5 is retitled "The collapse identity" and
states in the first sentence that it is an identity. It says explicitly that
counting the distinct predicted classes performs the same check and that the
identity adds no information beyond the scores it is computed from; it is
presented as an operational way to see *why* a classifier is at chance, not as a
detector. Section 4.8 says that the 124/124 agreement is a check of the
implementation rather than evidence of a capability, and the abstract and
highlights no longer list it as a contribution. The one substantive use — that
chance-level balanced accuracy is not the same as collapse, 180 cells at chance
versus 124 collapsed, concentrated in the imbalanced dataset — is retained and
stated as such. (Section 2.5; Section 4.8; Abstract; Highlights.)

### MC8 — practical importance is not established (High)

**Referee.** Is this an EEG-specific scientific problem or a generic
preprocessing inconsistency? The one audited example is correct by construction.

**Partially accepted; the framing is narrowed.** The introduction now says that
the paper is about implementation consistency and does not claim that the
mistake is common. Section 6.4 keeps the audit and states its result plainly:
the MOABB example fits every transform inside the training fold, so it is
equivariant by construction and cannot exhibit the failure; the exposure is in
pipelines that patch a normalisation step at prediction time. We put no number
on the size of that population and say so. What the paper offers instead of a
prevalence estimate is a one-line test that settles the question for any
particular codebase, and the direction experiment that shows what the risk is a
function of. (Section 1; Section 6.4 first limitation; Section 5 "The unit
test".)

### MC9 — the label-shift statement is too absolute (High)

**Referee.** Under p_B(x|y) = p_A(x|y) the prior is estimable (Saerens et al.);
and the mean-offset decomposition in the earlier draft omits the prior-mixing
term.

**Accepted; the algebra and the claim are corrected.** Equation (5) now reads

  μ_B − μ_A = ḡ + Σ_k π_kB h_k + Σ_k (π_kB − π_kA) m_k^A ,

with the prior-mixing term written out and described as present even when
nothing about the class-conditional distributions changes. The identifiability
sentence is restricted: under the label-shift assumption the priors are
identifiable from unlabelled data and can be estimated by the EM procedure of
Saerens et al. [12]; without it, a prior change and a class-conditional offset
are confounded. Section 4.6 reports the consequence: the label-based correction
adds 0.013 on NER2015, the one dataset whose priors change substantially, and
nothing on the four balanced ones. (Section 2.4 rewritten; Section 4.6; Section
4.9.)

### MC10 — conclusions contradict Table 6 (High)

**Referee.** NER2015 shows +0.013 for the label-informed correction; the paper
cannot say that elaborations do not help.

**Accepted.** The abstract no longer contains that claim, and Section 4.6 states
the numbers and says in terms that the earlier summary sentence was wrong:
labels change nothing on the four balanced datasets and gain 0.013 on NER2015,
which is what Section 2.4 predicts. The conclusion now says that the
prediction-relevant content of a correction is PWγ and that corrections agreeing
there are the same pipeline — a statement about equivalence, not about
optimality. (Abstract; Section 4.6; Section 7.)

### MC11 — the protocol is transductive and the online experiment is weak (Medium–High)

**Referee.** Using the whole target session to estimate μ_B is transductive;
the running-mean result depends on trial order; BCI-2b session retention needs
justification.

**Accepted.** Section 6.4 adds a paragraph stating that both forms of the
correction use the whole target session, that this is legitimate only under a
protocol that allows unlabelled target data, and that a strictly inductive
deployment is not covered. Section 5 keeps the two-order streaming experiment
and the conclusion drawn from it (a running reference does not remove the need
for a calibration block when the trial order is block-structured). The BCI-2b
session choice is now explained in Section 3, and the feedback confound is
measured by the pair-type breakdown reported there. (Section 6.4; Section 5;
Section 3.)

---

## Minor comments

1. **Scope of Proposition 4.** The proposition now says explicitly that it holds
   for a *fixed* model and does not apply to refitted or standardised pipelines,
   and the paper reports accuracy and calibration rather than AUC as the
   quantities of interest. (Section 2.2, Proposition 4.)
2. **Definition of ρ.** Equation (2) now defines ρ for K classes as
   ||P W μ_B||/(√K σ_s) with σ_s the SD of the source scores, and gives the
   binary reduction; the class-constant part is removed before the norm.
   (Section 2.3.)
3. **Bootstrap intervals.** Table 8 now reports the median per-subject ECE and a
   bootstrap interval of the mean over subjects, computed on every cell, with a
   sentence noting that the pipelines share subjects and that a paired test
   would be more efficient than comparing two marginal intervals. (Section 4.7.)
4. **Monotonicity of the sweep.** Addressed by the direction experiment: the
   sweep is no longer claimed to be monotone in the size of an arbitrary
   translation; Section 4.3 shows that the effect is zero for a translation in
   the null space of the weights, and the text states that the sweep of Section
   4.2 uses one direction only. (Section 4.3.)
5. **Physical interpretation of the origin.** Section 6.2 now says that the
   physical reading should not be pushed too far: an amplifier gain change and a
   reference-electrode change both alter the covariance, and a reference change
   is not a pure translation of the feature vector; "origin" describes the
   feature-space effect, not its electrical cause. (Section 6.2.)
6. **Calibration explanation.** The sentence about features "not being
   probabilities" is removed and replaced by the correct statement that a
   classifier can map arbitrary features to calibrated probabilities; the poor
   SEED calibration is attributed to task difficulty for a linear model on these
   features. (Section 4.7.)
7. **Online stability.** The random-order streaming result is now reported
   alongside the recorded-order one, and Section 6.4 states that the random-order
   variant uses a single draw per cell rather than a distribution over orderings.
   (Section 5; Section 6.4.)

---

## Summary of the new material

| item | new content |
|---|---|
| Section 2.2 | Proposition 2 as a family characterization; Proposition 3 with P W |
| Section 2.3 | signed law, Equation (4); corrected expansion |
| Section 2.4 | corrected mean decomposition, Equation (5); restricted identifiability |
| Section 4.3 | equal-norm direction control (Table 4) |
| Section 4.4 | dataset-level + cluster bootstrap statistics |
| Section 4.5 | sign prediction across nine settings (Table 6) |
| Section 4.10 | shrinkage control for the z-score identity |
| Section 3 | reconciled cell/session counts and sub-sampling disclosure |
| Section 4.7 | calibration on every cell with intervals (Table 8) |

Every number in the new material comes from `pv8_exp11.py` (direction and sign),
`pv8_exp12.py` (cluster statistics, full-cell sweeps, shrinkage control) and
`pv8_cal.py` (calibration intervals), whose plain-text output is archived with
the code.
