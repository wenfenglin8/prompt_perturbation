# Four-Task Similarity Sweep

- Sample-noise update: `noise_baseline = original_noise`, where `original_noise` is the average pairwise embedding distance among repeated generations under the original prompt.
- Batch: `3/10`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Total generation rows: `600`
- Total metric rows: `100`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | formatting | 25 | 0.0223 | 0.0277 | 0.0537 | 0.0309 |
| math_reasoning | MATH | formatting | 25 | 0.0583 | 0.0464 | 0.0494 | 0.0068 |
| code_generation | HumanEval | formatting | 25 | 0.1270 | 0.0320 | 0.1007 | 0.0722 |
| open_ended_writing | Alpaca | formatting | 25 | 0.0856 | 0.0583 | 0.0856 | 0.0340 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | formatting | 0.0309 | 0.0537 |
| math_reasoning | 1 | formatting | 0.0068 | 0.0494 |
| code_generation | 1 | formatting | 0.0722 | 0.1007 |
| open_ended_writing | 1 | formatting | 0.0340 | 0.0856 |