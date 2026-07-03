# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `50`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `7/10`
- Total generation calls: `600`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | reordering | 25 | 0.0226 | 0.0138 | 0.0172 | 0.0051 |
| math_reasoning | MATH | reordering | 25 | 0.0652 | 0.0593 | 0.0752 | 0.0180 |
| code_generation | HumanEval | reordering | 25 | 0.0289 | 0.0153 | 0.0250 | 0.0116 |
| open_ended_writing | Alpaca | reordering | 25 | 0.0730 | 0.0852 | 0.0914 | 0.0080 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | reordering | 0.0051 | 0.0172 |
| math_reasoning | 1 | reordering | 0.0180 | 0.0752 |
| code_generation | 1 | reordering | 0.0116 | 0.0250 |
| open_ended_writing | 1 | reordering | 0.0080 | 0.0914 |