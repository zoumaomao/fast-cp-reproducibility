# Paired Statistical Tests

Input: `results/uea_external_3ds_3seed_alpha005/fastcp_uea_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `aug_split_cp`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 27 | 0.0440777 | 0.0166667 | 0.0255137 | 0.0651284 | 0.000435842 | 0.000191563 | 0.592593 |
| 0.05 | drift | coverage_delta | 27 | -0.00191447 | 0 | -0.00366792 | -0.0003489 | 0.0649778 | 0.0372781 | 0.037037 |
| 0.05 | drift | abs_gap_delta | 27 | 0.000966184 | 0 | -0.000867776 | 0.00273752 | 0.28703 | 0.30863 | 0.222222 |
| 0.05 | gap | set_size_reduction | 27 | 0.0527152 | 0.0388889 | 0.030362 | 0.0774898 | 0.000516133 | 0.000187525 | 0.62963 |
| 0.05 | gap | coverage_delta | 27 | 0.00123457 | 0 | -0.00123457 | 0.00421811 | 0.461838 | 0.401082 | 0.111111 |
| 0.05 | gap | abs_gap_delta | 27 | 0.00246914 | 0 | 0.000143138 | 0.00524691 | 0.0739374 | 0.0860999 | 0.185185 |
| 0.05 | noise | set_size_reduction | 27 | 0.0542136 | 0.0388889 | 0.0330647 | 0.0778505 | 0.000293053 | 9.78348e-05 | 0.62963 |
| 0.05 | noise | coverage_delta | 27 | -0.00191447 | 0 | -0.00329218 | -0.000679907 | 0.0175523 | 0.00910349 | 0 |
| 0.05 | noise | abs_gap_delta | 27 | 0.000143138 | 0 | -0.00134192 | 0.00164609 | 0.799143 | 0.855019 | 0.148148 |
| 0.05 | __overall__ | set_size_reduction | 81 | 0.0503355 | 0.0289855 | 0.0380501 | 0.0628934 | 1.28768e-09 | 2.74857e-11 | 0.617284 |
| 0.05 | __overall__ | coverage_delta | 81 | -0.000864794 | 0 | -0.00202496 | 0.000404105 | 0.0773798 | 0.168075 | 0.0493827 |
| 0.05 | __overall__ | abs_gap_delta | 81 | 0.00119282 | 0 | 5.36396e-05 | 0.00240055 | 0.0663517 | 0.0559109 | 0.185185 |
