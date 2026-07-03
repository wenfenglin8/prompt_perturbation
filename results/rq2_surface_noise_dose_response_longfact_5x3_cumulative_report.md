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
- Tasks: `long_factual_qa`
- Cases per task: `5`
- Samples per prompt version: `3`
- Generation model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Case-level rows: `25`

Only the task instruction is perturbed; passages, math problems, and HumanEval function prompts are kept unchanged.

## Mean By Strength

| strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | mean_repeated_pass_rate_drop | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 1 | 5 | 0.9739 | 0.0000 | 0.1333 | -0.0000 | 0.2000 | 0.4000 |
| 2 | 2 | 5 | 0.9629 | 0.0002 | 0.0667 | -0.0667 | 0.0000 | 0.2000 |
| 3 | 4 | 5 | 0.9763 | 0.0000 | 0.1333 | 0.1333 | 0.4000 | 0.4000 |
| 4 | 8 | 5 | 0.9563 | 0.0031 | 0.3333 | -0.2000 | 0.2000 | 0.8000 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 25 | strength_edits | mean_cross_similarity | -0.5078 | -0.6142 |
| all_levels | 25 | strength_edits | abs_repeated_pass_rate_change | 0.5500 | 0.4593 |
| nonzero_levels | 20 | mean_cross_similarity | abs_repeated_pass_rate_change | 0.1901 | 0.0017 |
| nonzero_levels | 20 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.6201 | 0.7239 |

Similarity-to-correctness Spearman on nonzero levels is `0.0017`. This does not support the expected lower-similarity / larger-correctness-change direction.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.7239`. This supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| long_factual_qa | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 1 | 1 | 5 | 0.9739 | 0.0000 | 0.1333 | 0.2000 | 0.4000 |
| long_factual_qa | 2 | 2 | 5 | 0.9629 | 0.0002 | 0.0667 | 0.0000 | 0.2000 |
| long_factual_qa | 3 | 4 | 5 | 0.9763 | 0.0000 | 0.1333 | 0.4000 | 0.4000 |
| long_factual_qa | 4 | 8 | 5 | 0.9563 | 0.0031 | 0.3333 | 0.2000 | 0.8000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `5/5`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `4/5`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
