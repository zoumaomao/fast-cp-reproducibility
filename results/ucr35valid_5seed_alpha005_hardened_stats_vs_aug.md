# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_hardened/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `aug_split_cp`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | 0.110466 | 0.0454545 | 0.0976255 | 0.123626 | 1.27714e-62 | 7.48819e-49 | 0.775238 |
| 0.05 | drift | coverage_delta | 525 | -0.0086718 | 0 | -0.011456 | -0.00625747 | 4.34764e-25 | 5.23371e-11 | 0.0914286 |
| 0.05 | drift | abs_gap_delta | 525 | 5.42801e-05 | 0 | -0.00167638 | 0.00191862 | 0.000200877 | 0.952124 | 0.186667 |
| 0.05 | gap | set_size_reduction | 525 | 0.0909927 | 0.025974 | 0.076642 | 0.105243 | 1.29978e-38 | 1.81062e-31 | 0.708571 |
| 0.05 | gap | coverage_delta | 525 | -0.00558323 | 0 | -0.0080348 | -0.00338199 | 9.10019e-09 | 2.5426e-06 | 0.165714 |
| 0.05 | gap | abs_gap_delta | 525 | -0.000647575 | 0 | -0.0021963 | 0.001015 | 1.7864e-05 | 0.425522 | 0.169524 |
| 0.05 | noise | set_size_reduction | 525 | 0.0793709 | 0.0214634 | 0.0666429 | 0.0928016 | 1.47766e-33 | 3.82215e-28 | 0.653333 |
| 0.05 | noise | coverage_delta | 525 | -0.00192329 | 0 | -0.0039144 | -1.6382e-05 | 0.000595612 | 0.0502556 | 0.179048 |
| 0.05 | noise | abs_gap_delta | 525 | -0.00310501 | 0 | -0.00470988 | -0.00145856 | 2.46277e-08 | 0.000229102 | 0.171429 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.0936097 | 0.0292683 | 0.0859535 | 0.101285 | 7.50742e-130 | 4.45611e-103 | 0.712381 |
| 0.05 | __overall__ | coverage_delta | 1575 | -0.00539277 | 0 | -0.00674462 | -0.00410467 | 1.49993e-29 | 1.7528e-15 | 0.145397 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | -0.00123277 | 0 | -0.00219116 | -0.000249165 | 4.3962e-15 | 0.0124313 | 0.175873 |
