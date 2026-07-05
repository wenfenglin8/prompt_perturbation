# 为什么 `similarity_by_task` 里 corrupted instruction words 增加时 similarity 会局部上升

## 对应图

```text
results/rq2_figures/rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_similarity_by_task.png
```

这张图展示的是不同 task 下，surface-noise strength 和输出相似度之间的关系。

需要注意：图里的 similarity 不是 prompt similarity，而是 model output similarity。

## 图里的 Similarity 是怎么计算的

图中的 y 轴是：

```text
mean_cross_similarity
```

它不是：

```text
clean instruction 和 corrupted instruction 的文本相似度
```

而是：

```text
clean prompt 生成的 5 个 outputs
vs
perturbed prompt 生成的 5 个 outputs
```

之间的 embedding cross similarity。

代码逻辑是：

```python
raw_drift = avg_cross_distance(original_vectors, perturbed_vectors)
mean_cross_similarity = 1.0 - raw_drift
```

所以它测的是：

```text
模型输出之间有多相似
```

而不是：

```text
prompt 被污染得有多严重
```

因此，即使 corrupted instruction words 增加，模型也可能在某个 level 生成更接近 clean prompt 的答案，导致 output similarity 局部上升。

## 观察到的局部反弹

从合并后的 `by_task_level.csv` 看，确实有一些局部反弹。

```text
factual_qa:
0: 1.0000
2: 0.9784
4: 0.9706
8: 0.9735  <- 小幅反弹
16: 0.9685

long_factual_qa:
0: 1.0000
2: 0.9734
4: 0.9666
8: 0.9724  <- 小幅反弹
16: 0.9657

code_generation:
0: 1.0000
2: 0.9381
4: 0.9406  <- 小幅反弹
8: 0.9270
16: 0.9267

math_reasoning:
0: 1.0000
2: 0.9546
4: 0.9545
8: 0.9532
16: 0.9527
```

这些反弹幅度都很小。整体方向仍然是下降。

总图中的 overall mean 是单调下降的：

```text
0: 1.0000
2: 0.9611
4: 0.9581
8: 0.9565
16: 0.9534
```

## 为什么会局部上升

### 1. Output Similarity 不是 Deterministic Prompt Similarity

surface noise 的 strength 是 deterministic 的，但模型输出不是 deterministic 的。

即使 prompt 更 noisy，模型仍可能生成更接近 clean prompt 的答案。尤其 surface noise 是弱扰动，模型通常还能理解任务。

所以：

```text
prompt corruption strength 增加
```

不必然导致：

```text
output similarity 每一级都严格下降
```

更合理的预期是整体趋势下降，而不是逐点单调下降。

### 2. Repeated Sampling 仍有采样波动

每个 prompt version 采样 5 次。

虽然比 single sample 稳定，但 5 次仍然会有输出波动。某个 strength level 下，如果模型刚好生成了更模板化、更接近 clean 的答案，该 level 的 mean similarity 就可能反弹。

### 3. Surface Noise 在短 Instruction 上会饱和

surface noise 只污染 instruction 里的 eligible words。

对短 instruction，例如 factual QA、math、code generation，可污染的词有限。

例如 factual QA instruction：

```text
Read the passage and answer the question. Answer with the exact short answer only.
```

当 edits 增加到 8 或 16 时，实际能新增污染的词已经很少，甚至可能已经饱和。

因此：

```text
strength_edits = 16
```

更准确地说是：

```text
requested corruption budget = 16
```

不一定代表实际新增污染了 16 个不同词。

## 检查结果：不是明显计算错误

我检查了每个 case 内部的：

```text
strength_edits -> mean_cross_similarity
```

Spearman 方向。

结果是：

```text
code_generation: 48/49 cases negative
factual_qa: 39/45 cases negative
long_factual_qa: 48/50 cases negative
math_reasoning: 50/50 cases negative
```

也就是说，大多数 case 内部都是：

```text
strength 越高，similarity 越低
```

所以这不是随机乱掉，也不是明显的 batch 合并错误或 similarity 计算错误。

task-level 平均曲线中的小反弹，主要是模型输出采样波动和 surface-noise 饱和造成的局部现象。

## 当前图的问题

当前图容易让读者误解为：

```text
corrupted instruction words 是实际污染词数
mean_cross_similarity 应该随 strength 严格单调下降
```

但实际图中：

```text
x 轴是 requested corruption budget
y 轴是 model output similarity
```

这两个量之间不保证逐级单调。

## 推荐改法

### 1. 修改 x 轴说明

建议把 x 轴从：

```text
Surface-noise strength: corrupted instruction words
```

改成：

```text
Surface-noise strength: requested corrupted instruction words
```

或者：

```text
Requested surface-noise edit budget
```

这样更准确。

### 2. 加 Error Bar 或 Confidence Interval

当前 task-level line 只画了 mean，没有展示波动范围。

建议增加：

```text
standard error
bootstrap CI
```

这样可以看出 4 到 8 的小反弹是否在误差范围内。

### 3. 新增 Actual Corruption 指标

建议在 metrics 或 generation metadata 里记录：

```text
actual_corrupted_words
prompt_edit_distance
prompt_similarity
```

这样可以区分：

```text
requested edits
```

和：

```text
actual prompt perturbation
```

### 4. 改进 Surface-Noise 函数

如果要更严格的 dose-response，可以让 surface-noise 函数避免短 instruction 饱和。

可选方案：

```text
扩展 instruction wrapper，让 eligible words 更多
允许同一个词被多次施加不同字符扰动
把 surface noise 应用到 instruction + task framing，而不是只应用到短 instruction
记录并强制 actual_corrupted_words 达到目标
```

## 推荐解释

这张图中的局部上升不是明显的计算错误。原因是 y 轴表示的是模型输出相似度，而不是 prompt 本身的相似度。surface noise 的 requested strength 增加后，模型输出相似度总体下降，但由于 repeated sampling 波动、surface-noise 在短 instruction 上的饱和，以及模型对 typo/noise 的鲁棒性，个别 task-level mean 会出现小幅反弹。整体趋势仍然支持 surface noise strength 增加会降低 output similarity。
