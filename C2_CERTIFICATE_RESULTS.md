# C2 results: decision-stability certificate on real data

Script: `origin_equivariance/src/c2_certificate.py` (commit at the end of this round), seed fixed by the pipeline,
csp representation, causal filter, source-only EA, BCI-2b subjects 1-3, pair 01T -> 02T.

| subject | scored trials | flip rate | fraction certified stable | certificate vs observed flips | median margin | median critical strength |
|---|---|---|---|---|---|---|
| 1 | 83 | 0.361 | 0.639 | agreement 1.000 | 2.92 | 1.17 |
| 2 | 85 | 0.271 | 0.729 | agreement 1.000 | 2.01 | 1.32 |
| 3 | 73 | 0.027 | 0.973 | agreement 1.000 | 0.46 | 3.40 |

Reading.

1. The certificate (Proposition 4) is **exact on real data** for all three subjects: no sample certified stable
   flipped, and every sample that flipped failed the certificate. This is what an identity should do; the value is
   that it gives a per-sample, label-free statement about *stability*, not about accuracy.
2. Flip rates differ enormously between subjects (0.36 vs 0.03) while the correction is the same rule. A flip is
   not an error: a sample can flip from wrong to right.
3. The median critical strength is the multiplier on the displacement at which the first sample flips; values
   above 1 mean the applied displacement is below the tipping point for the median sample.

What this does not show: that flips predict accuracy. The pair (flip rate, accuracy change) is reported
separately in the 2x2 tables, and the two are not asserted to be monotonically related.
