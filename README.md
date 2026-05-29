# FAST-CP Reproducibility Package

This repository contains the code and saved artifacts for:

**FAST-CP: A Lightweight Perturbation-Aware Conformal Prediction Framework for Corrupted Time-Series Classification**

The project studies FAST-CP as a lightweight post-hoc uncertainty layer for corrupted time-series classification. It does not claim improved conformal validity under arbitrary distribution shift. The main claim is a practical coverage-efficiency tradeoff under limited compute, with a global augmented conformal fallback when empirical coverage is prioritized.

## Data Access

The experiments use public benchmark data:

- UCR univariate time-series archive, accessed through `aeon` dataset loaders or cached under `data/raw/`.
- UEA multivariate archive, accessed through `aeon` dataset loaders or cached under `data/uea/`.

No private data are required. If local cached files are absent, the scripts attempt to download the public datasets through the configured `aeon` loaders. For submission, provide either the cached public benchmark files if allowed by the submission system or clear network-enabled dataset download instructions with this repository.

## Environment

The main UCR and UEA experiments run with standard scientific Python packages. The optional FCN backbone check requires TensorFlow.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

The reported full UCR benchmark completed on an Apple M4 with 16 GB unified memory in 47.7 minutes.

## Quick Smoke Test

```bash
.venv/bin/python -m experiments.run_fastcp_pilot \
  --datasets ECG200 GunPoint \
  --seeds 0 \
  --corruptions gap noise \
  --alphas 0.05 \
  --n-kernels 64 \
  --fastcp-global-mix 0.35 \
  --out-dir results/smoke_reproduce
```

## Main UCR Benchmark

This command reproduces the expanded 35-dataset, five-seed UCR benchmark with fingerprint-control ablations.

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

Generate the audit tables and paper figures:

```bash
.venv/bin/python -m experiments.reviewer_audit_tables \
  --input results/ucr35valid_5seed_alpha005_rerun_20260529/fastcp_results.csv \
  --out-dir results/ucr35valid_5seed_alpha005_rerun_20260529/audit \
  --fig-dir figures/paper \
  --paper-fig-dir paper/figures
```

## Lambda Validation

The safe fallback and Pareto operating-point analysis uses a fixed tuning/evaluation protocol.

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
```

The held-out evaluation command and saved outputs are documented in `EXPERIMENT_LOG.md`.

## External and Backbone Checks

UEA multivariate validation:

```bash
.venv/bin/python -m experiments.run_external_uea_validation \
  --datasets BasicMotions Epilepsy NATOPS \
  --seeds 0 1 2 \
  --alphas 0.05 \
  --n-kernels 24 \
  --out-dir results/uea_external_3ds_3seed_alpha005
```

FCN backbone check:

```bash
.venv/bin/python -m experiments.run_deep_backbone_check \
  --datasets ECG200 GunPoint Coffee BME FaceFour ItalyPowerDemand MoteStrain Beef \
  --seeds 0 1 \
  --epochs 20 \
  --batch-size 16 \
  --out-dir results/deep_fcn8_2seed_alpha005
```

## Saved Results

The main paper tables and checks are backed by these files:

- `results/ucr35valid_5seed_alpha005_rerun_20260529/fastcp_results.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/REVIEWER_AUDIT_REPORT.md`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/full_method_table.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/tail_risk_table.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/severity_summary.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/fingerprint_variant_table.csv`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_tradeoff_table.csv`
- `results/uea_external_3ds_3seed_alpha005/fastcp_vs_aug.csv`
- `results/minirocket15_3seed_alpha005_01_fastcp035_vs_aug.csv`
- `results/deep_fcn8_2seed_alpha005/fcn_vs_aug_stats.csv`
- `results/runtime_summary.csv`

`MANIFEST.md` lists the major artifacts, and `EXPERIMENT_LOG.md` records dated commands, runtimes, results, and output locations.

## Build the Paper

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The compiled manuscript is written to `paper/main.pdf`.

## Code and Data Availability

See `CODE_AND_DATA_AVAILABILITY.md` for a concise statement of the released code, public data sources, saved result files, and reproduction entry points.

## Submission Package Checklist

For Pattern Analysis and Applications, prepare a code repository or supplementary archive containing:

- Source code in `experiments/`.
- Public data access instructions, or cached public UCR/UEA files if allowed by the submission system.
- Main result CSV files under `results/`.
- Generated paper figures under `paper/figures/`.
- This `README.md`, `MANIFEST.md`, and `EXPERIMENT_LOG.md`.

Before submission, remove local machine paths and temporary build metadata from the archive.
