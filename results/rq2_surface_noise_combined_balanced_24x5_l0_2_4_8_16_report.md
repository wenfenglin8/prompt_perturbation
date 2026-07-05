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
- Cases per task: `24`
- Samples per prompt version: `5`
- Generation model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Case-level rows: `480`

Only the task instruction is perturbed; passages, math problems, and HumanEval function prompts are kept unchanged.

## Mean By Strength

| strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | mean_repeated_pass_rate_drop | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 96 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 2 | 96 | 0.9666 | 0.0028 | 0.0577 | 0.0067 | 0.1771 | 0.3125 |
| 2 | 4 | 96 | 0.9630 | 0.0081 | 0.0504 | 0.0157 | 0.1458 | 0.2812 |
| 3 | 8 | 96 | 0.9592 | 0.0101 | 0.0820 | -0.0060 | 0.1667 | 0.3438 |
| 4 | 16 | 96 | 0.9589 | 0.0107 | 0.0826 | -0.0022 | 0.1562 | 0.3542 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 480 | strength_edits | mean_cross_similarity | -0.2490 | -0.4742 |
| all_levels | 480 | strength_edits | abs_repeated_pass_rate_change | 0.1665 | 0.2442 |
| nonzero_levels | 384 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.4568 | -0.3264 |
| nonzero_levels | 384 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.4563 | 0.2673 |

Similarity-to-correctness Spearman on nonzero levels is `-0.3264`. This supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.2673`. This supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | 0 | 0 | 24 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 1 | 2 | 24 | 0.9534 | 0.0054 | 0.0917 | 0.0833 | 0.2500 |
| code_generation | 2 | 4 | 24 | 0.9541 | 0.0086 | 0.1000 | 0.1667 | 0.2500 |
| code_generation | 3 | 8 | 24 | 0.9361 | 0.0187 | 0.1583 | 0.0833 | 0.3750 |
| code_generation | 4 | 16 | 24 | 0.9390 | 0.0218 | 0.1417 | 0.0833 | 0.3750 |
| factual_qa | 0 | 0 | 24 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 1 | 2 | 24 | 0.9860 | 0.0001 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 2 | 4 | 24 | 0.9734 | 0.0128 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 3 | 8 | 24 | 0.9772 | 0.0123 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 4 | 16 | 24 | 0.9739 | 0.0116 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 0 | 0 | 24 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 1 | 2 | 24 | 0.9792 | 0.0042 | 0.0224 | 0.3333 | 0.5833 |
| long_factual_qa | 2 | 4 | 24 | 0.9771 | 0.0056 | 0.0266 | 0.2500 | 0.5833 |
| long_factual_qa | 3 | 8 | 24 | 0.9810 | 0.0018 | 0.0278 | 0.2500 | 0.5833 |
| long_factual_qa | 4 | 16 | 24 | 0.9772 | 0.0057 | 0.0305 | 0.1667 | 0.5417 |
| math_reasoning | 0 | 0 | 24 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 1 | 2 | 24 | 0.9478 | 0.0015 | 0.1167 | 0.2917 | 0.4167 |
| math_reasoning | 2 | 4 | 24 | 0.9474 | 0.0053 | 0.0750 | 0.1667 | 0.2917 |
| math_reasoning | 3 | 8 | 24 | 0.9425 | 0.0075 | 0.1417 | 0.3333 | 0.4167 |
| math_reasoning | 4 | 16 | 24 | 0.9455 | 0.0038 | 0.1583 | 0.3750 | 0.5000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `87/96`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `37/96`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
