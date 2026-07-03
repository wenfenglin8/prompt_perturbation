# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `50`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `8/10`
- Total generation calls: `600`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | formatting | 25 | 0.0260 | 0.0270 | 0.0337 | 0.0097 |
| math_reasoning | MATH | formatting | 25 | 0.0594 | 0.0472 | 0.0566 | 0.0106 |
| code_generation | HumanEval | formatting | 25 | 0.0470 | 0.0360 | 0.0656 | 0.0319 |
| open_ended_writing | Alpaca | formatting | 25 | 0.1012 | 0.0786 | 0.0875 | 0.0123 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | formatting | 0.0097 | 0.0337 |
| math_reasoning | 1 | formatting | 0.0106 | 0.0566 |
| code_generation | 1 | formatting | 0.0319 | 0.0656 |
| open_ended_writing | 1 | formatting | 0.0123 | 0.0875 |