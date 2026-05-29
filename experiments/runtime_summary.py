from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize FAST-CP experiment runtimes.")
    parser.add_argument("--summaries", nargs="+", default=[
        "results/smoke/run_summary.json",
        "results/pilot5/run_summary.json",
        "results/pilot5_mixed/run_summary.json",
        "results/main10_small_alpha005/run_summary.json",
        "results/mix_ablation5_alpha005/run_summary.json",
        "results/main10_3seed_alpha005/run_summary.json",
        "results/ucr35valid_5seed_alpha005_hardened/run_summary.json",
        "results/lambda_tuning_10ds_3seed_alpha005_01_02/run_summary.json",
        "results/lambda_eval_25ds_3seed_alpha005_01_02/run_summary.json",
        "results/minirocket15_3seed_alpha005_01/run_summary.json",
    ])
    parser.add_argument("--out", default="results/runtime_summary.csv")
    parser.add_argument("--latex-out", default="results/runtime_summary.tex")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = []
    for path_str in args.summaries:
        path = Path(path_str)
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        n_datasets = len(data.get("datasets", []))
        n_seeds = len(data.get("seeds", []))
        n_corruptions = len(data.get("corruptions", []))
        n_alphas = len(data.get("alphas", []))
        rows.append(
            {
                "run": path.parent.name,
                "datasets": n_datasets,
                "seeds": n_seeds,
                "corruptions": n_corruptions,
                "alphas": n_alphas,
                "rows": data.get("rows"),
                "elapsed_sec": data.get("elapsed_sec"),
                "sec_per_dataset_seed": data.get("elapsed_sec") / max(1, n_datasets * n_seeds),
                "result_path": data.get("result_path"),
            }
        )
    df = pd.DataFrame(rows)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)

    latex_df = df.copy()
    latex_df["elapsed_min"] = latex_df["elapsed_sec"] / 60.0
    latex_df["sec_per_dataset_seed"] = latex_df["sec_per_dataset_seed"].map(lambda x: f"{x:.1f}")
    latex_df["elapsed_min"] = latex_df["elapsed_min"].map(lambda x: f"{x:.2f}")
    latex_df = latex_df[["run", "datasets", "seeds", "corruptions", "alphas", "rows", "elapsed_min", "sec_per_dataset_seed"]]
    latex = _latex_table(latex_df)
    Path(args.latex_out).write_text(latex)
    print(df.to_string(index=False))
    print(f"\nWrote {out} and {args.latex_out}")


def _latex_table(df: pd.DataFrame) -> str:
    header = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\caption{Runtime summary on Apple M4 16 GB. Times include dataset loading, feature extraction, model fitting, corruption generation, and conformal evaluation.}",
        r"\label{tab:runtime_summary}",
        r"\begin{tabular}{lrrrrrrr}",
        r"\toprule",
        r"Run & Datasets & Seeds & Corrupt. & $\alpha$ & Rows & Min. & Sec./ds-seed \\",
        r"\midrule",
    ]
    rows = []
    for _, row in df.iterrows():
        run = _display_run_name(str(row["run"])).replace("_", r"\_")
        rows.append(
            f"{run} & {row['datasets']} & {row['seeds']} & {row['corruptions']} & "
            f"{row['alphas']} & {row['rows']} & {row['elapsed_min']} & {row['sec_per_dataset_seed']} \\\\"
        )
    footer = [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(header + rows + footer) + "\n"


def _display_run_name(run: str) -> str:
    names = {
        "main10_small_alpha005": "main10",
        "mix_ablation5_alpha005": "mix_ablation5",
        "main10_3seed_alpha005": "main10_3seed",
        "ucr35valid_5seed_alpha005_hardened": "ucr35_5seed",
        "lambda_tuning_10ds_3seed_alpha005_01_02": "lambda_tune10",
        "lambda_eval_25ds_3seed_alpha005_01_02": "lambda_eval25",
        "minirocket15_3seed_alpha005_01": "minirocket15",
    }
    return names.get(run, run)


if __name__ == "__main__":
    main()
