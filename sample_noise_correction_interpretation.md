# Sample-Noise Correction 结果解释

本文解释 `rq1_four_task_similarity_sweep_result.md` 中的这一段结果：

```text
## Effect of Sample-Noise Correction
```

核心问题是：

```text
为什么有些 raw drift 在 correction 后变成 0，
但有些 perturbation correction 后仍然很大？
```

## 三个核心指标

在 four-task similarity sweep 中，我们比较的是 clean prompt 输出和 perturbed prompt 输出之间的 embedding distance。

三个关键指标是：

| 指标 | 含义 |
|---|---|
| `raw drift` | clean prompt outputs 和 perturbed prompt outputs 之间的平均距离 |
| `noise baseline` | 同一个 prompt 重复生成时，outputs 之间本来就存在的平均距离 |
| `corrected drift` | 扣除 sample noise 后剩下的 drift，即 perturbation-specific drift |

公式是：

```text
corrected drift = max(0, raw drift - noise baseline)
```

所以：

```text
如果 raw drift <= noise baseline，
那么 corrected drift = 0。
```

这表示 observed output difference 可以被模型正常采样波动解释，不能强说是 prompt perturbation 造成的。

## 为什么有些 raw drift 消失了？

例如：

```text
Math sentence:
raw drift       = 0.0308
corrected drift = 0.0000

Code character:
raw drift       = 0.0168
corrected drift = 0.0000

Writing character:
raw drift       = 0.0313
corrected drift = 0.0000
```

这些结果的意思是：

1. 表面上 clean prompt 和 perturbed prompt 的输出确实有差异。
2. 但是同一个 prompt 重复生成时，本身也会产生类似大小的差异。
3. 因此，这些 raw drift 不能被可靠解释为 perturbation effect。

换句话说：

```text
这些差异看起来像 perturbation 造成的，
但扣掉 sample noise 后，没有留下稳定的 perturbation-specific signal。
```

## 例子 1：Math sentence

结果：

```text
Math sentence:
raw drift       = 0.0308
corrected drift = 0.0000
```

解释：

sentence-level perturbation 看起来让 MATH 输出变化了 `0.0308`。但是 MATH 同一个 prompt 重复生成时，本来就会出现接近这个量级的输出波动。

因此：

```text
不能说 sentence perturbation 真的改变了 MATH 输出。
```

更准确地说：

```text
observed drift is explainable by sample noise.
```

## 例子 2：Code character

结果：

```text
Code character:
raw drift       = 0.0168
corrected drift = 0.0000
```

解释：

character-level typo 对 HumanEval code generation 的 raw drift 很小，而且小到可以被 repeated generation variability 覆盖。

因此：

```text
在这组小样本中，character typo 没有产生稳定的 code-output drift。
```

## 例子 3：Writing character

结果：

```text
Writing character:
raw drift       = 0.0313
corrected drift = 0.0000
```

解释：

open-ended writing 本身输出空间很大。即使 prompt 完全不变，模型每次生成的表达、句子结构、细节也会变化。

所以 Alpaca writing 中 character perturbation 的 raw drift 被 sample-noise baseline 完全解释掉。

这说明：

```text
对 open-ended writing，单次 clean output vs 单次 perturbed output 的比较尤其不可靠。
```

## 为什么 Open-Ended Writing 的 noise baseline 重要？

开放式写作没有唯一标准答案。模型可以用很多不同方式回答同一个 prompt。

因此：

```text
same prompt repeated outputs
```

本来就会有较大差异。

这就是为什么 Haase et al. 的 repeated generation / within-LLM variance 对本项目很重要：

```text
如果不估计同一 prompt 下的自然波动，
就会把正常生成差异误认为 prompt perturbation effect。
```

## 为什么 Semantic Perturbation 在 QA 和 Code 上仍然明显？

有些 perturbation 在 correction 后仍然保留较大 drift。例如：

```text
Factual QA semantic corrected drift = 0.2889
Code semantic corrected drift       = 0.1357
```

这表示：

1. clean prompt 和 semantic-perturbed prompt 的输出差异很大；
2. 同一个 prompt 内部的 repeated generation noise 很小；
3. 所以扣除 sample noise 后，仍然留下明显 difference。

因此，这类结果更有可能是真正的 perturbation effect。

## Factual QA semantic perturbation

结果：

```text
Factual QA semantic corrected drift = 0.2889
```

解释：

semantic-level instruction rewrite 对 SQuAD V2 的输出影响很明显。即使扣除同一 prompt 下的 repeated generation noise，输出仍然发生较大变化。

这说明：

```text
Factual QA 对 semantic-level prompt 表达变化比较敏感。
```

## Code semantic perturbation

结果：

```text
Code semantic corrected drift = 0.1357
```

解释：

HumanEval code generation 对 semantic-level instruction rewrite 也比较敏感。代码生成任务中，instruction 表达方式可能影响：

- 是否只输出代码；
- 是否包含 explanation；
- 代码结构；
- 边界条件处理；
- 函数实现风格。

所以 semantic perturbation 后仍有明显 corrected drift 是合理的。

## 总结

这段结果的核心含义是：

```text
sample-noise correction 区分了“看起来变了”和“真的因为 perturbation 变了”。
```

更具体地说：

| 情况 | 解释 |
|---|---|
| raw drift > 0, corrected drift = 0 | 输出看起来变了，但变化可以由 sample noise 解释 |
| corrected drift > 0 | 扣除 sample noise 后仍有变化，更可能是 perturbation effect |
| open-ended writing noise baseline 大 | 开放式任务天然随机性更强，单次比较不可靠 |
| semantic perturbation corrected drift 大 | 语义级 instruction 改写可能真正改变模型输出行为 |

一句话总结：

```text
有些 raw drift 扣掉自然波动后消失了；
但 semantic perturbation 对 Factual QA 和 Code 的影响扣掉 noise 后仍然明显，所以更可信。
```
