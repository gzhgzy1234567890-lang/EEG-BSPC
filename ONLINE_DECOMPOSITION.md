# ONLINE_DECOMPOSITION.md

Task A: decompose the displacement that the **past-only estimator actually subtracts**, not the whole-target
displacement used by the earlier global decomposition.

## What is decomposed

For scored block k (15 epochs, first block unscored) the estimator subtracts

    d_k = mu_hat(H_k) - mu_A,      mu_hat(H_k) = (1/B) * sum over history blocks b of mean(F_b)

with H_k the blocks 1..k-1. Writing, for every class c present in the history,

    pi_hat_c = (1/B) sum_b (n_bc / n_b),    m_hat_c = [sum_b (n_bc/n_b) mean_bc] / (B pi_hat_c),

gives sum_c pi_hat_c m_hat_c = mu_hat(H_k) exactly, because the class fractions inside a block sum to one. Hence

    d_k = sum_{c in A} (pi_hat_c - pi_A,c) m_A,c        <- d_mix
        + sum_{c in A} pi_hat_c (m_hat_c - m_A,c)       <- d_within
        + sum_{c not in A} pi_hat_c m_hat_c             <- d_unmatched

and the three terms reproduce d_k to machine precision. **Measured maximum reconstruction error over all 4,983 cells
and all scored blocks: 2.6e-14.**

The unmatched term is not split further: a class absent from the source has no source mean, so calling part of it
"composition" or "within-class" would be arbitrary. It is reported separately, and the shared-class subset is
analysed on its own (below).

## Conditions compared (same classifier, same scored trials, same warm-up)

| condition | correction applied |
|---|---|
| none | zero |
| full | d_k, exactly the estimator's own vector |
| mix | d_mix only |
| within | d_within only |
| shared | d_mix + d_within (the unmatched mass dropped) |
| unmatched | d_unmatched only, diagnostic |

## Subject-level results (32 subjects; balanced accuracy, bootstrap intervals, seed 20261101)

| condition | BA | delta vs none | 95 per cent interval | subjects negative | Wilcoxon p |
|---|---|---|---|---|---|
| none | 0.4415 | - | - | - | - |
| **full** | 0.3391 | **-0.1023** | [-0.1141, -0.0898] | 32/32 | 7.9e-07 |
| mix only | 0.3158 | **-0.1257** | [-0.1366, -0.1154] | 32/32 | 7.9e-07 |
| within only | 0.4616 | **+0.0202** | [+0.0151, +0.0253] | 3/32 | 2.2e-06 |
| shared only | 0.3148 | -0.1266 | [-0.1385, -0.1151] | 32/32 | 7.9e-07 |
| unmatched only | 0.3871 | -0.0544 | [-0.0628, -0.0459] | 32/32 | 7.9e-07 |

Flip rates against no correction: full 0.393, mix 0.398, within 0.144, shared 0.439.

## What this establishes, and what it does not

1. **The harm is carried by the class-mix component, in the estimator that is actually used.** Removing only the
   composition part is *worse* than the full correction (-0.1257 against -0.1023); removing only the within-class
   part *improves* balanced accuracy (+0.0202, positive in 29 of 32 subjects).
2. **The components are not additive in balanced accuracy**, and the paper will not treat them as such: the sum of
   the two single-component effects is -0.1055 against the -0.1023 of the full correction, a difference of 0.0032
   that comes from the non-linearity of the decision rule, not from the decomposition.
3. **The unmatched-class term is not negligible** and is reported: up to the whole history mass in some blocks; its
   own correction costs -0.0544. A shared-class subset analysis is reported separately.
4. **This is an oracle diagnostic.** The history labels are used to compute the components; they never enter the
   predictor. The decomposition says which part of the displacement does the damage; it does not identify why the
   sleep-stage proportions change across the night.
5. **It supersedes the earlier global decomposition as the mechanism evidence**, because the earlier one decomposed
   the whole-target displacement (-0.098) while the main result uses the past-only estimator. The two are now kept
   apart and labelled.

## Shared-class subset (block-level sensitivity)

The unmatched term cannot be split, so the same comparison is repeated on blocks whose history contains only classes
that also occur in the source. **49.6 per cent of the 14,949 scored blocks have zero unmatched mass**, 24.1 per cent
have more than half their history from an unmatched class, and the maximum is 1.0.

Balanced accuracy here is pooled per block and averaged over blocks, which is a different estimand from the
cell-level balanced accuracy in the table above; the magnitudes are therefore not comparable across the two tables,
only the signs and the ordering are.

| subset | subjects | BA none | full delta [95 per cent interval] | mix delta | within delta | subjects negative |
|---|---|---|---|---|---|---|
| all blocks | 32 | 0.6386 | -0.1774 [-0.2060, -0.1499] | -0.1660 | +0.0190 | 32/32 |
| **shared-class blocks only** | 32 | 0.6221 | **-0.1639 [-0.1922, -0.1368]** | -0.1459 | +0.0201 | 32/32 |
| blocks with unmatched mass > 0 | 32 | 0.6624 | -0.1281 [-0.1630, -0.0924] | -0.1837 | +0.0283 | 28/32 |

The pattern survives: in blocks where no class is unmatched, removing the composition term is still the damaging
intervention and removing the within-class term is still beneficial.

## Relationship to the earlier global decomposition

| analysis | displacement | result | status |
|---|---|---|---|
| earlier (S31) | whole target segment | mix removal costs -0.091, conditional gains +0.034 | superseded as mechanism evidence |
| this one | the estimator's own past-only d_k, exact to 2.6e-14 | mix removal costs -0.1257, within gains +0.0202 | primary mechanism evidence |

The signs agree; the magnitudes do not, because they answer different questions. The paper reports this one as the
mechanism analysis and the earlier one only as a sensitivity check.