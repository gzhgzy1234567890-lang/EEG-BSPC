# EXTERNAL_VALIDATION_REPORT.md

## What counts as external

| dataset | role | status |
|---|---|---|
| sleep-EDF cassette | main negative result | developed here; not external |
| sleep-EDF telemetry | same corpus, different acquisition protocol | replication of the protocol, **not** an independent dataset |
| BCI-IV-2a | positive regime, 2x2 protocol audit | explored dataset; 2a results EXPLORATORY |
| BCI-IV-2b | positive regime, pre-specified csp endpoint | explored dataset; PROSPECTIVE-IN-EXPLORED-DATA |
| SEED (released DE features) | positive regime | BLOCKED for the causal raw pipeline |
| Lee2019-MI | cross-day cohort | development version +0.010, p = 0.098: no gain established |
| grasp-and-lift | cache-order artefact | used as an audit case, not as a performance claim |

## What can be claimed

1. The sleep negative transfer reproduces across recordings (45/45) and subjects (32/32) **within one corpus**,
   and under a second acquisition protocol of the same corpus (telemetry, 21/22 subjects).
2. The positive regime reproduces on two BCI datasets with different channel counts and protocols, in a causal,
   source-only pipeline; on 2b this was pre-specified.
3. No dataset in this paper is outside the corpora used in development. **There is no independent third-party
   dataset in this work.**

## What cannot be claimed

- That the effects generalise to sleep EEG from another laboratory.
- That Lee2019-MI shows a gain: the development-version interval includes zero (p = 0.098).
- That telemetry is an independent dataset.

## Consequence for the manuscript

The abstract and discussion must say "in the corpora studied" and must not generalise to sleep EEG at large.
