from __future__ import annotations

import argparse
import json
from pathlib import Path


TUNING_DATASETS = [
    "ArrowHead",
    "CBF",
    "CricketX",
    "Earthquakes",
    "FaceAll",
    "Fish",
    "GunPointAgeSpan",
    "Ham",
    "MedicalImages",
    "MiddlePhalanxTW",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a fixed lambda tuning/evaluation split.")
    parser.add_argument("--input-summary", default="results/ucr35valid_5seed_alpha005_hardened/run_summary.json")
    parser.add_argument("--out-json", default="results/lambda_protocol/lambda_protocol.json")
    parser.add_argument("--out-md", default="results/lambda_protocol/LAMBDA_PROTOCOL.md")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = json.loads(Path(args.input_summary).read_text())
    all_datasets = summary["datasets"]
    tuning = [d for d in TUNING_DATASETS if d in all_datasets]
    evaluation = [d for d in all_datasets if d not in tuning]
    protocol = {
        "date": "2026-05-28",
        "purpose": "independent lambda selection and held-out alpha/Pareto evaluation",
        "all_datasets": all_datasets,
        "tuning_datasets": tuning,
        "evaluation_datasets": evaluation,
        "lambda_grid": [0.0, 0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 1.0],
        "alphas": [0.05, 0.1, 0.2],
        "selection_rule": {
            "coverage_tolerance": 0.01,
            "primary": "choose the feasible lambda with minimum average prediction-set size on tuning data",
            "feasible": "mean coverage >= 1-alpha-0.01 for every alpha on tuning data",
            "fallback": "if no lambda is feasible, minimize total coverage shortfall, then average set size",
        },
        "notes": [
            "Tuning and evaluation datasets are non-overlapping.",
            "The split is fixed before running the alpha/Pareto evaluation.",
            "This reduces but does not eliminate hyperparameter-selection risk.",
        ],
    }
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(protocol, indent=2))
    out_md.write_text(render_markdown(protocol))
    print(json.dumps(protocol, indent=2))
    print(f"Wrote {out_json} and {out_md}")


def render_markdown(protocol: dict[str, object]) -> str:
    lines = [
        "# Lambda Selection Protocol",
        "",
        f"Updated: `{protocol['date']}`",
        "",
        "## Purpose",
        "",
        str(protocol["purpose"]),
        "",
        "## Split",
        "",
        f"- Tuning datasets ({len(protocol['tuning_datasets'])}): `{', '.join(protocol['tuning_datasets'])}`",
        f"- Evaluation datasets ({len(protocol['evaluation_datasets'])}): `{', '.join(protocol['evaluation_datasets'])}`",
        "",
        "## Grid",
        "",
        f"- Lambda grid: `{protocol['lambda_grid']}`",
        f"- Alpha values: `{protocol['alphas']}`",
        "",
        "## Selection Rule",
        "",
        "- A lambda is feasible if mean coverage is at least `1-alpha-0.01` for every alpha on tuning data.",
        "- Among feasible lambdas, choose the one with the smallest average prediction-set size.",
        "- If no lambda is feasible, minimize total coverage shortfall, then average prediction-set size.",
        "",
        "## Caveat",
        "",
        "This is an independent validation protocol relative to the held-out evaluation datasets, but it is still empirical and does not provide a guarantee that the selected lambda transfers to other archives or real-world shifts.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
