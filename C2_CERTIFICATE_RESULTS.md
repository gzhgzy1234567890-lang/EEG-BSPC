# C2 results: decision-stability certificate on real data

Script: `origin_equivariance/src/c2_certificate.py`, csp representation, causal filter, source-only alignment,
BCI-2b pair 01T -> 02T, **all nine subjects** (extended from three in response to the referee's P2 item).

| subject | scored trials | flip rate | fraction certified stable | certificate vs observed flips | median margin | median critical strength |
|---|---|---|---|---|---|---|
| 1 | 83 | 0.361 | 0.639 | 1.000 | 2.92 | 1.17 |
| 2 | 85 | 0.271 | 0.729 | 1.000 | 2.01 | 1.32 |
| 3 | 73 | 0.027 | 0.973 | 1.000 | 0.46 | 3.40 |
| 4 | 114 | 0.167 | 0.833 | 1.000 | - | - |
| 5 | 121 | 0.273 | 0.727 | 1.000 | - | - |
| 6 | 70 | 0.229 | 0.771 | 1.000 | - | - |
| 7 | 96 | 0.302 | 0.698 | 1.000 | - | - |
| 8 | 75 | 0.093 | 0.907 | 1.000 | - | - |
| 9 | 76 | 0.224 | 0.776 | 1.000 | - | - |

**Totals: 793 scored trials over nine subjects, agreement 1.000 in every subject.** Flip rates range from 0.027 to
0.361; the fraction of trials the certificate declares stable ranges from 0.639 to 0.973.

Reading.

1. The certificate (Proposition 4) is exact on all nine subjects: no certified-stable sample flipped, and every
   sample that flipped failed the certificate. This is what an identity should do; the value is that it gives a
   per-sample, label-free statement about *stability*, not about accuracy.
2. Flip rates differ by more than an order of magnitude across subjects (0.027 to 0.361) under the same correction
   rule. A flip is not an error: a sample can flip from wrong to right.
3. The certificate is computed without labels; the flip column is computed with them, purely for checking.

What this does not show: that flips predict accuracy. The pair (flip rate, accuracy change) is reported separately
in the 2x2 tables, and the two are not asserted to be monotonically related.

## Change from the previous version

The earlier version reported three subjects. The referee asked for a wider demonstration (P2). All nine subjects
are now included; the agreement is unchanged at 1.000, which is expected for an identity but is now shown over
793 trials rather than 241.
