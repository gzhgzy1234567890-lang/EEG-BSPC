# TABLE_TRACEABILITY.md

Revision 2. Revision 1 was criticised, correctly, by the referee: the script compared archived values against
**hard-coded constants** and printed the cell text next to them, so it could not detect a mismatch between the Word
table and the archive. The script has been rewritten.

## What the check now does

`table_trace.py` reads Table 9 from `BSPC_Candidate_V8.docx`, extracts the numbers from each cell with a regular
expression, derives the same quantities from the archived outputs, and compares the two lists.

| row | archive used | result |
|---|---|---|
| BCI-2b csp gain | `statistics_recomputed_2b.json` | **OK**, +0.0341 [+0.0104, +0.0585] both sides |
| Sleep-EDF cassette loss | `b3_hierarchy.json` | **OK**, -0.102 [-0.115, -0.090] both sides |
| BCI-2a euc_ea gain | `causal_2a.json`, subject-level mean and bootstrap | **OK**, +0.071 [+0.041, +0.104] both sides |
| BCI-challenge ERRp | `errp_external.json`, subject-level bootstrap | **OK** on the point estimate; interval bounds differ in the fourth decimal |
| P300 speller | `p300_external_meanamp.json` | **OK**, -0.0005 [-0.0024, +0.0012] both sides |
| SEED correction gain | **not traced**: no per-subject SEED archive in this checkout | excluded from the claim |
| Grasp-and-lift artefact | **not traced** in this script | excluded from the claim |

Result: **TABLE TRACEABILITY PASS for 5 of the 7 data rows**, archived in `results/table9_traceability.json`.

## The mismatch the new script found

The sleep interval was printed as **[-0.114, -0.090]**. The archive value is -0.114547, which rounds to -0.115 at
three decimals. That is a genuine one-unit rounding error in the manuscript, present in Table 9 and in the Section
4.3 text, and it is now corrected to [-0.115, -0.090]. The causal-filtering interval in the same paragraph,
[-0.114, -0.089], was re-derived from its own archive (-0.11394) and is correct as printed.

The ERRp interval differs in the fourth decimal (manuscript -0.0166, checker -0.0167) because the checker recomputes
the bootstrap with an independent random stream. A tolerance of 1.5e-3 is applied to interval bounds for that
reason, and the tolerance is stated here rather than hidden.

## What is still not machine-checked

SEED +0.214 [+0.167, +0.260] and the grasp-and-lift contrast (+0.001 acquisition order against -0.108 sorted) come
from archives produced before the current script set. They were not re-derived, and the table-traceability claim
does not cover them. Their provenance is recorded in FILE_PROVENANCE.csv.
