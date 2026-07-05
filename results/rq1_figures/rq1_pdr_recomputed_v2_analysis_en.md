# RQ1 PDR Analysis After Evaluator Repair

## Scope

This analysis uses the repaired RQ1 PDR results from:

- `results/rq1_recomputed/rq1_pdr_50x5_recomputed_v2_metrics.csv`
- `results/rq1_recomputed/rq1_pdr_50x5_recomputed_v2_report.md`

The analysis excludes open-ended writing because PDR/correctness was not computed for that task. The included tasks are:

- factual question answering
- mathematical reasoning
- code generation

The figures are:

- `rq1_pdr_recomputed_v2_task_dependent_ranking.png`
- `rq1_pdr_recomputed_v2_task_dependent_ranking.pdf`
- `rq1_pdr_recomputed_v2_corrected_pdr_by_task_bars.png`
- `rq1_pdr_recomputed_v2_corrected_pdr_by_task_bars.pdf`

## RQ1

RQ1 asks whether the ranking of perturbation types is consistent across task types after applying a noise-baseline correction, or whether the ranking itself is task-dependent.

Using the repaired PDR results as correctness-side evidence, the answer is:

**The perturbation ranking is task-dependent.**

Paraphrasing is the most consistently harmful perturbation across the three objective tasks, but the full ranking of perturbation types changes by task.

## Key Aggregate Result

After repairing math and code evaluators:

| Metric | Value |
|---|---:|
| Clean repeated performance | 0.9426 |
| Perturbed repeated performance | 0.9395 |
| Clean baseline loss | 0.0574 |
| Perturbed loss | 0.0605 |
| Corrected PDR | 0.0031 |

Thus, the aggregate perturbation-induced loss is small:

```text
corrected PDR = 0.0031
```

This corresponds to a 0.31 percentage-point absolute drop.

## Task-Level Decomposition

| Task | Clean performance | Perturbed performance | Clean baseline loss | Perturbation-induced loss |
|---|---:|---:|---:|---:|
| Factual QA | 0.9789 | 0.9770 | 0.0211 | 0.0020 |
| Math reasoning | 0.8776 | 0.8736 | 0.1224 | 0.0040 |
| Code generation | 0.9712 | 0.9680 | 0.0288 | 0.0032 |

Most observed loss is clean-prompt baseline loss rather than perturbation-induced loss.

## Perturbation Ranking By Task

Corrected PDR values are in absolute performance units. Positive values indicate performance loss after perturbation; negative values indicate that the perturbed prompt performed slightly better than the clean prompt in repeated sampling.

### Factual QA

| Perturbation | Corrected PDR |
|---|---:|
| Paraphrase | 0.0072 |
| Formatting | 0.0040 |
| Context injection | 0.0013 |
| Reordering | -0.0013 |
| Surface noise | -0.0013 |

Ranking:

```text
paraphrase > formatting > context injection > reordering ≈ surface noise
```

### Math Reasoning

| Perturbation | Corrected PDR |
|---|---:|
| Reordering | 0.0240 |
| Paraphrase | 0.0160 |
| Surface noise | 0.0000 |
| Formatting | -0.0080 |
| Context injection | -0.0120 |

Ranking:

```text
reordering > paraphrase > surface noise > formatting > context injection
```

### Code Generation

| Perturbation | Corrected PDR |
|---|---:|
| Paraphrase | 0.0200 |
| Context injection | 0.0040 |
| Formatting | 0.0000 |
| Surface noise | 0.0000 |
| Reordering | -0.0080 |

Ranking:

```text
paraphrase > context injection > formatting ≈ surface noise > reordering
```

## Interpretation

The repaired PDR results show that perturbation effects are small in magnitude but not ranked consistently across tasks.

The clearest evidence for task dependence is reordering:

- It is the most harmful perturbation for math reasoning.
- It is near-neutral for factual QA.
- It is slightly beneficial for code generation in this run.

Paraphrasing is the most stable harmful perturbation:

- It is highest for factual QA.
- It is second highest for math reasoning.
- It is highest for code generation.

However, because the remaining perturbation types change order across tasks, the overall ranking is task-dependent rather than universal.

## Figure Caption

Figure X. Repaired PDR analysis for RQ1, excluding open-ended writing. Panel A reports corrected PDR by perturbation type and objective task, in percentage points; cell labels show the corrected PDR value and the within-task harmfulness rank. Panel B decomposes total perturbed loss into clean-prompt baseline loss and the additional perturbation-induced loss. After repairing the math and code evaluators, clean repeated performance is 0.9426 and perturbed repeated performance is 0.9395, yielding a small aggregate corrected PDR of 0.0031. The perturbation ranking is task-dependent: paraphrasing is consistently harmful, but reordering is most harmful for math reasoning while near-neutral or beneficial for the other tasks.

## Recommended Paper Wording

After repairing the math and code evaluators, the PDR-based correctness analysis shows that perturbation effects are small in magnitude and task-dependent. Excluding open-ended writing, paraphrasing is the only perturbation that remains consistently harmful across factual QA, mathematical reasoning, and code generation. However, the complete ranking of perturbation types is not stable: reordering is most harmful for math reasoning but not for factual QA or code generation, while formatting, context injection, and surface noise are near-neutral or slightly beneficial depending on the task. Thus, the repaired PDR evidence supports a task-dependent rather than universal perturbation ranking.

## Caveats

PDR measures correctness/performance loss, not semantic similarity directly. Therefore, these results should be presented as correctness-side evidence for RQ1 and should be interpreted alongside the semantic-similarity/noise-corrected drift analysis.

Negative corrected PDR values should not be interpreted as negative loss. They indicate that perturbed prompts performed slightly better than clean prompts in repeated sampling. Manual inspection of math examples suggests that such improvements often reflect stochastic reasoning variability rather than a systematic beneficial effect of perturbation.
