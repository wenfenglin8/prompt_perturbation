from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
OUT_DIR = RESULTS_DIR / "rq1_figures"
METRICS_PATH = RESULTS_DIR / "rq1_recomputed" / "rq1_pdr_50x5_recomputed_v2_metrics.csv"

TASK_ORDER = ["factual_qa", "math_reasoning", "code_generation"]
TASK_LABELS = {
    "factual_qa": "Factual QA",
    "math_reasoning": "Math reasoning",
    "code_generation": "Code generation",
}
PERTURBATION_ORDER = [
    "paraphrase",
    "reordering",
    "formatting",
    "context_injection",
    "surface_noise",
]
PERTURBATION_LABELS = {
    "paraphrase": "Paraphrase",
    "reordering": "Reordering",
    "formatting": "Formatting",
    "context_injection": "Context injection",
    "surface_noise": "Surface noise",
}
TASK_COLORS = {
    "factual_qa": "#2B6CB0",
    "math_reasoning": "#B7791F",
    "code_generation": "#2F855A",
}


def load_metrics() -> pd.DataFrame:
    df = pd.read_csv(METRICS_PATH)
    numeric_cols = [
        "clean_single_correct",
        "perturbed_single_correct",
        "clean_mean_correctness",
        "perturbed_mean_correctness",
        "uncorrected_pdr_loss",
        "perturbed_pdr_loss",
        "corrected_pdr",
        "correctness_sample_noise",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def summarize(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    grouped = (
        df.groupby(["perturbation", "task"], as_index=False)
        .agg(
            n=("case_id", "count"),
            clean_repeated=("clean_mean_correctness", "mean"),
            perturbed_repeated=("perturbed_mean_correctness", "mean"),
            clean_baseline_loss=("uncorrected_pdr_loss", "mean"),
            perturbed_loss=("perturbed_pdr_loss", "mean"),
            corrected_pdr=("corrected_pdr", "mean"),
            sample_noise=("correctness_sample_noise", "mean"),
        )
    )
    task_summary = (
        df.groupby("task", as_index=False)
        .agg(
            n=("case_id", "count"),
            clean_repeated=("clean_mean_correctness", "mean"),
            perturbed_repeated=("perturbed_mean_correctness", "mean"),
            clean_baseline_loss=("uncorrected_pdr_loss", "mean"),
            perturbed_loss=("perturbed_pdr_loss", "mean"),
            corrected_pdr=("corrected_pdr", "mean"),
            sample_noise=("correctness_sample_noise", "mean"),
        )
    )
    grouped["corrected_pdr_pp"] = grouped["corrected_pdr"] * 100
    task_summary["clean_baseline_loss_pp"] = task_summary["clean_baseline_loss"] * 100
    task_summary["corrected_pdr_pp"] = task_summary["corrected_pdr"] * 100
    return grouped, task_summary


def make_heatmap_values(grouped: pd.DataFrame) -> pd.DataFrame:
    heat = grouped.pivot(index="perturbation", columns="task", values="corrected_pdr_pp")
    heat = heat.loc[PERTURBATION_ORDER, TASK_ORDER]
    return heat


def rank_labels(heat: pd.DataFrame) -> dict[tuple[str, str], str]:
    labels: dict[tuple[str, str], str] = {}
    for task in TASK_ORDER:
        values = heat[task].sort_values(ascending=False)
        for rank, perturbation in enumerate(values.index, start=1):
            labels[(perturbation, task)] = f"#{rank}"
    return labels


def make_main_figure(grouped: pd.DataFrame, task_summary: pd.DataFrame) -> tuple[Path, Path, Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    heat = make_heatmap_values(grouped)
    ranks = rank_labels(heat)

    fig = plt.figure(figsize=(12.8, 6.4), constrained_layout=True)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1.0])

    ax = fig.add_subplot(gs[0, 0])
    max_abs = float(np.nanmax(np.abs(heat.to_numpy())))
    norm = TwoSlopeNorm(vmin=-max_abs, vcenter=0, vmax=max_abs)
    im = ax.imshow(heat.to_numpy(), cmap="RdBu_r", norm=norm, aspect="auto")

    ax.set_title("A. Corrected PDR by task and perturbation", fontsize=12, pad=10)
    ax.set_xticks(range(len(TASK_ORDER)))
    ax.set_xticklabels([TASK_LABELS[t] for t in TASK_ORDER], rotation=20, ha="right")
    ax.set_yticks(range(len(PERTURBATION_ORDER)))
    ax.set_yticklabels([PERTURBATION_LABELS[p] for p in PERTURBATION_ORDER])
    ax.tick_params(length=0)

    for i, perturbation in enumerate(PERTURBATION_ORDER):
        for j, task in enumerate(TASK_ORDER):
            value = float(heat.loc[perturbation, task])
            display_value = 0.0 if abs(value) < 0.005 else value
            color = "white" if abs(value) > max_abs * 0.55 else "#1A202C"
            ax.text(
                j,
                i,
                f"{display_value:+.2f} pp\n{ranks[(perturbation, task)]}",
                ha="center",
                va="center",
                fontsize=9,
                color=color,
            )

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cbar.set_label("Corrected PDR, percentage points")

    ax = fig.add_subplot(gs[0, 1])
    task_summary = task_summary.set_index("task").loc[TASK_ORDER].reset_index()
    x = np.arange(len(TASK_ORDER))
    width = 0.34
    baseline = task_summary["clean_baseline_loss_pp"].to_numpy()
    induced = task_summary["corrected_pdr_pp"].to_numpy()
    bars1 = ax.bar(
        x - width / 2,
        baseline,
        width=width,
        color="#718096",
        alpha=0.82,
        label="Clean baseline loss",
    )
    bars2 = ax.bar(
        x + width / 2,
        induced,
        width=width,
        color="#4A5568",
        alpha=0.85,
        label="Perturbation-induced loss",
    )
    ax.axhline(0, color="#222222", linewidth=0.9)
    ax.set_title("B. Baseline loss vs perturbation-induced loss", fontsize=12, pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels([TASK_LABELS[t] for t in TASK_ORDER], rotation=20, ha="right")
    ax.set_ylabel("Loss, percentage points")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, loc="upper right")

    ymax = max(float(np.nanmax(baseline)), float(np.nanmax(np.abs(induced)))) + 2.0
    ax.set_ylim(min(-1.0, float(np.nanmin(induced)) - 1.0), ymax)
    for bars in (bars1, bars2):
        for bar in bars:
            value = bar.get_height()
            y = value + 0.25 if value >= 0 else value - 0.25
            va = "bottom" if value >= 0 else "top"
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                y,
                f"{value:.2f}",
                ha="center",
                va=va,
                fontsize=9,
            )

    fig.suptitle(
        "RQ1 repaired PDR results: perturbation ranking is task-dependent",
        fontsize=14,
    )

    png = OUT_DIR / "rq1_pdr_recomputed_v2_task_dependent_ranking.png"
    pdf = OUT_DIR / "rq1_pdr_recomputed_v2_task_dependent_ranking.pdf"
    fig.savefig(png, dpi=300)
    fig.savefig(pdf)
    plt.close(fig)

    grouped_path = OUT_DIR / "rq1_pdr_recomputed_v2_grouped_for_paper.csv"
    grouped.to_csv(grouped_path, index=False)
    return png, pdf, grouped_path


def make_bar_figure(grouped: pd.DataFrame) -> tuple[Path, Path]:
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.2), sharey=True, constrained_layout=True)
    y_min = min(-1.6, grouped["corrected_pdr_pp"].min() - 0.8)
    y_max = max(2.8, grouped["corrected_pdr_pp"].max() + 0.8)
    for ax, task in zip(axes, TASK_ORDER):
        subset = (
            grouped[grouped["task"] == task]
            .set_index("perturbation")
            .loc[PERTURBATION_ORDER]
            .reset_index()
        )
        values = subset["corrected_pdr_pp"].to_numpy()
        colors = ["#C53030" if v > 0 else "#2B6CB0" if v < 0 else "#718096" for v in values]
        bars = ax.bar(range(len(PERTURBATION_ORDER)), values, color=colors, alpha=0.88)
        ax.axhline(0, color="#222222", linewidth=0.9)
        ax.set_title(TASK_LABELS[task], fontsize=12)
        ax.set_xticks(range(len(PERTURBATION_ORDER)))
        ax.set_xticklabels([PERTURBATION_LABELS[p] for p in PERTURBATION_ORDER], rotation=35, ha="right")
        ax.set_ylim(y_min, y_max)
        ax.grid(axis="y", alpha=0.25)
        for bar, value in zip(bars, values):
            display_value = 0.0 if abs(value) < 0.005 else value
            y = value + 0.12 if value >= 0 else value - 0.12
            va = "bottom" if value >= 0 else "top"
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                y,
                f"{display_value:+.2f}",
                ha="center",
                va=va,
                fontsize=8,
            )
    axes[0].set_ylabel("Corrected PDR, percentage points")
    fig.suptitle("Corrected PDR by perturbation within each task", fontsize=14)
    png = OUT_DIR / "rq1_pdr_recomputed_v2_corrected_pdr_by_task_bars.png"
    pdf = OUT_DIR / "rq1_pdr_recomputed_v2_corrected_pdr_by_task_bars.pdf"
    fig.savefig(png, dpi=300)
    fig.savefig(pdf)
    plt.close(fig)
    return png, pdf


def write_caption(grouped: pd.DataFrame, task_summary: pd.DataFrame, paths: dict[str, Path]) -> Path:
    overall_clean = task_summary["clean_repeated"].mean()
    overall_perturbed = task_summary["perturbed_repeated"].mean()
    overall_corrected = task_summary["corrected_pdr"].mean()

    factual = grouped[(grouped["task"] == "factual_qa")].set_index("perturbation")["corrected_pdr"]
    math = grouped[(grouped["task"] == "math_reasoning")].set_index("perturbation")["corrected_pdr"]
    code = grouped[(grouped["task"] == "code_generation")].set_index("perturbation")["corrected_pdr"]

    lines = [
        "# RQ1 Recomputed V2 PDR Figure Caption",
        "",
        "Suggested caption:",
        "",
        (
            "Figure X. Repaired PDR analysis for RQ1, excluding open-ended writing. "
            "Panel A reports corrected PDR by perturbation type and objective task, in percentage points; "
            "cell labels show the corrected PDR value and the within-task harmfulness rank. "
            "Panel B decomposes total perturbed loss into clean-prompt baseline loss and the additional "
            "perturbation-induced loss. After repairing the math and code evaluators, clean repeated "
            f"performance is {overall_clean:.4f} and perturbed repeated performance is {overall_perturbed:.4f}, "
            f"yielding a small aggregate corrected PDR of {overall_corrected:.4f}. "
            "The perturbation ranking is task-dependent: paraphrasing is consistently harmful, but reordering "
            "is most harmful for math reasoning while near-neutral or beneficial for the other tasks."
        ),
        "",
        "Values to mention in text:",
        "",
        f"- Factual QA highest corrected PDR: paraphrase `{factual.idxmax()}` = `{factual.max():.4f}`.",
        f"- Math reasoning highest corrected PDR: reordering = `{math['reordering']:.4f}`.",
        f"- Code generation highest corrected PDR: paraphrase = `{code['paraphrase']:.4f}`.",
        f"- Aggregate corrected PDR: `{overall_corrected:.4f}`.",
        "",
        "Files:",
        "",
    ]
    for label, path in paths.items():
        lines.append(f"- {label}: `{path.as_posix()}`")

    caption_path = OUT_DIR / "rq1_pdr_recomputed_v2_paper_figure_caption.md"
    caption_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return caption_path


def main() -> None:
    df = load_metrics()
    grouped, task_summary = summarize(df)
    main_png, main_pdf, grouped_path = make_main_figure(grouped, task_summary)
    bars_png, bars_pdf = make_bar_figure(grouped)
    caption = write_caption(
        grouped,
        task_summary,
        {
            "main_png": main_png,
            "main_pdf": main_pdf,
            "bar_png": bars_png,
            "bar_pdf": bars_pdf,
            "grouped_csv": grouped_path,
        },
    )
    print(f"Main PNG: {main_png}")
    print(f"Main PDF: {main_pdf}")
    print(f"Bar PNG: {bars_png}")
    print(f"Bar PDF: {bars_pdf}")
    print(f"Caption: {caption}")


if __name__ == "__main__":
    main()
