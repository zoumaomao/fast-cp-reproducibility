from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate FAST-CP result CSV files.")
    parser.add_argument("--input", default="results/pilot/fastcp_results.csv")
    parser.add_argument("--out", default="results/pilot_summary.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input)
    df["target_coverage"] = 1.0 - df["alpha"]
    df["coverage_gap"] = df["target_coverage"] - df["coverage"]
    group_cols = ["method", "alpha", "corruption"]
    summary = (
        df.groupby(group_cols, as_index=False)
        .agg(
            coverage=("coverage", "mean"),
            coverage_gap=("coverage_gap", "mean"),
            abs_coverage_gap=("coverage_gap", lambda s: s.abs().mean()),
            avg_set_size=("avg_set_size", "mean"),
            singleton_rate=("singleton_rate", "mean"),
            top1_accuracy=("top1_accuracy", "mean"),
            ece=("ece", "mean"),
        )
        .sort_values(["alpha", "corruption", "abs_coverage_gap", "avg_set_size"])
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out, index=False)
    print(summary.to_string(index=False))
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()

