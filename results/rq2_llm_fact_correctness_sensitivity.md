# RQ2 Sensitivity Analysis: Factual QA with LLM Equivalence Correctness

## What Changed

This run changes only the `factual_qa` correctness algorithm.

Original factual QA correctness:

```text
normalized exact match
```

New factual QA correctness:

```text
LLM equivalence judge
```

Math and code correctness are unchanged:

- `math_reasoning`: final-answer exact match.
- `code_generation`: HumanEval unit-test pass/fail.

## Judge Setup

| Item | Value |
|---|---:|
| Judge model | `gpt-4o-mini` |
| Factual outputs judged | 300 |
| Factual case-level comparisons | 50 |
| Original generations reused | yes |
| New answer generation | no |

The judge was instructed to mark a factual answer correct if the candidate answer is semantically equivalent to at least one reference answer, including longer answers that contain the correct answer without contradiction.

## Output Files

| File | Purpose |
|---|---|
| `results/rq2_semantic_correctness_llm_fact_factual_judgments.csv` | Per-output LLM factual correctness judgments |
| `results/rq2_semantic_correctness_llm_fact_factual_pdr_metrics.csv` | Factual-only PDR metrics using LLM correctness |
| `results/rq2_semantic_correctness_llm_fact_combined_pdr_metrics.csv` | Three-task PDR metrics with factual QA replaced by LLM correctness |
| `results/rq2_semantic_correctness_llm_fact_metrics.csv` | RQ2 semantic metrics with updated correctness fields |
| `results/rq2_semantic_correctness_llm_fact_report.md` | Full RQ2 report using LLM factual correctness |

## Difference from Exact Match

| Comparison | Count |
|---|---:|
| Factual outputs judged | 300 |
| Exact-match label differs from LLM label | 111 |
| Exact-match 0 -> LLM 1 | 111 |
| Exact-match 1 -> LLM 0 | 0 |

Interpretation:

The strict exact-match factual evaluator was conservative. The LLM equivalence judge accepted many outputs that were not exact string matches but were factually equivalent or contained the correct answer in a longer response.

## Factual QA Correctness Drift After LLM Judge

With LLM equivalence correctness, factual QA becomes much less sensitive to perturbations:

| Metric | Value |
|---|---:|
| Factual case-level comparisons | 50 |
| Factual cases with repeated correctness change | 2 |
| Factual cases with harmful correctness drop | 2 |

By perturbation:

| Perturbation | Mean noise-corrected drift | Mean abs repeated pass-rate change | Mean repeated pass-rate drop |
|---|---:|---:|---:|
| context_injection | 0.003 | 0.000 | 0.000 |
| formatting | 0.000 | 0.000 | 0.000 |
| paraphrase | 0.042 | 0.100 | 0.100 |
| reordering | 0.000 | 0.000 | 0.000 |
| surface_noise | 0.001 | 0.033 | 0.033 |

Interpretation:

Under semantic equivalence judging, most factual QA perturbations do not change factual correctness. This suggests that many exact-match factual errors were formatting or verbosity artifacts rather than genuinely wrong answers.

## RQ2 Overall Result with LLM Factual Correctness

Primary relationship:

```text
noise_corrected_drift -> abs_repeated_pass_rate_change
```

| Version | Pearson | Spearman | 95% CI | permutation p |
|---|---:|---:|---:|---:|
| Exact-match factual correctness | 0.328 | 0.346 | [0.188, 0.503] | 0.001 |
| LLM-equivalence factual correctness | 0.536 | 0.349 | [0.187, 0.501] | 0.001 |

Interpretation:

The overall Spearman relationship remains almost unchanged. This means the main RQ2 conclusion is robust to replacing factual exact match with LLM equivalence correctness.

Pearson increases from `0.328` to `0.536`, which suggests the LLM factual labels make the pooled linear relationship cleaner. However, because Spearman is the preferred metric for the discrete correctness target, the main conclusion should emphasize stability rather than a large improvement.

## Harmful Correctness Drop

| Version | X | Y | Pearson | Spearman | 95% CI | permutation p |
|---|---|---|---:|---:|---:|---:|
| Exact-match factual correctness | noise_corrected_drift | harmful_correctness_drop | 0.247 | 0.306 | [0.145, 0.463] | 0.001 |
| LLM-equivalence factual correctness | noise_corrected_drift | harmful_correctness_drop | 0.462 | 0.356 | [0.186, 0.505] | 0.001 |

Interpretation:

The harmful-drop relationship becomes stronger under LLM factual correctness. This supports the idea that noise-corrected semantic drift is useful not only for detecting correctness movement, but also for identifying cases where perturbation harms correctness.

## Factual QA Task-Level Result

For `factual_qa` alone:

| Version | Pearson | Spearman | 95% CI | permutation p |
|---|---:|---:|---:|---:|
| Exact-match factual correctness | 0.006 | 0.224 | [-0.162, 0.535] | 0.167 |
| LLM-equivalence factual correctness | 0.944 | 0.162 | [-0.149, 0.531] | 0.083 |

Interpretation:

The high Pearson under LLM judging is driven by very few factual cases with correctness change. Only 2 of 50 factual case-level comparisons changed under repeated correctness. Therefore, this task-level Pearson should not be overinterpreted.

The Spearman relationship remains weak and statistically uncertain. For factual QA, the robust conclusion is still:

```text
semantic drift does not reliably predict factual correctness drift at this sample size
```

## Sample-Noise Correction Gain

Overall gain:

| Baseline | Pearson delta | Spearman delta |
|---|---:|---:|
| raw repeated cross-drift | +0.055 | -0.060 |
| single-pair drift | +0.104 | -0.034 |

Factual QA only:

| Baseline | Pearson delta | Spearman delta |
|---|---:|---:|
| raw repeated cross-drift | -0.021 | -0.189 |
| single-pair drift | +0.031 | -0.065 |

Interpretation:

With LLM factual correctness, sample-noise correction still improves Pearson association overall, but it does not improve Spearman rank association. For factual QA specifically, raw repeated cross-drift remains a stronger rank-based indicator than corrected drift.

## Updated RQ2 Interpretation

This sensitivity analysis strengthens three points:

1. The main RQ2 relationship is robust: semantic drift remains positively associated with correctness drift after replacing factual exact match with LLM equivalence correctness.
2. Exact-match factual correctness was too strict for some outputs; LLM judging converts many factual outputs from incorrect to correct.
3. Factual QA remains task-dependent: when equivalence judging is used, factual correctness changes are rare, so semantic drift is not a reliable factual correctness predictor by itself.

## Recommended Wording

Use this as the factual correctness sensitivity statement:

> Replacing strict exact-match factual QA correctness with an LLM equivalence judge changes many individual factual labels but does not materially change the overall RQ2 conclusion. Noise-corrected semantic drift remains a statistically reliable but moderate indicator of correctness drift. The factual QA task-level relationship remains weak under rank-based analysis because equivalence judging makes factual correctness changes rare.

