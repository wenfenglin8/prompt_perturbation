# Four-Task Similarity Sweep, PDR-Aligned Perturbations

- Batch count: `10`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Total generation rows: `6000`
- Total metric rows: `1000`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | paraphrase | 50 | 0.1031 | 0.0373 | 0.0983 | 0.0625 |
| factual_qa | SQuAD V2 | reordering | 50 | 0.0418 | 0.0262 | 0.0400 | 0.0175 |
| factual_qa | SQuAD V2 | formatting | 50 | 0.0241 | 0.0288 | 0.0437 | 0.0185 |
| factual_qa | SQuAD V2 | context_injection | 50 | 0.0309 | 0.0199 | 0.0332 | 0.0153 |
| factual_qa | SQuAD V2 | surface_noise | 50 | 0.0371 | 0.0193 | 0.0381 | 0.0202 |
| math_reasoning | MATH | paraphrase | 50 | 0.0498 | 0.0502 | 0.0512 | 0.0048 |
| math_reasoning | MATH | reordering | 50 | 0.0667 | 0.0575 | 0.0752 | 0.0200 |
| math_reasoning | MATH | formatting | 50 | 0.0588 | 0.0480 | 0.0530 | 0.0073 |
| math_reasoning | MATH | context_injection | 50 | 0.0535 | 0.0473 | 0.0505 | 0.0061 |
| math_reasoning | MATH | surface_noise | 50 | 0.0520 | 0.0516 | 0.0534 | 0.0048 |
| code_generation | HumanEval | paraphrase | 50 | 0.0718 | 0.0327 | 0.0644 | 0.0338 |
| code_generation | HumanEval | reordering | 50 | 0.0479 | 0.0300 | 0.0433 | 0.0180 |
| code_generation | HumanEval | formatting | 50 | 0.0870 | 0.0393 | 0.0832 | 0.0451 |
| code_generation | HumanEval | context_injection | 50 | 0.0210 | 0.0323 | 0.0355 | 0.0057 |
| code_generation | HumanEval | surface_noise | 50 | 0.0567 | 0.0367 | 0.0491 | 0.0147 |
| open_ended_writing | Alpaca | paraphrase | 50 | 0.0762 | 0.0711 | 0.0735 | 0.0066 |
| open_ended_writing | Alpaca | reordering | 50 | 0.0735 | 0.0766 | 0.0813 | 0.0077 |
| open_ended_writing | Alpaca | formatting | 50 | 0.0934 | 0.0683 | 0.0865 | 0.0210 |
| open_ended_writing | Alpaca | context_injection | 50 | 0.0905 | 0.0676 | 0.0859 | 0.0192 |
| open_ended_writing | Alpaca | surface_noise | 50 | 0.0696 | 0.0775 | 0.0775 | 0.0046 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | paraphrase | 0.0625 | 0.0983 |
| factual_qa | 2 | surface_noise | 0.0202 | 0.0381 |
| factual_qa | 3 | formatting | 0.0185 | 0.0437 |
| factual_qa | 4 | reordering | 0.0175 | 0.0400 |
| factual_qa | 5 | context_injection | 0.0153 | 0.0332 |
| math_reasoning | 1 | reordering | 0.0200 | 0.0752 |
| math_reasoning | 2 | formatting | 0.0073 | 0.0530 |
| math_reasoning | 3 | context_injection | 0.0061 | 0.0505 |
| math_reasoning | 4 | paraphrase | 0.0048 | 0.0512 |
| math_reasoning | 5 | surface_noise | 0.0048 | 0.0534 |
| code_generation | 1 | formatting | 0.0451 | 0.0832 |
| code_generation | 2 | paraphrase | 0.0338 | 0.0644 |
| code_generation | 3 | reordering | 0.0180 | 0.0433 |
| code_generation | 4 | surface_noise | 0.0147 | 0.0491 |
| code_generation | 5 | context_injection | 0.0057 | 0.0355 |
| open_ended_writing | 1 | formatting | 0.0210 | 0.0865 |
| open_ended_writing | 2 | context_injection | 0.0192 | 0.0859 |
| open_ended_writing | 3 | reordering | 0.0077 | 0.0813 |
| open_ended_writing | 4 | paraphrase | 0.0066 | 0.0735 |
| open_ended_writing | 5 | surface_noise | 0.0046 | 0.0775 |