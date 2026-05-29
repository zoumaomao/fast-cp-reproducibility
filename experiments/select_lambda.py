from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Select lambda from an independent tuning sweep.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--protocol", default="results/lambda_protocol/lambda_protocol.json")
    parser.add_argument("--out-csv", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    protocol = json.loads(Path(args.protocol).read_text())
    tolerance = float(protocol["selection_rule"]["coverage_tolerance"])
    df = pd.read_csv(args.input)
    rows = []
    for method in sorted(m for m in df["method"].unique() if m.startswith("fast_cp_mixed_")):
        lam = parse_lambda(method)
        sub = df[df["method"] == method].copy()
        grouped = sub.groupby("alpha", as_index=False).agg(
            coverage=("coverage", "mean"),
            avg_set_size=("avg_set_size", "mean"),
        )
        coverage_shortfall = 0.0
        feasible = True
        for _, row in grouped.iterrows():
            target = 1.0 - float(row["alpha"]) - tolerance
            shortfall = max(0.0, target - float(row["coverage"]))
            coverage_shortfall += shortfall
            feasible = feasible and shortfall <= 1e-12
        rows.append(
            {
                "lambda": lam,
                "method": method,
                "feasible": feasible,
                "coverage_shortfall": coverage_shortfall,
                "mean_coverage": sub["coverage"].mean(),
                "mean_set_size": sub["avg_set_size"].mean(),
                "mean_abs_gap": (1.0 - sub["alpha"] - sub["coverage"]).abs().mean(),
            }
        )
    summary = pd.DataFrame(rows).sort_values(["feasible", "mean_set_size"], ascending=[False, True])
    feasible = summary[summary["feasible"]]
    if feasible.empty:
        chosen = summary.sort_values(["coverage_shortfall", "mean_set_size"]).iloc[0]
        selection_reason = "fallback_min_shortfall_then_size"
    else:
        chosen = feasible.sort_values("mean_set_size").iloc[0]
        selection_reason = "feasible_min_set_size"

    out_csv = Path(args.out_csv)
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out_csv, index=False)
    result = {
        "selected_lambda": float(chosen["lambda"]),
        "selected_method": str(chosen["method"]),
        "selection_reason": selection_reason,
        "coverage_tolerance": tolerance,
        "summary_csv": str(out_csv),
    }
    out_json.write_text(json.dumps(result, indent=2))
    out_md.write_text(render_markdown(summary, result))
    print(summary.to_string(index=False))
    print(json.dumps(result, indent=2))


def parse_lambda(method: str) -> float:
    return float(method.removeprefix("fast_cp_mixed_"))


def render_markdown(summary: pd.DataFrame, result: dict[str, object]) -> str:
    lines = [
        "# Lambda Selection Result",
        "",
        f"Selected lambda: `{result['selected_lambda']}`",
        f"Reason: `{result['selection_reason']}`",
        "",
        markdown_table(summary),
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
