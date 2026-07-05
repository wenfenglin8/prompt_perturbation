# RQ2 Surface-Noise Dose-Response Experiment

## Question

This experiment tests a stronger RQ2 design: within one perturbation family, surface noise is increased step by step, then output similarity and correctness change are measured at each severity level.

The intended dose-response pattern is:

```text
surface-noise strength increases -> output similarity decreases -> correctness change increases
```

## Design

- Perturbation family: `surface_noise`
- Strength levels, measured as corrupted instruction words: `0, 1, 2, 4, 8`
- Tasks: `long_factual_qa, math_reasoning, code_generation`
- Cases per task: `5`
- Samples per prompt version: `3`
- Generation model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Case-level rows: `75`

Only the task instruction is perturbed; passages, math problems, and HumanEval function prompts are kept unchanged.

## Mean By Strength

| strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | mean_repeated_pass_rate_drop | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 15 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 1 | 15 | 0.9594 | 0.0005 | 0.0958 | -0.0069 | 0.1333 | 0.4000 |
| 2 | 2 | 15 | 0.9631 | 0.0003 | 0.0735 | -0.0291 | 0.0667 | 0.3333 |
| 3 | 4 | 15 | 0.9585 | 0.0023 | 0.1053 | 0.0862 | 0.3333 | 0.4000 |
| 4 | 8 | 15 | 0.9470 | 0.0107 | 0.0889 | -0.0000 | 0.0667 | 0.2000 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 75 | strength_edits | mean_cross_similarity | -0.3424 | -0.5486 |
| all_levels | 75 | strength_edits | abs_repeated_pass_rate_change | 0.1317 | 0.1333 |
| nonzero_levels | 60 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.0315 | -0.2150 |
| nonzero_levels | 60 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.0827 | 0.1406 |

Similarity-to-correctness Spearman on nonzero levels is `-0.2150`. This supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.1406`. This supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 1 | 1 | 5 | 0.9770 | 0.0004 | 0.0667 | 0.0000 | 0.2000 |
| code_generation | 2 | 2 | 5 | 0.9856 | 0.0002 | 0.0667 | 0.0000 | 0.2000 |
| code_generation | 3 | 4 | 5 | 0.9797 | 0.0002 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 4 | 8 | 5 | 0.9566 | 0.0146 | 0.0667 | 0.0000 | 0.2000 |
| long_factual_qa | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 1 | 1 | 5 | 0.9611 | 0.0007 | 0.0206 | 0.0000 | 0.4000 |
| long_factual_qa | 2 | 2 | 5 | 0.9610 | 0.0001 | 0.0206 | 0.0000 | 0.4000 |
| long_factual_qa | 3 | 4 | 5 | 0.9565 | 0.0015 | 0.0492 | 0.4000 | 0.6000 |
| long_factual_qa | 4 | 8 | 5 | 0.9521 | 0.0026 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 1 | 1 | 5 | 0.9400 | 0.0002 | 0.2000 | 0.4000 | 0.6000 |
| math_reasoning | 2 | 2 | 5 | 0.9426 | 0.0006 | 0.1333 | 0.2000 | 0.4000 |
| math_reasoning | 3 | 4 | 5 | 0.9393 | 0.0052 | 0.2667 | 0.6000 | 0.6000 |
| math_reasoning | 4 | 8 | 5 | 0.9321 | 0.0149 | 0.2000 | 0.2000 | 0.4000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `15/15`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `5/15`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
