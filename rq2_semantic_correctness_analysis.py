import argparse
import csv
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Callable

import numpy as np

from four_task_similarity_sweep import (
    RESULTS_DIR,
    avg_cross_distance,
    avg_pairwise_distance,
    embed_texts,
    read_api_key,
    write_csv,
)


ROOT = Path(__file__).resolve().parent
DEFAULT_GENERATIONS = RESULTS_DIR / "generations_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv"
DEFAULT_PDR_METRICS = RESULTS_DIR / "pdr_metrics_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv"
OBJECTIVE_TASKS = {"factual_qa", "math_reasoning", "code_generation"}
METRIC_FIELDS = [
    "case_id",
    "task",
    "dataset",
    "perturbation",
    "uncorrected_single_drift",
    "original_noise",
    "perturbed_noise",
    "noise_baseline",
    "raw_perturbation_drift",
    "noise_corrected_drift",
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
    "correctness_sample_noise",
    "harmful_correctness_drop",
    "correctness_changed",
]


def read_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv_fields(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def to_float(value: str | float | int) -> float:
    return float(value)


def load_existing_metrics(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = read_csv(path)
    for row in rows:
        for field in METRIC_FIELDS:
            row.setdefault(field, "")
    return rows


def group_generation_rows(rows: list[dict], samples: int) -> list[dict]:
    groups = defaultdict(lambda: {"original": [], "perturbed": []})
    for row in rows:
        task = row["task"]
        if task not in OBJECTIVE_TASKS:
            continue
        version = row["version"]
        if version not in {"original", "perturbed"}:
            raise ValueError(f"Unexpected version {version!r} in {row['case_id']}")
        key = (row["case_id"], row["task"], row["dataset"], row["perturbation"])
        groups[key][version].append(row)

    cases = []
    for key, versions in groups.items():
        original = sorted(versions["original"], key=lambda row: int(row["sample_idx"]))
        perturbed = sorted(versions["perturbed"], key=lambda row: int(row["sample_idx"]))
        if len(original) != samples or len(perturbed) != samples:
            raise ValueError(
                f"{key[0]} expected {samples} original and {samples} perturbed rows, "
                f"got {len(original)} and {len(perturbed)}"
            )
        case_id, task, dataset, perturbation = key
        cases.append(
            {
                "case_id": case_id,
                "task": task,
                "dataset": dataset,
                "perturbation": perturbation,
                "original": original,
                "perturbed": perturbed,
            }
        )
    return sorted(cases, key=lambda item: (item["task"], item["perturbation"], item["case_id"]))


def load_pdr_metrics(path: Path) -> dict[tuple[str, str, str, str], dict]:
    rows = read_csv(path)
    metrics = {}
    for row in rows:
        task = row["task"]
        if task not in OBJECTIVE_TASKS:
            continue
        key = (row["case_id"], row["task"], row["dataset"], row["perturbation"])
        metrics[key] = row
    return metrics


def compute_semantic_row(case: dict, pdr_row: dict, api_key: str, embedding_model: str) -> dict:
    original_texts = [(row.get("output") or " ").strip() or " " for row in case["original"]]
    perturbed_texts = [(row.get("output") or " ").strip() or " " for row in case["perturbed"]]
    vectors = embed_texts(api_key, embedding_model, original_texts + perturbed_texts)
    original_vectors = vectors[: len(original_texts)]
    perturbed_vectors = vectors[len(original_texts) :]

    original_noise = avg_pairwise_distance(original_vectors)
    perturbed_noise = avg_pairwise_distance(perturbed_vectors)
    noise_baseline = (original_noise + perturbed_noise) / 2.0
    raw_perturbation_drift = avg_cross_distance(original_vectors, perturbed_vectors)
    noise_corrected_drift = max(0.0, raw_perturbation_drift - noise_baseline)
    uncorrected_single_drift = max(0.0, 1.0 - float(np.dot(original_vectors[0], perturbed_vectors[0])))

    clean_single_correct = to_float(pdr_row["clean_single_correct"])
    perturbed_single_correct = to_float(pdr_row["perturbed_single_correct"])
    clean_mean_correctness = to_float(pdr_row["clean_mean_correctness"])
    perturbed_mean_correctness = to_float(pdr_row["perturbed_mean_correctness"])
    single_pass_rate_drop = clean_single_correct - perturbed_single_correct
    repeated_pass_rate_drop = clean_mean_correctness - perturbed_mean_correctness

    return {
        "case_id": case["case_id"],
        "task": case["task"],
        "dataset": case["dataset"],
        "perturbation": case["perturbation"],
        "uncorrected_single_drift": uncorrected_single_drift,
        "original_noise": original_noise,
        "perturbed_noise": perturbed_noise,
        "noise_baseline": noise_baseline,
        "raw_perturbation_drift": raw_perturbation_drift,
        "noise_corrected_drift": noise_corrected_drift,
        "clean_single_correct": clean_single_correct,
        "perturbed_single_correct": perturbed_single_correct,
        "single_pass_rate_drop": single_pass_rate_drop,
        "abs_single_pass_rate_change": abs(single_pass_rate_drop),
        "single_sample_pdr": to_float(pdr_row["single_sample_pdr"]),
        "clean_mean_correctness": clean_mean_correctness,
        "perturbed_mean_correctness": perturbed_mean_correctness,
        "repeated_pass_rate_drop": repeated_pass_rate_drop,
        "abs_repeated_pass_rate_change": abs(repeated_pass_rate_drop),
        "repeated_sampling_pdr": to_float(pdr_row["repeated_sampling_pdr"]),
        "correctness_sample_noise": to_float(pdr_row["correctness_sample_noise"]),
        "harmful_correctness_drop": 1 if repeated_pass_rate_drop > 0 else 0,
        "correctness_changed": 1 if clean_mean_correctness != perturbed_mean_correctness else 0,
    }


def mean(values: list[float]) -> float:
    return float(statistics.mean(values)) if values else 0.0


def pearson(x: list[float], y: list[float]) -> float | None:
    if len(x) < 2 or len(x) != len(y):
        return None
    x_mean = mean(x)
    y_mean = mean(y)
    x_diffs = [value - x_mean for value in x]
    y_diffs = [value - y_mean for value in y]
    x_ss = sum(value * value for value in x_diffs)
    y_ss = sum(value * value for value in y_diffs)
    if x_ss <= 0.0 or y_ss <= 0.0:
        return None
    return sum(a * b for a, b in zip(x_diffs, y_diffs)) / math.sqrt(x_ss * y_ss)


def ranks(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda pair: pair[1])
    ranked = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranked[indexed[k][0]] = avg_rank
        i = j
    return ranked


def spearman(x: list[float], y: list[float]) -> float | None:
    if len(x) < 2 or len(x) != len(y):
        return None
    return pearson(ranks(x), ranks(y))


def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * p
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[int(position)]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def bootstrap_ci(
    rows: list[dict],
    x_field: str,
    y_field: str,
    corr_fn: Callable[[list[float], list[float]], float | None],
    samples: int,
    seed: int,
) -> tuple[float | None, float | None]:
    if len(rows) < 3 or samples <= 0:
        return None, None
    rng = random.Random(seed)
    estimates = []
    for _ in range(samples):
        selected = [rows[rng.randrange(len(rows))] for _ in range(len(rows))]
        x = [float(row[x_field]) for row in selected]
        y = [float(row[y_field]) for row in selected]
        value = corr_fn(x, y)
        if value is not None and not math.isnan(value):
            estimates.append(value)
    return percentile(estimates, 0.025), percentile(estimates, 0.975)


def permutation_p_value(
    rows: list[dict],
    x_field: str,
    y_field: str,
    corr_fn: Callable[[list[float], list[float]], float | None],
    samples: int,
    seed: int,
) -> float | None:
    if len(rows) < 3 or samples <= 0:
        return None
    x = [float(row[x_field]) for row in rows]
    y = [float(row[y_field]) for row in rows]
    observed = corr_fn(x, y)
    if observed is None or math.isnan(observed):
        return None
    rng = random.Random(seed)
    extreme = 1
    valid = 1
    for _ in range(samples):
        permuted_y = y[:]
        rng.shuffle(permuted_y)
        value = corr_fn(x, permuted_y)
        if value is None or math.isnan(value):
            continue
        valid += 1
        if abs(value) >= abs(observed):
            extreme += 1
    return extreme / valid


def correlation_rows(rows: list[dict], bootstrap_samples: int, seed: int) -> list[dict]:
    pairs = [
        ("noise_corrected_drift", "abs_repeated_pass_rate_change", "primary"),
        ("raw_perturbation_drift", "abs_repeated_pass_rate_change", "raw_auxiliary"),
        ("uncorrected_single_drift", "abs_repeated_pass_rate_change", "single_vs_repeated_auxiliary"),
        ("noise_corrected_drift", "repeated_pass_rate_drop", "signed_drop"),
        ("noise_corrected_drift", "harmful_correctness_drop", "harmful_drop_binary"),
        ("raw_perturbation_drift", "harmful_correctness_drop", "raw_harmful_drop_binary"),
        ("uncorrected_single_drift", "abs_single_pass_rate_change", "single_sample"),
        ("noise_corrected_drift", "abs_single_pass_rate_change", "single_change_auxiliary"),
    ]
    scopes = [("overall", "all", rows)]
    for task in sorted({row["task"] for row in rows}):
        scoped = [row for row in rows if row["task"] == task]
        scopes.append(("task", task, scoped))
    for perturbation in sorted({row["perturbation"] for row in rows}):
        scoped = [row for row in rows if row["perturbation"] == perturbation]
        scopes.append(("perturbation", perturbation, scoped))
    for task in sorted({row["task"] for row in rows}):
        for perturbation in sorted({row["perturbation"] for row in rows}):
            scoped = [row for row in rows if row["task"] == task and row["perturbation"] == perturbation]
            if len(scoped) >= 3:
                scopes.append(("task_perturbation", f"{task}:{perturbation}", scoped))

    output = []
    for scope_type, scope_value, scoped_rows in scopes:
        for x_field, y_field, label in pairs:
            x = [float(row[x_field]) for row in scoped_rows]
            y = [float(row[y_field]) for row in scoped_rows]
            pearson_value = pearson(x, y)
            spearman_value = spearman(x, y)
            ci_low, ci_high = bootstrap_ci(scoped_rows, x_field, y_field, spearman, bootstrap_samples, seed)
            spearman_p = permutation_p_value(scoped_rows, x_field, y_field, spearman, bootstrap_samples, seed)
            output.append(
                {
                    "scope_type": scope_type,
                    "scope_value": scope_value,
                    "n": len(scoped_rows),
                    "relationship": label,
                    "x": x_field,
                    "y": y_field,
                    "pearson": "" if pearson_value is None else pearson_value,
                    "spearman": "" if spearman_value is None else spearman_value,
                    "spearman_ci95_low": "" if ci_low is None else ci_low,
                    "spearman_ci95_high": "" if ci_high is None else ci_high,
                    "spearman_permutation_p_two_sided": "" if spearman_p is None else spearman_p,
                }
            )
    return output


def sample_noise_correction_comparison_rows(rows: list[dict], bootstrap_samples: int, seed: int) -> list[dict]:
    measures = [
        {
            "drift_measure": "noise_corrected_drift",
            "correction_status": "sample_noise_corrected",
            "sampling_design": "repeated_3x3",
            "correctness_target": "abs_repeated_pass_rate_change",
            "comparison_role": "primary_rq2_measure",
        },
        {
            "drift_measure": "raw_perturbation_drift",
            "correction_status": "uncorrected_raw_cross_drift",
            "sampling_design": "repeated_3x3",
            "correctness_target": "abs_repeated_pass_rate_change",
            "comparison_role": "same_target_uncorrected_baseline",
        },
        {
            "drift_measure": "uncorrected_single_drift",
            "correction_status": "uncorrected_single_pair",
            "sampling_design": "single_pair",
            "correctness_target": "abs_repeated_pass_rate_change",
            "comparison_role": "single_pair_to_repeated_target_baseline",
        },
        {
            "drift_measure": "uncorrected_single_drift",
            "correction_status": "uncorrected_single_pair",
            "sampling_design": "single_pair",
            "correctness_target": "abs_single_pass_rate_change",
            "comparison_role": "single_pair_internal_baseline",
        },
    ]
    scopes = [("overall", "all", rows)]
    for task in sorted({row["task"] for row in rows}):
        scopes.append(("task", task, [row for row in rows if row["task"] == task]))
    for perturbation in sorted({row["perturbation"] for row in rows}):
        scopes.append(("perturbation", perturbation, [row for row in rows if row["perturbation"] == perturbation]))

    output = []
    for scope_type, scope_value, scoped_rows in scopes:
        for measure in measures:
            x_field = measure["drift_measure"]
            y_field = measure["correctness_target"]
            x = [float(row[x_field]) for row in scoped_rows]
            y = [float(row[y_field]) for row in scoped_rows]
            pearson_value = pearson(x, y)
            spearman_value = spearman(x, y)
            ci_low, ci_high = bootstrap_ci(scoped_rows, x_field, y_field, spearman, bootstrap_samples, seed)
            spearman_p = permutation_p_value(scoped_rows, x_field, y_field, spearman, bootstrap_samples, seed)
            output.append(
                {
                    "scope_type": scope_type,
                    "scope_value": scope_value,
                    "n": len(scoped_rows),
                    **measure,
                    "pearson": "" if pearson_value is None else pearson_value,
                    "spearman": "" if spearman_value is None else spearman_value,
                    "spearman_ci95_low": "" if ci_low is None else ci_low,
                    "spearman_ci95_high": "" if ci_high is None else ci_high,
                    "spearman_permutation_p_two_sided": "" if spearman_p is None else spearman_p,
                }
            )
    return output


def paired_correlation_delta(
    rows: list[dict],
    corrected_field: str,
    baseline_field: str,
    y_field: str,
    corr_fn: Callable[[list[float], list[float]], float | None],
) -> float | None:
    corrected_x = [float(row[corrected_field]) for row in rows]
    baseline_x = [float(row[baseline_field]) for row in rows]
    y = [float(row[y_field]) for row in rows]
    corrected_value = corr_fn(corrected_x, y)
    baseline_value = corr_fn(baseline_x, y)
    if corrected_value is None or baseline_value is None:
        return None
    return corrected_value - baseline_value


def paired_delta_ci(
    rows: list[dict],
    corrected_field: str,
    baseline_field: str,
    y_field: str,
    corr_fn: Callable[[list[float], list[float]], float | None],
    samples: int,
    seed: int,
) -> tuple[float | None, float | None]:
    if len(rows) < 3 or samples <= 0:
        return None, None
    rng = random.Random(seed)
    estimates = []
    for _ in range(samples):
        selected = [rows[rng.randrange(len(rows))] for _ in range(len(rows))]
        value = paired_correlation_delta(selected, corrected_field, baseline_field, y_field, corr_fn)
        if value is not None and not math.isnan(value):
            estimates.append(value)
    return percentile(estimates, 0.025), percentile(estimates, 0.975)


def paired_delta_permutation_p_greater(
    rows: list[dict],
    corrected_field: str,
    baseline_field: str,
    y_field: str,
    corr_fn: Callable[[list[float], list[float]], float | None],
    samples: int,
    seed: int,
) -> float | None:
    observed = paired_correlation_delta(rows, corrected_field, baseline_field, y_field, corr_fn)
    if observed is None or math.isnan(observed):
        return None
    rng = random.Random(seed)
    y = [float(row[y_field]) for row in rows]
    corrected = [float(row[corrected_field]) for row in rows]
    baseline = [float(row[baseline_field]) for row in rows]
    extreme = 1
    valid = 1
    for _ in range(samples):
        permuted_corrected = []
        permuted_baseline = []
        for corrected_value, baseline_value in zip(corrected, baseline):
            if rng.random() < 0.5:
                permuted_corrected.append(corrected_value)
                permuted_baseline.append(baseline_value)
            else:
                permuted_corrected.append(baseline_value)
                permuted_baseline.append(corrected_value)
        corrected_corr = corr_fn(permuted_corrected, y)
        baseline_corr = corr_fn(permuted_baseline, y)
        if corrected_corr is None or baseline_corr is None:
            continue
        valid += 1
        if corrected_corr - baseline_corr >= observed:
            extreme += 1
    return extreme / valid


def sample_noise_correction_gain_rows(rows: list[dict], bootstrap_samples: int, seed: int) -> list[dict]:
    comparisons = [
        {
            "corrected_similarity_drift": "noise_corrected_drift",
            "baseline_similarity_drift": "raw_perturbation_drift",
            "baseline_type": "uncorrected_raw_cross_drift",
            "correctness_drift_target": "abs_repeated_pass_rate_change",
            "comparison_question": "Does sample-noise correction improve repeated-output correctness-drift indication over raw cross-drift?",
        },
        {
            "corrected_similarity_drift": "noise_corrected_drift",
            "baseline_similarity_drift": "uncorrected_single_drift",
            "baseline_type": "uncorrected_single_pair",
            "correctness_drift_target": "abs_repeated_pass_rate_change",
            "comparison_question": "Does sample-noise correction improve repeated-output correctness-drift indication over a single-pair baseline?",
        },
    ]
    scopes = [("overall", "all", rows)]
    for task in sorted({row["task"] for row in rows}):
        scopes.append(("task", task, [row for row in rows if row["task"] == task]))
    for perturbation in sorted({row["perturbation"] for row in rows}):
        scopes.append(("perturbation", perturbation, [row for row in rows if row["perturbation"] == perturbation]))

    output = []
    for scope_type, scope_value, scoped_rows in scopes:
        for comparison in comparisons:
            corrected_field = comparison["corrected_similarity_drift"]
            baseline_field = comparison["baseline_similarity_drift"]
            y_field = comparison["correctness_drift_target"]
            corrected_x = [float(row[corrected_field]) for row in scoped_rows]
            baseline_x = [float(row[baseline_field]) for row in scoped_rows]
            y = [float(row[y_field]) for row in scoped_rows]
            corrected_pearson = pearson(corrected_x, y)
            baseline_pearson = pearson(baseline_x, y)
            corrected_spearman = spearman(corrected_x, y)
            baseline_spearman = spearman(baseline_x, y)
            pearson_delta = paired_correlation_delta(scoped_rows, corrected_field, baseline_field, y_field, pearson)
            spearman_delta = paired_correlation_delta(scoped_rows, corrected_field, baseline_field, y_field, spearman)
            pearson_low, pearson_high = paired_delta_ci(
                scoped_rows, corrected_field, baseline_field, y_field, pearson, bootstrap_samples, seed
            )
            spearman_low, spearman_high = paired_delta_ci(
                scoped_rows, corrected_field, baseline_field, y_field, spearman, bootstrap_samples, seed
            )
            pearson_p_greater = paired_delta_permutation_p_greater(
                scoped_rows, corrected_field, baseline_field, y_field, pearson, bootstrap_samples, seed
            )
            spearman_p_greater = paired_delta_permutation_p_greater(
                scoped_rows, corrected_field, baseline_field, y_field, spearman, bootstrap_samples, seed
            )
            output.append(
                {
                    "scope_type": scope_type,
                    "scope_value": scope_value,
                    "n": len(scoped_rows),
                    **comparison,
                    "corrected_pearson": "" if corrected_pearson is None else corrected_pearson,
                    "baseline_pearson": "" if baseline_pearson is None else baseline_pearson,
                    "pearson_delta_corrected_minus_baseline": "" if pearson_delta is None else pearson_delta,
                    "pearson_delta_ci95_low": "" if pearson_low is None else pearson_low,
                    "pearson_delta_ci95_high": "" if pearson_high is None else pearson_high,
                    "pearson_delta_permutation_p_greater": "" if pearson_p_greater is None else pearson_p_greater,
                    "corrected_spearman": "" if corrected_spearman is None else corrected_spearman,
                    "baseline_spearman": "" if baseline_spearman is None else baseline_spearman,
                    "spearman_delta_corrected_minus_baseline": "" if spearman_delta is None else spearman_delta,
                    "spearman_delta_ci95_low": "" if spearman_low is None else spearman_low,
                    "spearman_delta_ci95_high": "" if spearman_high is None else spearman_high,
                    "spearman_delta_permutation_p_greater": "" if spearman_p_greater is None else spearman_p_greater,
                    "corrected_better_by_pearson": (
                        ""
                        if pearson_delta is None
                        else int(pearson_delta > 0)
                    ),
                    "corrected_better_by_spearman": (
                        ""
                        if spearman_delta is None
                        else int(spearman_delta > 0)
                    ),
                }
            )
    return output


def case_inspection_rows(rows: list[dict], top_n: int = 10) -> list[dict]:
    categories = [
        (
            "high_corrected_drift_high_correctness_drift",
            sorted(
                rows,
                key=lambda row: (
                    float(row["noise_corrected_drift"]) * float(row["abs_repeated_pass_rate_change"]),
                    float(row["abs_repeated_pass_rate_change"]),
                    float(row["noise_corrected_drift"]),
                ),
                reverse=True,
            ),
        ),
        (
            "high_corrected_drift_no_correctness_drift",
            sorted(
                [row for row in rows if float(row["abs_repeated_pass_rate_change"]) == 0.0],
                key=lambda row: float(row["noise_corrected_drift"]),
                reverse=True,
            ),
        ),
        (
            "low_corrected_drift_high_correctness_drift",
            sorted(
                [row for row in rows if float(row["abs_repeated_pass_rate_change"]) > 0.0],
                key=lambda row: (
                    -float(row["abs_repeated_pass_rate_change"]),
                    float(row["noise_corrected_drift"]),
                ),
            ),
        ),
        (
            "largest_harmful_correctness_drop",
            sorted(rows, key=lambda row: float(row["repeated_pass_rate_drop"]), reverse=True),
        ),
        (
            "largest_correctness_improvement",
            sorted(rows, key=lambda row: float(row["repeated_pass_rate_drop"])),
        ),
    ]
    output = []
    seen = set()
    fields = [
        "case_id",
        "task",
        "dataset",
        "perturbation",
        "noise_corrected_drift",
        "raw_perturbation_drift",
        "uncorrected_single_drift",
        "noise_baseline",
        "clean_mean_correctness",
        "perturbed_mean_correctness",
        "repeated_pass_rate_drop",
        "abs_repeated_pass_rate_change",
        "harmful_correctness_drop",
        "correctness_changed",
    ]
    for category, ordered_rows in categories:
        rank = 0
        for row in ordered_rows:
            rank += 1
            if rank > top_n:
                break
            key = (category, row["case_id"])
            if key in seen:
                continue
            seen.add(key)
            output.append({"inspection_category": category, "rank": rank, **{field: row[field] for field in fields}})
    return output


def grouped_rows(rows: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["task"], row["dataset"], row["perturbation"])].append(row)

    output = []
    for (task, dataset, perturbation), scoped in sorted(grouped.items()):
        output.append(
            {
                "task": task,
                "dataset": dataset,
                "perturbation": perturbation,
                "n": len(scoped),
                "mean_noise_corrected_drift": mean([float(row["noise_corrected_drift"]) for row in scoped]),
                "mean_raw_perturbation_drift": mean([float(row["raw_perturbation_drift"]) for row in scoped]),
                "mean_abs_repeated_pass_rate_change": mean(
                    [float(row["abs_repeated_pass_rate_change"]) for row in scoped]
                ),
                "mean_repeated_pass_rate_drop": mean([float(row["repeated_pass_rate_drop"]) for row in scoped]),
                "mean_repeated_sampling_pdr": mean([float(row["repeated_sampling_pdr"]) for row in scoped]),
                "share_harmful_correctness_drop": mean([float(row["harmful_correctness_drop"]) for row in scoped]),
                "share_correctness_changed": mean([float(row["correctness_changed"]) for row in scoped]),
            }
        )
    return output


def find_correlation(rows: list[dict], scope_type: str, scope_value: str, relationship: str) -> dict | None:
    for row in rows:
        if (
            row["scope_type"] == scope_type
            and row["scope_value"] == scope_value
            and row["relationship"] == relationship
        ):
            return row
    return None


def fmt(value: object, digits: int = 3) -> str:
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


def write_report(
    path: Path,
    rows: list[dict],
    grouped: list[dict],
    correlations: list[dict],
    correction_comparison: list[dict],
    correction_gain: list[dict],
    case_inspection: list[dict],
    generations_path: Path,
    pdr_metrics_path: Path,
    embedding_model: str,
) -> None:
    primary = find_correlation(correlations, "overall", "all", "primary")
    by_task = [
        find_correlation(correlations, "task", task, "primary")
        for task in sorted({row["task"] for row in rows})
    ]
    by_task = [row for row in by_task if row]
    by_perturbation = [
        find_correlation(correlations, "perturbation", perturbation, "primary")
        for perturbation in sorted({row["perturbation"] for row in rows})
    ]
    by_perturbation = [row for row in by_perturbation if row]
    correction_overall = [row for row in correction_comparison if row["scope_type"] == "overall"]
    corrected = next(
        row
        for row in correction_overall
        if row["drift_measure"] == "noise_corrected_drift"
        and row["correctness_target"] == "abs_repeated_pass_rate_change"
    )
    raw = next(
        row
        for row in correction_overall
        if row["drift_measure"] == "raw_perturbation_drift"
        and row["correctness_target"] == "abs_repeated_pass_rate_change"
    )
    gain_overall = [row for row in correction_gain if row["scope_type"] == "overall"]
    raw_gain = next(row for row in gain_overall if row["baseline_type"] == "uncorrected_raw_cross_drift")
    single_gain = next(row for row in gain_overall if row["baseline_type"] == "uncorrected_single_pair")
    harmful_overall = find_correlation(correlations, "overall", "all", "harmful_drop_binary")
    raw_harmful_overall = find_correlation(correlations, "overall", "all", "raw_harmful_drop_binary")
    inspection_preview = [
        row
        for row in case_inspection
        if row["inspection_category"]
        in {
            "high_corrected_drift_high_correctness_drift",
            "high_corrected_drift_no_correctness_drift",
            "low_corrected_drift_high_correctness_drift",
        }
        and int(row["rank"]) <= 3
    ]
    primary_spearman = None if primary is None or primary["spearman"] == "" else float(primary["spearman"])
    if primary_spearman is None:
        interpretation = "The primary overall correlation is undefined because one variable has no variance."
    elif abs(primary_spearman) < 0.2:
        interpretation = "The primary overall relationship is weak at this pilot scale."
    elif primary_spearman > 0:
        interpretation = "The primary overall relationship is positive: larger semantic drift tends to align with larger correctness change."
    else:
        interpretation = "The primary overall relationship is negative, so semantic drift is not acting as a monotonic degradation proxy here."

    report = [
        "# RQ2 Semantic Drift vs Correctness Change",
        "",
        "## Question",
        "",
        "RQ2 asks whether semantic drift predicts correctness changes for objective tasks.",
        "",
        "This first implementation excludes open-ended writing and uses factual QA, math reasoning, and code generation only.",
        "",
        "## Data Source",
        "",
        f"- Generations: `{generations_path.as_posix()}`",
        f"- Correctness metrics: `{pdr_metrics_path.as_posix()}`",
        f"- Embedding model: `{embedding_model}`",
        f"- Case-level comparisons: `{len(rows)}`",
        "",
        "## Method",
        "",
        "For each case, the script embeds the three original outputs and three perturbed outputs from the same PDR run.",
        "It computes original sample noise, perturbed sample noise, raw cross-version drift, and noise-corrected drift.",
        "The primary correctness-change variable is absolute repeated pass-rate change; PDR is reported as an auxiliary normalized metric.",
        "",
        "This report also treats sample-noise correction as an explicit comparison factor, linking RQ1's noise-corrected drift design to RQ2's correctness-prediction question.",
        "",
        "## Overall Result",
        "",
        markdown_table(
            [primary] if primary else [],
            [
                "scope_type",
                "scope_value",
                "n",
                "relationship",
                "pearson",
                "spearman",
                "spearman_ci95_low",
                "spearman_ci95_high",
                "spearman_permutation_p_two_sided",
            ],
        ),
        "",
        interpretation,
        "",
        "## Sample-Noise Correction Comparison",
        "",
        "This section directly tests whether sample-noise corrected similarity drift is a better indicator of correctness drift than uncorrected similarity drift.",
        "The target is the same in the main comparison: absolute repeated pass-rate change.",
        "",
        markdown_table(
            correction_overall,
            [
                "drift_measure",
                "correction_status",
                "sampling_design",
                "correctness_target",
                "comparison_role",
                "pearson",
                "spearman",
                "spearman_ci95_low",
                "spearman_ci95_high",
                "spearman_permutation_p_two_sided",
            ],
        ),
        "",
        f"On the repeated-sampling correctness target, the sample-noise corrected measure has Spearman {fmt(corrected['spearman'])}, while raw uncorrected cross-drift has Spearman {fmt(raw['spearman'])}.",
        "",
        "## Sample-Noise Correction Gain",
        "",
        markdown_table(
            gain_overall,
            [
                "baseline_type",
                "correctness_drift_target",
                "corrected_pearson",
                "baseline_pearson",
                "pearson_delta_corrected_minus_baseline",
                "pearson_delta_ci95_low",
                "pearson_delta_ci95_high",
                "corrected_spearman",
                "baseline_spearman",
                "spearman_delta_corrected_minus_baseline",
                "spearman_delta_ci95_low",
                "spearman_delta_ci95_high",
                "spearman_delta_permutation_p_greater",
                "corrected_better_by_pearson",
                "corrected_better_by_spearman",
            ],
        ),
        "",
        f"Against raw cross-drift, sample-noise correction changes Pearson by {fmt(raw_gain['pearson_delta_corrected_minus_baseline'])} and Spearman by {fmt(raw_gain['spearman_delta_corrected_minus_baseline'])}.",
        f"Against the single-pair baseline, sample-noise correction changes Pearson by {fmt(single_gain['pearson_delta_corrected_minus_baseline'])} and Spearman by {fmt(single_gain['spearman_delta_corrected_minus_baseline'])}.",
        "In this first RQ2 run, correction improves Pearson association with correctness drift, especially relative to the single-pair baseline, but it does not improve Spearman rank association over raw repeated cross-drift.",
        "",
        "## Correctness Degradation",
        "",
        "The primary RQ2 target measures absolute correctness drift. To separate change from degradation, this section checks whether similarity drift indicates harmful correctness drops.",
        "",
        markdown_table(
            [row for row in [harmful_overall, raw_harmful_overall] if row],
            [
                "relationship",
                "x",
                "y",
                "n",
                "pearson",
                "spearman",
                "spearman_ci95_low",
                "spearman_ci95_high",
                "spearman_permutation_p_two_sided",
            ],
        ),
        "",
        "This distinguishes the question 'did correctness move?' from 'did correctness get worse?'.",
        "",
        "## By Task",
        "",
        markdown_table(
            by_task,
            ["scope_value", "n", "relationship", "pearson", "spearman", "spearman_ci95_low", "spearman_ci95_high"],
        ),
        "",
        "## By Perturbation",
        "",
        markdown_table(
            by_perturbation,
            ["scope_value", "n", "relationship", "pearson", "spearman", "spearman_ci95_low", "spearman_ci95_high"],
        ),
        "",
        "## Case Inspection Preview",
        "",
        markdown_table(
            inspection_preview,
            [
                "inspection_category",
                "rank",
                "case_id",
                "task",
                "perturbation",
                "noise_corrected_drift",
                "raw_perturbation_drift",
                "clean_mean_correctness",
                "perturbed_mean_correctness",
                "repeated_pass_rate_drop",
                "abs_repeated_pass_rate_change",
            ],
        ),
        "",
        "The full inspection table lists high-drift/high-correctness-change cases, high-drift/no-change cases, low-drift/high-change cases, harmful drops, and correctness improvements.",
        "",
        "## Task x Perturbation Means",
        "",
        markdown_table(
            grouped,
            [
                "task",
                "dataset",
                "perturbation",
                "n",
                "mean_noise_corrected_drift",
                "mean_abs_repeated_pass_rate_change",
                "mean_repeated_pass_rate_drop",
                "share_harmful_correctness_drop",
                "share_correctness_changed",
            ],
        ),
        "",
        "## Limitations",
        "",
        "- This is a first RQ2 implementation over 150 case-level comparisons from the existing 10x3 PDR run.",
        "- Correlations are descriptive and should not be interpreted as causal evidence.",
        "- Correctness labels are task-specific, so pooled results should be read together with task-level results.",
        "- Code correctness depends on the existing HumanEval execution/evaluation logic from the PDR run.",
        "",
    ]
    path.write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generations", type=Path, default=DEFAULT_GENERATIONS)
    parser.add_argument("--pdr-metrics", type=Path, default=DEFAULT_PDR_METRICS)
    parser.add_argument("--embedding-model", default="text-embedding-3-small")
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--output-tag", default="rq2_semantic_correctness")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260701)
    args = parser.parse_args()

    RESULTS_DIR.mkdir(exist_ok=True)
    suffix = f"_{args.output_tag}" if args.output_tag else ""
    metrics_path = RESULTS_DIR / f"{args.output_tag}_metrics.csv"
    grouped_path = RESULTS_DIR / f"{args.output_tag}_grouped.csv"
    correlations_path = RESULTS_DIR / f"{args.output_tag}_correlations.csv"
    correction_comparison_path = RESULTS_DIR / f"{args.output_tag}_sample_noise_correction_comparison.csv"
    correction_gain_path = RESULTS_DIR / f"{args.output_tag}_sample_noise_correction_gain.csv"
    case_inspection_path = RESULTS_DIR / f"{args.output_tag}_case_inspection.csv"
    summary_path = RESULTS_DIR / f"{args.output_tag}_summary.json"
    report_path = RESULTS_DIR / f"{args.output_tag}_report.md"

    generation_rows = read_csv(args.generations)
    cases = group_generation_rows(generation_rows, args.samples)
    pdr_metrics = load_pdr_metrics(args.pdr_metrics)
    missing = [
        (case["case_id"], case["task"], case["dataset"], case["perturbation"])
        for case in cases
        if (case["case_id"], case["task"], case["dataset"], case["perturbation"]) not in pdr_metrics
    ]
    if missing:
        raise ValueError(f"Missing PDR metrics for {len(missing)} cases; first missing key: {missing[0]}")

    existing_rows = load_existing_metrics(metrics_path) if args.resume else []
    completed_case_ids = {row["case_id"] for row in existing_rows}
    output_rows = existing_rows[:]
    api_key = read_api_key()

    print(
        f"RQ2 semantic correctness analysis: {len(cases)} cases, {args.samples} samples/version, "
        f"embedding model {args.embedding_model}",
        flush=True,
    )
    if completed_case_ids:
        print(f"Resuming from {len(completed_case_ids)}/{len(cases)} completed cases.", flush=True)

    for idx, case in enumerate(cases, start=1):
        pct = idx / len(cases) * 100
        if case["case_id"] in completed_case_ids:
            print(f"Case {idx}/{len(cases)} ({pct:.1f}%) already complete: {case['case_id']}", flush=True)
            continue
        print(
            f"Case {idx}/{len(cases)} ({pct:.1f}%) embedding: "
            f"{case['task']} {case['perturbation']} {case['case_id']}",
            flush=True,
        )
        key = (case["case_id"], case["task"], case["dataset"], case["perturbation"])
        row = compute_semantic_row(case, pdr_metrics[key], api_key, args.embedding_model)
        output_rows.append(row)
        output_rows = sorted(output_rows, key=lambda item: (item["task"], item["perturbation"], item["case_id"]))
        write_csv_fields(metrics_path, output_rows, METRIC_FIELDS)
        completed_case_ids.add(case["case_id"])

    grouped = grouped_rows(output_rows)
    correlations = correlation_rows(output_rows, args.bootstrap_samples, args.seed)
    correction_comparison = sample_noise_correction_comparison_rows(output_rows, args.bootstrap_samples, args.seed)
    correction_gain = sample_noise_correction_gain_rows(output_rows, args.bootstrap_samples, args.seed)
    case_inspection = case_inspection_rows(output_rows)
    write_csv(grouped_path, grouped)
    write_csv(correlations_path, correlations)
    write_csv(correction_comparison_path, correction_comparison)
    write_csv(correction_gain_path, correction_gain)
    write_csv(case_inspection_path, case_inspection)
    summary = {
        "input_generations": str(args.generations),
        "input_pdr_metrics": str(args.pdr_metrics),
        "embedding_model": args.embedding_model,
        "objective_tasks": sorted(OBJECTIVE_TASKS),
        "case_level_comparisons": len(output_rows),
        "bootstrap_samples": args.bootstrap_samples,
        "seed": args.seed,
        "grouped": grouped,
        "correlations": correlations,
        "sample_noise_correction_comparison": correction_comparison,
        "sample_noise_correction_gain": correction_gain,
        "case_inspection": case_inspection,
    }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    write_report(
        report_path,
        output_rows,
        grouped,
        correlations,
        correction_comparison,
        correction_gain,
        case_inspection,
        args.generations,
        args.pdr_metrics,
        args.embedding_model,
    )
    print(f"Wrote {metrics_path}", flush=True)
    print(f"Wrote {grouped_path}", flush=True)
    print(f"Wrote {correlations_path}", flush=True)
    print(f"Wrote {correction_comparison_path}", flush=True)
    print(f"Wrote {correction_gain_path}", flush=True)
    print(f"Wrote {case_inspection_path}", flush=True)
    print(f"Wrote {summary_path}", flush=True)
    print(f"Wrote {report_path}", flush=True)


if __name__ == "__main__":
    main()
