# P300_EXTERNAL_RESULT.md

Outcome of the pre-registered independent-dataset test. The protocol was committed as `eebba0a` **before** the
run.

## What was run

| run | features | status |
|---|---|---|
| pre-registered | log-variance per channel in four sub-windows (64 features) | completed |
| exploratory | mean amplitude per channel in four sub-windows (64 features) | added after the pre-registered decoder turned out to be at chance; labelled EXPLORATORY |

## Pre-registered run

16 subjects, LDA fitted on the first half of each subject's epochs, past-only correction on the second half, block
15.

| quantity | value |
|---|---|
| mean delta balanced accuracy | **-0.0005** |
| subjects negative | 14 of 16 |
| sign test | p = 0.0042 |
| Wilcoxon | p = 0.093 |
| balanced accuracy without correction | 0.499-0.528 (chance) |

## Exploratory run (mean amplitude features)

| quantity | value |
|---|---|
| mean delta balanced accuracy | **-0.0005** |
| subjects positive | 7 of 16 |
| sign test | p = 0.80 |
| Wilcoxon | p = 0.88 |
| balanced accuracy without correction | 0.50-0.78 (decoder works for part of the cohort) |

## The pre-registered prediction failed, and why

The prediction was that the correction would **hurt** because the class prior is far from balanced (about 0.14).
It did not: the effect is -0.0005, indistinguishable from zero once the decoder works.

The diagnosis is straightforward and is itself a test of the theory. The P300 data contain one session per
subject, so source and target are two halves of the **same** session with the **same** class composition
(pi_A = 0.14, pi_B = 0.14 in every subject). The displacement that a correction removes is
mu_B - mu_A, and with identical composition and no drift between halves this is approximately zero. A correction
that removes approximately zero can neither help nor hurt, which is exactly what was observed.

So the experiment is a **negative control**: it confirms the inert branch of the prediction (no displacement ->
no effect) on a dataset outside the development corpora, and it **refutes** the specific prediction I wrote down,
because that prediction incorrectly assumed the composition differed between source and target.

## Evidence grading

| claim | grade |
|---|---|
| correction is inert when source and target share composition and no drift | independent dataset, pre-registered design, but the direction of the written prediction was wrong |
| correction hurts when composition differs | **not tested here**; the literature (Bakas 2023 via SPDIM) and the sleep-EDF results carry it |

## What goes into the paper

One sentence in the Discussion: an independent ERP dataset, used as a negative control, shows the correction is
inert when there is no displacement to remove (-0.0005, 7 of 16 positive), which is what the decomposition
predicts. The failed prediction is recorded here rather than quietly converted into a success.
