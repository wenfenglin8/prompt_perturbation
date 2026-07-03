# Four-Task Similarity Sweep

- Sample-noise update: `noise_baseline = original_noise`, where `original_noise` is the average pairwise embedding distance among repeated generations under the original prompt.
- Batch: `8/10`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Total generation rows: `600`
- Total metric rows: `100`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | formatting | 25 | 0.0260 | 0.0276 | 0.0337 | 0.0152 |
| math_reasoning | MATH | formatting | 25 | 0.0594 | 0.0474 | 0.0566 | 0.0142 |
| code_generation | HumanEval | formatting | 25 | 0.0470 | 0.0349 | 0.0656 | 0.0402 |
| open_ended_writing | Alpaca | formatting | 25 | 0.1012 | 0.0866 | 0.0875 | 0.0127 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | formatting | 0.0152 | 0.0337 |
| math_reasoning | 1 | formatting | 0.0142 | 0.0566 |
| code_generation | 1 | formatting | 0.0402 | 0.0656 |
| open_ended_writing | 1 | formatting | 0.0127 | 0.0875 |