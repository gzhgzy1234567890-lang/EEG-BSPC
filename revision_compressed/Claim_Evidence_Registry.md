# Claim–evidence registry

Each row of the manuscript's evidence table, with the pointer to the executed computation behind it.

| claim | class | evidence | where |
|---|---|---|---|
| a correction acts only through the projection of its displacement onto the weights | identity | §2.1, Eq. 1-2 | theory |
| a composition-only correction must hurt in the symmetric model | identity | §2.3 | theory, Monte Carlo in S2 |
| optimal strength is clip[0,1](b/(b+c)) | identity | §2.3 | theory |
| sleep-EDF full correction costs 0.1023, 32/32 negative | confirmatory, within corpus | online_decomposition_anchored.json | §4.6 |
| the anchored composition term costs 0.0715 and the within term gains 0.0202 | oracle diagnostic | online_decomposition_anchored.json | §4.6 |
| the decomposition reconstructs the displacement to 2.7e-14 | identity, checked | online_decomposition_anchored.json | §4.6 |
| composition alone raises the cost from 0.0034 to 0.0097; drift alone gains 0.0172 to 0.0601 | controlled intervention | factorial_2x2_rich.json | §4.7 |
| the measured optimum is 0.6 [0.5, 0.8] with composition and 0.8-0.9 without | controlled intervention | factorial_lambda_dense.json | §4.7 |
| SEED crossing between 50 and 100 s | archived sweep | seed_memory_scale.json | §4.4 |
| sleep-EDF memory sweep -0.1138/-0.1057/-0.1023, no sign change | controlled, real data | sleep_memory_sweep.json | §4.4 |
| grasp negative transfer is a cache artefact (-0.108 sorted, +0.001 in order) | protocol audit | gal_order_curves.json | §4.5 |
| P300 -0.0005 [-0.0024, +0.0012]; ERRp -0.0044 [-0.0166, +0.0075] | external, exploratory | errp_external.json, p300_external_meanamp.json | §4.8 |
| no label-free rule predicts the sign | negative result | §4.3 | §4.3 |
