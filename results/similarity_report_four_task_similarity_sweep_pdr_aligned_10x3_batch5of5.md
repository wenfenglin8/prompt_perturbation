# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `10`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `5/5`
- Total generation calls: `240`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | surface_noise | 10 | 0.0313 | 0.0253 | 0.0351 | 0.0098 |
| math_reasoning | MATH | surface_noise | 10 | 0.0638 | 0.0512 | 0.0616 | 0.0111 |
| code_generation | HumanEval | surface_noise | 10 | 0.0538 | 0.0360 | 0.0605 | 0.0288 |
| open_ended_writing | Alpaca | surface_noise | 10 | 0.1434 | 0.1025 | 0.1184 | 0.0265 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | surface_noise | 0.0098 | 0.0351 |
| math_reasoning | 1 | surface_noise | 0.0111 | 0.0616 |
| code_generation | 1 | surface_noise | 0.0288 | 0.0605 |
| open_ended_writing | 1 | surface_noise | 0.0265 | 0.1184 |