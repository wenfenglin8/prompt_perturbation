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
- Cases per task: `12`
- Samples per prompt version: `5`
- Generation model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Case-level rows: `240`

Only the task instruction is perturbed; passages, math problems, and HumanEval function prompts are kept unchanged.

## Mean By Strength

| strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | mean_repeated_pass_rate_drop | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 48 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 2 | 48 | 0.9677 | 0.0029 | 0.0663 | 0.0142 | 0.1458 | 0.2708 |
| 2 | 4 | 48 | 0.9634 | 0.0068 | 0.0760 | 0.0483 | 0.2083 | 0.2917 |
| 3 | 8 | 48 | 0.9676 | 0.0043 | 0.0761 | 0.0500 | 0.2708 | 0.3542 |
| 4 | 16 | 48 | 0.9647 | 0.0057 | 0.0734 | 0.0373 | 0.2083 | 0.3125 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 240 | strength_edits | mean_cross_similarity | -0.2012 | -0.4764 |
| all_levels | 240 | strength_edits | abs_repeated_pass_rate_change | 0.1015 | 0.2311 |
| nonzero_levels | 192 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.2668 | -0.2443 |
| nonzero_levels | 192 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.6123 | 0.2067 |

Similarity-to-correctness Spearman on nonzero levels is `-0.2443`. This supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.2067`. This supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | 0 | 0 | 12 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 1 | 2 | 12 | 0.9585 | 0.0100 | 0.1000 | 0.0833 | 0.1667 |
| code_generation | 2 | 4 | 12 | 0.9418 | 0.0208 | 0.1500 | 0.2500 | 0.2500 |
| code_generation | 3 | 8 | 12 | 0.9529 | 0.0070 | 0.0833 | 0.1667 | 0.2500 |
| code_generation | 4 | 16 | 12 | 0.9571 | 0.0084 | 0.0833 | 0.0833 | 0.1667 |
| factual_qa | 0 | 0 | 12 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 1 | 2 | 12 | 0.9745 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 2 | 4 | 12 | 0.9755 | 0.0043 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 3 | 8 | 12 | 0.9832 | 0.0055 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 4 | 16 | 12 | 0.9692 | 0.0074 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 0 | 0 | 12 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 1 | 2 | 12 | 0.9902 | 0.0004 | 0.0152 | 0.3333 | 0.5000 |
| long_factual_qa | 2 | 4 | 12 | 0.9872 | 0.0014 | 0.0208 | 0.3333 | 0.5000 |
| long_factual_qa | 3 | 8 | 12 | 0.9890 | 0.0009 | 0.0210 | 0.5000 | 0.5833 |
| long_factual_qa | 4 | 16 | 12 | 0.9876 | 0.0010 | 0.0268 | 0.4167 | 0.5833 |
| math_reasoning | 0 | 0 | 12 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 1 | 2 | 12 | 0.9476 | 0.0010 | 0.1500 | 0.1667 | 0.4167 |
| math_reasoning | 2 | 4 | 12 | 0.9489 | 0.0006 | 0.1333 | 0.2500 | 0.4167 |
| math_reasoning | 3 | 8 | 12 | 0.9453 | 0.0037 | 0.2000 | 0.4167 | 0.5833 |
| math_reasoning | 4 | 16 | 12 | 0.9450 | 0.0061 | 0.1833 | 0.3333 | 0.5000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `45/48`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `17/48`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
