# Prompt Perturbation 文献整理：扰动方式与扰动后评价输出准则

本文整理 5 篇参考文献中使用的 prompt / instruction perturbation 方法，以及扰动后采用的输出评价准则。重点关注两个问题：

1. 每篇文章把扰动加在哪里。
2. 扰动后如何评价模型输出或模型行为变化。

## 总表

| 文献 | 扰动对象 / 位置 | Perturbation 方式 | 扰动生成方式 | 扰动后评价输出准则 | 评价重点 |
|---|---|---|---|---|---|
| PromptRobust / PromptBench: *Towards Evaluating the Robustness of Large Language Models on Adversarial Prompts* | Prompt 本身，而不是每条 input sample | Character-level、word-level、sentence-level、semantic-level perturbations。具体包括 TextBugger、DeepWordBug、BertAttack、TextFooler、StressTest、CheckList、translation-style semantic prompts | 多数方法来自 adversarial attack 工具或已有攻击算法；目标是构造会降低模型表现的 adversarial prompts | Performance Drop Rate (PDR)、Average PDR (APDR)、人类语义保持判断、attention visualization、transferability analysis | 主要看扰动 prompt 后任务性能下降多少，核心是 adversarial prompt robustness |
| POSIX: *A Prompt Sensitivity Index for Large Language Models* | Prompt 本身 | Spelling errors、prompt template changes、paraphrasing / rewording。每个原始 prompt 生成 60 个 intent-aligned variants，每类 20 个 | 拼写错误通过字符级随机操作生成；模板变化基于 template grammar；paraphrases 由 GPT-3.5-Turbo 生成 | POSIX：同一 response 在原 prompt 与变体 prompt 下的 log-likelihood 相对变化；同时分析 response diversity、entropy、semantic coherence、confidence variance | 主要衡量 prompt sensitivity，不直接等同于 accuracy 或 correctness |
| *What Did I Do Wrong? Quantifying LLMs' Sensitivity and Consistency to Prompt Engineering* | Prompt engineering 表达，包括 prompt rephrasing、function calling schema、label description、变量命名、label ordering | 语义等价 prompt rephrasing；label 定义变化；变量名变化；label 顺序变化；prompt 策略变化，如 Simple、Detail、1-shot | 构造多个语义上等价或近似等价的 prompt variants，观察同一任务在不同 prompt 下的预测分布 | Sensitivity、Consistency、Micro-F1。Sensitivity 衡量同一样本在多个 prompt 下预测分布是否分散；Consistency 衡量同一真实类别下不同样本的预测分布是否一致 | 主要做黑盒分类诊断，强调 correctness 之外的稳定性 |
| *Enhancing LLM Robustness to Perturbed Instructions* | Task-level instruction template，而不是每条 sample | DeepWordBug character-level perturbations，包括 substitution、insertion、deletion；TextFooler word-level replacements，基于 counter-fitted GloVe embeddings | 使用 TextAttack 风格 greedy search，寻找能最大化 performance drop 的 instruction perturbation；通常避免扰动 stop words 和 class labels | Performance Drop Rate (PDR)；clean instruction 与 perturbed instruction 的 embedding cosine similarity；分析 semantic similarity 与 PDR 的关系 | 主要看 instruction-level perturbation 对分类准确率的破坏，以及如何提升鲁棒性 |
| *Within-Model vs Between-Prompt Variability in Large Language Models for Creative Tasks* | Prompt strategy / prompt variant | Baseline、one-shot、heuristic、anticipatory、zero-shot CoT、persona；minor prompt changes 包括 paraphrasing、formatting tweak、information order、random spelling errors | 为 AUT 创造力任务设计多个 prompt strategies 和 minor variants；每个 model-prompt 组合重复生成多次 | Originality、Fluency、linear mixed-effects variance decomposition。将方差分解为 model effect、prompt effect、model-prompt interaction、within-LLM sampling variance | 重点不是 correctness，而是区分 prompt effect 与 sampling noise |

## 逐篇详细整理

### 1. PromptRobust / PromptBench

**扰动位置**

这篇文章把 perturbation 加在 prompt 本身上，而不是加在具体 input sample 上。其基本假设是：一个 prompt 往往会被多个样本复用，因此 prompt 被扰动后，可能导致一整批样本的输出同时退化。

**扰动方式**

文章将 prompt perturbation 分成四个层级：

| 层级 | 具体方法 | 含义 |
|---|---|---|
| Character-level | TextBugger、DeepWordBug | 在单词内部加入字符级错误，例如插入、删除、重复、替换、交换字符 |
| Word-level | BertAttack、TextFooler | 将 prompt 中的词替换为同义词、上下文相近词或模型认为相近的替代词 |
| Sentence-level | StressTest、CheckList | 在 prompt 末尾追加无关句子、随机字符串或干扰性内容 |
| Semantic-level | Translation-style prompts | 模拟不同语言背景用户的表达方式，例如先用中文、法语、阿拉伯语、西班牙语、日语、韩语构造 prompt，再翻译回英文，引入语义保持但表达风格不同的 prompt |

**扰动生成策略**

这些扰动大多带有 adversarial attack 色彩，目标不是模拟普通随机噪声，而是构造能够显著降低模型表现的 prompt variants。因此，它更接近 adversarial prompt robustness evaluation。

**扰动后评价输出准则**

主要评价指标是 **Performance Drop Rate (PDR)**。它衡量扰动后模型表现相对于 clean prompt 下表现下降的比例。一般形式可以理解为：

```text
PDR = (Performance_clean - Performance_perturbed) / Performance_clean
```

当比较多个 attack、prompt type、model 或 dataset 时，文章还使用 **Average Performance Drop Rate (APDR)** 做聚合。

除 PDR / APDR 外，文章还使用了辅助评价：

| 评价项 | 作用 |
|---|---|
| Human evaluation | 判断扰动后的 prompt 是否仍然保持原始语义 |
| Attention visualization | 分析模型为什么在扰动 prompt 下出错 |
| Transferability analysis | 分析 adversarial prompts 是否能在不同模型之间迁移 |

**总结**

这篇文章提供了最完整的 prompt perturbation taxonomy，但其扰动偏 adversarial，目标是最大化性能下降。因此，如果研究目标是自然用户扰动，需要借鉴其分类体系，但不一定直接采用其攻击式生成方式。

### 2. POSIX: A Prompt Sensitivity Index for Large Language Models

**扰动位置**

POSIX 也是扰动 prompt 本身。它关心的是：如果两个 prompt 意图相同，模型对同一 response 的生成概率是否应该保持稳定。

**扰动方式**

POSIX 为每个原始 prompt 构造 60 个 intent-aligned variants，分为三类，每类 20 个：

| 类型 | 具体扰动方式 | 目的 |
|---|---|---|
| Spelling errors | 随机选择 1、2、4 或 8 个 tokens，并施加插入、删除、相邻字符交换、键盘邻近字母替换 | 模拟拼写错误或输入错误 |
| Prompt templates | 根据 template grammar 构造不同 prompt 模板 | 保持核心语义，但改变 prompt 结构 |
| Paraphrases / rewording | 使用 GPT-3.5-Turbo 生成语义保持的改写 | 模拟用户自然改写 |

**扰动生成策略**

POSIX 的 perturbations 强调 **intent-aligned**，即 prompt 变体应该保持与原 prompt 相同的任务意图。它不是为了最大化 accuracy drop，而是为了测试模型对表达变化的敏感程度。

**扰动后评价输出准则**

核心指标是 **POSIX**。它衡量同一个 response `y` 在原 prompt `x_i` 和变体 prompt `x_j` 下的 log-likelihood 相对变化。

也就是说，即使两个 prompt 语义等价，如果模型对同一个输出的概率估计发生明显变化，那么模型就被认为对 prompt 表达较敏感。

POSIX 的重点不是判断答案是否正确，而是衡量模型内部概率分布是否稳定。文章还进一步分析 POSIX 与以下现象的关系：

| 辅助分析项 | 含义 |
|---|---|
| Response diversity | prompt 变化是否导致输出内容更多样 |
| Response distribution entropy | 输出分布是否变得更分散 |
| Semantic coherence | 输出语义是否仍然连贯 |
| Confidence variance | 模型置信度是否随 prompt 改写发生波动 |

**总结**

POSIX 的重要贡献是把 prompt sensitivity 定义为概率层面的稳定性，而不是简单看输出字符串或准确率。但它需要访问 token probability / log-likelihood，因此对只返回文本的商业 API 不一定适用。

### 3. What Did I Do Wrong? Quantifying LLMs' Sensitivity and Consistency to Prompt Engineering

**扰动位置**

这篇文章研究的是 prompt engineering 过程中的微小变化，主要包括：

| 扰动位置 | 示例 |
|---|---|
| Prompt rephrasing | 语义等价改写 |
| Function calling schema | schema 表达方式变化 |
| Label description | 类别说明文字变化 |
| Variable naming | 变量名变化 |
| Label ordering | 标签顺序变化 |
| Prompting strategy | Simple、Detail、1-shot 等策略差异 |

**扰动方式**

文章主要使用语义等价或近似语义等价的 prompt variants。其核心观察是：即使 prompt 表面上只发生很小变化，例如 label 顺序改变、变量名改变、类别描述换一种说法，模型最终分类结果也可能发生变化。

**扰动生成策略**

这篇文章不强调 adversarial search，也不要求访问模型内部概率。它更接近黑盒诊断：构造多种 prompt rephrasings，然后观察模型预测分布如何变化。

**扰动后评价输出准则**

文章主要提出三个评价准则：

| 指标 | 评价对象 | 含义 |
|---|---|---|
| Sensitivity | 同一个样本在多个 prompt rephrasings 下的预测分布 | 如果同一样本在不同 prompt 下预测类别很分散，则 sensitivity 高 |
| Consistency | 同一真实类别中不同样本的预测分布 | 如果同类样本在 prompt variations 下行为相似，则 consistency 高；如果差异大，则 consistency 低 |
| Micro-F1 | 分类任务最终表现 | 作为传统 performance 指标，与 sensitivity / consistency 并列报告 |

Sensitivity 的思想是：对同一个 input sample，收集它在多个 prompt variants 下的预测结果。如果预测结果集中在同一类别，说明模型对 prompt 改写不敏感；如果分布很分散，说明模型对 prompt 表达高度敏感。

Consistency 的思想是：同一真实类别的样本，在 prompt variants 下应该表现出相似的预测分布。如果同类样本的预测行为差异很大，说明模型虽然可能在某些样本上答对，但其类别判断机制不稳定。

**总结**

这篇文章非常适合支持“accuracy 之外还需要稳定性指标”的论点。它的优势是黑盒可用，不依赖 token log-likelihood；局限是主要面向 classification tasks，并且实验中通常将 temperature 设得接近 0，以减少 sampling randomness。

### 4. Enhancing LLM Robustness to Perturbed Instructions

**扰动位置**

这篇文章扰动的是 **task-level instruction**，不是每条 input sample。也就是说，它关注固定 instruction template 被破坏后，整个任务表现是否下降。

**扰动方式**

文章主要使用两类扰动：

| 类型 | 方法 | 具体操作 |
|---|---|---|
| Character-level | DeepWordBug | 对 instruction 中的字符做 substitution、insertion、deletion 等操作 |
| Word-level | TextFooler | 使用 counter-fitted GloVe embeddings 进行 word replacement |

**扰动生成策略**

扰动生成采用 TextAttack 风格的 greedy search。目标是寻找能够最大化 performance drop 的 perturbed instruction。同时，为了避免破坏任务定义本身，通常限制某些内容不能被扰动，例如 stop words 和 class labels。

**扰动后评价输出准则**

主要指标是 **Performance Drop Rate (PDR)**。它衡量 perturbed instruction 下的 classification accuracy 相对于 clean instruction 下 accuracy 的下降比例：

```text
PDR = (Accuracy_clean - Accuracy_perturbed) / Accuracy_clean
```

文章还使用 embedding similarity 做语义分析：

| 指标 / 分析 | 含义 |
|---|---|
| E5-Mistral embedding cosine similarity | 计算 clean instruction 与 perturbed instruction 的语义相似度 |
| Similarity-PDR relationship | 分析语义相似度与 performance drop 之间的关系 |

**总结**

这篇文章说明 instruction-level perturbation 会导致整类任务退化。它的 PDR 公式非常适合借鉴到有标准答案或可自动评分的任务中。但它同样偏向 classification setting，对开放式生成任务的评价覆盖不足。

### 5. Within-Model vs Between-Prompt Variability in Large Language Models for Creative Tasks

**扰动位置**

这篇文章研究的是 creative tasks 中 prompt strategy 和 prompt variant 对输出差异的影响。它不把 perturbation 仅仅理解为错误或攻击，而是把不同 prompt 表达、策略和轻微变动都视为输出方差来源。

**扰动方式**

文章在 Alternative Uses Task (AUT) 创造力任务中设计了多种 prompt：

| 编号 | Prompt 类型 | 含义 |
|---|---|---|
| P1 | Baseline | 直接要求列出 plastic bottle 的各种用途 |
| P2 | One-shot example | 加入一个示例 |
| P3 | Heuristic prompt | 加入跨领域、发散思考等启发 |
| P4 | Anticipatory prompt | 提示避免不想要的输出 |
| P5 | Zero-shot CoT | 要求模型 step-by-step thinking |
| P6 | Persona prompt | 要求模型扮演有创造力的人 |
| P7 | Paraphrasing | 对 prompt 进行同义改写 |
| P8 | Formatting constraint | 改变格式要求，例如不要标题或冒号 |
| P9 | Information order | 改变信息呈现顺序 |
| P10 | Typo robustness | 加入随机拼写错误 |

**扰动生成策略**

这篇文章不使用 adversarial search，而是系统设计 prompt strategies 和 minor prompt changes。关键实验设计是：每个 model-prompt 组合重复生成多次，例如 100 次，从而估计 sampling noise。

**扰动后评价输出准则**

文章主要使用两个输出质量指标：

| 指标 | 含义 |
|---|---|
| Originality | 使用 AUT 自动评分系统，对每个 idea 评分，response-level originality 取有效 ideas 的平均分 |
| Fluency | 每个 response 中有效 idea 的数量 |

此外，文章最重要的分析方法是 **linear mixed-effects model / variance decomposition**，将总方差分解为：

| 方差来源 | 含义 |
|---|---|
| Model effect | 不同模型本身导致的差异 |
| Prompt effect | 不同 prompt 导致的差异 |
| Model-prompt interaction | 不同模型对不同 prompt 的响应方式不同 |
| Within-LLM sampling variance | 同一模型、同一 prompt 多次生成造成的随机波动 |

**总结**

这篇文章的重点不是扰动后模型是否答错，而是证明在 creative / open-ended generation 中，sampling variance 不能忽略。如果实验使用 non-zero temperature，只比较一次 clean prompt 输出和一次 perturbed prompt 输出是不可靠的，因为 observed difference 可能来自 sampling noise，而不是 prompt perturbation 本身。

## 对当前研究设计的直接启发

综合这 5 篇文章，可以将你的研究设计定位为：

> 在自然 prompt perturbation 下，同时评估 semantic drift、task correctness 和 output stability，并通过 repeated sampling 建立 sampling noise baseline。

具体来说：

1. **扰动构造**可以借鉴 PromptRobust 的四层 taxonomy：character、word、sentence、semantic，但不必采用完全 adversarial search。
2. **instruction-level perturbation**可以借鉴 *Enhancing LLM Robustness to Perturbed Instructions*，因为 instruction 被扰动会影响整批样本。
3. **稳定性评价**可以借鉴 POSIX 和 *What Did I Do Wrong?*。如果能拿到 token probability，可以考虑 POSIX；如果只能黑盒访问模型，则 sensitivity / consistency 更实用。
4. **有标准答案的任务**可以报告 correctness、accuracy、F1 或 PDR。
5. **开放式生成任务**需要报告 semantic drift、输出质量变化，以及 repeated sampling 下的 noise baseline。
6. **如果 temperature > 0**，必须对 clean prompt 和 perturbed prompt 都重复采样，否则无法区分 perturbation effect 和 sampling noise。

## 可直接采用的分类框架

| 维度 | 推荐选择 | 对应参考文献 |
|---|---|---|
| Perturbation taxonomy | Character、word、sentence、semantic | PromptRobust / PromptBench |
| Instruction-level perturbation | 扰动 task instruction template | Enhancing LLM Robustness |
| Natural rephrasing | Paraphrase、template change、format change、information order change | POSIX；What Did I Do Wrong；Within-Model vs Between-Prompt Variability |
| Correctness evaluation | Accuracy、Micro-F1、PDR | PromptRobust；Enhancing LLM Robustness；What Did I Do Wrong |
| Stability evaluation | Sensitivity、consistency、POSIX | POSIX；What Did I Do Wrong |
| Open-ended output evaluation | Originality、fluency、semantic drift | Within-Model vs Between-Prompt Variability |
| Sampling noise control | Repeated sampling and variance decomposition | Within-Model vs Between-Prompt Variability |
