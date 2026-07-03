# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `50`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `5/10`
- Total generation calls: `600`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | surface_noise | 25 | 0.0432 | 0.0222 | 0.0520 | 0.0322 |
| math_reasoning | MATH | surface_noise | 25 | 0.0522 | 0.0505 | 0.0538 | 0.0054 |
| code_generation | HumanEval | surface_noise | 25 | 0.0698 | 0.0432 | 0.0571 | 0.0176 |
| open_ended_writing | Alpaca | surface_noise | 25 | 0.0718 | 0.0659 | 0.0670 | 0.0040 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | surface_noise | 0.0322 | 0.0520 |
| math_reasoning | 1 | surface_noise | 0.0054 | 0.0538 |
| code_generation | 1 | surface_noise | 0.0176 | 0.0571 |
| open_ended_writing | 1 | surface_noise | 0.0040 | 0.0670 |