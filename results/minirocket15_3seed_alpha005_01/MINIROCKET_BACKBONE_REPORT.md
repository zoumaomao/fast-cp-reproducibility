# MiniROCKET Backbone Supplement

Updated: `2026-05-28`

## Purpose

This supplement addresses the methodological concern that the main FAST-CP result may depend on a compact random-convolution/logistic-regression classifier. We reran the conformal calibration pipeline with a stronger time-series backbone: MiniROCKET features followed by a calibrated ridge classifier.

## Setup

- Datasets: 15 fixed UCR datasets from the 35-dataset pool: `BME`, `Beef`, `BeetleFly`, `BirdChicken`, `Chinatown`, `Coffee`, `ECG200`, `ECGFiveDays`, `FaceFour`, `GunPoint`, `Herring`, `ItalyPowerDemand`, `Lightning7`, `Meat`, `MoteStrain`.
- Seeds: `0, 1, 2`.
- Corruptions: `gap`, `noise`, `drift`, each with three severities.
- Alpha values: `0.05`, `0.10`.
- Backbone: `aeon` MiniROCKET with `2048` kernels.
- Classifier: `StandardScaler(with_mean=False)` + `RidgeClassifierCV`, wrapped by `CalibratedClassifierCV(method="sigmoid")` to obtain probabilities.
- FAST-CP comparison: `lambda = 0.35` versus `lambda = 1.0`; `lambda = 1.0` is equivalent to augmented split conformal prediction.

Run summary:

- Runtime: `21.972` seconds on Apple M4 16 GB.
- Rows: `8100`.
- Error log: none.

## Main Result

`lambda = 0.35` versus `lambda = 1.0`:

| alpha | corruption | coverage delta | set-size reduction | reduction pct | abs-gap delta |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0.05 | drift | -0.0052 | 0.1195 | 4.38% | -0.0007 |
| 0.05 | gap | -0.0072 | 0.0921 | 3.56% | 0.0010 |
| 0.05 | noise | -0.0042 | 0.0713 | 2.32% | -0.0050 |
| 0.10 | drift | -0.0095 | 0.0914 | 3.92% | -0.0032 |
| 0.10 | gap | -0.0080 | 0.0734 | 3.13% | -0.0058 |
| 0.10 | noise | -0.0026 | 0.0435 | 1.29% | -0.0081 |

Overall paired statistics:

| alpha | set-size reduction | 95% CI | coverage delta | 95% CI | Wilcoxon p for set size |
| ---: | ---: | --- | ---: | --- | ---: |
| 0.05 | 0.0943 | [0.0770, 0.1121] | -0.0055 | [-0.0083, -0.0027] | 4.72e-38 |
| 0.10 | 0.0694 | [0.0559, 0.0833] | -0.0067 | [-0.0104, -0.0031] | 1.17e-19 |

## Interpretation

The stronger MiniROCKET backbone preserves the qualitative FAST-CP tradeoff. Intermediate local-global mixing still reduces prediction-set size by a statistically clear margin at both `alpha = 0.05` and `alpha = 0.10`, but it also lowers empirical coverage by roughly 0.55--0.67 percentage points overall.

This supplement strengthens the paper against the objection that the effect is only an artifact of the compact random-convolution/logistic model. It still does not prove transfer to deep TSC architectures such as InceptionTime, ResNet, or transformers; that remains a limitation.

## Output Files

- `results/minirocket15_3seed_alpha005_01/fastcp_results.csv`
- `results/minirocket15_3seed_alpha005_01/run_summary.json`
- `results/minirocket15_3seed_alpha005_01_summary.csv`
- `results/minirocket15_3seed_alpha005_01_fastcp035_vs_aug.csv`
- `results/minirocket15_3seed_alpha005_01_stats_035_vs_1.csv`
- `results/minirocket15_3seed_alpha005_01_stats_035_vs_1.md`
