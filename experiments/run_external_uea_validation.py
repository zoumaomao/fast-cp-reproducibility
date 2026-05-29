from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from aeon.datasets import load_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tqdm import tqdm

from experiments.conformal import (
    conformal_threshold,
    inverse_probability_scores,
    metrics,
    prediction_sets_from_threshold,
    weighted_prediction_sets,
)
from experiments.features import RandomConvFeatures, perturbation_fingerprint


CORRUPTION_LEVELS = {
    "gap": [0.05, 0.10, 0.20],
    "noise": [0.05, 0.10, 0.20],
    "drift": [0.10, 0.20, 0.40],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="External UEA validation for FAST-CP.")
    parser.add_argument("--datasets", nargs="+", default=["BasicMotions", "Epilepsy", "NATOPS"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    parser.add_argument("--corruptions", nargs="+", default=["gap", "noise", "drift"])
    parser.add_argument("--alphas", nargs="+", type=float, default=[0.05])
    parser.add_argument("--n-kernels", type=int, default=32)
    parser.add_argument("--calib-size", type=float, default=0.35)
    parser.add_argument("--fastcp-global-mix", type=float, default=0.35)
    parser.add_argument("--data-dir", default="data/uea")
    parser.add_argument("--out-dir", default="results/uea_external_3ds_3seed_alpha005")
    parser.add_argument("--max-iter", type=int, default=800)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    started = time.time()
    for dataset in tqdm(args.datasets, desc="uea datasets"):
        x_train, y_train, x_test, y_test = load_uea_dataset(dataset, args.data_dir)
        for seed in args.seeds:
            rows.extend(run_one_dataset(dataset, x_train, y_train, x_test, y_test, seed, args))
    results = pd.DataFrame(rows)
    result_path = out_dir / "fastcp_uea_results.csv"
    results.to_csv(result_path, index=False)
    summary = {
        "datasets": args.datasets,
        "seeds": args.seeds,
        "corruptions": args.corruptions,
        "alphas": args.alphas,
        "n_kernels_per_channel": args.n_kernels,
        "elapsed_sec": round(time.time() - started, 3),
        "rows": int(len(results)),
        "result_path": str(result_path),
    }
    (out_dir / "run_summary.json").write_text(json.dumps(summary, indent=2))
    write_summary_tables(results, out_dir)
    print(json.dumps(summary, indent=2))


def load_uea_dataset(name: str, data_dir: str | Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x_train, y_train_raw = load_classification(name, split="train", extract_path=str(data_dir))
    x_test, y_test_raw = load_classification(name, split="test", extract_path=str(data_dir))
    encoder = LabelEncoder()
    y_train = encoder.fit_transform(y_train_raw)
    y_test = encoder.transform(y_test_raw)
    return x_train.astype(np.float32), y_train, x_test.astype(np.float32), y_test


def run_one_dataset(
    dataset: str,
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    seed: int,
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    stratify = y_train if min(np.bincount(y_train)) >= 2 else None
    x_fit, x_calib, y_fit, y_calib = train_test_split(
        x_train,
        y_train,
        test_size=args.calib_size,
        random_state=seed,
        stratify=stratify,
    )
    featurizer = MultiChannelRandomConv(n_kernels=args.n_kernels, seed=seed).fit(x_fit)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=args.max_iter, solver="lbfgs"))
    model.fit(featurizer.transform(x_fit), y_fit)

    clean_probs = model.predict_proba(featurizer.transform(x_calib))
    clean_scores = inverse_probability_scores(clean_probs, y_calib)

    aug_x, aug_y = build_augmented_calibration(x_calib, y_calib, args.corruptions, seed)
    aug_probs = model.predict_proba(featurizer.transform(aug_x))
    aug_scores = inverse_probability_scores(aug_probs, aug_y)
    aug_fp_full = multivariate_fingerprint(aug_x, aug_probs)
    aug_fp_input = multivariate_fingerprint(aug_x, None)
    aug_fp_conf = aug_fp_full[:, -2:]

    rows: list[dict[str, object]] = []
    for corruption in args.corruptions:
        for severity in CORRUPTION_LEVELS[corruption]:
            rng = np.random.default_rng(seed + stable_offset(dataset, corruption, severity))
            x_eval = corrupt_multivariate(x_test, corruption, severity, rng)
            probs = model.predict_proba(featurizer.transform(x_eval))
            test_fp_full = multivariate_fingerprint(x_eval, probs)
            test_fp_input = multivariate_fingerprint(x_eval, None)
            test_fp_conf = test_fp_full[:, -2:]
            rand_rng = np.random.default_rng(seed + stable_offset(dataset, corruption, severity, "random"))
            random_aug_fp = rand_rng.normal(size=aug_fp_full.shape).astype(np.float32)
            random_test_fp = rand_rng.normal(size=test_fp_full.shape).astype(np.float32)

            for alpha in args.alphas:
                aug_global = conformal_threshold(aug_scores, alpha)
                candidates = {
                    "clean_split_cp": prediction_sets_from_threshold(
                        probs, conformal_threshold(clean_scores, alpha)
                    ),
                    "aug_split_cp": prediction_sets_from_threshold(probs, aug_global),
                    "fast_cp_mixed_input_only": weighted_prediction_sets(
                        aug_scores,
                        aug_fp_input,
                        probs,
                        test_fp_input,
                        alpha,
                        global_threshold=aug_global,
                        global_mix=args.fastcp_global_mix,
                    ),
                    "fast_cp_mixed_confidence_only": weighted_prediction_sets(
                        aug_scores,
                        aug_fp_conf,
                        probs,
                        test_fp_conf,
                        alpha,
                        global_threshold=aug_global,
                        global_mix=args.fastcp_global_mix,
                    ),
                    "fast_cp_mixed_random_fingerprint": weighted_prediction_sets(
                        aug_scores,
                        random_aug_fp,
                        probs,
                        random_test_fp,
                        alpha,
                        global_threshold=aug_global,
                        global_mix=args.fastcp_global_mix,
                    ),
                    "fast_cp_mixed": weighted_prediction_sets(
                        aug_scores,
                        aug_fp_full,
                        probs,
                        test_fp_full,
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
                        "n_train": int(x_fit.shape[0]),
                        "n_calib": int(x_calib.shape[0]),
                        "n_aug_calib": int(aug_x.shape[0]),
                        "n_test": int(x_test.shape[0]),
                        "n_channels": int(x_train.shape[1]),
                        "series_length": int(x_train.shape[2]),
                        "n_classes": int(len(np.unique(y_train))),
                    }
                    row.update(metrics(pred_sets, y_test, probs))
                    rows.append(row)
    return rows


class MultiChannelRandomConv:
    def __init__(self, n_kernels: int, seed: int):
        self.n_kernels = n_kernels
        self.seed = seed

    def fit(self, x: np.ndarray) -> "MultiChannelRandomConv":
        self.transforms_ = []
        for channel in range(x.shape[1]):
            self.transforms_.append(RandomConvFeatures(n_kernels=self.n_kernels, seed=self.seed + channel).fit(x[:, channel, :]))
        return self

    def transform(self, x: np.ndarray) -> np.ndarray:
        blocks = [transform.transform(x[:, channel, :]) for channel, transform in enumerate(self.transforms_)]
        return np.hstack(blocks).astype(np.float32)


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
            rng = np.random.default_rng(seed + stable_offset("uea_calib", corruption, severity))
            xs.append(corrupt_multivariate(x_calib, corruption, severity, rng))
            ys.append(y_calib)
    return np.vstack(xs), np.concatenate(ys)


def corrupt_multivariate(x: np.ndarray, corruption: str, severity: float, rng: np.random.Generator) -> np.ndarray:
    out = x.astype(np.float32, copy=True)
    if corruption == "gap":
        length = out.shape[2]
        gap = max(1, int(round(length * severity)))
        for i in range(out.shape[0]):
            start = int(rng.integers(0, max(1, length - gap + 1)))
            out[i, :, start : start + gap] = np.nan
        return fill_nan_channels(out)
    if corruption == "noise":
        scale = np.nanstd(out, axis=2, keepdims=True)
        scale = np.where(scale < 1e-8, 1.0, scale)
        return out + rng.normal(0.0, severity, size=out.shape).astype(np.float32) * scale
    if corruption == "drift":
        ramp = np.linspace(0.0, severity, out.shape[2], dtype=np.float32)[None, None, :]
        sign = rng.choice(np.array([-1.0, 1.0], dtype=np.float32), size=(out.shape[0], out.shape[1], 1))
        return out * (1.0 + sign * ramp)
    raise ValueError(f"unknown corruption: {corruption}")


def fill_nan_channels(x: np.ndarray) -> np.ndarray:
    out = x.copy()
    for i in range(out.shape[0]):
        for c in range(out.shape[1]):
            row = out[i, c]
            if np.isfinite(row).any():
                fill = float(np.nanmean(row))
            else:
                fill = 0.0
            out[i, c] = np.where(np.isfinite(row), row, fill)
    return out


def multivariate_fingerprint(x: np.ndarray, probs: np.ndarray | None) -> np.ndarray:
    n, channels, length = x.shape
    flat = x.reshape(n * channels, length)
    per_channel = perturbation_fingerprint(flat, None).reshape(n, channels, -1)
    blocks = [per_channel.mean(axis=1), per_channel.std(axis=1)]
    if probs is not None:
        sorted_probs = np.sort(probs, axis=1)
        top = sorted_probs[:, -1:]
        second = sorted_probs[:, -2:-1] if probs.shape[1] > 1 else np.zeros_like(top)
        blocks.extend([top.astype(np.float32), (top - second).astype(np.float32)])
    return np.hstack(blocks).astype(np.float32)


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
