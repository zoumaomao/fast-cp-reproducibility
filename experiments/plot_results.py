from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot FAST-CP pilot results.")
    parser.add_argument("--input", default="results/pilot/fastcp_results.csv")
    parser.add_argument("--out", default="figures")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input)
    df["target_coverage"] = 1.0 - df["alpha"]
    df["coverage_gap_abs"] = (df["target_coverage"] - df["coverage"]).abs()

    for alpha, sub in df.groupby("alpha"):
        grouped = sub.groupby("method", as_index=False).agg(
            coverage=("coverage", "mean"),
            set_size=("avg_set_size", "mean"),
            gap=("coverage_gap_abs", "mean"),
        )
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.scatter(grouped["set_size"], grouped["coverage"], s=70)
        for _, row in grouped.iterrows():
            ax.annotate(row["method"], (row["set_size"], row["coverage"]), fontsize=8, xytext=(4, 4), textcoords="offset points")
        ax.axhline(1.0 - alpha, color="black", linestyle="--", linewidth=1)
        ax.set_xlabel("Average prediction set size")
        ax.set_ylabel("Coverage")
        ax.set_title(f"Coverage/efficiency tradeoff, alpha={alpha}")
        fig.tight_layout()
        fig.savefig(out_dir / f"coverage_vs_size_alpha_{alpha:.2f}.png", dpi=180)
        plt.close(fig)
    print(f"Wrote figures to {out_dir}")


if __name__ == "__main__":
    main()

