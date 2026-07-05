# RQ2 结果整理

## RQ2 问题定义

当前 RQ2 可以表述为：

```text
For objective tasks, does semantic output drift under prompt perturbation correspond to measurable correctness or performance instability?
```

中文表述：

```text
对于具有客观正确性标准的任务，prompt perturbation 导致的语义输出漂移是否对应可测量的 correctness / performance 不稳定性？
```

RQ2 不包含 open-ended writing，因为 open-ended writing 没有稳定的标准答案或 pass/fail correctness。

当前 RQ2 涉及的主要任务包括：

```text
factual_qa
math_reasoning
code_generation
long_factual_qa
```

其中 `long_factual_qa` 是后来为 RQ2 重新设计的长答案事实问答任务，比短答案 SQuAD 更适合观察 semantic drift 和 correctness change。

## 推荐主线

RQ2 结果建议按三层组织：

```text
1. Main correlational RQ2 result:
   semantic drift vs correctness change, using three objective tasks.

2. Stronger dose-response RQ2 result:
   context-injection perturbation with increasing severity.

3. Sensitivity / contrast result:
   surface noise is weaker and less monotonic, showing that not all perturbation families produce clean correctness effects.
```

论文或 proposal 中，建议把 `context_injection_dose_response_three_task_stress_5x3` 作为 RQ2 dose-response 的主证据。

## Result 1: Semantic Drift vs Correctness Change

对应文件：

```text
results/rq2_semantic_correctness_llm_fact_report.md
```

数据来源：

```text
results/generations_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv
results/rq2_semantic_correctness_llm_fact_combined_pdr_metrics.csv
```

规模：

```text
150 case-level comparisons
3 objective tasks:
  factual_qa
  math_reasoning
  code_generation
5 perturbation types
```

核心结果：

```text
noise_corrected_drift -> abs_repeated_pass_rate_change

Pearson  = 0.536
Spearman = 0.349
Spearman 95% CI = [0.187, 0.501]
Permutation p = 0.001
```

解释：

```text
Noise-corrected semantic drift is positively associated with correctness change.
The relationship is statistically reliable but moderate.
```

中文解释：

```text
语义漂移越大，correctness change 通常也越大。
但这个关系不是强确定性关系，而是中等强度的统计相关。
```

### Harmful Correctness Drop

同一报告中还分析了 harmful correctness drop：

```text
noise_corrected_drift -> harmful_correctness_drop

Pearson  = 0.462
Spearman = 0.356
Spearman 95% CI = [0.186, 0.505]
Permutation p = 0.001
```

对照 raw drift：

```text
raw_perturbation_drift -> harmful_correctness_drop

Pearson  = 0.412
Spearman = 0.280
```

解释：

```text
对于 harmful correctness drop，noise-corrected drift 比 raw drift 更有解释力。
这是 RQ2 中较清楚支持 sample-noise correction 的结果。
```

## Result 2: Task-Level RQ2 Pattern

对应文件：

```text
results/rq2_semantic_correctness_llm_fact_report.md
```

任务级 Spearman：

```text
code_generation:
Spearman = 0.515
95% CI = [0.180, 0.732]

factual_qa:
Spearman = 0.162
95% CI = [-0.149, 0.531]

math_reasoning:
Spearman = 0.232
95% CI = [-0.044, 0.507]
```

解释：

```text
RQ2 是 task-dependent 的。
Code generation 中 semantic drift 与 correctness change 的关系最清楚。
Factual QA 和 math reasoning 的关系较弱或不稳定。
```

更谨慎的表述：

```text
The relationship between semantic drift and correctness change is strongest for code generation and weaker for factual QA and math reasoning at the current sample size.
```

## Result 3: Perturbation-Level RQ2 Pattern

对应文件：

```text
results/rq2_semantic_correctness_llm_fact_report.md
```

扰动类型级 Spearman：

```text
surface_noise:
Spearman = 0.436
95% CI = [0.039, 0.762]

context_injection:
Spearman = 0.382
95% CI = [-0.020, 0.715]

formatting:
Spearman = 0.322
95% CI = [-0.110, 0.692]

paraphrase:
Spearman = 0.289
95% CI = [-0.145, 0.616]

reordering:
Spearman = 0.271
95% CI = [-0.195, 0.655]
```

解释：

```text
Surface noise and context injection show clearer drift-correctness links than paraphrase or reordering.
Paraphrase can change wording or representation without necessarily changing task correctness.
```

## Result 4: Context Injection Dose-Response, Three-Task Stress Run

这是当前最适合作为 RQ2 dose-response 主证据的结果。

对应文件：

```text
results/rq2_context_injection_dose_response_three_task_stress_5x3_report.md
```

设计：

```text
Perturbation family: context_injection
Strength levels: 0, 1, 2, 3, 4, 5
Tasks:
  long_factual_qa
  math_reasoning
  code_generation
Cases per task: 5
Samples per prompt version: 3
Case-level rows: 90
```

整体结果：

```text
strength_edits -> mean_cross_similarity:
Spearman = -0.3653

strength_edits -> abs_repeated_pass_rate_change:
Spearman = 0.1946

mean_cross_similarity -> abs_repeated_pass_rate_change, nonzero levels:
Spearman = -0.2992

noise_corrected_drift -> abs_repeated_pass_rate_change, nonzero levels:
Spearman = 0.1802
```

解释：

```text
Increasing context-injection strength generally lowers output similarity.
Lower output similarity is associated with larger correctness / performance movement.
The drift-to-correctness relationship is directionally positive but modest in the pooled three-task result.
```

任务层面：

```text
long_factual_qa:
mean_cross_similarity -> abs change:
Spearman = -0.8155

noise_corrected_drift -> abs change:
Spearman = 0.4688

math_reasoning:
mean_cross_similarity -> abs change:
Spearman = 0.4662

noise_corrected_drift -> abs change:
Spearman = -0.0339

code_generation:
mean_cross_similarity -> abs change:
Spearman = -0.4187

noise_corrected_drift -> abs change:
Spearman = 0.2848
```

解释：

```text
Context injection 的 RQ2 关系在 long_factual_qa 中最清楚。
Code generation 有较弱但方向一致的关系。
Math reasoning 在当前样本量下不稳定。
```

推荐作为主结论：

```text
Across context-injection perturbations, observed semantic drift is more informative than nominal perturbation level. The clearest relationship appears in long factual QA, a weaker but directionally consistent relationship appears in code generation, and math reasoning remains unstable at the current sample size.
```

## Result 5: Context Injection LongFactQA Stress Only

对应文件：

```text
results/rq2_context_injection_dose_response_longfact_stress_5x3_report.md
```

设计：

```text
Task: long_factual_qa only
Long FACT QA set: stress
Cases: 5
Strength levels: 0, 1, 2, 3, 4, 5
Samples per prompt version: 3
Case-level rows: 30
```

关键结果：

```text
mean_cross_similarity -> abs_repeated_pass_rate_change, nonzero levels:
Spearman = -0.7443

noise_corrected_drift -> abs_repeated_pass_rate_change, nonzero levels:
Spearman = 0.5858
```

解释：

```text
在 long factual QA stress setting 中，context injection 的 RQ2 关系很清楚：
输出相似度越低，correctness change 越大；
noise-corrected drift 越大，correctness change 越大。
```

这是 RQ2 最强的单任务证据。

## Result 6: Surface Noise LongFactQA Stress

对应文件：

```text
results/rq2_surface_noise_dose_response_longfact_stress_5x3_report.md
```

设计：

```text
Perturbation family: surface_noise
Strength levels: 0, 1, 2, 4, 8 corrupted instruction words
Task: long_factual_qa
Long FACT QA set: stress
Cases: 5
Samples per prompt version: 3
Case-level rows: 25
```

关键结果：

```text
strength_edits -> mean_cross_similarity:
Spearman = -0.4961

strength_edits -> abs_repeated_pass_rate_change:
Spearman = 0.2176

mean_cross_similarity -> abs_repeated_pass_rate_change, nonzero levels:
Spearman = -0.6303

noise_corrected_drift -> abs_repeated_pass_rate_change, nonzero levels:
Spearman = -0.2896
```

解释：

```text
Surface noise 能降低 output similarity，并且 lower similarity 与 larger correctness change 有关系。
但 noise-corrected drift 本身没有呈现预期的正向关系。
因此 surface noise 不是最干净的 RQ2 dose-response evidence。
```

推荐定位：

```text
Surface noise should be used as a contrast condition: it changes output similarity, but it does not produce a clean monotonic correctness dose-response.
```

## 推荐论文写法

### 英文版本

```text
RQ2 examines whether semantic output drift under prompt perturbation is associated with correctness instability. Across the three objective tasks in the initial RQ2 analysis, noise-corrected semantic drift is positively associated with absolute repeated pass-rate change (Spearman = 0.349, 95% CI [0.187, 0.501], p = 0.001). The relationship is reliable but moderate, indicating that semantic drift is an informative but imperfect indicator of correctness change.

The dose-response experiments provide stronger evidence when perturbation severity is controlled within a perturbation family. In the context-injection stress setting, lower output similarity is associated with larger correctness change. This relationship is strongest for long factual QA, where nonzero-level similarity-to-correctness Spearman is -0.744 and corrected-drift-to-correctness Spearman is 0.586. In the three-task context-injection run, the pooled relationship remains directionally consistent but weaker, with the clearest task-level pattern in long factual QA and a weaker but directionally consistent pattern in code generation. Math reasoning remains unstable at the current sample size.

Overall, RQ2 supports the claim that semantic drift can indicate correctness instability, but the strength of the relationship depends on task type and perturbation family. Context injection provides the clearest dose-response evidence, while surface noise produces weaker and less monotonic correctness effects.
```

### 中文版本

```text
RQ2 考察 prompt perturbation 导致的语义输出漂移是否对应 correctness 不稳定性。在三类客观任务的初始 RQ2 分析中，noise-corrected semantic drift 与 absolute repeated pass-rate change 呈可靠但中等强度的正相关（Spearman = 0.349，95% CI [0.187, 0.501]，p = 0.001）。这说明 semantic drift 可以作为 correctness change 的一个有效但不完美的指标。

进一步的 dose-response 实验表明，当在同一 perturbation family 内控制扰动强度时，RQ2 关系更加清楚。尤其是在 context-injection stress setting 中，输出相似度越低，correctness change 越大。该关系在 long factual QA 中最强：nonzero levels 下 similarity-to-correctness Spearman = -0.744，corrected-drift-to-correctness Spearman = 0.586。在三任务 context-injection 实验中，整体关系方向一致但较弱，其中 long factual QA 最清楚，code generation 较弱但方向一致，math reasoning 在当前样本量下仍不稳定。

总体而言，RQ2 支持 semantic drift 能够提示 correctness instability 的主张，但该关系受到任务类型和扰动类型影响。Context injection 是当前最清楚的 dose-response 证据，而 surface noise 的 correctness effect 较弱且不完全单调。
```

## 需要避免的过度表述

不要写：

```text
Semantic drift always predicts correctness change.
```

更准确：

```text
Semantic drift is a statistically reliable but moderate indicator of correctness change.
```

不要写：

```text
Sample-noise correction always improves RQ2 prediction.
```

更准确：

```text
Sample-noise correction improves the interpretation of perturbation-specific drift and is useful for harmful-drop analysis, but it does not always improve rank correlation relative to raw repeated cross-drift.
```

不要写：

```text
Perturbation strength itself is always monotonic with correctness degradation.
```

更准确：

```text
Nominal perturbation strength is less reliable than observed semantic drift. Correctness change is not strictly monotonic by strength at the current sample size.
```

## 建议最终使用顺序

论文中建议这样呈现 RQ2：

```text
1. Define RQ2:
   Does semantic drift correspond to correctness instability?

2. Report initial three-task correlation:
   Spearman = 0.349 for noise-corrected drift vs absolute correctness change.

3. Report harmful-drop result:
   noise-corrected drift is also associated with harmful correctness drops.

4. Introduce dose-response as stronger test:
   perturbation strength is varied within a single perturbation family.

5. Use context injection as main dose-response evidence:
   long factual QA strongest, code generation weaker but consistent, math unstable.

6. Use surface noise as contrast:
   similarity changes, but correctness effects are weaker and less monotonic.

7. State limitations:
   small sample size, task dependence, discrete correctness labels, non-causal correlations.
```

