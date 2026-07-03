# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `50`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `6/10`
- Total generation calls: `600`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | paraphrase | 25 | 0.0762 | 0.0353 | 0.0813 | 0.0465 |
| math_reasoning | MATH | paraphrase | 25 | 0.0496 | 0.0501 | 0.0531 | 0.0055 |
| code_generation | HumanEval | paraphrase | 25 | 0.0629 | 0.0319 | 0.0501 | 0.0195 |
| open_ended_writing | Alpaca | paraphrase | 25 | 0.0923 | 0.0795 | 0.0838 | 0.0073 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | paraphrase | 0.0465 | 0.0813 |
| math_reasoning | 1 | paraphrase | 0.0055 | 0.0531 |
| code_generation | 1 | paraphrase | 0.0195 | 0.0501 |
| open_ended_writing | 1 | paraphrase | 0.0073 | 0.0838 |