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
- Tasks: `long_factual_qa`
- Long FACT QA set: `stress`
- Cases per task: `5`
- Samples per prompt version: `3`
- Generation model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Case-level rows: `30`

Only the task instruction is perturbed; passages, math problems, and HumanEval function prompts are kept unchanged.

## Mean By Strength

| strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | mean_repeated_pass_rate_drop | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 1 | 5 | 0.9873 | 0.0031 | 0.0552 | 0.0019 | 0.4000 | 0.6000 |
| 2 | 2 | 5 | 0.9872 | 0.0042 | 0.0390 | -0.0010 | 0.2000 | 0.4000 |
| 3 | 3 | 5 | 0.9901 | 0.0029 | 0.0324 | 0.0057 | 0.2000 | 0.4000 |
| 4 | 4 | 5 | 0.9914 | 0.0017 | 0.0495 | -0.0305 | 0.2000 | 0.4000 |
| 5 | 5 | 5 | 0.9893 | 0.0019 | 0.0495 | -0.0305 | 0.2000 | 0.4000 |

## Main Correlations

| scope | n | x | y | pearson | spearman |
| --- | --- | --- | --- | --- | --- |
| all_levels | 30 | strength_edits | mean_cross_similarity | -0.2064 | -0.3605 |
| all_levels | 30 | strength_edits | abs_repeated_pass_rate_change | 0.1857 | 0.1411 |
| nonzero_levels | 25 | mean_cross_similarity | abs_repeated_pass_rate_change | -0.6984 | -0.7443 |
| nonzero_levels | 25 | noise_corrected_drift | abs_repeated_pass_rate_change | 0.6431 | 0.5858 |

Similarity-to-correctness Spearman on nonzero levels is `-0.7443`. This supports the claim that lower output similarity is associated with larger correctness change.
Corrected-drift-to-correctness Spearman on nonzero levels is `0.5858`. This supports the equivalent drift framing.

## Task x Strength Means

| task | strength_level | strength_edits | n | mean_cross_similarity | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| long_factual_qa | 0 | 0 | 5 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| long_factual_qa | 1 | 1 | 5 | 0.9873 | 0.0031 | 0.0552 | 0.4000 | 0.6000 |
| long_factual_qa | 2 | 2 | 5 | 0.9872 | 0.0042 | 0.0390 | 0.2000 | 0.4000 |
| long_factual_qa | 3 | 3 | 5 | 0.9901 | 0.0029 | 0.0324 | 0.2000 | 0.4000 |
| long_factual_qa | 4 | 4 | 5 | 0.9914 | 0.0017 | 0.0495 | 0.2000 | 0.4000 |
| long_factual_qa | 5 | 5 | 5 | 0.9893 | 0.0019 | 0.0495 | 0.2000 | 0.4000 |

## Within-Case Monotonicity

- Cases where strength-to-similarity Spearman is negative: `4/5`
- Cases where strength-to-absolute-correctness-change Spearman is positive: `1/5`

## Interpretation Guide

- If strength-to-similarity is negative, the severity algorithm is successfully making outputs less similar.
- If similarity-to-correctness-change is negative, lower similarity is associated with larger correctness movement.
- If corrected-drift-to-correctness-change is positive, the result supports the RQ2 drift framing.
- If correctness metrics remain flat while similarity changes, the result should be interpreted as semantic/output instability without corresponding task-performance instability.
