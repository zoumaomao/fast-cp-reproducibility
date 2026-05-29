from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


FIG_DIR = Path("figures/paper")
FIG_DIR.mkdir(parents=True, exist_ok=True)


plt.rcParams.update(
    {
        "font.size": 10,
        "font.family": "serif",
        "axes.labelsize": 10,
        "axes.titlesize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIG_DIR / f"{name}.pdf")
    fig.savefig(FIG_DIR / f"{name}.png")
    plt.close(fig)


def main() -> None:
    comparison = pd.read_csv("results/ucr35valid_5seed_alpha005_hardened_fastcp_vs_aug.csv")
    win_loss = pd.read_csv("results/ucr35valid_5seed_alpha005_hardened_win_loss.csv")
    ablation = pd.read_csv("results/mix_ablation5_alpha005_summary.csv")
    runtime = pd.read_csv("results/runtime_summary.csv")
    lambda_pareto_path = Path("results/lambda_eval_25ds_3seed_alpha005_01_02_pareto.csv")

    fig_main_results(comparison)
    fig_mix_ablation(ablation)
    fig_win_loss(win_loss)
    fig_runtime(runtime)
    if lambda_pareto_path.exists():
        fig_lambda_pareto(pd.read_csv(lambda_pareto_path))
    write_latex_includes()
    print(f"Wrote paper figures to {FIG_DIR}")


def fig_main_results(df: pd.DataFrame) -> None:
    order = ["drift", "gap", "noise"]
    df = df.set_index("corruption").loc[order].reset_index()
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8))

    axes[0].bar(df["corruption"], df["set_size_reduction_pct"] * 100.0, color="#4C78A8")
    axes[0].axhline(0, color="black", linewidth=0.8)
    axes[0].set_ylabel("Set-size reduction (%)")
    axes[0].set_title("Efficiency gain")

    axes[1].bar(df["corruption"], df["coverage_delta"] * 100.0, color="#F58518")
    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].set_ylabel("Coverage delta (pp)")
    axes[1].set_title("Coverage change")
    for ax in axes:
        ax.set_xlabel("Corruption")
    fig.tight_layout()
    save(fig, "fig2_main_results")


def fig_mix_ablation(df: pd.DataFrame) -> None:
    rows = []
    for _, row in df.iterrows():
        method = row["method"]
        if method == "fast_cp":
            mix = 0.0
        elif method == "aug_split_cp":
            mix = 1.0
        elif method.startswith("fast_cp_mixed_"):
            mix = float(method.removeprefix("fast_cp_mixed_"))
        else:
            continue
        rows.append({**row.to_dict(), "mix": mix})
    plot_df = pd.DataFrame(rows)
    plot_df = plot_df.groupby("mix", as_index=False).agg(
        coverage=("coverage", "mean"),
        avg_set_size=("avg_set_size", "mean"),
        abs_coverage_gap=("abs_coverage_gap", "mean"),
    )

    fig, ax1 = plt.subplots(figsize=(4.8, 3.1))
    ax2 = ax1.twinx()
    ax1.plot(plot_df["mix"], plot_df["avg_set_size"], marker="o", color="#4C78A8", label="Set size")
    ax2.plot(plot_df["mix"], plot_df["abs_coverage_gap"], marker="s", color="#E45756", label="Abs. coverage gap")
    ax1.set_xlabel("Global threshold mix")
    ax1.set_ylabel("Average set size", color="#4C78A8")
    ax2.set_ylabel("Absolute coverage gap", color="#E45756")
    ax1.set_title("Local-global threshold tradeoff")
    fig.tight_layout()
    save(fig, "fig3_mix_ablation")


def fig_win_loss(df: pd.DataFrame) -> None:
    overall = df[df["dataset"] == "__OVERALL__"].iloc[0]
    labels = ["Set-size win", "Coverage close", "Abs-gap win"]
    values = [
        overall["set_size_win_rate"] * 100.0,
        overall["coverage_close_rate"] * 100.0,
        overall["abs_gap_win_rate"] * 100.0,
    ]
    fig, ax = plt.subplots(figsize=(4.7, 2.8))
    bars = ax.bar(labels, values, color=["#4C78A8", "#54A24B", "#B279A2"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Rate (%)")
    ax.set_title("Dataset/seed/corruption win rates")
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 2, f"{val:.1f}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    save(fig, "fig4_win_loss")


def fig_runtime(df: pd.DataFrame) -> None:
    keep = df[df["run"].isin(["main10_3seed_alpha005", "mix_ablation5_alpha005", "ucr35valid_5seed_alpha005_hardened"])]
    fig, ax = plt.subplots(figsize=(5.5, 2.8))
    ax.bar(keep["run"], keep["elapsed_sec"] / 60.0, color="#72B7B2")
    ax.set_ylabel("Runtime (min)")
    ax.set_title("Experiment runtime on M4 16 GB")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    save(fig, "fig5_runtime")


def fig_lambda_pareto(df: pd.DataFrame) -> None:
    plot_df = df.groupby(["alpha", "lambda"], as_index=False).agg(
        avg_set_size=("avg_set_size", "mean"),
        abs_coverage_gap=("abs_coverage_gap", "mean"),
    )
    alphas = sorted(plot_df["alpha"].unique())
    fig, axes = plt.subplots(1, len(alphas), figsize=(7.4, 2.55), sharey=True, constrained_layout=True)
    if len(alphas) == 1:
        axes = [axes]
    cmap = plt.get_cmap("viridis")

    for ax, alpha in zip(axes, alphas):
        sub = plot_df[plot_df["alpha"] == alpha].sort_values("lambda")
        colors = [cmap(v) for v in sub["lambda"]]
        ax.plot(sub["avg_set_size"], sub["abs_coverage_gap"], color="#555555", linewidth=1.0, zorder=1)
        sc = ax.scatter(
            sub["avg_set_size"],
            sub["abs_coverage_gap"],
            c=sub["lambda"],
            cmap=cmap,
            s=36,
            edgecolor="white",
            linewidth=0.5,
            zorder=2,
        )
        for key_lambda in [0.0, 0.35, 1.0]:
            row = sub[sub["lambda"].round(4) == key_lambda]
            if not row.empty:
                r = row.iloc[0]
                ax.annotate(
                    f"{key_lambda:g}",
                    (r["avg_set_size"], r["abs_coverage_gap"]),
                    textcoords="offset points",
                    xytext=(4, 4),
                    fontsize=8,
                )
        ax.set_title(rf"$\alpha={alpha:g}$")
        ax.set_xlabel("Average set size")
        ax.grid(alpha=0.18, linewidth=0.6)
    axes[0].set_ylabel("Absolute coverage gap")
    cbar = fig.colorbar(sc, ax=list(axes), shrink=0.82, pad=0.02)
    cbar.set_label(r"Global mix $\lambda$")
    save(fig, "fig6_lambda_pareto")


def write_latex_includes() -> None:
    text = r"""
% === Fig. 2: Main Results ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/paper/fig2_main_results.pdf}
    \caption{Main 10-dataset, 3-seed results at $\alpha=0.05$. FAST-CP-mixed reduces prediction-set size relative to augmented split conformal prediction across drift, gap, and noise corruptions, with small coverage changes.}
    \label{fig:main_results}
\end{figure}

% === Fig. 3: Mix Ablation ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.58\linewidth]{figures/paper/fig3_mix_ablation.pdf}
    \caption{Ablation of the local-global threshold mix on five datasets. Intermediate mixing recovers coverage relative to purely local thresholds while retaining smaller prediction sets than the global augmented threshold.}
    \label{fig:mix_ablation}
\end{figure}

% === Fig. 4: Win/Loss Summary ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.58\linewidth]{figures/paper/fig4_win_loss.pdf}
    \caption{Dataset/seed/corruption-level comparison of FAST-CP-mixed against augmented split conformal prediction.}
    \label{fig:win_loss}
\end{figure}

% === Fig. 5: Runtime ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.62\linewidth]{figures/paper/fig5_runtime.pdf}
    \caption{Runtime of the main and ablation experiments on Apple M4 16 GB.}
    \label{fig:runtime}
\end{figure}
""".strip()
    (FIG_DIR / "latex_includes.tex").write_text(text + "\n")


if __name__ == "__main__":
    main()
