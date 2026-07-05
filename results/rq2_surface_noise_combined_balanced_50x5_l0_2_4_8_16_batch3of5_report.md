# RQ2 surface_noise Dose-Response Experiment

## Question

This experiment tests a stronger RQ2 design: within one perturbation family, perturbation strength is increased step by step, then output similarity and correctness change are measured at each severity level.

The intended dose-response pattern is:

```text
surface_noise strength increases -> output similarity decreases -> correctness change increases
```

## Design

- Perturbation family: `surface_noise`
- Strength levels: `0, 2, 4, 8, 16`
- Tasks: `factual_qa, long_factual_qa, math_reasoning, code_generation`
- Long FACT QA set: `stress`
- Cases per task: `50`
- Samples per prompt version: `5`
- Generation model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Case-level rows: `200`

Only the task instruction is perturbed; passages, math problems, and HumanEval function prompts are kept unchanged.

## Mean By Strength

| strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | mean_repeated_pass_rate_drop | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 40 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 2 | 40 | 0.9608 | 0.0041 | 0.0667 | -0.0309 | 0.1750 | 0.3750 |
| 2 | 4 | 40 | 0.9461 | 0.0176 | 0.1420 | 0.0177 | 0.2750 | 0.4500 |
| 3 | 8 | 40 | 0.9533 | 0.0144 | 0.1151 | -0.0116 | 0.2750 | 0.4000 |
| 4 | 16 | 40 | 0.9497 | 0.0130 | 0.1259 | 0.0078 | 0.3500 | 0.5000 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 200 | strength_edits | mean_cross_similarity | -0.2159 | -0.4901 |
| all_levels | 200 | strength_edits | abs_repeated_pass_rate_change | 0.1806 | 0.2997 |
| nonzero_levels | 160 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.5685 | -0.4473 |
| nonzero_levels | 160 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.4979 | 0.3750 |

Similarity-to-correctness Spearman on nonzero levels is `-0.4473`. This supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.3750`. This supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 1 | 2 | 10 | 0.9407 | 0.0099 | 0.1200 | 0.0000 | 0.3000 |
| code_generation | 2 | 4 | 10 | 0.9294 | 0.0279 | 0.1600 | 0.1000 | 0.3000 |
| code_generation | 3 | 8 | 10 | 0.9188 | 0.0348 | 0.2600 | 0.1000 | 0.4000 |
| code_generation | 4 | 16 | 10 | 0.9130 | 0.0285 | 0.2600 | 0.1000 | 0.5000 |
| factual_qa | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 1 | 2 | 10 | 0.9857 | 0.0048 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 2 | 4 | 10 | 0.9617 | 0.0159 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 3 | 8 | 10 | 0.9780 | 0.0177 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 4 | 16 | 10 | 0.9691 | 0.0177 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 1 | 2 | 10 | 0.9620 | 0.0007 | 0.0470 | 0.5000 | 0.8000 |
| long_factual_qa | 2 | 4 | 10 | 0.9437 | 0.0228 | 0.0679 | 0.5000 | 0.7000 |
| long_factual_qa | 3 | 8 | 10 | 0.9608 | 0.0034 | 0.0403 | 0.4000 | 0.5000 |
| long_factual_qa | 4 | 16 | 10 | 0.9642 | 0.0042 | 0.0436 | 0.7000 | 0.9000 |
| math_reasoning | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 1 | 2 | 10 | 0.9548 | 0.0010 | 0.1000 | 0.2000 | 0.4000 |
| math_reasoning | 2 | 4 | 10 | 0.9495 | 0.0036 | 0.3400 | 0.5000 | 0.8000 |
| math_reasoning | 3 | 8 | 10 | 0.9556 | 0.0016 | 0.1600 | 0.6000 | 0.7000 |
| math_reasoning | 4 | 16 | 10 | 0.9525 | 0.0016 | 0.2000 | 0.6000 | 0.6000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `38/40`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `21/40`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
