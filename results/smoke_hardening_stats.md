# Paired Statistical Tests

Input: `results/smoke_hardening/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `aug_split_cp`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | gap | set_size_reduction | 6 | 0.0661111 | 0.0716667 | 0.0305556 | 0.103653 | 0.0625 | 0.0234168 | 0.833333 |
| 0.05 | gap | coverage_delta | 6 | -0.00222222 | 0 | -0.00502778 | 0 | 0.5 | 0.174688 | 0 |
| 0.05 | gap | abs_gap_delta | 6 | -0.00222222 | 0 | -0.00502778 | 0 | 0.5 | 0.174688 | 0 |
| 0.05 | noise | set_size_reduction | 6 | 0.05 | 0.06 | 0.00444444 | 0.0891806 | 0.15625 | 0.0957837 | 0.833333 |
| 0.05 | noise | coverage_delta | 6 | -0.00444444 | -0.00333333 | -0.0216944 | 0.0161389 | 0.875 | 0.698809 | 0.166667 |
| 0.05 | noise | abs_gap_delta | 6 | -0.00444444 | -0.00333333 | -0.0233333 | 0.0133333 | 0.625 | 0.698809 | 0.166667 |
| 0.05 | __overall__ | set_size_reduction | 12 | 0.0580556 | 0.06 | 0.0279097 | 0.0836111 | 0.00878906 | 0.00309209 | 0.833333 |
| 0.05 | __overall__ | coverage_delta | 12 | -0.00333333 | 0 | -0.0125139 | 0.00611111 | 0.40625 | 0.53635 | 0.0833333 |
| 0.05 | __overall__ | abs_gap_delta | 12 | -0.00333333 | 0 | -0.0119583 | 0.00611111 | 0.3125 | 0.53635 | 0.0833333 |
