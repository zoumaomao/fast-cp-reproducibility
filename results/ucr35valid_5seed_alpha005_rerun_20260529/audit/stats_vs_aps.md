# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_rerun_20260529/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `aps_aug_cp`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | 0.934488 | 0.49 | 0.798252 | 1.08151 | 4.43962e-68 | 2.37222e-34 | 0.868571 |
| 0.05 | drift | coverage_delta | 525 | -0.0233368 | -0.00888889 | -0.0280238 | -0.0187611 | 5.04137e-31 | 1.85152e-21 | 0.179048 |
| 0.05 | drift | abs_gap_delta | 525 | -0.00152448 | -0.00316456 | -0.00461592 | 0.00192892 | 1.35663e-08 | 0.36397 | 0.274286 |
| 0.05 | gap | set_size_reduction | 525 | 0.888809 | 0.594937 | 0.771254 | 1.01435 | 1.08513e-69 | 2.13252e-39 | 0.870476 |
| 0.05 | gap | coverage_delta | 525 | -0.0318995 | -0.0133333 | -0.0369186 | -0.0271098 | 6.16292e-38 | 5.05776e-33 | 0.158095 |
| 0.05 | gap | abs_gap_delta | 525 | 0.00456328 | 0 | 0.000837501 | 0.00856507 | 0.23093 | 0.019127 | 0.327619 |
| 0.05 | noise | set_size_reduction | 525 | 0.979156 | 0.539568 | 0.839546 | 1.13011 | 3.86247e-70 | 1.49683e-35 | 0.870476 |
| 0.05 | noise | coverage_delta | 525 | -0.0375517 | -0.015122 | -0.044465 | -0.0309336 | 4.25005e-39 | 1.96595e-25 | 0.158095 |
| 0.05 | noise | abs_gap_delta | 525 | 0.00650197 | -0.00116144 | 0.00156033 | 0.0117729 | 0.0138819 | 0.0123564 | 0.337143 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.934151 | 0.533333 | 0.858746 | 1.01615 | 5.81992e-204 | 5.86598e-105 | 0.869841 |
| 0.05 | __overall__ | coverage_delta | 1575 | -0.0309293 | -0.0128205 | -0.0341451 | -0.0277731 | 1.8206e-104 | 1.49666e-73 | 0.165079 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | 0.00318025 | -0.00217391 | 0.000841801 | 0.00557951 | 1.1648e-07 | 0.0090879 | 0.313016 |
