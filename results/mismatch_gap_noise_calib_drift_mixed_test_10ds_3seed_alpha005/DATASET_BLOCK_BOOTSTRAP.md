# Dataset-Level Block Bootstrap

Input: `results/mismatch_gap_noise_calib_drift_mixed_test_10ds_3seed_alpha005/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `aug_split_cp`

Each dataset is treated as one resampling block. Metrics are first averaged within each dataset over seeds, corruptions, and severities, then bootstrapped over datasets.
Positive `set_size_reduction` means the candidate has smaller prediction sets. Positive `coverage_delta` means the candidate has higher empirical coverage. Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_datasets | dataset_block_mean | dataset_block_median | ci95_low | ci95_high | positive_dataset_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | __overall__ | set_size_reduction | 10 | 0.0936173 | 0.117147 | 0.0538927 | 0.1323 | 1 |
| 0.05 | __overall__ | coverage_delta | 10 | -0.00483444 | -0.00295223 | -0.0086561 | -0.00172149 | 0.2 |
| 0.05 | __overall__ | abs_gap_delta | 10 | -0.00133055 | -0.00195959 | -0.00340641 | 0.000970996 | 0.2 |
| 0.05 | drift | set_size_reduction | 10 | 0.125228 | 0.161979 | 0.0689391 | 0.179211 | 1 |
| 0.05 | drift | coverage_delta | 10 | -0.00571254 | -0.00315425 | -0.010386 | -0.0019578 | 0.1 |
| 0.05 | drift | abs_gap_delta | 10 | -0.00195792 | -0.00173374 | -0.00402561 | -4.01654e-05 | 0.3 |
| 0.05 | mixed | set_size_reduction | 10 | 0.0620063 | 0.04783 | 0.0335914 | 0.093493 | 0.9 |
| 0.05 | mixed | coverage_delta | 10 | -0.00395635 | -0.00339689 | -0.00749339 | -0.000918099 | 0.3 |
| 0.05 | mixed | abs_gap_delta | 10 | -0.000703173 | -0.00122671 | -0.00378264 | 0.00249074 | 0.4 |
