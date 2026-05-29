# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_hardened/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `fast_cp_mixed_no_confidence`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | -0.0516905 | -0.028777 | -0.0579085 | -0.045761 | 3.03971e-72 | 1.95549e-51 | 0.032381 |
| 0.05 | drift | coverage_delta | 525 | 0.00735456 | 0 | 0.00617061 | 0.00862031 | 1.21679e-41 | 1.80583e-28 | 0.487619 |
| 0.05 | drift | abs_gap_delta | 525 | -0.00236855 | 0 | -0.00357067 | -0.00121082 | 0.00340698 | 9.13693e-05 | 0.262857 |
| 0.05 | gap | set_size_reduction | 525 | -0.0412654 | -0.0194805 | -0.047745 | -0.035138 | 1.42092e-47 | 1.12768e-32 | 0.106667 |
| 0.05 | gap | coverage_delta | 525 | 0.00591883 | 0 | 0.00483841 | 0.00712355 | 2.0131e-31 | 1.6494e-22 | 0.438095 |
| 0.05 | gap | abs_gap_delta | 525 | -0.0020366 | 0 | -0.00321928 | -0.000926757 | 0.106829 | 0.000420102 | 0.27619 |
| 0.05 | noise | set_size_reduction | 525 | -0.0360251 | -0.0155556 | -0.0417549 | -0.0305251 | 2.92681e-45 | 2.81031e-32 | 0.112381 |
| 0.05 | noise | coverage_delta | 525 | 0.00502478 | 0 | 0.00379728 | 0.00628194 | 7.6985e-23 | 1.17955e-14 | 0.377143 |
| 0.05 | noise | abs_gap_delta | 525 | -0.00123579 | 0 | -0.00244814 | -5.82614e-05 | 0.540665 | 0.040547 | 0.257143 |
| 0.05 | __overall__ | set_size_reduction | 1575 | -0.0429937 | -0.0215827 | -0.0465633 | -0.0395597 | 2.30516e-160 | 3.04926e-111 | 0.0838095 |
| 0.05 | __overall__ | coverage_delta | 1575 | 0.00609939 | 0 | 0.00543613 | 0.00680598 | 1.57493e-91 | 5.69733e-61 | 0.434286 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | -0.00188031 | 0 | -0.00257567 | -0.00122275 | 0.00235873 | 4.44285e-08 | 0.265397 |
