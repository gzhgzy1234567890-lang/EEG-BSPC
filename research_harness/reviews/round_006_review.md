# Round 006 review — the strength sweep, and a test of the closed-form optimum

Version: BSPC_Candidate_V8.docx, 20 pages, 11,546 words.

## Executed this round

| action | result |
|---|---|
| correction-strength sweep in the factorial (lambda = 0, 0.25, 0.5, 0.75, 1) | 2,880 runs over 12 subjects |
| predicted optimum lambda* = b/(b+c) compared with the measured optimum | 0.58 and 0.72 predicted against 0.75 measured where composition is present; 1.00 and 1.00 predicted against 0.75 and 1.00 where it is absent |
| per-stage recall added to Section 4.6 | wake 0.535 to 0.545, N1 0.397 to 0.253, N2 0.752 to 0.565, N3 0.679 to 0.623, REM 0.728 to 0.526 |
| flip rates added | 39.3 per cent full, 39.5 mix, 14.3 within |

## What the sweep shows

With no drift and no composition change every increase in strength costs accuracy, from 0 to -0.0053 at full
strength: correcting noise hurts in proportion to how much of it is corrected. With a drift the curve turns over,
peaking at 0.75 for half a standard deviation and at full strength for one. With a composition change present the
predicted optimum falls below one (0.58 and 0.72) and the measured optimum is 0.75 in both cases, so the direction
is right and the grid cannot resolve the difference.

This matters beyond the paper's own theory: the strength is the one knob a practitioner controls, and the result
says a partial strength is better than full when a composition displacement is present - which is a testable
statement rather than advice.

## Scores

| dimension | max | r5 | r6 | basis |
|---|---:|---:|---:|---|
| theory boundary | 8 | 7.5 | 7.5 | unchanged |
| online decomposition | 22 | 21 | **21.5** | per-stage recall and flip rates now reported |
| factorial | 16 | 14.5 | **15.5** | strength sweep and the predicted-versus-measured optimum |
| temporal | 10 | 9 | 9 | unchanged |
| protocol | 12 | 11 | 11 | unchanged |
| statistics | 12 | 11 | 11 | unchanged |
| reproducibility | 12 | 11 | 11 | unchanged |
| structure | 8 | 7 | 7 | unchanged |
| **total** | **100** | **91.5** | **93.5** | |

## Hard gates

All pass. The strength sweep is a new result and is reported with its grid limitation, not as a precise estimate of
the optimum.

## Remaining gap to 96

| dimension | now | ceiling | what would close it |
|---|---:|---:|---|
| structure | 7 | 8 | length: 11,546 words against a 5,000-word target |
| statistics | 11 | 12 | a confirmatory replication, which does not exist in this environment |
| protocol | 11 | 12 | same |
| reproducibility | 11 | 12 | third-party rerun, impossible here |
| factorial | 15.5 | 16 | finer strength grid |

## Decision

**Major Revision, 93.5/100.**
