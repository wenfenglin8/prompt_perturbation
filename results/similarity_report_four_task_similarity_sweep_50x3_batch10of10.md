# Four-Task Similarity Sweep

- Sample-noise update: `noise_baseline = original_noise`, where `original_noise` is the average pairwise embedding distance among repeated generations under the original prompt.
- Batch: `10/10`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Total generation rows: `600`
- Total metric rows: `100`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | surface_noise | 25 | 0.0309 | 0.0124 | 0.0242 | 0.0138 |
| math_reasoning | MATH | surface_noise | 25 | 0.0517 | 0.0537 | 0.0530 | 0.0074 |
| code_generation | HumanEval | surface_noise | 25 | 0.0437 | 0.0243 | 0.0412 | 0.0217 |
| open_ended_writing | Alpaca | surface_noise | 25 | 0.0673 | 0.0944 | 0.0880 | 0.0089 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | surface_noise | 0.0138 | 0.0242 |
| math_reasoning | 1 | surface_noise | 0.0074 | 0.0530 |
| code_generation | 1 | surface_noise | 0.0217 | 0.0412 |
| open_ended_writing | 1 | surface_noise | 0.0089 | 0.0880 |