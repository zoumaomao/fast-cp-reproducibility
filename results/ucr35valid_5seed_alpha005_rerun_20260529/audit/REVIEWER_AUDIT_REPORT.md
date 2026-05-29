# FAST-CP Reviewer Audit Report

## Full Method Table

| method | coverage | avg_set_size | abs_gap | coverage_delta_vs_aug | set_size_reduction_vs_aug | drift_set_size | gap_set_size | noise_set_size |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Clean SCP | 0.8656 | 1.9323 | 0.1049 | -0.0846 | 0.4862 | 1.9412 | 1.9240 | 1.9315 |
| Aug SCP / FAST-CP-safe | 0.9501 | 2.4185 | 0.0467 | 0.0000 | 0.0000 | 2.4405 | 2.4151 | 2.3998 |
| APS | 0.9757 | 3.2595 | 0.0423 | 0.0256 | -0.8411 | 3.2654 | 3.2128 | 3.3005 |
| RAPS | 0.9730 | 2.7313 | 0.0424 | 0.0229 | -0.3128 | 2.7262 | 2.7293 | 2.7384 |
| Mondrian | 0.9553 | 2.5021 | 0.0418 | 0.0052 | -0.0837 | 2.3172 | 2.7412 | 2.4480 |
| Conf-weighted | 0.9478 | 2.4262 | 0.0440 | -0.0023 | -0.0078 | 2.4421 | 2.4310 | 2.4056 |
| FAST-CP-local | 0.9440 | 2.3112 | 0.0446 | -0.0061 | 0.1073 | 2.3003 | 2.3096 | 2.3236 |
| FAST-CP-efficient | 0.9448 | 2.3254 | 0.0455 | -0.0053 | 0.0931 | 2.3309 | 2.3240 | 2.3213 |

## FAST-CP-Efficient vs Augmented Split CP

| alpha | corruption | n | candidate_coverage | baseline_coverage | coverage_delta | candidate_set_size | baseline_set_size | set_size_reduction | set_size_reduction_pct | candidate_abs_gap | baseline_abs_gap | abs_gap_delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0500 | drift | 525 | 0.9564 | 0.9651 | -0.0086 | 2.3309 | 2.4405 | 0.1096 | 0.0444 | 0.0367 | 0.0365 | 0.0002 |
| 0.0500 | gap | 525 | 0.9382 | 0.9437 | -0.0056 | 2.3240 | 2.4151 | 0.0911 | 0.0387 | 0.0500 | 0.0507 | -0.0007 |
| 0.0500 | noise | 525 | 0.9398 | 0.9415 | -0.0017 | 2.3213 | 2.3998 | 0.0785 | 0.0302 | 0.0499 | 0.0530 | -0.0032 |

## Undercoverage Tail Risk

| method | corruption | n_cells | mean_coverage | rate_below_target | rate_below_target_minus_1pp | rate_below_target_minus_2pp | p10_coverage | min_coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Aug SCP / FAST-CP-safe | __overall__ | 1575 | 0.9501 | 0.3283 | 0.2698 | 0.2222 | 0.8777 | 0.4629 |
| Aug SCP / FAST-CP-safe | drift | 525 | 0.9651 | 0.2610 | 0.1886 | 0.1505 | 0.9178 | 0.5314 |
| Aug SCP / FAST-CP-safe | gap | 525 | 0.9437 | 0.3752 | 0.3352 | 0.2781 | 0.8482 | 0.6333 |
| Aug SCP / FAST-CP-safe | noise | 525 | 0.9415 | 0.3486 | 0.2857 | 0.2381 | 0.8636 | 0.4629 |
| FAST-CP-efficient | __overall__ | 1575 | 0.9448 | 0.3905 | 0.3111 | 0.2565 | 0.8699 | 0.5029 |
| FAST-CP-efficient | drift | 525 | 0.9564 | 0.3448 | 0.2495 | 0.1886 | 0.9039 | 0.5314 |
| FAST-CP-efficient | gap | 525 | 0.9382 | 0.4324 | 0.3695 | 0.3124 | 0.8411 | 0.6333 |
| FAST-CP-efficient | noise | 525 | 0.9398 | 0.3943 | 0.3143 | 0.2686 | 0.8606 | 0.5029 |
| Confidence-only | __overall__ | 1575 | 0.9494 | 0.3283 | 0.2660 | 0.2121 | 0.8847 | 0.4971 |
| Confidence-only | drift | 525 | 0.9637 | 0.2533 | 0.1848 | 0.1410 | 0.9200 | 0.5314 |
| Confidence-only | gap | 525 | 0.9439 | 0.3943 | 0.3314 | 0.2629 | 0.8522 | 0.6333 |
| Confidence-only | noise | 525 | 0.9405 | 0.3371 | 0.2819 | 0.2324 | 0.8536 | 0.4971 |

## Worst 10 Coverage Drops

| dataset | seed | corruption | severity | alpha | fast_coverage | aug_coverage | coverage_delta | fast_set_size | aug_set_size | set_size_reduction | n_test | n_classes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Coffee | 3 | drift | 0.4000 | 0.0500 | 0.6786 | 1.0000 | -0.3214 | 1.2857 | 1.6071 | 0.3214 | 28 | 2 |
| BirdChicken | 2 | gap | 0.2000 | 0.0500 | 0.7000 | 1.0000 | -0.3000 | 1.3000 | 2.0000 | 0.7000 | 20 | 2 |
| Coffee | 2 | drift | 0.4000 | 0.0500 | 0.7500 | 1.0000 | -0.2500 | 1.1786 | 1.4643 | 0.2857 | 28 | 2 |
| BirdChicken | 2 | gap | 0.1000 | 0.0500 | 0.7500 | 1.0000 | -0.2500 | 1.3500 | 2.0000 | 0.6500 | 20 | 2 |
| BirdChicken | 2 | drift | 0.4000 | 0.0500 | 0.7500 | 1.0000 | -0.2500 | 1.5000 | 2.0000 | 0.5000 | 20 | 2 |
| BirdChicken | 2 | noise | 0.0500 | 0.0500 | 0.8000 | 1.0000 | -0.2000 | 1.5500 | 2.0000 | 0.4500 | 20 | 2 |
| BirdChicken | 2 | gap | 0.0500 | 0.0500 | 0.8000 | 1.0000 | -0.2000 | 1.3500 | 2.0000 | 0.6500 | 20 | 2 |
| BirdChicken | 2 | drift | 0.1000 | 0.0500 | 0.8000 | 1.0000 | -0.2000 | 1.3000 | 2.0000 | 0.7000 | 20 | 2 |
| BirdChicken | 2 | drift | 0.2000 | 0.0500 | 0.8000 | 1.0000 | -0.2000 | 1.3500 | 2.0000 | 0.6500 | 20 | 2 |
| Coffee | 3 | gap | 0.2000 | 0.0500 | 0.8214 | 1.0000 | -0.1786 | 1.2500 | 1.8214 | 0.5714 | 28 | 2 |

## Severity Summary

| method | corruption | severity | n_cells | coverage | avg_set_size | abs_gap |
| --- | --- | --- | --- | --- | --- | --- |
| Aug SCP / FAST-CP-safe | drift | 0.1000 | 175 | 0.9778 | 2.4734 | 0.0349 |
| FAST-CP-efficient | drift | 0.1000 | 175 | 0.9724 | 2.3589 | 0.0330 |
| Aug SCP / FAST-CP-safe | drift | 0.2000 | 175 | 0.9717 | 2.4596 | 0.0318 |
| FAST-CP-efficient | drift | 0.2000 | 175 | 0.9661 | 2.3552 | 0.0315 |
| Aug SCP / FAST-CP-safe | drift | 0.4000 | 175 | 0.9457 | 2.3886 | 0.0428 |
| FAST-CP-efficient | drift | 0.4000 | 175 | 0.9308 | 2.2785 | 0.0458 |
| Aug SCP / FAST-CP-safe | gap | 0.0500 | 175 | 0.9751 | 2.4624 | 0.0356 |
| FAST-CP-efficient | gap | 0.0500 | 175 | 0.9718 | 2.3530 | 0.0347 |
| Aug SCP / FAST-CP-safe | gap | 0.1000 | 175 | 0.9605 | 2.4559 | 0.0356 |
| FAST-CP-efficient | gap | 0.1000 | 175 | 0.9546 | 2.3569 | 0.0350 |
| Aug SCP / FAST-CP-safe | gap | 0.2000 | 175 | 0.8956 | 2.3269 | 0.0808 |
| FAST-CP-efficient | gap | 0.2000 | 175 | 0.8881 | 2.2620 | 0.0802 |
| Aug SCP / FAST-CP-safe | noise | 0.0500 | 175 | 0.9793 | 2.4869 | 0.0353 |
| FAST-CP-efficient | noise | 0.0500 | 175 | 0.9749 | 2.3764 | 0.0341 |
| Aug SCP / FAST-CP-safe | noise | 0.1000 | 175 | 0.9691 | 2.4557 | 0.0323 |
| FAST-CP-efficient | noise | 0.1000 | 175 | 0.9614 | 2.3541 | 0.0325 |
| Aug SCP / FAST-CP-safe | noise | 0.2000 | 175 | 0.8761 | 2.2568 | 0.0915 |
| FAST-CP-efficient | noise | 0.2000 | 175 | 0.8831 | 2.2335 | 0.0830 |

## Fingerprint Variants

| variant | coverage | avg_set_size | abs_gap | coverage_delta_vs_aug | set_size_reduction_vs_aug |
| --- | --- | --- | --- | --- | --- |
| Random fingerprint | 0.9440 | 2.3681 | 0.0489 | -0.0061 | 0.0504 |
| Input-only | 0.9387 | 2.2820 | 0.0474 | -0.0114 | 0.1365 |
| Confidence-only | 0.9494 | 2.3921 | 0.0443 | -0.0008 | 0.0263 |
| FAST-CP-efficient | 0.9448 | 2.3254 | 0.0455 | -0.0053 | 0.0931 |

