# Four-Task Similarity Sweep

- Sample-noise update: `noise_baseline = original_noise`, where `original_noise` is the average pairwise embedding distance among repeated generations under the original prompt.
- Batch: `5/10`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Total generation rows: `600`
- Total metric rows: `100`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | surface_noise | 25 | 0.0432 | 0.0313 | 0.0520 | 0.0281 |
| math_reasoning | MATH | surface_noise | 25 | 0.0522 | 0.0582 | 0.0538 | 0.0044 |
| code_generation | HumanEval | surface_noise | 25 | 0.0698 | 0.0474 | 0.0571 | 0.0238 |
| open_ended_writing | Alpaca | surface_noise | 25 | 0.0718 | 0.0579 | 0.0670 | 0.0133 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | surface_noise | 0.0281 | 0.0520 |
| math_reasoning | 1 | surface_noise | 0.0044 | 0.0538 |
| code_generation | 1 | surface_noise | 0.0238 | 0.0571 |
| open_ended_writing | 1 | surface_noise | 0.0133 | 0.0670 |