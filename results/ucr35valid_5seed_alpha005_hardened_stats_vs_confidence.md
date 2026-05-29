# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_hardened/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `confidence_weighted_cp`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | 0.112387 | 0.058309 | 0.0918365 | 0.133643 | 6.48062e-29 | 1.26034e-23 | 0.697143 |
| 0.05 | drift | coverage_delta | 525 | -0.00468201 | 0 | -0.00795562 | -0.00147919 | 4.44424e-07 | 0.00478323 | 0.255238 |
| 0.05 | drift | abs_gap_delta | 525 | 0.00227147 | 0 | 6.12473e-05 | 0.00456277 | 0.519997 | 0.046516 | 0.348571 |
| 0.05 | gap | set_size_reduction | 525 | 0.106395 | 0.0437318 | 0.0847839 | 0.129373 | 4.28335e-22 | 9.09672e-19 | 0.672381 |
| 0.05 | gap | coverage_delta | 525 | -0.00384054 | 0 | -0.00705129 | -0.000793239 | 0.000125395 | 0.0154951 | 0.300952 |
| 0.05 | gap | abs_gap_delta | 525 | 0.0030204 | 0 | 0.000705545 | 0.00528328 | 0.0102928 | 0.00973295 | 0.386667 |
| 0.05 | noise | set_size_reduction | 525 | 0.0853522 | 0.0333333 | 0.0626255 | 0.109025 | 1.0026e-13 | 1.66722e-12 | 0.619048 |
| 0.05 | noise | coverage_delta | 525 | -0.00066206 | 0 | -0.00462119 | 0.00298269 | 0.00522677 | 0.728102 | 0.308571 |
| 0.05 | noise | abs_gap_delta | 525 | -0.000546421 | 0 | -0.00349305 | 0.0024156 | 0.792333 | 0.713365 | 0.344762 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.101378 | 0.0431655 | 0.0889302 | 0.114249 | 4.18448e-60 | 3.04006e-50 | 0.662857 |
| 0.05 | __overall__ | coverage_delta | 1575 | -0.00306154 | 0 | -0.00497608 | -0.00122969 | 1.91235e-11 | 0.00206674 | 0.288254 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | 0.00158182 | 0 | 0.000165524 | 0.00298242 | 0.0897555 | 0.0316516 | 0.36 |
