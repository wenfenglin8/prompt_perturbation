import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
MPL_CACHE_DIR = RESULTS_DIR / ".matplotlib_cache"
MPL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE_DIR))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd


DEFAULT_RQ1 = RESULTS_DIR / "similarity_metrics_four_task_similarity_sweep_pdr_aligned_5x3.csv"
DEFAULT_RQ2 = RESULTS_DIR / "rq2_semantic_correctness_metrics.csv"
DEFAULT_RQ2_LLM_FACT = RESULTS_DIR / "rq2_semantic_correctness_llm_fact_metrics.csv"


def ensure_outdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_tornado(
    df: pd.DataFrame,
    value_col: str,
    group_col: str,
    title: str,
    xlabel: str,
    path: Path,
) -> pd.DataFrame:
    summary = (
        df.groupby(group_col, as_index=False)[value_col]
        .agg(["mean", "std", "count"])
        .reset_index()
        .sort_values("mean", ascending=True)
    )
    fig_height = max(4.5, 0.45 * len(summary) + 1.4)
    fig, ax = plt.subplots(figsize=(9, fig_height))
    ax.barh(summary[group_col], summary["mean"], color="#4C78A8")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(group_col)
    ax.grid(axis="x", alpha=0.25)
    for idx, value in enumerate(summary["mean"]):
        ax.text(value, idx, f" {value:.3f}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return summary.sort_values("mean", ascending=False)


def save_task_perturbation_tornado(
    df: pd.DataFrame,
    value_col: str,
    title: str,
    xlabel: str,
    path: Path,
) -> pd.DataFrame:
    temp = df.copy()
    temp["task_perturbation"] = temp["task"] + " / " + temp["perturbation"]
    return save_tornado(temp, value_col, "task_perturbation", title, xlabel, path)


def anova_table(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    model = ols(f"{value_col} ~ C(task) + C(perturbation) + C(task):C(perturbation)", data=df).fit()
    table = sm.stats.anova_lm(model, typ=2)
    return table.reset_index().rename(columns={"index": "effect"})


def tukey_table(df: pd.DataFrame, value_col: str, group_col: str) -> pd.DataFrame:
    result = pairwise_tukeyhsd(endog=df[value_col], groups=df[group_col], alpha=0.05)
    table = pd.DataFrame(data=result._results_table.data[1:], columns=result._results_table.data[0])
    return table


def run_dataset(
    name: str,
    df: pd.DataFrame,
    value_col: str,
    outdir: Path,
    report_lines: list[str],
    caution: str,
) -> None:
    for col in ["task", "perturbation", value_col]:
        if col not in df.columns:
            raise ValueError(f"{name} missing required column: {col}")
    df = df.copy()
    df[value_col] = pd.to_numeric(df[value_col])

    by_perturbation_png = outdir / f"{name}_tornado_by_perturbation.png"
    by_task_png = outdir / f"{name}_tornado_by_task.png"
    by_task_perturbation_png = outdir / f"{name}_tornado_by_task_perturbation.png"
    perturbation_summary = save_tornado(
        df,
        value_col,
        "perturbation",
        f"{name}: mean {value_col} by perturbation",
        f"Mean {value_col}",
        by_perturbation_png,
    )
    task_summary = save_tornado(
        df,
        value_col,
        "task",
        f"{name}: mean {value_col} by task",
        f"Mean {value_col}",
        by_task_png,
    )
    task_perturbation_summary = save_task_perturbation_tornado(
        df,
        value_col,
        f"{name}: mean {value_col} by task x perturbation",
        f"Mean {value_col}",
        by_task_perturbation_png,
    )

    perturbation_summary.to_csv(outdir / f"{name}_tornado_by_perturbation.csv", index=False)
    task_summary.to_csv(outdir / f"{name}_tornado_by_task.csv", index=False)
    task_perturbation_summary.to_csv(outdir / f"{name}_tornado_by_task_perturbation.csv", index=False)

    anova = anova_table(df, value_col)
    anova_path = outdir / f"{name}_anova_task_perturbation.csv"
    anova.to_csv(anova_path, index=False)

    tukey_perturbation = tukey_table(df, value_col, "perturbation")
    tukey_task = tukey_table(df, value_col, "task")
    temp = df.copy()
    temp["task_perturbation"] = temp["task"] + " / " + temp["perturbation"]
    tukey_task_perturbation = tukey_table(temp, value_col, "task_perturbation")
    tukey_perturbation.to_csv(outdir / f"{name}_tukey_perturbation.csv", index=False)
    tukey_task.to_csv(outdir / f"{name}_tukey_task.csv", index=False)
    tukey_task_perturbation.to_csv(outdir / f"{name}_tukey_task_perturbation.csv", index=False)

    report_lines.extend(
        [
            f"## {name}",
            "",
            f"- Dependent variable: `{value_col}`",
            f"- Rows: `{len(df)}`",
            f"- Caution: {caution}",
            "",
            "### Tornado Charts",
            "",
            f"- By perturbation: `{by_perturbation_png.as_posix()}`",
            f"- By task: `{by_task_png.as_posix()}`",
            f"- By task x perturbation: `{by_task_perturbation_png.as_posix()}`",
            "",
            "### Top Perturbation Effects",
            "",
            perturbation_summary[["perturbation", "mean", "std", "count"]].to_markdown(index=False, floatfmt=".4f"),
            "",
            "### Top Task Effects",
            "",
            task_summary[["task", "mean", "std", "count"]].to_markdown(index=False, floatfmt=".4f"),
            "",
            "### ANOVA: task + perturbation + interaction",
            "",
            anova.to_markdown(index=False, floatfmt=".5f"),
            "",
            "### Tukey HSD Outputs",
            "",
            f"- Perturbation Tukey table: `{(outdir / f'{name}_tukey_perturbation.csv').as_posix()}`",
            f"- Task Tukey table: `{(outdir / f'{name}_tukey_task.csv').as_posix()}`",
            f"- Task x perturbation Tukey table: `{(outdir / f'{name}_tukey_task_perturbation.csv').as_posix()}`",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rq1", type=Path, default=DEFAULT_RQ1)
    parser.add_argument("--rq2", type=Path, default=DEFAULT_RQ2)
    parser.add_argument("--rq2-llm-fact", type=Path, default=DEFAULT_RQ2_LLM_FACT)
    parser.add_argument("--outdir", type=Path, default=RESULTS_DIR / "proposal_visual_stats")
    args = parser.parse_args()

    ensure_outdir(args.outdir)
    report_lines = [
        "# Proposal Visual and Statistical Analysis",
        "",
        "This report checks the Proposal0.5 plan item about tornado charts, ANOVA, and Tukey HSD.",
        "",
        "The tornado charts visualize relative perturbation effects. The ANOVA/Tukey analyses are exploratory because some dependent variables, especially correctness drift, are discrete and bounded.",
        "",
    ]

    rq1 = pd.read_csv(args.rq1)
    run_dataset(
        "rq1_similarity_drift",
        rq1,
        "noise_corrected_drift",
        args.outdir,
        report_lines,
        "Continuous embedding-distance metric; ANOVA is more defensible here than for discrete correctness outcomes, though sample size is still small.",
    )

    rq2 = pd.read_csv(args.rq2)
    run_dataset(
        "rq2_correctness_drift_exact_fact",
        rq2,
        "abs_repeated_pass_rate_change",
        args.outdir,
        report_lines,
        "Correctness drift is discrete and bounded because each prompt version has three samples; treat ANOVA/Tukey as exploratory.",
    )
    run_dataset(
        "rq2_harmful_drop_exact_fact",
        rq2,
        "harmful_correctness_drop",
        args.outdir,
        report_lines,
        "Binary outcome; ANOVA is a rough exploratory comparison of group means, not a primary inference model.",
    )

    if args.rq2_llm_fact.exists():
        rq2_llm = pd.read_csv(args.rq2_llm_fact)
        run_dataset(
            "rq2_correctness_drift_llm_fact",
            rq2_llm,
            "abs_repeated_pass_rate_change",
            args.outdir,
            report_lines,
            "Sensitivity analysis using LLM-equivalence factual correctness; correctness drift remains discrete and bounded.",
        )

    report_path = args.outdir / "proposal_visual_stats_report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
