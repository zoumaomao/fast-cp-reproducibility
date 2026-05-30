# Dataset-Level Block Bootstrap

Input: `results/ucr35valid_5seed_alpha005_rerun_20260529/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `aug_split_cp`

Each dataset is treated as one resampling block. Metrics are first averaged within each dataset over seeds, corruptions, and severities, then bootstrapped over datasets.
Positive `set_size_reduction` means the candidate has smaller prediction sets. Positive `coverage_delta` means the candidate has higher empirical coverage. Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_datasets | dataset_block_mean | dataset_block_median | ci95_low | ci95_high | positive_dataset_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | __overall__ | set_size_reduction | 35 | 0.0930751 | 0.0768091 | 0.0645984 | 0.123566 | 0.914286 |
| 0.05 | __overall__ | coverage_delta | 35 | -0.00531189 | -0.0033189 | -0.00856501 | -0.00251433 | 0.171429 |
| 0.05 | __overall__ | abs_gap_delta | 35 | -0.00121268 | -0.000905218 | -0.00288811 | 0.000633116 | 0.285714 |
| 0.05 | drift | set_size_reduction | 35 | 0.109646 | 0.102406 | 0.0781289 | 0.143413 | 0.942857 |
| 0.05 | drift | coverage_delta | 35 | -0.00864381 | -0.00454545 | -0.0128637 | -0.00481237 | 0.114286 |
| 0.05 | drift | abs_gap_delta | 35 | 0.000245226 | -0.000683761 | -0.00185286 | 0.00256545 | 0.4 |
| 0.05 | gap | set_size_reduction | 35 | 0.091104 | 0.0556962 | 0.0568726 | 0.128299 | 0.857143 |
| 0.05 | gap | coverage_delta | 35 | -0.00557017 | -0.00189873 | -0.00959123 | -0.00211339 | 0.285714 |
| 0.05 | gap | abs_gap_delta | 35 | -0.000695421 | -0.00205128 | -0.00271311 | 0.00176427 | 0.228571 |
| 0.05 | noise | set_size_reduction | 35 | 0.0784751 | 0.0435556 | 0.052041 | 0.107691 | 0.885714 |
| 0.05 | noise | coverage_delta | 35 | -0.0017217 | -0.00182648 | -0.00476437 | 0.00118594 | 0.371429 |
| 0.05 | noise | abs_gap_delta | 35 | -0.00318785 | -0.00209073 | -0.00537159 | -0.00106142 | 0.257143 |
