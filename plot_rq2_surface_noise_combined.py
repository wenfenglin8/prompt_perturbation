from __future__ import annotations

import argparse
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


THREE_TASK_METRICS = RESULTS / "rq2_surface_noise_dose_response_from_kayley_5x3_metrics.csv"
LONGFACT_METRICS = RESULTS / "rq2_surface_noise_dose_response_longfact_stress_5x3_metrics.csv"

TASK_ORDER = ["factual_qa", "math_reasoning", "code_generation", "long_factual_qa"]
TASK_LABELS = {
    "factual_qa": "Factual QA",
    "math_reasoning": "Math",
    "code_generation": "Code",
    "long_factual_qa": "LongFactQA",
}
TASK_COLORS = {
    "factual_qa": "#2F80ED",
    "math_reasoning": "#F2994A",
    "code_generation": "#27AE60",
    "long_factual_qa": "#9B51E0",
}


def numericize(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if col not in {"base_case_id", "task", "dataset", "perturbation_family", "cohort", "source_file"}:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_metrics(metrics_paths: list[Path] | None = None) -> tuple[pd.DataFrame, list[Path]]:
    if metrics_paths:
        resolved = [path.resolve() for path in metrics_paths]
        frames = []
        for path in resolved:
            frame = pd.read_csv(path)
            frame["source_file"] = path.name
            frames.append(frame)
        return numericize(pd.concat(frames, ignore_index=True)), resolved
    three = pd.read_csv(THREE_TASK_METRICS)
    three["cohort"] = "three_task"
    longfact = pd.read_csv(LONGFACT_METRICS)
    longfact["cohort"] = "longfact_stress"
    df = pd.concat([three, longfact], ignore_index=True)
    return numericize(df), [THREE_TASK_METRICS, LONGFACT_METRICS]


def summarize_by_level(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["strength_level", "strength_edits"], as_index=False)
        .agg(
            n=("base_case_id", "size"),
            mean_cross_similarity=("mean_cross_similarity", "mean"),
            mean_paired_similarity=("mean_paired_similarity", "mean"),
            mean_raw_perturbation_drift=("raw_perturbation_drift", "mean"),
            mean_noise_corrected_drift=("noise_corrected_drift", "mean"),
            mean_clean_correctness=("clean_mean_correctness", "mean"),
            mean_perturbed_correctness=("perturbed_mean_correctness", "mean"),
            mean_abs_repeated_pass_rate_change=("abs_repeated_pass_rate_change", "mean"),
            mean_repeated_pass_rate_drop=("repeated_pass_rate_drop", "mean"),
            share_harmful_correctness_drop=("harmful_correctness_drop", "mean"),
            share_correctness_changed=("correctness_changed", "mean"),
        )
        .sort_values("strength_level")
    )


def summarize_by_task_level(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["task", "strength_level", "strength_edits"], as_index=False)
        .agg(
            n=("base_case_id", "size"),
            mean_cross_similarity=("mean_cross_similarity", "mean"),
            mean_noise_corrected_drift=("noise_corrected_drift", "mean"),
            mean_abs_repeated_pass_rate_change=("abs_repeated_pass_rate_change", "mean"),
            mean_repeated_pass_rate_drop=("repeated_pass_rate_drop", "mean"),
            share_harmful_correctness_drop=("harmful_correctness_drop", "mean"),
            share_correctness_changed=("correctness_changed", "mean"),
        )
        .sort_values(["task", "strength_level"])
    )


def corr_stats(df: pd.DataFrame) -> dict[str, float]:
    nonzero = df[df["strength_edits"] > 0]
    return {
        "all_strength_similarity_spearman": df["strength_edits"].corr(
            df["mean_cross_similarity"], method="spearman"
        ),
        "all_strength_correctness_spearman": df["strength_edits"].corr(
            df["abs_repeated_pass_rate_change"], method="spearman"
        ),
        "nonzero_similarity_correctness_spearman": nonzero["mean_cross_similarity"].corr(
            nonzero["abs_repeated_pass_rate_change"], method="spearman"
        ),
        "nonzero_corrected_drift_correctness_spearman": nonzero[
            "noise_corrected_drift"
        ].corr(nonzero["abs_repeated_pass_rate_change"], method="spearman"),
    }


def savefig(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_overall(by_level: pd.DataFrame, tag: str) -> None:
    x = by_level["strength_edits"].to_numpy()
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 7.2), sharex=True)
    specs = [
        ("mean_cross_similarity", "Mean cross similarity", "#2F80ED"),
        ("mean_abs_repeated_pass_rate_change", "Abs correctness change", "#D1495B"),
        ("mean_noise_corrected_drift", "Noise-corrected drift", "#40798C"),
        ("share_harmful_correctness_drop", "Harmful drop share", "#8E44AD"),
    ]
    for ax, (col, ylabel, color) in zip(axes.ravel(), specs):
        ax.plot(x, by_level[col], marker="o", linewidth=2.0, color=color)
        for row in by_level.itertuples():
            ax.annotate(
                f"n={int(row.n)}",
                (row.strength_edits, getattr(row, col)),
                xytext=(0, 7),
                textcoords="offset points",
                ha="center",
                fontsize=8,
                color="#333333",
            )
        ax.set_ylabel(ylabel)
        ax.margins(y=0.12)
        ax.grid(True, alpha=0.24)
    for ax in axes[-1]:
        ax.set_xlabel("Surface-noise strength: corrupted instruction words")
    fig.suptitle("RQ2 Surface Noise Combined: Three Tasks + LongFactQA", y=1.02, fontsize=13)
    savefig(fig, f"{tag}_overall_dose_response.png")


def plot_task_lines(by_task: pd.DataFrame, value_col: str, ylabel: str, name: str) -> None:
    fig, ax = plt.subplots(figsize=(8.8, 5.3))
    for task in TASK_ORDER:
        part = by_task[by_task["task"] == task].sort_values("strength_level")
        if part.empty:
            continue
        ax.plot(
            part["strength_edits"],
            part[value_col],
            marker="o",
            linewidth=2.0,
            color=TASK_COLORS[task],
            label=TASK_LABELS[task],
        )
    ax.set_xlabel("Surface-noise strength: corrupted instruction words")
    ax.set_ylabel(ylabel)
    ax.set_title("RQ2 Surface Noise Combined by Task")
    ax.grid(True, alpha=0.24)
    ax.legend(frameon=False, ncol=2)
    savefig(fig, name)


def add_regression(ax: plt.Axes, x: pd.Series, y: pd.Series) -> None:
    clean = pd.DataFrame({"x": x, "y": y}).replace([np.inf, -np.inf], np.nan).dropna()
    if len(clean) < 2 or clean["x"].nunique() < 2:
        return
    coef = np.polyfit(clean["x"], clean["y"], 1)
    xs = np.linspace(clean["x"].min(), clean["x"].max(), 100)
    ax.plot(xs, coef[0] * xs + coef[1], color="#111111", linewidth=1.6, alpha=0.8)


def plot_scatter(df: pd.DataFrame, x_col: str, xlabel: str, name: str) -> None:
    nonzero = df[df["strength_edits"] > 0].copy()
    fig, ax = plt.subplots(figsize=(8.4, 5.5))
    for task in TASK_ORDER:
        part = nonzero[nonzero["task"] == task]
        if part.empty:
            continue
        ax.scatter(
            part[x_col],
            part["abs_repeated_pass_rate_change"],
            s=52,
            alpha=0.76,
            color=TASK_COLORS[task],
            edgecolor="white",
            linewidth=0.6,
            label=TASK_LABELS[task],
        )
    add_regression(ax, nonzero[x_col], nonzero["abs_repeated_pass_rate_change"])
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Absolute repeated pass-rate change")
    ax.set_title("Surface Noise Combined: Case-Level Nonzero Strengths")
    ax.grid(True, alpha=0.24)
    ax.legend(frameon=False, ncol=2)
    savefig(fig, name)


def write_index(
    df: pd.DataFrame,
    by_level: pd.DataFrame,
    stats: dict[str, float],
    tag: str,
    source_paths: list[Path],
) -> None:
    path = OUT / f"{tag}_visualization_index.md"
    task_counts = df.groupby("task")["base_case_id"].nunique().to_dict()
    present_tasks = [task for task in TASK_ORDER if task in set(df["task"])]
    levels = ", ".join(str(int(x)) for x in sorted(df["strength_edits"].dropna().unique()))
    if {"version", "sample_idx"}.issubset(df.columns):
        samples = str(int(df.groupby(["base_case_id", "strength_edits", "version"])["sample_idx"].nunique().max()))
    else:
        samples = "NA; see source experiment summary/report"
    lines = [
        "# RQ2 Surface Noise Combined Visualizations",
        "",
        "Source files:",
        "",
        *[f"- `{path.resolve().relative_to(ROOT)}`" for path in source_paths],
        "",
        "Design:",
        "",
        "- Perturbation family: `surface_noise`",
        f"- Tasks: `{', '.join(present_tasks)}`",
        f"- Cases per task: `{task_counts}`",
        f"- Samples per prompt version: `{samples}`",
        f"- Strength levels: `{levels}` corrupted instruction words",
        f"- Combined case-level rows: `{len(df)}`",
        "",
        "Generated files:",
        "",
        f"- `{tag}_by_level.csv`",
        f"- `{tag}_by_task_level.csv`",
        f"- `{tag}_overall_dose_response.png`",
        f"- `{tag}_similarity_by_task.png`",
        f"- `{tag}_correctness_change_by_task.png`",
        f"- `{tag}_similarity_vs_correctness_scatter.png`",
        f"- `{tag}_corrected_drift_vs_correctness_scatter.png`",
        "",
        "Key statistics:",
        "",
        f"- Strength vs mean cross similarity, Spearman: `{stats['all_strength_similarity_spearman']:.4f}`",
        f"- Strength vs absolute repeated-pass-rate change, Spearman: `{stats['all_strength_correctness_spearman']:.4f}`",
        f"- Nonzero-level similarity vs absolute correctness change, Spearman: `{stats['nonzero_similarity_correctness_spearman']:.4f}`",
        f"- Nonzero-level corrected drift vs absolute correctness change, Spearman: `{stats['nonzero_corrected_drift_correctness_spearman']:.4f}`",
        "",
        "Combined mean by strength:",
        "",
        by_level[
            [
                "strength_edits",
                "n",
                "mean_cross_similarity",
                "mean_noise_corrected_drift",
                "mean_abs_repeated_pass_rate_change",
                "share_harmful_correctness_drop",
                "share_correctness_changed",
            ]
        ].to_markdown(index=False, floatfmt=".4f"),
        "",
        "Interpretation:",
        "",
        "Combining LongFactQA with the three-task result keeps the expected surface-noise similarity trend: stronger surface noise lowers output similarity. The correctness movement remains modest and task-dependent, so this combined result is best treated as a contrast condition rather than the strongest RQ2 dose-response evidence.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", type=Path, nargs="+", default=None)
    parser.add_argument("--tag", default="rq2_surface_noise_combined")
    args = parser.parse_args()

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
    df, source_paths = load_metrics(args.metrics)
    by_level = summarize_by_level(df)
    by_task = summarize_by_task_level(df)
    OUT.mkdir(parents=True, exist_ok=True)
    by_level.to_csv(OUT / f"{args.tag}_by_level.csv", index=False)
    by_task.to_csv(OUT / f"{args.tag}_by_task_level.csv", index=False)

    plot_overall(by_level, args.tag)
    plot_task_lines(
        by_task,
        "mean_cross_similarity",
        "Mean cross similarity",
        f"{args.tag}_similarity_by_task.png",
    )
    plot_task_lines(
        by_task,
        "mean_abs_repeated_pass_rate_change",
        "Mean absolute repeated pass-rate change",
        f"{args.tag}_correctness_change_by_task.png",
    )
    plot_scatter(
        df,
        "mean_cross_similarity",
        "Mean cross similarity",
        f"{args.tag}_similarity_vs_correctness_scatter.png",
    )
    plot_scatter(
        df,
        "noise_corrected_drift",
        "Noise-corrected semantic drift",
        f"{args.tag}_corrected_drift_vs_correctness_scatter.png",
    )
    write_index(df, by_level, corr_stats(df), args.tag, source_paths)
    print(f"Saved combined surface-noise figures to: {OUT}")


if __name__ == "__main__":
    main()
