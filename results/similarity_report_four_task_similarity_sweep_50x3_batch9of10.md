# Four-Task Similarity Sweep

- Sample-noise update: `noise_baseline = original_noise`, where `original_noise` is the average pairwise embedding distance among repeated generations under the original prompt.
- Batch: `9/10`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Total generation rows: `600`
- Total metric rows: `100`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | context_injection | 25 | 0.0112 | 0.0214 | 0.0185 | 0.0029 |
| math_reasoning | MATH | context_injection | 25 | 0.0536 | 0.0468 | 0.0533 | 0.0117 |
| code_generation | HumanEval | context_injection | 25 | 0.0133 | 0.0346 | 0.0279 | 0.0036 |
| open_ended_writing | Alpaca | context_injection | 25 | 0.0936 | 0.0730 | 0.0919 | 0.0273 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | context_injection | 0.0029 | 0.0185 |
| math_reasoning | 1 | context_injection | 0.0117 | 0.0533 |
| code_generation | 1 | context_injection | 0.0036 | 0.0279 |
| open_ended_writing | 1 | context_injection | 0.0273 | 0.0919 |