# Four-Task Similarity Sweep, PDR-Aligned Perturbations

- Batch count: `5`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Total generation rows: `1200`
- Total metric rows: `200`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | paraphrase | 10 | 0.0697 | 0.0349 | 0.0960 | 0.0611 |
| factual_qa | SQuAD V2 | reordering | 10 | 0.0476 | 0.0179 | 0.0172 | 0.0000 |
| factual_qa | SQuAD V2 | formatting | 10 | 0.0000 | 0.0190 | 0.0315 | 0.0139 |
| factual_qa | SQuAD V2 | context_injection | 10 | 0.0171 | 0.0263 | 0.0387 | 0.0150 |
| factual_qa | SQuAD V2 | surface_noise | 10 | 0.0313 | 0.0253 | 0.0351 | 0.0098 |
| math_reasoning | MATH | paraphrase | 10 | 0.0375 | 0.0442 | 0.0465 | 0.0045 |
| math_reasoning | MATH | reordering | 10 | 0.0681 | 0.0546 | 0.0543 | 0.0025 |
| math_reasoning | MATH | formatting | 10 | 0.0566 | 0.0470 | 0.0509 | 0.0069 |
| math_reasoning | MATH | context_injection | 10 | 0.0655 | 0.0526 | 0.0561 | 0.0052 |
| math_reasoning | MATH | surface_noise | 10 | 0.0638 | 0.0512 | 0.0616 | 0.0111 |
| code_generation | HumanEval | paraphrase | 10 | 0.0543 | 0.0313 | 0.0485 | 0.0198 |
| code_generation | HumanEval | reordering | 10 | 0.0623 | 0.0368 | 0.0551 | 0.0208 |
| code_generation | HumanEval | formatting | 10 | 0.0360 | 0.0313 | 0.0552 | 0.0294 |
| code_generation | HumanEval | context_injection | 10 | 0.0187 | 0.0272 | 0.0390 | 0.0161 |
| code_generation | HumanEval | surface_noise | 10 | 0.0538 | 0.0360 | 0.0605 | 0.0288 |
| open_ended_writing | Alpaca | paraphrase | 10 | 0.1207 | 0.1262 | 0.1278 | 0.0138 |
| open_ended_writing | Alpaca | reordering | 10 | 0.1092 | 0.1036 | 0.1152 | 0.0180 |
| open_ended_writing | Alpaca | formatting | 10 | 0.1369 | 0.1017 | 0.1569 | 0.0588 |
| open_ended_writing | Alpaca | context_injection | 10 | 0.1482 | 0.1220 | 0.1331 | 0.0209 |
| open_ended_writing | Alpaca | surface_noise | 10 | 0.1434 | 0.1025 | 0.1184 | 0.0265 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | paraphrase | 0.0611 | 0.0960 |
| factual_qa | 2 | context_injection | 0.0150 | 0.0387 |
| factual_qa | 3 | formatting | 0.0139 | 0.0315 |
| factual_qa | 4 | surface_noise | 0.0098 | 0.0351 |
| factual_qa | 5 | reordering | 0.0000 | 0.0172 |
| math_reasoning | 1 | surface_noise | 0.0111 | 0.0616 |
| math_reasoning | 2 | formatting | 0.0069 | 0.0509 |
| math_reasoning | 3 | context_injection | 0.0052 | 0.0561 |
| math_reasoning | 4 | paraphrase | 0.0045 | 0.0465 |
| math_reasoning | 5 | reordering | 0.0025 | 0.0543 |
| code_generation | 1 | formatting | 0.0294 | 0.0552 |
| code_generation | 2 | surface_noise | 0.0288 | 0.0605 |
| code_generation | 3 | reordering | 0.0208 | 0.0551 |
| code_generation | 4 | paraphrase | 0.0198 | 0.0485 |
| code_generation | 5 | context_injection | 0.0161 | 0.0390 |
| open_ended_writing | 1 | formatting | 0.0588 | 0.1569 |
| open_ended_writing | 2 | surface_noise | 0.0265 | 0.1184 |
| open_ended_writing | 3 | context_injection | 0.0209 | 0.1331 |
| open_ended_writing | 4 | reordering | 0.0180 | 0.1152 |
| open_ended_writing | 5 | paraphrase | 0.0138 | 0.1278 |