# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_hardened/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `raps_aug_cp`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | 0.400211 | 0.371429 | 0.355171 | 0.443612 | 9.8587e-52 | 5.28947e-54 | 0.820952 |
| 0.05 | drift | coverage_delta | 525 | -0.0230664 | -0.00952381 | -0.0276156 | -0.0186826 | 3.72066e-28 | 6.0563e-22 | 0.188571 |
| 0.05 | drift | abs_gap_delta | 525 | -0.000272648 | -0.00316456 | -0.00340981 | 0.00313125 | 1.65967e-06 | 0.871793 | 0.262857 |
| 0.05 | gap | set_size_reduction | 525 | 0.408003 | 0.390476 | 0.366029 | 0.448509 | 5.22105e-56 | 6.51972e-62 | 0.83619 |
| 0.05 | gap | coverage_delta | 525 | -0.0288306 | -0.0102564 | -0.0334389 | -0.0241698 | 3.54762e-33 | 2.80813e-29 | 0.188571 |
| 0.05 | gap | abs_gap_delta | 525 | 0.003014 | 0 | -0.000223763 | 0.00654654 | 0.0540033 | 0.0787433 | 0.333333 |
| 0.05 | noise | set_size_reduction | 525 | 0.422172 | 0.353333 | 0.376873 | 0.468114 | 6.69469e-54 | 1.24983e-57 | 0.83619 |
| 0.05 | noise | coverage_delta | 525 | -0.0346483 | -0.00949367 | -0.0418674 | -0.0281198 | 1.41624e-25 | 3.43303e-21 | 0.211429 |
| 0.05 | noise | abs_gap_delta | 525 | 0.00781264 | -1.11022e-16 | 0.00264311 | 0.013453 | 0.0114941 | 0.00394762 | 0.32 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.410129 | 0.38 | 0.384841 | 0.435628 | 7.65482e-158 | 1.656e-169 | 0.831111 |
| 0.05 | __overall__ | coverage_delta | 1575 | -0.0288484 | -0.01 | -0.0320438 | -0.0258057 | 8.02484e-83 | 4.12187e-65 | 0.19619 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | 0.003518 | -0.00195122 | 0.00120459 | 0.0058994 | 1.12876e-07 | 0.00360599 | 0.305397 |
