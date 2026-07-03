# Four-Task Similarity Sweep

- Sample-noise update: `noise_baseline = original_noise`, where `original_noise` is the average pairwise embedding distance among repeated generations under the original prompt.
- Batch: `4/10`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Total generation rows: `600`
- Total metric rows: `100`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | context_injection | 25 | 0.0506 | 0.0252 | 0.0479 | 0.0298 |
| math_reasoning | MATH | context_injection | 25 | 0.0534 | 0.0471 | 0.0477 | 0.0060 |
| code_generation | HumanEval | context_injection | 25 | 0.0286 | 0.0388 | 0.0431 | 0.0130 |
| open_ended_writing | Alpaca | context_injection | 25 | 0.0875 | 0.0660 | 0.0799 | 0.0168 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | context_injection | 0.0298 | 0.0479 |
| math_reasoning | 1 | context_injection | 0.0060 | 0.0477 |
| code_generation | 1 | context_injection | 0.0130 | 0.0431 |
| open_ended_writing | 1 | context_injection | 0.0168 | 0.0799 |