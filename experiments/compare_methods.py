from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare a candidate method against a baseline.")
    parser.add_argument("--input", default="results/pilot5_mixed/fastcp_results.csv")
    parser.add_argument("--candidate", default="fast_cp_mixed")
    parser.add_argument("--baseline", default="aug_split_cp")
    parser.add_argument("--out", default="results/method_comparison.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input)
    df["target_coverage"] = 1.0 - df["alpha"]
    df["abs_coverage_gap"] = (df["target_coverage"] - df["coverage"]).abs()
    keys = ["dataset", "seed", "corruption", "severity", "alpha"]

    cand = df[df["method"] == args.candidate].copy()
    base = df[df["method"] == args.baseline].copy()
    merged = cand.merge(base, on=keys, suffixes=("_candidate", "_baseline"))
    merged["set_size_reduction"] = merged["avg_set_size_baseline"] - merged["avg_set_size_candidate"]
    merged["set_size_reduction_pct"] = merged["set_size_reduction"] / merged["avg_set_size_baseline"].clip(lower=1e-8)
    merged["coverage_delta"] = merged["coverage_candidate"] - merged["coverage_baseline"]
    merged["abs_gap_delta"] = merged["abs_coverage_gap_candidate"] - merged["abs_coverage_gap_baseline"]

    summary = (
        merged.groupby(["alpha", "corruption"], as_index=False)
        .agg(
            n=("dataset", "count"),
            candidate_coverage=("coverage_candidate", "mean"),
            baseline_coverage=("coverage_baseline", "mean"),
            coverage_delta=("coverage_delta", "mean"),
            candidate_set_size=("avg_set_size_candidate", "mean"),
            baseline_set_size=("avg_set_size_baseline", "mean"),
            set_size_reduction=("set_size_reduction", "mean"),
            set_size_reduction_pct=("set_size_reduction_pct", "mean"),
            candidate_abs_gap=("abs_coverage_gap_candidate", "mean"),
            baseline_abs_gap=("abs_coverage_gap_baseline", "mean"),
            abs_gap_delta=("abs_gap_delta", "mean"),
        )
        .sort_values(["alpha", "corruption"])
    )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out, index=False)
    print(summary.to_string(index=False))
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
