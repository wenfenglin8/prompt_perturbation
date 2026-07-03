import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
DEFAULT_OUTPUT_DIR = RESULTS_DIR / "rq2_heatmaps"

TASK_ORDER = ["factual_qa", "math_reasoning", "code_generation"]
PERTURBATION_ORDER = [
    "paraphrase",
    "formatting",
    "reordering",
    "context_injection",
    "surface_noise",
]


DATASETS = {
    "exact_fact": {
        "label": "Exact-match factual QA",
        "grouped": RESULTS_DIR / "rq2_semantic_correctness_grouped.csv",
        "correlations": RESULTS_DIR / "rq2_semantic_correctness_correlations.csv",
    },
    "llm_fact": {
        "label": "LLM-equivalence factual QA",
        "grouped": RESULTS_DIR / "rq2_semantic_correctness_llm_fact_grouped.csv",
        "correlations": RESULTS_DIR / "rq2_semantic_correctness_llm_fact_correlations.csv",
    },
}


GROUPED_HEATMAPS = [
    {
        "field": "mean_noise_corrected_drift",
        "title": "Mean noise-corrected semantic drift",
        "filename": "mean_corrected_drift",
        "cmap": "YlGnBu",
        "fmt": ".3f",
        "vmin": 0.0,
        "vmax": None,
    },
    {
        "field": "mean_abs_repeated_pass_rate_change",
        "title": "Mean absolute repeated correctness change",
        "filename": "mean_abs_correctness_change",
        "cmap": "YlOrRd",
        "fmt": ".2f",
        "vmin": 0.0,
        "vmax": None,
    },
    {
        "field": "share_harmful_correctness_drop",
        "title": "Share with harmful correctness drop",
        "filename": "harmful_drop_share",
        "cmap": "OrRd",
        "fmt": ".2f",
        "vmin": 0.0,
        "vmax": 1.0,
    },
    {
        "field": "share_correctness_changed",
        "title": "Share with any correctness change",
        "filename": "correctness_changed_share",
        "cmap": "PuBuGn",
        "fmt": ".2f",
        "vmin": 0.0,
        "vmax": 1.0,
    },
]


CORRELATION_HEATMAPS = [
    {
        "relationship": "primary",
        "value": "spearman",
        "title": "Spearman: corrected drift vs correctness change",
        "filename": "spearman_corrected_vs_correctness_change",
        "cmap": "RdBu_r",
        "fmt": ".2f",
    },
    {
        "relationship": "harmful_drop_binary",
        "value": "spearman",
        "title": "Spearman: corrected drift vs harmful drop",
        "filename": "spearman_corrected_vs_harmful_drop",
        "cmap": "RdBu_r",
        "fmt": ".2f",
    },
]


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def matrix_from_grouped(df: pd.DataFrame, field: str) -> pd.DataFrame:
    pivot = df.pivot(index="task", columns="perturbation", values=field)
    return pivot.reindex(index=TASK_ORDER, columns=PERTURBATION_ORDER)


def matrix_from_correlations(df: pd.DataFrame, relationship: str, value: str) -> pd.DataFrame:
    rows = df[
        (df["scope_type"] == "task_perturbation")
        & (df["relationship"] == relationship)
    ].copy()
    split = rows["scope_value"].str.split(":", n=1, expand=True)
    rows["task"] = split[0]
    rows["perturbation"] = split[1]
    rows[value] = pd.to_numeric(rows[value], errors="coerce")
    pivot = rows.pivot(index="task", columns="perturbation", values=value)
    return pivot.reindex(index=TASK_ORDER, columns=PERTURBATION_ORDER)


def write_matrix_csv(path: Path, matrix: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    matrix.to_csv(path, quoting=csv.QUOTE_MINIMAL)


def annotate_heatmap(ax, matrix: pd.DataFrame, fmt: str) -> None:
    values = matrix.to_numpy()
    for row_idx, task in enumerate(matrix.index):
        for col_idx, perturbation in enumerate(matrix.columns):
            value = values[row_idx, col_idx]
            if pd.isna(value):
                text = "NA"
            else:
                text = format(float(value), fmt)
            ax.text(
                col_idx,
                row_idx,
                text,
                ha="center",
                va="center",
                color="black",
                fontsize=9,
            )


def plot_heatmap(
    matrix: pd.DataFrame,
    title: str,
    output_path: Path,
    cmap: str,
    fmt: str,
    vmin: float | None = None,
    vmax: float | None = None,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9.5, 4.2), constrained_layout=True)
    image = ax.imshow(matrix, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    annotate_heatmap(ax, matrix, fmt)
    ax.set_title(title, fontsize=13, pad=12)
    ax.set_xticks(range(len(matrix.columns)))
    ax.set_xticklabels(matrix.columns, rotation=30, ha="right")
    ax.set_yticks(range(len(matrix.index)))
    ax.set_yticklabels(matrix.index)
    ax.set_xlabel("Perturbation")
    ax.set_ylabel("Task")
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.colorbar(image, ax=ax, fraction=0.035, pad=0.02)
    fig.savefig(output_path, dpi=220)
    plt.close(fig)


def plot_panel(matrices: list[tuple[pd.DataFrame, dict]], title: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(15, 8.5), constrained_layout=True)
    fig.suptitle(title, fontsize=15)
    for ax, (matrix, spec) in zip(axes.flat, matrices):
        image = ax.imshow(
            matrix,
            cmap=spec["cmap"],
            vmin=spec.get("vmin"),
            vmax=spec.get("vmax"),
            aspect="auto",
        )
        annotate_heatmap(ax, matrix, spec["fmt"])
        ax.set_title(spec["title"], fontsize=11)
        ax.set_xticks(range(len(matrix.columns)))
        ax.set_xticklabels(matrix.columns, rotation=30, ha="right")
        ax.set_yticks(range(len(matrix.index)))
        ax.set_yticklabels(matrix.index)
        ax.tick_params(length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        fig.colorbar(image, ax=ax, fraction=0.04, pad=0.02)
    fig.savefig(output_path, dpi=220)
    plt.close(fig)


def generate_for_dataset(key: str, config: dict, output_dir: Path) -> list[Path]:
    grouped = read_csv(config["grouped"])
    correlations = read_csv(config["correlations"])
    written = []

    panel_matrices = []
    for spec in GROUPED_HEATMAPS:
        matrix = matrix_from_grouped(grouped, spec["field"])
        csv_path = output_dir / f"rq2_heatmap_{key}_{spec['filename']}.csv"
        png_path = output_dir / f"rq2_heatmap_{key}_{spec['filename']}.png"
        write_matrix_csv(csv_path, matrix)
        plot_heatmap(
            matrix,
            f"{config['label']}: {spec['title']}",
            png_path,
            spec["cmap"],
            spec["fmt"],
            spec.get("vmin"),
            spec.get("vmax"),
        )
        panel_matrices.append((matrix, spec))
        written.extend([csv_path, png_path])

    panel_path = output_dir / f"rq2_heatmap_{key}_summary_panel.png"
    plot_panel(panel_matrices, f"RQ2 heatmap summary - {config['label']}", panel_path)
    written.append(panel_path)

    for spec in CORRELATION_HEATMAPS:
        matrix = matrix_from_correlations(correlations, spec["relationship"], spec["value"])
        csv_path = output_dir / f"rq2_heatmap_{key}_{spec['filename']}.csv"
        png_path = output_dir / f"rq2_heatmap_{key}_{spec['filename']}.png"
        write_matrix_csv(csv_path, matrix)
        plot_heatmap(
            matrix,
            f"{config['label']}: {spec['title']}",
            png_path,
            spec["cmap"],
            spec["fmt"],
            -1.0,
            1.0,
        )
        written.extend([csv_path, png_path])

    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot RQ2 heatmaps from existing metrics.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    written = []
    for key, config in DATASETS.items():
        written.extend(generate_for_dataset(key, config, args.output_dir))

    print(f"Wrote {len(written)} files to {args.output_dir}")
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
