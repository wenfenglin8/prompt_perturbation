# Why This Project Uses a Reference-Informed Perturbation Implementation

This note explains why the current experiments do not directly use one official
reference-paper perturbation pipeline, and why the current perturbations should
be described as **reference-informed** or **literature-aligned**, not as an
exact reproduction of a single paper.

## Short Answer

The perturbation categories are aligned with ideas from the reference
literature, but the concrete perturbation-generation procedure is implemented
inside this project.

This is because no single official reference implementation covers all of the
following at once:

```text
factual QA
math reasoning
code generation
open-ended writing
same perturbation taxonomy
same model and decoding parameters
repeated sampling
sample-noise correction
PDR and semantic-drift analysis
```

Therefore, the current project uses a unified perturbation implementation so
that the comparison remains controlled across tasks.

## Main Difficulties

### 1. Task Coverage Does Not Match Exactly

PromptRobust / PromptBench aligns well with:

```text
SQuAD V2
MATH / Mathematics
classification / QA / reasoning tasks
```

However, the current project studies four task types:

```text
factual QA
math reasoning
code generation
open-ended writing
```

The code-generation and open-ended writing parts require:

```text
HumanEval
Alpaca
```

These are not fully covered by the PromptRobust / PromptBench setup. HumanEval
is an external supplement, and Alpaca is better aligned with POSIX than with
PromptRobust.

### 2. Official Pipelines May Target Adversarial Robustness

PromptRobust-style methods are closer to robustness or adversarial prompt
attack evaluation.

The current project focuses on natural prompt variation:

```text
non-adversarial perturbation
everyday instruction variation
instruction-only perturbation
```

Using a full adversarial attack pipeline would shift the research question from:

```text
How much observed drift under natural prompt variation remains after accounting for sample noise?
```

to:

```text
How robust is the model under adversarial prompt attacks?
```

Those are related but not identical questions.

### 3. The Reference Papers Do Not Share One Unified Perturbation Scheme

The project draws on several references:

```text
PromptRobust / PromptBench
POSIX
Haase et al.
Enhancing LLM Robustness to Perturbed Instructions
What Did I Do Wrong?
```

These papers use different datasets, metrics, and perturbation designs. There
is no single official implementation that provides:

```text
SQuAD V2 + MATH + HumanEval + Alpaca
same perturbation taxonomy
same repeated-sampling design
same sample-noise correction logic
same output format
```

For an apple-to-apple comparison, the project needs a unified implementation.

### 4. POSIX Is Not Directly Reproduced

POSIX is highly relevant because it emphasizes prompt sensitivity, semantic
coherence, and open-ended generation. However, the full POSIX method relies on
likelihood-based quantities such as:

```text
P(y | x)
log-likelihood ratios
```

This is difficult to apply directly in the current API-based, multi-task,
long-output setting:

```text
commercial APIs may not provide stable full log-likelihoods
long code and writing outputs make likelihood computation expensive
log-likelihood values are harder to compare across models
the proposal already uses embedding-based semantic similarity
```

Therefore, the project uses POSIX mainly for its semantic coherence / response
similarity motivation, not as a full POSIX reproduction.

### 5. Sample-Noise Correction Is a Project-Specific Combination

Haase et al. provide the key methodological motivation for repeated sampling
and within-LLM variability:

```text
single-sample comparisons can conflate prompt effects with ordinary sampling noise
```

However, Haase et al. do not provide a complete prompt-perturbation benchmark
for the current four tasks.

The current project combines:

```text
prompt perturbation evaluation
repeated sampling
within-prompt sample-noise baseline
noise-corrected semantic drift
PDR-style auxiliary correctness validation
```

This combined pipeline is not available as a single official reference
implementation.

## Current Perturbation Implementation

The current project implements five perturbation types:

```text
paraphrase
reordering
formatting
context_injection
surface_noise
```

They are implemented in:

```text
reference_perturbations.py
```

The implementation is project-specific:

| perturbation | implementation | reference motivation |
|---|---|---|
| paraphrase | LLM-generated intent-preserving rewrite | PromptRobust / PromptBench prompt rephrasing; POSIX intent-aligned variants |
| reordering | LLM-generated clause/order rewrite | PromptRobust-style information-order perturbation |
| formatting | `Question: ... Answer:` wrapper | POSIX-style template variation |
| context_injection | appends irrelevant context such as `and false is not true` | PromptRobust-style irrelevant-context perturbation |
| surface_noise | deterministic typo / character noise on non-essential instruction words | PromptRobust typo/noise perturbation; typo robustness motivation |

## Recommended Wording

Use:

```text
The perturbation categories are motivated by and aligned with the reference literature,
but the concrete perturbation generation algorithms are project-specific implementations.
```

or:

```text
The study implements a unified reference-informed natural perturbation scheme based on
perturbation categories discussed in PromptRobust / PromptBench and POSIX, while using
Haase et al.'s repeated-sampling insight for sample-noise correction.
```

Avoid:

```text
We exactly reproduce PromptRobust's perturbation algorithm.
```

Avoid:

```text
All datasets and perturbations come directly from one reference paper.
```

## Possible Future Improvement

To make the project more reference-faithful, a supplementary experiment could
be added on a narrower subset:

```text
SQuAD V2 + MATH only
PromptRobust / PromptBench-style perturbation settings
PDR evaluation
repeated sampling for sample-noise-aware comparison
```

This would not replace the four-task experiment, but it would provide a more
direct reference-faithful validation subset.

---

# 为什么本项目使用参考文献启发的扰动实现

本文说明为什么当前实验没有直接使用某一篇参考文献的官方
prompt perturbation pipeline，以及为什么当前扰动方式应表述为
**reference-informed** 或 **literature-aligned**，而不是某一篇论文的
完全复现。

## 简短回答

当前扰动类别与参考文献中的思想是对齐的，但具体的扰动生成过程是在本项目
内部自行实现的。

原因是，没有任何一个官方参考实现可以同时覆盖以下所有要求：

```text
factual QA
math reasoning
code generation
open-ended writing
same perturbation taxonomy
same model and decoding parameters
repeated sampling
sample-noise correction
PDR and semantic-drift analysis
```

因此，当前项目使用统一的扰动实现，以保证不同任务之间的比较条件受控。

## 主要困难

### 1. 任务覆盖并不完全匹配

PromptRobust / PromptBench 与以下任务较好对齐：

```text
SQuAD V2
MATH / Mathematics
classification / QA / reasoning tasks
```

但是，当前项目研究四类任务：

```text
factual QA
math reasoning
code generation
open-ended writing
```

其中 code generation 和 open-ended writing 分别需要：

```text
HumanEval
Alpaca
```

这些并没有被 PromptRobust / PromptBench 设置完整覆盖。HumanEval 是外部补充
数据集，而 Alpaca 相比 PromptRobust 更接近 POSIX 的 open-ended /
instruction-following 设置。

### 2. 官方 pipeline 可能更偏 adversarial robustness

PromptRobust-style 方法更接近 robustness 或 adversarial prompt attack
evaluation。

当前项目关注的是自然 prompt variation：

```text
non-adversarial perturbation
everyday instruction variation
instruction-only perturbation
```

如果直接使用完整的 adversarial attack pipeline，研究问题会从：

```text
How much observed drift under natural prompt variation remains after accounting for sample noise?
```

变成：

```text
How robust is the model under adversarial prompt attacks?
```

这两个问题相关，但并不相同。

### 3. 参考文献之间没有统一的扰动方案

本项目参考了多篇文献：

```text
PromptRobust / PromptBench
POSIX
Haase et al.
Enhancing LLM Robustness to Perturbed Instructions
What Did I Do Wrong?
```

这些论文使用的数据集、指标和扰动设计都不一样。没有一个官方实现可以提供：

```text
SQuAD V2 + MATH + HumanEval + Alpaca
same perturbation taxonomy
same repeated-sampling design
same sample-noise correction logic
same output format
```

为了做 apple-to-apple comparison，本项目需要一个统一实现。

### 4. 没有直接复现完整 POSIX

POSIX 与本项目高度相关，因为它强调 prompt sensitivity、semantic coherence
和 open-ended generation。但是，完整 POSIX 方法依赖 likelihood-based
quantities，例如：

```text
P(y | x)
log-likelihood ratios
```

这很难直接应用到当前基于 API 的、多任务、长输出实验设置中：

```text
commercial APIs may not provide stable full log-likelihoods
long code and writing outputs make likelihood computation expensive
log-likelihood values are harder to compare across models
the proposal already uses embedding-based semantic similarity
```

因此，本项目主要借用了 POSIX 的 semantic coherence / response similarity
动机，而不是完整复现 POSIX。

### 5. Sample-noise correction 是本项目的组合式扩展

Haase et al. 为 repeated sampling 和 within-LLM variability 提供了关键方法论
动机：

```text
single-sample comparisons can conflate prompt effects with ordinary sampling noise
```

但是，Haase et al. 并没有为当前四类任务提供完整的 prompt-perturbation
benchmark。

当前项目组合了：

```text
prompt perturbation evaluation
repeated sampling
within-prompt sample-noise baseline
noise-corrected semantic drift
PDR-style auxiliary correctness validation
```

这一组合 pipeline 并不存在于任何一个官方参考实现中。

## 当前扰动实现

当前项目实现了五类 perturbation：

```text
paraphrase
reordering
formatting
context_injection
surface_noise
```

它们实现于：

```text
reference_perturbations.py
```

具体实现是项目自行实现的：

| perturbation | implementation | reference motivation |
|---|---|---|
| paraphrase | LLM 生成的 intent-preserving rewrite | PromptRobust / PromptBench prompt rephrasing；POSIX intent-aligned variants |
| reordering | LLM 生成的 clause/order rewrite | PromptRobust-style information-order perturbation |
| formatting | `Question: ... Answer:` 模板包装 | POSIX-style template variation |
| context_injection | 添加无关上下文，例如 `and false is not true` | PromptRobust-style irrelevant-context perturbation |
| surface_noise | 对非关键 instruction words 施加确定性的 typo / character noise | PromptRobust typo/noise perturbation；typo robustness motivation |

## 推荐表述

可以使用：

```text
The perturbation categories are motivated by and aligned with the reference literature,
but the concrete perturbation generation algorithms are project-specific implementations.
```

或者：

```text
The study implements a unified reference-informed natural perturbation scheme based on
perturbation categories discussed in PromptRobust / PromptBench and POSIX, while using
Haase et al.'s repeated-sampling insight for sample-noise correction.
```

应避免：

```text
We exactly reproduce PromptRobust's perturbation algorithm.
```

也应避免：

```text
All datasets and perturbations come directly from one reference paper.
```

## 可能的后续改进

为了让项目更接近 reference-faithful，可以在更窄的任务子集上增加一个补充实验：

```text
SQuAD V2 + MATH only
PromptRobust / PromptBench-style perturbation settings
PDR evaluation
repeated sampling for sample-noise-aware comparison
```

这个补充实验不会替代四任务实验，但可以提供一个更直接、更加忠实参考文献的
validation subset。
