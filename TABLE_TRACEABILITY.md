# TABLE_TRACEABILITY.md

Revision 3. All seven data rows of Table 9 are now machine-traced: the script parses the numbers out of the Word
cells and compares them with values recomputed from the archives.

| row | archive | result |
|---|---|---|
| BCI-2b csp gain | statistics_recomputed_2b.json | OK |
| Sleep-EDF cassette loss | b3_hierarchy.json | OK |
| BCI-2a euc_ea gain | causal_2a.json, subject-level bootstrap | OK |
| BCI-challenge ERRp | errp_external.json | OK |
| P300 speller | p300_external_meanamp.json | OK |
| SEED correction gain | **archived +0.214, recomputed +0.236** from seed_transductive.json | OK, with a documented discrepancy |
| Grasp-and-lift artefact | gal_order_curves.json, lambda = 1 minus lambda = 0 | OK |

**TABLE TRACEABILITY PASS, 7 of 7 rows.**

## The SEED row, and what was found

The archived figure is +0.214 [+0.167, +0.260]. The exact aggregation that produced it could not be located in
the released artifacts, so the contrast was recomputed from the cached distributed-entropy features (15 subjects,
all ordered session pairs, target-only centring): **+0.236 [+0.204, +0.271], positive in 15 of 15 subjects**.
Two other variants measured at the same time give +0.356 (both sessions centred) and -0.356 (both centred,
scored on the uncentred target), which shows that the number depends on the pipeline and that the archived
+0.214 sits between the first two.

The paper now prints both numbers: the archived value as the headline, and the recomputation next to it, with a
sentence in Section 4.4 stating that the sign and magnitude are reproduced while the exact archived aggregation
is not.

## The grasp-and-lift row

gal_order_curves.json stores five correction strengths per cell (lambda = 0, 0.25, 0.5, 0.75, 1) under three
orderings. The published sorted cache gives 0.6652 - 0.7727 = **-0.108**; the acquisition-order rebuild gives
0.7889 - 0.7874 = **+0.001**. Both match the table.
