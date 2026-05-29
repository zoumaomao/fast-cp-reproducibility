# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_rerun_20260529/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `fast_cp_mixed_input_only`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | -0.052576 | -0.028777 | -0.0589246 | -0.046632 | 2.96332e-72 | 1.16114e-50 | 0.0304762 |
| 0.05 | drift | coverage_delta | 525 | 0.00744219 | 0 | 0.00624481 | 0.00874137 | 3.34807e-43 | 1.14833e-27 | 0.499048 |
| 0.05 | drift | abs_gap_delta | 525 | -0.00227948 | 0 | -0.00343656 | -0.00116695 | 0.00246687 | 7.9502e-05 | 0.262857 |
| 0.05 | gap | set_size_reduction | 525 | -0.0410698 | -0.0194805 | -0.0475632 | -0.0348423 | 4.69362e-47 | 3.43437e-32 | 0.0990476 |
| 0.05 | gap | coverage_delta | 525 | 0.00580799 | 0 | 0.00472037 | 0.00701683 | 2.48316e-29 | 1.9764e-21 | 0.43619 |
| 0.05 | gap | abs_gap_delta | 525 | -0.00194516 | 0 | -0.00310869 | -0.000831433 | 0.155982 | 0.00081688 | 0.27619 |
| 0.05 | noise | set_size_reduction | 525 | -0.0365409 | -0.0158228 | -0.0423683 | -0.0310271 | 1.44386e-46 | 5.94385e-33 | 0.112381 |
| 0.05 | noise | coverage_delta | 525 | 0.00511871 | 0 | 0.00390206 | 0.00639067 | 5.53952e-24 | 2.46839e-15 | 0.386667 |
| 0.05 | noise | abs_gap_delta | 525 | -0.00129252 | 0 | -0.00252635 | -0.000159839 | 0.436296 | 0.0329098 | 0.251429 |
| 0.05 | __overall__ | set_size_reduction | 1575 | -0.0433956 | -0.0215827 | -0.0469945 | -0.0399026 | 1.59465e-161 | 7.44721e-111 | 0.0806349 |
| 0.05 | __overall__ | coverage_delta | 1575 | 0.00612296 | 0 | 0.00543366 | 0.00683955 | 5.77052e-92 | 2.88033e-60 | 0.440635 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | -0.00183905 | 0 | -0.00252514 | -0.00119991 | 0.00219623 | 6.04199e-08 | 0.263492 |
