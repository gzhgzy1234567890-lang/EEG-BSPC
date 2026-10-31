# LIMITATIONS_AND_BLOCKERS.md

## Scientific limitations

1. One dataset for the negative result (sleep-EDF cassette, replicated in telemetry), no independent sleep corpus.
2. The positive BCI result is prospective on a dataset used in development; 2a is exploratory.
3. The composition decomposition on sleep-EDF is an oracle diagnostic: it uses the true target labels.
4. The mechanism is located (class-mix part) but not explained (why the proportions move across nights).
5. The theory is one-dimensional and Gaussian except for the certificate, which is an identity.
6. Flip rates are not accuracy estimates and are not used as such.
7. The filter contrast is an implementation difference, not a pure future-information contrast.

## Blockers (external)

| id | blocker | what it prevents | resolution |
|---|---|---|---|
| B1 | SEED raw/continuous EEG absent | the raw-to-feature causal rerun and a filter-only SEED comparison | obtain Preprocessed_EEG or the .cnt set |
| B2 | no third-party replication | independent reproduction claim | an external group runs the package |
| B4 | no dataset outside the development corpora | external validity beyond "corpora studied" | a new sleep or BCI corpus with a pre-registered protocol |

## Non-blockers, recorded for completeness

- The BCI-2a cue latency is taken from the dataset documentation rather than measured from annotations; the
  window statement in the manuscript is trial-relative so the claim does not depend on it.
- The Holm correction is vacuous with one live test and is described as such.
