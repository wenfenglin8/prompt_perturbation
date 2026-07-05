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
| 1 | 2 | 40 | 0.9508 | 0.0140 | 0.0962 | -0.0219 | 0.1750 | 0.4000 |
| 2 | 4 | 40 | 0.9537 | 0.0171 | 0.0733 | -0.0225 | 0.1000 | 0.3250 |
| 3 | 8 | 40 | 0.9504 | 0.0146 | 0.0832 | 0.0035 | 0.2500 | 0.4250 |
| 4 | 16 | 40 | 0.9460 | 0.0167 | 0.1037 | -0.0113 | 0.2250 | 0.4500 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 200 | strength_edits | mean_cross_similarity | -0.1706 | -0.4841 |
| all_levels | 200 | strength_edits | abs_repeated_pass_rate_change | 0.1293 | 0.2841 |
| nonzero_levels | 160 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.5530 | -0.4489 |
| nonzero_levels | 160 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.7424 | 0.2979 |

Similarity-to-correctness Spearman on nonzero levels is `-0.4489`. This supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.2979`. This supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 1 | 2 | 10 | 0.9168 | 0.0492 | 0.2400 | 0.1000 | 0.3000 |
| code_generation | 2 | 4 | 10 | 0.9320 | 0.0390 | 0.1800 | 0.1000 | 0.2000 |
| code_generation | 3 | 8 | 10 | 0.9247 | 0.0480 | 0.1400 | 0.1000 | 0.3000 |
| code_generation | 4 | 16 | 10 | 0.9187 | 0.0436 | 0.1800 | 0.1000 | 0.3000 |
| factual_qa | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 1 | 2 | 10 | 0.9484 | 0.0043 | 0.0133 | 0.1000 | 0.1000 |
| factual_qa | 2 | 4 | 10 | 0.9526 | 0.0161 | 0.0067 | 0.0000 | 0.1000 |
| factual_qa | 3 | 8 | 10 | 0.9431 | 0.0044 | 0.0067 | 0.1000 | 0.1000 |
| factual_qa | 4 | 16 | 10 | 0.9469 | 0.0062 | 0.0067 | 0.1000 | 0.1000 |
| long_factual_qa | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 1 | 2 | 10 | 0.9788 | 0.0013 | 0.0514 | 0.4000 | 0.9000 |
| long_factual_qa | 2 | 4 | 10 | 0.9704 | 0.0122 | 0.0465 | 0.3000 | 0.7000 |
| long_factual_qa | 3 | 8 | 10 | 0.9763 | 0.0036 | 0.0463 | 0.4000 | 0.8000 |
| long_factual_qa | 4 | 16 | 10 | 0.9607 | 0.0163 | 0.0683 | 0.4000 | 0.9000 |
| math_reasoning | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 1 | 2 | 10 | 0.9593 | 0.0012 | 0.0800 | 0.1000 | 0.3000 |
| math_reasoning | 2 | 4 | 10 | 0.9598 | 0.0008 | 0.0600 | 0.0000 | 0.3000 |
| math_reasoning | 3 | 8 | 10 | 0.9574 | 0.0023 | 0.1400 | 0.4000 | 0.5000 |
| math_reasoning | 4 | 16 | 10 | 0.9576 | 0.0007 | 0.1600 | 0.3000 | 0.5000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `37/40`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `18/40`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
