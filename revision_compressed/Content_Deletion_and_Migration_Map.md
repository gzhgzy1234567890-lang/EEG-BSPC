# Content deletion and migration map

Every removal below was either merged into a surviving paragraph or moved to the supplement. No negative result, no
limitation and no statistical detail was deleted outright.

| original location | content | action | rationale | kept where |
|---|---|---|---|---|
| §2.1 | notation paragraph | condensed into one paragraph plus reference to S1 | the full notation is mechanical | §2.1, S1 |
| §2.2 proofs | four full proofs | propositions kept, proofs replaced by one-line arguments plus S2 | the proofs are unchanged and already archived | §2.2, S2 |
| §2.3 | derivation of the second-order loss | kept, shortened | it carries the mechanism | §2.3, S2 |
| §4.1 | two-pipeline equivalence and standardisation | condensed to one paragraph; Table 3 and Fig. 1 unchanged | the identity is stated once | §4.1 |
| §4.2 | origin sweep paragraph | condensed into the section opener | Fig. 2 unchanged | §4.2 |
| §4.2.1 | estimator ranking prose | replaced by two sentences; full ranking already in S34/S35 | the ranking is not the claim | §4.2.1, S34, S35 |
| §4.3 | synthetic regimes prose | two sentences; Table 4 and Fig. 3 unchanged | superseded by the controlled factorial | §4.3, S34 |
| §4.4 | strength and memory prose | merged into one section with the memory sweep | the two answered one question | §4.4 |
| §4.6 | decomposition | kept in full, tightened | core mechanism | §4.6 |
| §4.7 | factorial | kept, tightened | core mechanism | §4.7 |
| §4.8 (old) | memory and time scales | merged into §4.4 | duplicated §4.4 | §4.4 |
| §4.9 (old) | mechanistic limitations | merged into the Discussion | duplicated 5.1 | Discussion |
| §4.10 | independent validation | kept as §4.8 | evidence class must stay visible | §4.8 |
| §4.11 | filtering and alignment | kept as §4.9 | protocol audit | §4.9 |
| §5.1 | limitations list | merged into one Discussion section | duplication with 4.9 | Discussion |
| §6 | conclusion restating every result | rewritten to 144 words | it repeated Results | §6 |
## Part C. What was corrected after the independent review of 1 November

The independent reviewer found four mathematical errors in Section 2.2 of the compressed draft, one of which
contradicted Table 1. All four were reproduced and corrected; none needed a new experiment.

| item | before | after |
|---|---|---|
| Proposition 1 | "the mean-corrected pipeline is unchanged; the uncorrected pipeline is not" | uncorrected and mean are both equivariant; only the one-sided pipeline is not |
| Proposition 2 | "if and only if gamma differs from the sample mean by a constant" | the condition is gamma(X + c1) = gamma(X) + c, satisfied by the mean, the median and a training reference plus a constant |
| Proposition 3 | "iff the correction lies in the span of the weights" | iff F W d = 0, i.e. d in the null space of F W |
| Proposition 4 | rankings of raw scores and of pairwise margins are the same transformation | confined to one score function; the cross-function claim is withdrawn |
| proofs | pointed at S2, which is a direction-control experiment | new S37 holds the four proofs |
| factorial design | "two levels of each factor" | 2 x 3: composition at 2 levels, drift at 3 |
| strength optimum | "the interval still touches 1.0 at one standard deviation" | with composition present both intervals exclude 1.0; without it both include it |
| sign convention | "costs 0.0034 [-0.0046, -0.0020]" | signed change -0.0034 [-0.0046, -0.0020] |
| Table 8 memory row | attributed the memory result to the strength grid | strength grid varies strength; the memory evidence is the one-to-three-block sweep on real data |
| manifest CSV | 10 of 11 rows missing the commit column | uniform 8 columns, commit in every row |
| checker | hard-coded Windows path | resolves its inputs relative to the archive and runs from the unzipped package |
| Figure 1-5 files | absent from the package | `Figures_main/` added with the five figures extracted from the submitted DOCX |
