# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `10`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `2/5`
- Total generation calls: `240`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | reordering | 10 | 0.0476 | 0.0179 | 0.0172 | 0.0000 |
| math_reasoning | MATH | reordering | 10 | 0.0681 | 0.0546 | 0.0543 | 0.0025 |
| code_generation | HumanEval | reordering | 10 | 0.0623 | 0.0368 | 0.0551 | 0.0208 |
| open_ended_writing | Alpaca | reordering | 10 | 0.1092 | 0.1036 | 0.1152 | 0.0180 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | reordering | 0.0000 | 0.0172 |
| math_reasoning | 1 | reordering | 0.0025 | 0.0543 |
| code_generation | 1 | reordering | 0.0208 | 0.0551 |
| open_ended_writing | 1 | reordering | 0.0180 | 0.1152 |