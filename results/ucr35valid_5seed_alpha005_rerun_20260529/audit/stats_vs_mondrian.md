# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_rerun_20260529/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `mondrian_corruption_cp`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | -0.0137202 | 0 | -0.0514163 | 0.0244502 | 0.085716 | 0.477322 | 0.430476 |
| 0.05 | drift | coverage_delta | 525 | 0.00253098 | 0 | -0.00171197 | 0.00666847 | 0.0862206 | 0.235299 | 0.382857 |
| 0.05 | drift | abs_gap_delta | 525 | -0.00412679 | 0 | -0.00777969 | -0.000482395 | 0.000331213 | 0.0251032 | 0.295238 |
| 0.05 | gap | set_size_reduction | 525 | 0.417217 | 0.133333 | 0.333482 | 0.502685 | 3.01656e-27 | 1.29681e-20 | 0.666667 |
| 0.05 | gap | coverage_delta | 525 | -0.0166964 | -0.00719424 | -0.0209388 | -0.0123188 | 1.1744e-14 | 2.83957e-13 | 0.230476 |
| 0.05 | gap | abs_gap_delta | 525 | 0.00819883 | 0 | 0.00470421 | 0.0116527 | 0.00106956 | 4.07427e-06 | 0.428571 |
| 0.05 | noise | set_size_reduction | 525 | 0.126726 | 0.0499419 | 0.0906063 | 0.165157 | 6.20527e-14 | 1.08979e-10 | 0.624762 |
| 0.05 | noise | coverage_delta | 525 | -0.0174502 | 0 | -0.0238658 | -0.011445 | 1.319e-07 | 5.42157e-08 | 0.268571 |
| 0.05 | noise | abs_gap_delta | 525 | 0.00718798 | 0 | 0.00201699 | 0.0127441 | 0.241888 | 0.00941088 | 0.306667 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.176741 | 0.03207 | 0.142462 | 0.211332 | 1.18236e-25 | 3.47145e-23 | 0.573968 |
| 0.05 | __overall__ | coverage_delta | 1575 | -0.0105385 | 0 | -0.0134482 | -0.00767819 | 6.32771e-13 | 2.23791e-12 | 0.293968 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | 0.00375334 | 0 | 0.00141076 | 0.00622659 | 0.575657 | 0.00289098 | 0.343492 |
