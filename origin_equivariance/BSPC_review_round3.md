# Referee report, second round — BSPC submission

**Manuscript:** "Origin equivariance in cross-session EEG decoding: what a mean correction repairs and how to screen for the risk" (v8, round 3)

**Recommendation: Minor revision.**

The authors have answered the structural objections of my first report, and in two places they have changed the paper's claims to fit what the data support. The algebra is correct, the causal demonstration is clean, and the negative results are stated as negative results. What remains is a list of small items, none of which requires a new experiment.

## What the authors fixed

1. **Statistics.** The unit-level result is now an exact permutation test over the eleven units (p = 0.009), and every cell-level correlation is labelled descriptive. The abstract no longer quotes a cell-level p-value. Accepted.
2. **Second exposed dataset.** The classifier sweep is replicated on BCI-2a (classes 1 vs 2, thirteen settings): Spearman −0.654, p = 0.015, same sign reversal at ρ ≈ 1. Accepted.
3. **Composition with second-order alignment.** The new paragraph shows that the mean correction still gains 0.0725/0.0236 inside the Euclidean-aligned representation and 0.0417/0.0452 inside the tangent representation. This is the experiment I asked for, and it establishes that the two corrections are not substitutes. Accepted.
4. **Prevalence.** The authors audited the MOABB cross-session example and found that it fits every transform inside the training fold, so it is equivariant by construction. They then reframed the claim: the exposure is a property of custom pipelines that patch a normalisation step at prediction time, not of framework code. This is a narrower claim than the one I objected to, and it is one the manuscript can support. Accepted, and the reframing improves the introduction.
5. **Streaming.** The random-order result has been replaced by a comparison of the recorded order and a random order. The recorded order fails on the block-structured sessions (SEED 0.672 against 0.709; grasp-and-lift 0.678 against 0.794), and the authors now say that a running reference does not remove the need for a calibration block. This is the right conclusion and it is stronger than the previous paragraph. Accepted.
6. **Decision-space form.** The new corollary and Section 4.6 give the correction a deployment form that needs K numbers instead of D, verified to 0.0e+00 against the feature-space form for three linear families on three datasets. This gives the paper the method component that was missing. Accepted.
7. **Presentation.** Figures remade, captions added, references cleaned (18 cited = 18 listed), abstract at 250 words, the residual subsection shortened and downgraded.

## Minor items that remain

1. **Calibration needs a per-subject spread.** Table 7 reports ECE averaged over 60 cells. Please report the per-subject ECE with a bootstrap interval, or restrict the calibration claim to BCI-2b where the probability model is meaningful. (No new experiment; the numbers exist.)
2. **One more audited example.** The MOABB audit is a single script. One more — Braindecode's BCIC-IV-2a tutorial or a pyRiemann example — would let Section 6.4 say "two published examples" instead of one. If neither exhibits the failure, say so; the point is now about where the exposure lives, not about its frequency.
3. **Non-linear models.** Section 4.6 says the decision-space form is an approximation for non-linear models and that it was not tested. Please either test it on a small non-linear model (a kernel or a shallow network on BCI-2b) or state explicitly in the limitations that the corollary covers affine models only.
4. **Highlights.** The highlights still describe the paper of the previous round; add the decision-space deployment form and drop one of the weaker bullets.
5. **Fig. 2b** legend overlaps the data; move it or place it outside.

## Assessment

The paper now has: a characterization theorem, a verified corollary giving a deployment form, a causal demonstration that isolates the origin, two mediators validated on independent datasets, an exact diagnostic that separates collapse from chance, an honest account of what cannot be repaired, and a procedure. For BSPC this is a methods contribution of the kind the journal publishes, and the negative results are reported in a way that a reader can use.

I recommend minor revision. Items 1, 3, 4 and 5 are editorial; item 2 is one short audit.
