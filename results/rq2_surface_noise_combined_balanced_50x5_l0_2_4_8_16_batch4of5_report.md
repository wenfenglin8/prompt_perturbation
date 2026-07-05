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
| 1 | 2 | 40 | 0.9643 | 0.0068 | 0.1015 | -0.0652 | 0.1000 | 0.4250 |
| 2 | 4 | 40 | 0.9586 | 0.0126 | 0.1170 | -0.0587 | 0.1750 | 0.4250 |
| 3 | 8 | 40 | 0.9568 | 0.0133 | 0.1210 | -0.0962 | 0.1000 | 0.4250 |
| 4 | 16 | 40 | 0.9545 | 0.0153 | 0.0984 | -0.0530 | 0.1750 | 0.3750 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 200 | strength_edits | mean_cross_similarity | -0.2322 | -0.4845 |
| all_levels | 200 | strength_edits | abs_repeated_pass_rate_change | 0.1095 | 0.2219 |
| nonzero_levels | 160 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.7916 | -0.6178 |
| nonzero_levels | 160 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.7318 | 0.3741 |

Similarity-to-correctness Spearman on nonzero levels is `-0.6178`. This supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.3741`. This supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| code_generation | 1 | 2 | 10 | 0.9427 | 0.0240 | 0.2000 | 0.1000 | 0.4000 |
| code_generation | 2 | 4 | 10 | 0.9319 | 0.0331 | 0.1800 | 0.2000 | 0.5000 |
| code_generation | 3 | 8 | 10 | 0.9265 | 0.0364 | 0.2800 | 0.1000 | 0.6000 |
| code_generation | 4 | 16 | 10 | 0.9186 | 0.0462 | 0.3000 | 0.1000 | 0.6000 |
| factual_qa | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 1 | 2 | 10 | 0.9918 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 2 | 4 | 10 | 0.9851 | 0.0084 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 3 | 8 | 10 | 0.9879 | 0.0062 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | 4 | 16 | 10 | 0.9872 | 0.0075 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 1 | 2 | 10 | 0.9751 | 0.0020 | 0.0459 | 0.3000 | 0.8000 |
| long_factual_qa | 2 | 4 | 10 | 0.9659 | 0.0069 | 0.0280 | 0.3000 | 0.5000 |
| long_factual_qa | 3 | 8 | 10 | 0.9723 | 0.0045 | 0.0242 | 0.3000 | 0.6000 |
| long_factual_qa | 4 | 16 | 10 | 0.9690 | 0.0045 | 0.0337 | 0.5000 | 0.6000 |
| math_reasoning | 0 | 0 | 10 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | 1 | 2 | 10 | 0.9474 | 0.0011 | 0.1600 | 0.0000 | 0.5000 |
| math_reasoning | 2 | 4 | 10 | 0.9516 | 0.0021 | 0.2600 | 0.2000 | 0.7000 |
| math_reasoning | 3 | 8 | 10 | 0.9406 | 0.0060 | 0.1800 | 0.0000 | 0.5000 |
| math_reasoning | 4 | 16 | 10 | 0.9431 | 0.0028 | 0.0600 | 0.1000 | 0.3000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `35/40`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `14/40`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
