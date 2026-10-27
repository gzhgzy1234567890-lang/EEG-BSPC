# Round 3 status — BSPC v8 (referee verdict: minor revision)

## Verdict

`BSPC_review_round3.md`: **Minor revision.** The structural objections of the
first report are answered; five small items remain (two editorial, three
requiring no new experiments).

## Changes made in round 3

| item | what changed |
|---|---|
| Referee M2 (prevalence) | audited the MOABB cross-session example: every transform is fitted inside the training fold, so it is equivariant by construction; the manuscript now says the exposure lives in custom pipelines, not framework code, and reframes the claim accordingly (Section 1, Section 6.4, ref [18]) |
| Referee M9 (streaming) | replaced the random-order result with a recorded-order comparison. Recorded order is exact on BCI-2b but fails on the block-structured SEED (0.672 vs 0.709) and grasp-and-lift (0.678 vs 0.794); the text now says a running reference does not remove the need for a calibration block |
| New contribution | corollary: the correction can be applied in decision space (K numbers, no features, no refit), verified to 0.0e+00 against the feature-space form for three linear families on three datasets; new Section 4.6 |
| Referee item 4 | highlights updated to include the decision-space form |
| Referee item 3 | limitations now state that the corollary is proved for affine models only |

## Remaining minor items (listed for the revision)

1. Calibration: report per-subject ECE with a bootstrap interval, or restrict
   the claim to BCI-2b. (Numbers exist; no new experiment.)
2. One more audited published example (Braindecode or pyRiemann).
3. Fig. 2b legend overlaps the data.

## Files

- `BSPC_draft_v8.md` — manuscript (250-word abstract, 18 refs, 8 tables, 3 figures)
- `BSPC_review_round3.md` — second referee report (minor revision)
- `BSPC_review_v8.md` — first referee report (major revision, superseded)
- `results/` — every number, with the script that produced it
- `figs/` — Figures 1-3
- scripts: `pv8_*.py` (common, exp1-exp9, screen, final, figs, checks, apply_rev*)
