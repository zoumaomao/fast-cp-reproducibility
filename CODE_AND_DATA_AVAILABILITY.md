# Code and Data Availability

This repository contains the source code, reproducibility instructions, and saved result files for the FAST-CP experiments.

## Code

All experiment code is provided under `experiments/`. The main entry points are:

- `experiments/run_fastcp_pilot.py` for the UCR benchmark, baselines, lambda-grid runs, and fingerprint-control ablations.
- `experiments/reviewer_audit_tables.py` for the main paper tables, tail-risk analysis, severity-level table, fingerprint-control table, and figures.
- `experiments/run_external_uea_validation.py` for UEA multivariate validation.
- `experiments/run_deep_backbone_check.py` for the FCN backbone check.
- `experiments/select_lambda.py` for coverage-prioritized lambda selection and global fallback analysis.

## Data

The study uses public benchmark datasets only:

- UCR Time Series Classification Archive.
- UEA Multivariate Time Series Classification Archive.

The scripts load these datasets through `aeon` dataset loaders and use local caches under `data/raw/` and `data/uea/` when available. The `data/` directory is intentionally not versioned because it contains public benchmark caches that can be downloaded again.

## Saved Results

The main CSV, JSON, Markdown, and figure outputs are provided under `results/`, `figures/`, and `paper/figures/`. Key result files include:

- `results/ucr35valid_5seed_alpha005_rerun_20260529/fastcp_results.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/full_method_table.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/tail_risk_table.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/severity_summary.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/fingerprint_variant_table.csv`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_tradeoff_table.csv`
- `results/uea_external_3ds_3seed_alpha005/fastcp_vs_aug.csv`
- `results/deep_fcn8_2seed_alpha005/fcn_vs_aug_stats.csv`
- `results/runtime_summary.csv`

## Reproduction

The environment setup, smoke test, full benchmark command, lambda-validation command, UEA validation command, FCN command, and paper-build command are documented in `README.md` and `REPRODUCIBILITY.md`.

`EXPERIMENT_LOG.md` records dated experiment updates, commands, runtimes, result summaries, and output locations.
