# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `2`
- Samples per clean / perturbed prompt: `3`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | paraphrase | 2 | 0.1261 | 0.0000 | 0.1261 | 0.1261 |
| factual_qa | SQuAD V2 | reordering | 2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | SQuAD V2 | formatting | 2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | SQuAD V2 | context_injection | 2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | SQuAD V2 | surface_noise | 2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | MATH | paraphrase | 2 | 0.0240 | 0.0275 | 0.0270 | 0.0005 |
| math_reasoning | MATH | reordering | 2 | 0.0248 | 0.0296 | 0.0270 | 0.0000 |
| math_reasoning | MATH | formatting | 2 | 0.0438 | 0.0380 | 0.0335 | 0.0000 |
| math_reasoning | MATH | context_injection | 2 | 0.0445 | 0.0300 | 0.0319 | 0.0031 |
| math_reasoning | MATH | surface_noise | 2 | 0.0191 | 0.0306 | 0.0282 | 0.0000 |
| code_generation | HumanEval | paraphrase | 2 | 0.0568 | 0.0208 | 0.0326 | 0.0118 |
| code_generation | HumanEval | reordering | 2 | 0.0253 | 0.0306 | 0.0253 | 0.0022 |
| code_generation | HumanEval | formatting | 2 | 0.0129 | 0.0066 | 0.0069 | 0.0003 |
| code_generation | HumanEval | context_injection | 2 | 0.0550 | 0.0529 | 0.0499 | 0.0000 |
| code_generation | HumanEval | surface_noise | 2 | 0.0044 | 0.0030 | 0.0029 | 0.0000 |
| open_ended_writing | Alpaca | paraphrase | 2 | 0.0278 | 0.0260 | 0.0347 | 0.0087 |
| open_ended_writing | Alpaca | reordering | 2 | 0.0452 | 0.0614 | 0.0576 | 0.0000 |
| open_ended_writing | Alpaca | formatting | 2 | 0.0621 | 0.0191 | 0.0527 | 0.0336 |
| open_ended_writing | Alpaca | context_injection | 2 | 0.0575 | 0.0303 | 0.0671 | 0.0368 |
| open_ended_writing | Alpaca | surface_noise | 2 | 0.0404 | 0.0140 | 0.0300 | 0.0160 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | paraphrase | 0.1261 | 0.1261 |
| factual_qa | 2 | surface_noise | 0.0000 | 0.0000 |
| factual_qa | 3 | reordering | 0.0000 | 0.0000 |
| factual_qa | 4 | formatting | 0.0000 | 0.0000 |
| factual_qa | 5 | context_injection | 0.0000 | 0.0000 |
| math_reasoning | 1 | context_injection | 0.0031 | 0.0319 |
| math_reasoning | 2 | paraphrase | 0.0005 | 0.0270 |
| math_reasoning | 3 | reordering | 0.0000 | 0.0270 |
| math_reasoning | 4 | formatting | 0.0000 | 0.0335 |
| math_reasoning | 5 | surface_noise | 0.0000 | 0.0282 |
| code_generation | 1 | paraphrase | 0.0118 | 0.0326 |
| code_generation | 2 | reordering | 0.0022 | 0.0253 |
| code_generation | 3 | formatting | 0.0003 | 0.0069 |
| code_generation | 4 | context_injection | 0.0000 | 0.0499 |
| code_generation | 5 | surface_noise | 0.0000 | 0.0029 |
| open_ended_writing | 1 | context_injection | 0.0368 | 0.0671 |
| open_ended_writing | 2 | formatting | 0.0336 | 0.0527 |
| open_ended_writing | 3 | surface_noise | 0.0160 | 0.0300 |
| open_ended_writing | 4 | paraphrase | 0.0087 | 0.0347 |
| open_ended_writing | 5 | reordering | 0.0000 | 0.0576 |