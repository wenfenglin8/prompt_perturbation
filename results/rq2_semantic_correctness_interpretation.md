# RQ2 实验结果解释：Semantic Drift 是否指示 Correctness Drift

## 1. RQ2 要回答什么

RQ2 的核心问题是：

> 对有客观正确性标准的任务，semantic / similarity drift 是否能够指示 correctness drift？

这里的 `similarity drift` 指 original prompt 和 perturbed prompt 产生的输出在 embedding 空间中的距离变化。

这里的 `correctness drift` 指 original prompt 和 perturbed prompt 的正确率变化。

本次 RQ2 使用三类有客观 correctness label 的任务：

| Task | Dataset | Correctness |
|---|---|---|
| factual_qa | SQuAD V2 | short-answer exact match |
| math_reasoning | MATH | final-answer match |
| code_generation | HumanEval | unit-test pass/fail |

本次分析规模：

| Item | Value |
|---|---:|
| case-level comparisons | 150 |
| tasks | 3 |
| perturbation types | 5 |
| samples per prompt version | 3 |
| generated outputs used | 900 |

## 2. 主要结果：similarity drift 和 correctness drift 有正相关

主分析使用：

```text
X = noise_corrected_drift
Y = abs_repeated_pass_rate_change
```

也就是说，我们检验的是：

> 做了 sample-noise correction 后的 similarity drift，是否能指示 repeated-sampling correctness 的变化幅度？

总体结果：

| X | Y | Pearson | Spearman | 95% CI | permutation p |
|---|---|---:|---:|---:|---:|
| noise_corrected_drift | abs_repeated_pass_rate_change | 0.328 | 0.346 | [0.188, 0.503] | 0.001 |

解释：

- `Spearman = 0.346` 表示存在中等偏弱的正向排序关系。
- 也就是说，semantic drift 较大的 case，通常 correctness drift 也更大。
- 95% CI 完全大于 0，说明这个正相关比较稳定。
- permutation p = 0.001，说明这个关系不太可能是随机排列造成的。

可以写成论文式结论：

> Across objective tasks, noise-corrected semantic drift is positively associated with correctness drift. The relationship is statistically reliable but moderate in magnitude.

中文解释：

> 在三个客观任务上，做了 sample-noise correction 的 semantic drift 能够在一定程度上指示 correctness drift；但它不是强预测器，只能说明二者有稳定的中等偏弱关联。

## 3. Correction 后是否更好指示 correctness drift

这是 RQ1 到 RQ2 的关键衔接。

RQ1 关心：

```text
sample noise correction 是否能更干净地隔离 perturbation-specific semantic drift
```

RQ2 进一步关心：

```text
这个 corrected semantic drift 是否更能指示 correctness drift
```

我们比较了三种 similarity drift：

| Drift measure | Meaning |
|---|---|
| noise_corrected_drift | 扣除 sample noise 后的 perturbation-specific drift |
| raw_perturbation_drift | 未扣除 sample noise 的 repeated cross-version drift |
| uncorrected_single_drift | 单个 original output 和单个 perturbed output 的距离 |

总体 comparison：

| Comparison | Pearson delta | Spearman delta | Interpretation |
|---|---:|---:|---|
| corrected vs raw cross-drift | +0.030 | -0.029 | Pearson 略好，但 Spearman 略差 |
| corrected vs single-pair baseline | +0.061 | +0.015 | corrected 略好 |

paired permutation test：

| Baseline | Pearson delta p | Spearman delta p |
|---|---:|---:|
| raw cross-drift | 0.284 | 0.617 |
| single-pair baseline | 0.171 | 0.462 |

解释：

- correction 后的 drift 在 Pearson 上比两个 baseline 都高。
- 但是提升幅度不大。
- Spearman 上，corrected drift 只略好于 single-pair baseline，但低于 raw cross-drift。
- paired permutation p-value 不显著，说明“correction 一定提升预测力”这个结论目前证据不足。

更稳妥的结论是：

> Sample-noise correction improves the methodological cleanliness of the semantic drift measure, and it shows some Pearson-level gain over uncorrected baselines. However, this first RQ2 run does not show a stable overall rank-correlation improvement over raw repeated cross-drift.

中文解释：

> sample-noise correction 让 similarity drift 的定义更干净，更接近 perturbation 本身造成的变化；但从当前数据看，它并没有在所有统计口径上稳定提升对 correctness drift 的指示能力。

## 4. Correctness change 和 correctness degradation 要分开看

主分析的 `abs_repeated_pass_rate_change` 回答的是：

```text
correctness 是否发生变化
```

但这不区分正确率是下降还是上升。

因此我们又分析了 harmful correctness drop：

```text
harmful_correctness_drop = 1 if clean_mean_correctness > perturbed_mean_correctness else 0
```

结果：

| X | Y | Pearson | Spearman | 95% CI | permutation p |
|---|---|---:|---:|---:|---:|
| noise_corrected_drift | harmful_correctness_drop | 0.247 | 0.306 | [0.145, 0.463] | 0.001 |
| raw_perturbation_drift | harmful_correctness_drop | 0.200 | 0.213 | [0.074, 0.340] | 0.009 |

解释：

- corrected semantic drift 对 harmful correctness drop 也有正相关。
- corrected drift 的 Spearman = 0.306，高于 raw drift 的 0.213。
- 这说明 correction 在“是否导致正确性下降”这个问题上更有用。

可以写成：

> Noise-corrected semantic drift is also associated with harmful correctness drops, and here it outperforms raw cross-drift.

中文解释：

> 如果研究重点是 correctness 是否受损，而不只是 correctness 有没有变化，那么 sample-noise corrected drift 更有价值。

## 5. 任务差异：RQ2 是 task-dependent 的

按任务看，主分析结果是：

| Task | Pearson | Spearman | 95% CI | Interpretation |
|---|---:|---:|---:|---|
| code_generation | 0.747 | 0.515 | [0.180, 0.732] | 最强，semantic drift 明显指示 correctness drift |
| factual_qa | 0.006 | 0.224 | [-0.162, 0.535] | 较弱，不稳定 |
| math_reasoning | -0.060 | 0.232 | [-0.044, 0.507] | 较弱，不稳定 |

解释：

### code_generation

code generation 上关系最强。

原因可能是：

- 代码输出的语义/结构变化更容易影响 unit tests。
- 小的代码结构变化可能直接导致 pass/fail 改变。
- embedding drift 在代码任务上更容易捕捉到功能层面的变化。

因此 code_generation 是当前 RQ2 最支持的任务。

### factual_qa

factual QA 上 corrected drift 的预测力较弱。

可能原因：

- short answer correctness 很离散。
- 输出表述可能变化，但答案仍然相同。
- 也可能答案错误但 embedding 距离不大。
- raw drift 在 factual QA 上反而更高，说明 sample-noise correction 可能扣掉了一些与答案变化相关的输出差异。

### math_reasoning

math reasoning 上主相关也较弱，但 correction gain 很明显。

特别是 corrected vs raw：

| Task | Pearson delta | Spearman delta |
|---|---:|---:|
| math_reasoning | +0.280 | +0.470 |

解释：

- math 输出中有较多 reasoning trace 变化。
- raw drift 可能混入了 sampling noise 或推理表达差异。
- correction 后更能排除这些噪声，因此相对 raw drift 更接近 correctness drift。

## 6. Perturbation 差异

按 perturbation 看，主结果是：

| Perturbation | Spearman | Interpretation |
|---|---:|---|
| surface_noise | 0.608 | 最强 |
| context_injection | 0.467 | 较强 |
| reordering | 0.271 | 中弱 |
| formatting | 0.221 | 中弱 |
| paraphrase | 0.112 | 最弱 |

解释：

- `surface_noise` 和 `context_injection` 更容易造成 correctness drift。
- `paraphrase` 的 semantic drift 不太能稳定对应 correctness drift，说明 paraphrase 可能更多改变表达，而不是改变答案正确性。
- `formatting` 和 `reordering` 的影响更 task-dependent。

## 7. Case inspection 说明了为什么相关性不是很强

case inspection 里有三类关键样本：

### 7.1 高 similarity drift + 高 correctness drift

例如：

| Case | Task | Perturbation | clean correctness | perturbed correctness |
|---|---|---|---:|---:|
| promptrobust_pdr_formatting_humaneval_03 | code_generation | formatting | 1.0 | 0.0 |
| promptrobust_pdr_paraphrase_humaneval_04 | code_generation | paraphrase | 1.0 | 0.0 |
| promptrobust_pdr_formatting_humaneval_09 | code_generation | formatting | 1.0 | 0.0 |

这些样本支持 RQ2 的主假设：

> similarity drift 大时，correctness 也发生明显变化。

### 7.2 高 similarity drift + correctness 不变

例如：

| Case | Task | Perturbation | clean correctness | perturbed correctness |
|---|---|---|---:|---:|
| promptrobust_pdr_paraphrase_squad_08 | factual_qa | paraphrase | 0.0 | 0.0 |
| promptrobust_pdr_formatting_math_03 | math_reasoning | formatting | 0.0 | 0.0 |
| promptrobust_pdr_surface_noise_humaneval_01 | code_generation | surface_noise | 0.0 | 0.0 |

这些样本说明：

> semantic drift 不一定导致 correctness drift。

尤其当 clean 和 perturbed 都错时，输出可以变化很大，但 correctness 仍然都是 0。

### 7.3 低 similarity drift + 高 correctness drift

例如：

| Case | Task | Perturbation | clean correctness | perturbed correctness |
|---|---|---|---:|---:|
| promptrobust_pdr_surface_noise_math_08 | math_reasoning | surface_noise | 0.0 | 1.0 |
| promptrobust_pdr_surface_noise_math_06 | math_reasoning | surface_noise | 1.0 | 0.0 |
| promptrobust_pdr_surface_noise_humaneval_09 | code_generation | surface_noise | 1.0 | 0.0 |

这些样本说明：

> correctness 可能被很小的 output difference 改变，尤其是 math final answer 或 code pass/fail。

因此 similarity drift 不能完全替代 correctness evaluation。

## 8. 当前 RQ2 的主结论

当前数据支持以下结论：

1. noise-corrected semantic drift 与 correctness drift 存在稳定正相关。
2. 这个关系整体是 moderate，而不是 strong。
3. 关系明显 task-dependent，code_generation 最强。
4. correction 后的 drift 在 harmful correctness drop 上比 raw drift 更有解释力。
5. correction 是否整体提升 correctness drift 指示能力，目前证据混合：
   - Pearson 上有提升；
   - Spearman 上不稳定；
   - paired permutation test 还不支持“显著提升”的强结论。
6. semantic drift 不能替代 correctness evaluation，因为存在高 drift 但 correctness 不变、低 drift 但 correctness 改变的 case。

## 9. 建议的论文表述

建议写成：

> RQ2 shows that semantic drift is a statistically reliable but moderate indicator of correctness drift on objective tasks. The association is strongest for code generation and weaker for factual QA and math reasoning. Sample-noise correction improves the methodological specificity of the drift measure and is more informative for harmful correctness drops, but it does not uniformly improve rank-based prediction over raw repeated cross-drift.

中文对应：

> RQ2 结果表明，在客观任务上，semantic drift 能够稳定但中等程度地指示 correctness drift。该关系具有明显任务差异，在 code generation 上最强，在 factual QA 和 math reasoning 上较弱。sample-noise correction 提高了 drift 指标的方法学针对性，并且对 harmful correctness drop 更有解释力，但它并没有在所有任务和所有统计口径上稳定优于 raw drift。

## 10. 还需要补什么

RQ2 当前已经可以支撑初步结论。

如果要进一步增强论文说服力，下一步建议：

1. 对 `rq2_semantic_correctness_case_inspection.csv` 做人工样本分析。
2. 抽取每类 2-3 个 case，展示 original output、perturbed output、correctness 变化。
3. 重点解释：
   - 为什么 code_generation 中 drift 更能指示 correctness；
   - 为什么 factual_qa 中 drift 和 correctness 经常脱钩；
   - 为什么 math 中小 drift 也可能造成 final answer correctness 改变。

