from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from aeon.classification.deep_learning import FCNClassifier, ResNetClassifier
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from experiments.conformal import (
    conformal_threshold,
    inverse_probability_scores,
    metrics,
    prediction_sets_from_threshold,
    weighted_prediction_sets,
)
from experiments.corruptions import corrupt_batch, fill_nans
from experiments.data import load_ucr_dataset
from experiments.features import perturbation_fingerprint


CORRUPTION_LEVELS = {
    "gap": [0.05, 0.10, 0.20],
    "noise": [0.05, 0.10, 0.20],
    "drift": [0.10, 0.20, 0.40],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Small deep TSC backbone check for FAST-CP.")
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=["ECG200", "GunPoint", "Coffee", "BME", "FaceFour", "ItalyPowerDemand", "MoteStrain", "Beef"],
    )
    parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1])
    parser.add_argument("--corruptions", nargs="+", default=["gap", "noise", "drift"])
    parser.add_argument("--alphas", nargs="+", type=float, default=[0.05])
    parser.add_argument("--backbone", choices=["fcn", "resnet"], default="fcn")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--calib-size", type=float, default=0.35)
    parser.add_argument("--fastcp-global-mix", type=float, default=0.35)
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--out-dir", default="results/deep_fcn8_2seed_alpha005")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    started = time.time()
    for dataset in tqdm(args.datasets, desc=f"{args.backbone} datasets"):
        x_train, y_train, x_test, y_test = load_ucr_dataset(dataset, args.data_dir)
        for seed in args.seeds:
            rows.extend(run_one_dataset(dataset, x_train, y_train, x_test, y_test, seed, args, out_dir))
    results = pd.DataFrame(rows)
    result_path = out_dir / "deep_backbone_results.csv"
    results.to_csv(result_path, index=False)
    summary = {
        "datasets": args.datasets,
        "seeds": args.seeds,
        "corruptions": args.corruptions,
        "alphas": args.alphas,
        "backbone": args.backbone,
        "epochs": args.epochs,
        "elapsed_sec": round(time.time() - started, 3),
        "rows": int(len(results)),
        "result_path": str(result_path),
    }
    (out_dir / "run_summary.json").write_text(json.dumps(summary, indent=2))
    write_summary_tables(results, out_dir)
    print(json.dumps(summary, indent=2))


def run_one_dataset(
    dataset: str,
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    seed: int,
    args: argparse.Namespace,
    out_dir: Path,
) -> list[dict[str, object]]:
    stratify = y_train if min(np.bincount(y_train)) >= 2 else None
    x_fit, x_calib, y_fit, y_calib = train_test_split(
        x_train,
        y_train,
        test_size=args.calib_size,
        random_state=seed,
        stratify=stratify,
    )
    model = make_model(args, seed, out_dir / "keras_tmp" / f"{dataset}_{seed}")
    model.fit(x_fit[:, None, :], y_fit)

    clean_probs = model.predict_proba(x_calib[:, None, :])
    clean_scores = inverse_probability_scores(clean_probs, y_calib)
    aug_x, aug_y = build_augmented_calibration(x_calib, y_calib, args.corruptions, seed)
    aug_probs = model.predict_proba(fill_nans(aug_x)[:, None, :])
    aug_scores = inverse_probability_scores(aug_probs, aug_y)
    aug_fp = perturbation_fingerprint(aug_x, aug_probs)
    aug_fp_conf = aug_fp[:, -2:]

    rows: list[dict[str, object]] = []
    for corruption in args.corruptions:
        for severity in CORRUPTION_LEVELS[corruption]:
            rng = np.random.default_rng(seed + stable_offset(dataset, corruption, severity))
            x_eval = corrupt_batch(x_test, corruption, severity, rng)
            probs = model.predict_proba(fill_nans(x_eval)[:, None, :])
            test_fp = perturbation_fingerprint(x_eval, probs)
            for alpha in args.alphas:
                aug_global = conformal_threshold(aug_scores, alpha)
                candidates = {
                    "clean_split_cp": prediction_sets_from_threshold(
                        probs, conformal_threshold(clean_scores, alpha)
                    ),
                    "aug_split_cp": prediction_sets_from_threshold(probs, aug_global),
                    "fast_cp_mixed_confidence_only": weighted_prediction_sets(
                        aug_scores,
                        aug_fp_conf,
                        probs,
                        test_fp[:, -2:],
                        alpha,
                        global_threshold=aug_global,
                        global_mix=args.fastcp_global_mix,
                    ),
                    "fast_cp_mixed": weighted_prediction_sets(
                        aug_scores,
                        aug_fp,
                        probs,
                        test_fp,
                        alpha,
                        global_threshold=aug_global,
                        global_mix=args.fastcp_global_mix,
                    ),
                }
                for method, pred_sets in candidates.items():
                    row = {
                        "dataset": dataset,
                        "seed": seed,
                        "corruption": corruption,
                        "severity": severity,
                        "alpha": alpha,
                        "method": method,
                        "backbone": args.backbone,
                        "epochs": args.epochs,
                        "n_train": int(x_fit.shape[0]),
                        "n_calib": int(x_calib.shape[0]),
                        "n_aug_calib": int(aug_x.shape[0]),
                        "n_test": int(x_test.shape[0]),
                        "n_classes": int(len(np.unique(y_train))),
                    }
                    row.update(metrics(pred_sets, y_test, probs))
                    rows.append(row)
    return rows


def make_model(args: argparse.Namespace, seed: int, file_path: Path):
    file_path.mkdir(parents=True, exist_ok=True)
    common = dict(
        n_epochs=args.epochs,
        batch_size=args.batch_size,
        random_state=seed,
        verbose=False,
        file_path=str(file_path),
        save_best_model=False,
        save_last_model=False,
        save_init_model=False,
    )
    if args.backbone == "fcn":
        return FCNClassifier(**common)
    return ResNetClassifier(**common)


def build_augmented_calibration(
    x_calib: np.ndarray,
    y_calib: np.ndarray,
    corruptions: list[str],
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    xs = [x_calib.astype(np.float32)]
    ys = [y_calib]
    for corruption in corruptions:
        for severity in CORRUPTION_LEVELS[corruption]:
            rng = np.random.default_rng(seed + stable_offset("deep_calib", corruption, severity))
            xs.append(corrupt_batch(x_calib, corruption, severity, rng))
            ys.append(y_calib)
    return np.vstack(xs), np.concatenate(ys)


def write_summary_tables(df: pd.DataFrame, out_dir: Path) -> None:
    df = df.copy()
    df["target_coverage"] = 1.0 - df["alpha"]
    df["abs_coverage_gap"] = (df["target_coverage"] - df["coverage"]).abs()
    summary = (
        df.groupby(["method", "alpha", "corruption"], as_index=False)
        .agg(
            coverage=("coverage", "mean"),
            avg_set_size=("avg_set_size", "mean"),
            abs_gap=("abs_coverage_gap", "mean"),
            n_cells=("dataset", "count"),
        )
        .sort_values(["alpha", "corruption", "method"])
    )
    summary.to_csv(out_dir / "summary.csv", index=False)
    keys = ["dataset", "seed", "corruption", "severity", "alpha"]
    cand = df[df["method"] == "fast_cp_mixed"]
    base = df[df["method"] == "aug_split_cp"]
    merged = cand.merge(base, on=keys, suffixes=("_fast", "_aug"))
    merged["coverage_delta"] = merged["coverage_fast"] - merged["coverage_aug"]
    merged["set_size_reduction"] = merged["avg_set_size_aug"] - merged["avg_set_size_fast"]
    comparison = (
        merged.groupby(["alpha", "corruption"], as_index=False)
        .agg(
            coverage_delta=("coverage_delta", "mean"),
            set_size_reduction=("set_size_reduction", "mean"),
            fast_coverage=("coverage_fast", "mean"),
            aug_coverage=("coverage_aug", "mean"),
            fast_set_size=("avg_set_size_fast", "mean"),
            aug_set_size=("avg_set_size_aug", "mean"),
        )
    )
    comparison.to_csv(out_dir / "fastcp_vs_aug.csv", index=False)


def stable_offset(*parts: object) -> int:
    text = "::".join(map(str, parts))
    return sum((i + 1) * ord(ch) for i, ch in enumerate(text)) % 1_000_000


if __name__ == "__main__":
    main()
