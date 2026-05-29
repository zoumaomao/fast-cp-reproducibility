# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_rerun_20260529/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `raps_aug_cp`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | 0.395351 | 0.371429 | 0.351719 | 0.439215 | 8.0272e-52 | 1.15471e-53 | 0.826667 |
| 0.05 | drift | coverage_delta | 525 | -0.0223724 | -0.00769231 | -0.0269715 | -0.0178501 | 9.59678e-27 | 2.9893e-20 | 0.2 |
| 0.05 | drift | abs_gap_delta | 525 | -0.000358364 | -0.00316456 | -0.00346838 | 0.00303761 | 2.9201e-06 | 0.831082 | 0.274286 |
| 0.05 | gap | set_size_reduction | 525 | 0.405321 | 0.389744 | 0.363792 | 0.445607 | 5.32111e-56 | 7.22408e-62 | 0.841905 |
| 0.05 | gap | coverage_delta | 525 | -0.0282431 | -0.00952381 | -0.0331589 | -0.0235412 | 2.62266e-33 | 8.55578e-29 | 0.188571 |
| 0.05 | gap | abs_gap_delta | 525 | 0.00259507 | 0 | -0.000697402 | 0.00624363 | 0.0380593 | 0.13816 | 0.325714 |
| 0.05 | noise | set_size_reduction | 525 | 0.4171 | 0.353846 | 0.371523 | 0.463111 | 8.06966e-53 | 4.75125e-56 | 0.838095 |
| 0.05 | noise | coverage_delta | 525 | -0.0339588 | -0.00949367 | -0.0410916 | -0.0270874 | 3.5198e-24 | 6.86182e-20 | 0.230476 |
| 0.05 | noise | abs_gap_delta | 525 | 0.00713778 | -0.00116144 | 0.00201949 | 0.0127739 | 0.00867838 | 0.00880292 | 0.333333 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.405924 | 0.376623 | 0.381134 | 0.431744 | 9.10785e-157 | 1.88705e-167 | 0.835556 |
| 0.05 | __overall__ | coverage_delta | 1575 | -0.0281914 | -0.00878594 | -0.0314323 | -0.0250195 | 5.29741e-80 | 2.24667e-61 | 0.206349 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | 0.00312483 | -0.00204082 | 0.000795901 | 0.005529 | 8.73123e-08 | 0.0101882 | 0.311111 |
