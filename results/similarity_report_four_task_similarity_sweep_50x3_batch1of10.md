# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `50`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `1/10`
- Total generation calls: `600`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | paraphrase | 25 | 0.1301 | 0.0393 | 0.1152 | 0.0784 |
| math_reasoning | MATH | paraphrase | 25 | 0.0499 | 0.0503 | 0.0494 | 0.0040 |
| code_generation | HumanEval | paraphrase | 25 | 0.0806 | 0.0334 | 0.0786 | 0.0481 |
| open_ended_writing | Alpaca | paraphrase | 25 | 0.0601 | 0.0626 | 0.0633 | 0.0059 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | paraphrase | 0.0784 | 0.1152 |
| math_reasoning | 1 | paraphrase | 0.0040 | 0.0494 |
| code_generation | 1 | paraphrase | 0.0481 | 0.0786 |
| open_ended_writing | 1 | paraphrase | 0.0059 | 0.0633 |