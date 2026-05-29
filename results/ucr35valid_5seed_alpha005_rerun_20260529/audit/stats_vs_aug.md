# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_rerun_20260529/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `aug_split_cp`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | 0.109646 | 0.0431655 | 0.0969511 | 0.122643 | 3.57902e-64 | 7.52485e-49 | 0.784762 |
| 0.05 | drift | coverage_delta | 525 | -0.00864381 | 0 | -0.0113312 | -0.00626273 | 1.0075e-24 | 5.3706e-11 | 0.087619 |
| 0.05 | drift | abs_gap_delta | 525 | 0.000245226 | 0 | -0.00144508 | 0.0021224 | 0.000997065 | 0.784769 | 0.192381 |
| 0.05 | gap | set_size_reduction | 525 | 0.091104 | 0.025974 | 0.0766221 | 0.105646 | 3.7269e-38 | 2.37683e-31 | 0.693333 |
| 0.05 | gap | coverage_delta | 525 | -0.00557017 | 0 | -0.00803699 | -0.00341693 | 6.76634e-09 | 2.67519e-06 | 0.161905 |
| 0.05 | gap | abs_gap_delta | 525 | -0.000695421 | 0 | -0.00221971 | 0.00102149 | 1.44016e-05 | 0.391814 | 0.16381 |
| 0.05 | noise | set_size_reduction | 525 | 0.0784751 | 0.0206186 | 0.065741 | 0.0918139 | 8.49437e-34 | 7.45753e-28 | 0.660952 |
| 0.05 | noise | coverage_delta | 525 | -0.0017217 | 0 | -0.00366635 | 0.000198046 | 0.00215725 | 0.077688 | 0.184762 |
| 0.05 | noise | abs_gap_delta | 525 | -0.00318785 | 0 | -0.00484909 | -0.00152497 | 1.2002e-08 | 0.000130738 | 0.169524 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.0930751 | 0.03 | 0.085592 | 0.100655 | 1.30493e-130 | 1.51619e-102 | 0.713016 |
| 0.05 | __overall__ | coverage_delta | 1575 | -0.00531189 | 0 | -0.00664019 | -0.00403603 | 2.266e-28 | 3.89008e-15 | 0.144762 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | -0.00121268 | 0 | -0.00215128 | -0.000211566 | 1.58639e-14 | 0.0133571 | 0.175238 |
