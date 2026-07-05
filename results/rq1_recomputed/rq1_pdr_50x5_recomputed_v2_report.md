# RQ1 PDR 50x5 Recomputed V2 With Manual-Audited Math Equivalence And Robust Code Evaluation

## Aggregate
- metric_rows: `750`
- generation_rows: `7500`
- changed_generation_scores: `2392`
- avg_clean_single: `0.9413`
- avg_perturbed_single: `0.9382`
- avg_clean_mean: `0.9426`
- avg_perturbed_mean: `0.9395`
- uncorrected_pdr_loss: `0.0574`
- perturbed_pdr_loss: `0.0605`
- corrected_pdr: `0.0031`

## By Task
| task | n | clean single | perturbed single | clean repeated | perturbed repeated | uncorrected loss | corrected PDR |
|---|---:|---:|---:|---:|---:|---:|---:|
| factual_qa | 250 | 0.9800 | 0.9787 | 0.9789 | 0.9770 | 0.0211 | 0.0020 |
| math_reasoning | 250 | 0.8800 | 0.8680 | 0.8776 | 0.8736 | 0.1224 | 0.0040 |
| code_generation | 250 | 0.9640 | 0.9680 | 0.9712 | 0.9680 | 0.0288 | 0.0032 |

## By Perturbation And Task
| perturbation | task | n | clean single | perturbed single | clean repeated | perturbed repeated | corrected PDR |
|---|---|---:|---:|---:|---:|---:|---:|
| paraphrase | factual_qa | 50 | 0.9800 | 0.9800 | 0.9800 | 0.9728 | 0.0072 |
| paraphrase | math_reasoning | 50 | 0.8800 | 0.8600 | 0.8760 | 0.8600 | 0.0160 |
| paraphrase | code_generation | 50 | 0.9800 | 0.9600 | 0.9760 | 0.9560 | 0.0200 |
| reordering | factual_qa | 50 | 0.9800 | 0.9800 | 0.9787 | 0.9800 | -0.0013 |
| reordering | math_reasoning | 50 | 0.9000 | 0.8800 | 0.9040 | 0.8800 | 0.0240 |
| reordering | code_generation | 50 | 0.9600 | 0.9800 | 0.9640 | 0.9720 | -0.0080 |
| formatting | factual_qa | 50 | 0.9800 | 0.9733 | 0.9773 | 0.9733 | 0.0040 |
| formatting | math_reasoning | 50 | 0.8600 | 0.9200 | 0.8680 | 0.8760 | -0.0080 |
| formatting | code_generation | 50 | 0.9600 | 0.9800 | 0.9680 | 0.9680 | 0.0000 |
| context_injection | factual_qa | 50 | 0.9800 | 0.9800 | 0.9800 | 0.9787 | 0.0013 |
| context_injection | math_reasoning | 50 | 0.8600 | 0.8400 | 0.8560 | 0.8680 | -0.0120 |
| context_injection | code_generation | 50 | 0.9600 | 0.9600 | 0.9720 | 0.9680 | 0.0040 |
| surface_noise | factual_qa | 50 | 0.9800 | 0.9800 | 0.9787 | 0.9800 | -0.0013 |
| surface_noise | math_reasoning | 50 | 0.9000 | 0.8400 | 0.8840 | 0.8840 | 0.0000 |
| surface_noise | code_generation | 50 | 0.9600 | 0.9600 | 0.9760 | 0.9760 | 0.0000 |
