# -*- coding: utf-8 -*-
"""Round 3 edits: decision-space corollary, its verification, honest streaming."""
import io

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v8.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)

REPL = []

# 1. corollary after Proposition 3
REPL.append((
"""Proposition 3 follows from the same computation. The two one-sided forms differ only in the sign of the shift; they are the same kind of failure.""",
"""Proposition 3 follows from the same computation. The two one-sided forms differ only in the sign of the shift; they are the same kind of failure.

**Corollary (decision-space form).** For an affine model the correction can be applied to the K scores instead of to the D features: subtracting δ_k = w_k'(μB − μA) from score k returns the same predictions as the feature-space correction, and requires neither the features nor a refit. The two forms are related by Proposition 2, since they differ by exactly W(μB − μA)."""

))

# 2. new subsection before calibration, and renumber the following ones
REPL.append((
"""### 4.6 Probability calibration""",
"""### 4.6 Applying the correction without the features

The corollary of Proposition 2 has a practical consequence for deployed systems: a model that is frozen, wrapped behind an interface, or stored without its feature pipeline can still be corrected, because the correction needs only the K numbers δ_k = w_k'(μB − μA). We verified the equivalence on three linear families and three datasets. For LDA, logistic regression and a linear support-vector machine, on BCI-2b (60 cells), BCI-2a (36 cells) and grasp-and-lift (60 cells), the decision-space form returned predictions identical to the feature-space form in 100 per cent of samples, with a maximum discrepancy of 0.0e+00 and equal balanced accuracy to four decimals (for example 0.7365 and 0.7365 for LDA on 2b, 0.7188 and 0.7188 for the support-vector machine).

The practical difference between the forms is what they require. The feature-space form needs the target features, which in a deployed system means storing them; the decision-space form needs the target scores, which the system already computes, and K numbers rather than D. For the three linear families the two are interchangeable; for a non-linear model the decision-space form is an approximation, and we have not tested it.

### 4.7 Probability calibration"""
))
REPL.append(("### 4.7 The collapse certificate, and the difference between chance and collapse",
             "### 4.8 The collapse certificate, and the difference between chance and collapse"))
REPL.append(("### 4.8 What is left", "### 4.9 What is left"))
REPL.append(("and Section 4.7 shows that the two are different events",
             "and Section 4.8 shows that the two are different events"))
REPL.append(("Section 4.8 measures how much of the residual",
             "Section 4.9 measures how much of the residual"))

# 3. honest streaming paragraph
REPL.append((
"""**Deployment.** For an online system the target mean is not available at the first trial. A running mean, warm-started at the source mean, converges quickly: evaluated on the trials that follow a warm-up of k trials, the running-reference pipeline reaches 0.7335 (k = 5), 0.7349 (k = 10) and 0.7350 (k = 50) against a batch value of 0.7365 on BCI-2b, 0.7090 against 0.7094 on SEED, and 0.7910 against 0.7938 on grasp-and-lift. The correction therefore does not require a calibration session; it requires that the reference be estimated from the same session as the test trial, which is what a running mean does.""",
"""**Deployment, and why the trial order matters.** For an online system the target mean is not available at the first trial, and the natural substitute is a running mean warm-started at the source mean. Whether that works depends on the order in which the trials arrive, and the two orders give different answers. With the trials drawn in a random order, the running reference is close to the batch correction after five trials: 0.7334 at k = 5 against a batch value of 0.7365 on BCI-2b, 0.7086 against 0.7094 on SEED, 0.7911 against 0.7938 on grasp-and-lift, and 0.6105 against 0.6119 on BCI-2a. With the trials in their recorded order the same pipeline is exact on BCI-2b (0.7409 against 0.7365) and clearly worse on the two datasets whose sessions are organised in blocks: 0.6724 against 0.7094 on SEED and 0.6781 against 0.7938 on grasp-and-lift, because the first trials of those sessions belong to one film or one series and are not a sample of the session. A running reference therefore does not remove the need for a calibration block; it moves the requirement to one of two conditions, either an exchangeable trial order or a warm-up that spans the blocks. We report both orders because the random-order result alone would have overstated the method."""
))

# 4. procedure step 2 mention decision-space form
REPL.append((
"""**Step 2 — use the equivariant form.** Centre both sessions and fit on the centred training data, or standardise with training statistics, which is equivalent. A pipeline that does this is invariant to the origin by Proposition 1, and Proposition 2 says nothing else needs to be done.""",
"""**Step 2 — use the equivariant form.** Centre both sessions and fit on the centred training data, or standardise with training statistics, which is equivalent. A pipeline that does this is invariant to the origin by Proposition 1, and Proposition 2 says nothing else needs to be done. If the model is frozen or the features are unavailable, subtract w_k'(μB − μA) from score k instead: Section 4.6 shows that this is exact for affine models and needs K numbers rather than D."""
))

for a, b in REPL:
    if a not in s:
        print("MISS:", a[:70].replace("\n", " "))
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
print("written", n0, "->", len(s))
