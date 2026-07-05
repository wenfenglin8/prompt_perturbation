# RQ1 Recomputed V2 Perturbation Rankings / RQ1 修正后扰动排名

Data source:

- `results/rq1_recomputed/rq1_pdr_50x5_recomputed_v2_metrics.csv`
- `results/rq1_figures/rq1_pdr_recomputed_v2_grouped_for_paper.csv`

Scope:

- Included: factual QA, math reasoning, code generation
- Excluded: open-ended writing, because PDR/correctness was not computed for it

Metric:

```text
corrected_PDR = clean_repeated_performance - perturbed_repeated_performance
```

Positive corrected PDR means perturbation-induced performance loss. Negative corrected PDR means the perturbed prompt performed slightly better than the clean prompt in repeated sampling.

## English Summary

Based on the repaired PDR results, the perturbation ranking is task-dependent. Paraphrasing is the most consistently harmful perturbation across the three objective tasks, but the full ranking changes by task.

### Ranking By Task

| Task | Ranking by harmful corrected PDR |
|---|---|
| Factual QA | paraphrase > formatting > context injection > reordering ≈ surface noise |
| Math reasoning | reordering > paraphrase > surface noise > formatting > context injection |
| Code generation | paraphrase > context injection > formatting ≈ surface noise > reordering |

### Values By Task

#### Factual QA

| Rank | Perturbation | Corrected PDR |
|---:|---|---:|
| 1 | paraphrase | 0.0072 |
| 2 | formatting | 0.0040 |
| 3 | context injection | 0.0013 |
| 4 | reordering | -0.0013 |
| 5 | surface noise | -0.0013 |

#### Math Reasoning

| Rank | Perturbation | Corrected PDR |
|---:|---|---:|
| 1 | reordering | 0.0240 |
| 2 | paraphrase | 0.0160 |
| 3 | surface noise | 0.0000 |
| 4 | formatting | -0.0080 |
| 5 | context injection | -0.0120 |

#### Code Generation

| Rank | Perturbation | Corrected PDR |
|---:|---|---:|
| 1 | paraphrase | 0.0200 |
| 2 | context injection | 0.0040 |
| 3 | formatting | 0.0000 |
| 4 | surface noise | 0.0000 |
| 5 | reordering | -0.0080 |

## 中文总结

基于修正后的 PDR 结果，五种 perturbation 的影响排名是 task-dependent，而不是跨任务一致的 universal ranking。Paraphrasing 是三个 objective tasks 中最稳定有害的扰动，但完整排名会随任务改变。

### 按任务的扰动排名

| 任务 | 按 harmful corrected PDR 排名 |
|---|---|
| Factual QA | paraphrase > formatting > context injection > reordering ≈ surface noise |
| Math reasoning | reordering > paraphrase > surface noise > formatting > context injection |
| Code generation | paraphrase > context injection > formatting ≈ surface noise > reordering |

### 按任务的具体数值

#### Factual QA

| 排名 | Perturbation | Corrected PDR |
|---:|---|---:|
| 1 | paraphrase | 0.0072 |
| 2 | formatting | 0.0040 |
| 3 | context injection | 0.0013 |
| 4 | reordering | -0.0013 |
| 5 | surface noise | -0.0013 |

#### Math Reasoning

| 排名 | Perturbation | Corrected PDR |
|---:|---|---:|
| 1 | reordering | 0.0240 |
| 2 | paraphrase | 0.0160 |
| 3 | surface noise | 0.0000 |
| 4 | formatting | -0.0080 |
| 5 | context injection | -0.0120 |

#### Code Generation

| 排名 | Perturbation | Corrected PDR |
|---:|---|---:|
| 1 | paraphrase | 0.0200 |
| 2 | context injection | 0.0040 |
| 3 | formatting | 0.0000 |
| 4 | surface noise | 0.0000 |
| 5 | reordering | -0.0080 |

## RQ1 Answer / RQ1 回答

English:

The repaired PDR evidence supports a task-dependent perturbation ranking. The ranking of perturbation types is not consistent across factual QA, mathematical reasoning, and code generation. Paraphrasing is consistently harmful, but reordering, formatting, context injection, and surface noise change their relative positions across tasks.

中文：

修正后的 PDR 证据支持 task-dependent perturbation ranking。五种扰动类型在 factual QA、math reasoning 和 code generation 中的排名并不一致。Paraphrasing 稳定表现为有害，但 reordering、formatting、context injection 和 surface noise 的相对位置会随任务改变。
