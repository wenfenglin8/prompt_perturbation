# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `5`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `5/5`
- Total generation calls: `120`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | surface_noise | 5 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | MATH | surface_noise | 5 | 0.0328 | 0.0616 | 0.0547 | 0.0007 |
| code_generation | HumanEval | surface_noise | 5 | 0.0403 | 0.0128 | 0.0457 | 0.0333 |
| open_ended_writing | Alpaca | surface_noise | 5 | 0.1647 | 0.0618 | 0.1597 | 0.1016 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | surface_noise | 0.0000 | 0.0000 |
| math_reasoning | 1 | surface_noise | 0.0007 | 0.0547 |
| code_generation | 1 | surface_noise | 0.0333 | 0.0457 |
| open_ended_writing | 1 | surface_noise | 0.1016 | 0.1597 |