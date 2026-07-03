# Perturbation 方案来源与代码实现说明

本文用于说明当前项目中的 perturbation 方案是如何从 5 篇参考文献中提炼出来的，以及这些方案在代码中是如何实现的。

## 总结

`project_perturbation_plan_by_task.md` 里的 5 类 perturbation 是基于参考文献提炼后的项目方案，不是 5 篇文献原封不动的方法实现。

更准确地说：

```text
参考文献提供 perturbation category 和 evaluation logic；
项目方案把这些 category 改造成适合四类任务的 natural prompt perturbations；
代码实现目前是轻量、手写、可控版本，而不是完整复现原论文攻击算法。
```

这样设计的原因是：本项目关注的是 natural prompt perturbation under repeated sampling，并比较 sample-noise correction 前后的估计差异，而不是复现 adversarial robustness benchmark。

## 已经在代码中实现并跑过的 perturbation

当前实现主要分布在以下脚本：

- `sample_noise_pilot.py`
- `four_task_similarity_sweep.py`
- `promptrobust_reference_pdr_eval.py`

| 实现名 | 代码中如何实现 | 文献依据 | 是否原样复现文献 |
|---|---|---|---|
| `character` / typo / surface noise | 用固定 replacement 字典把 instruction 里的词拼错，例如 `Read -> Raed`, `answer -> answr`, `question -> quesiton` | PromptRobust 的 TextBugger / DeepWordBug；POSIX spelling errors；Enhancing LLM Robustness 的 DeepWordBug | 不是原样复现。是简化版、手写规则版 |
| `word` | 按 task 替换成另一种 instruction wording，例如 factual QA 改成 `Review the provided passage...` | PromptRobust 的 word-level perturbation / TextFooler；POSIX rewording | 不是 TextFooler 自动同义词攻击，是人工改写 |
| `sentence` | 在 instruction 末尾追加一句无关说明，例如 `extra wording that is not relevant...` | PromptRobust sentence-level；StressTest / CheckList | 是同一类别的简化实现，不是完整 StressTest / CheckList |
| `semantic` | 按 task 替换成语义等价的新 instruction | PromptRobust semantic-level；POSIX intent-aligned variants | 不是翻译回译式 PromptRobust semantic attack，是手写语义改写 |
| `paraphrase` | 只改写 instruction，不改 sample body，例如 QA、Math、Code、Alpaca 都换一种任务说明 | POSIX paraphrase；What Did I Do Wrong rephrasing；Haase et al. paraphrasing | 是项目化手写 paraphrase，不是 GPT-3.5 批量生成 20 个 paraphrases |

## `project_perturbation_plan_by_task.md` 中的 5 类主扰动

`project_perturbation_plan_by_task.md` 提出了 5 类适合项目主实验的 perturbation：

| 项目方案 | 当前是否完整实现 | 说明 |
|---|---|---|
| P1 `Paraphrase` | 已实现并跑过 | `reference_four_task` 和 cross-task paraphrase 验证用的就是这个思路 |
| P2 `Format Change` | 方案中有，当前没有作为独立 perturbation 系统跑完整矩阵 | 一些 prompt 有格式变化，但还不是严格独立变量 |
| P3 `Information Reordering` | 方案中有，当前没有完整实现为独立 perturbation | 需要专门写函数控制 instruction / context / question 顺序 |
| P4 `Surface Noise` | 已实现 | 对应 typo / character perturbation |
| P5 `Context Injection` | 部分实现 | `sentence` perturbation 接近这个，但还没有按四类任务完整细化 |

## 每类 perturbation 与参考文献的关系

### 1. Paraphrase

来源：

- POSIX: paraphrasing / rewording
- What Did I Do Wrong: prompt rephrasing
- Haase et al.: minor prompt changes 中的 paraphrasing

项目实现：

- 手写 task-specific paraphrase。
- 只改写 instruction。
- 不改动 passage、math problem、function signature、examples、ground-truth-critical content。

实现性质：

```text
reference-derived category;
project-adapted implementation;
not exact paper reproduction.
```

### 2. Surface Noise / Character Perturbation

来源：

- PromptRobust: character-level perturbations, including TextBugger and DeepWordBug
- POSIX: spelling errors
- Enhancing LLM Robustness: DeepWordBug-style character perturbations
- Haase et al.: random spelling errors as minor prompt changes

项目实现：

- 使用固定 replacement 字典制造轻微拼写错误。
- 主要扰动 instruction。
- 避免扰动 factual passage、math numbers/formulas、code signature、examples。

实现性质：

```text
same perturbation family as prior work;
simplified controlled implementation;
not adversarial search.
```

### 3. Word-Level / Rewording

来源：

- PromptRobust: word-level methods such as TextFooler and BertAttack
- POSIX: rewording / intent-aligned variants

项目实现：

- 当前不是用 TextFooler 或 BertAttack 自动替换词。
- 而是按 task 手写新的 instruction wording。

原因：

- 自动同义词替换容易改变 math condition、QA evidence、code requirement。
- 对本项目来说，必须保证 task intent 和 ground truth 不变。

实现性质：

```text
inspired by word-level perturbation;
implemented as controlled instruction rewording;
not full TextFooler / BertAttack reproduction.
```

### 4. Sentence / Context Injection

来源：

- PromptRobust: sentence-level perturbation
- StressTest / CheckList: irrelevant sentence or distracting content

项目实现：

- 在 instruction 后追加无关但不矛盾的句子。
- 当前 `sentence` perturbation 接近 `Context Injection`，但还不是完整的四任务专门版本。

实现性质：

```text
same high-level idea as sentence-level perturbation;
implemented as a light irrelevant-sentence insertion;
not full StressTest / CheckList reproduction.
```

### 5. Semantic Perturbation

来源：

- PromptRobust: semantic-level perturbation, including translation-style prompts
- POSIX: intent-aligned prompt variants

项目实现：

- 手写语义等价 instruction。
- 没有实现多语言 prompt 或 translation-backtranslation pipeline。

实现性质：

```text
semantic-equivalent prompt variant;
project-adapted;
not PromptRobust translation-style reproduction.
```

### 6. Format Change

来源：

- Haase et al.: formatting tweak
- POSIX: prompt template changes
- What Did I Do Wrong: schema / prompt engineering expression changes

项目状态：

- 已经在方案中定义为 P2。
- 当前没有作为独立 perturbation 完整实现并跑主矩阵。

需要补充的实现：

```text
same instruction and same sample;
only change layout, labels, bullet points, numbering, or output-format wording;
do not add or remove task requirements.
```

### 7. Information Reordering

来源：

- Haase et al.: information order minor change
- POSIX: template variation

项目状态：

- 已经在方案中定义为 P3。
- 当前没有作为独立 perturbation 完整实现并跑主矩阵。

需要补充的实现：

```text
move instruction / constraints / context / question order;
keep content identical or semantically equivalent;
avoid changing math problem internals or code signatures.
```

## 为什么没有直接复现原论文攻击算法

PromptRobust 和 Enhancing LLM Robustness 中的一些 perturbation 是 adversarial attack，目标是通过 greedy search 或 attack algorithm 最大化 performance drop。

本项目的目标不同：

```text
不是 adversarial attack benchmark；
而是研究自然 prompt 扰动下，single-generation evaluation 是否会把 sample noise 误当成 perturbation effect。
```

因此，当前实现故意采用更可控的 instruction-level perturbation：

1. 保持 task sample 不变。
2. 保持 ground truth 不变。
3. 每种 perturbation 单独评估。
4. 对 clean 和 perturbed prompt 都 repeated sampling。
5. 比较 raw drift / PDR 和 sample-noise-corrected estimate。

## 推荐写进论文或 proposal 的表述

```text
The perturbation categories are derived from prior work, but implemented as controlled, task-preserving prompt variants rather than full adversarial attacks. This design is intentional because the study focuses on natural prompt sensitivity and sample-noise correction, not adversarial robustness benchmarking.
```

中文解释：

```text
本项目的扰动类别来自参考文献，但具体实现是面向本项目四类任务重新设计的受控 prompt 变体。它们不是对原论文 adversarial attack 方法的完整复现，而是为了保证 task sample 和 ground truth 不变，从而比较 single-generation evaluation 与 repeated-sampling / sample-noise-corrected evaluation 的差异。
```

