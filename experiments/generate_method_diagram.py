from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


OUT_DIRS = [Path("figures/paper"), Path("paper/figures")]

plt.rcParams.update(
    {
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "font.family": "DejaVu Sans",
    }
)


def box(ax, xy, wh, text, color):
    patch = FancyBboxPatch(
        xy,
        wh[0],
        wh[1],
        boxstyle="round,pad=0.02,rounding_size=0.035",
        linewidth=1.2,
        edgecolor="#2b2b2b",
        facecolor=color,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + wh[0] / 2, xy[1] + wh[1] / 2, text, ha="center", va="center", fontsize=9)


def arrow(ax, start, end):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=13,
            linewidth=1.2,
            color="#333333",
        )
    )


def main() -> None:
    for out_dir in OUT_DIRS:
        out_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    box(ax, (0.04, 0.60), (0.17, 0.22), "Test time\nseries", "#dbeafe")
    box(ax, (0.28, 0.72), (0.20, 0.18), "Compact TSC\nclassifier", "#ecfccb")
    box(ax, (0.28, 0.44), (0.20, 0.18), "Perturbation\nfingerprint", "#fef3c7")
    box(ax, (0.56, 0.64), (0.18, 0.18), "Local weighted\nthreshold", "#fce7f3")
    box(ax, (0.56, 0.36), (0.18, 0.18), "Global augmented\nthreshold", "#ede9fe")
    box(ax, (0.80, 0.50), (0.16, 0.20), "Mixed threshold\nprediction set", "#e0f2fe")

    box(ax, (0.04, 0.18), (0.17, 0.18), "Augmented\ncalibration set", "#f3f4f6")
    box(ax, (0.28, 0.18), (0.20, 0.16), "Scores +\nfingerprints", "#f3f4f6")

    arrow(ax, (0.21, 0.71), (0.28, 0.81))
    arrow(ax, (0.21, 0.67), (0.28, 0.53))
    arrow(ax, (0.48, 0.81), (0.56, 0.73))
    arrow(ax, (0.48, 0.53), (0.56, 0.70))
    arrow(ax, (0.21, 0.27), (0.28, 0.26))
    arrow(ax, (0.48, 0.26), (0.56, 0.45))
    arrow(ax, (0.74, 0.73), (0.80, 0.62))
    arrow(ax, (0.74, 0.45), (0.80, 0.58))

    ax.text(0.65, 0.58, r"$q_{\mathrm{mix}}=(1-\lambda)q_{\mathrm{local}}+\lambda q_{\mathrm{global}}$", fontsize=9, ha="center")
    ax.text(0.50, 0.05, "FAST-CP uses cheap corruption fingerprints to adapt conformal thresholds without retraining.", fontsize=9, ha="center")

    fig.tight_layout()
    for out_dir in OUT_DIRS:
        fig.savefig(out_dir / "fig1_method.pdf", dpi=300)
        fig.savefig(out_dir / "fig1_method.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
