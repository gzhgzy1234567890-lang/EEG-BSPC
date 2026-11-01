# Round 005 review — tables moved out, and the real memory sweep that limits the story

Version: BSPC_Candidate_V8.docx, 20 pages, 11,303 words, 7 tables; supplement 32 pages (S1-S35).

## Executed this round

| action | result |
|---|---|
| memory sweep on the real sleep-EDF corpus (1, 2, 3 blocks of history) | -0.1138, -0.1057, -0.1023, all 32/32 negative |
| Tables 4 and 5 moved to supplement S35 and the rest renumbered 1-7 | 7 tables in the main text, references 1-7 consistent |
| Section 4.8 extended with the real sweep | states that memory reduces the loss by 0.012 and never changes its sign |
| archives rebuilt and verified | FREEZE PASS, CONSISTENCY PASS |

## The scientific result of the round, and it cuts against the earlier reading

The controlled grid says the effect should fall steeply as memory grows (-0.2749 at one block to -0.0276 at sixteen).
The real corpus says: -0.1138, -0.1057, -0.1023 over the three available block lengths. **The sign never flips.**
A 60-epoch series holds only three blocks, so sleep-EDF sits at the bottom of the curve and cannot be pushed up it.
The paper now says this explicitly, and Section 4.8 no longer implies that a longer memory would rescue the corpus.

## Scores

| dimension | max | r4 | r5 | basis |
|---|---:|---:|---:|---|
| theory boundary | 8 | 7.5 | 7.5 | unchanged |
| online decomposition | 22 | 21 | 21 | unchanged |
| factorial | 16 | 14.5 | 14.5 | unchanged |
| temporal | 10 | 8 | **9** | now measured on the real corpus, and the limit it imposes is stated |
| protocol | 12 | 11 | 11 | unchanged |
| statistics | 12 | 11 | 11 | unchanged |
| reproducibility | 12 | 11 | 11 | unchanged |
| structure | 8 | 6.5 | **7** | two large tables moved out; 20 pages; numbering verified |
| **total** | **100** | **90.5** | **91.5** | |

## Hard gates

All pass. One new risk is recorded: the real sweep contradicts a strong reading of the memory account, and the
manuscript now states the contradiction instead of leaving the controlled grid to speak alone.

## Length, again

11,303 words, down 554 from the peak of 11,857 (4.7 per cent). The 20-25 per cent target is not reachable without
removing evidence sections, and the paper keeps them. This is recorded as a standing gap rather than quietly
dropped.

## Decision

**Major Revision, 91.5/100.**
