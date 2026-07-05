# RQ2 context_injection Dose-Response Experiment

## Question

This experiment tests a stronger RQ2 design: within one perturbation family, perturbation strength is increased step by step, then output similarity and correctness change are measured at each severity level.

The intended dose-response pattern is:

```text
context_injection strength increases -> output similarity decreases -> correctness change increases
```

## Design

- Perturbation family: `context_injection`
- Strength levels: `0, 1, 2, 3, 4, 5`
- Tasks: `long_factual_qa, math_reasoning, code_generation`
- Long FACT QA set: `stress`
- Cases per task: `5`
- Samples per prompt version: `3`
- Generation model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Case-level rows: `90`

Only the task instruction is perturbed; passages, math problems, and HumanEval function prompts are kept unchanged.

## Mean By Strength

| strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | mean_repeated_pass_rate_drop | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 15 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 1 | 15 | 0.9453 | 0.0293 | 0.2275 | -0.0481 | 0.2000 | 0.5333 |
| 2 | 2 | 15 | 0.9510 | 0.0119 | 0.1483 | -0.0594 | 0.1333 | 0.4000 |
| 3 | 3 | 15 | 0.9502 | 0.0271 | 0.1671 | -0.1163 | 0.1333 | 0.4000 |
| 4 | 4 | 15 | 0.9613 | 0.0106 | 0.1836 | -0.1264 | 0.1333 | 0.5333 |
| 5 | 5 | 15 | 0.9642 | 0.0104 | 0.1550 | -0.1550 | 0.0000 | 0.4000 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 90 | strength_edits | mean_cross_similarity | -0.1184 | -0.3653 |
| all_levels | 90 | strength_edits | abs_repeated_pass_rate_change | 0.1255 | 0.1946 |
| nonzero_levels | 75 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.2628 | -0.2992 |
| nonzero_levels | 75 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.2251 | 0.1802 |

Similarity-to-correctness Spearman on nonzero levels is `-0.2992`. This supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.1802`. This supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 1 | 1 | 5 | 0.9019 | 0.0835 | 0.2667 | 0.2000 | 0.4000 |
| code_generation | 2 | 2 | 5 | 0.9244 | 0.0285 | 0.0667 | 0.2000 | 0.2000 |
| code_generation | 3 | 3 | 5 | 0.9347 | 0.0466 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 4 | 4 | 5 | 0.9598 | 0.0148 | 0.0667 | 0.0000 | 0.2000 |
| code_generation | 5 | 5 | 5 | 0.9706 | 0.0141 | 0.0667 | 0.0000 | 0.2000 |
| long_factual_qa | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 1 | 1 | 5 | 0.9812 | 0.0033 | 0.0824 | 0.4000 | 0.6000 |
| long_factual_qa | 2 | 2 | 5 | 0.9877 | 0.0012 | 0.0450 | 0.0000 | 0.4000 |
| long_factual_qa | 3 | 3 | 5 | 0.9874 | 0.0021 | 0.0345 | 0.2000 | 0.4000 |
| long_factual_qa | 4 | 4 | 5 | 0.9866 | 0.0026 | 0.0840 | 0.2000 | 0.6000 |
| long_factual_qa | 5 | 5 | 5 | 0.9875 | 0.0023 | 0.0650 | 0.0000 | 0.4000 |
| math_reasoning | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 1 | 1 | 5 | 0.9528 | 0.0010 | 0.3333 | 0.0000 | 0.6000 |
| math_reasoning | 2 | 2 | 5 | 0.9409 | 0.0059 | 0.3333 | 0.2000 | 0.6000 |
| math_reasoning | 3 | 3 | 5 | 0.9284 | 0.0327 | 0.4667 | 0.2000 | 0.8000 |
| math_reasoning | 4 | 4 | 5 | 0.9375 | 0.0144 | 0.4000 | 0.2000 | 0.8000 |
| math_reasoning | 5 | 5 | 5 | 0.9346 | 0.0147 | 0.3333 | 0.0000 | 0.6000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `13/15`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `8/15`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
