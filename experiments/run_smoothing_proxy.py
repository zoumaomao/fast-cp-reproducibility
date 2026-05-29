from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from experiments.conformal import (
    conformal_threshold,
    inverse_probability_scores,
    metrics,
    prediction_sets_from_threshold,
    weighted_prediction_sets,
)
from experiments.corruptions import corrupt_batch
from experiments.data import load_ucr_dataset
from experiments.features import RandomConvFeatures, perturbation_fingerprint
from experiments.run_fastcp_pilot import CORRUPTION_LEVELS, build_augmented_calibration, stable_offset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a small smoothing-proxy conformal baseline.")
    parser.add_argument("--datasets", nargs="+", default=["ECG200", "GunPoint", "Coffee"])
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--corruptions", nargs="+", default=["gap", "noise", "drift"])
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--n-kernels", type=int, default=96)
    parser.add_argument("--repeats", type=int, default=8)
    parser.add_argument("--smoothing-sigma", type=float, default=0.05)
    parser.add_argument("--fastcp-global-mix", type=float, default=0.35)
    parser.add_argument("--out-dir", default="results/smoothing_proxy3_alpha005")
    parser.add_argument("--data-dir", default="data/raw")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    started = time.time()
    rows = []
    for dataset in tqdm(args.datasets, desc="datasets"):
        x_train, y_train, x_test, y_test = load_ucr_dataset(dataset, args.data_dir)
        rows.extend(run_dataset(dataset, x_train, y_train, x_test, y_test, args))
    df = pd.DataFrame(rows)
    result_path = out_dir / "smoothing_proxy_results.csv"
    df.to_csv(result_path, index=False)
    summary = {
        "datasets": args.datasets,
        "seed": args.seed,
        "corruptions": args.corruptions,
        "alpha": args.alpha,
        "repeats": args.repeats,
        "smoothing_sigma": args.smoothing_sigma,
        "elapsed_sec": round(time.time() - started, 3),
        "rows": int(len(df)),
        "result_path": str(result_path),
    }
    (out_dir / "run_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


def run_dataset(dataset: str, x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray, y_test: np.ndarray, args: argparse.Namespace) -> list[dict[str, object]]:
    stratify = y_train if min(np.bincount(y_train)) >= 2 else None
    x_fit, x_calib, y_fit, y_calib = train_test_split(
        x_train,
        y_train,
        test_size=0.35,
        random_state=args.seed,
        stratify=stratify,
    )
    featurizer = RandomConvFeatures(n_kernels=args.n_kernels, seed=args.seed).fit(x_fit)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=800, solver="lbfgs"))
    model.fit(featurizer.transform(x_fit), y_fit)

    aug_x, aug_y, _ = build_augmented_calibration(x_calib, y_calib, args.corruptions, args.seed)
    aug_probs = model.predict_proba(featurizer.transform(aug_x))
    aug_scores = inverse_probability_scores(aug_probs, aug_y)
    aug_threshold = conformal_threshold(aug_scores, args.alpha)
    aug_fp = perturbation_fingerprint(aug_x, aug_probs)

    smooth_started = time.time()
    aug_smooth_probs = average_smoothed_probs(aug_x, featurizer, model, args.repeats, args.smoothing_sigma, args.seed)
    smooth_calib_time = time.time() - smooth_started
    smooth_scores = inverse_probability_scores(aug_smooth_probs, aug_y)
    smooth_threshold = conformal_threshold(smooth_scores, args.alpha)

    rows: list[dict[str, object]] = []
    for corruption in args.corruptions:
        for severity in CORRUPTION_LEVELS[corruption]:
            rng = np.random.default_rng(args.seed + stable_offset(dataset, corruption, severity))
            x_eval = corrupt_batch(x_test, corruption, severity, rng)
            probs = model.predict_proba(featurizer.transform(x_eval))
            test_fp = perturbation_fingerprint(x_eval, probs)
            fast_sets = weighted_prediction_sets(
                aug_scores,
                aug_fp,
                probs,
                test_fp,
                args.alpha,
                global_threshold=aug_threshold,
                global_mix=args.fastcp_global_mix,
            )
            aug_sets = prediction_sets_from_threshold(probs, aug_threshold)

            smooth_eval_started = time.time()
            smooth_probs = average_smoothed_probs(
                x_eval,
                featurizer,
                model,
                args.repeats,
                args.smoothing_sigma,
                args.seed + stable_offset("smooth", dataset, corruption, severity),
            )
            smooth_eval_time = time.time() - smooth_eval_started
            smooth_sets = prediction_sets_from_threshold(smooth_probs, smooth_threshold)

            for method, pred_sets, method_probs, extra_time in [
                ("aug_split_cp", aug_sets, probs, 0.0),
                ("fast_cp_mixed", fast_sets, probs, 0.0),
                ("smoothing_proxy_cp", smooth_sets, smooth_probs, smooth_calib_time + smooth_eval_time),
            ]:
                row = {
                    "dataset": dataset,
                    "seed": args.seed,
                    "corruption": corruption,
                    "severity": severity,
                    "alpha": args.alpha,
                    "method": method,
                    "repeats": args.repeats if method == "smoothing_proxy_cp" else 1,
                    "extra_smoothing_sec": extra_time,
                    "n_test": int(x_test.shape[0]),
                    "n_classes": int(len(np.unique(y_train))),
                }
                row.update(metrics(pred_sets, y_test, method_probs))
                rows.append(row)
    return rows


def average_smoothed_probs(
    x: np.ndarray,
    featurizer: RandomConvFeatures,
    model,
    repeats: int,
    sigma: float,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    probs = None
    scale = np.nanstd(x, axis=1, keepdims=True)
    scale = np.where(scale < 1e-8, 1.0, scale)
    for _ in range(repeats):
        noisy = x + rng.normal(0.0, sigma, size=x.shape).astype(np.float32) * scale
        current = model.predict_proba(featurizer.transform(noisy))
        probs = current if probs is None else probs + current
    return probs / repeats


if __name__ == "__main__":
    main()
