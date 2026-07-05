from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
OUT = RESULTS / "rq2_figures"
os.environ.setdefault("MPLCONFIGDIR", str(RESULTS / ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


TAG = "rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16"
METRICS = [RESULTS / f"{TAG}_batch{i}of5_metrics.csv" for i in range(1, 6)]


def load_code_nonzero() -> pd.DataFrame:
    df = pd.concat([pd.read_csv(path) for path in METRICS], ignore_index=True)
    code = df[(df["task"] == "code_generation") & (df["strength_edits"] > 0)].copy()
    code["direction"] = np.select(
        [
            code["repeated_pass_rate_drop"] > 0,
            code["repeated_pass_rate_drop"] < 0,
        ],
        [
            "Harmful drop",
            "Improved under perturbation",
        ],
        default="Unchanged",
    )
    return code


def savefig(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight")
    plt.close(fig)


def add_regression(ax: plt.Axes, x: pd.Series, y: pd.Series) -> None:
    clean = pd.DataFrame({"x": x, "y": y}).replace([np.inf, -np.inf], np.nan).dropna()
    if len(clean) < 2 or clean["x"].nunique() < 2:
        return
    coef = np.polyfit(clean["x"], clean["y"], 1)
    xs = np.linspace(clean["x"].min(), clean["x"].max(), 120)
    ax.plot(xs, coef[0] * xs + coef[1], color="#111111", linewidth=1.8, alpha=0.78, label="Linear trend")


def plot_direction_scatter(code: pd.DataFrame) -> None:
    colors = {
        "Harmful drop": "#D1495B",
        "Improved under perturbation": "#2A9D8F",
        "Unchanged": "#7A8793",
    }
    markers = {2: "o", 4: "s", 8: "^", 16: "D"}
    rho = code["mean_cross_similarity"].corr(
        code["abs_repeated_pass_rate_change"],
        method="spearman",
    )

    fig, ax = plt.subplots(figsize=(8.8, 5.7))
    for direction, part in code.groupby("direction"):
        for strength, sub in part.groupby("strength_edits"):
            ax.scatter(
                sub["mean_cross_similarity"],
                sub["abs_repeated_pass_rate_change"],
                s=54,
                alpha=0.74,
                color=colors[direction],
                marker=markers.get(int(strength), "o"),
                edgecolor="white",
                linewidth=0.55,
                label=f"{direction}, edits={int(strength)}",
            )

    add_regression(ax, code["mean_cross_similarity"], code["abs_repeated_pass_rate_change"])
    ax.text(
        0.02,
        0.96,
        f"Spearman rho = {rho:.4f}\nn = {len(code)} nonzero code rows",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=10,
        bbox={"boxstyle": "round,pad=0.28", "fc": "white", "ec": "#CCCCCC", "alpha": 0.9},
    )
    ax.set_title("Code Generation: Similarity vs Correctness Change under Surface Noise")
    ax.set_xlabel("Mean cross similarity")
    ax.set_ylabel("Absolute repeated pass-rate change")
    ax.grid(True, alpha=0.24)
    handles, labels = ax.get_legend_handles_labels()
    trend = [(h, l) for h, l in zip(handles, labels) if l == "Linear trend"]
    point_items = [(h, l) for h, l in zip(handles, labels) if l != "Linear trend"]
    direction_handles = []
    direction_labels = []
    seen = set()
    for handle, label in point_items:
        direction = label.split(", edits=")[0]
        if direction not in seen:
            seen.add(direction)
            direction_handles.append(handle)
            direction_labels.append(direction)
    if trend:
        direction_handles.extend([trend[0][0]])
        direction_labels.extend([trend[0][1]])
    ax.legend(direction_handles, direction_labels, frameon=False, loc="upper right")
    savefig(fig, f"{TAG}_code_only_similarity_vs_correctness_direction.png")


def plot_binned_trend(code: pd.DataFrame) -> None:
    clean = code[["mean_cross_similarity", "abs_repeated_pass_rate_change"]].dropna().copy()
    clean["similarity_bin"] = pd.qcut(clean["mean_cross_similarity"], q=6, duplicates="drop")
    grouped = (
        clean.groupby("similarity_bin", observed=True)
        .agg(
            mean_similarity=("mean_cross_similarity", "mean"),
            mean_abs_change=("abs_repeated_pass_rate_change", "mean"),
            std_abs_change=("abs_repeated_pass_rate_change", "std"),
            n=("abs_repeated_pass_rate_change", "size"),
        )
        .reset_index(drop=True)
    )
    grouped["se"] = grouped["std_abs_change"].fillna(0.0) / np.sqrt(grouped["n"])
    grouped.to_csv(OUT / f"{TAG}_code_only_similarity_bins.csv", index=False)

    fig, ax = plt.subplots(figsize=(7.8, 5.1))
    ax.errorbar(
        grouped["mean_similarity"],
        grouped["mean_abs_change"],
        yerr=grouped["se"],
        marker="o",
        linewidth=2.0,
        capsize=4,
        color="#40798C",
    )
    for row in grouped.itertuples():
        ax.annotate(
            f"n={int(row.n)}",
            (row.mean_similarity, row.mean_abs_change),
            xytext=(0, 7),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            color="#333333",
        )
    ax.invert_xaxis()
    ax.set_title("Code Generation: Correctness Movement by Similarity Bin")
    ax.set_xlabel("Mean cross similarity bin average (lower similarity to the right)")
    ax.set_ylabel("Mean absolute repeated pass-rate change")
    ax.grid(True, alpha=0.24)
    savefig(fig, f"{TAG}_code_only_similarity_bin_trend.png")


def main() -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )
    code = load_code_nonzero()
    plot_direction_scatter(code)
    plot_binned_trend(code)
    print(f"Saved code-only figures to: {OUT}")


if __name__ == "__main__":
    main()
