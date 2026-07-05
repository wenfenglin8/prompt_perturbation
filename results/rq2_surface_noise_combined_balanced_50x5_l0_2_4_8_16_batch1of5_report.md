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
| 1 | 2 | 40 | 0.9562 | 0.0066 | 0.0746 | -0.0176 | 0.1500 | 0.4250 |
| 2 | 4 | 40 | 0.9561 | 0.0059 | 0.0717 | -0.0136 | 0.1500 | 0.3750 |
| 3 | 8 | 40 | 0.9501 | 0.0127 | 0.1234 | -0.0550 | 0.1750 | 0.4750 |
| 4 | 16 | 40 | 0.9501 | 0.0112 | 0.1103 | -0.0260 | 0.2750 | 0.5250 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 200 | strength_edits | mean_cross_similarity | -0.2696 | -0.4923 |
| all_levels | 200 | strength_edits | abs_repeated_pass_rate_change | 0.2181 | 0.3252 |
| nonzero_levels | 160 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.4681 | -0.3309 |
| nonzero_levels | 160 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.4700 | 0.2473 |

Similarity-to-correctness Spearman on nonzero levels is `-0.3309`. This supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.2473`. This supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 1 | 2 | 10 | 0.9257 | 0.0158 | 0.1400 | 0.2000 | 0.4000 |
| code_generation | 2 | 4 | 10 | 0.9270 | 0.0047 | 0.1200 | 0.1000 | 0.4000 |
| code_generation | 3 | 8 | 10 | 0.9053 | 0.0318 | 0.2800 | 0.0000 | 0.6000 |
| code_generation | 4 | 16 | 10 | 0.9146 | 0.0227 | 0.2600 | 0.1000 | 0.7000 |
| factual_qa | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 1 | 2 | 10 | 0.9761 | 0.0051 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 2 | 4 | 10 | 0.9686 | 0.0131 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 3 | 8 | 10 | 0.9701 | 0.0098 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 4 | 16 | 10 | 0.9645 | 0.0121 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 1 | 2 | 10 | 0.9651 | 0.0047 | 0.0385 | 0.3000 | 0.8000 |
| long_factual_qa | 2 | 4 | 10 | 0.9707 | 0.0046 | 0.0466 | 0.3000 | 0.6000 |
| long_factual_qa | 3 | 8 | 10 | 0.9671 | 0.0046 | 0.0536 | 0.4000 | 0.7000 |
| long_factual_qa | 4 | 16 | 10 | 0.9672 | 0.0044 | 0.0614 | 0.7000 | 1.0000 |
| math_reasoning | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 1 | 2 | 10 | 0.9580 | 0.0010 | 0.1200 | 0.1000 | 0.5000 |
| math_reasoning | 2 | 4 | 10 | 0.9580 | 0.0013 | 0.1200 | 0.2000 | 0.5000 |
| math_reasoning | 3 | 8 | 10 | 0.9581 | 0.0047 | 0.1600 | 0.3000 | 0.6000 |
| math_reasoning | 4 | 16 | 10 | 0.9541 | 0.0055 | 0.1200 | 0.3000 | 0.4000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `38/40`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `22/40`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
