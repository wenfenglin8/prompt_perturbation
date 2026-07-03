from __future__ import annotations

import math
import os
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
OUT = RESULTS / "rq2_visualizations"
os.environ.setdefault("MPLCONFIGDIR", str(RESULTS / ".matplotlib_cache"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TASK_ORDER = ["factual_qa", "math_reasoning", "code_generation"]
PERTURBATION_ORDER = [
    "context_injection",
    "formatting",
    "paraphrase",
    "reordering",
    "surface_noise",
]
TASK_LABELS = {
    "factual_qa": "Factual QA",
    "math_reasoning": "Math",
    "code_generation": "Code",
}
PERTURBATION_LABELS = {
    "context_injection": "Context",
    "formatting": "Format",
    "paraphrase": "Paraphrase",
    "reordering": "Reorder",
    "surface_noise": "Surface",
}
TASK_COLORS = {
    "factual_qa": "#2F80ED",
    "math_reasoning": "#F2994A",
    "code_generation": "#27AE60",
}


def ensure_numeric(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if col not in {"case_id", "task", "dataset", "perturbation", "scope_type", "scope_value", "relationship", "x", "y"}:
            converted = pd.to_numeric(out[col], errors="coerce")
            if converted.notna().sum() > 0:
                out[col] = converted
    return out


def load_csv(path: Path) -> pd.DataFrame:
    return ensure_numeric(pd.read_csv(path))


def savefig(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight")
    plt.close(fig)


def add_regression_line(ax: plt.Axes, x: pd.Series, y: pd.Series, color: str = "#333333") -> None:
    clean = pd.DataFrame({"x": x, "y": y}).replace([np.inf, -np.inf], np.nan).dropna()
    if len(clean) < 2 or clean["x"].nunique() < 2:
        return
    coef = np.polyfit(clean["x"], clean["y"], 1)
    xs = np.linspace(clean["x"].min(), clean["x"].max(), 100)
    ys = coef[0] * xs + coef[1]
    ax.plot(xs, ys, color=color, linewidth=1.8, alpha=0.85)


def scatter_overall(metrics: pd.DataFrame, tag: str, title_suffix: str) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    for task in TASK_ORDER:
        part = metrics[metrics["task"] == task]
        if part.empty:
            continue
        ax.scatter(
            part["noise_corrected_drift"],
            part["abs_repeated_pass_rate_change"],
            s=42,
            alpha=0.74,
            color=TASK_COLORS[task],
            edgecolor="white",
            linewidth=0.55,
            label=TASK_LABELS[task],
        )
    add_regression_line(
        ax,
        metrics["noise_corrected_drift"],
        metrics["abs_repeated_pass_rate_change"],
        "#111111",
    )
    ax.set_title(f"RQ2: Semantic Drift vs Correctness Drift{title_suffix}")
    ax.set_xlabel("Noise-corrected semantic drift")
    ax.set_ylabel("Absolute repeated pass-rate change")
    ax.grid(True, alpha=0.22)
    ax.legend(frameon=False, ncol=3, loc="upper right")
    savefig(fig, f"01_overall_scatter_{tag}.png")


def scatter_task_facets(metrics: pd.DataFrame, tag: str, title_suffix: str) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13.4, 4.35), sharey=True)
    xmax = max(metrics["noise_corrected_drift"].max() * 1.08, 0.01)
    for ax, task in zip(axes, TASK_ORDER):
        part = metrics[metrics["task"] == task]
        ax.scatter(
            part["noise_corrected_drift"],
            part["abs_repeated_pass_rate_change"],
            s=44,
            alpha=0.78,
            color=TASK_COLORS[task],
            edgecolor="white",
            linewidth=0.55,
        )
        add_regression_line(
            ax,
            part["noise_corrected_drift"],
            part["abs_repeated_pass_rate_change"],
            TASK_COLORS[task],
        )
        ax.set_title(TASK_LABELS[task])
        ax.set_xlabel("Corrected drift")
        ax.set_xlim(-0.005, xmax)
        ax.grid(True, alpha=0.22)
    axes[0].set_ylabel("Abs repeated pass-rate change")
    fig.suptitle(f"RQ2 by Task{title_suffix}", y=1.02, fontsize=13)
    savefig(fig, f"02_task_faceted_scatter_{tag}.png")


def correlation_bar(correlations: pd.DataFrame, tag: str, title_suffix: str) -> None:
    rows = [
        ("noise_corrected_drift", "primary", "Corrected"),
        ("raw_perturbation_drift", "raw_auxiliary", "Raw repeated"),
        ("uncorrected_single_drift", "single_vs_repeated_auxiliary", "Single pair"),
    ]
    data = []
    for x_name, rel, label in rows:
        row = correlations[
            (correlations["scope_type"] == "overall")
            & (correlations["scope_value"] == "all")
            & (correlations["relationship"] == rel)
            & (correlations["x"] == x_name)
            & (correlations["y"] == "abs_repeated_pass_rate_change")
        ]
        if not row.empty:
            item = row.iloc[0]
            data.append(
                {
                    "measure": label,
                    "pearson": float(item["pearson"]),
                    "spearman": float(item["spearman"]),
                    "spearman_low": float(item.get("spearman_ci95_low", np.nan)),
                    "spearman_high": float(item.get("spearman_ci95_high", np.nan)),
                }
            )
    if not data:
        return
    df = pd.DataFrame(data)
    x = np.arange(len(df))
    width = 0.36
    fig, ax = plt.subplots(figsize=(7.5, 4.9))
    ax.bar(x - width / 2, df["pearson"], width, label="Pearson", color="#6C5CE7", alpha=0.88)
    ax.bar(x + width / 2, df["spearman"], width, label="Spearman", color="#00A6A6", alpha=0.88)
    err_low = df["spearman"] - df["spearman_low"]
    err_high = df["spearman_high"] - df["spearman"]
    if err_low.notna().all() and err_high.notna().all():
        ax.errorbar(
            x + width / 2,
            df["spearman"],
            yerr=[err_low, err_high],
            fmt="none",
            ecolor="#1F2933",
            elinewidth=1.1,
            capsize=3,
        )
    ax.axhline(0, color="#333333", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(df["measure"])
    ax.set_ylim(0, max(0.65, float(df[["pearson", "spearman"]].max().max()) + 0.12))
    ax.set_ylabel("Correlation with correctness drift")
    ax.set_title(f"Corrected vs Uncorrected Drift Measures{title_suffix}")
    ax.grid(True, axis="y", alpha=0.22)
    ax.legend(frameon=False)
    savefig(fig, f"03_correlation_measure_comparison_{tag}.png")


def harmful_drop_bins(metrics: pd.DataFrame, tag: str, title_suffix: str) -> None:
    clean = metrics[["noise_corrected_drift", "harmful_correctness_drop"]].dropna().copy()
    if clean.empty:
        return
    clean["harmful_correctness_drop"] = clean["harmful_correctness_drop"].astype(float)
    try:
        clean["bin"] = pd.qcut(clean["noise_corrected_drift"], q=5, duplicates="drop")
    except ValueError:
        clean["bin"] = pd.cut(clean["noise_corrected_drift"], bins=5, duplicates="drop")
    grouped = clean.groupby("bin", observed=True).agg(
        share=("harmful_correctness_drop", "mean"),
        n=("harmful_correctness_drop", "size"),
        mean_drift=("noise_corrected_drift", "mean"),
    )
    labels = [f"{row.mean_drift:.3f}\n(n={int(row.n)})" for row in grouped.itertuples()]
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    ax.bar(np.arange(len(grouped)), grouped["share"], color="#D1495B", alpha=0.86)
    ax.set_xticks(np.arange(len(grouped)))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, min(1.0, max(0.35, float(grouped["share"].max()) + 0.15)))
    ax.set_xlabel("Noise-corrected drift bins, labeled by mean drift")
    ax.set_ylabel("Share with harmful correctness drop")
    ax.set_title(f"Harmful Correctness Drop by Drift Level{title_suffix}")
    ax.grid(True, axis="y", alpha=0.22)
    savefig(fig, f"04_harmful_drop_by_drift_bin_{tag}.png")


def heatmap(
    grouped: pd.DataFrame,
    value_col: str,
    tag: str,
    filename_suffix: str,
    title: str,
    cmap: str = "viridis",
) -> None:
    table = (
        grouped.pivot_table(
            index="task",
            columns="perturbation",
            values=value_col,
            aggfunc="mean",
        )
        .reindex(index=TASK_ORDER, columns=PERTURBATION_ORDER)
    )
    data = table.to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(8.5, 4.35))
    im = ax.imshow(data, cmap=cmap, aspect="auto")
    ax.set_xticks(np.arange(len(PERTURBATION_ORDER)))
    ax.set_xticklabels([PERTURBATION_LABELS[p] for p in PERTURBATION_ORDER], rotation=35, ha="right")
    ax.set_yticks(np.arange(len(TASK_ORDER)))
    ax.set_yticklabels([TASK_LABELS[t] for t in TASK_ORDER])
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            if math.isnan(val):
                text = ""
            else:
                text = f"{val:.3f}"
            ax.text(j, i, text, ha="center", va="center", color="white" if val > np.nanmax(data) * 0.55 else "#111111", fontsize=9)
    cbar = fig.colorbar(im, ax=ax)
    cbar.ax.set_ylabel(value_col, rotation=270, labelpad=16)
    ax.set_title(title)
    savefig(fig, f"05_heatmap_{filename_suffix}_{tag}.png")


def perturbation_correlation_bars(correlations: pd.DataFrame, tag: str, title_suffix: str) -> None:
    rows = correlations[
        (correlations["scope_type"] == "perturbation")
        & (correlations["relationship"] == "primary")
    ].copy()
    if rows.empty:
        return
    rows["scope_value"] = pd.Categorical(rows["scope_value"], categories=PERTURBATION_ORDER, ordered=True)
    rows = rows.sort_values("scope_value")
    x = np.arange(len(rows))
    y = rows["spearman"].astype(float).to_numpy()
    low = rows["spearman_ci95_low"].astype(float).to_numpy()
    high = rows["spearman_ci95_high"].astype(float).to_numpy()
    fig, ax = plt.subplots(figsize=(8.2, 4.75))
    ax.bar(x, y, color="#40798C", alpha=0.88)
    ax.errorbar(x, y, yerr=[y - low, high - y], fmt="none", ecolor="#1F2933", capsize=3, linewidth=1.1)
    ax.axhline(0, color="#333333", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([PERTURBATION_LABELS[str(p)] for p in rows["scope_value"]], rotation=25, ha="right")
    ax.set_ylabel("Spearman correlation")
    ax.set_title(f"RQ2 Correlation by Perturbation{title_suffix}")
    ax.grid(True, axis="y", alpha=0.22)
    savefig(fig, f"06_perturbation_spearman_{tag}.png")


def case_inspection_scatter(metrics: pd.DataFrame, tag: str, title_suffix: str) -> None:
    fig, ax = plt.subplots(figsize=(8.6, 5.7))
    for task in TASK_ORDER:
        part = metrics[metrics["task"] == task]
        ax.scatter(
            part["noise_corrected_drift"],
            part["abs_repeated_pass_rate_change"],
            s=38,
            alpha=0.58,
            color=TASK_COLORS[task],
            edgecolor="white",
            linewidth=0.5,
            label=TASK_LABELS[task],
        )

    candidates = []
    candidates.extend(
        metrics.sort_values(
            ["noise_corrected_drift", "abs_repeated_pass_rate_change"],
            ascending=False,
        ).head(3).index.tolist()
    )
    high_drift_no_change = metrics[
        metrics["abs_repeated_pass_rate_change"].astype(float) == 0
    ].sort_values("noise_corrected_drift", ascending=False).head(3)
    candidates.extend(high_drift_no_change.index.tolist())
    high_change_low_drift = metrics[
        metrics["abs_repeated_pass_rate_change"].astype(float) >= 0.99
    ].sort_values("noise_corrected_drift", ascending=True).head(3)
    candidates.extend(high_change_low_drift.index.tolist())

    seen = set()
    for idx in candidates:
        if idx in seen or idx not in metrics.index:
            continue
        seen.add(idx)
        row = metrics.loc[idx]
        label = f"{TASK_LABELS.get(row['task'], row['task'])}/{PERTURBATION_LABELS.get(row['perturbation'], row['perturbation'])}"
        ax.annotate(
            label,
            (row["noise_corrected_drift"], row["abs_repeated_pass_rate_change"]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,
            color="#111111",
            bbox={"boxstyle": "round,pad=0.18", "fc": "white", "ec": "#CCCCCC", "alpha": 0.82},
        )

    ax.set_xlabel("Noise-corrected semantic drift")
    ax.set_ylabel("Absolute repeated pass-rate change")
    ax.set_title(f"Representative RQ2 Cases{title_suffix}")
    ax.grid(True, alpha=0.22)
    ax.legend(frameon=False, ncol=3, loc="upper right")
    savefig(fig, f"07_case_inspection_scatter_{tag}.png")


def factual_judge_transition() -> None:
    path = RESULTS / "rq2_semantic_correctness_llm_fact_factual_judgments.csv"
    if not path.exists():
        return
    df = load_csv(path)
    if "exact_correct" not in df.columns and "exact_match_correct" in df.columns:
        df["exact_correct"] = df["exact_match_correct"]
    if not {"exact_correct", "llm_correct"}.issubset(df.columns):
        return
    trans = df.groupby(["exact_correct", "llm_correct"]).size().reset_index(name="n")
    labels = ["Exact 0 -> LLM 0", "Exact 0 -> LLM 1", "Exact 1 -> LLM 0", "Exact 1 -> LLM 1"]
    counts = []
    for exact, llm in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        row = trans[(trans["exact_correct"] == exact) & (trans["llm_correct"] == llm)]
        counts.append(int(row["n"].iloc[0]) if not row.empty else 0)
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    colors = ["#8ECAE6", "#219EBC", "#FFB703", "#2A9D8F"]
    ax.bar(np.arange(len(labels)), counts, color=colors, alpha=0.9)
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylabel("Factual outputs")
    ax.set_title("Factual QA Correctness: Exact Match vs LLM Judge")
    ax.grid(True, axis="y", alpha=0.22)
    for i, count in enumerate(counts):
        ax.text(i, count + max(counts) * 0.02, str(count), ha="center", va="bottom", fontsize=9)
    savefig(fig, "08_factual_exact_vs_llm_transition.png")


def exact_vs_llm_summary(exact_corr: pd.DataFrame, llm_corr: pd.DataFrame) -> None:
    def get_primary(corr: pd.DataFrame) -> tuple[float, float, float, float]:
        row = corr[
            (corr["scope_type"] == "overall")
            & (corr["scope_value"] == "all")
            & (corr["relationship"] == "primary")
        ].iloc[0]
        return (
            float(row["pearson"]),
            float(row["spearman"]),
            float(row["spearman_ci95_low"]),
            float(row["spearman_ci95_high"]),
        )

    exact = get_primary(exact_corr)
    llm = get_primary(llm_corr)
    labels = ["Exact factual", "LLM factual"]
    pearson = [exact[0], llm[0]]
    spearman = [exact[1], llm[1]]
    low = np.array([exact[2], llm[2]])
    high = np.array([exact[3], llm[3]])
    x = np.arange(2)
    width = 0.36
    fig, ax = plt.subplots(figsize=(6.9, 4.8))
    ax.bar(x - width / 2, pearson, width, color="#6C5CE7", alpha=0.88, label="Pearson")
    ax.bar(x + width / 2, spearman, width, color="#00A6A6", alpha=0.88, label="Spearman")
    ax.errorbar(x + width / 2, spearman, yerr=[np.array(spearman) - low, high - np.array(spearman)], fmt="none", ecolor="#1F2933", capsize=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max(0.7, max(pearson + spearman) + 0.12))
    ax.set_ylabel("Overall RQ2 correlation")
    ax.set_title("RQ2 Sensitivity to Factual Correctness Evaluator")
    ax.grid(True, axis="y", alpha=0.22)
    ax.legend(frameon=False)
    savefig(fig, "09_exact_vs_llm_rq2_correlation.png")


def run_version(tag: str, title_suffix: str, metrics_path: Path, grouped_path: Path, corr_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame] | None:
    if not metrics_path.exists() or not grouped_path.exists() or not corr_path.exists():
        print(f"Skipping {tag}: missing one or more input files")
        return None
    metrics = load_csv(metrics_path)
    grouped = load_csv(grouped_path)
    correlations = load_csv(corr_path)

    scatter_overall(metrics, tag, title_suffix)
    scatter_task_facets(metrics, tag, title_suffix)
    correlation_bar(correlations, tag, title_suffix)
    harmful_drop_bins(metrics, tag, title_suffix)
    heatmap(
        grouped,
        "mean_noise_corrected_drift",
        tag,
        "corrected_drift",
        f"Mean Noise-Corrected Drift{title_suffix}",
        "magma",
    )
    heatmap(
        grouped,
        "mean_abs_repeated_pass_rate_change",
        tag,
        "correctness_change",
        f"Mean Correctness Drift{title_suffix}",
        "viridis",
    )
    heatmap(
        grouped,
        "share_harmful_correctness_drop",
        tag,
        "harmful_drop_share",
        f"Share of Harmful Correctness Drops{title_suffix}",
        "plasma",
    )
    perturbation_correlation_bars(correlations, tag, title_suffix)
    case_inspection_scatter(metrics, tag, title_suffix)
    return metrics, grouped, correlations


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

    exact = run_version(
        "exact_fact",
        " (Exact Factual QA)",
        RESULTS / "rq2_semantic_correctness_metrics.csv",
        RESULTS / "rq2_semantic_correctness_grouped.csv",
        RESULTS / "rq2_semantic_correctness_correlations.csv",
    )
    llm = run_version(
        "llm_fact",
        " (LLM Factual QA)",
        RESULTS / "rq2_semantic_correctness_llm_fact_metrics.csv",
        RESULTS / "rq2_semantic_correctness_llm_fact_grouped.csv",
        RESULTS / "rq2_semantic_correctness_llm_fact_correlations.csv",
    )

    factual_judge_transition()
    if exact is not None and llm is not None:
        exact_vs_llm_summary(exact[2], llm[2])

    print(f"Saved RQ2 visualizations to: {OUT}")
    for path in sorted(OUT.glob("*.png")):
        print(path.name)


if __name__ == "__main__":
    main()
