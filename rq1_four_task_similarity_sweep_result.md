# RQ1 Four-Task Similarity Sweep Result

Updated on 2026-06-30 using the current perturbation implementation.

## Experiment Setup

| Item | Setting |
|---|---|
| Model | `gpt-4o-mini` |
| Embedding model | `text-embedding-3-small` |
| Cases per task | 2 |
| Samples per clean / perturbed prompt | 3 |
| Tasks | factual QA, math reasoning, code generation, open-ended writing |
| Datasets | SQuAD V2, MATH, HumanEval, Alpaca |
| Perturbations | paraphrase, reordering, formatting, context_injection, surface_noise |
| Evaluation | embedding-based semantic drift |
| Correction | `max(0, raw drift - noise baseline)` |

Run command:

```powershell
python four_task_similarity_sweep.py --dataset-cases-per-task 2 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag rq1_four_task_similarity_sweep_current_2x3
```

Total generation calls:

```text
4 tasks x 2 cases x 5 perturbations x 2 prompt versions x 3 samples = 240
```

The current implementation also makes LLM-sampler calls while constructing `paraphrase` and `reordering` perturbed instructions.

## Output Files

| File | Content |
|---|---|
| `results/generations_rq1_four_task_similarity_sweep_current_2x3.csv` | All generated outputs |
| `results/similarity_metrics_rq1_four_task_similarity_sweep_current_2x3.csv` | Per-case similarity metrics |
| `results/similarity_grouped_rq1_four_task_similarity_sweep_current_2x3.csv` | Task x perturbation grouped metrics |
| `results/similarity_rankings_rq1_four_task_similarity_sweep_current_2x3.csv` | Corrected sensitivity ranking per task |
| `results/similarity_summary_rq1_four_task_similarity_sweep_current_2x3.json` | Full structured result |
| `results/similarity_report_rq1_four_task_similarity_sweep_current_2x3.md` | Auto-generated report |

## Metric Definitions

```text
uncorrected single drift
= embedding distance between the first clean output and first perturbed output

raw perturbation drift
= average embedding distance across all clean-vs-perturbed output pairs

noise baseline
= average within-clean and within-perturbed output distance

noise-corrected drift
= max(0, raw perturbation drift - noise baseline)
```

## Grouped Drift Result

| Task | Dataset | Perturbation | N | Uncorrected single drift | Noise baseline | Raw drift | Corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| Factual QA | SQuAD V2 | paraphrase | 2 | 0.1261 | 0.0000 | 0.1261 | 0.1261 |
| Factual QA | SQuAD V2 | reordering | 2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Factual QA | SQuAD V2 | formatting | 2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Factual QA | SQuAD V2 | context_injection | 2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Factual QA | SQuAD V2 | surface_noise | 2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Math reasoning | MATH | paraphrase | 2 | 0.0240 | 0.0275 | 0.0270 | 0.0005 |
| Math reasoning | MATH | reordering | 2 | 0.0248 | 0.0296 | 0.0270 | 0.0000 |
| Math reasoning | MATH | formatting | 2 | 0.0438 | 0.0380 | 0.0335 | 0.0000 |
| Math reasoning | MATH | context_injection | 2 | 0.0445 | 0.0300 | 0.0319 | 0.0031 |
| Math reasoning | MATH | surface_noise | 2 | 0.0191 | 0.0306 | 0.0282 | 0.0000 |
| Code generation | HumanEval | paraphrase | 2 | 0.0568 | 0.0208 | 0.0326 | 0.0118 |
| Code generation | HumanEval | reordering | 2 | 0.0253 | 0.0306 | 0.0253 | 0.0022 |
| Code generation | HumanEval | formatting | 2 | 0.0129 | 0.0066 | 0.0069 | 0.0003 |
| Code generation | HumanEval | context_injection | 2 | 0.0550 | 0.0529 | 0.0499 | 0.0000 |
| Code generation | HumanEval | surface_noise | 2 | 0.0044 | 0.0030 | 0.0029 | 0.0000 |
| Open-ended writing | Alpaca | paraphrase | 2 | 0.0278 | 0.0260 | 0.0347 | 0.0087 |
| Open-ended writing | Alpaca | reordering | 2 | 0.0452 | 0.0614 | 0.0576 | 0.0000 |
| Open-ended writing | Alpaca | formatting | 2 | 0.0621 | 0.0191 | 0.0527 | 0.0336 |
| Open-ended writing | Alpaca | context_injection | 2 | 0.0575 | 0.0303 | 0.0671 | 0.0368 |
| Open-ended writing | Alpaca | surface_noise | 2 | 0.0404 | 0.0140 | 0.0300 | 0.0160 |

## Corrected Sensitivity Ranking

| Task | Rank | Perturbation | Corrected drift | Raw drift |
|---|---:|---|---:|---:|
| Factual QA | 1 | paraphrase | 0.1261 | 0.1261 |
| Factual QA | 2 | surface_noise | 0.0000 | 0.0000 |
| Factual QA | 3 | reordering | 0.0000 | 0.0000 |
| Factual QA | 4 | formatting | 0.0000 | 0.0000 |
| Factual QA | 5 | context_injection | 0.0000 | 0.0000 |
| Math reasoning | 1 | context_injection | 0.0031 | 0.0319 |
| Math reasoning | 2 | paraphrase | 0.0005 | 0.0270 |
| Math reasoning | 3 | reordering | 0.0000 | 0.0270 |
| Math reasoning | 4 | formatting | 0.0000 | 0.0335 |
| Math reasoning | 5 | surface_noise | 0.0000 | 0.0282 |
| Code generation | 1 | paraphrase | 0.0118 | 0.0326 |
| Code generation | 2 | reordering | 0.0022 | 0.0253 |
| Code generation | 3 | formatting | 0.0003 | 0.0069 |
| Code generation | 4 | context_injection | 0.0000 | 0.0499 |
| Code generation | 5 | surface_noise | 0.0000 | 0.0029 |
| Open-ended writing | 1 | context_injection | 0.0368 | 0.0671 |
| Open-ended writing | 2 | formatting | 0.0336 | 0.0527 |
| Open-ended writing | 3 | surface_noise | 0.0160 | 0.0300 |
| Open-ended writing | 4 | paraphrase | 0.0087 | 0.0347 |
| Open-ended writing | 5 | reordering | 0.0000 | 0.0576 |

## Interpretation

In this 2-case-per-task pilot, the corrected sensitivity ranking is task-dependent.

Factual QA is only sensitive to paraphrase in this run; the other perturbations produce effectively identical outputs after correction. Math reasoning shows very small corrected drifts overall, with context injection highest but still close to zero. Code generation is most affected by paraphrase, with reordering a distant second. Open-ended writing shows the largest corrected drift under context injection and formatting, with surface noise also retaining some drift after sample-noise correction.

Because this is still a small 2x3 pilot, the ranking should be treated as exploratory. The main RQ1-relevant result is that the noise-corrected ranking is not consistent across task types under the current five-perturbation implementation.
