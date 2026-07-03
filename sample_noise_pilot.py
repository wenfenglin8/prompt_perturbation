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

from reference_perturbations import add_surface_noise, perturb_instruction


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"


CASES = [
    {
        "id": "fact_01",
        "task": "factual_qa",
        "original": "What is the capital city of Canada? Answer in one short sentence.",
    },
    {
        "id": "fact_02",
        "task": "factual_qa",
        "original": "Who wrote the novel Pride and Prejudice? Answer briefly.",
    },
    {
        "id": "math_01",
        "task": "math_reasoning",
        "original": "A shop sells pencils in packs of 8. If Maya buys 6 packs and gives away 11 pencils, how many pencils does she have left? Show the calculation.",
    },
    {
        "id": "math_02",
        "task": "math_reasoning",
        "original": "A train travels 180 miles in 3 hours. What is its average speed in miles per hour? Give the numeric answer.",
    },
    {
        "id": "code_01",
        "task": "code_generation",
        "original": "Write a Python function named is_palindrome(s) that returns True if s is a palindrome after ignoring spaces and letter case.",
    },
    {
        "id": "writing_01",
        "task": "open_ended_writing",
        "original": "Write a concise paragraph explaining why prompt wording can affect large language model outputs.",
    },
]


PROMPTROBUST_CASES = [
    {
        "id": "promptrobust_sst2_01",
        "task": "sst2_sentiment",
        "original": "Determine whether the movie review is positive or negative. Answer with exactly one label: positive or negative.\n\nReview: a warm, funny, engaging film.",
        "perturbed": add_surface_noise(
            "Determine whether the movie review is positive or negative. Answer with exactly one label: positive or negative."
        )
        + "\n\nReview: a warm, funny, engaging film.",
    },
    {
        "id": "promptrobust_sst2_02",
        "task": "sst2_sentiment",
        "original": "Determine whether the movie review is positive or negative. Answer with exactly one label: positive or negative.\n\nReview: dull, lifeless, and far too long.",
        "perturbed": add_surface_noise(
            "Determine whether the movie review is positive or negative. Answer with exactly one label: positive or negative."
        )
        + "\n\nReview: dull, lifeless, and far too long.",
    },
]


PROMPTROBUST_HARD_CASES = [
    {
        "id": "promptrobust_hard_sst2_01",
        "task": "sst2_sentiment_hard",
        "original": "Determine whether the movie review is positive or negative. Answer with exactly one label: positive or negative.\n\nReview: uneven and frequently frustrating, but its final act is surprisingly moving.",
        "perturbed": add_surface_noise(
            "Determine whether the movie review is positive or negative. Answer with exactly one label: positive or negative."
        )
        + "\n\nReview: uneven and frequently frustrating, but its final act is surprisingly moving.",
    },
    {
        "id": "promptrobust_hard_sst2_02",
        "task": "sst2_sentiment_hard",
        "original": "Determine whether the movie review is positive or negative. Answer with exactly one label: positive or negative.\n\nReview: not especially original, yet charming enough to keep me smiling.",
        "perturbed": add_surface_noise(
            "Determine whether the movie review is positive or negative. Answer with exactly one label: positive or negative."
        )
        + "\n\nReview: not especially original, yet charming enough to keep me smiling.",
    },
    {
        "id": "promptrobust_hard_sst2_03",
        "task": "sst2_sentiment_hard",
        "original": "Determine whether the movie review is positive or negative. Answer with exactly one label: positive or negative.\n\nReview: beautifully shot, but emotionally empty and slow.",
        "perturbed": add_surface_noise(
            "Determine whether the movie review is positive or negative. Answer with exactly one label: positive or negative."
        )
        + "\n\nReview: beautifully shot, but emotionally empty and slow.",
    },
    {
        "id": "promptrobust_hard_sst2_04",
        "task": "sst2_sentiment_hard",
        "original": "Determine whether the movie review is positive or negative. Answer with exactly one label: positive or negative.\n\nReview: I wanted to dislike it, but the performances won me over.",
        "perturbed": add_surface_noise(
            "Determine whether the movie review is positive or negative. Answer with exactly one label: positive or negative."
        )
        + "\n\nReview: I wanted to dislike it, but the performances won me over.",
    },
]


def surface_noise_perturb_instruction(text: str) -> str:
    return add_surface_noise(text)


def build_proposal_cases(api_key: str, model: str) -> list[dict]:
    cases = []
    for case in CASES:
        cases.append(
            {
                **case,
                "perturbed": perturb_instruction(
                    case["original"],
                    "paraphrase",
                    case["task"],
                    api_key,
                    model,
                ),
            }
        )
    return cases


def load_promptrobust_squad_math_cases(max_per_task: int = 2) -> list[dict]:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError(
            "The datasets package is required for the promptrobust_squad_math suite."
        ) from exc

    cases = []

    squad = load_dataset("squad_v2", split=f"validation[:{max_per_task}]")
    for idx, item in enumerate(squad):
        instruction = (
            "Read the passage and answer the question. If the answer cannot be found in the passage, "
            "say unanswerable. Answer in one concise sentence."
        )
        prompt_body = f"\n\nPassage: {item['context']}\n\nQuestion: {item['question']}"
        cases.append(
            {
                "id": f"promptrobust_squad_v2_{idx + 1:02d}",
                "task": "squad_v2_factual_qa",
                "original": instruction + prompt_body,
                "perturbed": surface_noise_perturb_instruction(instruction) + prompt_body,
            }
        )

    math_ds = load_dataset("DigitalLearningGmbH/MATH-lighteval", split=f"test[:{max_per_task}]")
    for idx, item in enumerate(math_ds):
        instruction = (
            "As a mathematics instructor, calculate the answer to the following problem. "
            "Show your reasoning and put the final answer at the end."
        )
        prompt_body = f"\n\nProblem: {item['problem']}"
        cases.append(
            {
                "id": f"promptrobust_math_{idx + 1:02d}",
                "task": "math_reasoning",
                "original": instruction + prompt_body,
                "perturbed": surface_noise_perturb_instruction(instruction) + prompt_body,
            }
        )

    return cases


def load_posix_mmlu_bbh_cases(max_per_task: int = 2) -> list[dict]:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError("The datasets package is required for the posix_mmlu_bbh suite.") from exc

    cases = []

    mmlu = load_dataset("cais/mmlu", "all", split=f"test[:{max_per_task}]")
    labels = ["A", "B", "C", "D"]
    for idx, item in enumerate(mmlu):
        choices = "\n".join(
            f"({label}) {choice}" for label, choice in zip(labels, item["choices"])
        )
        original = (
            "Answer the following multiple-choice question. "
            "Choose the single best option and answer with the option letter only."
            f"\n\nSubject: {item['subject']}\nQuestion: {item['question']}\n{choices}"
        )
        perturbed = perturb_instruction(original, "formatting", "mmlu_multiple_choice_reasoning")
        cases.append(
            {
                "id": f"posix_mmlu_{idx + 1:02d}",
                "task": "mmlu_multiple_choice_reasoning",
                "original": original,
                "perturbed": perturbed,
            }
        )

    bbh = load_dataset(
        "maveriq/bigbenchhard",
        "logical_deduction_three_objects",
        split=f"train[:{max_per_task}]",
    )
    for idx, item in enumerate(bbh):
        original = (
            "Solve the following reasoning problem. Think carefully, then answer with the correct option only."
            f"\n\n{item['input']}"
        )
        perturbed = perturb_instruction(original, "formatting", "bbh_logical_deduction")
        cases.append(
            {
                "id": f"posix_bbh_logical_deduction_{idx + 1:02d}",
                "task": "bbh_logical_deduction",
                "original": original,
                "perturbed": perturbed,
            }
        )

    return cases


def load_reference_four_task_cases(max_per_task: int = 1, api_key: str | None = None, model: str = "gpt-4o-mini") -> list[dict]:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError("The datasets package is required for the reference_four_task suite.") from exc

    cases = []

    squad = load_dataset("squad_v2", split=f"validation[:{max_per_task}]")
    for idx, item in enumerate(squad):
        instruction = (
            "Read the passage and answer the question. If the answer cannot be found in the passage, "
            "say unanswerable. Answer in one concise sentence."
        )
        prompt_body = f"\n\nPassage: {item['context']}\n\nQuestion: {item['question']}"
        cases.append(
            {
                "id": f"ref_squad_v2_{idx + 1:02d}",
                "task": "factual_qa",
                "original": instruction + prompt_body,
                "perturbed": perturb_instruction(instruction, "paraphrase", "factual_qa", api_key, model)
                + prompt_body,
            }
        )

    math_ds = load_dataset("DigitalLearningGmbH/MATH-lighteval", split=f"test[:{max_per_task}]")
    for idx, item in enumerate(math_ds):
        instruction = (
            "As a mathematics instructor, calculate the answer to the following problem. "
            "Show your reasoning and put the final answer at the end."
        )
        prompt_body = f"\n\nProblem: {item['problem']}"
        cases.append(
            {
                "id": f"ref_math_{idx + 1:02d}",
                "task": "math_reasoning",
                "original": instruction + prompt_body,
                "perturbed": perturb_instruction(instruction, "paraphrase", "math_reasoning", api_key, model)
                + prompt_body,
            }
        )

    human_eval = load_dataset("openai/openai_humaneval", split=f"test[:{max_per_task}]")
    for idx, item in enumerate(human_eval):
        prompt = item["prompt"].rstrip()
        cases.append(
            {
                "id": f"ref_humaneval_{idx + 1:02d}",
                "task": "code_generation",
                "original": (
                    "Complete the following Python function. Return only valid Python code, with no explanation."
                    f"\n\n{prompt}"
                ),
                "perturbed": perturb_instruction(
                    "Complete the following Python function. Return only valid Python code, with no explanation.",
                    "paraphrase",
                    "code_generation",
                    api_key,
                    model,
                )
                + f"\n\n{prompt}",
            }
        )

    alpaca = load_dataset("tatsu-lab/alpaca", split=f"train[:{max_per_task}]")
    for idx, item in enumerate(alpaca):
        instruction = item["instruction"].strip()
        input_text = item.get("input", "").strip()
        input_block = f"\n\nInput:\n{input_text}" if input_text else ""
        cases.append(
            {
                "id": f"ref_alpaca_{idx + 1:02d}",
                "task": "open_ended_writing",
                "original": f"Respond to the following instruction clearly and directly.\n\nInstruction:\n{instruction}{input_block}",
                "perturbed": f"{perturb_instruction('Respond to the following instruction clearly and directly.', 'paraphrase', 'open_ended_writing', api_key, model)}\n\nRequest:\n{instruction}{input_block}",
            }
        )

    return cases


def read_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key
    key_file = ROOT / "api.txt"
    if key_file.exists():
        return key_file.read_text(encoding="utf-8").strip()
    raise RuntimeError("OPENAI_API_KEY is not set and api.txt was not found.")


def post_json(url: str, api_key: str, payload: dict, timeout: int = 90) -> dict:
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"{response.status_code} {response.text[:1000]}")
    return response.json()


def generate_text(api_key: str, model: str, prompt: str, temperature: float, top_p: float) -> str:
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a precise assistant. Answer the user request directly.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "top_p": top_p,
    }
    data = post_json("https://api.openai.com/v1/chat/completions", api_key, payload)
    return data["choices"][0]["message"]["content"].strip()


def embed_texts(api_key: str, model: str, texts: list[str]) -> np.ndarray:
    payload = {"model": model, "input": texts}
    data = post_json("https://api.openai.com/v1/embeddings", api_key, payload)
    vectors = [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
    arr = np.array(vectors, dtype=float)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    return arr / np.maximum(norms, 1e-12)


def avg_pairwise_distance(vectors: np.ndarray) -> float:
    distances = []
    for i, j in itertools.combinations(range(len(vectors)), 2):
        distances.append(max(0.0, 1.0 - float(np.dot(vectors[i], vectors[j]))))
    return float(statistics.mean(distances)) if distances else 0.0


def avg_cross_distance(a: np.ndarray, b: np.ndarray) -> float:
    distances = []
    for i in range(len(a)):
        for j in range(len(b)):
            distances.append(max(0.0, 1.0 - float(np.dot(a[i], b[j]))))
    return float(statistics.mean(distances))


def bootstrap_probability_between_exceeds_noise(
    original_vectors: np.ndarray,
    perturbed_vectors: np.ndarray,
    rounds: int,
    seed: int,
) -> float:
    rng = np.random.default_rng(seed)
    n_original = len(original_vectors)
    n_perturbed = len(perturbed_vectors)
    wins = 0
    for _ in range(rounds):
        oi = rng.integers(0, n_original, n_original)
        pi = rng.integers(0, n_perturbed, n_perturbed)
        o = original_vectors[oi]
        p = perturbed_vectors[pi]
        original_noise = avg_pairwise_distance(o)
        perturbed_noise = avg_pairwise_distance(p)
        baseline = (original_noise + perturbed_noise) / 2.0
        between = avg_cross_distance(o, p)
        if between > baseline:
            wins += 1
    return wins / rounds


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--embedding-model", default="text-embedding-3-small")
    parser.add_argument("--samples", type=int, default=4)
    parser.add_argument("--max-cases", type=int, default=None)
    parser.add_argument("--case-ids", default=None, help="Comma-separated case ids to run.")
    parser.add_argument(
        "--suite",
        choices=[
            "proposal",
            "promptrobust",
            "promptrobust_hard",
            "promptrobust_squad_math",
            "posix_mmlu_bbh",
            "reference_four_task",
        ],
        default="proposal",
        help="Use proposal pilot cases or PromptRobust-style prompt-attack cases.",
    )
    parser.add_argument(
        "--dataset-cases-per-task",
        type=int,
        default=2,
        help="Number of examples per task to load for dataset-backed suites.",
    )
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--sleep", type=float, default=0.2)
    parser.add_argument("--bootstrap-rounds", type=int, default=1000)
    parser.add_argument("--output-tag", default="", help="Optional suffix for result filenames.")
    args = parser.parse_args()

    api_key = read_api_key()
    RESULTS_DIR.mkdir(exist_ok=True)

    generation_rows = []
    metric_rows = []

    if args.suite == "promptrobust":
        case_pool = PROMPTROBUST_CASES
    elif args.suite == "promptrobust_hard":
        case_pool = PROMPTROBUST_HARD_CASES
    elif args.suite == "promptrobust_squad_math":
        case_pool = load_promptrobust_squad_math_cases(args.dataset_cases_per_task)
    elif args.suite == "posix_mmlu_bbh":
        case_pool = load_posix_mmlu_bbh_cases(args.dataset_cases_per_task)
    elif args.suite == "reference_four_task":
        case_pool = load_reference_four_task_cases(args.dataset_cases_per_task, api_key, args.model)
    else:
        case_pool = build_proposal_cases(api_key, args.model)

    if args.case_ids:
        wanted = {item.strip() for item in args.case_ids.split(",") if item.strip()}
        cases = [case for case in case_pool if case["id"] in wanted]
        missing = wanted - {case["id"] for case in cases}
        if missing:
            raise ValueError(f"Unknown case id(s): {', '.join(sorted(missing))}")
    else:
        cases = case_pool[: args.max_cases] if args.max_cases is not None else case_pool
    print(f"Running suite={args.suite}, {len(cases)} case(s), {args.samples} sample(s) per prompt version.")

    for case in cases:
        outputs = {"original": [], "perturbed": []}
        for version in ["original", "perturbed"]:
            prompt = case[version]
            for sample_idx in range(args.samples):
                text = generate_text(api_key, args.model, prompt, args.temperature, args.top_p)
                outputs[version].append(text)
                generation_rows.append(
                    {
                        "case_id": case["id"],
                        "task": case["task"],
                        "version": version,
                        "sample_idx": sample_idx,
                        "prompt": prompt,
                        "output": text,
                    }
                )
                time.sleep(args.sleep)

        all_texts = outputs["original"] + outputs["perturbed"]
        vectors = embed_texts(api_key, args.embedding_model, all_texts)
        original_vectors = vectors[: args.samples]
        perturbed_vectors = vectors[args.samples :]

        original_noise = avg_pairwise_distance(original_vectors)
        perturbed_noise = avg_pairwise_distance(perturbed_vectors)
        noise_baseline = (original_noise + perturbed_noise) / 2.0
        uncorrected_single_drift = max(
            0.0,
            1.0 - float(np.dot(original_vectors[0], perturbed_vectors[0])),
        )
        raw_perturbation_drift = avg_cross_distance(original_vectors, perturbed_vectors)
        corrected_drift = raw_perturbation_drift - noise_baseline
        corrected_drift_clipped = max(0.0, corrected_drift)
        signal_to_noise = raw_perturbation_drift / noise_baseline if noise_baseline > 0 else float("inf")
        bootstrap_prob = bootstrap_probability_between_exceeds_noise(
            original_vectors,
            perturbed_vectors,
            args.bootstrap_rounds,
            seed=abs(hash(case["id"])) % (2**32),
        )

        metric_rows.append(
            {
                "case_id": case["id"],
                "task": case["task"],
                "original_noise": original_noise,
                "perturbed_noise": perturbed_noise,
                "noise_baseline": noise_baseline,
                "uncorrected_single_drift": uncorrected_single_drift,
                "raw_perturbation_drift": raw_perturbation_drift,
                "noise_corrected_drift": corrected_drift,
                "noise_corrected_drift_clipped": corrected_drift_clipped,
                "signal_to_noise_ratio": signal_to_noise,
                "bootstrap_p_between_gt_noise": bootstrap_prob,
            }
        )

    suffix = f"_{args.output_tag}" if args.output_tag else ""
    generations_path = RESULTS_DIR / f"generations{suffix}.csv"
    metrics_csv_path = RESULTS_DIR / f"noise_metrics{suffix}.csv"
    metrics_json_path = RESULTS_DIR / f"noise_metrics{suffix}.json"
    report_path = RESULTS_DIR / f"sample_noise_report{suffix}.md"

    write_csv(
        generations_path,
        generation_rows,
        ["case_id", "task", "version", "sample_idx", "prompt", "output"],
    )
    write_csv(
        metrics_csv_path,
        metric_rows,
        [
            "case_id",
            "task",
            "original_noise",
            "perturbed_noise",
            "noise_baseline",
            "uncorrected_single_drift",
            "raw_perturbation_drift",
            "noise_corrected_drift",
            "noise_corrected_drift_clipped",
            "signal_to_noise_ratio",
            "bootstrap_p_between_gt_noise",
        ],
    )

    summary = {
        "model": args.model,
        "suite": args.suite,
        "embedding_model": args.embedding_model,
        "samples_per_prompt_version": args.samples,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "metrics": metric_rows,
    }
    metrics_json_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    avg_raw = statistics.mean(row["raw_perturbation_drift"] for row in metric_rows)
    avg_uncorrected_single = statistics.mean(row["uncorrected_single_drift"] for row in metric_rows)
    avg_noise = statistics.mean(row["noise_baseline"] for row in metric_rows)
    avg_corrected = statistics.mean(row["noise_corrected_drift_clipped"] for row in metric_rows)
    noise_share = avg_noise / avg_raw if avg_raw > 0 else 0.0

    lines = [
        "# Sample Noise Pilot Report",
        "",
        f"- Suite: `{args.suite}`",
        f"- Model: `{args.model}`",
        f"- Embedding model: `{args.embedding_model}`",
        f"- Samples per original/perturbed prompt: `{args.samples}`",
        f"- Decoding: temperature `{args.temperature}`, top_p `{args.top_p}`",
        "",
        "## Aggregate Result",
        "",
        f"- Average uncorrected single-sample drift: `{avg_uncorrected_single:.4f}`",
        f"- Average raw perturbation drift: `{avg_raw:.4f}`",
        f"- Average sample-noise baseline: `{avg_noise:.4f}`",
        f"- Average noise-corrected drift: `{avg_corrected:.4f}`",
        f"- Estimated share of raw drift explainable by sampling noise: `{noise_share:.1%}`",
        "",
        "Interpretation: raw prompt-perturbation drift overstates the perturbation effect whenever the noise baseline is non-trivial. The noise-corrected value estimates the part of the observed drift that remains after accounting for ordinary repeated-generation variability.",
        "",
        "## Per-Item Metrics",
        "",
        "| case | task | uncorrected single drift | noise baseline | raw drift | corrected drift | SNR | bootstrap P(raw>noise) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in metric_rows:
        lines.append(
            f"| {row['case_id']} | {row['task']} | {row['uncorrected_single_drift']:.4f} | "
            f"{row['noise_baseline']:.4f} | "
            f"{row['raw_perturbation_drift']:.4f} | {row['noise_corrected_drift_clipped']:.4f} | "
            f"{row['signal_to_noise_ratio']:.2f} | {row['bootstrap_p_between_gt_noise']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Link to Haase et al.",
            "",
            "Haase et al. argue that LLM evaluation based on a single generation conflates prompt effects with sampling variability. This pilot operationalizes that claim for prompt perturbation: first estimate within-prompt variability from repeated generations, then subtract that baseline from between-prompt drift. A perturbation should be treated as meaningful only when its between-version drift clearly exceeds the within-version noise baseline.",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {generations_path}")
    print(f"Wrote {metrics_csv_path}")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
