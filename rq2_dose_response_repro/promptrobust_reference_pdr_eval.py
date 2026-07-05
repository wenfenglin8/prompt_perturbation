import argparse
import csv
import json
import multiprocessing
import os
import re
import statistics
import time
from pathlib import Path

import requests

from reference_perturbations import REFERENCE_PERTURBATIONS, perturb_instruction


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"


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
            {
                "role": "system",
                "content": "You are a precise assistant. Follow the requested output format exactly.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "top_p": top_p,
    }
    data = post_json("https://api.openai.com/v1/chat/completions", api_key, payload)
    return data["choices"][0]["message"]["content"].strip()


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\.\-/]", " ", text)
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_boxed_answer(solution: str) -> str:
    matches = re.findall(r"\\boxed\{([^{}]+)\}", solution)
    if matches:
        return matches[-1].strip()
    lines = [line.strip() for line in solution.splitlines() if line.strip()]
    return lines[-1] if lines else solution.strip()


def extract_model_final_answer(output: str) -> str:
    boxed = re.findall(r"\\boxed\{([^{}]+)\}", output)
    if boxed:
        return boxed[-1].strip()
    patterns = [
        r"final answer\s*(?:is|:)?\s*([^\n]+)",
        r"answer\s*(?:is|:)?\s*([^\n]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, output, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip().rstrip(".")
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return lines[-1].strip().rstrip(".") if lines else output.strip()


def is_squad_correct(output: str, answers: list[str]) -> bool:
    normalized_output = normalize_text(output)
    return any(normalized_output == normalize_text(answer) for answer in answers)


def is_math_correct(output: str, reference_solution: str) -> bool:
    predicted = normalize_text(extract_model_final_answer(output))
    expected = normalize_text(extract_boxed_answer(reference_solution))
    return predicted == expected


def strip_code_fence(output: str) -> str:
    text = output.strip()
    fenced = re.search(r"```(?:python)?\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        return fenced.group(1).strip()
    return text


def _humaneval_worker(code_candidates: list[str], test_code: str, entry_point: str, queue: multiprocessing.Queue) -> None:
    namespace = {}
    last_error = "failed"
    for code in code_candidates:
        namespace.clear()
        try:
            exec(code, namespace)
            exec(test_code, namespace)
            namespace["check"](namespace[entry_point])
        except Exception as exc:
            last_error = type(exc).__name__
            continue
        queue.put((True, "passed"))
        return
    queue.put((False, last_error))


def is_humaneval_correct(
    output: str,
    test_code: str,
    entry_point: str,
    prompt_prefix: str = "",
    timeout_seconds: float = 5.0,
) -> bool:
    completion = strip_code_fence(output)
    code_candidates = []
    if prompt_prefix:
        code_candidates.append(prompt_prefix.rstrip() + "\n" + completion)
    code_candidates.append(completion)
    queue: multiprocessing.Queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=_humaneval_worker, args=(code_candidates, test_code, entry_point, queue))
    process.start()
    process.join(timeout_seconds)
    if process.is_alive():
        process.terminate()
        process.join(1)
        return False
    if queue.empty():
        return False
    passed, _ = queue.get()
    return bool(passed)


def load_cases(max_per_task: int, perturbations: list[str], tasks: set[str], api_key: str, model: str) -> list[dict]:
    try:
        from datasets import Dataset
    except ImportError as exc:
        raise RuntimeError("The datasets package is required.") from exc

    cases = []

    if "factual_qa" in tasks:
        squad_arrow = (
            Path.home()
            / ".cache"
            / "huggingface"
            / "datasets"
            / "squad_v2"
            / "squad_v2"
            / "0.0.0"
            / "3ffb306f725f7d2ce8394bc1873b24868140c412"
            / "squad_v2-validation.arrow"
        )
        if not squad_arrow.exists():
            raise RuntimeError(f"SQuAD V2 local Arrow file was not found: {squad_arrow}")
        squad = Dataset.from_file(str(squad_arrow))
        squad_count = 0
        for item in squad:
            answers = [answer for answer in item["answers"]["text"] if answer.strip()]
            if not answers:
                continue
            instruction = "Read the passage and answer the question. Answer with the exact short answer only."
            prompt_body = f"\n\nPassage: {item['context']}\n\nQuestion: {item['question']}"
            for perturbation in perturbations:
                cases.append(
                    {
                        "id": f"promptrobust_pdr_{perturbation}_squad_{squad_count + 1:02d}",
                        "task": "factual_qa",
                        "dataset": "SQuAD V2",
                        "perturbation": perturbation,
                        "original": instruction + prompt_body,
                        "perturbed": perturb_instruction(instruction, perturbation, "factual_qa", api_key, model) + prompt_body,
                        "answers": answers,
                    }
                )
            squad_count += 1
            if squad_count >= max_per_task:
                break

    if "math_reasoning" in tasks:
        math_arrow = (
            Path.home()
            / ".cache"
            / "huggingface"
            / "datasets"
            / "DigitalLearningGmbH___math-lighteval"
            / "default"
            / "0.0.0"
            / "0530c78699ea5e8eb5530600900e1f328b48acad"
            / "math-lighteval-test.arrow"
        )
        if not math_arrow.exists():
            raise RuntimeError(f"MATH local Arrow file was not found: {math_arrow}")
        math_ds = Dataset.from_file(str(math_arrow))
        for idx, item in enumerate(math_ds.select(range(max_per_task))):
            instruction = "Solve the mathematics problem. Put the final answer only on the last line."
            prompt_body = f"\n\nProblem: {item['problem']}"
            for perturbation in perturbations:
                cases.append(
                    {
                        "id": f"promptrobust_pdr_{perturbation}_math_{idx + 1:02d}",
                        "task": "math_reasoning",
                        "dataset": "MATH",
                        "perturbation": perturbation,
                        "original": instruction + prompt_body,
                        "perturbed": perturb_instruction(instruction, perturbation, "math_reasoning", api_key, model) + prompt_body,
                        "solution": item["solution"],
                    }
                )

    if "code_generation" in tasks:
        human_eval_arrow = (
            Path.home()
            / ".cache"
            / "huggingface"
            / "datasets"
            / "openai___openai_humaneval"
            / "openai_humaneval"
            / "0.0.0"
            / "7dce6050a7d6d172f3cc5c32aa97f52fa1a2e544"
            / "openai_humaneval-test.arrow"
        )
        if not human_eval_arrow.exists():
            raise RuntimeError(f"HumanEval local Arrow file was not found: {human_eval_arrow}")
        human_eval = Dataset.from_file(str(human_eval_arrow))
        for idx, item in enumerate(human_eval.select(range(max_per_task))):
            instruction = "Complete the following Python function. Return only valid Python code, with no explanation."
            prompt_body = f"\n\n{item['prompt'].rstrip()}"
            for perturbation in perturbations:
                cases.append(
                    {
                        "id": f"promptrobust_pdr_{perturbation}_humaneval_{idx + 1:02d}",
                        "task": "code_generation",
                        "dataset": "HumanEval",
                        "perturbation": perturbation,
                        "original": instruction + prompt_body,
                        "perturbed": perturb_instruction(instruction, perturbation, "code_generation", api_key, model) + prompt_body,
                        "code_prompt": item["prompt"].rstrip(),
                        "test": item["test"],
                        "entry_point": item["entry_point"],
                    }
                )

    return cases


def pdr(clean_performance: float, perturbed_performance: float) -> float:
    if clean_performance <= 0:
        return 0.0
    return (clean_performance - perturbed_performance) / clean_performance


def performance_loss(performance: float) -> float:
    return 1.0 - performance


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--dataset-cases-per-task", type=int, default=2)
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--sleep", type=float, default=0.2)
    parser.add_argument("--output-tag", default="promptrobust_reference_pdr")
    parser.add_argument(
        "--perturbations",
        default="all",
        help="Comma-separated perturbations: paraphrase,reordering,formatting,context_injection,surface_noise, or all.",
    )
    parser.add_argument(
        "--tasks",
        default="factual_qa,math_reasoning",
        help="Comma-separated tasks: factual_qa,math_reasoning,code_generation.",
    )
    args = parser.parse_args()

    api_key = read_api_key()
    RESULTS_DIR.mkdir(exist_ok=True)
    if args.perturbations.strip().lower() == "all":
        perturbations = REFERENCE_PERTURBATIONS
    else:
        perturbations = [item.strip() for item in args.perturbations.split(",") if item.strip()]
    unknown = sorted(set(perturbations) - set(REFERENCE_PERTURBATIONS))
    if unknown:
        raise ValueError(f"Unknown perturbation(s): {', '.join(unknown)}")
    tasks = {item.strip() for item in args.tasks.split(",") if item.strip()}
    task_order = ["factual_qa", "math_reasoning", "code_generation"]
    unknown_tasks = sorted(tasks - set(task_order))
    if unknown_tasks:
        raise ValueError(f"Unknown task(s): {', '.join(unknown_tasks)}")
    print("Loading dataset-backed PromptRobust-aligned cases...", flush=True)
    cases = load_cases(args.dataset_cases_per_task, perturbations, tasks, api_key, args.model)

    generation_rows = []
    metric_rows = []

    print(f"Running {len(cases)} PromptRobust-aligned case(s), {args.samples} sample(s) per prompt version.", flush=True)
    total_requests = len(cases) * 2 * args.samples
    completed_requests = 0
    for case_idx, case in enumerate(cases, start=1):
        print(
            f"Running case {case_idx}/{len(cases)}: {case['id']} "
            f"({case['task']}, {case['perturbation']})",
            flush=True,
        )
        correctness = {"original": [], "perturbed": []}
        for version in ["original", "perturbed"]:
            for sample_idx in range(args.samples):
                percent_before = (completed_requests / total_requests) * 100
                print(
                    f"Progress {completed_requests}/{total_requests} "
                    f"({percent_before:.1f}%) - requesting {version} sample {sample_idx + 1}/{args.samples}",
                    flush=True,
                )
                output = generate_text(api_key, args.model, case[version], args.temperature, args.top_p)
                completed_requests += 1
                percent_after = (completed_requests / total_requests) * 100
                print(
                    f"Progress {completed_requests}/{total_requests} ({percent_after:.1f}%) complete",
                    flush=True,
                )
                if case["task"] == "factual_qa":
                    correct = is_squad_correct(output, case["answers"])
                    reference = " | ".join(case["answers"])
                elif case["task"] == "math_reasoning":
                    correct = is_math_correct(output, case["solution"])
                    reference = extract_boxed_answer(case["solution"])
                elif case["task"] == "code_generation":
                    correct = is_humaneval_correct(output, case["test"], case["entry_point"], case["code_prompt"])
                    reference = f"HumanEval unit tests for {case['entry_point']}"
                else:
                    raise ValueError(f"Unsupported task: {case['task']}")
                correctness[version].append(1 if correct else 0)
                generation_rows.append(
                    {
                        "case_id": case["id"],
                        "task": case["task"],
                        "dataset": case["dataset"],
                        "perturbation": case["perturbation"],
                        "version": version,
                        "sample_idx": sample_idx,
                        "prompt": case[version],
                        "output": output,
                        "reference_answer": reference,
                        "correct": int(correct),
                    }
                )
                time.sleep(args.sleep)

        clean_single = correctness["original"][0]
        perturbed_single = correctness["perturbed"][0]
        clean_mean = statistics.mean(correctness["original"])
        perturbed_mean = statistics.mean(correctness["perturbed"])
        clean_loss = performance_loss(clean_mean)
        perturbed_loss = performance_loss(perturbed_mean)
        corrected_pdr = perturbed_loss - clean_loss
        clean_noise = statistics.pstdev(correctness["original"]) if len(correctness["original"]) > 1 else 0.0
        perturbed_noise = statistics.pstdev(correctness["perturbed"]) if len(correctness["perturbed"]) > 1 else 0.0
        correctness_noise = (clean_noise + perturbed_noise) / 2.0

        metric_rows.append(
            {
                "case_id": case["id"],
                "task": case["task"],
                "dataset": case["dataset"],
                "perturbation": case["perturbation"],
                "clean_single_correct": clean_single,
                "perturbed_single_correct": perturbed_single,
                "clean_mean_correctness": clean_mean,
                "perturbed_mean_correctness": perturbed_mean,
                "uncorrected_pdr_loss": clean_loss,
                "perturbed_pdr_loss": perturbed_loss,
                "corrected_pdr": corrected_pdr,
                "correctness_sample_noise": correctness_noise,
            }
        )

    suffix = f"_{args.output_tag}" if args.output_tag else ""
    generations_path = RESULTS_DIR / f"generations{suffix}.csv"
    metrics_csv_path = RESULTS_DIR / f"pdr_metrics{suffix}.csv"
    metrics_json_path = RESULTS_DIR / f"pdr_metrics{suffix}.json"
    report_path = RESULTS_DIR / f"pdr_report{suffix}.md"

    with generations_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "case_id",
                "task",
                "dataset",
                "perturbation",
                "version",
                "sample_idx",
                "prompt",
                "output",
                "reference_answer",
                "correct",
            ],
        )
        writer.writeheader()
        writer.writerows(generation_rows)

    with metrics_csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(metric_rows[0].keys()))
        writer.writeheader()
        writer.writerows(metric_rows)

    summary = {
        "model": args.model,
        "samples_per_prompt_version": args.samples,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "dataset_cases_per_task": args.dataset_cases_per_task,
        "perturbations": perturbations,
        "tasks": sorted(tasks),
        "reference_alignment": {
            "paper": "PromptRobust / PromptBench",
            "datasets": sorted({row["dataset"] for row in metric_rows}),
            "perturbation": perturbations,
            "evaluation": "Performance Drop Rate (PDR)",
        },
        "metrics": metric_rows,
    }
    metrics_json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    avg_clean_single = statistics.mean(row["clean_single_correct"] for row in metric_rows)
    avg_perturbed_single = statistics.mean(row["perturbed_single_correct"] for row in metric_rows)
    avg_clean_repeated = statistics.mean(row["clean_mean_correctness"] for row in metric_rows)
    avg_perturbed_repeated = statistics.mean(row["perturbed_mean_correctness"] for row in metric_rows)
    dataset_uncorrected_pdr = performance_loss(avg_clean_repeated)
    dataset_perturbed_loss = performance_loss(avg_perturbed_repeated)
    dataset_corrected_pdr = dataset_perturbed_loss - dataset_uncorrected_pdr

    group_rows = []
    for perturbation in perturbations:
        for task in task_order:
            rows = [
                row
                for row in metric_rows
                if row["perturbation"] == perturbation and row["task"] == task
            ]
            if not rows:
                continue
            clean_single = statistics.mean(row["clean_single_correct"] for row in rows)
            perturbed_single = statistics.mean(row["perturbed_single_correct"] for row in rows)
            clean_repeated = statistics.mean(row["clean_mean_correctness"] for row in rows)
            perturbed_repeated = statistics.mean(row["perturbed_mean_correctness"] for row in rows)
            uncorrected = performance_loss(clean_repeated)
            perturbed_loss = performance_loss(perturbed_repeated)
            corrected = perturbed_loss - uncorrected
            group_rows.append(
                {
                    "perturbation": perturbation,
                    "task": task,
                    "n": len(rows),
                    "clean_single": clean_single,
                    "perturbed_single": perturbed_single,
                    "clean_repeated": clean_repeated,
                    "perturbed_repeated": perturbed_repeated,
                    "uncorrected_pdr": uncorrected,
                    "perturbed_loss": perturbed_loss,
                    "corrected_pdr": corrected,
                }
            )

    lines = [
        "# PromptRobust-Aligned PDR Evaluation",
        "",
        "This run aligns the small validation with PromptRobust / PromptBench as closely as the local setup allows:",
        "",
        f"- Datasets: `{', '.join(sorted({row['dataset'] for row in metric_rows}))}`.",
        f"- Tasks: `{', '.join(task for task in task_order if task in tasks)}`.",
        f"- Perturbations: `{', '.join(perturbations)}` applied to the instruction only.",
        "- Evaluation criterion: loss-based Performance Drop Rate (PDR), using task correctness as performance.",
        "- Uncorrected PDR: clean-prompt loss from repeated clean generations, `1 - mean(clean correctness)`.",
        "- Corrected PDR: additional perturbed-prompt loss, `(1 - mean(perturbed correctness)) - (1 - mean(clean correctness))`.",
        "- Code generation correctness: HumanEval pass@1-style unit-test pass/fail; completions are evaluated as HumanEval prompt + model completion, with standalone full-code outputs accepted as a fallback.",
        "",
        "## Aggregate Result",
        "",
        f"- Average clean single-sample correctness: `{avg_clean_single:.4f}`",
        f"- Average perturbed single-sample correctness: `{avg_perturbed_single:.4f}`",
        f"- Average clean repeated correctness: `{avg_clean_repeated:.4f}`",
        f"- Average perturbed repeated correctness: `{avg_perturbed_repeated:.4f}`",
        f"- Dataset-level uncorrected PDR loss: `{dataset_uncorrected_pdr:.4f}`",
        f"- Dataset-level perturbed PDR loss: `{dataset_perturbed_loss:.4f}`",
        f"- Dataset-level corrected PDR: `{dataset_corrected_pdr:.4f}`",
        "",
        "## Grouped Result",
        "",
        "| perturbation | task | n | clean single | perturbed single | clean repeated | perturbed repeated | uncorrected PDR loss | perturbed loss | corrected PDR |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in group_rows:
        lines.append(
            f"| {row['perturbation']} | {row['task']} | {row['n']} | "
            f"{row['clean_single']:.4f} | {row['perturbed_single']:.4f} | "
            f"{row['clean_repeated']:.4f} | {row['perturbed_repeated']:.4f} | "
            f"{row['uncorrected_pdr']:.4f} | {row['perturbed_loss']:.4f} | {row['corrected_pdr']:.4f} |"
        )
    lines.extend(
        [
        "",
        "## Per-Item Metrics",
        "",
        "| case | perturbation | task | dataset | clean single | perturbed single | clean mean | perturbed mean | uncorrected PDR loss | perturbed loss | corrected PDR | correctness noise |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    )
    for row in metric_rows:
        lines.append(
            f"| {row['case_id']} | {row['perturbation']} | {row['task']} | {row['dataset']} | "
            f"{row['clean_single_correct']} | {row['perturbed_single_correct']} | "
            f"{row['clean_mean_correctness']:.4f} | {row['perturbed_mean_correctness']:.4f} | "
            f"{row['uncorrected_pdr_loss']:.4f} | {row['perturbed_pdr_loss']:.4f} | "
            f"{row['corrected_pdr']:.4f} | "
            f"{row['correctness_sample_noise']:.4f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The uncorrected condition estimates clean-prompt loss from repeated clean-prompt generations compared with the reference answer. "
            "The corrected condition estimates additional perturbed-prompt loss by subtracting the clean-prompt loss from the perturbed-prompt loss. "
            "This separates baseline task failure under the clean prompt from additional loss attributable to prompt perturbation.",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {generations_path}")
    print(f"Wrote {metrics_csv_path}")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
