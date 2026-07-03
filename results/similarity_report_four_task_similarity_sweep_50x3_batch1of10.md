# Four-Task Similarity Sweep

- Sample-noise update: `noise_baseline = original_noise`, where `original_noise` is the average pairwise embedding distance among repeated generations under the original prompt.
- Batch: `1/10`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Total generation rows: `600`
- Total metric rows: `100`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | paraphrase | 25 | 0.1301 | 0.0363 | 0.1152 | 0.0920 |
| math_reasoning | MATH | paraphrase | 25 | 0.0499 | 0.0495 | 0.0494 | 0.0073 |
| code_generation | HumanEval | paraphrase | 25 | 0.0806 | 0.0301 | 0.0786 | 0.0510 |
| open_ended_writing | Alpaca | paraphrase | 25 | 0.0601 | 0.0672 | 0.0633 | 0.0058 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | paraphrase | 0.0920 | 0.1152 |
| math_reasoning | 1 | paraphrase | 0.0073 | 0.0494 |
| code_generation | 1 | paraphrase | 0.0510 | 0.0786 |
| open_ended_writing | 1 | paraphrase | 0.0058 | 0.0633 |