# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `50`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `10/10`
- Total generation calls: `600`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | surface_noise | 25 | 0.0309 | 0.0164 | 0.0242 | 0.0083 |
| math_reasoning | MATH | surface_noise | 25 | 0.0517 | 0.0527 | 0.0530 | 0.0042 |
| code_generation | HumanEval | surface_noise | 25 | 0.0437 | 0.0302 | 0.0412 | 0.0118 |
| open_ended_writing | Alpaca | surface_noise | 25 | 0.0673 | 0.0892 | 0.0880 | 0.0052 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | surface_noise | 0.0083 | 0.0242 |
| math_reasoning | 1 | surface_noise | 0.0042 | 0.0530 |
| code_generation | 1 | surface_noise | 0.0118 | 0.0412 |
| open_ended_writing | 1 | surface_noise | 0.0052 | 0.0880 |