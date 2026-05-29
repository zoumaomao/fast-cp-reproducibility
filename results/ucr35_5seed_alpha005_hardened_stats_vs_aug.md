# Paired Statistical Tests

Input: `results/ucr35_5seed_alpha005_hardened/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `aug_split_cp`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 510 | 0.112628 | 0.0455844 | 0.0992562 | 0.126304 | 3.41569e-60 | 3.94357e-48 | 0.768627 |
| 0.05 | drift | coverage_delta | 510 | -0.00890493 | 0 | -0.0117361 | -0.00649283 | 2.19687e-24 | 5.70701e-11 | 0.0941176 |
| 0.05 | drift | abs_gap_delta | 510 | 7.78023e-05 | 0 | -0.00166574 | 0.00198582 | 0.000363338 | 0.933375 | 0.192157 |
| 0.05 | gap | set_size_reduction | 510 | 0.0926667 | 0.025974 | 0.0784986 | 0.107009 | 7.39408e-37 | 6.58573e-31 | 0.7 |
| 0.05 | gap | coverage_delta | 510 | -0.00571612 | 0 | -0.00823298 | -0.00349534 | 1.81342e-08 | 2.86959e-06 | 0.170588 |
| 0.05 | gap | abs_gap_delta | 510 | -0.000635299 | 0 | -0.00215412 | 0.00110186 | 4.30827e-05 | 0.447584 | 0.17451 |
| 0.05 | noise | set_size_reduction | 510 | 0.0807062 | 0.02 | 0.067345 | 0.0946272 | 9.56331e-32 | 1.50956e-27 | 0.643137 |
| 0.05 | noise | coverage_delta | 510 | -0.00195637 | 0 | -0.00394692 | 2.89678e-05 | 0.00113135 | 0.0530442 | 0.184314 |
| 0.05 | noise | abs_gap_delta | 510 | -0.00317284 | 0 | -0.00489209 | -0.00152862 | 4.10691e-08 | 0.00025434 | 0.176471 |
| 0.05 | __overall__ | set_size_reduction | 1530 | 0.0953335 | 0.028777 | 0.0875052 | 0.103934 | 7.11591e-124 | 3.4179e-101 | 0.703922 |
| 0.05 | __overall__ | coverage_delta | 1530 | -0.00552581 | 0 | -0.00691731 | -0.00425938 | 2.99467e-28 | 2.32317e-15 | 0.149673 |
| 0.05 | __overall__ | abs_gap_delta | 1530 | -0.00124344 | 0 | -0.00221111 | -0.000208591 | 3.18987e-14 | 0.0143118 | 0.181046 |
