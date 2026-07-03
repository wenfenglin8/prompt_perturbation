# Four-Task Similarity Sweep

- Sample-noise update: `noise_baseline = original_noise`, where `original_noise` is the average pairwise embedding distance among repeated generations under the original prompt.
- Batch: `2/10`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Total generation rows: `600`
- Total metric rows: `100`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | reordering | 25 | 0.0610 | 0.0353 | 0.0628 | 0.0392 |
| math_reasoning | MATH | reordering | 25 | 0.0683 | 0.0537 | 0.0753 | 0.0261 |
| code_generation | HumanEval | reordering | 25 | 0.0670 | 0.0491 | 0.0617 | 0.0280 |
| open_ended_writing | Alpaca | reordering | 25 | 0.0740 | 0.0682 | 0.0713 | 0.0139 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | reordering | 0.0392 | 0.0628 |
| math_reasoning | 1 | reordering | 0.0261 | 0.0753 |
| code_generation | 1 | reordering | 0.0280 | 0.0617 |
| open_ended_writing | 1 | reordering | 0.0139 | 0.0713 |