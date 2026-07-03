# Four-Task Similarity Sweep

- Model: `gpt-5.4`
- Embedding model: `text-embedding-3-small`
- Cases per task: `10`
- Samples per clean / perturbed prompt: `3`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Batch: `1/1`
- Total generation calls: `1200`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | paraphrase | 10 | 0.0530 | 0.0288 | 0.0251 | 0.0000 |
| factual_qa | SQuAD V2 | reordering | 10 | 0.0000 | 0.0429 | 0.0371 | 0.0000 |
| factual_qa | SQuAD V2 | formatting | 10 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | SQuAD V2 | context_injection | 10 | 0.0763 | 0.0175 | 0.0413 | 0.0238 |
| factual_qa | SQuAD V2 | surface_noise | 10 | 0.0002 | 0.0001 | 0.0001 | 0.0000 |
| math_reasoning | MATH | paraphrase | 10 | 0.2462 | 0.1278 | 0.2764 | 0.1500 |
| math_reasoning | MATH | reordering | 10 | 0.0719 | 0.0247 | 0.0646 | 0.0400 |
| math_reasoning | MATH | formatting | 10 | 0.0621 | 0.0532 | 0.0578 | 0.0090 |
| math_reasoning | MATH | context_injection | 10 | 0.0659 | 0.0531 | 0.0679 | 0.0182 |
| math_reasoning | MATH | surface_noise | 10 | 0.0464 | 0.0379 | 0.0575 | 0.0204 |
| code_generation | HumanEval | paraphrase | 10 | 0.0262 | 0.0173 | 0.0451 | 0.0278 |
| code_generation | HumanEval | reordering | 10 | 0.0278 | 0.0193 | 0.0164 | 0.0001 |
| code_generation | HumanEval | formatting | 10 | 0.0025 | 0.0051 | 0.0058 | 0.0008 |
| code_generation | HumanEval | context_injection | 10 | 0.0374 | 0.0172 | 0.0265 | 0.0094 |
| code_generation | HumanEval | surface_noise | 10 | 0.0278 | 0.0102 | 0.0110 | 0.0007 |
| open_ended_writing | Alpaca | paraphrase | 10 | 0.0749 | 0.0875 | 0.1039 | 0.0173 |
| open_ended_writing | Alpaca | reordering | 10 | 0.1095 | 0.0631 | 0.1272 | 0.0646 |
| open_ended_writing | Alpaca | formatting | 10 | 0.1277 | 0.0804 | 0.0994 | 0.0190 |
| open_ended_writing | Alpaca | context_injection | 10 | 0.1490 | 0.0757 | 0.1368 | 0.0636 |
| open_ended_writing | Alpaca | surface_noise | 10 | 0.0871 | 0.0743 | 0.0937 | 0.0207 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | context_injection | 0.0238 | 0.0413 |
| factual_qa | 2 | reordering | 0.0000 | 0.0371 |
| factual_qa | 3 | surface_noise | 0.0000 | 0.0001 |
| factual_qa | 4 | paraphrase | 0.0000 | 0.0251 |
| factual_qa | 5 | formatting | 0.0000 | 0.0000 |
| math_reasoning | 1 | paraphrase | 0.1500 | 0.2764 |
| math_reasoning | 2 | reordering | 0.0400 | 0.0646 |
| math_reasoning | 3 | surface_noise | 0.0204 | 0.0575 |
| math_reasoning | 4 | context_injection | 0.0182 | 0.0679 |
| math_reasoning | 5 | formatting | 0.0090 | 0.0578 |
| code_generation | 1 | paraphrase | 0.0278 | 0.0451 |
| code_generation | 2 | context_injection | 0.0094 | 0.0265 |
| code_generation | 3 | formatting | 0.0008 | 0.0058 |
| code_generation | 4 | surface_noise | 0.0007 | 0.0110 |
| code_generation | 5 | reordering | 0.0001 | 0.0164 |
| open_ended_writing | 1 | reordering | 0.0646 | 0.1272 |
| open_ended_writing | 2 | context_injection | 0.0636 | 0.1368 |
| open_ended_writing | 3 | surface_noise | 0.0207 | 0.0937 |
| open_ended_writing | 4 | formatting | 0.0190 | 0.0994 |
| open_ended_writing | 5 | paraphrase | 0.0173 | 0.1039 |