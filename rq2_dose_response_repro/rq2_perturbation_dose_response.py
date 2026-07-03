import argparse
import csv
import json
import re
import statistics
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

from four_task_similarity_sweep import (
    RESULTS_DIR,
    avg_cross_distance,
    avg_pairwise_distance,
    embed_texts,
    read_api_key,
)
from promptrobust_reference_pdr_eval import (
    extract_boxed_answer,
    generate_text,
    is_humaneval_correct,
    is_math_correct,
    is_squad_correct,
    pdr,
)
from reference_perturbations import add_surface_noise
from rq2_semantic_correctness_analysis import pearson, spearman


ROOT = Path(__file__).resolve().parent
OBJECTIVE_TASKS = ["factual_qa", "long_factual_qa", "math_reasoning", "code_generation"]
LONG_FACTQA_CASES = [
    {
        "topic": "normans",
        "context": (
            "The Normans were descended from Norse Viking settlers who established themselves in the region "
            "that became Normandy in northern France during the 10th and 11th centuries. Their early leadership "
            "is associated with Rollo, a Viking leader who received land from the West Frankish king Charles the "
            "Simple. Over time the Normans adopted the French language, Christianity, and local customs while "
            "retaining a reputation for military organization."
        ),
        "question": "Who were the Normans, where did they settle, and how did their culture change over time?",
        "reference": (
            "The Normans were descendants of Norse Viking settlers who settled in Normandy in northern France "
            "during the 10th and 11th centuries. Their early settlement is associated with Rollo and an agreement "
            "with Charles the Simple. Over time they adopted French language, Christianity, and local customs."
        ),
        "required_fact_groups": [
            ["norse", "viking"],
            ["normandy", "northern france"],
            ["10th", "11th"],
            ["rollo"],
            ["french"],
            ["christian"],
        ],
    },
    {
        "topic": "photosynthesis",
        "context": (
            "Photosynthesis is the process by which plants, algae, and some bacteria convert light energy into "
            "chemical energy. In plants, chlorophyll in chloroplasts captures light, while carbon dioxide and "
            "water are used to make glucose. Oxygen is released as a byproduct. The glucose can be used for "
            "growth, stored for later, or broken down through cellular respiration."
        ),
        "question": "Explain how photosynthesis works and what products it creates.",
        "reference": (
            "Photosynthesis uses chlorophyll in chloroplasts to capture light energy. Plants use carbon dioxide "
            "and water to produce glucose, and oxygen is released as a byproduct. The glucose stores chemical "
            "energy that can support growth or later respiration."
        ),
        "required_fact_groups": [
            ["chlorophyll"],
            ["chloroplast"],
            ["light"],
            ["carbon dioxide", "co2"],
            ["water"],
            ["glucose", "sugar"],
            ["oxygen"],
        ],
    },
    {
        "topic": "magna_carta",
        "context": (
            "Magna Carta was issued in 1215 after English barons rebelled against King John. It was sealed at "
            "Runnymede and attempted to limit royal power by affirming that the king was subject to the law. "
            "Although many clauses addressed feudal disputes, later generations treated Magna Carta as an "
            "important symbol of due process, lawful judgment, and limits on arbitrary authority."
        ),
        "question": "What was Magna Carta, why was it issued, and why did it become historically important?",
        "reference": (
            "Magna Carta was issued in 1215 after barons challenged King John and it was sealed at Runnymede. "
            "It limited royal power by asserting that the king was subject to law. It later became important as "
            "a symbol of due process, lawful judgment, and constraints on arbitrary authority."
        ),
        "required_fact_groups": [
            ["1215"],
            ["king john"],
            ["baron"],
            ["runnymede"],
            ["limit", "limited", "subject to law"],
            ["due process", "lawful judgment", "arbitrary"],
        ],
    },
    {
        "topic": "apollo_11",
        "context": (
            "Apollo 11 was the NASA mission that first landed humans on the Moon. Neil Armstrong and Buzz Aldrin "
            "landed the lunar module Eagle on July 20, 1969, while Michael Collins remained in lunar orbit in "
            "the command module Columbia. Armstrong became the first person to walk on the lunar surface, and "
            "Aldrin joined him soon afterward. The mission returned lunar samples and demonstrated a successful "
            "crewed lunar landing."
        ),
        "question": "Summarize Apollo 11's main achievement and the roles of Armstrong, Aldrin, and Collins.",
        "reference": (
            "Apollo 11 first landed humans on the Moon on July 20, 1969. Neil Armstrong and Buzz Aldrin landed "
            "in the lunar module Eagle and walked on the surface, while Michael Collins stayed in lunar orbit "
            "aboard Columbia. The mission returned lunar samples and proved a crewed lunar landing was possible."
        ),
        "required_fact_groups": [
            ["moon"],
            ["july 20, 1969", "1969"],
            ["armstrong"],
            ["aldrin"],
            ["collins"],
            ["lunar orbit", "orbit"],
            ["eagle"],
        ],
    },
    {
        "topic": "penicillin",
        "context": (
            "Penicillin was discovered by Alexander Fleming in 1928 after he noticed that a mold contaminating "
            "one of his bacterial culture plates inhibited bacterial growth. The active substance came from a "
            "Penicillium mold. Later work by Howard Florey, Ernst Chain, and others helped purify and mass "
            "produce penicillin, turning it into an effective antibiotic that transformed treatment of bacterial "
            "infections."
        ),
        "question": "Describe how penicillin was discovered and why it mattered medically.",
        "reference": (
            "Alexander Fleming discovered penicillin in 1928 when Penicillium mold on a culture plate inhibited "
            "bacterial growth. Later researchers such as Howard Florey and Ernst Chain helped purify and mass "
            "produce it. Penicillin mattered because it became an effective antibiotic for treating bacterial "
            "infections."
        ),
        "required_fact_groups": [
            ["alexander fleming", "fleming"],
            ["1928"],
            ["mold", "penicillium"],
            ["bacterial growth", "bacteria"],
            ["florey"],
            ["chain"],
            ["antibiotic"],
        ],
    },
]
GENERATION_FIELDS = [
    "base_case_id",
    "task",
    "dataset",
    "perturbation_family",
    "strength_level",
    "strength_edits",
    "version",
    "sample_idx",
    "prompt",
    "output",
    "reference_answer",
    "correct",
]
METRIC_FIELDS = [
    "base_case_id",
    "task",
    "dataset",
    "perturbation_family",
    "strength_level",
    "strength_edits",
    "original_noise",
    "perturbed_noise",
    "noise_baseline",
    "raw_perturbation_drift",
    "noise_corrected_drift",
    "mean_cross_similarity",
    "mean_paired_similarity",
    "clean_single_correct",
    "perturbed_single_correct",
    "single_pass_rate_drop",
    "abs_single_pass_rate_change",
    "single_sample_pdr",
    "clean_mean_correctness",
    "perturbed_mean_correctness",
    "repeated_pass_rate_drop",
    "abs_repeated_pass_rate_change",
    "repeated_sampling_pdr",
    "harmful_correctness_drop",
    "correctness_changed",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv_fields(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def dataset_from_arrow(path: Path):
    from datasets import Dataset

    if not path.exists():
        raise RuntimeError(f"Dataset Arrow file was not found: {path}")
    return Dataset.from_file(str(path))


def load_base_cases(max_per_task: int, tasks: set[str]) -> list[dict]:
    base = Path.home() / ".cache" / "huggingface" / "datasets"
    cases = []

    if "factual_qa" in tasks:
        squad = dataset_from_arrow(
            base
            / "squad_v2"
            / "squad_v2"
            / "0.0.0"
            / "3ffb306f725f7d2ce8394bc1873b24868140c412"
            / "squad_v2-validation.arrow"
        )
        count = 0
        for item in squad:
            answers = [answer for answer in item["answers"]["text"] if answer.strip()]
            if not answers:
                continue
            instruction = "Read the passage and answer the question. Answer with the exact short answer only."
            body = f"\n\nPassage: {item['context']}\n\nQuestion: {item['question']}"
            cases.append(
                {
                    "base_case_id": f"rq2_dose_squad_{count + 1:02d}",
                    "task": "factual_qa",
                    "dataset": "SQuAD V2",
                    "instruction": instruction,
                    "body": body,
                    "original": instruction + body,
                    "answers": answers,
                }
            )
            count += 1
            if count >= max_per_task:
                break

    if "long_factual_qa" in tasks:
        instruction = (
            "Read the passage and answer the question in two to three complete sentences. "
            "Include all key facts needed to answer the question accurately."
        )
        for idx, item in enumerate(LONG_FACTQA_CASES[:max_per_task]):
            body = f"\n\nPassage: {item['context']}\n\nQuestion: {item['question']}"
            cases.append(
                {
                    "base_case_id": f"rq2_dose_longfact_{idx + 1:02d}",
                    "task": "long_factual_qa",
                    "dataset": "LongFactQA-Handwritten",
                    "instruction": instruction,
                    "body": body,
                    "original": instruction + body,
                    "reference": item["reference"],
                    "required_fact_groups": item["required_fact_groups"],
                }
            )

    if "math_reasoning" in tasks:
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
            cases.append(
                {
                    "base_case_id": f"rq2_dose_math_{idx + 1:02d}",
                    "task": "math_reasoning",
                    "dataset": "MATH",
                    "instruction": instruction,
                    "body": body,
                    "original": instruction + body,
                    "solution": item["solution"],
                }
            )

    if "code_generation" in tasks:
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
            cases.append(
                {
                    "base_case_id": f"rq2_dose_humaneval_{idx + 1:02d}",
                    "task": "code_generation",
                    "dataset": "HumanEval",
                    "instruction": instruction,
                    "body": body,
                    "original": instruction + body,
                    "code_prompt": item["prompt"].rstrip(),
                    "test": item["test"],
                    "entry_point": item["entry_point"],
                }
            )

    return sorted(cases, key=lambda row: (OBJECTIVE_TASKS.index(row["task"]), row["base_case_id"]))


def normalize_for_fact_match(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def is_long_factqa_correct(output: str, required_fact_groups: list[list[str]]) -> bool:
    normalized = normalize_for_fact_match(output)
    for aliases in required_fact_groups:
        if not any(normalize_for_fact_match(alias) in normalized for alias in aliases):
            return False
    return True


def reference_answer(case: dict) -> str:
    if case["task"] == "factual_qa":
        return " | ".join(case["answers"])
    if case["task"] == "long_factual_qa":
        return case["reference"]
    if case["task"] == "math_reasoning":
        return extract_boxed_answer(case["solution"])
    if case["task"] == "code_generation":
        return f"HumanEval unit tests for {case['entry_point']}"
    raise ValueError(f"Unsupported task: {case['task']}")


def score_output(case: dict, output: str) -> bool:
    if case["task"] == "factual_qa":
        return is_squad_correct(output, case["answers"])
    if case["task"] == "long_factual_qa":
        return is_long_factqa_correct(output, case["required_fact_groups"])
    if case["task"] == "math_reasoning":
        return is_math_correct(output, case["solution"])
    if case["task"] == "code_generation":
        return is_humaneval_correct(output, case["test"], case["entry_point"], case["code_prompt"])
    raise ValueError(f"Unsupported task: {case['task']}")


def perturbed_prompt(case: dict, edits: int) -> str:
    if edits <= 0:
        return case["original"]
    return add_surface_noise(case["instruction"], edits=edits) + case["body"]


def existing_rows(
    rows: list[dict],
    base_case_id: str,
    version: str,
    strength_edits: int | None,
    samples: int,
) -> list[dict]:
    selected = [
        row
        for row in rows
        if row["base_case_id"] == base_case_id
        and row["version"] == version
        and (strength_edits is None or int(row["strength_edits"]) == strength_edits)
    ]
    selected = sorted(selected, key=lambda row: int(row["sample_idx"]))
    if len(selected) >= samples:
        return selected[:samples]
    return []


def generation_row(
    case: dict,
    level_idx: int,
    edits: int,
    version: str,
    sample_idx: int,
    prompt: str,
    output: str,
    correct: bool,
) -> dict:
    return {
        "base_case_id": case["base_case_id"],
        "task": case["task"],
        "dataset": case["dataset"],
        "perturbation_family": "surface_noise",
        "strength_level": level_idx,
        "strength_edits": edits,
        "version": version,
        "sample_idx": sample_idx,
        "prompt": prompt,
        "output": output,
        "reference_answer": reference_answer(case),
        "correct": int(correct),
    }


def ensure_outputs(
    case: dict,
    level_idx: int,
    edits: int,
    version: str,
    prompt: str,
    samples: int,
    generation_rows: list[dict],
    api_key: str,
    model: str,
    temperature: float,
    top_p: float,
    sleep: float,
    progress: dict | None = None,
) -> list[dict]:
    cached = existing_rows(generation_rows, case["base_case_id"], version, edits, samples)
    if cached:
        return cached
    generated = []
    for sample_idx in range(samples):
        if progress:
            pct_before = progress["completed"] / progress["total"] * 100 if progress["total"] else 100.0
            progress_text = f"Progress {progress['completed']}/{progress['total']} ({pct_before:.1f}%) - "
        else:
            progress_text = ""
        print(
            f"{progress_text}Generating {case['base_case_id']} {version} level={level_idx} edits={edits} "
            f"sample {sample_idx + 1}/{samples}",
            flush=True,
        )
        output = generate_text(api_key, model, prompt, temperature, top_p)
        if progress:
            progress["completed"] += 1
            pct_after = progress["completed"] / progress["total"] * 100 if progress["total"] else 100.0
            print(f"Progress {progress['completed']}/{progress['total']} ({pct_after:.1f}%) complete", flush=True)
        correct = score_output(case, output)
        row = generation_row(case, level_idx, edits, version, sample_idx, prompt, output, correct)
        generation_rows.append(row)
        generated.append(row)
        time.sleep(sleep)
    return generated


def compute_metric_row(
    case: dict,
    level_idx: int,
    edits: int,
    original_rows: list[dict],
    perturbed_rows: list[dict],
    api_key: str,
    embedding_model: str,
) -> dict:
    clean_correctness = [float(row["correct"]) for row in original_rows]
    perturbed_correctness = [float(row["correct"]) for row in perturbed_rows]
    clean_single = clean_correctness[0]
    perturbed_single = perturbed_correctness[0]
    clean_mean = statistics.mean(clean_correctness)
    perturbed_mean = statistics.mean(perturbed_correctness)
    single_drop = clean_single - perturbed_single
    repeated_drop = clean_mean - perturbed_mean

    if edits <= 0:
        original_noise = 0.0
        perturbed_noise = 0.0
        noise_baseline = 0.0
        raw_drift = 0.0
        corrected_drift = 0.0
        mean_cross_similarity = 1.0
        mean_paired_similarity = 1.0
    else:
        original_texts = [(row.get("output") or " ").strip() or " " for row in original_rows]
        perturbed_texts = [(row.get("output") or " ").strip() or " " for row in perturbed_rows]
        vectors = embed_texts(api_key, embedding_model, original_texts + perturbed_texts)
        original_vectors = vectors[: len(original_texts)]
        perturbed_vectors = vectors[len(original_texts) :]
        original_noise = avg_pairwise_distance(original_vectors)
        perturbed_noise = avg_pairwise_distance(perturbed_vectors)
        noise_baseline = (original_noise + perturbed_noise) / 2.0
        raw_drift = avg_cross_distance(original_vectors, perturbed_vectors)
        corrected_drift = max(0.0, raw_drift - noise_baseline)
        mean_cross_similarity = 1.0 - raw_drift
        paired_count = min(len(original_vectors), len(perturbed_vectors))
        mean_paired_similarity = float(
            statistics.mean(
                float(np.dot(original_vectors[idx], perturbed_vectors[idx])) for idx in range(paired_count)
            )
        )

    return {
        "base_case_id": case["base_case_id"],
        "task": case["task"],
        "dataset": case["dataset"],
        "perturbation_family": "surface_noise",
        "strength_level": level_idx,
        "strength_edits": edits,
        "original_noise": original_noise,
        "perturbed_noise": perturbed_noise,
        "noise_baseline": noise_baseline,
        "raw_perturbation_drift": raw_drift,
        "noise_corrected_drift": corrected_drift,
        "mean_cross_similarity": mean_cross_similarity,
        "mean_paired_similarity": mean_paired_similarity,
        "clean_single_correct": clean_single,
        "perturbed_single_correct": perturbed_single,
        "single_pass_rate_drop": single_drop,
        "abs_single_pass_rate_change": abs(single_drop),
        "single_sample_pdr": pdr(clean_single, perturbed_single),
        "clean_mean_correctness": clean_mean,
        "perturbed_mean_correctness": perturbed_mean,
        "repeated_pass_rate_drop": repeated_drop,
        "abs_repeated_pass_rate_change": abs(repeated_drop),
        "repeated_sampling_pdr": pdr(clean_mean, perturbed_mean),
        "harmful_correctness_drop": 1 if repeated_drop > 0 else 0,
        "correctness_changed": 1 if clean_mean != perturbed_mean else 0,
    }


def mean(values: list[float]) -> float:
    return float(statistics.mean(values)) if values else 0.0


def grouped_by_level(rows: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[int(row["strength_level"]), int(row["strength_edits"])].append(row)
    output = []
    for (level, edits), scoped in sorted(grouped.items()):
        output.append(
            {
                "strength_level": level,
                "strength_edits": edits,
                "n": len(scoped),
                "mean_cross_similarity": mean([float(row["mean_cross_similarity"]) for row in scoped]),
                "mean_paired_similarity": mean([float(row["mean_paired_similarity"]) for row in scoped]),
                "mean_raw_perturbation_drift": mean([float(row["raw_perturbation_drift"]) for row in scoped]),
                "mean_noise_corrected_drift": mean([float(row["noise_corrected_drift"]) for row in scoped]),
                "mean_clean_correctness": mean([float(row["clean_mean_correctness"]) for row in scoped]),
                "mean_perturbed_correctness": mean([float(row["perturbed_mean_correctness"]) for row in scoped]),
                "mean_abs_repeated_pass_rate_change": mean(
                    [float(row["abs_repeated_pass_rate_change"]) for row in scoped]
                ),
                "mean_repeated_pass_rate_drop": mean([float(row["repeated_pass_rate_drop"]) for row in scoped]),
                "share_harmful_correctness_drop": mean([float(row["harmful_correctness_drop"]) for row in scoped]),
                "share_correctness_changed": mean([float(row["correctness_changed"]) for row in scoped]),
            }
        )
    return output


def grouped_by_task_level(rows: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["task"], int(row["strength_level"]), int(row["strength_edits"])].append(row)
    output = []
    for (task, level, edits), scoped in sorted(grouped.items()):
        output.append(
            {
                "task": task,
                "strength_level": level,
                "strength_edits": edits,
                "n": len(scoped),
                "mean_cross_similarity": mean([float(row["mean_cross_similarity"]) for row in scoped]),
                "mean_noise_corrected_drift": mean([float(row["noise_corrected_drift"]) for row in scoped]),
                "mean_abs_repeated_pass_rate_change": mean(
                    [float(row["abs_repeated_pass_rate_change"]) for row in scoped]
                ),
                "mean_repeated_pass_rate_drop": mean([float(row["repeated_pass_rate_drop"]) for row in scoped]),
                "share_harmful_correctness_drop": mean([float(row["harmful_correctness_drop"]) for row in scoped]),
                "share_correctness_changed": mean([float(row["correctness_changed"]) for row in scoped]),
            }
        )
    return output


def correlation_row(scope: str, rows: list[dict], x_field: str, y_field: str) -> dict:
    x = [float(row[x_field]) for row in rows]
    y = [float(row[y_field]) for row in rows]
    pearson_value = pearson(x, y)
    spearman_value = spearman(x, y)
    return {
        "scope": scope,
        "n": len(rows),
        "x": x_field,
        "y": y_field,
        "pearson": "" if pearson_value is None else pearson_value,
        "spearman": "" if spearman_value is None else spearman_value,
    }


def correlation_rows(rows: list[dict]) -> list[dict]:
    pairs = [
        ("strength_edits", "mean_cross_similarity"),
        ("strength_edits", "noise_corrected_drift"),
        ("strength_edits", "abs_repeated_pass_rate_change"),
        ("mean_cross_similarity", "abs_repeated_pass_rate_change"),
        ("mean_paired_similarity", "abs_repeated_pass_rate_change"),
        ("noise_corrected_drift", "abs_repeated_pass_rate_change"),
        ("mean_cross_similarity", "harmful_correctness_drop"),
        ("noise_corrected_drift", "harmful_correctness_drop"),
    ]
    output = []
    scopes = [("all_levels", rows), ("nonzero_levels", [row for row in rows if int(row["strength_edits"]) > 0])]
    for task in sorted({row["task"] for row in rows}):
        scopes.append((f"task:{task}", [row for row in rows if row["task"] == task]))
        scopes.append(
            (
                f"task_nonzero:{task}",
                [row for row in rows if row["task"] == task and int(row["strength_edits"]) > 0],
            )
        )
    for scope, scoped in scopes:
        if len(scoped) < 2:
            continue
        for x_field, y_field in pairs:
            output.append(correlation_row(scope, scoped, x_field, y_field))
    return output


def within_case_monotonic_rows(rows: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["base_case_id"]].append(row)
    output = []
    for base_case_id, scoped in sorted(grouped.items()):
        scoped = sorted(scoped, key=lambda row: int(row["strength_edits"]))
        if len(scoped) < 3:
            continue
        strength = [float(row["strength_edits"]) for row in scoped]
        similarity = [float(row["mean_cross_similarity"]) for row in scoped]
        corrected = [float(row["noise_corrected_drift"]) for row in scoped]
        abs_change = [float(row["abs_repeated_pass_rate_change"]) for row in scoped]
        task = scoped[0]["task"]
        output.append(
            {
                "base_case_id": base_case_id,
                "task": task,
                "n_levels": len(scoped),
                "spearman_strength_to_similarity": "" if spearman(strength, similarity) is None else spearman(strength, similarity),
                "spearman_strength_to_corrected_drift": ""
                if spearman(strength, corrected) is None
                else spearman(strength, corrected),
                "spearman_strength_to_abs_correctness_change": ""
                if spearman(strength, abs_change) is None
                else spearman(strength, abs_change),
                "spearman_similarity_to_abs_correctness_change": ""
                if spearman(similarity, abs_change) is None
                else spearman(similarity, abs_change),
            }
        )
    return output


def fmt(value: object, digits: int = 4) -> str:
    if value == "" or value is None:
        return "NA"
    return f"{float(value):.{digits}f}"


def markdown_table(rows: list[dict], fields: list[str]) -> str:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join(["---"] * len(fields)) + " |"]
    for row in rows:
        values = []
        for field in fields:
            value = row[field]
            values.append(fmt(value) if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def find_corr(rows: list[dict], scope: str, x: str, y: str) -> dict | None:
    for row in rows:
        if row["scope"] == scope and row["x"] == x and row["y"] == y:
            return row
    return None


def write_report(
    path: Path,
    metric_rows: list[dict],
    level_rows: list[dict],
    task_level_rows: list[dict],
    correlations: list[dict],
    monotonic: list[dict],
    args: argparse.Namespace,
) -> None:
    sim_to_change = find_corr(correlations, "nonzero_levels", "mean_cross_similarity", "abs_repeated_pass_rate_change")
    drift_to_change = find_corr(correlations, "nonzero_levels", "noise_corrected_drift", "abs_repeated_pass_rate_change")
    strength_to_similarity = find_corr(correlations, "all_levels", "strength_edits", "mean_cross_similarity")
    strength_to_change = find_corr(correlations, "all_levels", "strength_edits", "abs_repeated_pass_rate_change")
    monotonic_similarity_negative = [
        row
        for row in monotonic
        if row["spearman_strength_to_similarity"] != ""
        and float(row["spearman_strength_to_similarity"]) < 0
    ]
    monotonic_change_positive = [
        row
        for row in monotonic
        if row["spearman_strength_to_abs_correctness_change"] != ""
        and float(row["spearman_strength_to_abs_correctness_change"]) > 0
    ]
    similarity_statement = "NA"
    if sim_to_change and sim_to_change["spearman"] != "":
        sim_spearman = float(sim_to_change["spearman"])
        if sim_spearman < 0:
            similarity_statement = (
                f"Similarity-to-correctness Spearman on nonzero levels is `{fmt(sim_spearman)}`. "
                "This supports the claim that lower output similarity is associated with larger correctness change."
            )
        elif sim_spearman > 0:
            similarity_statement = (
                f"Similarity-to-correctness Spearman on nonzero levels is `{fmt(sim_spearman)}`. "
                "This does not support the expected lower-similarity / larger-correctness-change direction."
            )
        else:
            similarity_statement = (
                "Similarity-to-correctness Spearman on nonzero levels is `0.0000`, indicating no rank association."
            )
    drift_statement = "NA"
    if drift_to_change and drift_to_change["spearman"] != "":
        drift_spearman = float(drift_to_change["spearman"])
        if drift_spearman > 0:
            drift_statement = (
                f"Corrected-drift-to-correctness Spearman on nonzero levels is `{fmt(drift_spearman)}`. "
                "This supports the equivalent drift framing."
            )
        elif drift_spearman < 0:
            drift_statement = (
                f"Corrected-drift-to-correctness Spearman on nonzero levels is `{fmt(drift_spearman)}`. "
                "This does not support the expected corrected-drift / correctness-change direction at this scale."
            )
        else:
            drift_statement = (
                "Corrected-drift-to-correctness Spearman on nonzero levels is `0.0000`, indicating no rank association."
            )

    report = [
        "# RQ2 Surface-Noise Dose-Response Experiment",
        "",
        "## Question",
        "",
        "This experiment tests a stronger RQ2 design: within one perturbation family, surface noise is increased step by step, then output similarity and correctness change are measured at each severity level.",
        "",
        "The intended dose-response pattern is:",
        "",
        "```text",
        "surface-noise strength increases -> output similarity decreases -> correctness change increases",
        "```",
        "",
        "## Design",
        "",
        f"- Perturbation family: `surface_noise`",
        f"- Strength levels, measured as corrupted instruction words: `{', '.join(str(x) for x in args.levels)}`",
        f"- Tasks: `{', '.join(args.tasks)}`",
        f"- Cases per task: `{args.dataset_cases_per_task}`",
        f"- Samples per prompt version: `{args.samples}`",
        f"- Generation model: `{args.model}`",
        f"- Embedding model: `{args.embedding_model}`",
        f"- Case-level rows: `{len(metric_rows)}`",
        "",
        "Only the task instruction is perturbed; passages, math problems, and HumanEval function prompts are kept unchanged.",
        "",
        "## Mean By Strength",
        "",
        markdown_table(
            level_rows,
            [
                "strength_level",
                "strength_edits",
                "n",
                "mean_cross_similarity",
                "mean_noise_corrected_drift",
                "mean_abs_repeated_pass_rate_change",
                "mean_repeated_pass_rate_drop",
                "share_harmful_correctness_drop",
                "share_correctness_changed",
            ],
        ),
        "",
        "## Main Correlations",
        "",
        markdown_table(
            [
                row
                for row in [strength_to_similarity, strength_to_change, sim_to_change, drift_to_change]
                if row is not None
            ],
            ["scope", "n", "x", "y", "pearson", "spearman"],
        ),
        "",
        similarity_statement,
        drift_statement,
        "",
        "## Task x Strength Means",
        "",
        markdown_table(
            task_level_rows,
            [
                "task",
                "strength_level",
                "strength_edits",
                "n",
                "mean_cross_similarity",
                "mean_noise_corrected_drift",
                "mean_abs_repeated_pass_rate_change",
                "share_harmful_correctness_drop",
                "share_correctness_changed",
            ],
        ),
        "",
        "## Within-Case Monotonicity",
        "",
        f"- Cases where strength-to-similarity Spearman is negative: `{len(monotonic_similarity_negative)}/{len(monotonic)}`",
        f"- Cases where strength-to-absolute-correctness-change Spearman is positive: `{len(monotonic_change_positive)}/{len(monotonic)}`",
        "",
        "## Interpretation Guide",
        "",
        "- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.",
        "- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.",
        "- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.",
        "- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.",
        "",
    ]
    path.write_text("\n".join(report), encoding="utf-8")


def parse_int_list(value: str) -> list[int]:
    levels = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not levels:
        raise ValueError("At least one strength level is required.")
    if any(level < 0 for level in levels):
        raise ValueError("Strength levels must be nonnegative.")
    return sorted(dict.fromkeys(levels))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--embedding-model", default="text-embedding-3-small")
    parser.add_argument("--dataset-cases-per-task", type=int, default=2)
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--levels", type=parse_int_list, default=parse_int_list("0,1,2,4,8"))
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--sleep", type=float, default=0.2)
    parser.add_argument("--tasks", default="factual_qa,math_reasoning,code_generation")
    parser.add_argument("--output-tag", default="rq2_surface_noise_dose_response")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    args.tasks = [item.strip() for item in args.tasks.split(",") if item.strip()]
    unknown_tasks = sorted(set(args.tasks) - set(OBJECTIVE_TASKS))
    if unknown_tasks:
        raise ValueError(f"Unknown task(s): {', '.join(unknown_tasks)}")

    RESULTS_DIR.mkdir(exist_ok=True)
    generations_path = RESULTS_DIR / f"{args.output_tag}_generations.csv"
    metrics_path = RESULTS_DIR / f"{args.output_tag}_metrics.csv"
    level_path = RESULTS_DIR / f"{args.output_tag}_by_level.csv"
    task_level_path = RESULTS_DIR / f"{args.output_tag}_by_task_level.csv"
    correlations_path = RESULTS_DIR / f"{args.output_tag}_correlations.csv"
    monotonic_path = RESULTS_DIR / f"{args.output_tag}_within_case_monotonicity.csv"
    summary_path = RESULTS_DIR / f"{args.output_tag}_summary.json"
    report_path = RESULTS_DIR / f"{args.output_tag}_report.md"

    generation_rows = read_csv(generations_path) if args.resume else []
    metric_rows = read_csv(metrics_path) if args.resume else []
    completed = {
        (row["base_case_id"], int(row["strength_edits"]))
        for row in metric_rows
    }

    api_key = read_api_key()
    cases = load_base_cases(args.dataset_cases_per_task, set(args.tasks))
    generation_keys = {
        (
            row["base_case_id"],
            row["version"],
            int(row["strength_edits"]),
            int(row["sample_idx"]),
        )
        for row in generation_rows
        if not (row["version"] == "perturbed" and int(row["strength_edits"]) == 0)
    }
    total_generation_requests = len(cases) * args.samples * (1 + len([level for level in args.levels if level > 0]))
    progress = {"completed": len(generation_keys), "total": total_generation_requests}
    total_metric_rows = len(cases) * len(args.levels)
    print(
        f"Running surface-noise dose-response: {len(cases)} base cases, "
        f"{len(args.levels)} levels, {args.samples} samples/version.",
        flush=True,
    )
    if completed:
        print(f"Resuming from {len(completed)}/{len(cases) * len(args.levels)} completed metric rows.", flush=True)

    for case_idx, case in enumerate(cases, start=1):
        metric_pct = len(completed) / total_metric_rows * 100 if total_metric_rows else 100.0
        print(
            f"Metric progress {len(completed)}/{total_metric_rows} ({metric_pct:.1f}%) - "
            f"Base case {case_idx}/{len(cases)}: {case['base_case_id']} ({case['task']})",
            flush=True,
        )
        original_rows = ensure_outputs(
            case,
            0,
            0,
            "original",
            case["original"],
            args.samples,
            generation_rows,
            api_key,
            args.model,
            args.temperature,
            args.top_p,
            args.sleep,
            progress,
        )
        write_csv_fields(generations_path, generation_rows, GENERATION_FIELDS)

        for level_idx, edits in enumerate(args.levels):
            metric_key = (case["base_case_id"], edits)
            if metric_key in completed:
                metric_pct = len(completed) / total_metric_rows * 100 if total_metric_rows else 100.0
                print(
                    f"Metric progress {len(completed)}/{total_metric_rows} ({metric_pct:.1f}%) - "
                    f"Already complete: {case['base_case_id']} edits={edits}",
                    flush=True,
                )
                continue
            metric_pct = len(completed) / total_metric_rows * 100 if total_metric_rows else 100.0
            print(
                f"Metric progress {len(completed)}/{total_metric_rows} ({metric_pct:.1f}%) - "
                f"Computing {case['base_case_id']} edits={edits}",
                flush=True,
            )
            if edits <= 0:
                perturbed_rows = [
                    generation_row(
                        case,
                        level_idx,
                        edits,
                        "perturbed",
                        int(row["sample_idx"]),
                        case["original"],
                        row["output"],
                        bool(int(row["correct"])),
                    )
                    for row in original_rows
                ]
                generation_rows.extend(perturbed_rows)
            else:
                prompt = perturbed_prompt(case, edits)
                perturbed_rows = ensure_outputs(
                    case,
                    level_idx,
                    edits,
                    "perturbed",
                    prompt,
                    args.samples,
                    generation_rows,
                    api_key,
                    args.model,
                    args.temperature,
                    args.top_p,
                    args.sleep,
                    progress,
                )
            metric_row = compute_metric_row(
                case,
                level_idx,
                edits,
                original_rows,
                perturbed_rows,
                api_key,
                args.embedding_model,
            )
            metric_rows.append(metric_row)
            metric_rows = sorted(metric_rows, key=lambda row: (row["task"], row["base_case_id"], int(row["strength_edits"])))
            completed.add(metric_key)
            metric_pct = len(completed) / total_metric_rows * 100 if total_metric_rows else 100.0
            print(
                f"Metric progress {len(completed)}/{total_metric_rows} ({metric_pct:.1f}%) complete",
                flush=True,
            )
            write_csv_fields(generations_path, generation_rows, GENERATION_FIELDS)
            write_csv_fields(metrics_path, metric_rows, METRIC_FIELDS)

    level_rows = grouped_by_level(metric_rows)
    task_level_rows = grouped_by_task_level(metric_rows)
    correlations = correlation_rows(metric_rows)
    monotonic = within_case_monotonic_rows(metric_rows)
    write_csv_fields(level_path, level_rows, list(level_rows[0].keys()) if level_rows else [])
    write_csv_fields(task_level_path, task_level_rows, list(task_level_rows[0].keys()) if task_level_rows else [])
    write_csv_fields(correlations_path, correlations, list(correlations[0].keys()) if correlations else [])
    write_csv_fields(monotonic_path, monotonic, list(monotonic[0].keys()) if monotonic else [])
    summary = {
        "model": args.model,
        "embedding_model": args.embedding_model,
        "dataset_cases_per_task": args.dataset_cases_per_task,
        "samples": args.samples,
        "levels": args.levels,
        "tasks": args.tasks,
        "perturbation_family": "surface_noise",
        "case_level_rows": len(metric_rows),
        "by_level": level_rows,
        "correlations": correlations,
        "within_case_monotonicity": monotonic,
    }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    write_report(report_path, metric_rows, level_rows, task_level_rows, correlations, monotonic, args)
    print(f"Wrote {generations_path}", flush=True)
    print(f"Wrote {metrics_path}", flush=True)
    print(f"Wrote {level_path}", flush=True)
    print(f"Wrote {task_level_path}", flush=True)
    print(f"Wrote {correlations_path}", flush=True)
    print(f"Wrote {monotonic_path}", flush=True)
    print(f"Wrote {summary_path}", flush=True)
    print(f"Wrote {report_path}", flush=True)


if __name__ == "__main__":
    main()
