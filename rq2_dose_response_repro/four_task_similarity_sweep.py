import argparse
import csv
import itertools
import json
import os
import statistics
import time
from pathlib import Path

import numpy as np
import requests

from reference_perturbations import REFERENCE_PERTURBATIONS, perturb_instruction


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
TASK_ORDER = ["factual_qa", "math_reasoning", "code_generation", "open_ended_writing"]
DATASETS_BY_TASK = {
    "factual_qa": "SQuAD V2",
    "math_reasoning": "MATH",
    "code_generation": "HumanEval",
    "open_ended_writing": "Alpaca",
}


def read_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key
    key_file = ROOT / "api.txt"
    if key_file.exists():
        return key_file.read_text(encoding="utf-8").strip()
    raise RuntimeError("OPENAI_API_KEY is not set and api.txt was not found.")


def post_json(url: str, api_key: str, payload: dict, timeout: int = 90) -> dict:
    last_error = None
    for attempt in range(5):
        try:
            response = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=timeout,
            )
            if response.status_code >= 500 or response.status_code == 429:
                last_error = RuntimeError(f"{response.status_code} {response.text[:1000]}")
                time.sleep(2**attempt)
                continue
            if response.status_code >= 400:
                raise RuntimeError(f"{response.status_code} {response.text[:1000]}")
            return response.json()
        except requests.RequestException as exc:
            last_error = exc
            time.sleep(2**attempt)
    raise RuntimeError(f"Request failed after retries: {last_error}")


def generate_text(api_key: str, model: str, prompt: str, temperature: float, top_p: float) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a precise assistant. Answer directly."},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "top_p": top_p,
    }
    data = post_json("https://api.openai.com/v1/chat/completions", api_key, payload)
    return data["choices"][0]["message"]["content"].strip()


def embed_texts(api_key: str, model: str, texts: list[str]) -> np.ndarray:
    data = post_json("https://api.openai.com/v1/embeddings", api_key, {"model": model, "input": texts})
    vectors = [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
    arr = np.array(vectors, dtype=float)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    return arr / np.maximum(norms, 1e-12)


def dataset_from_arrow(path: Path):
    from datasets import Dataset

    if not path.exists():
        raise RuntimeError(f"Dataset Arrow file not found: {path}")
    return Dataset.from_file(str(path))


def load_cases(
    max_per_task: int,
    perturbations: list[str],
    api_key: str,
    model: str,
    batch_count: int = 1,
    batch_index: int = 1,
) -> list[dict]:
    cases = []
    base = Path.home() / ".cache" / "huggingface" / "datasets"
    expected_cases = max_per_task * len(perturbations) * len(TASK_ORDER)
    expected_selected_cases = sum(
        1 for case_number in range(1, expected_cases + 1) if (case_number - 1) % batch_count == batch_index - 1
    )
    candidate_count = 0

    def should_prepare(task: str, perturbation: str) -> bool:
        nonlocal candidate_count
        candidate_count += 1
        selected = (candidate_count - 1) % batch_count == batch_index - 1
        if selected:
            next_count = len(cases) + 1
            print(
                f"Case prep {next_count}/{expected_selected_cases} "
                f"({next_count / expected_selected_cases * 100:.1f}%; global {candidate_count}/{expected_cases}) "
                f"- {task} {perturbation}",
                flush=True,
            )
        return selected

    def append_case(case: dict) -> None:
        next_count = len(cases) + 1
        cases.append(case)

    squad = dataset_from_arrow(
        base
        / "squad_v2"
        / "squad_v2"
        / "0.0.0"
        / "3ffb306f725f7d2ce8394bc1873b24868140c412"
        / "squad_v2-validation.arrow"
    )
    squad_count = 0
    for item in squad:
        answers = [answer for answer in item["answers"]["text"] if answer.strip()]
        if not answers:
            continue
        instruction = "Read the passage and answer the question. Answer with the exact short answer only."
        body = f"\n\nPassage: {item['context']}\n\nQuestion: {item['question']}"
        for perturbation in perturbations:
            if not should_prepare("factual_qa", perturbation):
                continue
            append_case(
                {
                    "case_id": f"fourtask_{perturbation}_squad_{squad_count + 1:02d}",
                    "task": "factual_qa",
                    "dataset": "SQuAD V2",
                    "perturbation": perturbation,
                    "original": instruction + body,
                    "perturbed": perturb_instruction(instruction, perturbation, "factual_qa", api_key, model) + body,
                }
            )
        squad_count += 1
        if squad_count >= max_per_task:
            break

    math_ds = dataset_from_arrow(
        base
        / "DigitalLearningGmbH___math-lighteval"
        / "default"
        / "0.0.0"
        / "0530c78699ea5e8eb5530600900e1f328b48acad"
        / "math-lighteval-test.arrow"
    )
    for idx, item in enumerate(math_ds.select(range(max_per_task))):
        instruction = "Solve the mathematics problem. Put the final answer only on the last line."
        body = f"\n\nProblem: {item['problem']}"
        for perturbation in perturbations:
            if not should_prepare("math_reasoning", perturbation):
                continue
            append_case(
                {
                    "case_id": f"fourtask_{perturbation}_math_{idx + 1:02d}",
                    "task": "math_reasoning",
                    "dataset": "MATH",
                    "perturbation": perturbation,
                    "original": instruction + body,
                    "perturbed": perturb_instruction(instruction, perturbation, "math_reasoning", api_key, model) + body,
                }
            )

    human_eval = dataset_from_arrow(
        base
        / "openai___openai_humaneval"
        / "openai_humaneval"
        / "0.0.0"
        / "7dce6050a7d6d172f3cc5c32aa97f52fa1a2e544"
        / "openai_humaneval-test.arrow"
    )
    for idx, item in enumerate(human_eval.select(range(max_per_task))):
        instruction = "Complete the following Python function. Return only valid Python code, with no explanation."
        body = f"\n\n{item['prompt'].rstrip()}"
        for perturbation in perturbations:
            if not should_prepare("code_generation", perturbation):
                continue
            append_case(
                {
                    "case_id": f"fourtask_{perturbation}_humaneval_{idx + 1:02d}",
                    "task": "code_generation",
                    "dataset": "HumanEval",
                    "perturbation": perturbation,
                    "original": instruction + body,
                    "perturbed": perturb_instruction(instruction, perturbation, "code_generation", api_key, model) + body,
                }
            )

    alpaca = dataset_from_arrow(
        base
        / "tatsu-lab___alpaca"
        / "default"
        / "0.0.0"
        / "dce01c9b08f87459cf36a430d809084718273017"
        / "alpaca-train.arrow"
    )
    for idx, item in enumerate(alpaca.select(range(max_per_task))):
        instruction_text = item["instruction"].strip()
        input_text = item.get("input", "").strip()
        input_block = f"\n\nInput:\n{input_text}" if input_text else ""
        instruction = "Respond to the following instruction clearly and directly."
        body = f"\n\nInstruction:\n{instruction_text}{input_block}"
        for perturbation in perturbations:
            if not should_prepare("open_ended_writing", perturbation):
                continue
            append_case(
                {
                    "case_id": f"fourtask_{perturbation}_alpaca_{idx + 1:02d}",
                    "task": "open_ended_writing",
                    "dataset": "Alpaca",
                    "perturbation": perturbation,
                    "original": instruction + body,
                    "perturbed": perturb_instruction(instruction, perturbation, "open_ended_writing", api_key, model) + body,
                }
            )

    return cases


def avg_pairwise_distance(vectors: np.ndarray) -> float:
    distances = [
        max(0.0, 1.0 - float(np.dot(vectors[i], vectors[j])))
        for i, j in itertools.combinations(range(len(vectors)), 2)
    ]
    return float(statistics.mean(distances)) if distances else 0.0


def avg_cross_distance(a: np.ndarray, b: np.ndarray) -> float:
    distances = [
        max(0.0, 1.0 - float(np.dot(a[i], b[j])))
        for i in range(len(a))
        for j in range(len(b))
    ]
    return float(statistics.mean(distances)) if distances else 0.0


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def coerce_metric_rows(rows: list[dict]) -> list[dict]:
    numeric_fields = [
        "uncorrected_single_drift",
        "original_noise",
        "perturbed_noise",
        "noise_baseline",
        "raw_perturbation_drift",
        "noise_corrected_drift",
    ]
    for row in rows:
        for field in numeric_fields:
            row[field] = float(row[field])
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--embedding-model", default="text-embedding-3-small")
    parser.add_argument("--dataset-cases-per-task", type=int, default=2)
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--output-tag", default="four_task_similarity_sweep")
    parser.add_argument("--sleep", type=float, default=0.2)
    parser.add_argument("--resume", action="store_true", help="Resume from existing generation and metric CSV files for the output tag.")
    parser.add_argument("--batch-count", type=int, default=1, help="Split the case matrix into this many batches.")
    parser.add_argument("--batch-index", type=int, default=1, help="Run this 1-based batch index.")
    args = parser.parse_args()
    if args.batch_count < 1:
        raise ValueError("--batch-count must be at least 1")
    if args.batch_index < 1 or args.batch_index > args.batch_count:
        raise ValueError("--batch-index must be between 1 and --batch-count")

    api_key = read_api_key()
    RESULTS_DIR.mkdir(exist_ok=True)
    perturbations = REFERENCE_PERTURBATIONS
    suffix = f"_{args.output_tag}" if args.output_tag else ""
    generations_path = RESULTS_DIR / f"generations{suffix}.csv"
    metrics_path = RESULTS_DIR / f"similarity_metrics{suffix}.csv"
    grouped_path = RESULTS_DIR / f"similarity_grouped{suffix}.csv"
    rankings_path = RESULTS_DIR / f"similarity_rankings{suffix}.csv"
    json_path = RESULTS_DIR / f"similarity_summary{suffix}.json"
    report_path = RESULTS_DIR / f"similarity_report{suffix}.md"

    cases = load_cases(
        args.dataset_cases_per_task,
        perturbations,
        api_key,
        args.model,
        batch_count=args.batch_count,
        batch_index=args.batch_index,
    )

    generations = read_csv(generations_path) if args.resume and generations_path.exists() else []
    metrics = coerce_metric_rows(read_csv(metrics_path)) if args.resume and metrics_path.exists() else []
    completed_case_ids = {row["case_id"] for row in metrics}
    total_requests = len(cases) * 2 * args.samples
    completed = len(generations)

    print(
        f"Running {len(cases)} cases, {args.samples} samples per prompt version, "
        f"{total_requests} total generation calls. "
        f"Batch {args.batch_index}/{args.batch_count}.",
        flush=True,
    )
    if completed_case_ids:
        print(
            f"Resuming with {len(completed_case_ids)}/{len(cases)} cases complete and "
            f"{completed}/{total_requests} generation calls already written.",
            flush=True,
        )
    for case_idx, case in enumerate(cases, start=1):
        if case["case_id"] in completed_case_ids:
            print(
                f"Case {case_idx}/{len(cases)} ({case_idx / len(cases) * 100:.1f}%) already complete: "
                f"{case['case_id']}",
                flush=True,
            )
            continue
        print(
            f"Case {case_idx}/{len(cases)} ({case_idx / len(cases) * 100:.1f}%): {case['case_id']} "
            f"({case['task']}, {case['perturbation']})",
            flush=True,
        )
        outputs = {"original": [], "perturbed": []}
        for version in ["original", "perturbed"]:
            for sample_idx in range(args.samples):
                print(
                    f"Progress {completed}/{total_requests} ({completed / total_requests * 100:.1f}%) "
                    f"- requesting {version} {sample_idx + 1}/{args.samples}",
                    flush=True,
                )
                output = generate_text(api_key, args.model, case[version], args.temperature, args.top_p)
                completed += 1
                print(f"Progress {completed}/{total_requests} ({completed / total_requests * 100:.1f}%) complete", flush=True)
                outputs[version].append(output)
                generations.append(
                    {
                        "case_id": case["case_id"],
                        "task": case["task"],
                        "dataset": case["dataset"],
                        "perturbation": case["perturbation"],
                        "version": version,
                        "sample_idx": sample_idx,
                        "prompt": case[version],
                        "output": output,
                    }
                )
                time.sleep(args.sleep)

        vectors = embed_texts(api_key, args.embedding_model, outputs["original"] + outputs["perturbed"])
        original_vectors = vectors[: args.samples]
        perturbed_vectors = vectors[args.samples :]
        original_noise = avg_pairwise_distance(original_vectors)
        perturbed_noise = avg_pairwise_distance(perturbed_vectors)
        noise_baseline = (original_noise + perturbed_noise) / 2.0
        uncorrected = max(0.0, 1.0 - float(np.dot(original_vectors[0], perturbed_vectors[0])))
        raw = avg_cross_distance(original_vectors, perturbed_vectors)
        corrected = max(0.0, raw - noise_baseline)
        metrics.append(
            {
                "case_id": case["case_id"],
                "task": case["task"],
                "dataset": case["dataset"],
                "perturbation": case["perturbation"],
                "uncorrected_single_drift": uncorrected,
                "original_noise": original_noise,
                "perturbed_noise": perturbed_noise,
                "noise_baseline": noise_baseline,
                "raw_perturbation_drift": raw,
                "noise_corrected_drift": corrected,
            }
        )
        write_csv(generations_path, generations)
        write_csv(metrics_path, metrics)
        completed_case_ids.add(case["case_id"])
        print(
            f"Checkpoint complete: {len(completed_case_ids)}/{len(cases)} cases "
            f"({len(completed_case_ids) / len(cases) * 100:.1f}%) written.",
            flush=True,
        )

    grouped = []
    for task in TASK_ORDER:
        for perturbation in perturbations:
            rows = [row for row in metrics if row["task"] == task and row["perturbation"] == perturbation]
            if not rows:
                continue
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

    write_csv(generations_path, generations)
    write_csv(metrics_path, metrics)
    write_csv(grouped_path, grouped)
    write_csv(rankings_path, rankings)
    json_path.write_text(
        json.dumps(
            {
                "model": args.model,
                "embedding_model": args.embedding_model,
                "dataset_cases_per_task": args.dataset_cases_per_task,
                "samples": args.samples,
                "temperature": args.temperature,
                "top_p": args.top_p,
                "total_generation_calls": total_requests,
                "batch_count": args.batch_count,
                "batch_index": args.batch_index,
                "tasks": TASK_ORDER,
                "datasets_by_task": DATASETS_BY_TASK,
                "perturbation_alignment": {
                    "source": "pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md",
                    "perturbations": perturbations,
                    "scope": "Same perturbation taxonomy as the three-task PDR validation; applied to instruction text only.",
                },
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
        "# Four-Task Similarity Sweep",
        "",
        f"- Model: `{args.model}`",
        f"- Embedding model: `{args.embedding_model}`",
        f"- Cases per task: `{args.dataset_cases_per_task}`",
        f"- Samples per clean / perturbed prompt: `{args.samples}`",
        f"- Tasks: `{', '.join(TASK_ORDER)}`",
        f"- Datasets: `{', '.join(DATASETS_BY_TASK[task] for task in TASK_ORDER)}`",
        f"- Perturbations: `{', '.join(perturbations)}`",
        "- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.",
        f"- Batch: `{args.batch_index}/{args.batch_count}`",
        f"- Total generation calls: `{total_requests}`",
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
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
