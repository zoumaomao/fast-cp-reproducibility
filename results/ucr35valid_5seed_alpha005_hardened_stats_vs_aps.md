# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_hardened/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `aps_aug_cp`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | 0.935381 | 0.509494 | 0.800559 | 1.08369 | 1.68923e-67 | 1.89759e-34 | 0.860952 |
| 0.05 | drift | coverage_delta | 525 | -0.023755 | -0.00952381 | -0.0283458 | -0.0192855 | 6.1426e-32 | 2.16972e-22 | 0.161905 |
| 0.05 | drift | abs_gap_delta | 525 | -0.00191282 | -0.0031746 | -0.00507746 | 0.00157831 | 9.95557e-10 | 0.2612 | 0.253333 |
| 0.05 | gap | set_size_reduction | 525 | 0.887231 | 0.594937 | 0.769717 | 1.01401 | 4.76008e-69 | 2.54917e-39 | 0.866667 |
| 0.05 | gap | coverage_delta | 525 | -0.032456 | -0.0136986 | -0.037224 | -0.0275958 | 3.18388e-38 | 2.9765e-33 | 0.158095 |
| 0.05 | gap | abs_gap_delta | 525 | 0.0048468 | 0 | 0.00117414 | 0.00867038 | 0.267194 | 0.0117381 | 0.329524 |
| 0.05 | noise | set_size_reduction | 525 | 0.980589 | 0.555556 | 0.844976 | 1.12997 | 5.24426e-70 | 9.48499e-36 | 0.868571 |
| 0.05 | noise | coverage_delta | 525 | -0.0377625 | -0.015122 | -0.0447585 | -0.0313566 | 1.04079e-39 | 5.75222e-26 | 0.140952 |
| 0.05 | noise | abs_gap_delta | 525 | 0.00690414 | -0.000798722 | 0.00182759 | 0.0123426 | 0.0156347 | 0.00832851 | 0.314286 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.9344 | 0.535714 | 0.85934 | 1.01555 | 1.07396e-202 | 3.32923e-105 | 0.865397 |
| 0.05 | __overall__ | coverage_delta | 1575 | -0.0313245 | -0.012987 | -0.0345759 | -0.0282961 | 3.14141e-106 | 2.01589e-75 | 0.153651 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | 0.00327937 | -0.00217391 | 0.000898206 | 0.00572616 | 5.34526e-08 | 0.00732819 | 0.299048 |
