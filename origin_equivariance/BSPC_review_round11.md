# Referee report, round 11 — BSPC submission v17

**Recommendation: Minor revision.**

The two items I set as the condition for minor revision are addressed. The paper
is internally consistent, its claims are proportionate, and the practical
premise now has evidence behind it, small but real.

## The two items

**1. The code audit (Section 4.11).** The authors inspected three components of
the frameworks a cross-session pipeline actually uses — the MOABB cross-session
evaluation, the MNE `Scaler`, and the Braindecode causal
`exponential_moving_demean` — and recorded, for each, which data the reference is
taken from. All three take it from the training fold or from a causal running
mean; none centres the target at prediction time. The authors state that the
audit is small, that it establishes that the failure is an implementation choice
rather than a property of the frameworks, and that they did not audit the
population of custom pipelines. That is the honest version of what I asked for,
and it is enough: the paper no longer rests its practical premise on a
hypothesis alone, it rests it on three inspected implementations plus a test that
settles the question for any codebase.

**2. The tables.** The two parameterisations are now merged into one table with
both columns, so the oracle numbers no longer stand alone while the model's
parameterisation sits in a footnote. This is the right fix and better than the
swap I suggested.

## Minor items

1. **Highlights.** Add one bullet for the audit and the boundary result; the
   current five are mostly algebra and the BSPC reader will look for what can be
   used.
2. **Section 5.** The z_w ranges (0.35, 4) are descriptive; the sentence now
   implies they are thresholds. Say that they are the ranges observed on the
   eleven units.
3. **Fig. 1 caption** now matches the text ("decays toward 1/K without reaching
   it uniformly"), which is correct; make sure the corresponding sentence in
   Section 4.2 keeps the per-dataset numbers, which it does.

## Assessment

The manuscript is now an audit in the sense the title promises: one definition
per quantity, numbers that agree across abstract, results, discussion and
conclusion, an explicit boundary statement for every claim, a small but real code
audit, and two negative results reported as negative. The characterization is a
corollary of linear discriminant theory and the paper says so; the empirical
content is the measured boundary and the failure modes, and that is what BSPC
publishes as a methods study.

I recommend minor revision. The three items above are editorial.
