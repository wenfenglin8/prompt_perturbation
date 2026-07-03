# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `50`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `9/10`
- Total generation calls: `600`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | context_injection | 25 | 0.0112 | 0.0180 | 0.0185 | 0.0042 |
| math_reasoning | MATH | context_injection | 25 | 0.0536 | 0.0473 | 0.0533 | 0.0088 |
| code_generation | HumanEval | context_injection | 25 | 0.0133 | 0.0303 | 0.0279 | 0.0023 |
| open_ended_writing | Alpaca | context_injection | 25 | 0.0936 | 0.0737 | 0.0919 | 0.0196 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | context_injection | 0.0042 | 0.0185 |
| math_reasoning | 1 | context_injection | 0.0088 | 0.0533 |
| code_generation | 1 | context_injection | 0.0023 | 0.0279 |
| open_ended_writing | 1 | context_injection | 0.0196 | 0.0919 |