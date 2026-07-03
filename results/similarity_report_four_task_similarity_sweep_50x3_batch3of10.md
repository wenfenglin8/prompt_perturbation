# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `50`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `3/10`
- Total generation calls: `600`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | formatting | 25 | 0.0223 | 0.0305 | 0.0537 | 0.0274 |
| math_reasoning | MATH | formatting | 25 | 0.0583 | 0.0487 | 0.0494 | 0.0039 |
| code_generation | HumanEval | formatting | 25 | 0.1270 | 0.0426 | 0.1007 | 0.0583 |
| open_ended_writing | Alpaca | formatting | 25 | 0.0856 | 0.0580 | 0.0856 | 0.0297 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | formatting | 0.0274 | 0.0537 |
| math_reasoning | 1 | formatting | 0.0039 | 0.0494 |
| code_generation | 1 | formatting | 0.0583 | 0.1007 |
| open_ended_writing | 1 | formatting | 0.0297 | 0.0856 |