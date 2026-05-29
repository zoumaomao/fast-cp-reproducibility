# Independent Lambda Validation and Alpha/Lambda Pareto Report

Updated: `2026-05-28`

## Protocol

- Tuning split: 10 fixed UCR datasets.
- Held-out evaluation split: 25 disjoint UCR datasets.
- Seeds: `0, 1, 2`.
- Corruptions: `gap`, `noise`, `drift`, each with three severities.
- Alpha grid: `0.05, 0.10, 0.20`.
- Lambda grid: `0.0, 0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 1.0`.
- Selection rule: choose the smallest-set lambda among lambdas whose mean coverage is at least `1-alpha-0.01` for every alpha on the tuning split; if none is feasible, minimize total coverage shortfall, then set size.

## Tuning Result

No lambda satisfied the coverage-feasibility rule on the tuning split. The fallback rule selected `lambda = 1.0`, i.e. the augmented split conformal threshold.

This means the independent protocol does **not** support `lambda = 0.35` as a validated default. The honest interpretation is that `lambda = 0.35` is a Pareto/tradeoff point used in the main benchmark, while coverage-prioritized selection retreats to the global augmented threshold.

Tuning outputs:

- `results/lambda_protocol/lambda_selection.json`
- `results/lambda_protocol/lambda_selection_summary.csv`
- `results/lambda_protocol/LAMBDA_SELECTION.md`
- `results/lambda_tuning_10ds_3seed_alpha005_01_02/fastcp_results.csv`
- `results/lambda_tuning_10ds_3seed_alpha005_01_02_summary.csv`
- `results/lambda_tuning_10ds_3seed_alpha005_01_02_pareto.csv`
- `results/lambda_tuning_10ds_3seed_alpha005_01_02_pareto.md`

## Held-out Evaluation Result

The held-out evaluation produced `32400` result rows over 25 datasets and completed in `1190.633` seconds on Apple M4 16 GB. No error log was produced.

Mean FAST-CP-mixed behavior over the held-out split:

| alpha | lambda | coverage | avg_set_size | abs_coverage_gap |
| ---: | ---: | ---: | ---: | ---: |
| 0.05 | 0.00 | 0.9445 | 2.0689 | 0.0467 |
| 0.05 | 0.35 | 0.9466 | 2.0907 | 0.0459 |
| 0.05 | 1.00 | 0.9549 | 2.2032 | 0.0470 |
| 0.10 | 0.00 | 0.8932 | 1.7147 | 0.0742 |
| 0.10 | 0.35 | 0.8923 | 1.7113 | 0.0773 |
| 0.10 | 1.00 | 0.8975 | 1.7505 | 0.0782 |
| 0.20 | 0.00 | 0.7928 | 1.3082 | 0.1030 |
| 0.20 | 0.35 | 0.7947 | 1.3043 | 0.1072 |
| 0.20 | 1.00 | 0.7956 | 1.3152 | 0.1079 |

Paired statistics for `lambda = 0.35` versus `lambda = 1.0`:

| alpha | set-size reduction | 95% CI | coverage delta | 95% CI |
| ---: | ---: | --- | ---: | --- |
| 0.05 | 0.1125 | [0.0997, 0.1269] | -0.0083 | [-0.0109, -0.0058] |
| 0.10 | 0.0392 | [0.0296, 0.0499] | -0.0052 | [-0.0083, -0.0026] |
| 0.20 | 0.0109 | [0.0046, 0.0179] | -0.0009 | [-0.0032, 0.0012] |

Interpretation:

- At `alpha = 0.05`, `lambda = 0.35` remains an efficient Pareto point: it significantly reduces set size but loses about 0.83 percentage points of coverage relative to `lambda = 1.0`.
- At `alpha = 0.10`, the efficiency gain shrinks and still carries a measurable coverage drop.
- At `alpha = 0.20`, the set-size gain is tiny and the coverage difference is not statistically clear.
- The Pareto frontier varies by alpha and corruption, so a single fixed lambda should not be described as generally validated.

Held-out outputs:

- `results/lambda_eval_25ds_3seed_alpha005_01_02/fastcp_results.csv`
- `results/lambda_eval_25ds_3seed_alpha005_01_02/run_summary.json`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_summary.csv`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_pareto.csv`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_pareto.md`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_stats_035_vs_1.csv`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_stats_035_vs_1.md`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_stats_0_vs_1.csv`
- `results/lambda_eval_25ds_3seed_alpha005_01_02_stats_0_vs_1.md`
- `figures/paper/fig6_lambda_pareto.pdf`
- `figures/paper/fig6_lambda_pareto.png`
- `paper/figures/fig6_lambda_pareto.pdf`
- `paper/figures/fig6_lambda_pareto.png`
