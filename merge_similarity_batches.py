import argparse
import csv
import json
import statistics
from pathlib import Path

from four_task_similarity_sweep import DATASETS_BY_TASK, RESULTS_DIR, TASK_ORDER, write_csv
from reference_perturbations import REFERENCE_PERTURBATIONS


NUMERIC_FIELDS = [
    "uncorrected_single_drift",
    "original_noise",
    "perturbed_noise",
    "noise_baseline",
    "raw_perturbation_drift",
    "noise_corrected_drift",
]


def read_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_metric_rows(path: Path) -> list[dict]:
    rows = read_csv(path)
    for row in rows:
        for field in NUMERIC_FIELDS:
            row[field] = float(row[field])
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-count", type=int, required=True)
    parser.add_argument("--batch-tag-prefix", required=True)
    parser.add_argument("--output-tag", required=True)
    args = parser.parse_args()

    generations = []
    metrics = []
    for batch_index in range(1, args.batch_count + 1):
        batch_tag = f"{args.batch_tag_prefix}_batch{batch_index}of{args.batch_count}"
        generations_path = RESULTS_DIR / f"generations_{batch_tag}.csv"
        metrics_path = RESULTS_DIR / f"similarity_metrics_{batch_tag}.csv"
        if not generations_path.exists() or not metrics_path.exists():
            raise RuntimeError(f"Missing batch {batch_index}/{args.batch_count}: {generations_path} or {metrics_path}")
        generations.extend(read_csv(generations_path))
        metrics.extend(read_metric_rows(metrics_path))

    grouped = []
    for task in TASK_ORDER:
        for perturbation in REFERENCE_PERTURBATIONS:
            rows = [row for row in metrics if row["task"] == task and row["perturbation"] == perturbation]
            if not rows:
                raise RuntimeError(f"Missing rows for task={task}, perturbation={perturbation}")
            grouped.append(
                {
                    "task": task,
                    "perturbation": perturbation,
                    "dataset": rows[0]["dataset"],
                    "n": len(rows),
                    "uncorrected_single_drift": statistics.mean(row["uncorrected_single_drift"] for row in rows),
                    "noise_baseline": statistics.mean(row["noise_baseline"] for row in rows),
                    "raw_perturbation_drift": statistics.mean(row["raw_perturbation_drift"] for row in rows),
                    "noise_corrected_drift": statistics.mean(row["noise_corrected_drift"] for row in rows),
                }
            )

    rankings = []
    for task in TASK_ORDER:
        rows = sorted(
            [row for row in grouped if row["task"] == task],
            key=lambda row: row["noise_corrected_drift"],
            reverse=True,
        )
        for rank, row in enumerate(rows, start=1):
            rankings.append(
                {
                    "task": task,
                    "rank": rank,
                    "perturbation": row["perturbation"],
                    "noise_corrected_drift": row["noise_corrected_drift"],
                    "raw_perturbation_drift": row["raw_perturbation_drift"],
                }
            )

    suffix = f"_{args.output_tag}"
    generations_path = RESULTS_DIR / f"generations{suffix}.csv"
    metrics_path = RESULTS_DIR / f"similarity_metrics{suffix}.csv"
    grouped_path = RESULTS_DIR / f"similarity_grouped{suffix}.csv"
    rankings_path = RESULTS_DIR / f"similarity_rankings{suffix}.csv"
    json_path = RESULTS_DIR / f"similarity_summary{suffix}.json"
    report_path = RESULTS_DIR / f"similarity_report{suffix}.md"

    write_csv(generations_path, generations)
    write_csv(metrics_path, metrics)
    write_csv(grouped_path, grouped)
    write_csv(rankings_path, rankings)
    json_path.write_text(
        json.dumps(
            {
                "batch_count": args.batch_count,
                "batch_tag_prefix": args.batch_tag_prefix,
                "tasks": TASK_ORDER,
                "datasets_by_task": DATASETS_BY_TASK,
                "perturbations": REFERENCE_PERTURBATIONS,
                "total_generation_rows": len(generations),
                "total_metric_rows": len(metrics),
                "grouped": grouped,
                "rankings": rankings,
                "metrics": metrics,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Four-Task Similarity Sweep, PDR-Aligned Perturbations",
        "",
        f"- Batch count: `{args.batch_count}`",
        f"- Tasks: `{', '.join(TASK_ORDER)}`",
        f"- Datasets: `{', '.join(DATASETS_BY_TASK[task] for task in TASK_ORDER)}`",
        f"- Perturbations: `{', '.join(REFERENCE_PERTURBATIONS)}`",
        "- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.",
        f"- Total generation rows: `{len(generations)}`",
        f"- Total metric rows: `{len(metrics)}`",
        "",
        "## Grouped Drift",
        "",
        "| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in grouped:
        lines.append(
            f"| {row['task']} | {row['dataset']} | {row['perturbation']} | {row['n']} | "
            f"{row['uncorrected_single_drift']:.4f} | {row['noise_baseline']:.4f} | "
            f"{row['raw_perturbation_drift']:.4f} | {row['noise_corrected_drift']:.4f} |"
        )
    lines.extend(["", "## Corrected Sensitivity Ranking", "", "| task | rank | perturbation | corrected drift | raw drift |", "|---|---:|---|---:|---:|"])
    for row in rankings:
        lines.append(
            f"| {row['task']} | {row['rank']} | {row['perturbation']} | "
            f"{row['noise_corrected_drift']:.4f} | {row['raw_perturbation_drift']:.4f} |"
        )
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {generations_path}")
    print(f"Wrote {metrics_path}")
    print(f"Wrote {grouped_path}")
    print(f"Wrote {rankings_path}")
    print(f"Wrote {json_path}")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
