# RQ1 修正后 PDR 结果分析

## 分析范围

本分析使用修正 evaluator 后的 RQ1 PDR 结果：

- `results/rq1_recomputed/rq1_pdr_50x5_recomputed_v2_metrics.csv`
- `results/rq1_recomputed/rq1_pdr_50x5_recomputed_v2_report.md`

由于 open-ended writing 没有统计 PDR / correctness，本分析排除 open-ended writing。当前只包含三个 objective task：

- factual question answering
- mathematical reasoning
- code generation

对应图文件：

- `rq1_pdr_recomputed_v2_task_dependent_ranking.png`
- `rq1_pdr_recomputed_v2_task_dependent_ranking.pdf`
- `rq1_pdr_recomputed_v2_corrected_pdr_by_task_bars.png`
- `rq1_pdr_recomputed_v2_corrected_pdr_by_task_bars.pdf`

## RQ1 回答

RQ1 关注：在做 noise-baseline correction 后，五种 perturbation 的影响排名是否在不同任务之间一致，还是这个排名本身依赖任务类型。

基于目前修正后的 PDR 数据，结论是：

**perturbation ranking 是 task-dependent，不是跨任务一致的 universal ranking。**

paraphrasing 是三个 objective tasks 中最稳定有害的 perturbation，但五种 perturbation 的完整排序会随任务改变。

## 总体结果

修复 math 和 code evaluator 后：

| 指标 | 数值 |
|---|---:|
| Clean repeated performance | 0.9426 |
| Perturbed repeated performance | 0.9395 |
| Clean baseline loss | 0.0574 |
| Perturbed loss | 0.0605 |
| Corrected PDR | 0.0031 |

因此，总体 perturbation-induced loss 很小：

```text
corrected PDR = 0.0031
```

这表示 0.31 个百分点的绝对性能下降。

## 按任务分解

| Task | Clean performance | Perturbed performance | Clean baseline loss | Perturbation-induced loss |
|---|---:|---:|---:|---:|
| Factual QA | 0.9789 | 0.9770 | 0.0211 | 0.0020 |
| Math reasoning | 0.8776 | 0.8736 | 0.1224 | 0.0040 |
| Code generation | 0.9712 | 0.9680 | 0.0288 | 0.0032 |

这里最重要的是区分：

```text
clean baseline loss = 模型/任务本身在 clean prompt 下已有的错误
perturbation-induced loss = perturbation 相对 clean prompt 额外造成的错误
```

目前大部分 loss 来自 clean baseline loss，而不是 perturbation-induced loss。

## 按任务的 perturbation 排名

Corrected PDR 为正，表示 perturbation 后性能下降，也就是出现 perturbation-induced loss。Corrected PDR 为负，表示 perturbed prompt 在 repeated sampling 中略好于 clean prompt。

### Factual QA

| Perturbation | Corrected PDR |
|---|---:|
| Paraphrase | 0.0072 |
| Formatting | 0.0040 |
| Context injection | 0.0013 |
| Reordering | -0.0013 |
| Surface noise | -0.0013 |

排名：

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

排名：

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

排名：

```text
paraphrase > context injection > formatting ≈ surface noise > reordering
```

## 解释

修正后的 PDR 结果说明：perturbation effect 的绝对值整体较小，但五种 perturbation 的排序并不稳定，而是明显依赖任务。

最明显的 task-dependent 证据是 reordering：

- 在 math reasoning 中，reordering 是最有害的 perturbation。
- 在 factual QA 中，reordering 接近中性。
- 在 code generation 中，reordering 在本次结果里略微提高表现。

paraphrasing 是最稳定有害的 perturbation：

- factual QA 中最高。
- math reasoning 中第二高。
- code generation 中最高。

但除了 paraphrasing 外，其他 perturbation 的顺序明显随任务改变。因此，RQ1 的答案应该是 task-dependent ranking，而不是 universal ranking。

## 图注建议

Figure X. Repaired PDR analysis for RQ1, excluding open-ended writing. Panel A reports corrected PDR by perturbation type and objective task, in percentage points; cell labels show the corrected PDR value and the within-task harmfulness rank. Panel B decomposes total perturbed loss into clean-prompt baseline loss and the additional perturbation-induced loss. After repairing the math and code evaluators, clean repeated performance is 0.9426 and perturbed repeated performance is 0.9395, yielding a small aggregate corrected PDR of 0.0031. The perturbation ranking is task-dependent: paraphrasing is consistently harmful, but reordering is most harmful for math reasoning while near-neutral or beneficial for the other tasks.

## 论文正文建议写法

修正 math 和 code evaluator 后，基于 PDR 的 correctness 分析显示，perturbation effect 的整体幅度较小，并且具有明显的 task dependence。排除 open-ended writing 后，paraphrasing 是唯一在 factual QA、math reasoning 和 code generation 中都稳定表现为有害的 perturbation。然而，五种 perturbation 的完整排序并不稳定：reordering 在 math reasoning 中最有害，但在 factual QA 和 code generation 中并非如此；formatting、context injection 和 surface noise 则根据任务不同表现为接近中性或略微有益。因此，修正后的 PDR 证据支持 task-dependent perturbation ranking，而不是 universal perturbation ranking。

## 注意事项

PDR 衡量的是 correctness / performance loss，不是 semantic similarity 本身。因此，这个结果应该作为 RQ1 的 correctness-side evidence，而不是直接替代 semantic similarity / noise-corrected drift 分析。

Corrected PDR 为负时，不应该写成“负 loss”。更准确的解释是：perturbed prompt 在 repeated sampling 中略好于 clean prompt。对 math 的人工检查显示，这类提升很多时候来自模型推理路径的随机波动，而不是 perturbation 系统性有益。
