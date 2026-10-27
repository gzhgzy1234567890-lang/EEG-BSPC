# Referee report, round 4 — BSPC submission v9

**Manuscript:** *Origin equivariance in cross-session EEG decoding: what mean
correction repairs, when it fails, and how to detect the failure*

**Recommendation: Major revision** (previous round: Reject). The theoretical
errors are corrected, the claims now match the evidence, and two new
experiments materially strengthen the paper. What keeps this from a minor
revision is one missing validation and one missing audit; both are bounded.

## What the authors fixed, in the order of my previous report

**MC1 (uniqueness).** Withdrawn correctly. Proposition 2 is now a
characterization of the equivariant family, the counter-example γ = μ_B + a is
acknowledged in the text, and no uniqueness is claimed. The abstract, the
contribution list and the conclusion are consistent with the new statement.

**MC2 (prediction equivalence).** Corrected to P W(γ − γ') = 0 with the
projector defined, and the finite-sample caveat — sufficient, not necessary —
is stated in the proposition, the abstract and the discussion. This is now
mathematically sound.

**MC3 (the screen).** This is the most substantial improvement. The authors ran
the counter-example I constructed: equal-norm origins parallel and orthogonal
to the weights give the same norm-based statistic and penalties of −0.21 and
0.000. They then did what I asked and compared it with a source-only indicator
related to the decision direction, z_w = ||P W μ_A||/(√K σ_s). The projected
statistic is better at every level: dataset level −0.90 (p = 0.035) against
−0.80 (p = 0.10), unit level −0.855 against −0.755, cluster-bootstrap interval
[−1.00, −0.60] against [−1.00, −0.28], and cell level −0.502 against −0.382.
The permutation test over eleven pseudo-independent units has been removed and
replaced by a cluster bootstrap over datasets. A leave-one-dataset-out
evaluation is reported, including where it fails (the predictions are
compressed toward zero on the two BCI datasets). This answers the specific
request.

**MC4 (damage law).** The expansion now has the correct coefficient, the claim
that sensitivity increases with decoder quality is withdrawn, and the signed
law Δ = BA(c, t* − s) − BA(c, t*) is new. The sign is predicted in 80–97 per
cent of cells across nine classifier settings, and the SVM reversal is
explained rather than excused. This is a genuine improvement in mechanism.

**MC5 (standardisation).** The incorrect sentence is withdrawn. Section 4.1
separates the three operations, and Section 4.10 gives the control I asked
for: with shrinkage set to zero the z-score/none agreement falls from 100 per
cent to 51.8 per cent on grasp-and-lift. The claim is now empirical and
bounded, as it should be.

**MC6 (counts).** Reconciled. Sessions are counted (182), cells are defined as
ordered session pairs, NER2015's use of both directions is justified, the
BCI-2b feedback confound is measured (+0.031/+0.025/+0.043 by pair type), every
subsample is disclosed, and the calibration analysis now uses every cell.

**MC7 (certificate).** Downgraded to an identity, with the trivial check
acknowledged in the text. The only substantive use — chance accuracy is not
collapse, 180 versus 124 — is stated as such. This is the right treatment.

**MC9, MC10, MC11.** The label-shift decomposition now carries the
prior-mixing term and the identifiability claim is restricted to the label-shift
assumption with the Saerens reference; the NER2015 gain of 0.013 is reported and
the earlier summary sentence is retracted; the transductive protocol is stated
as a limitation and the streaming experiment now reports both trial orders with
the block-order failure.

**Minors.** ρ is defined for K classes; Proposition 4 is restricted to fixed
models; calibration has per-subject intervals and a note on paired comparison;
the sweep's direction dependence is handled by the new experiment; the
electrical interpretation is qualified; the calibration explanation is
corrected.

## What remains

**1. The screen has still not been validated on a dataset that played no part
in its construction.** The leave-one-dataset-out fit is a step in the right
direction but four datasets are not a training set, and the authors say so. One
additional cross-session dataset — SEED-IV, Alljoined, or any public two-session
set with a different feature family — used *only* as a held-out test of the
sign and rank of z_w would convert the claim from "consistent across our five"
to "replicated outside our five". Without it, the screen remains the weakest
link, exactly as in my previous report.

**2. The prevalence audit is still a single example.** The authors are honest
about it, and the reframing (exposure lives in custom pipelines, not in
frameworks) is defensible. A second audited example would let the paper say
"two published examples, both correct by construction" and would cost a
paragraph.

**3. The sign analysis uses target labels.** t* is estimated from the aligned
target scores, so the sign prediction is descriptive rather than deployable.
This is stated, but a reader will ask what a deployable version would require.
One sentence on that — e.g. estimating t* from the source scores under the
aligned model — would close it.

## Assessment

The paper has moved from "core results are wrong" to "core results are correct
and one of them lacks external validation". The characterization, the direction
control, the projected statistic, the signed law, the full-cell calibration and
the reconciled protocol are all sound. If items 1–3 are addressed, I would
expect to recommend minor revision: item 1 is one experiment on a public
dataset, item 2 is one paragraph, item 3 is one sentence.

I note for the editor that the authors have responded to a reject report by
correcting their theory rather than defending it, which is rare and should be
weighed in their favour.
