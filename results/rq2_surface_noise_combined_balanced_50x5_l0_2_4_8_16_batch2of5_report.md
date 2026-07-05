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
| 1 | 2 | 40 | 0.9736 | 0.0034 | 0.0516 | 0.0057 | 0.1500 | 0.3250 |
| 2 | 4 | 40 | 0.9759 | 0.0015 | 0.0406 | -0.0054 | 0.1500 | 0.3000 |
| 3 | 8 | 40 | 0.9720 | 0.0074 | 0.0493 | 0.0041 | 0.1500 | 0.3500 |
| 4 | 16 | 40 | 0.9667 | 0.0091 | 0.0438 | -0.0046 | 0.1000 | 0.3000 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 200 | strength_edits | mean_cross_similarity | -0.2588 | -0.4896 |
| all_levels | 200 | strength_edits | abs_repeated_pass_rate_change | 0.0992 | 0.2002 |
| nonzero_levels | 160 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.3569 | -0.3299 |
| nonzero_levels | 160 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.0960 | 0.2759 |

Similarity-to-correctness Spearman on nonzero levels is `-0.3299`. This supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.2759`. This supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 1 | 2 | 10 | 0.9648 | 0.0115 | 0.0600 | 0.1000 | 0.2000 |
| code_generation | 2 | 4 | 10 | 0.9827 | 0.0001 | 0.0200 | 0.0000 | 0.1000 |
| code_generation | 3 | 8 | 10 | 0.9598 | 0.0200 | 0.0200 | 0.0000 | 0.1000 |
| code_generation | 4 | 16 | 10 | 0.9687 | 0.0118 | 0.0200 | 0.0000 | 0.1000 |
| factual_qa | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 1 | 2 | 10 | 0.9899 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 2 | 4 | 10 | 0.9847 | 0.0038 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 3 | 8 | 10 | 0.9884 | 0.0068 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 4 | 16 | 10 | 0.9747 | 0.0148 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 1 | 2 | 10 | 0.9862 | 0.0014 | 0.0462 | 0.3000 | 0.8000 |
| long_factual_qa | 2 | 4 | 10 | 0.9824 | 0.0016 | 0.0426 | 0.5000 | 0.8000 |
| long_factual_qa | 3 | 8 | 10 | 0.9854 | 0.0011 | 0.0573 | 0.3000 | 0.8000 |
| long_factual_qa | 4 | 16 | 10 | 0.9675 | 0.0074 | 0.0750 | 0.3000 | 0.8000 |
| math_reasoning | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 1 | 2 | 10 | 0.9536 | 0.0008 | 0.1000 | 0.2000 | 0.3000 |
| math_reasoning | 2 | 4 | 10 | 0.9536 | 0.0005 | 0.1000 | 0.1000 | 0.3000 |
| math_reasoning | 3 | 8 | 10 | 0.9544 | 0.0018 | 0.1200 | 0.3000 | 0.5000 |
| math_reasoning | 4 | 16 | 10 | 0.9561 | 0.0025 | 0.0800 | 0.1000 | 0.3000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `38/40`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `13/40`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
