# Paired Statistical Tests

Input: `results/mismatch_gap_noise_calib_drift_mixed_test_10ds_3seed_alpha005/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `aug_split_cp`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 90 | 0.125228 | 0.0716456 | 0.0968565 | 0.158149 | 8.62641e-15 | 3.93782e-12 | 0.866667 |
| 0.05 | drift | coverage_delta | 90 | -0.00571254 | 0 | -0.00812209 | -0.00355309 | 4.33771e-07 | 4.78928e-06 | 0.0888889 |
| 0.05 | drift | abs_gap_delta | 90 | -0.00195792 | 0 | -0.00388934 | 2.90095e-05 | 0.0160675 | 0.0590976 | 0.166667 |
| 0.05 | mixed | set_size_reduction | 90 | 0.0620063 | 0.0294173 | 0.0384787 | 0.0869623 | 1.57695e-06 | 3.30529e-06 | 0.677778 |
| 0.05 | mixed | coverage_delta | 90 | -0.00395635 | -0.000555556 | -0.00640352 | -0.00151299 | 0.00192862 | 0.00209389 | 0.222222 |
| 0.05 | mixed | abs_gap_delta | 90 | -0.000703173 | 0 | -0.0028581 | 0.00145964 | 0.410252 | 0.526876 | 0.3 |
| 0.05 | __overall__ | set_size_reduction | 180 | 0.0936173 | 0.0466667 | 0.0748796 | 0.114042 | 1.76297e-19 | 1.37695e-16 | 0.772222 |
| 0.05 | __overall__ | coverage_delta | 180 | -0.00483444 | 0 | -0.00660179 | -0.00328286 | 1.67811e-08 | 6.38772e-08 | 0.155556 |
| 0.05 | __overall__ | abs_gap_delta | 180 | -0.00133055 | 0 | -0.00281606 | 0.000173981 | 0.0255009 | 0.0790558 | 0.233333 |
