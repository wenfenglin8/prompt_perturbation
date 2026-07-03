import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
DEFAULT_OUTPUT_DIR = RESULTS_DIR / "rq2_similarity_correctness"

DATASETS = {
    "exact_fact": {
        "label": "Exact-match factual QA",
        "metrics": RESULTS_DIR / "rq2_semantic_correctness_metrics.csv",
    },
    "llm_fact": {
        "label": "LLM-equivalence factual QA",
        "metrics": RESULTS_DIR / "rq2_semantic_correctness_llm_fact_metrics.csv",
    },
}

TASK_COLORS = {
    "factual_qa": "#2B6CB0",
    "math_reasoning": "#D97706",
    "code_generation": "#2F855A",
}


def load_metrics(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    numeric_fields = [
        "noise_corrected_drift",
        "raw_perturbation_drift",
        "abs_repeated_pass_rate_change",
        "harmful_correctness_drop",
    ]
    for field in numeric_fields:
        df[field] = pd.to_numeric(df[field], errors="coerce")
    df["noise_corrected_similarity"] = 1.0 - df["noise_corrected_drift"]
    df["raw_output_similarity"] = 1.0 - df["raw_perturbation_drift"]
    return df


def add_fit_line(ax, x, y, color="#222222") -> None:
    clean = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(clean) < 2 or clean["x"].nunique() < 2:
        return
    slope, intercept = pd.Series(clean["x"]).cov(clean["y"]) / clean["x"].var(), None
    intercept = clean["y"].mean() - slope * clean["x"].mean()
    x_min, x_max = clean["x"].min(), clean["x"].max()
    xs = [x_min, x_max]
    ys = [intercept + slope * value for value in xs]
    ax.plot(xs, ys, color=color, linewidth=1.8, linestyle="--", alpha=0.9)


def plot_overall_scatter(df: pd.DataFrame, label: str, key: str, output_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8.5, 5.5), constrained_layout=True)
    for task, group in df.groupby("task"):
        ax.scatter(
            group["noise_corrected_similarity"],
            group["abs_repeated_pass_rate_change"],
            s=42,
            alpha=0.72,
            color=TASK_COLORS.get(task, "#555555"),
            label=task,
            edgecolors="white",
            linewidths=0.4,
        )
    add_fit_line(ax, df["noise_corrected_similarity"], df["abs_repeated_pass_rate_change"])
    ax.set_title(f"{label}: output similarity vs correctness change", fontsize=13)
    ax.set_xlabel("Noise-corrected output similarity (1 - corrected drift)")
    ax.set_ylabel("Absolute repeated correctness change")
    ax.set_ylim(-0.02, max(0.36, df["abs_repeated_pass_rate_change"].max() + 0.04))
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    path = output_dir / f"rq2_similarity_correctness_scatter_{key}.png"
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def plot_task_facets(df: pd.DataFrame, label: str, key: str, output_dir: Path) -> Path:
    tasks = ["factual_qa", "math_reasoning", "code_generation"]
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), sharey=True, constrained_layout=True)
    fig.suptitle(f"{label}: relationship by task", fontsize=14)
    for ax, task in zip(axes, tasks):
        group = df[df["task"] == task]
        ax.scatter(
            group["noise_corrected_similarity"],
            group["abs_repeated_pass_rate_change"],
            s=44,
            alpha=0.75,
            color=TASK_COLORS.get(task, "#555555"),
            edgecolors="white",
            linewidths=0.4,
        )
        add_fit_line(ax, group["noise_corrected_similarity"], group["abs_repeated_pass_rate_change"])
        ax.set_title(task)
        ax.set_xlabel("Corrected similarity")
        ax.grid(alpha=0.25)
    axes[0].set_ylabel("Absolute repeated correctness change")
    path = output_dir / f"rq2_similarity_correctness_by_task_{key}.png"
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def plot_similarity_bins(df: pd.DataFrame, label: str, key: str, output_dir: Path) -> tuple[Path, Path]:
    binned = df.copy()
    # Quantile bins keep enough cases in each bin despite similarity values clustering near 1.
    binned["similarity_bin"] = pd.qcut(
        binned["noise_corrected_similarity"],
        q=5,
        duplicates="drop",
    )
    summary = (
        binned.groupby("similarity_bin", observed=True)
        .agg(
            mean_similarity=("noise_corrected_similarity", "mean"),
            n=("case_id", "count"),
            mean_correctness_change=("abs_repeated_pass_rate_change", "mean"),
            harmful_drop_share=("harmful_correctness_drop", "mean"),
        )
        .reset_index()
    )
    csv_path = output_dir / f"rq2_similarity_correctness_bins_{key}.csv"
    summary.to_csv(csv_path, index=False)

    fig, ax1 = plt.subplots(figsize=(8.5, 5.2), constrained_layout=True)
    ax1.plot(
        summary["mean_similarity"],
        summary["mean_correctness_change"],
        marker="o",
        linewidth=2.0,
        color="#B91C1C",
        label="Mean correctness change",
    )
    ax1.set_xlabel("Mean corrected output similarity by quantile bin")
    ax1.set_ylabel("Mean absolute repeated correctness change", color="#B91C1C")
    ax1.tick_params(axis="y", labelcolor="#B91C1C")
    ax1.grid(alpha=0.25)

    ax2 = ax1.twinx()
    ax2.plot(
        summary["mean_similarity"],
        summary["harmful_drop_share"],
        marker="s",
        linewidth=2.0,
        color="#1D4ED8",
        label="Harmful drop share",
    )
    ax2.set_ylabel("Share with harmful correctness drop", color="#1D4ED8")
    ax2.tick_params(axis="y", labelcolor="#1D4ED8")
    ax2.set_ylim(-0.02, max(0.42, summary["harmful_drop_share"].max() + 0.08))
    ax1.set_title(f"{label}: correctness outcomes by similarity bin", fontsize=13)

    path = output_dir / f"rq2_similarity_correctness_bins_{key}.png"
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return csv_path, path


def generate(key: str, config: dict, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    df = load_metrics(config["metrics"])
    paths = [
        plot_overall_scatter(df, config["label"], key, output_dir),
        plot_task_facets(df, config["label"], key, output_dir),
    ]
    paths.extend(plot_similarity_bins(df, config["label"], key, output_dir))
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    written = []
    for key, config in DATASETS.items():
        written.extend(generate(key, config, args.output_dir))

    print(f"Wrote {len(written)} files to {args.output_dir}")
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
