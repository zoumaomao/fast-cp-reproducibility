# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_hardened/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `mondrian_corruption_cp`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | -0.0120883 | 0 | -0.0499796 | 0.0258272 | 0.106691 | 0.53159 | 0.432381 |
| 0.05 | drift | coverage_delta | 525 | 0.00247769 | 0 | -0.00179372 | 0.00677167 | 0.0899826 | 0.246738 | 0.392381 |
| 0.05 | drift | abs_gap_delta | 525 | -0.00420272 | 0 | -0.00773724 | -0.000558305 | 0.000224051 | 0.0229619 | 0.299048 |
| 0.05 | gap | set_size_reduction | 525 | 0.417895 | 0.133333 | 0.334561 | 0.504071 | 4.05725e-27 | 1.56297e-20 | 0.666667 |
| 0.05 | gap | coverage_delta | 525 | -0.0167432 | -0.00719424 | -0.02113 | -0.0124018 | 1.37811e-14 | 2.71149e-13 | 0.228571 |
| 0.05 | gap | abs_gap_delta | 525 | 0.00821698 | 0 | 0.00479459 | 0.0116495 | 0.00113758 | 4.15601e-06 | 0.424762 |
| 0.05 | noise | set_size_reduction | 525 | 0.128255 | 0.0461538 | 0.091443 | 0.166877 | 3.22155e-14 | 7.64927e-11 | 0.622857 |
| 0.05 | noise | coverage_delta | 525 | -0.0175932 | 0 | -0.0238544 | -0.0115727 | 8.48529e-08 | 4.41518e-08 | 0.262857 |
| 0.05 | noise | abs_gap_delta | 525 | 0.00718482 | 0 | 0.00206105 | 0.012715 | 0.247381 | 0.00957598 | 0.312381 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.17802 | 0.03207 | 0.142954 | 0.212735 | 4.68813e-26 | 2.3201e-23 | 0.573968 |
| 0.05 | __overall__ | coverage_delta | 1575 | -0.0106196 | 0 | -0.0135847 | -0.00773031 | 4.72607e-13 | 1.67792e-12 | 0.294603 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | 0.00373303 | 0 | 0.00137483 | 0.00616687 | 0.521753 | 0.00311954 | 0.345397 |
