# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `5`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `2/5`
- Total generation calls: `120`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | reordering | 5 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | MATH | reordering | 5 | 0.0618 | 0.0429 | 0.0457 | 0.0032 |
| code_generation | HumanEval | reordering | 5 | 0.0782 | 0.0173 | 0.0638 | 0.0465 |
| open_ended_writing | Alpaca | reordering | 5 | 0.0516 | 0.0889 | 0.0916 | 0.0066 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | reordering | 0.0000 | 0.0000 |
| math_reasoning | 1 | reordering | 0.0032 | 0.0457 |
| code_generation | 1 | reordering | 0.0465 | 0.0638 |
| open_ended_writing | 1 | reordering | 0.0066 | 0.0916 |