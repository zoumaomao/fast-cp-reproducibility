# Reproducibility Statement

This project follows the replicable research requirement expected by Pattern Analysis and Applications.

## Code

All experiment code is in `experiments/`. The main entry points are:

- `experiments/run_fastcp_pilot.py`: UCR benchmark, baselines, fingerprint ablations, and lambda-grid runs.
- `experiments/reviewer_audit_tables.py`: main tables, tail-risk audit, severity table, fingerprint-control table, and paper figures.
- `experiments/run_external_uea_validation.py`: UEA multivariate validation.
- `experiments/run_deep_backbone_check.py`: FCN backbone check.
- `experiments/select_lambda.py`: coverage-prioritized lambda selection and global fallback protocol.

## Public Data

The study uses public benchmark datasets:

- UCR univariate time-series archive.
- UEA multivariate time-series archive.

The scripts use `aeon` loaders and local caches under `data/raw/` and `data/uea/` when available. No private data are used.

## Main Saved Outputs

The main reported results can be inspected without rerunning all experiments:

- `results/ucr35valid_5seed_alpha005_rerun_20260529/fastcp_results.csv`
- `results/ucr35valid_5seed_alpha005_rerun_20260529/audit/REVIEWER_AUDIT_REPORT.md`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_tradeoff_table.csv`
- `results/uea_external_3ds_3seed_alpha005/fastcp_vs_aug.csv`
- `results/deep_fcn8_2seed_alpha005/fcn_vs_aug_stats.csv`
- `results/runtime_summary.csv`

`EXPERIMENT_LOG.md` records commands, update dates, runtimes, result summaries, and output locations.

## Hardware

The full 35-dataset, five-seed UCR benchmark with control ablations completed in 47.7 minutes on an Apple M4 with 16 GB unified memory. No GPU is required for the main benchmark. The FCN backbone check uses TensorFlow and is reported as a supplementary robustness check.

## Submission Artifact Recommendation

For journal submission, provide a code repository or supplementary archive containing:

- `experiments/`
- `paper/`
- `README.md`
- `REPRODUCIBILITY.md`
- `MANIFEST.md`
- `EXPERIMENT_LOG.md`
- `requirements.txt`
- public data access instructions or cached public benchmark files if permitted
- saved CSV/JSON/Markdown outputs under `results/`

Remove local machine paths and temporary build metadata before upload.
