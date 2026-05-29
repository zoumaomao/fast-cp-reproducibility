from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize alpha/lambda Pareto frontier for FAST-CP.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-csv", required=True)
    parser.add_argument("--out-md", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input)
    rows = []
    for method in sorted(m for m in df["method"].unique() if m.startswith("fast_cp_mixed_")):
        lam = float(method.removeprefix("fast_cp_mixed_"))
        sub = df[df["method"] == method].copy()
        sub["target_coverage"] = 1.0 - sub["alpha"]
        sub["abs_coverage_gap"] = (sub["target_coverage"] - sub["coverage"]).abs()
        grouped = sub.groupby(["alpha", "corruption"], as_index=False).agg(
            coverage=("coverage", "mean"),
            avg_set_size=("avg_set_size", "mean"),
            abs_coverage_gap=("abs_coverage_gap", "mean"),
        )
        for _, row in grouped.iterrows():
            rows.append({"lambda": lam, "method": method, **row.to_dict()})
    table = pd.DataFrame(rows)
    table["pareto"] = False
    for (alpha, corruption), group in table.groupby(["alpha", "corruption"]):
        idxs = group.index.tolist()
        for idx in idxs:
            row = table.loc[idx]
            dominated = False
            for other_idx in idxs:
                if other_idx == idx:
                    continue
                other = table.loc[other_idx]
                better_or_equal = (
                    other["avg_set_size"] <= row["avg_set_size"]
                    and other["abs_coverage_gap"] <= row["abs_coverage_gap"]
                )
                strictly_better = (
                    other["avg_set_size"] < row["avg_set_size"]
                    or other["abs_coverage_gap"] < row["abs_coverage_gap"]
                )
                if better_or_equal and strictly_better:
                    dominated = True
                    break
            table.loc[idx, "pareto"] = not dominated
    table = table.sort_values(["alpha", "corruption", "lambda"])
    out_csv = Path(args.out_csv)
    out_md = Path(args.out_md)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out_csv, index=False)
    out_md.write_text(render_markdown(table))
    print(table.to_string(index=False))
    print(f"Wrote {out_csv} and {out_md}")


def render_markdown(table: pd.DataFrame) -> str:
    pareto = table[table["pareto"]].copy()
    lines = [
        "# Alpha/Lambda Pareto Frontier",
        "",
        "Pareto is computed by minimizing both average prediction-set size and absolute coverage gap within each alpha/corruption group.",
        "",
        "## Pareto Points",
        "",
        markdown_table(pareto),
        "",
        "## Full Grid",
        "",
        markdown_table(table),
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
