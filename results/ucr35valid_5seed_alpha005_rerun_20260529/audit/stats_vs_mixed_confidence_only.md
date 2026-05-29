# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_rerun_20260529/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `fast_cp_mixed_confidence_only`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | 0.083524 | 0.0407895 | 0.0704739 | 0.0966882 | 1.88833e-33 | 4.33004e-31 | 0.718095 |
| 0.05 | drift | coverage_delta | 525 | -0.00728808 | 0 | -0.00994092 | -0.00487172 | 1.9127e-18 | 3.87634e-08 | 0.146667 |
| 0.05 | drift | abs_gap_delta | 525 | 0.00266082 | 0 | 0.00092498 | 0.00455758 | 0.309572 | 0.00435892 | 0.28381 |
| 0.05 | gap | set_size_reduction | 525 | 0.0701427 | 0.028777 | 0.0558743 | 0.0843581 | 1.0955e-23 | 2.43633e-20 | 0.672381 |
| 0.05 | gap | coverage_delta | 525 | -0.00572935 | 0 | -0.00819054 | -0.0036278 | 2.23057e-08 | 1.18215e-06 | 0.222857 |
| 0.05 | gap | abs_gap_delta | 525 | 0.00252457 | 0 | 0.00101668 | 0.00421213 | 0.0485646 | 0.00190653 | 0.318095 |
| 0.05 | noise | set_size_reduction | 525 | 0.0465464 | 0.0166667 | 0.033139 | 0.060322 | 2.16201e-12 | 3.38613e-11 | 0.586667 |
| 0.05 | noise | coverage_delta | 525 | -0.000657785 | 0 | -0.00300195 | 0.00176932 | 0.00433507 | 0.582818 | 0.238095 |
| 0.05 | noise | abs_gap_delta | 525 | -0.00157124 | 0 | -0.00362969 | 0.000355291 | 0.0108644 | 0.124337 | 0.230476 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.0667377 | 0.0282051 | 0.0589673 | 0.0744762 | 4.41172e-64 | 1.11619e-56 | 0.659048 |
| 0.05 | __overall__ | coverage_delta | 1575 | -0.00455841 | 0 | -0.00594904 | -0.00322671 | 3.35206e-23 | 1.79653e-10 | 0.20254 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | 0.00120472 | 0 | 0.000179319 | 0.00228626 | 0.793334 | 0.0245505 | 0.27746 |
