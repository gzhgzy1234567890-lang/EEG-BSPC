# Response to the round-9 report — rebuild from a single source

The report's central point was that the manuscript carried two definitions of
`z_w`, stale numbers in the Discussion, and a missing table — i.e. that the
paper was not internally consistent. That was correct, and the cause was the
patch-by-patch revision process. We discarded the accumulated draft and rebuilt
the manuscript from one set of numbers.

## What was rebuilt

**One definition.** Equation (2) defines `z_w` with the scale taken from the
*centred* scores, `σ_k = SD[(P S)_{:,k}]`. That is the only definition in the
paper; the scalar `|w'μ_A|/σ_s` form appears only as the binary special case.
The invariance under a class-common linear score term is proved in the text and
verified numerically to 4.4 × 10⁻¹⁶; the weaker invariances are verified to
10⁻¹⁴ and 10⁻¹³. The uncentred convention that made the statistic
representation-dependent appears nowhere except in the sentence that explains
why it is not used.

**One set of numbers.** Every `z_w`-dependent quantity was recomputed with the
corrected definition and the text now carries only those:

| quantity | value in v16 |
|---|---|
| eleven-unit rank correlation | −0.83 |
| five-dataset rank correlation | −0.80 |
| six-dataset rank correlation, exact permutation p | −0.77, p = 0.103 |
| development-cell AUC (loss > 0.05, 228/845) | 0.841 |
| SEED-IV median `z_w`, median penalty | 24.4, −0.070 |
| SEED-IV within-dataset AUC | 0.515 |
| held-out operating point | sens 1.000, spec 0.000, prec 0.544 |

The former six-dataset result (−0.94, p = 0.017) and the former SEED-IV median
(1.00) appear nowhere. A grep of the built document for the stale strings
returns zero hits.

**Structure.** Ten tables numbered 1–10 and used in order (the missing Table 6
is the leave-one-dataset-out operating point, which the text references), four
figures cited in the order 3, 1, 2, 4 as they appear, no "earlier version" or
referee-facing language, one equation per numbered object, and `ρ`, `s`, `t*`,
`z_T` and `z_w` each defined once (Section 2.3 now states explicitly that ρ uses
μ_B and s uses μ_A and that they are different quantities).

**Positioning.** The paper is now an audit: title, abstract, Section 5 ("The
audit procedure") and Section 6.1 ("what the audit establishes, and what it does
not") are written around the mechanism, the boundaries and the negative results.
The source-only statistic is reported as an open question, not as a contribution.

## Verification

- Built document: 172 non-empty paragraphs, 10 tables, 4 embedded figures,
  245-word abstract, 19 references, no placeholders, no stray markup.
- Numeric audit of the built text: zero occurrences of the stale values, zero
  occurrences of the revision-history strings.

## What is still missing

The systematic audit of public preprocessing implementations — the one item the
referee has asked for since the second report and the one I have not delivered.
The manuscript states it as the natural next study and as a limitation rather
than pretending the single MOABB example is a survey. Until that is done, the
paper's practical motivation rests on a hypothesis.
