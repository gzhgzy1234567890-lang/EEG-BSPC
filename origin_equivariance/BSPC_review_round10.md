# Referee report, round 10 — BSPC submission v16

**Recommendation: Major Revision** (previous round: Reject). One substantive
item and one structural item keep this from minor revision.

## The consistency problems are gone

The last report's fatal items were internal: two definitions of `z_w`, stale
numbers left in the Discussion, a missing table, revision-history language. The
authors have discarded the accumulated draft and rebuilt the paper from one set
of numbers. I checked the built document:

- one definition of the statistic, with the scale from the centred scores, the
  invariance proved and verified to 4 × 10⁻¹⁶ under the transformation that broke
  the previous version;
- the six-dataset association is reported as −0.77 with exact p = 0.103 and the
  former −0.94/p = 0.017 appears nowhere; the held-out median is 24.4 and the
  within-dataset AUC 0.515, consistently across abstract, results, discussion and
  conclusion;
- ten tables used in order, four figures, one numbering per equation, and ρ and s
  distinguished (they were conflated before);
- no revision-history language.

This is what I asked for, and it changes the character of the manuscript: it
reads as a study rather than as a sequence of replies.

## What still blocks minor revision

**1. The code audit.** The paper's practical premise is that a pipeline can be
built with an inconsistent centring reference. The authors have one audited
example, and it is correct by construction. Without a small structured audit —
five to ten released preprocessing scripts, with the reference each one uses —
the premise stays a hypothesis. This has been my first or second item in four
consecutive reports and it is the only thing standing between this manuscript and
a minor-revision decision.

**2. The Gaussian model's status, one last time.** Section 4.5 is now honest: the
oracle parameterisation is described as oracle-assisted and its circularity is
stated, the model parameterisation is reported beside it, and the text says the
model is "a mechanism with a measured range of validity". But Table 7 still leads
with the oracle numbers, and a reader who stops at the table will take r = 0.99
as the model's performance. I would swap the tables, or merge them so that the
model's parameterisation is not a footnote to the oracle one.

## Minor items

- Fig. 1's caption says the one-sided pipeline "slides and stops"; the text now
  says it does not reach 1/K uniformly within the sweep. Make the caption match.
- The Highlights are five bullets and the fifth is about the statistic's failure;
  that is fine, but the first three describe the algebra. Consider one bullet on
  the boundary result, which is the part a BSPC reader can use.
- Section 5's z_w ranges (0.35, 4) are descriptive; say so in the same sentence
  as the numbers.

## Assessment

The paper is now a consistent audit of a preprocessing step: what the correction
is, when it fails, how the failure scales with the classifier's threshold error,
and what a source-only statistic can and cannot see. The negative results are
reported and the claims are proportionate. Add the code audit, reorder Table 7,
and I expect to recommend minor revision.
