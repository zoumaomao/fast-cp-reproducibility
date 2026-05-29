from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import RidgeClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from experiments.conformal import (
    aps_prediction_sets,
    aps_scores,
    conformal_threshold,
    inverse_probability_scores,
    metrics,
    mondrian_prediction_sets,
    prediction_sets_from_threshold,
    smooth_probs,
    weighted_prediction_sets,
)
from experiments.corruptions import corrupt_batch, fill_nans
from experiments.data import load_ucr_dataset
from experiments.features import RandomConvFeatures, perturbation_fingerprint


CORRUPTION_LEVELS = {
    "gap": [0.05, 0.10, 0.20],
    "noise": [0.05, 0.10, 0.20],
    "drift": [0.10, 0.20, 0.40],
    "warp": [0.25, 0.50, 0.80],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run FAST-CP pilot experiments on UCR datasets.")
    parser.add_argument("--datasets", nargs="+", default=["ECG200", "GunPoint", "ItalyPowerDemand", "TwoLeadECG", "Coffee"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[0])
    parser.add_argument("--corruptions", nargs="+", default=["gap", "noise", "drift"])
    parser.add_argument("--alphas", nargs="+", type=float, default=[0.10, 0.05])
    parser.add_argument("--n-kernels", type=int, default=192)
    parser.add_argument("--backbone", choices=["randomconv", "minirocket"], default="randomconv")
    parser.add_argument("--minirocket-kernels", type=int, default=2048)
    parser.add_argument("--calib-size", type=float, default=0.35)
    parser.add_argument("--fastcp-global-mix", type=float, default=0.35)
    parser.add_argument("--fastcp-global-mixes", nargs="+", type=float, default=None)
    parser.add_argument("--raps-lambda", type=float, default=0.01)
    parser.add_argument("--raps-k", type=int, default=1)
    parser.add_argument(
        "--fingerprint-ablations",
        nargs="*",
        default=[],
        choices=[
            "input_only",
            "confidence_only",
            "no_missing",
            "no_spectral",
            "no_drift",
            "no_confidence",
            "random_fingerprint",
        ],
        help="Optional FAST-CP-mixed feature ablations to add as extra methods.",
    )
    parser.add_argument("--out-dir", default="results/pilot")
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--max-iter", type=int, default=800)
    parser.add_argument("--continue-on-error", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    started = time.time()

    for dataset in tqdm(args.datasets, desc="datasets"):
        try:
            x_train, y_train, x_test, y_test = load_ucr_dataset(dataset, args.data_dir)
            if len(np.unique(y_train)) < 2:
                raise ValueError("dataset has fewer than two classes")
            for seed in args.seeds:
                rows.extend(run_one_dataset(dataset, x_train, y_train, x_test, y_test, seed, args))
        except Exception as exc:
            if not args.continue_on_error:
                raise
            error_path = out_dir / "errors.log"
            with error_path.open("a") as handle:
                handle.write(f"{dataset}: {type(exc).__name__}: {exc}\n")

    results = pd.DataFrame(rows)
    result_path = out_dir / "fastcp_results.csv"
    results.to_csv(result_path, index=False)
    summary = {
        "datasets": args.datasets,
        "seeds": args.seeds,
        "corruptions": args.corruptions,
        "alphas": args.alphas,
        "backbone": args.backbone,
        "n_kernels": args.n_kernels,
        "minirocket_kernels": args.minirocket_kernels,
        "elapsed_sec": round(time.time() - started, 3),
        "rows": int(len(results)),
        "result_path": str(result_path),
        "errors_path": str(out_dir / "errors.log") if (out_dir / "errors.log").exists() else None,
    }
    (out_dir / "run_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


def run_one_dataset(
    dataset: str,
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    seed: int,
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    rng = np.random.default_rng(seed)
    stratify = y_train if min(np.bincount(y_train)) >= 2 else None
    x_fit, x_calib, y_fit, y_calib = train_test_split(
        x_train,
        y_train,
        test_size=args.calib_size,
        random_state=seed,
        stratify=stratify,
    )

    featurizer, model = fit_backbone(x_fit, y_fit, seed, args)

    clean_calib_probs = model.predict_proba(transform_backbone(featurizer, x_calib))
    clean_calib_scores = inverse_probability_scores(clean_calib_probs, y_calib)
    clean_calib_fp = perturbation_fingerprint(x_calib, clean_calib_probs)

    aug_x, aug_y, aug_groups = build_augmented_calibration(x_calib, y_calib, args.corruptions, seed)
    aug_probs = model.predict_proba(transform_backbone(featurizer, aug_x))
    aug_scores = inverse_probability_scores(aug_probs, aug_y)
    aug_aps_scores = aps_scores(aug_probs, aug_y)
    aug_raps_scores = aps_scores(aug_probs, aug_y, raps_lambda=args.raps_lambda, raps_k=args.raps_k)
    aug_fp = perturbation_fingerprint(aug_x, aug_probs)
    aug_fp_conf = aug_fp[:, -2:]
    global_mixes = args.fastcp_global_mixes if args.fastcp_global_mixes is not None else [args.fastcp_global_mix]

    rows: list[dict[str, object]] = []
    for corruption in args.corruptions:
        for severity in CORRUPTION_LEVELS[corruption]:
            local_rng = np.random.default_rng(seed + stable_offset(dataset, corruption, severity))
            x_eval_raw = corrupt_batch(x_test, corruption, severity, local_rng)
            probs = model.predict_proba(transform_backbone(featurizer, x_eval_raw))
            test_fp = perturbation_fingerprint(x_eval_raw, probs)
            random_fp_rng = np.random.default_rng(seed + stable_offset(dataset, corruption, severity, "random_fingerprint"))
            random_aug_fp = random_fp_rng.normal(size=aug_fp.shape).astype(np.float32)
            random_test_fp = random_fp_rng.normal(size=test_fp.shape).astype(np.float32)

            for alpha in args.alphas:
                aug_global_threshold = conformal_threshold(aug_scores, alpha)
                aps_threshold = conformal_threshold(aug_aps_scores, alpha)
                raps_threshold = conformal_threshold(aug_raps_scores, alpha)
                candidates = {
                    "clean_split_cp": prediction_sets_from_threshold(
                        probs, conformal_threshold(clean_calib_scores, alpha)
                    ),
                    "aug_split_cp": prediction_sets_from_threshold(
                        probs, aug_global_threshold
                    ),
                    "aps_aug_cp": aps_prediction_sets(
                        probs, aps_threshold
                    ),
                    "raps_aug_cp": aps_prediction_sets(
                        probs, raps_threshold, raps_lambda=args.raps_lambda, raps_k=args.raps_k
                    ),
                    "mondrian_corruption_cp": mondrian_prediction_sets(
                        aug_scores, aug_groups, probs, corruption, alpha, fallback_threshold=aug_global_threshold
                    ),
                    "label_smooth_aug_cp": prediction_sets_from_threshold(
                        smooth_probs(probs), conformal_threshold(inverse_probability_scores(smooth_probs(aug_probs), aug_y), alpha)
                    ),
                    "confidence_weighted_cp": weighted_prediction_sets(
                        aug_scores, aug_fp_conf, probs, test_fp[:, -2:], alpha
                    ),
                    "fast_cp": weighted_prediction_sets(
                        aug_scores, aug_fp, probs, test_fp, alpha
                    ),
                }
                for mix in global_mixes:
                    method_name = "fast_cp_mixed" if len(global_mixes) == 1 else f"fast_cp_mixed_{mix:g}"
                    candidates[method_name] = weighted_prediction_sets(
                        aug_scores,
                        aug_fp,
                        probs,
                        test_fp,
                        alpha,
                        global_threshold=aug_global_threshold,
                        global_mix=mix,
                    )
                    for ablation in args.fingerprint_ablations:
                        if ablation == "random_fingerprint":
                            ablated_aug_fp = random_aug_fp
                            ablated_test_fp = random_test_fp
                        else:
                            ablated_aug_fp = select_fingerprint_columns(aug_fp, ablation)
                            ablated_test_fp = select_fingerprint_columns(test_fp, ablation)
                        candidates[f"{method_name}_{ablation}"] = weighted_prediction_sets(
                            aug_scores,
                            ablated_aug_fp,
                            probs,
                            ablated_test_fp,
                            alpha,
                            global_threshold=aug_global_threshold,
                            global_mix=mix,
                        )
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
                        "n_classes": int(len(np.unique(y_train))),
                    }
                    row.update(metrics(pred_sets, y_test, probs))
                    rows.append(row)
    return rows


def fit_backbone(
    x_fit: np.ndarray,
    y_fit: np.ndarray,
    seed: int,
    args: argparse.Namespace,
) -> tuple[object, object]:
    if args.backbone == "randomconv":
        featurizer = RandomConvFeatures(n_kernels=args.n_kernels, seed=seed).fit(x_fit)
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=args.max_iter, solver="lbfgs"),
        )
        model.fit(featurizer.transform(x_fit), y_fit)
        return featurizer, model

    if args.backbone == "minirocket":
        try:
            from aeon.transformations.collection.convolution_based import MiniRocket
        except ImportError as exc:
            raise RuntimeError("MiniROCKET backbone requires `aeon`; install it with `pip install aeon`.") from exc

        featurizer = MiniRocket(n_kernels=args.minirocket_kernels, random_state=seed, n_jobs=1)
        x_features = featurizer.fit_transform(fill_nans(x_fit)[:, None, :])
        min_class_count = int(np.min(np.bincount(y_fit)))
        if min_class_count < 2:
            model = make_pipeline(
                StandardScaler(with_mean=False),
                LogisticRegression(max_iter=args.max_iter, solver="lbfgs"),
            )
        else:
            base = make_pipeline(
                StandardScaler(with_mean=False),
                RidgeClassifierCV(alphas=np.logspace(-3, 3, 10)),
            )
            model = CalibratedClassifierCV(base, method="sigmoid", cv=min(3, min_class_count))
        model.fit(x_features, y_fit)
        return featurizer, model

    raise ValueError(f"unknown backbone: {args.backbone}")


def transform_backbone(featurizer: object, x: np.ndarray) -> np.ndarray:
    if isinstance(featurizer, RandomConvFeatures):
        return featurizer.transform(x)
    return featurizer.transform(fill_nans(x)[:, None, :])


def build_augmented_calibration(
    x_calib: np.ndarray,
    y_calib: np.ndarray,
    corruptions: list[str],
    seed: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xs = [x_calib.astype(np.float32)]
    ys = [y_calib]
    groups = [np.full(y_calib.shape, "clean", dtype=object)]
    for corruption in corruptions:
        for severity in CORRUPTION_LEVELS[corruption]:
            rng = np.random.default_rng(seed + stable_offset("calib", corruption, severity))
            xs.append(corrupt_batch(x_calib, corruption, severity, rng))
            ys.append(y_calib)
            groups.append(np.full(y_calib.shape, corruption, dtype=object))
    return np.vstack(xs), np.concatenate(ys), np.concatenate(groups)


def select_fingerprint_columns(fingerprint: np.ndarray, ablation: str) -> np.ndarray:
    # Columns: missing, local variation, spectral entropy, autocorrelation, drift,
    # amplitude, top confidence, margin.
    columns = {
        "input_only": [0, 1, 2, 3, 4, 5],
        "confidence_only": [6, 7],
        "no_missing": [1, 2, 3, 4, 5, 6, 7],
        "no_spectral": [0, 1, 3, 4, 5, 6, 7],
        "no_drift": [0, 1, 2, 3, 5, 6, 7],
        "no_confidence": [0, 1, 2, 3, 4, 5],
    }[ablation]
    return fingerprint[:, columns]


def stable_offset(*parts: object) -> int:
    text = "::".join(map(str, parts))
    return sum((i + 1) * ord(ch) for i, ch in enumerate(text)) % 1_000_000


if __name__ == "__main__":
    main()
