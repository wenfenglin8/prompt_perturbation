# 为什么 Surface-Noise Scatter 里的 Code-Generation 点特别分散

## 对应图

```text
results/rq2_figures/rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_similarity_vs_correctness_scatter.png
```

这张图只画了非零 surface-noise 强度：

```text
strength_edits = 2, 4, 8, 16
```

x 轴是：

```text
mean_cross_similarity
```

y 轴是：

```text
abs_repeated_pass_rate_change
```

也就是：

```text
abs(clean_mean_correctness - perturbed_mean_correctness)
```

## 数据完整性检查

我检查了 5 个 batch 合并后的 metrics 数据。

```text
Total metric rows: 1000
Duplicate base_case_id + strength_edits rows: 0
Rows per task:
  code_generation    250
  factual_qa         250
  long_factual_qa    250
  math_reasoning     250
```

对非零扰动强度而言：

```text
code_generation rows: 200
```

所以 code-generation 的点很散，并不是由重复行或 batch 合并错误造成的。

## 主要原因

code-generation 的点更分散，主要是因为 HumanEval correctness 是二元的，而且对输出格式很敏感。

每个 prompt version 采样 5 次。每个 HumanEval 输出只有两种结果：

```text
pass = 1.0
fail = 0.0
```

因此 repeated correctness mean 只能取这些离散值：

```text
0.0, 0.2, 0.4, 0.6, 0.8, 1.0
```

所以 code-generation 的 y 轴值也会以离散跳变的形式出现：

```text
0.0, 0.2, 0.4, 0.6, 0.8, 1.0
```

这会让 code-generation 的点看起来比 partial-credit 或连续评分任务更分散。

## Absolute Change 会混合 Improvement 和 Harmful Drop

这张图画的是绝对变化：

```text
abs_repeated_pass_rate_change
```

所以它不区分：

```text
clean 比 perturbed 更好
perturbed 比 clean 更好
```

对于 code-generation 的非零扰动 rows，方向统计是：

```text
unchanged: 127
improved under perturbed: 56
dropped under perturbed: 17
```

对于高变化 rows：

```text
abs_repeated_pass_rate_change >= 0.4
```

方向统计是：

```text
improved under perturbed: 37
dropped under perturbed: 9
unchanged: 0
```

因此，很多 y 值很高的 code 点并不是 harmful failure。它们是 perturbed prompt 下通过测试的样本更多，所以 correctness movement 很大。

## 为什么 Code 特别敏感

HumanEval correctness 取决于代码是否能执行并通过单元测试，也很受输出格式影响。

评估器会尝试执行：

```text
HumanEval prompt prefix + model completion
```

同时也接受 standalone full-code output 作为 fallback。

一些很小的生成风格变化都可能影响 pass/fail：

```text
是否重复 function header
是否漏掉 function header
markdown fences
额外解释文字
imports
indentation
edge-case handling
minor syntax mistakes
```

surface noise 只改 instruction，不改 HumanEval function prompt 本身。但它仍然可能改变模型补全代码的格式或风格，从而让 unit-test pass/fail 出现较大波动。

## Embedding Similarity 不等于 Functional Equivalence

x 轴基于 clean outputs 和 perturbed outputs 之间的 embedding similarity。

但对代码来说，embedding similarity 不等于 functional equivalence：

```text
两个代码输出看起来语义差异较大，但都可能通过测试。
两个代码输出看起来语义很接近，但一个小 bug 就可能导致测试失败。
```

所以在 individual-case 层面，semantic similarity 和 unit-test correctness 不会完全对齐。

## 但这不是随机噪声

虽然 code 点视觉上很分散，但它们仍然有很强的单调关系：

```text
code_generation nonzero similarity vs correctness-change Spearman = -0.7385
```

也就是说：

```text
similarity 越低，correctness movement 越大
```

所以 code-generation 的点云不是随机的。它是 noisy and discrete，但方向上和 RQ2 的预期一致。

## 推荐解释

code-generation 点大范围分散，并不是 batch merging 或 counting error。它主要反映了 HumanEval pass/fail 评分的二元性和格式敏感性。在当前图里，correctness change 使用绝对值，所以 harmful drops 和 improvements 都会显示成大的 movement。此外，代码输出的 embedding similarity 和 functional equivalence 并不完全一致，这也会进一步拉散 case-level scatter。

## 建议补充图

建议补一张 code-only scatter，把 direction 分开：

```text
performance drop
performance improvement
unchanged
```

这样可以更清楚地说明：很多高 y 值的 code-generation 点，其实是 perturbed prompt 下表现变好，而不是有害的 robustness failure。
