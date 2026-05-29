from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


KEYS = ["dataset", "seed", "corruption", "severity", "alpha"]

METHOD_LABELS = {
    "clean_split_cp": "Clean SCP",
    "aug_split_cp": "Aug SCP / global fallback",
    "aps_aug_cp": "APS",
    "raps_aug_cp": "RAPS",
    "mondrian_corruption_cp": "Mondrian",
    "confidence_weighted_cp": "Conf-weighted",
    "fast_cp": "FAST-CP-local",
    "fast_cp_mixed": "FAST-CP-efficient",
    "fast_cp_mixed_random_fingerprint": "Random fingerprint",
    "fast_cp_mixed_input_only": "Input-only",
    "fast_cp_mixed_confidence_only": "Confidence-only",
    "fast_cp_mixed_no_confidence": "Input-only (alias)",
}

MAIN_METHOD_ORDER = [
    "clean_split_cp",
    "aug_split_cp",
    "aps_aug_cp",
    "raps_aug_cp",
    "mondrian_corruption_cp",
    "confidence_weighted_cp",
    "fast_cp",
    "fast_cp_mixed",
]

FINGERPRINT_METHOD_ORDER = [
    "fast_cp_mixed_random_fingerprint",
    "fast_cp_mixed_input_only",
    "fast_cp_mixed_confidence_only",
    "fast_cp_mixed",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate reviewer audit tables for FAST-CP experiments.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--fig-dir", default="figures/paper")
    parser.add_argument("--paper-fig-dir", default="paper/figures")
    parser.add_argument("--baseline", default="aug_split_cp")
    parser.add_argument("--candidate", default="fast_cp_mixed")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir = Path(args.fig_dir)
    paper_fig_dir = Path(args.paper_fig_dir)
    fig_dir.mkdir(parents=True, exist_ok=True)
    paper_fig_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input)
    df["target_coverage"] = 1.0 - df["alpha"]
    df["coverage_gap"] = df["target_coverage"] - df["coverage"]
    df["abs_coverage_gap"] = df["coverage_gap"].abs()

    full = full_method_table(df, args.baseline)
    full.to_csv(out_dir / "full_method_table.csv", index=False)
    write_tex_table(full, out_dir / "full_method_table.tex", caption="Main method comparison on the expanded 35-dataset, five-seed UCR benchmark at $\\alpha=0.05$.", label="tab:full_method_table")

    comparison = comparison_by_corruption(df, args.candidate, args.baseline)
    comparison.to_csv(out_dir / "fastcp_vs_aug_by_corruption.csv", index=False)

    tail = tail_risk_table(df, methods=[args.baseline, args.candidate, "fast_cp_mixed_confidence_only"])
    tail.to_csv(out_dir / "tail_risk_table.csv", index=False)
    write_tex_table(tail, out_dir / "tail_risk_table.tex", caption="Undercoverage tail-risk audit on the expanded benchmark. Rates are fractions of dataset/seed/corruption/severity evaluation cells.", label="tab:tail_risk")

    worst = worst_coverage_drops(df, args.candidate, args.baseline)
    worst.to_csv(out_dir / "worst_coverage_drops.csv", index=False)

    severity = severity_summary(df, methods=[args.baseline, args.candidate])
    severity.to_csv(out_dir / "severity_summary.csv", index=False)

    fingerprint = fingerprint_variant_table(df, args.baseline)
    fingerprint.to_csv(out_dir / "fingerprint_variant_table.csv", index=False)
    write_tex_table(fingerprint, out_dir / "fingerprint_variant_table.tex", caption="Fingerprint contribution audit under the same mixed-threshold framework.", label="tab:fingerprint_variants")

    plot_coverage_delta(df, args.candidate, args.baseline, fig_dir)
    plot_coverage_delta(df, args.candidate, args.baseline, paper_fig_dir)
    plot_main_results(comparison, fig_dir)
    plot_main_results(comparison, paper_fig_dir)

    report = render_markdown(full, comparison, tail, worst, severity, fingerprint)
    (out_dir / "REVIEWER_AUDIT_REPORT.md").write_text(report)
    print(report)
    print(f"Wrote reviewer audit outputs to {out_dir}")


def full_method_table(df: pd.DataFrame, baseline: str) -> pd.DataFrame:
    rows = []
    base = df[df["method"] == baseline][KEYS + ["avg_set_size", "coverage", "abs_coverage_gap"]]
    for method in MAIN_METHOD_ORDER:
        sub = df[df["method"] == method].copy()
        if sub.empty:
            continue
        merged = sub.merge(base, on=KEYS, suffixes=("", "_baseline"))
        row = {
            "method": METHOD_LABELS.get(method, method),
            "coverage": sub["coverage"].mean(),
            "avg_set_size": sub["avg_set_size"].mean(),
            "abs_gap": sub["abs_coverage_gap"].mean(),
            "coverage_delta_vs_aug": merged["coverage"].sub(merged["coverage_baseline"]).mean(),
            "set_size_reduction_vs_aug": merged["avg_set_size_baseline"].sub(merged["avg_set_size"]).mean(),
        }
        for corruption in ["drift", "gap", "noise"]:
            row[f"{corruption}_set_size"] = sub[sub["corruption"] == corruption]["avg_set_size"].mean()
        rows.append(row)
    return pd.DataFrame(rows)


def comparison_by_corruption(df: pd.DataFrame, candidate: str, baseline: str) -> pd.DataFrame:
    cand = df[df["method"] == candidate].copy()
    base = df[df["method"] == baseline].copy()
    merged = cand.merge(base, on=KEYS, suffixes=("_candidate", "_baseline"))
    merged["target_coverage"] = 1.0 - merged["alpha"]
    merged["abs_gap_candidate"] = (merged["target_coverage"] - merged["coverage_candidate"]).abs()
    merged["abs_gap_baseline"] = (merged["target_coverage"] - merged["coverage_baseline"]).abs()
    merged["coverage_delta"] = merged["coverage_candidate"] - merged["coverage_baseline"]
    merged["set_size_reduction"] = merged["avg_set_size_baseline"] - merged["avg_set_size_candidate"]
    merged["set_size_reduction_pct"] = merged["set_size_reduction"] / merged["avg_set_size_baseline"].clip(lower=1e-8)
    merged["abs_gap_delta"] = merged["abs_gap_candidate"] - merged["abs_gap_baseline"]
    return (
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
            candidate_abs_gap=("abs_gap_candidate", "mean"),
            baseline_abs_gap=("abs_gap_baseline", "mean"),
            abs_gap_delta=("abs_gap_delta", "mean"),
        )
        .sort_values(["alpha", "corruption"])
    )


def tail_risk_table(df: pd.DataFrame, methods: list[str]) -> pd.DataFrame:
    rows = []
    for method in methods:
        sub = df[df["method"] == method].copy()
        if sub.empty:
            continue
        for corruption in ["__overall__", "drift", "gap", "noise"]:
            cur = sub if corruption == "__overall__" else sub[sub["corruption"] == corruption]
            if cur.empty:
                continue
            target = cur["target_coverage"]
            rows.append(
                {
                    "method": METHOD_LABELS.get(method, method),
                    "corruption": corruption,
                    "n_cells": int(len(cur)),
                    "mean_coverage": cur["coverage"].mean(),
                    "rate_below_target": (cur["coverage"] < target).mean(),
                    "rate_below_target_minus_1pp": (cur["coverage"] < target - 0.01).mean(),
                    "rate_below_target_minus_2pp": (cur["coverage"] < target - 0.02).mean(),
                    "p10_coverage": cur["coverage"].quantile(0.10),
                    "min_coverage": cur["coverage"].min(),
                }
            )
    return pd.DataFrame(rows)


def worst_coverage_drops(df: pd.DataFrame, candidate: str, baseline: str) -> pd.DataFrame:
    cand = df[df["method"] == candidate]
    base = df[df["method"] == baseline]
    merged = cand.merge(base, on=KEYS, suffixes=("_candidate", "_baseline"))
    merged["coverage_delta"] = merged["coverage_candidate"] - merged["coverage_baseline"]
    merged["set_size_reduction"] = merged["avg_set_size_baseline"] - merged["avg_set_size_candidate"]
    keep = [
        "dataset",
        "seed",
        "corruption",
        "severity",
        "alpha",
        "coverage_candidate",
        "coverage_baseline",
        "coverage_delta",
        "avg_set_size_candidate",
        "avg_set_size_baseline",
        "set_size_reduction",
        "n_test_candidate",
        "n_classes_candidate",
    ]
    return merged.sort_values("coverage_delta").head(10)[keep].rename(
        columns={
            "coverage_candidate": "fast_coverage",
            "coverage_baseline": "aug_coverage",
            "avg_set_size_candidate": "fast_set_size",
            "avg_set_size_baseline": "aug_set_size",
            "n_test_candidate": "n_test",
            "n_classes_candidate": "n_classes",
        }
    )


def severity_summary(df: pd.DataFrame, methods: list[str]) -> pd.DataFrame:
    sub = df[df["method"].isin(methods)].copy()
    sub["method"] = sub["method"].map(lambda m: METHOD_LABELS.get(m, m))
    return (
        sub.groupby(["method", "corruption", "severity"], as_index=False)
        .agg(
            n_cells=("dataset", "count"),
            coverage=("coverage", "mean"),
            avg_set_size=("avg_set_size", "mean"),
            abs_gap=("abs_coverage_gap", "mean"),
        )
        .sort_values(["corruption", "severity", "method"])
    )


def fingerprint_variant_table(df: pd.DataFrame, baseline: str) -> pd.DataFrame:
    base = df[df["method"] == baseline][KEYS + ["coverage", "avg_set_size", "abs_coverage_gap"]]
    rows = []
    for method in FINGERPRINT_METHOD_ORDER:
        sub = df[df["method"] == method].copy()
        if sub.empty:
            continue
        merged = sub.merge(base, on=KEYS, suffixes=("", "_baseline"))
        rows.append(
            {
                "variant": METHOD_LABELS.get(method, method),
                "coverage": sub["coverage"].mean(),
                "avg_set_size": sub["avg_set_size"].mean(),
                "abs_gap": sub["abs_coverage_gap"].mean(),
                "coverage_delta_vs_aug": merged["coverage"].sub(merged["coverage_baseline"]).mean(),
                "set_size_reduction_vs_aug": merged["avg_set_size_baseline"].sub(merged["avg_set_size"]).mean(),
            }
        )
    return pd.DataFrame(rows)


def plot_coverage_delta(df: pd.DataFrame, candidate: str, baseline: str, fig_dir: Path) -> None:
    cand = df[df["method"] == candidate]
    base = df[df["method"] == baseline]
    merged = cand.merge(base, on=KEYS, suffixes=("_candidate", "_baseline"))
    merged["coverage_delta_pp"] = 100.0 * (merged["coverage_candidate"] - merged["coverage_baseline"])
    data = [merged[merged["corruption"] == c]["coverage_delta_pp"].to_numpy() for c in ["drift", "gap", "noise"]]

    plt.rcParams.update({"font.family": "serif", "pdf.fonttype": 42, "ps.fonttype": 42})
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    ax.boxplot(data, labels=["drift", "gap", "noise"], showfliers=False, patch_artist=True)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axhline(-1.0, color="#B00020", linewidth=0.8, linestyle="--")
    ax.set_ylabel("Coverage delta vs Aug SCP (pp)")
    ax.set_xlabel("Corruption")
    ax.set_title("Coverage-tail distribution")
    fig.tight_layout()
    fig.savefig(fig_dir / "fig7_coverage_delta_tail.pdf", bbox_inches="tight")
    fig.savefig(fig_dir / "fig7_coverage_delta_tail.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_main_results(df: pd.DataFrame, fig_dir: Path) -> None:
    order = ["drift", "gap", "noise"]
    plot_df = df.set_index("corruption").loc[order].reset_index()
    plt.rcParams.update({"font.family": "serif", "pdf.fonttype": 42, "ps.fonttype": 42})
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8))
    axes[0].bar(plot_df["corruption"], plot_df["set_size_reduction_pct"] * 100.0, color="#4C78A8")
    axes[0].axhline(0, color="black", linewidth=0.8)
    axes[0].set_ylabel("Set-size reduction (%)")
    axes[0].set_title("Efficiency gain")
    axes[1].bar(plot_df["corruption"], plot_df["coverage_delta"] * 100.0, color="#F58518")
    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].set_ylabel("Coverage delta (pp)")
    axes[1].set_title("Coverage change")
    for ax in axes:
        ax.set_xlabel("Corruption")
    fig.tight_layout()
    fig.savefig(fig_dir / "fig2_main_results.pdf", bbox_inches="tight")
    fig.savefig(fig_dir / "fig2_main_results.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_tex_table(df: pd.DataFrame, path: Path, caption: str, label: str) -> None:
    rounded = df.copy()
    for col in rounded.columns:
        if pd.api.types.is_float_dtype(rounded[col]):
            rounded[col] = rounded[col].map(lambda x: f"{x:.4f}")
    headers = [latex_escape(str(col).replace("_", " ")) for col in rounded.columns]
    lines = [
        "\\begin{tabular}{" + "l" + "r" * (len(headers) - 1) + "}",
        "\\toprule",
        " & ".join(headers) + " \\\\",
        "\\midrule",
    ]
    for _, row in rounded.iterrows():
        cells = [latex_escape(str(value)) for value in row]
        lines.append(" & ".join(cells) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    table = "\n".join(lines)
    text = "\\begin{table}[t]\n\\centering\n\\small\n" + table + f"\n\\caption{{{caption}}}\n\\label{{{label}}}\n\\end{{table}}\n"
    path.write_text(text)


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def render_markdown(
    full: pd.DataFrame,
    comparison: pd.DataFrame,
    tail: pd.DataFrame,
    worst: pd.DataFrame,
    severity: pd.DataFrame,
    fingerprint: pd.DataFrame,
) -> str:
    return "\n\n".join(
        [
            "# FAST-CP Reviewer Audit Report",
            "## Full Method Table\n\n" + markdown_table(full),
            "## FAST-CP-Efficient vs Augmented Split CP\n\n" + markdown_table(comparison),
            "## Undercoverage Tail Risk\n\n" + markdown_table(tail),
            "## Worst 10 Coverage Drops\n\n" + markdown_table(worst),
            "## Severity Summary\n\n" + markdown_table(severity),
            "## Fingerprint Variants\n\n" + markdown_table(fingerprint),
            "",
        ]
    )


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(map(str, headers)) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        cells = []
        for value in row:
            if isinstance(value, float):
                cells.append(f"{value:.4f}")
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
