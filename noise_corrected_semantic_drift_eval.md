# Noise-Corrected Semantic Drift Evaluation

## 目标

本评价准则用于比较两种估计方式：

1. **Uncorrected**：直接比较一次 clean output 和一次 perturbed output。
2. **Sample-noise-corrected**：先估计同一个 prompt 多次采样时自身产生的随机差异，再从 clean-vs-perturbed 的观测差异中扣除这部分采样噪声。

核心问题是：

> 在相同数据集、相同扰动、相同模型、相同采样参数下，perturbation 造成的输出变化有多少是真正由 prompt 扰动引起的，有多少只是模型采样随机性造成的？

## 评价原理

LLM 在非确定性采样设置下，例如：

```text
temperature = 0.7
top_p = 0.9
```

即使输入完全相同，多次生成的答案也可能不同。因此，单次 clean output 和单次 perturbed output 的差异并不一定全部来自 perturbation。

观测到的差异可以理解为：

```text
observed difference = perturbation effect + sampling randomness
```

`Noise-Corrected Semantic Drift` 的目的就是从观测差异中扣除 sampling randomness，只保留更接近 perturbation 本身造成的语义漂移。

## 输出集合定义

对原始 prompt 重复采样，得到 clean outputs：

```text
C = {c1, c2, ..., cn}
```

对扰动后的 prompt 重复采样，得到 perturbed outputs：

```text
P = {p1, p2, ..., pn}
```

其中 `n` 是每个 prompt 的重复采样次数，例如当前实验常用：

```text
n = 3
```

## 语义距离

两个输出之间的差异用 embedding cosine distance 衡量：

```text
d(x, y) = 1 - cosine_similarity(embedding(x), embedding(y))
```

含义：

- `d(x, y)` 越小，两个输出语义越接近。
- `d(x, y)` 越大，两个输出语义漂移越明显。

这个距离比较的是输出在语义空间里的距离，而不是字符串表面的 exact match。

## Uncorrected Drift

Uncorrected 方法只取一次 clean output 和一次 perturbed output：

```text
D_uncorr = d(c1, p1)
```

它的含义是：

> 单次 clean 生成和单次 perturbed 生成之间的语义差异。

问题是，`D_uncorr` 同时包含 perturbation effect 和 sampling randomness，所以它可能高估 perturbation 的影响。

## Raw Between-Prompt Drift

为了减少单次采样偶然性，先计算 clean outputs 和 perturbed outputs 之间的平均距离：

```text
D_between = mean_{i,j} d(ci, pj)
```

含义：

> clean prompt 的输出分布和 perturbed prompt 的输出分布之间的平均语义差异。

但是，`D_between` 仍然包含两个 prompt 各自内部的采样噪声。

## Within-Prompt Sample Noise

clean prompt 自身的采样噪声：

```text
D_clean_noise = mean_{i<j} d(ci, cj)
```

perturbed prompt 自身的采样噪声：

```text
D_perturbed_noise = mean_{i<j} d(pi, pj)
```

综合 sample noise：

```text
D_noise = 0.5 * (D_clean_noise + D_perturbed_noise)
```

含义：

> 在没有比较不同 prompt 的情况下，模型仅因为重复采样而产生的平均语义差异。

## Noise-Corrected Semantic Drift

最终的 corrected drift 定义为：

```text
D_corr = max(0, D_between - D_noise)
```

含义：

> clean-vs-perturbed 的平均语义差异，扣除同 prompt 多次采样本来就会产生的随机差异。

使用 `max(0, ...)` 是为了避免出现负漂移。若 `D_between <= D_noise`，说明 clean 和 perturbed 之间的差异没有超过模型自身采样波动范围，因此记为 0。

## 解释示例

示例 1：

```text
D_between = 0.20
D_noise = 0.15
D_corr = 0.05
```

解释：

clean 和 perturbed 的输出看起来有 `0.20` 的语义差异，但其中 `0.15` 是模型采样随机性本身造成的。扣除 sample noise 后，可以归因给 perturbation 的语义漂移约为 `0.05`。

示例 2：

```text
D_between = 0.12
D_noise = 0.15
D_corr = 0
```

解释：

clean 和 perturbed 之间的差异没有超过模型自身随机波动范围，因此不能认为这个 perturbation 造成了稳定的语义变化。

## 建议报告的指标

每个 task、每种 perturbation 都建议报告：

```text
D_uncorr
D_between
D_noise
D_corr
correction_ratio
```

其中：

```text
correction_ratio = D_corr / D_between
```

若 `D_between = 0`，则 `correction_ratio` 记为 `NA`。

## 指标解释

`D_uncorr`：

```text
单次比较得到的扰动敏感性。
```

`D_between`：

```text
多次采样后，clean output distribution 和 perturbed output distribution 的原始距离。
```

`D_noise`：

```text
同一个 prompt 多次采样产生的自然语义波动。
```

`D_corr`：

```text
扣除采样噪声后，perturbation 本身更可能造成的语义漂移。
```

`correction_ratio`：

```text
原始 between-prompt drift 中有多少比例在扣除 sample noise 后仍然保留。
```

## 适合当前数据集的原因

该准则适合当前四类任务：

```text
factual QA
math reasoning
code generation
open-ended writing
```

原因是：

1. 它不要求每个任务都有标准答案。
2. 它可以用于 open-ended writing。
3. 它不依赖模型 logprobs。
4. 它可以在相同数据集、相同扰动、相同采样参数下直接比较 corrected 和 uncorrected。
5. 它与 sample noise correction 的研究目标一致。

## 与参考文献的关系

`PromptRobust` 和 `Enhancing LLM Robustness to Perturbed Instructions` 使用 PDR 衡量扰动后的性能下降，适合有明确 task score 的任务，例如 QA、classification、math 或 code pass rate。

但 PDR 不适合作为四任务统一主指标，因为 open-ended writing 没有稳定的 ground-truth score。

`POSIX` 关注 prompt sensitivity，并包含 response semantic coherence / semantic similarity 的思想，但完整 POSIX 指标依赖 response likelihood 或 confidence distribution，不适合作为当前 API 实验的主指标。

`What Did I Do Wrong` 主要面向 classification prompt sensitivity，基于 label distribution entropy 和 consistency，不适合 QA、math、code、writing 四类任务的统一评价。

`Within-Model vs Between-Prompt Variability` 的核心思想是区分同一 prompt 内部的生成随机性和不同 prompt 之间的变异，这与本评价准则的 sample-noise correction 思路一致。

因此，推荐将 `Noise-Corrected Semantic Drift` 作为主 evaluation criterion，将 PDR / task score drop 作为客观任务上的辅助指标。

## 最终建议

主评价准则：

```text
Noise-Corrected Semantic Drift
```

辅助评价准则：

```text
Performance Drop Rate / task score drop
```

辅助准则仅用于有客观评分的任务：

```text
factual QA
math reasoning
code generation
```

不建议将 PDR 用于 open-ended writing。

