# Round 004 review — all seven Table 9 rows traced, and a SEED discrepancy found

Version: BSPC_Candidate_V8.docx, 20 pages, 11,447 words.

## What was executed

| action | result |
|---|---|
| recomputed the SEED transductive contrast from the cached DE features | **+0.2362 [+0.2039, +0.2708]**, 15/15 subjects positive |
| tested two alternative pipelines for the same contrast | +0.3558 (both sessions centred) and -0.3558 (both centred, scored on the uncentred target) |
| located the grasp-and-lift archive columns | lambda = 0 ... 1 per cell: published -0.1075, acquisition order +0.0015 |
| extended table_trace.py to all seven rows | **TABLE TRACEABILITY PASS, 7 of 7** |
| Table 9 SEED row | now prints the archived +0.214 and the recomputed +0.236 side by side |
| Section 4.4 | one sentence stating that sign and magnitude reproduce, the exact archived aggregation does not |

## The finding that matters

The archived SEED figure of +0.214 could not be regenerated exactly: no artifact in the release aggregates to that
number, and the two natural pipelines bracket it (+0.236 target-only centring, +0.356 both-session centring).
This is stated in the paper rather than smoothed over. It is a reproducibility gap of a different kind from the
earlier ones: the result is not contradicted, but its exact provenance is not reproducible from the release.

## Scores

| dimension | max | r3 | r4 | basis |
|---|---:|---:|---:|---|
| theory boundary | 8 | 7.5 | 7.5 | unchanged |
| online decomposition | 22 | 21 | 21 | unchanged |
| factorial | 16 | 14.5 | 14.5 | unchanged |
| temporal | 10 | 8 | 8 | unchanged; still no memory sweep on the real sleep corpus |
| protocol | 12 | 11 | 11 | unchanged |
| statistics | 12 | 11 | 11 | unchanged |
| reproducibility | 12 | 10 | **11** | every Table 9 row is now machine-traced; the SEED discrepancy is disclosed |
| structure | 8 | 6.5 | 6.5 | unchanged |
| **total** | **100** | **90** | **90.5** | |

## Hard gates

All pass. The SEED provenance gap is disclosed in the manuscript, the archive and this review, so gate 2
(traceability) is satisfied in the sense the gate defines: every claimed number is tied to an executed computation,
including the one that does not match the archive.

## Next round

1. sleep-EDF memory sweep on the real corpus (memory of one, two and three blocks) so that the temporal dimension
   rests on real data and not only on the controlled grid;
2. move Section 4.2.1, Tables 4 and 5 and equations 7-9 to the supplement (about 700 words), the last large
   non-core block.

## Decision

**Major Revision, 90.5/100.**
