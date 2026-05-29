# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_hardened/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `fast_cp_mixed_no_spectral`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | -0.0012972 | 0 | -0.00282697 | 0.000215649 | 0.0309047 | 0.0990518 | 0.272381 |
| 0.05 | drift | coverage_delta | 525 | -0.000188794 | 0 | -0.000569583 | 0.000174361 | 0.55664 | 0.295986 | 0.102857 |
| 0.05 | drift | abs_gap_delta | 525 | -0.000105088 | 0 | -0.000446632 | 0.000240391 | 0.505003 | 0.55174 | 0.0952381 |
| 0.05 | gap | set_size_reduction | 525 | 0.00703566 | 0 | 0.00543022 | 0.00874386 | 1.0156e-17 | 2.94753e-15 | 0.441905 |
| 0.05 | gap | coverage_delta | 525 | -0.000946731 | 0 | -0.00131876 | -0.000617917 | 2.02692e-10 | 1.81499e-07 | 0.047619 |
| 0.05 | gap | abs_gap_delta | 525 | 0.000418512 | 0 | 8.5606e-05 | 0.000781199 | 0.00710988 | 0.0210224 | 0.125714 |
| 0.05 | noise | set_size_reduction | 525 | -0.00487923 | 0 | -0.00693609 | -0.00301817 | 2.62107e-10 | 7.50701e-07 | 0.184762 |
| 0.05 | noise | coverage_delta | 525 | 9.00899e-05 | 0 | -0.000262665 | 0.000441231 | 0.132011 | 0.626481 | 0.140952 |
| 0.05 | noise | abs_gap_delta | 525 | -6.36914e-05 | 0 | -0.000407563 | 0.000295963 | 0.462593 | 0.723722 | 0.108571 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.000286408 | 0 | -0.000757742 | 0.00129432 | 0.813794 | 0.583304 | 0.299683 |
| 0.05 | __overall__ | coverage_delta | 1575 | -0.000348478 | 0 | -0.000559446 | -0.000148404 | 0.00314383 | 0.000957329 | 0.0971429 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | 8.32443e-05 | 0 | -0.00011628 | 0.000289552 | 0.522474 | 0.421475 | 0.109841 |
