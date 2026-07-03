# Proposal Similarity vs Noise-Corrected Semantic Drift

## 核心结论

`Noise-Corrected Semantic Drift` 不是脱离 proposal 的新评价方向。

更准确地说：

```text
proposal 定义的是 semantic similarity 这个基础度量；
Noise-Corrected Semantic Drift 是把 proposal 里的 similarity + noise baseline 思路操作化成一个可计算的 corrected effect size。
```

两者的研究对象是一致的：

```text
clean prompt 生成的 output
vs
perturbed prompt 生成的 output
```

也就是说，比较的是输出之间的语义变化，而不是 original prompt 和 perturbed prompt 本身之间的相似度。

## 1. Similarity 和 Drift 的方向不同

Proposal 中的基础指标是：

```text
semantic similarity = cosine_similarity(embedding(clean_output), embedding(perturbed_output))
```

含义：

```text
值越大，两个输出越相似；
值越小，两个输出语义漂移越明显。
```

当前 `Noise-Corrected Semantic Drift` 使用的是：

```text
semantic drift = 1 - cosine_similarity(embedding(clean_output), embedding(perturbed_output))
```

含义：

```text
值越大，语义漂移越明显；
值越小，两个输出越相似。
```

所以二者只是方向相反：

```text
drift = 1 - similarity
similarity = 1 - drift
```

本质上，它们都基于 embedding cosine comparison。

## 2. Proposal 已经包含 noise baseline 的思想

Proposal 的 4.3 Noise Baseline Design 中写到：

```text
The distribution of semantic similarities among the multiple outputs generated from the same prompt constitutes that prompt's noise baseline.
The similarity between the original prompt and each perturbed version will then be compared against this baseline.
```

这说明 proposal 原本就不是只做一次 clean-output 和 perturbed-output 的简单比较。

它的核心思路是：

```text
1. 对同一个 prompt 多次生成，得到 within-prompt similarity distribution。
2. 把这个 distribution 作为 sample noise baseline。
3. 再判断 clean vs perturbed 的相似度变化是否超过这个 baseline。
```

因此，sample-noise correction 本身是 proposal 的核心设计，不是额外新增的研究方向。

## 3. 当前公式是对 proposal 思路的具体化

Proposal 说明了要把 clean-vs-perturbed similarity 和 noise baseline 比较，但没有给出一个单一的 corrected drift 公式。

当前 `Noise-Corrected Semantic Drift` 把这个思路具体化为：

```text
D_corr = max(0, D_between - D_noise)
```

其中：

```text
D_between = clean outputs 和 perturbed outputs 之间的平均语义距离
D_noise   = 同一个 prompt 内部多次采样产生的平均语义距离
```

这个公式的含义是：

```text
perturbation-specific drift
= observed clean-vs-perturbed drift
  - within-prompt sample noise
```

因此，当前公式可以被理解为 proposal 中 noise-baseline comparison 的一个可执行实现版本。

## 4. Proposal 更强调显著性检验，当前公式更强调 effect size

Proposal 的 4.6 Analysis Methods and Visualization 中写到：

```text
The difference between the post-perturbation similarity and the noise-baseline similarity will be assessed for significance using paired tests, and its magnitude will be quantified using an effect size such as Cohen's d.
```

这说明 proposal 原本计划报告两类结果：

```text
1. significance test:
   判断 perturbation effect 是否显著超过 sample noise。

2. effect size:
   量化 perturbation effect 的大小。
```

当前 `D_corr` 更接近第二类：

```text
corrected effect size
```

它直接给出扣除 sample noise 后还剩多少 semantic drift。

如果要更严格贴合 proposal，最终分析中建议同时保留：

```text
D_corr
paired test p-value
Cohen's d
```

这样既有 corrected magnitude，也有显著性判断。

## 5. 当前实现和 proposal 的一个真实差异：embedding model

Proposal 的 4.5 Measurement Metrics 中写的是：

```text
The degree of semantic drift in model output will be measured as the cosine similarity between the original and perturbed outputs, computed using Sentence-BERT embeddings.
```

也就是说，proposal 明确指定：

```text
Sentence-BERT embeddings
```

而当前代码实现中使用的是：

```text
text-embedding-3-small
```

这个差异需要明确处理。

如果要严格按照 proposal，应该把当前 similarity 计算改成 Sentence-BERT，例如：

```text
all-MiniLM-L6-v2
all-mpnet-base-v2
```

如果继续使用 OpenAI embedding，也可以，但方法描述中不能继续写 Sentence-BERT，而应该改成：

```text
embedding-based cosine similarity
```

或者明确写：

```text
OpenAI text-embedding-3-small
```

## 6. Proposal metric 和 current operational metric 的关系

可以这样概括二者关系：

```text
Proposal metric:
semantic similarity between clean and perturbed outputs,
compared against a within-prompt noise baseline.

Current operational metric:
convert similarity to drift,
compute between-prompt drift,
subtract within-prompt sample-noise drift,
and report the remaining perturbation-specific drift.
```

换句话说：

```text
proposal: 定义研究思想和基础 similarity metric
current metric: 给出具体可执行的 corrected drift 公式
```

## 7. 是否需要修改当前方法

需要确认的不是 `Noise-Corrected Semantic Drift` 这个思路本身，而是两个实现细节：

### 7.1 是否使用 Sentence-BERT

如果目标是严格贴合 proposal：

```text
需要把 similarity embedding model 改成 Sentence-BERT。
```

如果目标是保持当前 API-based 实验便利性：

```text
可以继续用 text-embedding-3-small，
但 proposal 或论文方法部分需要改写，不能声称使用 Sentence-BERT。
```

### 7.2 是否补充显著性检验

如果要完整对应 proposal 4.6：

```text
需要在 D_corr 之外补充 paired tests 和 Cohen's d。
```

如果当前阶段只是做 RQ1 pilot 或方法验证：

```text
D_corr 可以先作为主 effect-size 指标。
```

## 最终判断

`Noise-Corrected Semantic Drift` 与 proposal 的 similarity 定义没有根本冲突。

它的作用是把 proposal 中较抽象的描述：

```text
compare post-perturbation similarity against noise baseline
```

具体化为一个可以直接计算、排序和画图的指标：

```text
D_corr = max(0, D_between - D_noise)
```

因此，它可以作为 proposal similarity metric 的 operationalized version。

但为了严格一致，后续需要决定：

```text
1. similarity embedding 是否改回 Sentence-BERT；
2. 是否在 D_corr 外补充 paired test 和 Cohen's d。
```

