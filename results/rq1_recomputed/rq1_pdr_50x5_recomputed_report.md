# RQ1 PDR 50x5 Recomputed With Robust Math/Code Evaluation

## Aggregate
- metric_rows: `750`
- generation_rows: `7500`
- changed_generation_scores: `2261`
- avg_clean_single: `0.9200`
- avg_perturbed_single: `0.9169`
- avg_clean_repeated: `0.9231`
- avg_perturbed_repeated: `0.9182`
- uncorrected_pdr_loss: `0.0769`
- perturbed_pdr_loss: `0.0818`
- corrected_pdr: `0.0049`

## By Task
| task | n | clean single | perturbed single | clean repeated | perturbed repeated | uncorrected loss | corrected PDR |
|---|---:|---:|---:|---:|---:|---:|---:|
| factual_qa | 250 | 0.9800 | 0.9787 | 0.9789 | 0.9770 | 0.0211 | 0.0020 |
| math_reasoning | 250 | 0.8160 | 0.8040 | 0.8192 | 0.8096 | 0.1808 | 0.0096 |
| code_generation | 250 | 0.9640 | 0.9680 | 0.9712 | 0.9680 | 0.0288 | 0.0032 |

## By Perturbation And Task
| perturbation | task | n | clean single | perturbed single | clean repeated | perturbed repeated | corrected PDR |
|---|---|---:|---:|---:|---:|---:|---:|
| paraphrase | factual_qa | 50 | 0.9800 | 0.9800 | 0.9800 | 0.9728 | 0.0072 |
| paraphrase | math_reasoning | 50 | 0.8000 | 0.8000 | 0.8240 | 0.8000 | 0.0240 |
| paraphrase | code_generation | 50 | 0.9800 | 0.9600 | 0.9760 | 0.9560 | 0.0200 |
| reordering | factual_qa | 50 | 0.9800 | 0.9800 | 0.9787 | 0.9800 | -0.0013 |
| reordering | math_reasoning | 50 | 0.8400 | 0.8200 | 0.8320 | 0.8200 | 0.0120 |
| reordering | code_generation | 50 | 0.9600 | 0.9800 | 0.9640 | 0.9720 | -0.0080 |
| formatting | factual_qa | 50 | 0.9800 | 0.9733 | 0.9773 | 0.9733 | 0.0040 |
| formatting | math_reasoning | 50 | 0.7800 | 0.8400 | 0.8120 | 0.8080 | 0.0040 |
| formatting | code_generation | 50 | 0.9600 | 0.9800 | 0.9680 | 0.9680 | 0.0000 |
| context_injection | factual_qa | 50 | 0.9800 | 0.9800 | 0.9800 | 0.9787 | 0.0013 |
| context_injection | math_reasoning | 50 | 0.8200 | 0.7600 | 0.8040 | 0.8040 | 0.0000 |
| context_injection | code_generation | 50 | 0.9600 | 0.9600 | 0.9720 | 0.9680 | 0.0040 |
| surface_noise | factual_qa | 50 | 0.9800 | 0.9800 | 0.9787 | 0.9800 | -0.0013 |
| surface_noise | math_reasoning | 50 | 0.8400 | 0.8000 | 0.8240 | 0.8160 | 0.0080 |
| surface_noise | code_generation | 50 | 0.9600 | 0.9600 | 0.9760 | 0.9760 | 0.0000 |
