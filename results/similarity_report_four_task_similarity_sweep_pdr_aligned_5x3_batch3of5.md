# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `5`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `3/5`
- Total generation calls: `120`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | formatting | 5 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | MATH | formatting | 5 | 0.0433 | 0.0613 | 0.0528 | 0.0011 |
| code_generation | HumanEval | formatting | 5 | 0.0500 | 0.0186 | 0.0565 | 0.0382 |
| open_ended_writing | Alpaca | formatting | 5 | 0.1479 | 0.0980 | 0.1523 | 0.0543 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | formatting | 0.0000 | 0.0000 |
| math_reasoning | 1 | formatting | 0.0011 | 0.0528 |
| code_generation | 1 | formatting | 0.0382 | 0.0565 |
| open_ended_writing | 1 | formatting | 0.0543 | 0.1523 |