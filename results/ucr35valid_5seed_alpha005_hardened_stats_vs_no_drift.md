# Paired Statistical Tests

Input: `results/ucr35valid_5seed_alpha005_hardened/fastcp_results.csv`
Candidate: `fast_cp_mixed`
Baseline: `fast_cp_mixed_no_drift`

Positive `set_size_reduction` means the candidate has smaller prediction sets.
Positive `coverage_delta` means the candidate has higher empirical coverage.
Negative `abs_gap_delta` means the candidate is closer to target coverage.

| alpha | corruption | metric | n_pairs | mean | median | ci95_low | ci95_high | wilcoxon_p | ttest_p | positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | drift | set_size_reduction | 525 | 0.00114099 | 0 | -0.00208191 | 0.00439944 | 0.0175035 | 0.49121 | 0.274286 |
| 0.05 | drift | coverage_delta | 525 | -0.000150776 | 0 | -0.000741421 | 0.000427798 | 0.219558 | 0.618602 | 0.0914286 |
| 0.05 | drift | abs_gap_delta | 525 | 8.54614e-05 | 0 | -0.000457621 | 0.000687187 | 0.733991 | 0.765567 | 0.121905 |
| 0.05 | gap | set_size_reduction | 525 | 0.00498126 | 0 | 0.00214278 | 0.00776847 | 0.0283785 | 0.000874034 | 0.344762 |
| 0.05 | gap | coverage_delta | 525 | -0.000655198 | 0 | -0.00116533 | -0.000176265 | 0.000271246 | 0.012884 | 0.08 |
| 0.05 | gap | abs_gap_delta | 525 | 0.000684393 | 0 | 0.000199045 | 0.00114753 | 3.09337e-05 | 0.00406084 | 0.173333 |
| 0.05 | noise | set_size_reduction | 525 | 0.00267525 | 0 | -0.000287048 | 0.0056365 | 0.677591 | 0.0779832 | 0.304762 |
| 0.05 | noise | coverage_delta | 525 | -0.000501339 | 0 | -0.000916634 | -9.47605e-05 | 0.00117344 | 0.0199403 | 0.0971429 |
| 0.05 | noise | abs_gap_delta | 525 | 0.000592565 | 0 | 0.000205922 | 0.00102159 | 0.0183666 | 0.00563587 | 0.146667 |
| 0.05 | __overall__ | set_size_reduction | 1575 | 0.0029325 | 0 | 0.00118945 | 0.0047742 | 0.876419 | 0.00111585 | 0.307937 |
| 0.05 | __overall__ | coverage_delta | 1575 | -0.000435771 | 0 | -0.000743641 | -0.000145752 | 2.84649e-06 | 0.00408462 | 0.0895238 |
| 0.05 | __overall__ | abs_gap_delta | 1575 | 0.00045414 | 0 | 0.000187234 | 0.00074322 | 5.28449e-05 | 0.00151676 | 0.147302 |
