# Lambda Selection Protocol

Updated: `2026-05-28`

## Purpose

independent lambda selection and held-out alpha/Pareto evaluation

## Split

- Tuning datasets (10): `ArrowHead, CBF, CricketX, Earthquakes, FaceAll, Fish, GunPointAgeSpan, Ham, MedicalImages, MiddlePhalanxTW`
- Evaluation datasets (25): `BME, Beef, BeetleFly, BirdChicken, Chinatown, Coffee, CricketY, CricketZ, DistalPhalanxOutlineAgeGroup, DistalPhalanxOutlineCorrect, DistalPhalanxTW, ECG200, ECGFiveDays, FaceFour, FacesUCR, GunPoint, GunPointMaleVersusFemale, GunPointOldVersusYoung, Herring, ItalyPowerDemand, Lightning7, Meat, MiddlePhalanxOutlineAgeGroup, MiddlePhalanxOutlineCorrect, MoteStrain`

## Grid

- Lambda grid: `[0.0, 0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 1.0]`
- Alpha values: `[0.05, 0.1, 0.2]`

## Selection Rule

- A lambda is feasible if mean coverage is at least `1-alpha-0.01` for every alpha on tuning data.
- Among feasible lambdas, choose the one with the smallest average prediction-set size.
- If no lambda is feasible, minimize total coverage shortfall, then average prediction-set size.

## Caveat

This is an independent validation protocol relative to the held-out evaluation datasets, but it is still empirical and does not provide a guarantee that the selected lambda transfers to other archives or real-world shifts.
