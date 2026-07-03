# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `50`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `4/10`
- Total generation calls: `600`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | context_injection | 25 | 0.0506 | 0.0218 | 0.0479 | 0.0265 |
| math_reasoning | MATH | context_injection | 25 | 0.0534 | 0.0472 | 0.0477 | 0.0034 |
| code_generation | HumanEval | context_injection | 25 | 0.0286 | 0.0343 | 0.0431 | 0.0091 |
| open_ended_writing | Alpaca | context_injection | 25 | 0.0875 | 0.0615 | 0.0799 | 0.0188 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | context_injection | 0.0265 | 0.0479 |
| math_reasoning | 1 | context_injection | 0.0034 | 0.0477 |
| code_generation | 1 | context_injection | 0.0091 | 0.0431 |
| open_ended_writing | 1 | context_injection | 0.0188 | 0.0799 |