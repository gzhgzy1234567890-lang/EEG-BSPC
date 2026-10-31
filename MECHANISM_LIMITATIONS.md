# MECHANISM_LIMITATIONS.md

What the mechanism analysis in this paper can and cannot support, claim by claim.

| claim | what supports it | what would falsify it | confounds not controlled | status |
|---|---|---|---|---|
| The sleep-EDF loss is carried by the class-mix part of the displacement | block-wise oracle decomposition (-0.092 mix-only vs +0.020 conditional), non-additivity -0.041 | a decomposition in which removing the mix part leaves the loss intact | class identity, night position, time-of-night drift, electrode impedance | ORACLE-DIAGNOSTIC, exploratory |
| The loss is not a threshold artefact | uniform-prior control moves it by 0.003 against 0.102 | a prior/threshold setting that removes the loss | none for this question | supported |
| The loss is not a matched-composition artefact | six matching specifications all give about -0.104 | a matching scheme that reverses the sign | matching on unmeasured covariates (impedance, sleep depth) | supported within the measured strata |
| Class concentration drives the loss | **withdrawn** | - | - | the five-definition regeneration found no effect (-0.023 to +0.005) |
| The correction helps on SEED because the displacement is real drift | memory-scale crossover between 50 and 100 s | a drift-free generator reproducing the gain | SEED preprocessing already smooths the features; the "drift" is not measured directly | EXPLORATORY |
| Label-free gates cannot predict the sign | all tested gates fail across tasks | a gate that predicts the sign out of sample | the space of gates is not exhausted | result of the rules tested, not an impossibility theorem |

## The honest summary

The mechanism analysis **locates** the sleep loss (class-mix displacement) and **excludes** three alternative
explanations (threshold, prior, matched composition). It does **not** explain why the class proportions move across
nights, and it does not identify a deployable signal that would predict the sign. Both gaps are stated in the
manuscript's Discussion rather than papered over.
