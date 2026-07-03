# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `5`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `4/5`
- Total generation calls: `120`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | context_injection | 5 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | MATH | context_injection | 5 | 0.0831 | 0.0532 | 0.0512 | 0.0018 |
| code_generation | HumanEval | context_injection | 5 | 0.0634 | 0.0266 | 0.0299 | 0.0051 |
| open_ended_writing | Alpaca | context_injection | 5 | 0.0990 | 0.0719 | 0.0857 | 0.0161 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | context_injection | 0.0000 | 0.0000 |
| math_reasoning | 1 | context_injection | 0.0018 | 0.0512 |
| code_generation | 1 | context_injection | 0.0051 | 0.0299 |
| open_ended_writing | 1 | context_injection | 0.0161 | 0.0857 |