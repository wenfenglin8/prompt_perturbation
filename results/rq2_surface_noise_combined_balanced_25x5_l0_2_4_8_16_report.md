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
- Cases per task: `25`
- Samples per prompt version: `5`
- Generation model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Case-level rows: `500`

Only the task instruction is perturbed; passages, math problems, and HumanEval function prompts are kept unchanged.

## Mean By Strength

| strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | mean_repeated_pass_rate_drop | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 100 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 2 | 100 | 0.9692 | 0.0022 | 0.0549 | 0.0326 | 0.1900 | 0.3000 |
| 2 | 4 | 100 | 0.9632 | 0.0081 | 0.0664 | 0.0515 | 0.2400 | 0.3000 |
| 3 | 8 | 100 | 0.9595 | 0.0125 | 0.0755 | 0.0305 | 0.2200 | 0.3500 |
| 4 | 16 | 100 | 0.9564 | 0.0127 | 0.0818 | 0.0404 | 0.2100 | 0.3300 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 500 | strength_edits | mean_cross_similarity | -0.2299 | -0.4918 |
| all_levels | 500 | strength_edits | abs_repeated_pass_rate_change | 0.1514 | 0.2303 |
| nonzero_levels | 400 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.3376 | -0.3486 |
| nonzero_levels | 400 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.2945 | 0.2095 |

Similarity-to-correctness Spearman on nonzero levels is `-0.3486`. This supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.2095`. This supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | 0 | 0 | 25 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 1 | 2 | 25 | 0.9679 | 0.0046 | 0.0720 | 0.2000 | 0.2000 |
| code_generation | 2 | 4 | 25 | 0.9499 | 0.0202 | 0.1200 | 0.2000 | 0.2400 |
| code_generation | 3 | 8 | 25 | 0.9452 | 0.0258 | 0.0960 | 0.1200 | 0.2400 |
| code_generation | 4 | 16 | 25 | 0.9428 | 0.0212 | 0.0960 | 0.0800 | 0.2000 |
| factual_qa | 0 | 0 | 25 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 1 | 2 | 25 | 0.9771 | 0.0000 | 0.0027 | 0.0400 | 0.0400 |
| factual_qa | 2 | 4 | 25 | 0.9725 | 0.0084 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 3 | 8 | 25 | 0.9605 | 0.0207 | 0.0107 | 0.0400 | 0.0400 |
| factual_qa | 4 | 16 | 25 | 0.9561 | 0.0212 | 0.0107 | 0.0400 | 0.0400 |
| long_factual_qa | 0 | 0 | 25 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 1 | 2 | 25 | 0.9822 | 0.0017 | 0.0248 | 0.1600 | 0.4400 |
| long_factual_qa | 2 | 4 | 25 | 0.9807 | 0.0014 | 0.0255 | 0.4000 | 0.5600 |
| long_factual_qa | 3 | 8 | 25 | 0.9828 | 0.0014 | 0.0273 | 0.3200 | 0.6400 |
| long_factual_qa | 4 | 16 | 25 | 0.9798 | 0.0038 | 0.0367 | 0.2800 | 0.6000 |
| math_reasoning | 0 | 0 | 25 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 1 | 2 | 25 | 0.9495 | 0.0026 | 0.1200 | 0.3600 | 0.5200 |
| math_reasoning | 2 | 4 | 25 | 0.9496 | 0.0025 | 0.1200 | 0.3600 | 0.4000 |
| math_reasoning | 3 | 8 | 25 | 0.9496 | 0.0022 | 0.1680 | 0.4000 | 0.4800 |
| math_reasoning | 4 | 16 | 25 | 0.9471 | 0.0045 | 0.1840 | 0.4400 | 0.4800 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `94/100`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `38/100`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
