# REVIEWER_1_REPORT.md — Methods and statistics

Internal adversarial review. Not an external referee.

Manuscript: BSPC_Candidate_V8 (19 pages, 10,244 words), commit 5518bcc.

## Summary judgement

**Major revision.** The statistical machinery is now largely coherent, but three issues would still stop me from
recommending acceptance.

## M1. The 2a result is described as exploratory but the numbers are quoted like a result (Section 4.8, p. 14)

The subsection reports +0.0705 with a Wilcoxon p of 0.0039 and then says the numbers are exploratory because the
representation was chosen after a run. That is honest, but a reader will still take 0.0705 as the paper's positive
result on BCI-2a. Severity: moderate. Requirement: either mark the number inline as exploratory at first mention,
or move the 2a factorial entirely to the supplement and keep 2b as the only positive BCI claim.

## M2. The filter contrast is still not a future-information contrast (Section 4.8, p. 14)

The paper says this, but the abstract repeats "-0.011, p = 0.13" without the caveat. A reader may read it as an
information-leak effect. Severity: moderate. Requirement: add "(implementation difference, not only future
access)" to every abstract-level mention.

## M3. Holm correction is asserted, not performed (Section 4.8, p. 14; STATISTICAL_ANALYSIS_PLAN)

The family has one live test because SEED is blocked, so the correction is vacuous; the paper says "uncorrected".
That is fine, but the plan says "Holm across the pre-specified tests", which suggests a performed correction.
Severity: low. Requirement: state in the plan that with one live test Holm is the identity, or drop the Holm
sentence.

## M4. The certificate is validated on three subjects only (Section 2.3, p. 6)

Three subjects, 241 scored trials, exact agreement. That is a demonstration, not a validation. Severity: low.
Requirement: say "on three subjects" explicitly (it does) and do not use "validated" anywhere.

## M5. Sleep-EDF hierarchy

The audit reproduces -0.1023 [-0.1145, -0.0900] with 32/32. Good. But per-class recall is only reported for the
D5 subset; the main table has no recall. Severity: low.

## Verdict

Major revision. M1 and M2 are textual but consequential; M3 is bookkeeping.
