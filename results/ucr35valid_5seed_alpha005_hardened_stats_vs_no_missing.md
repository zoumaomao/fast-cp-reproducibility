# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_hardened/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `fast_cp_mixed_no_missing`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | 0.0156697 | 0 | 0.0110511 | 0.020367 | 2.10802e-13 | 6.99039e-11 | 0.489524 |
| 0.05 | drift | coverage_delta | 525 | -0.00116756 | 0 | -0.00191752 | -0.000452073 | 7.98291e-07 | 0.00232272 | 0.0780952 |
| 0.05 | drift | abs_gap_delta | 525 | 0.000586238 | 0 | -0.000103781 | 0.00133977 | 0.126376 | 0.117513 | 0.173333 |
| 0.05 | gap | set_size_reduction | 525 | -0.0121186 | 0 | -0.0162538 | -0.00813746 | 1.53445e-08 | 1.00369e-08 | 0.260952 |
| 0.05 | gap | coverage_delta | 525 | 0.00121944 | 0 | 0.000604313 | 0.00190414 | 0.000679109 | 0.000296573 | 0.146667 |
| 0.05 | gap | abs_gap_delta | 525 | -0.00117345 | 0 | -0.00177723 | -0.000608789 | 6.14032e-05 | 8.24635e-05 | 0.102857 |
| 0.05 | noise | set_size_reduction | 525 | 0.0162339 | 0.00194363 | 0.0119383 | 0.020824 | 6.92903e-20 | 3.75242e-12 | 0.510476 |
| 0.05 | noise | coverage_delta | 525 | -0.00191379 | 0 | -0.00253994 | -0.00132319 | 3.78325e-14 | 3.53251e-09 | 0.0533333 |
| 0.05 | noise | abs_gap_delta | 525 | 0.00096466 | 0 | 0.000363034 | 0.00162909 | 0.00264649 | 0.00241355 | 0.190476 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.00659501 | 0 | 0.00407589 | 0.00911659 | 7.27374e-12 | 8.77105e-07 | 0.420317 |
| 0.05 | __overall__ | coverage_delta | 1575 | -0.000620637 | 0 | -0.00100401 | -0.000236181 | 2.51695e-08 | 0.00220813 | 0.0926984 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | 0.000125815 | 0 | -0.000218414 | 0.000500134 | 0.66021 | 0.512463 | 0.155556 |
