# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_rerun_20260529/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `fast_cp_mixed_random_fingerprint`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | 0.0624141 | 0.0133333 | 0.0520116 | 0.0732918 | 4.25198e-28 | 7.61792e-27 | 0.571429 |
| 0.05 | drift | coverage_delta | 525 | -0.00336028 | 0 | -0.00591562 | -0.00112448 | 0.00138697 | 0.00695273 | 0.20381 |
| 0.05 | drift | abs_gap_delta | 525 | -7.05252e-05 | 0 | -0.00162743 | 0.00167358 | 0.00504278 | 0.934604 | 0.20381 |
| 0.05 | gap | set_size_reduction | 525 | 0.0412864 | 0.00291545 | 0.0291289 | 0.0533863 | 2.56922e-07 | 5.29182e-11 | 0.506667 |
| 0.05 | gap | coverage_delta | 525 | -0.000586591 | 0 | -0.00313564 | 0.00168324 | 0.129236 | 0.632228 | 0.285714 |
| 0.05 | gap | abs_gap_delta | 525 | -0.00270804 | 0 | -0.00440224 | -0.000906007 | 1.14284e-08 | 0.00180886 | 0.16381 |
| 0.05 | noise | set_size_reduction | 525 | 0.0242871 | 0 | 0.0132823 | 0.0352822 | 0.000231841 | 1.59712e-05 | 0.462857 |
| 0.05 | noise | coverage_delta | 525 | 0.006406 | 0 | 0.00390986 | 0.00915637 | 5.95844e-06 | 2.50821e-06 | 0.304762 |
| 0.05 | noise | abs_gap_delta | 525 | -0.00723346 | 0 | -0.00987653 | -0.00496972 | 1.8581e-12 | 1.07725e-08 | 0.175238 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.0426625 | 0.00362319 | 0.0361245 | 0.0488875 | 2.63881e-30 | 1.40746e-35 | 0.513651 |
| 0.05 | __overall__ | coverage_delta | 1575 | 0.00081971 | 0 | -0.000629543 | 0.00222081 | 0.0663486 | 0.268704 | 0.264762 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | -0.00333734 | 0 | -0.00446314 | -0.00218799 | 7.65505e-20 | 1.38274e-08 | 0.180952 |
