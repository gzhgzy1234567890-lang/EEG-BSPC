# ONLINE_DECOMPOSITION.md

Revision 3, after the referee pointed out that the split was not origin-invariant.

## What was wrong in revision 2

The composition term was defined as sum_{c in A}(pi_hat_c - pi_A,c) m_A,c and the residual as
sum_{c notin A} pi_hat_c m_hat_c. When the history contains a class absent from the source with total mass u, a
global translation of every feature by a moves the first term by -u a and the second by +u a. The sum is invariant,
the parts are not, so the reported composition effect depended on an arbitrary origin. The referee is right and
revision 2 is withdrawn.

## The anchored decomposition now used

Every term is anchored on the source mean mu_A:

    d_mix  = sum_{c in A} (pi_hat_c - pi_A,c)(m_A,c - mu_A)
    d_with = sum_{c in A} pi_hat_c (m_hat_c - m_A,c)
    d_unm  = sum_{c notin A} pi_hat_c (m_hat_c - mu_A)

Each is invariant under a common translation, and the three sum to d_k exactly. Maximum reconstruction error over
4,983 cells and 14,949 scored blocks: **2.7e-14**.

**Test.** With an unmatched class present, translating every feature by four units moves the anchored terms by less
than 1e-9 and the unanchored ones by more than 1e-3 (part of the released test suite).

## Subject-level results (32 subjects)

| condition | delta | 95 per cent interval | negative | dz |
|---|---|---|---|---|
| full correction | -0.1023 | [-0.1145, -0.0900] | 32/32 | -2.84 |
| **composition only (anchored)** | **-0.0715** | **[-0.0792, -0.0635]** | 32/32 | -3.09 |
| composition only (unanchored, withdrawn) | -0.1257 | [-0.1366, -0.1154] | 32/32 | -4.10 |
| within-class only | +0.0202 | [+0.0151, +0.0252] | 3/32 | +1.36 |
| composition + within | -0.0759 | [-0.0859, -0.0655] | 32/32 | -2.58 |
| unmatched only | -0.0148 | [-0.0183, -0.0111] | 29/32 | -1.41 |

## What changes and what does not

- The ordering is unchanged: removing the composition term is the damaging intervention and removing the
  within-class term is beneficial.
- The magnitude of the composition effect nearly halves: -0.0715 instead of -0.1257. The paper now reports the
  anchored value and keeps the unanchored one only as a stated diagnostic.
- The unmatched residual is small once anchored (-0.0148 against -0.0544), which is itself informative: most of what
  looked like an unmatched-class effect was the arbitrary origin.

## Still true from revision 2

- the decomposition is an oracle diagnostic: history labels never enter the predictor;
- the components are not additive in balanced accuracy;
- half of the scored blocks have no unmatched class in their history at all.
