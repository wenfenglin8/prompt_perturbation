# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `10`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `1/5`
- Total generation calls: `240`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | paraphrase | 10 | 0.0697 | 0.0349 | 0.0960 | 0.0611 |
| math_reasoning | MATH | paraphrase | 10 | 0.0375 | 0.0442 | 0.0465 | 0.0045 |
| code_generation | HumanEval | paraphrase | 10 | 0.0543 | 0.0313 | 0.0485 | 0.0198 |
| open_ended_writing | Alpaca | paraphrase | 10 | 0.1207 | 0.1262 | 0.1278 | 0.0138 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | paraphrase | 0.0611 | 0.0960 |
| math_reasoning | 1 | paraphrase | 0.0045 | 0.0465 |
| code_generation | 1 | paraphrase | 0.0198 | 0.0485 |
| open_ended_writing | 1 | paraphrase | 0.0138 | 0.1278 |