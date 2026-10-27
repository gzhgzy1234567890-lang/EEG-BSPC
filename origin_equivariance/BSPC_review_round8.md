# Referee report, round 8 — BSPC submission v13

**Recommendation: Major Revision** (previous round: Reject).

The authors have taken the rejection seriously and restructured the paper
rather than decorating it. Three of my four substantive objections are closed,
and the fourth (novelty) is now handled by narrowing the claim to what the
evidence supports. I do not think the paper should be rejected in this form.

## The four objections

**1. Binary model on four-class data — closed.** The 2a cells are now explicitly
the two-class subproblem (classes 1 and 2), stated in Section 3 and in the Table
7 caption, and no four-class claim remains.

**2. Gaussian parameterisation — closed, and the check hurts the paper in the
right way.** The authors recomputed the law with c = (m₁ − m₀)/(2σ_w) and a
within-class scale, as the model requires, and report both variants side by side:
the correlation for BCI-2b falls from 0.989 to 0.861 and the MAE rises from
0.013 to 0.057; on grasp-and-lift from 0.649 to 0.271; on NER2015 the within-class
scale is not estimable. They also state the circularity: in the old variant c is
computed from the aligned accuracy that also appears in the observed change. The
paper no longer calls the model a predictive law. This is exactly the correction
I asked for, and the honest reporting of the weaker parameterisation is more
valuable than the stronger number would have been.

**3. Target-label dependence — closed by deletion of the claim, not by a new
estimator.** The law is described as a descriptive decomposition, the word
"predictive" is gone from the abstract and the conclusion, and the split-sample
results remain as evidence about the *sign* only. I would have preferred a
label-free estimate of t*, but the authors' choice is defensible given the
weaker model fit.

**4. The screen — closed by demotion.** The external threshold test (specificity
0.000 on SEED-IV) is in the paper, the screen is an exploratory section, the
title no longer promises it, and the abstract says it fails as an operational
rule. The six-dataset association is presented as six observations, with the
correlation between SEED and SEED-IV acknowledged.

## The remaining objection, and why it no longer blocks

My objection was that the theory is a corollary of affine classification and
that the empirical part must therefore carry the paper. With the screen demoted
and the law weakened, what remains is: a correct characterization, a causal
origin experiment, a failure mechanism (threshold displacement and collapse) with
its sign explained, an honest account of the boundaries by feature family and
classifier, and two negative results (the benefit is not screenable; the
operational screen does not transfer). That is a narrower paper than the one
submitted, and it is the one the evidence supports. BSPC publishes this kind of
methods study, and Section 6.1 now separates the three kinds of statement
properly.

## What still blocks minor revision

1. **An audit.** The report I wrote last round asked for a systematic audit of
   public pipelines; the paper still has one audited example, and the authors now
   state it as an open problem. One more example, or a small structured audit of
   five to ten released preprocessing scripts, would let the practical motivation
   stand on evidence rather than on a hypothesis.
2. **The mechanical legacy of eight revisions is not fully cleaned.** The
   equation numbering is fixed, the duplicate table is gone and the meta-language
   is removed, but the paper still reads in places like a reply to referees
   ("we report both variants", "the model check"), and the Highlights file has
   not been regenerated for this version.

## Assessment

The paper has moved from "claims the evidence does not support" to "claims the
evidence supports, with the failures reported". If the authors add one audited
example and polish the narrative voice, I expect to recommend minor revision.
