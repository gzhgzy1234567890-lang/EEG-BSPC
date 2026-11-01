# Round 002 review — manuscript integration

Version: BSPC_Candidate_V8.docx, 21 pages, 11,857 words, 9 tables, retitled
*Mean correction in EEG decoding: decision geometry, temporal memory, and failure modes*.
Git: manuscript rewritten this round; evidence documents unchanged since round 1.

## What changed this round

| change | detail |
|---|---|
| three mechanism sections added | 4.6 online decomposition, 4.7 controlled factorial, 4.8 memory and time scales |
| later sections renumbered | 4.6-4.8 became 4.9-4.11 |
| old global decomposition demoted | now a single sensitivity paragraph pointing to supplement S31 |
| memory-scale paragraph replaced | pointer to 4.8 instead of a duplicate sweep |
| conclusion's causal paragraph rewritten | cites 4.6-4.8, keeps the no-label-free-rule statement |
| title | changed to the recommended title, now supported by the new sections |
| abstract | rewritten around the decomposition, the factorial and the memory scale; 249 words, inside the 250 limit |

## Verification

- CONSISTENCY PASS: all ten abstract numbers appear in the body; claim locations resolve; freeze rows match;
- FREEZE CHECK PASS, 12 files; both archives rebuilt (audit 73 entries, submission 12);
- page count 21, tables 9, abstract 249 words.

## Scores

| dimension | max | round 1 | round 2 | basis for the change |
|---|---:|---:|---:|---|
| scientific question and theory boundary | 8 | 7.5 | 7.5 | unchanged |
| online mechanism decomposition | 22 | 21 | 21 | unchanged evidence, now reported in the paper |
| controlled mechanism intervention | 16 | 14.5 | 14.5 | unchanged |
| temporal-scale explanation | 10 | 8 | 8 | unchanged |
| data protocol and reliability | 12 | 11 | 11 | unchanged |
| statistical rigour | 12 | 11 | 11 | unchanged |
| reproducibility | 12 | 10 | 10 | unchanged; archives rebuilt and verified |
| structure and expression | 8 | 5 | **6.5** | the paper now contains the mechanism evidence and a title that matches it; length still not reduced |
| **total** | **100** | **88** | **90** | |

## Hard gates

All previously passing gates still pass. Two remain open on evidence rather than on text:

| gate | status |
|---|---|
| core results traceable | 5 of 7 Table 9 rows machine-traced; SEED and grasp rows are not |
| no third-party replication | structural, cannot be closed in this environment |

## What is still missing for 96

1. **Length.** 11,857 words against a 5,000-word target reported by a third-party index for BSPC full papers; the
   goal asks for a 20-25 per cent cut and this round achieved none of it (new sections added about as much as the
   trims removed).
2. **Reproducibility 10/12.** Two Table 9 rows are untraced and no external replication exists.
3. **Structure 6.5/8.** The paper now has the right sections but not the right density: the estimator leaderboard
   and the older synthetic section still occupy main-text space that the new mechanism sections need.

## Decision

**Major Revision, 90/100.** Next round: move the estimator leaderboard and the older synthetic analysis to the
supplement, compress the conclusion's restatements, and re-measure against a 9,000-word target.
