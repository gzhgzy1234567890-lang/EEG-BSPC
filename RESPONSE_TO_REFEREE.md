# RESPONSE_TO_REFEREE.md

Point-by-point response to the Major Revision report of 1 November 2026. Every claim below was checked by direct
computation before any edit; the verification script is `origin_equivariance/src/verify_referee_claims.py` and its
output is quoted where relevant.

## MC1 — second-order coefficient

**The referee is right and the proof was wrong.**

- Shipped: BA(0) − BA(d) = d²/(2σ²)·φ(a/σ).
- Correct: a d²/(2σ³)·φ(a/σ), since BA''(0) = φ'(a/σ)/σ² = −a φ(a/σ)/σ³.
- Local check: a=2, σ=1, d=0.2 gives loss 0.002167; the shipped formula gives 0.001080; the corrected one 0.002160.
  The referee's numbers are reproduced exactly.
- Why the tests missed it: every parameter choice in the old test had a = σ, where a/σ³ = 1/σ².
- Fix: THEORY_PROOFS.md Prop 3 rewritten; the sign remark on BA'' corrected; the regression test now evaluates the
  coefficient at (a, σ) = (2, 1), (0.5, 2), (2, 0.7) and asserts a relative error below 1e-4. It reports 8e-8,
  7e-8 and 9e-7.
- Also checked: no simulation or table used the second-order coefficient. The D1 grid depends on the sign of the
  effect, which is unchanged; the 50/50 result stands.

## MC2 — constrained optimal weight

**The referee is right on all three points.**

- The residual is r(λ) = b − λ(c + b) = (1 − λ)b − λc; the document had +λc.
- The weight must be clipped: λ* = clip_{[0,1]}(b/(b+c)), undefined when b + c = 0.
- Worked cases now in the proof: (0.5, −0.4) → 1 (the document printed 5); (0.8, 0.2) → 0.8; (0, 0.5) → 0;
  (0.5, −0.5) → undefined, all weights equivalent.
- The regression test checks the residual at λ = 0, 0.5, 1 and the numerical optimum of λ against the clipped
  formula (0.533 against 0.533).

## MC3 — threshold dimension

**The referee is right; the model now defines the threshold in feature space.**

- The rule is x > t, a score-space threshold is w t, and substituting a raw score threshold into BA(t) is correct
  only when w = 1.
- The referee's example is reproduced: a=2, σ=1, w=4, τ=1 gives 0.9200 if τ is misread as a feature threshold and
  0.9739 with t = τ/w = 0.25.
- The remark after Proposition 2 now states the projection argument for D dimensions and the equal-variance
  restriction it carries.

## MC4 — Proposition 5 and the certificate tie convention

**The referee's counterexample is correct and is now the proof.**

- With features (0.4, 1.2, −1.2, −1.2) and displacement 0.5, labels (+,+,−,−) give −0.250 and (−,+,−,−) give
  +0.167. Reproduced locally.
- Proposition 5 is therefore restated as a finite-sample non-identifiability result and proved there; the population
  statement (a positive expected gain requires drift b) is kept separately, because the two answer different
  questions. The word "open" is removed.
- The certificate now states its tie convention: strict inequality when no corrected score ties the top score,
  non-strict exactly for the classes that tie.

## MC5 — evidence grading

**Accepted.** The manuscript now carries a single evidence-class column and no longer calls the five development
datasets a confirmatory chain. The relevant sentence in Section 2.3's neighbourhood was rephrased; a consolidated
table is being added in this revision. The current classes are: CONFIRMATORY (sleep-EDF cassette, grasp-and-lift
artefact), PROSPECTIVE-IN-EXPLORED-DATA (BCI-2b, D3, D5), EXPLORATORY (2a and every secondary representation),
ORACLE-DIAGNOSTIC (block-wise decomposition), TRANSDUCTIVE (BBSE), EXPLORATORY-INDEPENDENT (P300, ERRp), and one
WITHDRAWN row.

## MC6 — "inert" overstates the null results

**Accepted.** The word is removed from the abstract-level claims. The two external results are now reported as
"no reliable gain or loss was observed under this protocol", with a stated equivalence margin of ±0.02 on balanced
accuracy: the P300 mean is −0.0005 with 7/16 positive and the ERRp mean is −0.0044 with 6/16 positive; both point
estimates lie inside ±0.02, but the intervals are wide and the ERRp decoder is near chance, so neither is presented
as evidence of equivalence.

## MC7 — mechanism wording

**Accepted.** The text says the harm is *located* in the class-mix component under an oracle diagnostic, that six
class-set matching schemes show robustness to that stratification, and that the root cause of the composition
change is not identified. No physiological mechanism is claimed.

## MC8 — novelty relative to SPDIM

**Accepted and already implemented before this report**: SPDIM [23] is cited in the related-work paragraph with the
qualitative claim attributed to it, and the contribution is limited to the first-order displacement formula, the
certificate, and the protocol audit. The response repeats this so the second round can check it directly.

## MC9 — archive consistency

**The referee is right; the archive was stale.**

- MANIFEST.md said 18 pages and 9,345 words against a 20-page, 11,069-word manuscript. Regenerated; the build now
  reads the counts rather than carrying literals.
- The quality gate said 93 while the status said 95. Both are superseded by the revision-2 gate at **89**, which
  records the hard-gate failure rather than hiding it.
- FREEZE_RECORD.md was refreshed.
- The referee's observation that the ZIP contains no executable source is correct and is now stated in the manifest:
  the package is an audit archive, the code lives in the repository.

## Minor comments

1. Pair counting fixed: "three per subject, 27 in total"; cells are separately defined as pairs × representations.
2. Symbols unified in the proof document; the manuscript now states t is a feature-space threshold.
3. References [23] and [25] now carry venue, year and full author lists.
4. The abstract is being shortened in the next revision; the current 262-word version still carries too many
   secondary numbers.
5. The practical paragraph no longer suggests that partial strength is a validated safe setting.

## The honesty point

The referee's central criticism — that a self-audit reporting "theory verified" cannot be treated as independent
evidence of correctness — is accepted without qualification. Three of the four mathematical items were errors, not
ambiguities. The gate that passed them has been regraded downward and the failure is recorded in
FINAL_QUALITY_GATE.md rather than quietly overwritten.

## Round 2 of the referee response

| item | status |
|---|---|
| MC5 evidence tiers | fixed: the five-test family is pre-specified but explicitly not five independent confirmations; SEED preprocessing, development reuse of 2a/2b and the two failing datasets are stated together |
| MC6 equivalence | fixed: inert removed; P300 -0.0005 [-0.0024, +0.0012]; ERRp -0.0044 [-0.0166, +0.0075]; 0.02 margin quoted with the caveat that the decoders are too weak for an equivalence claim |
| MC7 mechanism | fixed: the text claims only that the harm is located in the class-mix component under an oracle diagnostic |
| minor 1 | pair counting corrected |
| minor 3 | references 23 and 25 completed |
| minor 4 | abstract reduced to 219 words |
| minor 5 | partial-strength advice removed |
