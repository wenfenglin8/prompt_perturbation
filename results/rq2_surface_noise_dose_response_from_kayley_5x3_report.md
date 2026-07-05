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
| 1 | 1 | 15 | 0.9707 | 0.0013 | 0.1333 | -0.0444 | 0.0667 | 0.2667 |
| 2 | 2 | 15 | 0.9721 | 0.0008 | 0.0889 | -0.0444 | 0.0667 | 0.2667 |
| 3 | 4 | 15 | 0.9656 | 0.0015 | 0.0667 | -0.0222 | 0.0667 | 0.2000 |
| 4 | 8 | 15 | 0.9640 | 0.0057 | 0.1556 | -0.0222 | 0.0667 | 0.3333 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 75 | strength_edits | mean_cross_similarity | -0.2628 | -0.4164 |
| all_levels | 75 | strength_edits | abs_repeated_pass_rate_change | 0.1808 | 0.1903 |
| nonzero_levels | 60 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.3185 | -0.4914 |
| nonzero_levels | 60 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.1898 | 0.2622 |

Similarity-to-correctness Spearman on nonzero levels is `-0.4914`. This supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.2622`. This supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 1 | 1 | 5 | 0.9802 | 0.0000 | 0.0667 | 0.0000 | 0.2000 |
| code_generation | 2 | 2 | 5 | 0.9752 | 0.0000 | 0.0667 | 0.0000 | 0.2000 |
| code_generation | 3 | 4 | 5 | 0.9632 | 0.0003 | 0.0667 | 0.0000 | 0.2000 |
| code_generation | 4 | 8 | 5 | 0.9566 | 0.0091 | 0.0667 | 0.0000 | 0.2000 |
| factual_qa | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 1 | 1 | 5 | 0.9981 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 2 | 2 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 3 | 4 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 4 | 8 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 1 | 1 | 5 | 0.9339 | 0.0039 | 0.3333 | 0.2000 | 0.6000 |
| math_reasoning | 2 | 2 | 5 | 0.9412 | 0.0023 | 0.2000 | 0.2000 | 0.6000 |
| math_reasoning | 3 | 4 | 5 | 0.9335 | 0.0040 | 0.1333 | 0.2000 | 0.4000 |
| math_reasoning | 4 | 8 | 5 | 0.9353 | 0.0081 | 0.4000 | 0.2000 | 0.8000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `11/15`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `5/15`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
