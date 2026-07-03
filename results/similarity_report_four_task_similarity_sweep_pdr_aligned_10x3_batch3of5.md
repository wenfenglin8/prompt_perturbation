# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `10`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `3/5`
- Total generation calls: `240`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | formatting | 10 | 0.0000 | 0.0190 | 0.0315 | 0.0139 |
| math_reasoning | MATH | formatting | 10 | 0.0566 | 0.0470 | 0.0509 | 0.0069 |
| code_generation | HumanEval | formatting | 10 | 0.0360 | 0.0313 | 0.0552 | 0.0294 |
| open_ended_writing | Alpaca | formatting | 10 | 0.1369 | 0.1017 | 0.1569 | 0.0588 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | formatting | 0.0139 | 0.0315 |
| math_reasoning | 1 | formatting | 0.0069 | 0.0509 |
| code_generation | 1 | formatting | 0.0294 | 0.0552 |
| open_ended_writing | 1 | formatting | 0.0588 | 0.1569 |