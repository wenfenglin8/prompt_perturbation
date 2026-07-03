import argparse
import csv
import itertools
import json
import os
import statistics
from collections import defaultdict
from pathlib import Path

import numpy as np
import requests


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
                continue
            if response.status_code >= 400:
                raise RuntimeError(f"{response.status_code} {response.text[:1000]}")
            return response.json()
        except requests.RequestException as exc:
            last_error = exc
    raise RuntimeError(f"Request failed after retries: {last_error}")


def embed_texts(api_key: str, model: str, texts: list[str]) -> np.ndarray:
    data = post_json("https://api.openai.com/v1/embeddings", api_key, {"model": model, "input": texts})
    vectors = [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
    arr = np.array(vectors, dtype=float)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    return arr / np.maximum(norms, 1e-12)


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generations", required=True)
    parser.add_argument("--embedding-model", default="text-embedding-3-small")
    parser.add_argument("--output-tag", required=True)
    args = parser.parse_args()

    api_key = read_api_key()
    rows = []
    with Path(args.generations).open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows.extend(reader)

    grouped = defaultdict(lambda: {"original": [], "perturbed": [], "meta": None})
    for row in rows:
        key = (row["case_id"], row["perturbation"], row["task"], row["dataset"])
        grouped[key][row["version"]].append(row["output"])
        grouped[key]["meta"] = {
            "case_id": row["case_id"],
            "perturbation": row["perturbation"],
            "task": row["task"],
            "dataset": row["dataset"],
        }

    metric_rows = []
    for key, item in grouped.items():
        original = item["original"]
        perturbed = item["perturbed"]
        vectors = embed_texts(api_key, args.embedding_model, original + perturbed)
        original_vectors = vectors[: len(original)]
        perturbed_vectors = vectors[len(original) :]
        original_noise = avg_pairwise_distance(original_vectors)
        perturbed_noise = avg_pairwise_distance(perturbed_vectors)
        noise_baseline = (original_noise + perturbed_noise) / 2.0
        uncorrected_single_drift = max(0.0, 1.0 - float(np.dot(original_vectors[0], perturbed_vectors[0])))
        raw_drift = avg_cross_distance(original_vectors, perturbed_vectors)
        corrected = max(0.0, raw_drift - noise_baseline)
        metric_rows.append(
            {
                **item["meta"],
                "uncorrected_single_drift": uncorrected_single_drift,
                "original_noise": original_noise,
                "perturbed_noise": perturbed_noise,
                "noise_baseline": noise_baseline,
                "raw_perturbation_drift": raw_drift,
                "noise_corrected_drift": corrected,
            }
        )

    grouped_rows = []
    for perturbation in sorted({row["perturbation"] for row in metric_rows}):
        for task in sorted({row["task"] for row in metric_rows}):
            subset = [row for row in metric_rows if row["perturbation"] == perturbation and row["task"] == task]
            if not subset:
                continue
            grouped_rows.append(
                {
                    "perturbation": perturbation,
                    "task": task,
                    "n": len(subset),
                    "uncorrected_single_drift": statistics.mean(row["uncorrected_single_drift"] for row in subset),
                    "noise_baseline": statistics.mean(row["noise_baseline"] for row in subset),
                    "raw_perturbation_drift": statistics.mean(row["raw_perturbation_drift"] for row in subset),
                    "noise_corrected_drift": statistics.mean(row["noise_corrected_drift"] for row in subset),
                }
            )

    metrics_csv = RESULTS_DIR / f"similarity_metrics_{args.output_tag}.csv"
    grouped_csv = RESULTS_DIR / f"similarity_grouped_{args.output_tag}.csv"
    metrics_json = RESULTS_DIR / f"similarity_metrics_{args.output_tag}.json"

    with metrics_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(metric_rows[0].keys()))
        writer.writeheader()
        writer.writerows(metric_rows)

    with grouped_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(grouped_rows[0].keys()))
        writer.writeheader()
        writer.writerows(grouped_rows)

    metrics_json.write_text(
        json.dumps(
            {
                "embedding_model": args.embedding_model,
                "source_generations": args.generations,
                "metrics": metric_rows,
                "grouped": grouped_rows,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {metrics_csv}")
    print(f"Wrote {grouped_csv}")
    print(f"Wrote {metrics_json}")


if __name__ == "__main__":
    main()
