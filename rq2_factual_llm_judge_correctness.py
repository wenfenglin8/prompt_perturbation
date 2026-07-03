import argparse
import csv
import json
import re
import statistics
import time
from pathlib import Path

from promptrobust_reference_pdr_eval import pdr, post_json, read_api_key


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
DEFAULT_GENERATIONS = RESULTS_DIR / "generations_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv"
DEFAULT_PDR_METRICS = RESULTS_DIR / "pdr_metrics_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv"
DEFAULT_SEMANTIC_METRICS = RESULTS_DIR / "rq2_semantic_correctness_metrics.csv"


def read_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames or list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def extract_question(prompt: str) -> str:
    match = re.search(r"\n\nQuestion:\s*(.*)", prompt, flags=re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


def judge_factual_equivalence(
    api_key: str,
    model: str,
    question: str,
    reference_answer: str,
    output: str,
) -> tuple[int, str]:
    prompt = f"""
You are evaluating factual QA answer equivalence.

Question:
{question}

Accepted reference answer(s):
{reference_answer}

Candidate model answer:
{output}

Decide whether the candidate answer is factually equivalent to at least one reference answer.

Guidelines:
- Mark correct if the candidate directly gives the same entity, date, number, location, or short answer.
- Mark correct if the candidate includes the correct answer in a longer sentence without contradiction.
- Mark incorrect if it gives a different answer, refuses, is ambiguous, or contradicts the reference.
- Do not require exact wording.
- Be strict about negation.

Return only valid JSON:
{{"correct": true or false, "reason": "short reason"}}
""".strip()
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a strict factual answer equivalence judge."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "top_p": 1,
        "response_format": {"type": "json_object"},
    }
    data = post_json("https://api.openai.com/v1/chat/completions", api_key, payload)
    content = data["choices"][0]["message"]["content"].strip()
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, flags=re.DOTALL)
        if not match:
            raise
        parsed = json.loads(match.group(0))
    return (1 if bool(parsed.get("correct")) else 0), str(parsed.get("reason", "")).strip()


def factual_generation_rows(generation_rows: list[dict]) -> list[dict]:
    return [row for row in generation_rows if row["task"] == "factual_qa"]


def judgment_key(row: dict) -> str:
    return "|".join([row["case_id"], row["version"], row["sample_idx"]])


def load_existing_judgments(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    rows = read_csv(path)
    return {judgment_key(row): row for row in rows}


def compute_factual_pdr_metrics(judgments: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, str, str], dict[str, list[int]]] = {}
    for row in judgments:
        key = (row["case_id"], row["task"], row["dataset"], row["perturbation"])
        grouped.setdefault(key, {"original": [], "perturbed": []})
        grouped[key][row["version"]].append(int(row["llm_correct"]))

    metric_rows = []
    for (case_id, task, dataset, perturbation), versions in sorted(grouped.items()):
        original = versions["original"]
        perturbed = versions["perturbed"]
        clean_single = original[0]
        perturbed_single = perturbed[0]
        clean_mean = statistics.mean(original)
        perturbed_mean = statistics.mean(perturbed)
        clean_noise = statistics.pstdev(original) if len(original) > 1 else 0.0
        perturbed_noise = statistics.pstdev(perturbed) if len(perturbed) > 1 else 0.0
        metric_rows.append(
            {
                "case_id": case_id,
                "task": task,
                "dataset": dataset,
                "perturbation": perturbation,
                "clean_single_correct": clean_single,
                "perturbed_single_correct": perturbed_single,
                "single_sample_pdr": pdr(clean_single, perturbed_single),
                "clean_mean_correctness": clean_mean,
                "perturbed_mean_correctness": perturbed_mean,
                "repeated_sampling_pdr": pdr(clean_mean, perturbed_mean),
                "correctness_sample_noise": (clean_noise + perturbed_noise) / 2.0,
            }
        )
    return metric_rows


def merge_pdr_metrics(original_metrics: list[dict], factual_metrics: list[dict]) -> list[dict]:
    factual_by_case = {row["case_id"]: row for row in factual_metrics}
    merged = []
    for row in original_metrics:
        if row["task"] == "factual_qa":
            merged.append(factual_by_case[row["case_id"]])
        else:
            merged.append(row)
    return merged


def apply_pdr_to_semantic_metrics(semantic_rows: list[dict], pdr_rows: list[dict]) -> list[dict]:
    pdr_by_case = {row["case_id"]: row for row in pdr_rows}
    output = []
    for row in semantic_rows:
        pdr_row = pdr_by_case[row["case_id"]]
        updated = dict(row)
        for field in [
            "clean_single_correct",
            "perturbed_single_correct",
            "single_sample_pdr",
            "clean_mean_correctness",
            "perturbed_mean_correctness",
            "repeated_sampling_pdr",
            "correctness_sample_noise",
        ]:
            updated[field] = pdr_row[field]
        clean_single = float(updated["clean_single_correct"])
        perturbed_single = float(updated["perturbed_single_correct"])
        clean_mean = float(updated["clean_mean_correctness"])
        perturbed_mean = float(updated["perturbed_mean_correctness"])
        single_drop = clean_single - perturbed_single
        repeated_drop = clean_mean - perturbed_mean
        updated["single_pass_rate_drop"] = single_drop
        updated["abs_single_pass_rate_change"] = abs(single_drop)
        updated["repeated_pass_rate_drop"] = repeated_drop
        updated["abs_repeated_pass_rate_change"] = abs(repeated_drop)
        updated["harmful_correctness_drop"] = 1 if repeated_drop > 0 else 0
        updated["correctness_changed"] = 1 if clean_mean != perturbed_mean else 0
        output.append(updated)
    return output


def write_explanation(path: Path, model: str, judgment_count: int, factual_metrics: list[dict]) -> None:
    changed = sum(1 for row in factual_metrics if float(row["clean_mean_correctness"]) != float(row["perturbed_mean_correctness"]))
    harmful = sum(1 for row in factual_metrics if float(row["clean_mean_correctness"]) > float(row["perturbed_mean_correctness"]))
    lines = [
        "# RQ2 Factual QA LLM Equivalence Correctness",
        "",
        "This run replaces only the `factual_qa` correctness labels with an LLM equivalence judge.",
        "Math and code correctness are unchanged from the original PDR run.",
        "",
        f"- Judge model: `{model}`",
        f"- Judged factual outputs: `{judgment_count}`",
        f"- Factual case-level comparisons: `{len(factual_metrics)}`",
        f"- Factual cases with repeated correctness change: `{changed}`",
        f"- Factual cases with harmful correctness drop: `{harmful}`",
        "",
        "The judge accepts semantically equivalent short answers and longer answers that contain the correct answer without contradiction.",
        "This is a sensitivity analysis for the strict normalized exact-match factual correctness used in the original run.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generations", type=Path, default=DEFAULT_GENERATIONS)
    parser.add_argument("--original-pdr-metrics", type=Path, default=DEFAULT_PDR_METRICS)
    parser.add_argument("--semantic-metrics", type=Path, default=DEFAULT_SEMANTIC_METRICS)
    parser.add_argument("--judge-model", default="gpt-4o-mini")
    parser.add_argument("--output-tag", default="rq2_semantic_correctness_llm_fact")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--sleep", type=float, default=0.05)
    args = parser.parse_args()

    api_key = read_api_key()
    generation_rows = read_csv(args.generations)
    factual_rows = factual_generation_rows(generation_rows)
    judgments_path = RESULTS_DIR / f"{args.output_tag}_factual_judgments.csv"
    factual_pdr_path = RESULTS_DIR / f"{args.output_tag}_factual_pdr_metrics.csv"
    combined_pdr_path = RESULTS_DIR / f"{args.output_tag}_combined_pdr_metrics.csv"
    semantic_metrics_path = RESULTS_DIR / f"{args.output_tag}_metrics.csv"
    explanation_path = RESULTS_DIR / f"{args.output_tag}_factual_judge_explanation.md"

    existing = load_existing_judgments(judgments_path) if args.resume else {}
    judgments = list(existing.values())
    total = len(factual_rows)
    print(f"Judging factual QA outputs with {args.judge_model}: {total} rows", flush=True)
    if existing:
        print(f"Resuming from {len(existing)}/{total} existing judgments.", flush=True)

    fieldnames = [
        "case_id",
        "task",
        "dataset",
        "perturbation",
        "version",
        "sample_idx",
        "question",
        "reference_answer",
        "output",
        "exact_match_correct",
        "llm_correct",
        "judge_reason",
        "judge_model",
    ]
    for idx, row in enumerate(factual_rows, start=1):
        key = judgment_key(row)
        pct = idx / total * 100
        if key in existing:
            print(f"Judgment {idx}/{total} ({pct:.1f}%) already complete: {key}", flush=True)
            continue
        print(f"Judgment {idx}/{total} ({pct:.1f}%): {key}", flush=True)
        correct, reason = judge_factual_equivalence(
            api_key,
            args.judge_model,
            extract_question(row["prompt"]),
            row["reference_answer"],
            row["output"],
        )
        judged = {
            "case_id": row["case_id"],
            "task": row["task"],
            "dataset": row["dataset"],
            "perturbation": row["perturbation"],
            "version": row["version"],
            "sample_idx": row["sample_idx"],
            "question": extract_question(row["prompt"]),
            "reference_answer": row["reference_answer"],
            "output": row["output"],
            "exact_match_correct": row["correct"],
            "llm_correct": correct,
            "judge_reason": reason,
            "judge_model": args.judge_model,
        }
        judgments.append(judged)
        write_csv(judgments_path, judgments, fieldnames)
        time.sleep(args.sleep)

    judgments = sorted(judgments, key=lambda item: (item["case_id"], item["version"], int(item["sample_idx"])))
    write_csv(judgments_path, judgments, fieldnames)
    factual_pdr = compute_factual_pdr_metrics(judgments)
    write_csv(factual_pdr_path, factual_pdr)
    combined_pdr = merge_pdr_metrics(read_csv(args.original_pdr_metrics), factual_pdr)
    write_csv(combined_pdr_path, combined_pdr)
    updated_semantic = apply_pdr_to_semantic_metrics(read_csv(args.semantic_metrics), combined_pdr)
    write_csv(semantic_metrics_path, updated_semantic)
    write_explanation(explanation_path, args.judge_model, len(judgments), factual_pdr)

    print(f"Wrote {judgments_path}", flush=True)
    print(f"Wrote {factual_pdr_path}", flush=True)
    print(f"Wrote {combined_pdr_path}", flush=True)
    print(f"Wrote {semantic_metrics_path}", flush=True)
    print(f"Wrote {explanation_path}", flush=True)


if __name__ == "__main__":
    main()
