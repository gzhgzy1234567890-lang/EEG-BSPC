# Round 003 review — trimming and the S34 archive

Version: BSPC_Candidate_V8.docx, 20 pages, 11,399 words; supplement 31 pages (S1-S34).

## What changed

| change | words removed from main text |
|---|---|
| estimator ranking narrative replaced by pointers to S34 | about 120 |
| old synthetic section (4.3) reduced to an introduction paragraph | about 90 |
| methods: primary-tests and preprocessing paragraphs condensed | about 120 |
| conclusion: P300, ERRp and matching paragraphs condensed | about 130 |
| **total** | **458 words, 3.9 per cent** |

New: S34 in the supplement (4 pages) holding the removed text so that every number cited in the main text stays
checkable. A first trims round (Section 4.6-4.8 insertion) had already removed about 660 words.

## Verification

- CONSISTENCY PASS; FREEZE CHECK PASS (12 files); audit archive 73 entries, submission 12;
- page count 20 (from 21), supplement 31 pages; abstract 249 words.

## Honest assessment of the length target

The goal asks for a 20-25 per cent cut of non-core text. **This round achieved 3.9 per cent**, and in total
about 12 per cent since the peak of 11,857 words. The reason is structural rather than stylistic: the remaining
bulk is evidence, not padding.

| section | words | can it move? |
|---|---:|---|
| 4.2.1 estimator leaderboard with Tables 4 and 5 | 730 | yes, but the tables and equations 7-9 must travel with it |
| 4.10 independent validation (P300, ERRp, Lee2019) | 614 | no: negative results must stay |
| 6. Conclusion | about 800 | partly; the restatements are already condensed |
| 3. Data and protocol | about 900 | no: reproducibility detail |

## Scores

| dimension | max | r1 | r2 | r3 | basis |
|---|---:|---:|---:|---:|---|
| theory boundary | 8 | 7.5 | 7.5 | 7.5 | unchanged |
| online decomposition | 22 | 21 | 21 | 21 | unchanged |
| factorial | 16 | 14.5 | 14.5 | 14.5 | unchanged |
| temporal | 10 | 8 | 8 | 8 | unchanged |
| protocol | 12 | 11 | 11 | 11 | unchanged |
| statistics | 12 | 11 | 11 | 11 | unchanged |
| reproducibility | 12 | 10 | 10 | 10 | unchanged |
| structure | 8 | 5 | 6.5 | 6.5 | S34 exists and pointers are honest, but the length target is not met |
| **total** | **100** | **88** | **90** | **90** | |

## Decision

**Major Revision, 90/100.** Two things cap the score and both are addressed next round:

1. move Section 4.2.1 with its two tables and equations to the supplement (about 700 words, the last large
   non-core block), and
2. close the two untraced Table 9 rows (SEED and grasp-and-lift) so that reproducibility can rise from 10 to 11,
   and add a memory sweep on the real sleep-EDF data so that the temporal dimension rests on a real corpus and
   not only on the controlled grid.
