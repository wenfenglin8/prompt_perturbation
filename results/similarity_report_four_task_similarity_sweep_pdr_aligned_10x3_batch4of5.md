# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `10`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `4/5`
- Total generation calls: `240`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | context_injection | 10 | 0.0171 | 0.0263 | 0.0387 | 0.0150 |
| math_reasoning | MATH | context_injection | 10 | 0.0655 | 0.0526 | 0.0561 | 0.0052 |
| code_generation | HumanEval | context_injection | 10 | 0.0187 | 0.0272 | 0.0390 | 0.0161 |
| open_ended_writing | Alpaca | context_injection | 10 | 0.1482 | 0.1220 | 0.1331 | 0.0209 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | context_injection | 0.0150 | 0.0387 |
| math_reasoning | 1 | context_injection | 0.0052 | 0.0561 |
| code_generation | 1 | context_injection | 0.0161 | 0.0390 |
| open_ended_writing | 1 | context_injection | 0.0209 | 0.1331 |