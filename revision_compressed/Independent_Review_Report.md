# Independent review of the compressed manuscript (round 1)

Version reviewed: `Revised_Manuscript.docx`, 17 pages, 7,232 body words (excluding references and tables),
5 figures, 7 tables; supplement 33 pages; new Highlights and cover letter.
Baseline for comparison: `BASELINE_v8_before_compression.docx`, 21 pages, 10,710 body words.

## 1. Is it shorter?

Yes: 10,710 -> 7,232 body words, a 32 per cent reduction, with no loss of figures (5/5) or tables (7/7). The
reduction is distributed, not concentrated in one section: Introduction -359, Theory -732, Data -493, Results -656,
Conclusion -802, with the Discussion roughly unchanged.

## 2. Did mechanism explanation improve, or only shrink?

Improved in three specific ways.

| change | before | after | why it helps |
|---|---|---|---|
| the decomposition is now introduced with its anchoring requirement | the anchoring was explained only after the numbers | the text states that the components are anchored on the source mean *because* an unmatched class makes the unanchored split origin-dependent | a reader can see why the numbers are what they are without reading S36 |
| the additivity caveat now names both causes | it attributed the gap only to the classifier non-linearity | it separates the interaction between terms from the non-linearity of balanced accuracy as a functional | removes a wrong attribution the earlier version contained |
| the optimum-strength claim is conditional | "the optimum falls below full strength exactly when a composition term is present" | "the measured optimum falls below full strength when a composition term is present, and the interval still touches 1.0 at one standard deviation" | matches the bootstrap interval rather than overstating it |

## 3. Did the theory-experiment link tighten?

The theory section now states the four propositions with one-line arguments and points to S2 for the proofs, so the
main text carries the logic rather than the algebra. The Monte Carlo result and the exact coefficient are in the
same paragraph as the claim they support, which was not the case before.

## 4. Did reproducibility improve?

New artefacts: `Result_to_Code_Manifest.csv` (11 results, each with script, data, seed, output and commit),
`Claim_Evidence_Registry.md` (13 claims with their class and location), `REPRODUCE.md` (run order, runtimes, and an
explicit list of what cannot be regenerated). The manuscript's Data availability points at `ef8c890`, which holds the
anchored decomposition and the dense grid.

## 5. Did statistics clarity improve?

The inference unit is stated for the factorial (12 subjects, seeds averaged inside subject), the recall denominators
are stated, and the Discussion now separates what the evidence supports from what remains a hypothesis. The
SEED discrepancy (+0.214 archived against +0.236 recomputed) is repeated in the Discussion rather than only where it
first appears.

## 6. New errors introduced?

Two were found and fixed during the compression: a renumbering gap (sections 4.8 and 4.9 were removed, leaving
4.10/4.11 stranded) and a stale cross-reference to the deleted limitations section. Both are corrected; the caption
order is now Table 1-3, Fig. 1-2, Table 4, Fig. 3-4, Table 5-6, Fig. 5, Table 7, and every abstract number appears in
the body.

## 7. Remaining weaknesses

- The Results still contain six subsections; the goal's target of five coherent questions is only partly met.
- The independent-validation section (614 words) was not compressed; it is the largest remaining block that could
  move detail to the supplement.
- Figure numbering is sequential but Figs 3 and 4 sit inside different results subsections than in the baseline,
  which a reviewer will not notice but an author should check against the figure files.

## Scores

| dimension | max | baseline | revised |
|---|---:|---:|---:|
| theory boundary | 8 | 7.5 | 7.5 |
| online decomposition | 22 | 20.5 | 20.5 |
| factorial | 16 | 15.5 | 15.5 |
| temporal | 10 | 8.5 | 8.5 |
| protocol | 12 | 11.5 | 11.5 |
| statistics | 12 | 11.0 | 11.0 |
| reproducibility | 12 | 10.5 | 11.0 |
| structure | 8 | 6.5 | 7.5 |
| **total** | **100** | **91.5** | **93.0** |

## Decision

**Ready for submission after one more pass** on the independent-validation section and a figure/table cross-check
against the exported PDF.
