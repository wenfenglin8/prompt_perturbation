# Evaluation Criteria From Five References for Four-Task Study

## 核心结论

仔细对照 5 篇参考文献后，结论是：

```text
没有一篇文献里的完整 evaluation criterion 可以原封不动覆盖当前 4 类 task。
```

当前 4 类 task 是：

```text
factual QA
math reasoning
code generation
open-ended writing
```

最接近当前研究目标的是 `POSIX`，但完整 POSIX 也不适合直接照搬。

更合理的主评价准则是：

```text
POSIX 的 semantic coherence / response similarity 思想
+
Haase et al. 的 within-prompt sampling noise correction 思想
```

也就是：

```text
Noise-Corrected Semantic Drift
```

## 五篇参考文献逐篇判断

| Reference | 文献中的评价准则 | 是否适合当前 4 类 task | 判断 |
|---|---|---:|---|
| PromptRobust | PDR: Performance Drop Rate | 部分适合 | 适合 QA/math/code，不适合 open-ended writing |
| Enhancing LLM Robustness to Perturbed Instructions | PDR based on accuracy | 不适合作为主指标 | 只做 classification，不能覆盖 code/writing |
| POSIX | Prompt Sensitivity Index | 最接近 | 理论上覆盖 MCQ 和 open-ended，但完整 POSIX 依赖 log-likelihood |
| What Did I Do Wrong | sensitivity / consistency based on class distribution entropy | 不适合 | classification-only |
| Within-Model vs Between-Prompt Variability | variance decomposition: prompt vs model vs within-LLM variance | 适合做方法论依据 | 不是直接 evaluation score，但支持 sample-noise correction |

## 1. PromptRobust

`PromptRobust` 使用的核心评价准则是：

```text
PDR = 1 - performance(perturbed) / performance(clean)
```

即：

```text
Performance Drop Rate
```

它的优点是可以把不同任务中的 performance drop 归一化，使不同 dataset / model / perturbation 之间更容易比较。

但是它要求每个任务都有明确的 performance score。

对当前四类任务来说：

```text
factual QA: 可以使用
math reasoning: 可以使用
code generation: 可以使用
open-ended writing: 不适合
```

原因是 open-ended writing 没有稳定、客观、统一的 ground-truth correctness score。

因此：

```text
PDR 不适合作为四类 task 的统一主指标。
```

它更适合作为辅助指标，用于有客观评分标准的任务。

## 2. Enhancing LLM Robustness to Perturbed Instructions

这篇文献也使用 PDR，但它的 PDR 是基于 classification accuracy。

实验任务主要是：

```text
CoLA
QNLI
SST-2
```

也就是说，它关注的是 perturbed instruction 对 classification accuracy 的影响。

这个评价准则的问题是：

```text
classification accuracy 无法自然扩展到 code generation 和 open-ended writing。
```

因此，这篇文献的 PDR 可以支持 robustness evaluation 的思路，但不适合作为当前四类 task 的主评价准则。

## 3. POSIX

`POSIX` 是五篇中最接近当前研究目标的。

它明确指出，prompt sensitivity 不应该只看 performance / accuracy，还应该考虑：

```text
response diversity
response distribution entropy
semantic coherence
variance in confidence / log-likelihood
```

其中最适合当前研究的是：

```text
semantic coherence
```

POSIX 的核心思想之一是：

```text
对于 intent-aligned prompts，模型生成的 responses 应该保持语义一致。
```

这与当前 proposal 中的 semantic similarity 定义高度一致：

```text
semantic similarity between original and perturbed outputs
computed using embeddings
```

POSIX 也在实验中覆盖了：

```text
MMLU: MCQ-style tasks
Alpaca: open-ended generation
```

这说明它确实考虑了 open-ended generation。

但是，完整 POSIX 的核心依赖：

```text
P(y | x)
log-likelihood ratio
```

也就是要知道模型在不同 prompt 下生成同一 response 的 likelihood。

这在当前 API-based 实验和四任务设置中存在问题：

```text
1. commercial API 不一定稳定提供 logprobs；
2. 不同模型的 likelihood 可比性差；
3. code generation 和 long-form writing 中重新计算 response likelihood 成本高；
4. 该指标实现复杂度明显高于当前 proposal 所需。
```

因此：

```text
完整 POSIX 不建议直接照搬。
```

但 POSIX 的 semantic coherence / response similarity 维度非常适合作为当前主评价思想。

## 4. What Did I Do Wrong

这篇文献提出两个 diagnostic metrics：

```text
sensitivity
consistency
```

其中 sensitivity 是基于 prompt rephrasings 下 predicted class distribution 的 entropy。

consistency 是比较同一类别样本之间 predicted class distributions 的相似性。

这两个指标的问题是：

```text
它们是 classification-only。
```

文献自身也承认其限制：

```text
the proposed metrics work for classification problems only
```

因此，这套评价准则不适合当前四类 task，尤其不适合：

```text
math reasoning
code generation
open-ended writing
```

## 5. Within-Model vs Between-Prompt Variability

这篇文献的核心贡献不是提出一个适用于所有 task 的 direct evaluation score，而是证明：

```text
single-sample evaluation conflates prompt effects with sampling noise
```

它通过 repeated sampling 和 variance decomposition 区分：

```text
prompt effect
model effect
within-LLM sampling variance
```

这与当前 proposal 的核心思想一致：

```text
先估计同一个 prompt 多次生成时的 sample noise baseline，
再判断 clean-vs-perturbed 的变化是否超过该 baseline。
```

所以这篇文献最适合作为：

```text
sample-noise correction 的方法论依据。
```

但它不提供一个可以直接套用到 QA/math/code/writing 四类任务的统一 evaluation criterion。

## 为什么不能直接用 PDR 作为主指标

PDR 的定义是：

```text
PDR = 1 - performance(perturbed) / performance(clean)
```

它要求每个任务都有明确 performance score。

当前四类任务中：

```text
factual QA: 有 reference answer，可以算 EM/F1
math reasoning: 有 final answer，可以算 exact match
code generation: 有 unit tests，可以算 pass rate
open-ended writing: 没有 objective correctness
```

因此：

```text
PDR 不能作为四类 task 的统一主评价标准。
```

它更适合作为 RQ2 或辅助指标，用来分析：

```text
semantic drift 是否与 correctness change 有关联。
```

## 为什么不能直接用完整 POSIX

完整 POSIX 的优势是它不只看 accuracy，而是尝试衡量 prompt sensitivity 本身。

但它的核心计算需要：

```text
log-likelihood of responses under different prompt variants
```

也就是：

```text
P(y_i | x_j)
```

这对当前研究不理想：

```text
1. API 模型不一定提供完整 log-likelihood；
2. 不同模型之间 log-likelihood 可比性弱；
3. code generation 和 open-ended writing 的长输出会增加计算成本；
4. 当前 proposal 已经选择了 embedding-based semantic similarity，而不是 likelihood-based sensitivity。
```

所以完整 POSIX 不建议作为当前主指标。

## 最适合当前研究的参考组合

最合适的组合是：

```text
POSIX 的 semantic coherence / response similarity
+
Haase et al. 的 within-prompt sampling noise correction
```

具体对应到当前研究：

```text
1. 用 embedding cosine similarity 衡量 clean output 和 perturbed output 的语义相似度。
2. 用 repeated sampling 估计同一个 prompt 内部的 sample noise。
3. 从 clean-vs-perturbed drift 中扣除 within-prompt noise。
4. 得到 noise-corrected perturbation-specific semantic drift。
```

这就是：

```text
Noise-Corrected Semantic Drift
```

## 推荐的主评价准则

主 evaluation criterion：

```text
Noise-Corrected Semantic Drift
```

推荐表述：

```text
We use embedding-based semantic similarity as the core output-level sensitivity measure,
following the semantic coherence / response similarity motivation in POSIX,
and apply a repeated-sampling noise baseline motivated by Haase et al.
```

## 推荐的辅助评价准则

辅助 criterion：

```text
PDR / task correctness drop
```

仅用于有客观评分标准的任务：

```text
factual QA
math reasoning
code generation
```

不用于：

```text
open-ended writing
```

## 最终判断

最终评价准则应当写成：

```text
没有单篇 reference 的完整评价准则可以直接覆盖当前四类 task；
最合适的是以 POSIX 的 semantic coherence 为主评价思想，
用 Haase et al. 的 within-prompt variance correction 做 sample-noise correction；
PDR 只作为有标准答案任务的辅助 correctness 指标。
```

