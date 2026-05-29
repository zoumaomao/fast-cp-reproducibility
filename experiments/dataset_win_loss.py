from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create dataset-level win/loss table for two methods.")
    parser.add_argument("--input", default="results/main10_3seed_alpha005/fastcp_results.csv")
    parser.add_argument("--candidate", default="fast_cp_mixed")
    parser.add_argument("--baseline", default="aug_split_cp")
    parser.add_argument("--out", default="results/dataset_win_loss.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input)
    keys = ["dataset", "seed", "corruption", "severity", "alpha"]
    df["target_coverage"] = 1.0 - df["alpha"]
    df["abs_coverage_gap"] = (df["target_coverage"] - df["coverage"]).abs()
    cand = df[df["method"] == args.candidate].copy()
    base = df[df["method"] == args.baseline].copy()
    merged = cand.merge(base, on=keys, suffixes=("_candidate", "_baseline"))
    merged["set_size_win"] = merged["avg_set_size_candidate"] < merged["avg_set_size_baseline"]
    merged["coverage_close"] = (merged["coverage_candidate"] - merged["coverage_baseline"]).abs() <= 0.01
    merged["abs_gap_win"] = merged["abs_coverage_gap_candidate"] <= merged["abs_coverage_gap_baseline"]

    dataset_summary = (
        merged.groupby(["dataset", "alpha"], as_index=False)
        .agg(
            n=("set_size_win", "count"),
            set_size_win_rate=("set_size_win", "mean"),
            coverage_close_rate=("coverage_close", "mean"),
            abs_gap_win_rate=("abs_gap_win", "mean"),
            avg_set_size_candidate=("avg_set_size_candidate", "mean"),
            avg_set_size_baseline=("avg_set_size_baseline", "mean"),
            avg_coverage_candidate=("coverage_candidate", "mean"),
            avg_coverage_baseline=("coverage_baseline", "mean"),
        )
        .sort_values(["set_size_win_rate", "abs_gap_win_rate"], ascending=False)
    )
    overall = pd.DataFrame(
        [
            {
                "dataset": "__OVERALL__",
                "alpha": merged["alpha"].iloc[0] if not merged.empty else None,
                "n": len(merged),
                "set_size_win_rate": merged["set_size_win"].mean(),
                "coverage_close_rate": merged["coverage_close"].mean(),
                "abs_gap_win_rate": merged["abs_gap_win"].mean(),
                "avg_set_size_candidate": merged["avg_set_size_candidate"].mean(),
                "avg_set_size_baseline": merged["avg_set_size_baseline"].mean(),
                "avg_coverage_candidate": merged["coverage_candidate"].mean(),
                "avg_coverage_baseline": merged["coverage_baseline"].mean(),
            }
        ]
    )
    out_df = pd.concat([overall, dataset_summary], ignore_index=True)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(out, index=False)
    print(out_df.to_string(index=False))
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
