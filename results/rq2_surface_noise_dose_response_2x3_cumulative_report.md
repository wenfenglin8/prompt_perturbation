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
- Cases per task: `2`
- Samples per prompt version: `3`
- Generation model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Case-level rows: `30`

Only the task instruction is perturbed; passages, math problems, and HumanEval function prompts are kept unchanged.

## Mean By Strength

| strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | mean_repeated_pass_rate_drop | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 6 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 1 | 6 | 0.9792 | 0.0002 | 0.1111 | 0.1111 | 0.3333 | 0.3333 |
| 2 | 2 | 6 | 0.9787 | 0.0001 | 0.0556 | 0.0556 | 0.1667 | 0.1667 |
| 3 | 4 | 6 | 0.9728 | 0.0029 | 0.1667 | 0.1667 | 0.5000 | 0.5000 |
| 4 | 8 | 6 | 0.9707 | 0.0036 | 0.1111 | 0.1111 | 0.3333 | 0.3333 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 30 | strength_edits | mean_cross_similarity | -0.4555 | -0.5804 |
| all_levels | 30 | strength_edits | abs_repeated_pass_rate_change | 0.2132 | 0.2465 |
| nonzero_levels | 24 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.5875 | -0.5929 |
| nonzero_levels | 24 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.4204 | 0.3772 |

Similarity-to-correctness Spearman on nonzero levels is `-0.5929`. A negative value supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.3772`. A positive value supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | 0 | 0 | 2 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 1 | 1 | 2 | 0.9793 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 2 | 2 | 2 | 0.9784 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 3 | 4 | 2 | 0.9779 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 4 | 8 | 2 | 0.9732 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 0 | 0 | 2 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 1 | 1 | 2 | 0.9828 | 0.0000 | 0.1667 | 0.5000 | 0.5000 |
| factual_qa | 2 | 2 | 2 | 0.9828 | 0.0000 | 0.1667 | 0.5000 | 0.5000 |
| factual_qa | 3 | 4 | 2 | 0.9828 | 0.0000 | 0.1667 | 0.5000 | 0.5000 |
| factual_qa | 4 | 8 | 2 | 0.9828 | 0.0000 | 0.1667 | 0.5000 | 0.5000 |
| math_reasoning | 0 | 0 | 2 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 1 | 1 | 2 | 0.9755 | 0.0007 | 0.1667 | 0.5000 | 0.5000 |
| math_reasoning | 2 | 2 | 2 | 0.9748 | 0.0003 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 3 | 4 | 2 | 0.9576 | 0.0087 | 0.3333 | 1.0000 | 1.0000 |
| math_reasoning | 4 | 8 | 2 | 0.9561 | 0.0107 | 0.1667 | 0.5000 | 0.5000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `5/6`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `2/6`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
