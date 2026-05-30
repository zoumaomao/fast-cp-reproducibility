from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


KEYS = ["dataset", "seed", "corruption", "severity", "alpha"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dataset-level block bootstrap for paired FAST-CP comparisons.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--candidate", default="fast_cp_mixed")
    parser.add_argument("--baseline", default="aug_split_cp")
    parser.add_argument("--out-csv", required=True)
    parser.add_argument("--out-md", required=True)
    parser.add_argument("--bootstrap", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input)
    df["target_coverage"] = 1.0 - df["alpha"]
    df["abs_coverage_gap"] = (df["target_coverage"] - df["coverage"]).abs()

    cand = df[df["method"] == args.candidate].copy()
    base = df[df["method"] == args.baseline].copy()
    merged = cand.merge(base, on=KEYS, suffixes=("_candidate", "_baseline"))
    if merged.empty:
        raise ValueError("No paired rows found for requested methods.")

    merged["set_size_reduction"] = merged["avg_set_size_baseline"] - merged["avg_set_size_candidate"]
    merged["coverage_delta"] = merged["coverage_candidate"] - merged["coverage_baseline"]
    merged["abs_gap_delta"] = merged["abs_coverage_gap_candidate"] - merged["abs_coverage_gap_baseline"]

    rows = []
    for alpha in sorted(merged["alpha"].unique()):
        sub_alpha = merged[merged["alpha"] == alpha]
        for metric in ["set_size_reduction", "coverage_delta", "abs_gap_delta"]:
            rows.append(summarize_dataset_blocks(sub_alpha, metric, alpha, "__overall__", args.bootstrap, args.seed))
        for corruption in sorted(sub_alpha["corruption"].unique()):
            sub = sub_alpha[sub_alpha["corruption"] == corruption]
            for metric in ["set_size_reduction", "coverage_delta", "abs_gap_delta"]:
                rows.append(summarize_dataset_blocks(sub, metric, alpha, corruption, args.bootstrap, args.seed))

    out = pd.DataFrame(rows)
    out_csv = Path(args.out_csv)
    out_md = Path(args.out_md)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_csv, index=False)
    out_md.write_text(render_markdown(out, args))
    print(out.to_string(index=False))


def summarize_dataset_blocks(
    df: pd.DataFrame,
    metric: str,
    alpha: float,
    corruption: str,
    bootstrap: int,
    seed: int,
) -> dict[str, object]:
    blocks = df.groupby("dataset", as_index=False)[metric].mean().sort_values("dataset")
    values = blocks[metric].to_numpy(dtype=np.float64)
    ci_low, ci_high = bootstrap_ci(values, bootstrap, seed)
    return {
        "alpha": alpha,
        "corruption": corruption,
        "metric": metric,
        "n_datasets": int(values.size),
        "dataset_block_mean": float(values.mean()),
        "dataset_block_median": float(np.median(values)),
        "ci95_low": ci_low,
        "ci95_high": ci_high,
        "positive_dataset_rate": float(np.mean(values > 0.0)),
    }


def bootstrap_ci(values: np.ndarray, rounds: int, seed: int) -> tuple[float, float]:
    if values.size == 1:
        val = float(values[0])
        return val, val
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, values.size, size=(rounds, values.size))
    means = values[idx].mean(axis=1)
    low, high = np.quantile(means, [0.025, 0.975])
    return float(low), float(high)


def render_markdown(df: pd.DataFrame, args: argparse.Namespace) -> str:
    lines = [
        "# Dataset-Level Block Bootstrap",
        "",
        f"Input: `{args.input}`",
        f"Candidate: `{args.candidate}`",
        f"Baseline: `{args.baseline}`",
        "",
        "Each dataset is treated as one resampling block. Metrics are first averaged within each dataset over seeds, corruptions, and severities, then bootstrapped over datasets.",
        "Positive `set_size_reduction` means the candidate has smaller prediction sets. Positive `coverage_delta` means the candidate has higher empirical coverage. Negative `abs_gap_delta` means the candidate is closer to target coverage.",
        "",
        markdown_table(df),
        "",
    ]
    return "\n".join(lines)


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        cells = []
        for value in row:
            if isinstance(value, float):
                cells.append(f"{value:.6g}")
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
