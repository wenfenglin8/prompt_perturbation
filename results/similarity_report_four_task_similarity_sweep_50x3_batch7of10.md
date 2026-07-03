# Four-Task Similarity Sweep

- Sample-noise update: `noise_baseline = original_noise`, where `original_noise` is the average pairwise embedding distance among repeated generations under the original prompt.
- Batch: `7/10`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Total generation rows: `600`
- Total metric rows: `100`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | reordering | 25 | 0.0226 | 0.0129 | 0.0172 | 0.0057 |
| math_reasoning | MATH | reordering | 25 | 0.0652 | 0.0488 | 0.0752 | 0.0303 |
| code_generation | HumanEval | reordering | 25 | 0.0289 | 0.0164 | 0.0250 | 0.0144 |
| open_ended_writing | Alpaca | reordering | 25 | 0.0730 | 0.0784 | 0.0914 | 0.0190 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | reordering | 0.0057 | 0.0172 |
| math_reasoning | 1 | reordering | 0.0303 | 0.0752 |
| code_generation | 1 | reordering | 0.0144 | 0.0250 |
| open_ended_writing | 1 | reordering | 0.0190 | 0.0914 |