# Four-Task Similarity Sweep

- Sample-noise update: `noise_baseline = original_noise`, where `original_noise` is the average pairwise embedding distance among repeated generations under the original prompt.
- Batch: `6/10`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Total generation rows: `600`
- Total metric rows: `100`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | paraphrase | 25 | 0.0762 | 0.0303 | 0.0813 | 0.0510 |
| math_reasoning | MATH | paraphrase | 25 | 0.0496 | 0.0488 | 0.0531 | 0.0085 |
| code_generation | HumanEval | paraphrase | 25 | 0.0629 | 0.0329 | 0.0501 | 0.0254 |
| open_ended_writing | Alpaca | paraphrase | 25 | 0.0923 | 0.0736 | 0.0838 | 0.0160 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | paraphrase | 0.0510 | 0.0813 |
| math_reasoning | 1 | paraphrase | 0.0085 | 0.0531 |
| code_generation | 1 | paraphrase | 0.0254 | 0.0501 |
| open_ended_writing | 1 | paraphrase | 0.0160 | 0.0838 |