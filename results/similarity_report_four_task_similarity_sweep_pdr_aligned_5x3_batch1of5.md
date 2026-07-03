# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `5`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `1/5`
- Total generation calls: `120`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | paraphrase | 5 | 0.0674 | 0.0201 | 0.0539 | 0.0338 |
| math_reasoning | MATH | paraphrase | 5 | 0.0520 | 0.0467 | 0.0577 | 0.0121 |
| code_generation | HumanEval | paraphrase | 5 | 0.0366 | 0.0077 | 0.0445 | 0.0369 |
| open_ended_writing | Alpaca | paraphrase | 5 | 0.1375 | 0.0872 | 0.0889 | 0.0066 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | paraphrase | 0.0338 | 0.0539 |
| math_reasoning | 1 | paraphrase | 0.0121 | 0.0577 |
| code_generation | 1 | paraphrase | 0.0369 | 0.0445 |
| open_ended_writing | 1 | paraphrase | 0.0066 | 0.0889 |