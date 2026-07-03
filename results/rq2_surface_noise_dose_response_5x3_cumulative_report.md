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
- Tasks: `factual_qa, math_reasoning, code_generation`
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
| 1 | 1 | 15 | 0.9700 | 0.0019 | 0.1111 | 0.0667 | 0.1333 | 0.2000 |
| 2 | 2 | 15 | 0.9671 | 0.0026 | 0.0889 | 0.0000 | 0.1333 | 0.2667 |
| 3 | 4 | 15 | 0.9603 | 0.0051 | 0.1556 | 0.1111 | 0.2667 | 0.3333 |
| 4 | 8 | 15 | 0.9560 | 0.0095 | 0.2000 | 0.0667 | 0.2667 | 0.4000 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 75 | strength_edits | mean_cross_similarity | -0.3483 | -0.5225 |
| all_levels | 75 | strength_edits | abs_repeated_pass_rate_change | 0.2635 | 0.3062 |
| nonzero_levels | 60 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.1954 | -0.2829 |
| nonzero_levels | 60 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.1660 | -0.0363 |

Similarity-to-correctness Spearman on nonzero levels is `-0.2829`. This supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `-0.0363`. This does not support the expected corrected-drift / correctness-change direction at this scale.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 1 | 1 | 5 | 0.9661 | 0.0029 | 0.0667 | 0.0000 | 0.2000 |
| code_generation | 2 | 2 | 5 | 0.9621 | 0.0078 | 0.0667 | 0.0000 | 0.2000 |
| code_generation | 3 | 4 | 5 | 0.9535 | 0.0112 | 0.0667 | 0.2000 | 0.2000 |
| code_generation | 4 | 8 | 5 | 0.9399 | 0.0227 | 0.1333 | 0.0000 | 0.2000 |
| factual_qa | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 1 | 1 | 5 | 0.9882 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 2 | 2 | 5 | 0.9904 | 0.0000 | 0.0667 | 0.2000 | 0.2000 |
| factual_qa | 3 | 4 | 5 | 0.9863 | 0.0003 | 0.1333 | 0.2000 | 0.4000 |
| factual_qa | 4 | 8 | 5 | 0.9912 | 0.0000 | 0.1333 | 0.4000 | 0.4000 |
| math_reasoning | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 1 | 1 | 5 | 0.9555 | 0.0027 | 0.2667 | 0.4000 | 0.4000 |
| math_reasoning | 2 | 2 | 5 | 0.9486 | 0.0000 | 0.1333 | 0.2000 | 0.4000 |
| math_reasoning | 3 | 4 | 5 | 0.9410 | 0.0039 | 0.2667 | 0.4000 | 0.4000 |
| math_reasoning | 4 | 8 | 5 | 0.9370 | 0.0057 | 0.3333 | 0.4000 | 0.6000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `14/15`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `6/15`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
