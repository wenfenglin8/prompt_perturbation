# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `50`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `2/10`
- Total generation calls: `600`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | reordering | 25 | 0.0610 | 0.0387 | 0.0628 | 0.0300 |
| math_reasoning | MATH | reordering | 25 | 0.0683 | 0.0556 | 0.0753 | 0.0221 |
| code_generation | HumanEval | reordering | 25 | 0.0670 | 0.0448 | 0.0617 | 0.0244 |
| open_ended_writing | Alpaca | reordering | 25 | 0.0740 | 0.0680 | 0.0713 | 0.0073 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | reordering | 0.0300 | 0.0628 |
| math_reasoning | 1 | reordering | 0.0221 | 0.0753 |
| code_generation | 1 | reordering | 0.0244 | 0.0617 |
| open_ended_writing | 1 | reordering | 0.0073 | 0.0713 |