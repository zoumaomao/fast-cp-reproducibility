# FAST-CP Experiment Log

This log records experiment updates, commands, result summaries, and output locations.

## 2026-05-29

### Reference metadata cleanup - completed

Purpose:

- Replace preprint-style references with formal publication metadata where available.
- Normalize author order, title capitalization, DOI fields, and name spelling before submission.

Changes:

- Replaced the Angelopoulos and Bates conformal prediction introduction entry with the 2023 Foundations and Trends in Machine Learning version.
- Replaced the aeon entry with the 2024 Journal of Machine Learning Research version.
- Updated the ICLR conformal image-classifier entry author order to Angelopoulos, Bates, Jordan, and Malik.
- Standardized the MiniROCKET title capitalization and retained its KDD DOI.
- Standardized Nanopoulos and Buza spelling in the bibliography.

### Statements and declarations update - completed

Purpose:

- Add a Springer/PAA-style generative AI disclosure before submission.

Change:

- Added `paper/sections/7_declarations.tex`.
- Included a `Statements and Declarations` section before the bibliography in `paper/main.tex`.
- Declared that ChatGPT assisted with drafting, language editing, readability, and organization, while human authors conducted and verified the experimental design, implementation, analysis, interpretation, and conclusions.

### Pattern Analysis and Applications submission framing - completed

Purpose:

- Retarget the manuscript framing toward an application-oriented pattern analysis venue.
- Avoid presenting FAST-CP as a theory-first conformal-validity improvement under distribution shift.
- Prepare a reproducibility package aligned with the journal's replicable research expectation.

Changes:

- Updated the title to: "FAST-CP: A Lightweight Perturbation-Aware Conformal Prediction Framework for Corrupted Time-Series Classification".
- Rewrote the abstract around corrupted time-series classification, lightweight post-hoc uncertainty calibration, practical coverage-efficiency tradeoff, reproducible benchmarking, and limited compute.
- Added `README.md` with setup, public UCR/UEA data access, reproduction commands, saved CSV result locations, and submission package checklist.
- Added `REPRODUCIBILITY.md` with a concise code/data/results/hardware statement for submission materials.
- Added TensorFlow to `requirements.txt` for the FCN backbone check.

### Submission polish after final internal review - completed

Purpose:

- Apply final wording changes before submission.
- Reduce the chance that reviewers misread efficiency deltas as standalone wins.
- Make limitations read like scoped claims rather than defensive self-criticism.

Changes:

- Renamed the main table column from `Reduction` to `Size Delta vs Aug` in the manuscript source.
- Added a Table 1 caption note that positive size deltas indicate smaller sets than Aug SCP but must be interpreted jointly with coverage.
- Replaced the abstract conclusion phrase `perturbation-aware post-hoc calibration` with `perturbation-aware local weighting, combined with global fallback calibration`.
- Replaced `semi-real corrupted inputs` with `real multichannel series under synthetic gap, noise, and drift stress tests`.
- Reorganized limitations into three categories: validity/calibration scope, data/model coverage, and fingerprint/hyperparameter limitations.

Verification:

- Recompiled `paper/main.pdf`.
- Final PDF: 15 pages.
- No undefined citations/references, no overfull boxes, and no Type 3 fonts detected.

### Expanded UCR/FAST-CP benchmark with control ablations - completed

Purpose:

- Regenerate the 35-dataset, five-seed FAST-CP benchmark inside the project root only.
- Avoid relying on any previous adjacent-project outputs.
- Add same-framework fingerprint controls requested by review: input-only, confidence-only, full fingerprint, and random fingerprint.
- Produce reviewer audit artifacts for undercoverage tails, worst coverage drops, severity-level behavior, and a complete method table.

Command:

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets ArrowHead BME Beef BeetleFly BirdChicken CBF Chinatown Coffee CricketX CricketY CricketZ DistalPhalanxOutlineAgeGroup DistalPhalanxOutlineCorrect DistalPhalanxTW ECG200 ECGFiveDays Earthquakes FaceAll FaceFour FacesUCR Fish GunPoint GunPointAgeSpan GunPointMaleVersusFemale GunPointOldVersusYoung Ham Herring ItalyPowerDemand Lightning7 Meat MedicalImages MiddlePhalanxOutlineAgeGroup MiddlePhalanxOutlineCorrect MiddlePhalanxTW MoteStrain \
  --seeds 0 1 2 3 4 \
  --corruptions gap noise drift \
  --alphas 0.05 \
  --n-kernels 64 \
  --fastcp-global-mix 0.35 \
  --fingerprint-ablations input_only confidence_only no_missing no_spectral no_drift no_confidence random_fingerprint \
  --continue-on-error \
  --out-dir results/ucr35valid_5seed_alpha005_rerun_20260529
```

Planned result files:

- `results/ucr35valid_5seed_alpha005_rerun_20260529/fastcp_results.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/run_summary.json`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/logs/run.log`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/REVIEWER_AUDIT_REPORT.md`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/full_method_table.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/tail_risk_table.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/worst_coverage_drops.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/severity_summary.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/fingerprint_variant_table.csv`

Run summary:

- Status: completed.
- Datasets: 35.
- Seeds: `0 1 2 3 4`.
- Corruptions: `gap noise drift`.
- Alpha: `0.05`.
- Rows: 25200.
- Runtime: 2863.665 seconds, or 47.7 minutes, on Apple M4 16 GB.
- Error log: none.

Key result for `fast_cp_mixed` / FAST-CP-efficient versus augmented split CP:

| Corruption | Coverage delta | Set-size reduction | Reduction | Abs.-gap delta |
|---|---:|---:|---:|---:|
| Drift | -0.0086 | 0.1096 | 4.44% | 0.0002 |
| Gap | -0.0056 | 0.0911 | 3.87% | -0.0007 |
| Noise | -0.0017 | 0.0785 | 3.02% | -0.0032 |
| Overall | -0.0053 | 0.0931 | n/a | -0.0012 |

Reviewer audit highlights:

- Undercoverage tail risk increased relative to augmented split CP: below-target cell rate `32.83% -> 39.05%`; below target by more than 1 pp `26.98% -> 31.11%`.
- Worst coverage drops are concentrated in tiny test sets such as `Coffee` and `BirdChicken`.
- Fingerprint controls show a nuanced contribution:
  - random fingerprint: coverage `0.9440`, set size `2.3681`, reduction `0.0504`;
  - input-only: coverage `0.9387`, set size `2.2820`, reduction `0.1365`;
  - confidence-only: coverage `0.9494`, set size `2.3921`, reduction `0.0263`;
  - full fingerprint: coverage `0.9448`, set size `2.3254`, reduction `0.0931`.

Paper update:

- Renamed the paper to "FAST-CP: Perturbation-Aware Post-Hoc Conformal Calibration for Corrupted Time-Series Classification".
- Reframed the coverage-prioritized mode as a global fallback rather than a separate FAST-CP variant.
- Added full method table, undercoverage-tail audit, coverage-delta tail figure, and fingerprint/random-control table.
- Recompiled `paper/main.pdf`; final check found no undefined references/citations, no overfull boxes, and no Type 3 fonts.

### External UEA multivariate validation - completed

Purpose:

- Add a small external validation beyond univariate UCR.
- Use real multichannel sensor/motion series from UEA datasets, then apply the same semi-real gap, noise, and drift stress tests.
- Check whether the FAST-CP tradeoff persists outside the main UCR setting.

Command:

```bash
.venv/bin/python -m experiments.run_external_uea_validation \
  --datasets BasicMotions Epilepsy NATOPS \
  --seeds 0 1 2 \
  --alphas 0.05 \
  --n-kernels 24 \
  --out-dir results/uea_external_3ds_3seed_alpha005
```

Run summary:

- Status: completed.
- Datasets: `BasicMotions`, `Epilepsy`, `NATOPS`.
- Seeds: `0 1 2`.
- Rows: 486.
- Runtime: 134.235 seconds.

Key result for `fast_cp_mixed` versus augmented split CP:

| Corruption | FAST coverage | Aug coverage | Coverage delta | Set-size reduction |
|---|---:|---:|---:|---:|
| Drift | 0.9499 | 0.9519 | -0.0019 | 0.0441 |
| Gap | 0.9491 | 0.9479 | 0.0012 | 0.0527 |
| Noise | 0.9639 | 0.9658 | -0.0019 | 0.0542 |
| Overall | 0.9543 | 0.9552 | -0.0009 | 0.0503 |

Result files:

- `results/uea_external_3ds_3seed_alpha005/fastcp_uea_results.csv`
- `results/uea_external_3ds_3seed_alpha005/fastcp_vs_aug.csv`
- `results/uea_external_3ds_3seed_alpha005/stats_vs_aug.csv`
- `results/uea_external_3ds_3seed_alpha005/stats_vs_aug.md`
- `results/uea_external_3ds_3seed_alpha005/run_summary.json`

### Deep FCN backbone check - completed

Purpose:

- Add a small deep TSC backbone supplement.
- Test whether the mixed-threshold Pareto behavior is exclusive to the compact random-convolution/logistic baseline.

Command:

```bash
.venv/bin/python -m experiments.run_deep_backbone_check \
  --datasets ECG200 GunPoint Coffee BME FaceFour ItalyPowerDemand MoteStrain Beef \
  --seeds 0 1 \
  --epochs 20 \
  --batch-size 16 \
  --out-dir results/deep_fcn8_2seed_alpha005
```

Run summary:

- Status: completed.
- Backbone: FCNClassifier.
- Datasets: 8.
- Seeds: `0 1`.
- Alpha: `0.05`.
- Rows: 576.
- Runtime: 45.774 seconds.

Key result for `fast_cp_mixed` versus augmented split CP:

| Corruption | FAST coverage | Aug coverage | Coverage delta | Set-size reduction |
|---|---:|---:|---:|---:|
| Drift | 0.9519 | 0.9544 | -0.0026 | 0.0139 |
| Gap | 0.9426 | 0.9431 | -0.0005 | 0.0139 |
| Noise | 0.9679 | 0.9691 | -0.0012 | 0.0138 |
| Overall | 0.9541 | 0.9556 | -0.0014 | 0.0139 |

Result files:

- `results/deep_fcn8_2seed_alpha005/deep_backbone_results.csv`
- `results/deep_fcn8_2seed_alpha005/summary.csv`
- `results/deep_fcn8_2seed_alpha005/fastcp_vs_aug.csv`
- `results/deep_fcn8_2seed_alpha005/fcn_vs_aug_stats.csv`
- `results/deep_fcn8_2seed_alpha005/FCN_BACKBONE_REPORT.md`
- `results/deep_fcn8_2seed_alpha005/run_summary.json`

## 2026-05-28

### MiniROCKET stronger-backbone supplement - completed

Purpose:

- Address the concern that the FAST-CP result may depend on the compact random-convolution/logistic-regression classifier.
- Test whether the coverage-efficiency tradeoff persists when the base TSC model is replaced by a stronger MiniROCKET-style feature extractor.

Code update:

- Added `--backbone {randomconv,minirocket}` to `experiments/run_fastcp_pilot.py`.
- Added `--minirocket-kernels`.
- MiniROCKET branch uses `aeon` MiniROCKET features with a calibrated ridge classifier.
- Gap-corrupted NaNs are filled before MiniROCKET transformation, matching the existing random-convolution preprocessing behavior.

Command:

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets BME Beef BeetleFly BirdChicken Chinatown Coffee ECG200 ECGFiveDays FaceFour GunPoint Herring ItalyPowerDemand Lightning7 Meat MoteStrain \
  --seeds 0 1 2 \
  --corruptions gap noise drift \
  --alphas 0.05 0.10 \
  --backbone minirocket \
  --minirocket-kernels 2048 \
  --fastcp-global-mixes 0.35 1.0 \
  --continue-on-error \
  --out-dir results/minirocket15_3seed_alpha005_01
```

Run summary:

- Datasets: 15.
- Seeds: 3.
- Alpha values: `0.05`, `0.10`.
- Rows: 8100.
- Runtime: 21.972 seconds.
- Error log: none.

Key result for `lambda=0.35` versus `lambda=1.0`:

| Alpha | Set-size reduction | 95% CI | Coverage delta | 95% CI |
|---:|---:|---|---:|---|
| 0.05 | 0.0943 | [0.0770, 0.1121] | -0.0055 | [-0.0083, -0.0027] |
| 0.10 | 0.0694 | [0.0559, 0.0833] | -0.0067 | [-0.0104, -0.0031] |

Interpretation:

- The qualitative FAST-CP coverage-efficiency tradeoff persists under MiniROCKET.
- This addresses the compact-backbone objection partially.
- It still does not prove transfer to deep TSC backbones such as InceptionTime, ResNet, or transformers.

Result files:

- `results/minirocket15_3seed_alpha005_01/fastcp_results.csv`
- `results/minirocket15_3seed_alpha005_01/run_summary.json`
- `results/minirocket15_3seed_alpha005_01_summary.csv`
- `results/minirocket15_3seed_alpha005_01_fastcp035_vs_aug.csv`
- `results/minirocket15_3seed_alpha005_01_stats_035_vs_1.csv`
- `results/minirocket15_3seed_alpha005_01_stats_035_vs_1.md`
- `results/minirocket15_3seed_alpha005_01/MINIROCKET_BACKBONE_REPORT.md`

### Independent lambda validation and alpha/lambda Pareto - completed

Purpose:

- Address the reviewer concern that `lambda = 0.35` was selected from a small ablation and then treated too strongly.
- Add broader coverage levels with `alpha ∈ {0.05, 0.10, 0.20}`.
- Produce a held-out Pareto frontier over the local-global threshold mix.

Protocol:

- Created a fixed non-overlapping protocol with 10 tuning datasets and 25 held-out evaluation datasets.
- Lambda grid: `0.0, 0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 1.0`.
- Selection rule: a lambda is feasible only if tuning-set mean coverage is at least `1-alpha-0.01` for every alpha; among feasible lambdas, select the smallest average set size.

Commands:

```bash
.venv/bin/python -m experiments.create_lambda_protocol

.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets ArrowHead CBF CricketX Earthquakes FaceAll Fish GunPointAgeSpan Ham MedicalImages MiddlePhalanxTW \
  --seeds 0 1 2 \
  --corruptions gap noise drift \
  --alphas 0.05 0.1 0.2 \
  --n-kernels 64 \
  --fastcp-global-mixes 0.0 0.1 0.2 0.35 0.5 0.65 0.8 1.0 \
  --continue-on-error \
  --out-dir results/lambda_tuning_10ds_3seed_alpha005_01_02

.venv/bin/python -m experiments.select_lambda \
  --input results/lambda_tuning_10ds_3seed_alpha005_01_02/fastcp_results.csv \
  --protocol results/lambda_protocol/lambda_protocol.json \
  --out-csv results/lambda_protocol/lambda_selection_summary.csv \
  --out-json results/lambda_protocol/lambda_selection.json \
  --out-md results/lambda_protocol/LAMBDA_SELECTION.md

.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets BME Beef BeetleFly BirdChicken Chinatown Coffee CricketY CricketZ DistalPhalanxOutlineAgeGroup DistalPhalanxOutlineCorrect DistalPhalanxTW ECG200 ECGFiveDays FaceFour FacesUCR GunPoint GunPointMaleVersusFemale GunPointOldVersusYoung Herring ItalyPowerDemand Lightning7 Meat MiddlePhalanxOutlineAgeGroup MiddlePhalanxOutlineCorrect MoteStrain \
  --seeds 0 1 2 \
  --corruptions gap noise drift \
  --alphas 0.05 0.1 0.2 \
  --n-kernels 64 \
  --fastcp-global-mixes 0.0 0.1 0.2 0.35 0.5 0.65 0.8 1.0 \
  --continue-on-error \
  --out-dir results/lambda_eval_25ds_3seed_alpha005_01_02
```

Run summaries:

- Tuning run: 10 datasets, 3 seeds, 3 alphas, 12960 rows, 838.515 seconds, no error log.
- Held-out run: 25 datasets, 3 seeds, 3 alphas, 32400 rows, 1190.633 seconds, no error log.

Key results:

- No lambda satisfied the tuning feasibility rule.
- Fallback selected `lambda = 1.0`, equivalent to augmented split conformal prediction.
- Held-out `lambda = 0.35` versus `lambda = 1.0`:
  - `alpha = 0.05`: set-size reduction `0.1125` labels, 95% CI `[0.0997, 0.1269]`; coverage delta `-0.0083`, 95% CI `[-0.0109, -0.0058]`.
  - `alpha = 0.10`: set-size reduction `0.0392` labels, 95% CI `[0.0296, 0.0499]`; coverage delta `-0.0052`, 95% CI `[-0.0083, -0.0026]`.
  - `alpha = 0.20`: set-size reduction `0.0109` labels, 95% CI `[0.0046, 0.0179]`; coverage delta `-0.0009`, 95% CI `[-0.0032, 0.0012]`.

Interpretation:

- `lambda = 0.35` is not independently validated as a default.
- It remains a useful Pareto point at stricter coverage levels, especially `alpha = 0.05`.
- If coverage preservation is prioritized by the independent rule, the selected setting is the global augmented threshold (`lambda = 1.0`).

Result files:

- `results/lambda_protocol/LAMBDA_PROTOCOL.md`
- `results/lambda_protocol/LAMBDA_SELECTION.md`
- `results/lambda_protocol/LAMBDA_EVAL_REPORT.md`
- `results/lambda_tuning_10ds_3seed_alpha005_01_02/fastcp_results.csv`
- `results/lambda_tuning_10ds_3seed_alpha005_01_02_summary.csv`
- `results/lambda_tuning_10ds_3seed_alpha005_01_02_pareto.csv`
- `results/lambda_eval_25ds_3seed_alpha005_01_02/fastcp_results.csv`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_summary.csv`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_pareto.csv`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_stats_035_vs_1.csv`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_stats_0_vs_1.csv`
- `paper/figures/fig6_lambda_pareto.pdf`

### Research Planning

- Created the research direction and experiment plan for **FAST-CP: Fast Perturbation-Fingerprint Weighted Conformal Prediction for Robust Time-Series Classification**.
- Selected the topic because it fits the Apple M4 16 GB, 1-2 day full-experiment constraint better than large-model or heavy vision experiments.
- Avoided using `conformal + early-exit + HAR` as the main novelty because close prior work already exists.

Files:

- `idea-stage/IDEA_REPORT.md`
- `refine-logs/FINAL_PROPOSAL.md`
- `refine-logs/EXPERIMENT_PLAN.md`

### Environment Setup

- Created a local Python virtual environment at `.venv`.
- Installed lightweight dependencies listed in `requirements.txt`.
- Verified that the UCR aeon-toolkit dataset URL works by downloading `ECG200.zip`.
- Noted that the system Anaconda Python has a NumPy / scipy / scikit-learn ABI mismatch, so experiments should use `.venv/bin/python`.

Files:

- `.venv/`
- `requirements.txt`
- `data/raw/ECG200.zip`
- `data/raw/ECG200/`

### Experiment Code Implemented

- Implemented UCR dataset downloading/loading.
- Implemented four corruption families: gap, noise, drift, and warp.
- Implemented lightweight random convolution features.
- Implemented conformal baselines:
  - `clean_split_cp`
  - `aug_split_cp`
  - `label_smooth_aug_cp`
  - `confidence_weighted_cp`
  - `fast_cp`
- Implemented result aggregation and plotting scripts.

Files:

- `experiments/data.py`
- `experiments/corruptions.py`
- `experiments/features.py`
- `experiments/conformal.py`
- `experiments/run_fastcp_pilot.py`
- `experiments/aggregate_results.py`
- `experiments/plot_results.py`
- `README.md`

### Experiments Run

#### Smoke attempt 1 - failed

Command:

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets ECG200 GunPoint \
  --seeds 0 \
  --corruptions gap noise \
  --n-kernels 96 \
  --out-dir results/smoke
```

Result:

- Failed before training completed.
- Cause: `scikit-learn 1.8.0` removed/does not accept the legacy `LogisticRegression(multi_class="auto")` argument.
- Fix applied: removed the `multi_class` argument from `experiments/run_fastcp_pilot.py`.

Planned smoke command:

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets ECG200 GunPoint \
  --seeds 0 \
  --corruptions gap noise \
  --n-kernels 96 \
  --out-dir results/smoke
```

Planned smoke result files:

- `results/smoke/fastcp_results.csv`
- `results/smoke/run_summary.json`
- `results/smoke_summary.csv`

#### Smoke attempt 2 - completed

Command:

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets ECG200 GunPoint \
  --seeds 0 \
  --corruptions gap noise \
  --n-kernels 96 \
  --out-dir results/smoke
```

Run summary:

- Status: completed.
- Datasets: `ECG200`, `GunPoint`.
- Seeds: `0`.
- Corruptions: `gap`, `noise`.
- Alpha values: `0.10`, `0.05`.
- Result rows: `120`.
- Runtime: `11.595` seconds.

Result files:

- `results/smoke/fastcp_results.csv`
- `results/smoke/run_summary.json`
- `results/smoke_summary.csv`
- `figures/smoke/coverage_vs_size_alpha_0.05.png`
- `figures/smoke/coverage_vs_size_alpha_0.10.png`

Aggregate result snapshot:

| Alpha | Corruption | Best coverage/size tradeoff observed |
|---:|---|---|
| 0.05 | gap | `fast_cp` reached coverage `0.9733` with average set size `1.3861`; `aug_split_cp` reached `0.9789` with size `1.4339`. |
| 0.05 | noise | `fast_cp` reached coverage `0.9550` with size `1.4156`; `aug_split_cp` reached `0.9533` with size `1.4300`. |
| 0.10 | gap | `fast_cp` reached coverage `0.9489` with size `1.2178`; `aug_split_cp` reached `0.9483` with size `1.2222`. |
| 0.10 | noise | `fast_cp` reached coverage `0.9106` with size `1.2278`; `aug_split_cp` reached `0.9144` with size `1.2439`. |

Interpretation:

- Smoke test confirms the code path works end to end.
- On this tiny 2-dataset run, `fast_cp` usually gives slightly smaller prediction sets than augmented split CP while maintaining similar coverage.
- This is not enough evidence for a paper claim yet; the next step is a 5-10 dataset pilot with drift included.

#### Pilot-5 run - completed

Command:

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets ECG200 GunPoint ItalyPowerDemand TwoLeadECG Coffee \
  --seeds 0 \
  --corruptions gap noise drift \
  --n-kernels 128 \
  --out-dir results/pilot5
```

Run summary:

- Status: completed.
- Datasets: `ECG200`, `GunPoint`, `ItalyPowerDemand`, `TwoLeadECG`, `Coffee`.
- Seeds: `0`.
- Corruptions: `gap`, `noise`, `drift`.
- Alpha values: `0.10`, `0.05`.
- Result rows: `450`.
- Runtime: `85.159` seconds.

Result files:

- `results/pilot5/fastcp_results.csv`
- `results/pilot5/run_summary.json`
- `results/pilot5_summary.csv`
- `figures/pilot5/coverage_vs_size_alpha_0.05.png`
- `figures/pilot5/coverage_vs_size_alpha_0.10.png`

Aggregate result snapshot:

| Alpha | Corruption | FAST-CP | Strong baseline comparison |
|---:|---|---|---|
| 0.05 | drift | coverage `0.9446`, size `1.1319` | `aug_split_cp`: coverage `0.9707`, size `1.2699` |
| 0.05 | gap | coverage `0.9407`, size `1.1416` | `aug_split_cp`: coverage `0.9585`, size `1.2572` |
| 0.05 | noise | coverage `0.9437`, size `1.1751` | `aug_split_cp`: coverage `0.9615`, size `1.2530` |
| 0.10 | drift | coverage `0.8793`, size `1.0003` | `aug_split_cp`: coverage `0.8892`, size `1.0046` |
| 0.10 | gap | coverage `0.8730`, size `1.0043` | `aug_split_cp`: coverage `0.8795`, size `1.0004` |
| 0.10 | noise | coverage `0.8778`, size `1.0474` | `confidence_weighted_cp`: coverage `0.8961`, size `1.0850` |

Interpretation:

- FAST-CP produces smaller prediction sets than augmented split CP in most alpha `0.05` settings.
- Coverage is slightly under target in several conditions, especially at alpha `0.10`.
- The method has an efficiency signal, but the next implementation update should add a conservative local threshold option, such as quantile inflation or mixing local and global thresholds.
- The pilot is promising enough to continue, but not yet paper-ready.

#### Pilot-5 mixed-threshold run - completed

Code update:

- Added `fast_cp_mixed`, which blends the local FAST-CP weighted threshold with the global augmented conformal threshold.
- Default blend used in this run: `--fastcp-global-mix 0.35`.
- Files changed:
  - `experiments/conformal.py`
  - `experiments/run_fastcp_pilot.py`
  - `README.md`

Command:

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets ECG200 GunPoint ItalyPowerDemand TwoLeadECG Coffee \
  --seeds 0 \
  --corruptions gap noise drift \
  --n-kernels 128 \
  --fastcp-global-mix 0.35 \
  --out-dir results/pilot5_mixed
```

Run summary:

- Status: completed.
- Result rows: `540`.
- Runtime: `80.387` seconds.

Result files:

- `results/pilot5_mixed/fastcp_results.csv`
- `results/pilot5_mixed/run_summary.json`
- `results/pilot5_mixed_summary.csv`
- `figures/pilot5_mixed/coverage_vs_size_alpha_0.05.png`
- `figures/pilot5_mixed/coverage_vs_size_alpha_0.10.png`

Aggregate result snapshot:

| Alpha | Corruption | `fast_cp_mixed` | Baseline comparison |
|---:|---|---|---|
| 0.05 | drift | coverage `0.9682`, size `1.1545` | `aug_split_cp`: coverage `0.9707`, size `1.2699` |
| 0.05 | gap | coverage `0.9620`, size `1.1516` | `aug_split_cp`: coverage `0.9585`, size `1.2572` |
| 0.05 | noise | coverage `0.9605`, size `1.1865` | `aug_split_cp`: coverage `0.9615`, size `1.2530` |
| 0.10 | drift | coverage `0.8864`, size `1.0006` | `aug_split_cp`: coverage `0.8892`, size `1.0046` |
| 0.10 | gap | coverage `0.8779`, size `1.0003` | `aug_split_cp`: coverage `0.8795`, size `1.0004` |
| 0.10 | noise | coverage `0.8711`, size `1.0344` | `fast_cp`: coverage `0.8778`, size `1.0474` |

Interpretation:

- `fast_cp_mixed` is a stronger candidate than pure `fast_cp` at alpha `0.05`: it keeps coverage close to or above augmented split CP while reducing average prediction set size.
- At alpha `0.10`, all methods are near singleton-set behavior, so the result is less informative and more sensitive to classifier accuracy.
- The next useful experiment is a larger alpha `0.05` run on 10-20 datasets with `fast_cp_mixed` as the primary method and an ablation over global-mix values.

#### Main10 alpha-0.05 attempt with Wafer - stopped

Command:

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets ECG200 GunPoint ItalyPowerDemand TwoLeadECG Coffee Beef Plane Wafer SonyAIBORobotSurface1 SonyAIBORobotSurface2 \
  --seeds 0 \
  --corruptions gap noise drift \
  --alphas 0.05 \
  --n-kernels 128 \
  --fastcp-global-mix 0.35 \
  --continue-on-error \
  --out-dir results/main10_alpha005
```

Result:

- Manually stopped after roughly 4 minutes 43 seconds.
- Progress reached 7/10 datasets, then became too slow on a larger dataset.
- No final result CSV was written.
- Engineering lesson: avoid very large UCR datasets until feature extraction is cached/vectorized, or use a curated small-to-medium benchmark list.

#### Main10 curated alpha-0.05 run - completed

Command:

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets ECG200 GunPoint ItalyPowerDemand TwoLeadECG Coffee Beef Plane FaceFour Lightning2 Lightning7 \
  --seeds 0 \
  --corruptions gap noise drift \
  --alphas 0.05 \
  --n-kernels 96 \
  --fastcp-global-mix 0.35 \
  --continue-on-error \
  --out-dir results/main10_small_alpha005
```

Run summary:

- Status: completed.
- Datasets: `ECG200`, `GunPoint`, `ItalyPowerDemand`, `TwoLeadECG`, `Coffee`, `Beef`, `Plane`, `FaceFour`, `Lightning2`, `Lightning7`.
- Seed: `0`.
- Corruptions: `gap`, `noise`, `drift`.
- Alpha: `0.05`.
- Result rows: `540`.
- Runtime: `116.603` seconds.
- Errors: none.

Result files:

- `results/main10_small_alpha005/fastcp_results.csv`
- `results/main10_small_alpha005/run_summary.json`
- `results/main10_small_alpha005_summary.csv`
- `results/main10_small_alpha005_fastcp_vs_aug.csv`
- `figures/main10_small_alpha005/coverage_vs_size_alpha_0.05.png`

Aggregate comparison against `aug_split_cp`:

| Corruption | Coverage delta | Set-size reduction | Set-size reduction pct | Abs coverage-gap delta |
|---|---:|---:|---:|---:|
| drift | -0.0066 | 0.0961 | 5.02% | -0.0060 |
| gap | -0.0052 | 0.0680 | 3.84% | -0.0008 |
| noise | -0.0074 | 0.0799 | 3.96% | -0.0041 |

Interpretation:

- `fast_cp_mixed` has a consistent efficiency signal: smaller sets under all three corruptions.
- Coverage is slightly lower than augmented split CP but remains close to target, and mean absolute coverage gap is slightly better.
- Result-to-claim verdict: `partial`, not yet enough for a full paper claim.

#### Auto-review round 1 - completed locally

- Review mode: local strict review, because no `claude-review` MCP was exposed.
- Score: `5.8 / 10`.
- Verdict: promising but not submission-ready.
- Required next experiments:
  - 3-seed main10 at alpha `0.05`.
  - `global_mix` ablation on 5 datasets.
  - dataset-level win/loss table.

Review files:

- `findings.md`
- `review-stage/AUTO_REVIEW.md`
- `review-stage/REVIEW_STATE.json`

#### Mix ablation-5 alpha-0.05 run - completed

Command:

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets ECG200 GunPoint ItalyPowerDemand TwoLeadECG Coffee \
  --seeds 0 \
  --corruptions gap noise drift \
  --alphas 0.05 \
  --n-kernels 96 \
  --fastcp-global-mixes 0.0 0.2 0.35 0.5 0.8 1.0 \
  --out-dir results/mix_ablation5_alpha005
```

Run summary:

- Status: completed.
- Runtime: `60.487` seconds.
- Result rows: `495`.
- Result files:
  - `results/mix_ablation5_alpha005/fastcp_results.csv`
  - `results/mix_ablation5_alpha005/run_summary.json`
  - `results/mix_ablation5_alpha005_summary.csv`

Interpretation:

- Pure local weighting (`mix=0.0`) gives the smallest sets but weaker coverage.
- `mix=0.2` and `mix=0.35` are the best practical local-global tradeoff.
- `mix=1.0` matches augmented split CP and confirms the interpolation behavior.

#### Main10 3-seed alpha-0.05 run - completed

Command:

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets ECG200 GunPoint ItalyPowerDemand TwoLeadECG Coffee Beef Plane FaceFour Lightning2 Lightning7 \
  --seeds 0 1 2 \
  --corruptions gap noise drift \
  --alphas 0.05 \
  --n-kernels 96 \
  --fastcp-global-mix 0.35 \
  --continue-on-error \
  --out-dir results/main10_3seed_alpha005
```

Run summary:

- Status: completed.
- Runtime: `325.770` seconds.
- Result rows: `1620`.
- Errors: none.

Result files:

- `results/main10_3seed_alpha005/fastcp_results.csv`
- `results/main10_3seed_alpha005/run_summary.json`
- `results/main10_3seed_alpha005_summary.csv`
- `results/main10_3seed_alpha005_fastcp_vs_aug.csv`
- `results/main10_3seed_alpha005_win_loss.csv`
- `figures/main10_3seed_alpha005/coverage_vs_size_alpha_0.05.png`

Aggregate comparison against `aug_split_cp`:

| Corruption | Coverage delta | Set-size reduction | Set-size reduction pct | Abs coverage-gap delta |
|---|---:|---:|---:|---:|
| drift | -0.0051 | 0.0848 | 4.17% | -0.0022 |
| gap | -0.0021 | 0.0626 | 3.25% | -0.0019 |
| noise | -0.0016 | 0.0652 | 2.91% | -0.0039 |

Dataset-level win/loss:

- Overall set-size win rate: `63.33%`.
- Coverage-close rate within 1 percentage point: `69.26%`.
- Absolute coverage-gap win rate: `87.78%`.

#### Auto-review round 2 - completed locally

- Review mode: local strict review.
- Score: `6.4 / 10`.
- Verdict: almost ready for paper planning under a narrowed claim.
- Status: auto-review stage completed.
- Remaining before paper draft:
  - runtime summary table;
  - optional smoothing-proxy baseline;
  - paper outline and figures.

#### Paper planning and figure generation - completed

Actions:

- Added runtime summary generation.
- Generated publication-style result figures.
- Created paper outline with claims-evidence matrix, section plan, figure plan, and citation scaffold.

Files:

- `results/runtime_summary.csv`
- `results/runtime_summary.tex`
- `figures/paper/fig2_main_results.pdf`
- `figures/paper/fig2_main_results.png`
- `figures/paper/fig3_mix_ablation.pdf`
- `figures/paper/fig3_mix_ablation.png`
- `figures/paper/fig4_win_loss.pdf`
- `figures/paper/fig4_win_loss.png`
- `figures/paper/fig5_runtime.pdf`
- `figures/paper/fig5_runtime.png`
- `figures/paper/latex_includes.tex`
- `PAPER_PLAN.md`

Interpretation:

- The project is now ready for paper drafting under the narrowed claim.
- Remaining TODO before a complete manuscript: create manual Fig. 1, verify BibTeX, and optionally add a smoothing-proxy baseline.

#### LaTeX manuscript draft - completed

Actions:

- Created a LaTeX manuscript scaffold under `paper/`.
- Generated the manual-style method diagram for Fig. 1.
- Added verified bibliography entries for cited prior work.
- Compiled the manuscript with `latexmk`.
- Checked the resulting PDF for undefined-reference markers and `[VERIFY]` markers.

Files:

- `paper/main.tex`
- `paper/main.pdf`
- `paper/references.bib`
- `paper/math_commands.tex`
- `paper/sections/0_abstract.tex`
- `paper/sections/1_introduction.tex`
- `paper/sections/2_related_work.tex`
- `paper/sections/3_method.tex`
- `paper/sections/4_experiments.tex`
- `paper/sections/5_analysis.tex`
- `paper/sections/6_limitations_conclusion.tex`
- `paper/sections/A_appendix.tex`
- `paper/figures/fig1_method.pdf`

Compile summary:

- Status: success.
- Output: `paper/main.pdf`.
- Pages: `8`.
- PDF size: `210077` bytes.
- No `??`, `[?]`, or `[VERIFY]` markers found in extracted PDF text.

Remaining TODO:

- Polish prose and related work.
- Add venue-specific formatting if a target journal template is chosen.

#### Smoothing-proxy baseline - completed

Command:

```bash
.venv/bin/python -m experiments.run_smoothing_proxy \
  --datasets ECG200 GunPoint Coffee \
  --seed 0 \
  --corruptions gap noise drift \
  --alpha 0.05 \
  --n-kernels 96 \
  --repeats 8 \
  --out-dir results/smoothing_proxy3_alpha005
```

Run summary:

- Status: completed.
- Runtime: `140.024` seconds.
- Result rows: `81`.
- Smoothing repeats: `8`.

Result files:

- `results/smoothing_proxy3_alpha005/smoothing_proxy_results.csv`
- `results/smoothing_proxy3_alpha005/run_summary.json`
- `results/smoothing_proxy3_alpha005_summary.csv`
- `results/smoothing_proxy3_alpha005_method_summary.csv`

Method-level summary:

| Method | Coverage | Abs. gap | Avg. set size | Extra smoothing sec |
|---|---:|---:|---:|---:|
| `aug_split_cp` | 0.9718 | 0.0331 | 1.4076 | 0.0000 |
| `fast_cp_mixed` | 0.9717 | 0.0329 | 1.2853 | 0.0000 |
| `smoothing_proxy_cp` | 0.9732 | 0.0347 | 1.4495 | 11.8090 |

Interpretation:

- The smoothing proxy gives similar coverage but larger sets than FAST-CP-mixed on this small subset.
- Repeated noisy inference adds measurable overhead, supporting the practical motivation for FAST-CP.

#### Final manuscript recompile after smoothing supplement - completed

Date: `2026-05-28`

Actions:

- Added the smoothing-proxy comparison to the manuscript analysis section.
- Updated the limitations section to make clear that the smoothing result is a small proxy rather than a full randomized-smoothing conformal baseline.
- Recompiled the paper with `latexmk`.
- Checked the PDF text and LaTeX log for unresolved references or verification placeholders.
- Checked that no experiment or LaTeX processes were left running.

Files:

- `paper/sections/5_analysis.tex`
- `paper/sections/6_limitations_conclusion.tex`
- `paper/main.pdf`

Compile/check summary:

- Status: success.
- Output: `paper/main.pdf`.
- Pages: `8`.
- PDF size: `210801` bytes.
- No `??`, `[?]`, or `[VERIFY]` markers found in extracted PDF text.
- No undefined citation/reference messages found in `paper/main.log`.
- No residual experiment or compile processes found.

#### Paper improvement loop - completed locally

Date: `2026-05-28`

Review mode:

- Local self-review loop, used instead of external Claude/MCP review per user instruction.
- Rounds: `2`.
- Score progression: `6.4 / 10` before fixes to `7.0 / 10` after fixes.

Actions:

- Added an explicit guarantee-boundary paragraph distinguishing standard split-CP exchangeability coverage from FAST-CP's empirical post-hoc adaptation under corruptions.
- Added a main numerical comparison table against augmented split conformal prediction.
- Clarified fixed `lambda=0.35` selection and baseline definitions.
- Added a reproducibility-artifacts paragraph.
- Regenerated all paper figures with non-Type-3 embedded fonts.
- Recompiled and verified the manuscript.

Files:

- `paper/PAPER_IMPROVEMENT_LOG.md`
- `paper/PAPER_IMPROVEMENT_STATE.json`
- `paper/sections/3_method.tex`
- `paper/sections/4_experiments.tex`
- `paper/sections/5_analysis.tex`
- `paper/sections/A_appendix.tex`
- `experiments/generate_paper_figures.py`
- `experiments/generate_method_diagram.py`
- `paper/main.pdf`

Final compile/check summary:

- Status: success.
- Output: `paper/main.pdf`.
- Pages: `9`.
- PDF size: `212451` bytes.
- No `??`, `[?]`, `[VERIFY]`, `TODO`, or stale-update markers found in extracted PDF text.
- No undefined citation/reference warnings found in `paper/main.log`.
- No overfull or underfull box warnings found in `paper/main.log`.
- `pdffonts` reports embedded Type 1 fonts only.
- No residual experiment or compile processes found.

#### Interpretation-depth revision - completed

Date: `2026-05-28`

Motivation:

- Addressed follow-up concerns that the conclusion identified what happened but did not sufficiently explain why, especially around confidence-only weighting, the meaning of the stability proposition, and the status of `lambda=0.35`.

Actions:

- Reframed confidence-only weighting as a strong conservative alternative rather than merely an ablation.
- Clarified that the full fingerprint is an efficiency-oriented choice and does not strictly dominate confidence-only weighting.
- Downgraded the local-threshold proposition to a conditional diagnostic statement, not theory support for coverage.
- Changed the `lambda=0.35` framing to an empirical benchmark setting with unverified out-of-benchmark generality.
- Added formal definitions for absolute coverage gap and absolute-gap delta.
- Specified weighted quantile implementation and tie behavior.
- Clarified that the local weighted calibration pool includes augmented calibration variants.
- Added related work on weighted conformal prediction under covariate shift and localized conformal prediction.
- Expanded limitations around alpha values, Pareto fronts, stronger TSC architectures, multivariate/real-world data, confidence-feature circularity, and heuristic bandwidth/mix choices.

Files:

- `paper/sections/2_related_work.tex`
- `paper/sections/3_method.tex`
- `paper/sections/4_experiments.tex`
- `paper/sections/6_limitations_conclusion.tex`
- `paper/sections/A_appendix.tex`
- `paper/references.bib`
- `paper/main.pdf`
- `HARD_REVIEW_RESPONSE.md`

Final check:

- Status: success.
- Output: `paper/main.pdf`.
- Pages: `11`.
- PDF size: `250393` bytes.
- No undefined citation/reference warnings found in `paper/main.log`.
- No `??`, `[?]`, `[VERIFY]`, or `TODO` markers found in extracted PDF text.
- No overfull boxes found in `paper/main.log`.
- `pdffonts` reports embedded Type 1 fonts only.
- No residual experiment or compile processes found.

#### Submission target shortlist - completed

Date: `2026-05-28`

Actions:

- Checked current journal metadata and scope pages for SCI Q2-style applied AI targets.
- Selected `Applied Intelligence` as the recommended primary target.
- Saved a target rationale, backup targets, and required pre-submission tasks.

Files:

- `SUBMISSION_TARGETS.md`

Notes:

- `Applied Intelligence` is the best current fit because the manuscript is an applied AI calibration/reliability paper with real-life corruption motivation and a reproducible commodity-hardware pipeline.
- Current quartile should still be verified through institutional JCR access before final submission.

#### Hard-review follow-up benchmark - completed

Date: `2026-05-28`

Motivation:

- Addressed hard reviewer concerns about small experimental scale, missing significance tests, weak baselines, unclear lambda selection, weak feature motivation, and lack of theory.

Actions:

- Added APS, RAPS, and corruption-family Mondrian conformal baselines.
- Added fingerprint ablations: no missingness, no spectral entropy, no drift, and no confidence/margin.
- Added paired statistical tests with Wilcoxon, paired t-test, bootstrap confidence intervals, and positive-rate reporting.
- Added systematic UCR dataset selection with inclusion/exclusion reasons.
- Ran a 35-valid-dataset, 5-seed benchmark at alpha `0.05`.
- Added a local weighted-threshold stability proposition and proof sketch.
- Updated the manuscript to use the expanded evidence and an honest coverage-efficiency tradeoff claim.

Selection:

- Initial selection file: `results/ucr_selection/ucr35_selected.csv`.
- Selection rule: total examples <= `2500`, series length <= `512`, class count <= `20`.
- `DiatomSizeReduction` failed during the expanded run because one split lacked a training class; it was replaced by `MoteStrain`.
- Final valid datasets: `35`.

Main expanded run:

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets <35 selected UCR datasets> \
  --seeds 0 1 2 3 4 \
  --corruptions gap noise drift \
  --alphas 0.05 \
  --n-kernels 64 \
  --fastcp-global-mix 0.35 \
  --fingerprint-ablations no_missing no_spectral no_drift no_confidence \
  --continue-on-error \
  --out-dir results/ucr35_5seed_alpha005_hardened
```

Replacement run:

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets MoteStrain \
  --seeds 0 1 2 3 4 \
  --corruptions gap noise drift \
  --alphas 0.05 \
  --n-kernels 64 \
  --fastcp-global-mix 0.35 \
  --fingerprint-ablations no_missing no_spectral no_drift no_confidence \
  --continue-on-error \
  --out-dir results/ucr35_5seed_alpha005_hardened_motestrain
```

Combined result:

- Output: `results/ucr35valid_5seed_alpha005_hardened/fastcp_results.csv`.
- Rows: `20475`.
- Runtime: `2731.609` seconds (`45.5` minutes).
- Dataset-seed runtime: `15.6` seconds.

Main result versus augmented split CP:

| Corruption | Coverage delta | Set-size reduction | Reduction | Abs-gap delta |
|---|---:|---:|---:|---:|
| drift | -0.0087 | 0.1105 | 4.45% | 0.0001 |
| gap | -0.0056 | 0.0910 | 3.87% | -0.0006 |
| noise | -0.0019 | 0.0794 | 3.04% | -0.0031 |

Statistical tests versus augmented split CP:

| Metric | Overall mean | 95% bootstrap CI | Wilcoxon p |
|---|---:|---:|---:|
| set-size reduction | 0.0936 | [0.0860, 0.1013] | 7.51e-130 |
| coverage delta | -0.0054 | [-0.0067, -0.0041] | 1.50e-29 |
| abs-gap delta | -0.0012 | [-0.0022, -0.0002] | 4.40e-15 |

Dataset-level win/loss:

- Set-size win rate: `71.24%`.
- Coverage within 1 percentage point: `73.40%`.
- Absolute coverage-gap win rate: `82.41%`.

Important interpretation change:

- The set-size reduction is statistically strong.
- The old "no coverage cost" framing is not supported.
- The revised claim is a significant prediction-set efficiency gain with a small measured coverage decrease.

Files:

- `HARD_REVIEW_RESPONSE.md`
- `theory-stage/LOCAL_THRESHOLD_STABILITY.md`
- `results/ucr35valid_5seed_alpha005_hardened/fastcp_results.csv`
- `results/ucr35valid_5seed_alpha005_hardened_summary.csv`
- `results/ucr35valid_5seed_alpha005_hardened_fastcp_vs_aug.csv`
- `results/ucr35valid_5seed_alpha005_hardened_stats_vs_aug.csv`
- `results/ucr35valid_5seed_alpha005_hardened_stats_vs_mondrian.csv`
- `results/ucr35valid_5seed_alpha005_hardened_stats_vs_aps.csv`
- `results/ucr35valid_5seed_alpha005_hardened_stats_vs_raps.csv`
- `results/ucr35valid_5seed_alpha005_hardened_win_loss.csv`
- `paper/main.pdf`

Final manuscript check:

- Status: success.
- Output: `paper/main.pdf`.
- Pages: `10`.
- PDF size: `242844` bytes.
- No undefined citation/reference warnings found in `paper/main.log`.
- No `??`, `[?]`, `[VERIFY]`, or `TODO` markers found in extracted PDF text.
- `pdffonts` reports embedded Type 1 fonts only.
- No residual experiment or compile processes found.
