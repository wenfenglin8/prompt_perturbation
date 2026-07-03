# RQ2 Implementation Plan

## RQ2 Definition

Current RQ2 from `research.md`:

```text
For tasks with objective correctness, does semantic drift predict correctness changes?
```

In practical terms, RQ2 asks:

```text
When a prompt perturbation changes the model's output in embedding / semantic space,
does that change also correspond to a measurable change in task correctness?
```

This is different from RQ1:

```text
RQ1: Which perturbation types produce noise-corrected semantic drift, and are rankings task-dependent?
RQ2: Does that semantic drift actually predict correctness degradation or correctness change?
```

## Scope

RQ2 should only use tasks with objective correctness labels:

| Task | Dataset | Correctness criterion | Use for RQ2? |
|---|---|---|---:|
| factual_qa | SQuAD V2 | exact short-answer match | Yes |
| math_reasoning | MATH | final-answer exact match | Yes |
| code_generation | HumanEval | pass@1-style unit-test pass/fail | Yes |
| open_ended_writing | Alpaca | no single objective correctness label | No, keep as future qualitative / auxiliary analysis |

Therefore, the first RQ2 implementation should focus on:

```text
factual_qa
math_reasoning
code_generation
```

## Best Existing Data to Reuse

The strongest current input for RQ2 is the three-task PDR 10x3 run:

```text
results/generations_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv
results/pdr_metrics_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv
results/pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md
```

This run already contains:

```text
3 objective tasks
10 cases/task
5 perturbations
3 clean generations per case
3 perturbed generations per case
correctness for every generated output
PDR metrics per task-perturbation-case
```

Scale:

```text
3 tasks x 10 cases/task x 5 perturbations = 150 case-level comparisons
150 comparisons x 2 prompt versions x 3 samples = 900 generated outputs
```

## Why Not Use the RQ1 Similarity Run Directly?

The latest RQ1 similarity run is:

```text
results/similarity_report_four_task_similarity_sweep_pdr_aligned_5x3.md
```

It is useful for RQ1, but it is not ideal as the primary RQ2 input because:

1. It uses only `5 cases/task`.
2. It includes Alpaca, which has no objective correctness label.
3. Its generations are not the same generations as the PDR 10x3 run.

For RQ2, the best design is to compute semantic drift and correctness change
from the **same generated outputs**. Therefore, RQ2 should start from the
PDR 10x3 generation file and add semantic-drift calculations to it.

## Recommended RQ2 Method

### Step 1. Load Existing PDR Generations

Input:

```text
results/generations_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv
```

Required columns:

```text
case_id
task
dataset
perturbation
version
sample_idx
output
correct
```

Each `case_id` should have:

```text
3 original outputs
3 perturbed outputs
```

### Step 2. Compute Semantic Drift on the Same Outputs

For each `case_id`, embed all six outputs:

```text
original outputs:  o1, o2, o3
perturbed outputs: p1, p2, p3
```

Then compute:

```text
original_noise = average pairwise distance among o1, o2, o3
perturbed_noise = average pairwise distance among p1, p2, p3
noise_baseline = (original_noise + perturbed_noise) / 2
raw_perturbation_drift = average cross-distance between original outputs and perturbed outputs
noise_corrected_drift = max(0, raw_perturbation_drift - noise_baseline)
uncorrected_single_drift = distance(o1, p1)
```

Use the same embedding setup as RQ1:

```text
embedding model: text-embedding-3-small
distance: 1 - cosine_similarity
```

### Step 3. Join Correctness Metrics

Input:

```text
results/pdr_metrics_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv
```

Join by:

```text
case_id
task
dataset
perturbation
```

Correctness fields already available:

```text
clean_single_correct
perturbed_single_correct
single_sample_pdr
clean_mean_correctness
perturbed_mean_correctness
repeated_sampling_pdr
correctness_sample_noise
```

Add derived fields:

```text
repeated_pass_rate_drop = clean_mean_correctness - perturbed_mean_correctness
abs_repeated_pass_rate_change = abs(clean_mean_correctness - perturbed_mean_correctness)
single_pass_rate_drop = clean_single_correct - perturbed_single_correct
harmful_correctness_drop = repeated_pass_rate_drop > 0
correctness_changed = clean_mean_correctness != perturbed_mean_correctness
```

Important note:

```text
PDR can be unstable when clean correctness is near zero.
Therefore, repeated_pass_rate_drop should be the primary correctness-change variable.
PDR should be reported as an auxiliary normalized metric.
```

## Main RQ2 Analyses

### Analysis A. Case-Level Correlation

Unit:

```text
case_id x perturbation
```

Expected N:

```text
150 case-level rows
```

Primary variables:

```text
X = noise_corrected_drift
Y = abs_repeated_pass_rate_change
```

Also report:

```text
X = raw_perturbation_drift
Y = abs_repeated_pass_rate_change

X = noise_corrected_drift
Y = repeated_pass_rate_drop

X = uncorrected_single_drift
Y = abs(single_pass_rate_drop)
```

Recommended statistics:

```text
Spearman correlation
Pearson correlation
bootstrap confidence interval
permutation p-value, optional
```

Why Spearman matters:

```text
The relationship may be monotonic but not linear.
Correctness is discrete because each case has only 3 samples per prompt version.
```

### Analysis B. Task-Specific Correlation

Run the same correlation separately for:

```text
factual_qa
math_reasoning
code_generation
```

Reason:

```text
Semantic drift may predict correctness differently by task.
For code, small semantic changes can break tests.
For QA, large wording differences may still preserve the exact answer.
For math, reasoning traces can drift while final answer correctness remains unchanged or improves.
```

### Analysis C. Perturbation-Specific Correlation

Group by perturbation:

```text
paraphrase
reordering
formatting
context_injection
surface_noise
```

Question:

```text
Are some perturbations more likely to produce correctness change when semantic drift is high?
```

This can show whether semantic drift is generally predictive or only predictive
for certain perturbation types.

### Analysis D. Group-Level Comparison

Aggregate by:

```text
task x perturbation
```

Expected N:

```text
3 tasks x 5 perturbations = 15 group-level rows
```

For each group, compute:

```text
mean_noise_corrected_drift
mean_abs_pass_rate_change
mean_repeated_pass_rate_drop
mean_repeated_sampling_pdr
```

This gives an interpretable table:

```text
Does the task-perturbation group with larger semantic drift also show larger correctness change?
```

Because N=15 is small, group-level correlation should be descriptive, not the
main statistical evidence.

## Recommended Output Files

Create a new script:

```text
rq2_semantic_correctness_analysis.py
```

Recommended output files:

```text
results/rq2_semantic_correctness_metrics.csv
results/rq2_semantic_correctness_grouped.csv
results/rq2_semantic_correctness_correlations.csv
results/rq2_semantic_correctness_summary.json
results/rq2_semantic_correctness_report.md
```

Suggested contents:

### `rq2_semantic_correctness_metrics.csv`

One row per case-level comparison:

```text
case_id
task
dataset
perturbation
uncorrected_single_drift
original_noise
perturbed_noise
noise_baseline
raw_perturbation_drift
noise_corrected_drift
clean_single_correct
perturbed_single_correct
single_pass_rate_drop
single_sample_pdr
clean_mean_correctness
perturbed_mean_correctness
repeated_pass_rate_drop
abs_repeated_pass_rate_change
repeated_sampling_pdr
correctness_sample_noise
harmful_correctness_drop
correctness_changed
```

### `rq2_semantic_correctness_grouped.csv`

One row per task-perturbation group:

```text
task
dataset
perturbation
n
mean_noise_corrected_drift
mean_raw_perturbation_drift
mean_abs_repeated_pass_rate_change
mean_repeated_pass_rate_drop
mean_repeated_sampling_pdr
share_harmful_correctness_drop
share_correctness_changed
```

### `rq2_semantic_correctness_correlations.csv`

Rows such as:

```text
scope
task
perturbation
x_metric
y_metric
n
spearman_r
pearson_r
bootstrap_ci_low
bootstrap_ci_high
```

### `rq2_semantic_correctness_report.md`

Human-readable report with:

```text
RQ2 definition
data source
methods
overall correlation result
by-task result
by-perturbation result
grouped interpretation
limitations
recommended wording for proposal / paper
```

## Expected Interpretations

RQ2 has three possible outcomes.

### Outcome 1. Strong Positive Relationship

If higher noise-corrected semantic drift predicts larger correctness change:

```text
Noise-corrected semantic drift is not only an output-variation metric; it also tracks
task-performance instability for objective tasks.
```

This would strengthen the practical value of the RQ1 metric.

### Outcome 2. Weak or Task-Dependent Relationship

If the relationship is weak overall but visible in some tasks:

```text
Semantic drift and correctness change are related in a task-dependent way.
For some tasks, especially code generation, semantic drift may be more predictive
of correctness loss, while factual QA and math can preserve correctness despite
surface or reasoning-trace drift.
```

This is likely and scientifically useful.

### Outcome 3. No Clear Relationship

If semantic drift does not predict correctness change:

```text
Semantic drift and correctness degradation are distinct robustness outcomes.
Prompt perturbations can change outputs in semantic or stylistic space without
necessarily changing task correctness.
```

This is also valuable because it justifies reporting both:

```text
Noise-Corrected Semantic Drift
PDR / correctness change
```

## Recommended RQ2 Claim Style

Do not assume semantic drift automatically means correctness loss.

Use cautious wording:

```text
RQ2 tests whether noise-corrected semantic drift is associated with correctness
change on objective tasks. Because semantic drift and correctness drop measure
different outcomes, the analysis reports both pass-rate change and PDR, and
examines whether the relationship differs by task and perturbation type.
```

If the current 10x3 data are used:

```text
This RQ2 analysis reuses the three-task PDR 10x3 generation set and computes
semantic drift on the same clean and perturbed outputs, allowing an apple-to-apple
comparison between output drift and correctness change.
```

## Implementation Recommendation

Best next step:

```text
Implement rq2_semantic_correctness_analysis.py using the existing PDR 10x3 generation file.
```

This requires:

```text
No new text generation calls.
Embedding calls are needed for the existing generated outputs.
```

Why this is efficient:

```text
The expensive generation step is already complete.
The correctness labels are already available.
Only semantic embeddings need to be added for the same outputs.
```

Recommended first version:

```text
1. Read existing PDR 10x3 generations and metrics.
2. Compute embedding-based semantic drift per case.
3. Join semantic metrics with correctness metrics.
4. Compute overall, by-task, and by-perturbation correlations.
5. Write CSV / JSON / Markdown report.
```

## Limitations to State

1. The first RQ2 analysis covers only objective tasks:

```text
factual_qa
math_reasoning
code_generation
```

It excludes open-ended writing because Alpaca has no single ground-truth
correctness label.

2. Correctness is discrete and low-sample per prompt:

```text
3 clean samples
3 perturbed samples
```

Therefore, pass-rate changes can only take a few values.

3. PDR is unstable when clean correctness is zero or near zero.

Therefore:

```text
repeated_pass_rate_drop
abs_repeated_pass_rate_change
```

should be primary, while PDR remains auxiliary.

4. The current perturbations are natural and non-adversarial.

Therefore, a weak relationship between drift and correctness loss does not mean
the perturbations are invalid. It may mean natural prompt variation changes
outputs without consistently harming correctness.

## Bottom Line

RQ2 should be implemented as a link analysis between:

```text
noise-corrected semantic drift
```

and:

```text
correctness change / pass-rate drop / PDR
```

on the same generated outputs from the three-task PDR 10x3 run.

This is the cleanest next step because it avoids new text generation and directly
tests whether the semantic-drift signal from RQ1 has task-performance meaning
for objective tasks.

---

# RQ2 实现计划

## RQ2 定义

`research.md` 中当前的 RQ2 是：

```text
For tasks with objective correctness, does semantic drift predict correctness changes?
```

实际含义是，RQ2 要回答：

```text
当 prompt perturbation 在 embedding / semantic space 中改变模型输出时，
这种语义层面的变化是否也对应着可测量的 task correctness 变化？
```

这和 RQ1 不同：

```text
RQ1: 哪些 perturbation 类型会产生 noise-corrected semantic drift，并且 ranking 是否 task-dependent？
RQ2: 这些 semantic drift 是否真的能预测 correctness degradation 或 correctness change？
```

## 范围

RQ2 应只使用有客观 correctness label 的任务：

| Task | Dataset | Correctness criterion | 是否用于 RQ2 |
|---|---|---|---:|
| factual_qa | SQuAD V2 | exact short-answer match | 是 |
| math_reasoning | MATH | final-answer exact match | 是 |
| code_generation | HumanEval | pass@1-style unit-test pass/fail | 是 |
| open_ended_writing | Alpaca | 没有单一客观 correctness label | 否，保留为未来 qualitative / auxiliary analysis |

因此，第一版 RQ2 实现应聚焦于：

```text
factual_qa
math_reasoning
code_generation
```

## 最适合复用的现有数据

RQ2 当前最强的输入数据是三任务 PDR 10x3 运行结果：

```text
results/generations_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv
results/pdr_metrics_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv
results/pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md
```

这次运行已经包含：

```text
3 objective tasks
10 cases/task
5 perturbations
3 clean generations per case
3 perturbed generations per case
correctness for every generated output
PDR metrics per task-perturbation-case
```

规模：

```text
3 tasks x 10 cases/task x 5 perturbations = 150 case-level comparisons
150 comparisons x 2 prompt versions x 3 samples = 900 generated outputs
```

## 为什么不直接使用 RQ1 similarity run？

最新 RQ1 similarity run 是：

```text
results/similarity_report_four_task_similarity_sweep_pdr_aligned_5x3.md
```

它适合用于 RQ1，但不适合作为 RQ2 的主要输入，因为：

1. 它只有 `5 cases/task`。
2. 它包含 Alpaca，而 Alpaca 没有 objective correctness label。
3. 它的 generations 和 PDR 10x3 run 不是同一批 generations。

对 RQ2 来说，最好的设计是在**同一批 generated outputs** 上同时计算
semantic drift 和 correctness change。因此，RQ2 应从 PDR 10x3 generation
file 出发，在它上面补算 semantic drift。

## 推荐的 RQ2 方法

### Step 1. 读取已有 PDR generations

输入：

```text
results/generations_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv
```

需要的列：

```text
case_id
task
dataset
perturbation
version
sample_idx
output
correct
```

每个 `case_id` 应有：

```text
3 original outputs
3 perturbed outputs
```

### Step 2. 在同一批 outputs 上计算 semantic drift

对每个 `case_id`，embedding 六个输出：

```text
original outputs:  o1, o2, o3
perturbed outputs: p1, p2, p3
```

然后计算：

```text
original_noise = average pairwise distance among o1, o2, o3
perturbed_noise = average pairwise distance among p1, p2, p3
noise_baseline = (original_noise + perturbed_noise) / 2
raw_perturbation_drift = average cross-distance between original outputs and perturbed outputs
noise_corrected_drift = max(0, raw_perturbation_drift - noise_baseline)
uncorrected_single_drift = distance(o1, p1)
```

使用和 RQ1 相同的 embedding 设置：

```text
embedding model: text-embedding-3-small
distance: 1 - cosine_similarity
```

### Step 3. 合并 correctness metrics

输入：

```text
results/pdr_metrics_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv
```

按以下字段合并：

```text
case_id
task
dataset
perturbation
```

已有 correctness 字段：

```text
clean_single_correct
perturbed_single_correct
single_sample_pdr
clean_mean_correctness
perturbed_mean_correctness
repeated_sampling_pdr
correctness_sample_noise
```

新增派生字段：

```text
repeated_pass_rate_drop = clean_mean_correctness - perturbed_mean_correctness
abs_repeated_pass_rate_change = abs(clean_mean_correctness - perturbed_mean_correctness)
single_pass_rate_drop = clean_single_correct - perturbed_single_correct
harmful_correctness_drop = repeated_pass_rate_drop > 0
correctness_changed = clean_mean_correctness != perturbed_mean_correctness
```

重要说明：

```text
当 clean correctness 接近 0 时，PDR 可能不稳定。
因此，repeated_pass_rate_drop 应作为主要 correctness-change 变量。
PDR 应作为辅助 normalized metric 报告。
```

## 主要 RQ2 分析

### Analysis A. Case-level correlation

分析单位：

```text
case_id x perturbation
```

预期 N：

```text
150 case-level rows
```

主要变量：

```text
X = noise_corrected_drift
Y = abs_repeated_pass_rate_change
```

也报告：

```text
X = raw_perturbation_drift
Y = abs_repeated_pass_rate_change

X = noise_corrected_drift
Y = repeated_pass_rate_drop

X = uncorrected_single_drift
Y = abs(single_pass_rate_drop)
```

推荐统计量：

```text
Spearman correlation
Pearson correlation
bootstrap confidence interval
permutation p-value, optional
```

为什么 Spearman 重要：

```text
二者关系可能是单调但非线性的。
correctness 是离散变量，因为每个 prompt version 只有 3 个 samples。
```

### Analysis B. Task-specific correlation

分别对以下任务做同样的 correlation：

```text
factual_qa
math_reasoning
code_generation
```

原因：

```text
semantic drift 对 correctness 的预测能力可能因任务而异。
对于 code，小的 semantic change 就可能破坏 unit tests。
对于 QA，大的 wording difference 也可能仍然保留 exact answer。
对于 math，reasoning trace 可能发生 drift，但 final answer correctness 不变甚至提高。
```

### Analysis C. Perturbation-specific correlation

按 perturbation 分组：

```text
paraphrase
reordering
formatting
context_injection
surface_noise
```

问题：

```text
当 semantic drift 较高时，是否某些 perturbation 更容易导致 correctness change？
```

这可以说明 semantic drift 是普遍具有预测力，还是只对某些 perturbation 类型有预测力。

### Analysis D. Group-level comparison

按以下组合聚合：

```text
task x perturbation
```

预期 N：

```text
3 tasks x 5 perturbations = 15 group-level rows
```

每组计算：

```text
mean_noise_corrected_drift
mean_abs_pass_rate_change
mean_repeated_pass_rate_drop
mean_repeated_sampling_pdr
```

这会得到一个易解释的表：

```text
semantic drift 更大的 task-perturbation group 是否也显示更大的 correctness change？
```

由于 N=15 很小，group-level correlation 应作为描述性结果，而不是主要统计证据。

## 推荐输出文件

创建新脚本：

```text
rq2_semantic_correctness_analysis.py
```

推荐输出文件：

```text
results/rq2_semantic_correctness_metrics.csv
results/rq2_semantic_correctness_grouped.csv
results/rq2_semantic_correctness_correlations.csv
results/rq2_semantic_correctness_summary.json
results/rq2_semantic_correctness_report.md
```

### `rq2_semantic_correctness_metrics.csv`

每个 case-level comparison 一行：

```text
case_id
task
dataset
perturbation
uncorrected_single_drift
original_noise
perturbed_noise
noise_baseline
raw_perturbation_drift
noise_corrected_drift
clean_single_correct
perturbed_single_correct
single_pass_rate_drop
single_sample_pdr
clean_mean_correctness
perturbed_mean_correctness
repeated_pass_rate_drop
abs_repeated_pass_rate_change
repeated_sampling_pdr
correctness_sample_noise
harmful_correctness_drop
correctness_changed
```

### `rq2_semantic_correctness_grouped.csv`

每个 task-perturbation group 一行：

```text
task
dataset
perturbation
n
mean_noise_corrected_drift
mean_raw_perturbation_drift
mean_abs_repeated_pass_rate_change
mean_repeated_pass_rate_drop
mean_repeated_sampling_pdr
share_harmful_correctness_drop
share_correctness_changed
```

### `rq2_semantic_correctness_correlations.csv`

包含如下行：

```text
scope
task
perturbation
x_metric
y_metric
n
spearman_r
pearson_r
bootstrap_ci_low
bootstrap_ci_high
```

### `rq2_semantic_correctness_report.md`

人类可读报告，包含：

```text
RQ2 definition
data source
methods
overall correlation result
by-task result
by-perturbation result
grouped interpretation
limitations
recommended wording for proposal / paper
```

## 可能的结果解释

RQ2 可能有三种结果。

### Outcome 1. 强正相关

如果更高的 noise-corrected semantic drift 能预测更大的 correctness change：

```text
Noise-corrected semantic drift is not only an output-variation metric; it also tracks
task-performance instability for objective tasks.
```

这会增强 RQ1 指标的实际价值。

### Outcome 2. 弱相关或 task-dependent relationship

如果整体关系较弱，但某些任务中可见：

```text
Semantic drift and correctness change are related in a task-dependent way.
For some tasks, especially code generation, semantic drift may be more predictive
of correctness loss, while factual QA and math can preserve correctness despite
surface or reasoning-trace drift.
```

这很可能出现，而且具有科学价值。

### Outcome 3. 没有明显关系

如果 semantic drift 不能预测 correctness change：

```text
Semantic drift and correctness degradation are distinct robustness outcomes.
Prompt perturbations can change outputs in semantic or stylistic space without
necessarily changing task correctness.
```

这同样有价值，因为它说明需要同时报告：

```text
Noise-Corrected Semantic Drift
PDR / correctness change
```

## 推荐的 RQ2 表述方式

不要默认认为 semantic drift 自动意味着 correctness loss。

建议使用谨慎表述：

```text
RQ2 tests whether noise-corrected semantic drift is associated with correctness
change on objective tasks. Because semantic drift and correctness drop measure
different outcomes, the analysis reports both pass-rate change and PDR, and
examines whether the relationship differs by task and perturbation type.
```

如果使用当前 10x3 数据：

```text
This RQ2 analysis reuses the three-task PDR 10x3 generation set and computes
semantic drift on the same clean and perturbed outputs, allowing an apple-to-apple
comparison between output drift and correctness change.
```

## 实现建议

最佳下一步：

```text
Implement rq2_semantic_correctness_analysis.py using the existing PDR 10x3 generation file.
```

这需要：

```text
No new text generation calls.
Embedding calls are needed for the existing generated outputs.
```

为什么这样高效：

```text
The expensive generation step is already complete.
The correctness labels are already available.
Only semantic embeddings need to be added for the same outputs.
```

推荐第一版实现：

```text
1. Read existing PDR 10x3 generations and metrics.
2. Compute embedding-based semantic drift per case.
3. Join semantic metrics with correctness metrics.
4. Compute overall, by-task, and by-perturbation correlations.
5. Write CSV / JSON / Markdown report.
```

## 需要说明的限制

1. 第一版 RQ2 分析只覆盖 objective tasks：

```text
factual_qa
math_reasoning
code_generation
```

它排除 open-ended writing，因为 Alpaca 没有单一 ground-truth correctness label。

2. Correctness 是离散的，而且每个 prompt 的 sample 数较少：

```text
3 clean samples
3 perturbed samples
```

因此，pass-rate changes 只能取少数几个值。

3. 当 clean correctness 为 0 或接近 0 时，PDR 不稳定。

因此：

```text
repeated_pass_rate_drop
abs_repeated_pass_rate_change
```

应作为主要变量，而 PDR 作为辅助指标。

4. 当前 perturbations 是 natural and non-adversarial。

因此，如果 drift 和 correctness loss 的关系较弱，并不表示 perturbations 无效。
它可能说明 natural prompt variation 会改变输出，但不一定稳定损害 correctness。

## Bottom Line

RQ2 应实现为以下二者之间的关联分析：

```text
noise-corrected semantic drift
```

和：

```text
correctness change / pass-rate drop / PDR
```

分析应基于三任务 PDR 10x3 run 中的同一批 generated outputs。

这是最干净的下一步，因为它避免新的 text generation，并且可以直接检验
RQ1 中的 semantic-drift signal 是否对 objective tasks 具有 task-performance
意义。
