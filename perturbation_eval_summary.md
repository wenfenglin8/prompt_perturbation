# LLM Prompt Perturbation 文献整理：扰动方式与输出评价准则

## 总表

| 文章 | 研究对象 | Perturbation 位置 | 扰动方式 | 扰动后评价输出准则 | 关键备注 |
|---|---|---|---|---|---|
| PromptRobust / PromptBench: *Towards Evaluating the Robustness of Large Language Models on Adversarial Prompts* | 9个LLM，8类任务，13个数据集 | prompt本身，不是sample | character-level、word-level、sentence-level、semantic-level；具体包括 TextBugger、DeepWordBug、BertAttack、TextFooler、StressTest、CheckList、semantic translation-style prompts | Performance Drop Rate, PDR；也做APDR聚合；此外做人类语义保持判断、attention visualization、transferability analysis | 核心是“对抗性prompt鲁棒性”；评价重点是准确率下降 |
| POSIX: *A Prompt Sensitivity Index for Large Language Models* | MMLU、Alpaca；8个开源LLM | prompt本身 | spelling errors、prompt template changes、paraphrasing/rewording；每个prompt生成60个intent-aligned variants，每类20个 | POSIX：同一response在原prompt与变体prompt下的log-likelihood相对变化；同时验证与response diversity、entropy、semantic coherence、confidence variance的关系 | 核心是“敏感性指标”，不是准确率；需要访问token概率 |
| *What Did I Do Wrong? Quantifying LLMs’ Sensitivity and Consistency to Prompt Engineering* | 文本分类任务 | prompt engineering / function calling schema / label descriptions / prompt rephrasings | 语义等价prompt rephrasing；还考察label definition、变量命名、label ordering等微小prompt变化；比较Simple、Detail、1-shot策略 | sensitivity：同一样本在Q个rephrasings下预测分布的熵/变化；consistency：同一类别不同样本的预测分布相似性；同时报告micro-F1 | 核心是黑盒分类诊断；temperature接近0以减少采样随机性 |
| *Enhancing LLM Robustness to Perturbed Instructions* | Llama 3、Flan-T5；CoLA、QNLI、SST-2 | task-level instruction，不是每条sample | DeepWordBug：character-level substitutions/insertions/deletions；TextFooler：基于counter-fitted GloVe的word replacements；使用TextAttack式greedy search最大化性能下降 | PDR：扰动instruction后的classification accuracy相对clean instruction下降；还用E5-Mistral embedding cosine similarity分析扰动语义偏移与PDR关系 | 核心是修复扰动instruction；比较self-denoising、PPL smoothing、instruction ensembling、representation alignment |
| *Within-Model vs Between-Prompt Variability in Large Language Models for Creative Tasks* | 12个LLM；AUT创造力任务；每个model×prompt生成100次 | prompt strategy / prompt variant | 1个baseline + 5种prompting strategies：one-shot、heuristic、anticipatory、zero-shot CoT、persona；再加4种minor changes：paraphrasing、formatting tweak、information order、random spelling errors | originality：AUT自动评分1–5；fluency：有效idea数量；linear mixed-effects variance decomposition，将总方差分解为model、prompt、model×prompt、within-LLM sampling variance | 核心不是传统扰动鲁棒性，而是证明sampling variance不可忽略；没有task correctness |

## 逐篇详细整理

### 1. PromptRobust / PromptBench

这篇文章把扰动加在prompt上，而不是加在具体输入样本sample上。作者认为一个prompt可能会被多个样本复用，因此prompt被扰动后可能导致一整批样本的输出都出错。

扰动方式分为四层：

1. Character-level：使用TextBugger和DeepWordBug，在单词内部加入拼写错误，例如添加、删除、重复、替换、交换字符。
2. Word-level：使用BertAttack和TextFooler，把词替换成同义词或上下文相近词。
3. Sentence-level：使用StressTest和CheckList，在prompt末尾追加无关句子或随机字符串，用来干扰模型注意力。
4. Semantic-level：模拟不同语言背景用户的表达方式，选取中文、法语、阿拉伯语、西班牙语、日语、韩语，先构造对应语言prompt，再翻译回英文，引入语言风格差异。

输出评价准则主要是Performance Drop Rate，PDR。它衡量扰动后模型在任务上的performance相对于clean prompt下降了多少。对于多个attack、prompt type、model、dataset，文章还使用APDR进行平均聚合。此外，作者还做人类评估，判断扰动prompt是否仍然语义保持；并用attention visualization解释为什么模型出错；还分析adversarial prompts在不同模型之间的transferability。

这篇文章对你的项目最重要的启发是：它提供了比较完整的prompt perturbation taxonomy，但它的扰动是adversarially searched，目标是最大化性能下降，不完全等同于普通用户自然改写。

### 2. POSIX

POSIX的目标不是直接测accuracy下降，而是提出一个prompt sensitivity index。它认为如果两个prompt意图相同，那么模型对同一response的生成概率不应该因为prompt表达方式变化而大幅改变。

扰动方式包括三类，每个原始prompt生成60个变体，每类20个：

1. Spelling Errors：随机选择1、2、4或8个tokens，并对其施加插入、删除、相邻字符交换、键盘邻近字母替换。
2. Prompt Templates：根据Sclar等人的template grammar设计20个不同模板，保持核心语义但改变prompt结构。
3. Paraphrases：用GPT-3.5-Turbo为每个原始prompt生成20个意图保持的改写。

评价准则是POSIX。它衡量的是：当prompt从x_i换成另一个intent-aligned prompt x_j时，模型对同一输出y的log-likelihood发生多大相对变化。POSIX不是accuracy指标，而是敏感性指标。文章还说明POSIX能够体现四个方面：response diversity、response distribution entropy、semantic coherence、variance in confidence。

这篇文章对你的项目的启发是：语义相似度本身不一定足够，因为两个输出字符串相同，模型内部的confidence/log-likelihood仍然可能变化。但POSIX需要token probability，所以对商业API不一定适用。

### 3. What Did I Do Wrong?

这篇文章关注黑盒分类任务中的prompt engineering问题。它不要求访问模型内部概率，也不只看accuracy，而是提出两个诊断指标：sensitivity和consistency。

扰动方式主要是语义等价prompt rephrasing。文章的动机来自软件开发中的function calling和schema构造：label description、变量命名、label顺序、是否加冠词等微小变化，都可能改变最终分类结果。实验中还比较Simple、Detail、1-shot等prompt策略，并在多个rephrased prompts下观察预测分布。

输出评价准则有三个：

1. Sensitivity：对同一样本，统计不同prompt rephrasings下预测类别分布的变化。如果预测分布越分散，sensitivity越高。
2. Consistency：对同一真实类别下的不同样本，比较它们在prompt rephrasings下的预测分布是否相似。如果同类样本行为差异大，consistency低。
3. Micro-F1：作为传统performance指标，和sensitivity/consistency并列报告。

这篇文章对你的项目的启发是：它把“correctness之外的稳定性”作为独立诊断指标，非常适合解释为什么accuracy高的模型仍然可能不可靠。但它主要限于classification tasks，并通过temperature接近0来避免采样随机性，因此没有处理non-zero temperature下的sampling noise。

### 4. Enhancing LLM Robustness to Perturbed Instructions

这篇文章研究的是task-level instructions被扰动后，如何提升模型鲁棒性。它不是扰动每条input sample，而是扰动固定的instruction template。

扰动方式有两类：

1. DeepWordBug：character-level perturbations，包括substitutions、insertions、deletions。
2. TextFooler：word-level perturbations，使用counter-fitted GloVe embeddings进行词替换。

扰动生成方式是TextAttack式greedy search。目标函数是最大化perturbed instruction造成的performance drop，同时要求stop words和class labels不能被扰动。

评价准则主要是PDR，即Performance Drop Rate。它衡量扰动instruction后的classification accuracy相对于clean instruction accuracy的下降比例。文章还使用E5-Mistral embedding计算clean instruction和perturbed instruction之间的cosine similarity，并分析semantic similarity与PDR之间的负相关关系。

这篇文章对你的项目的启发是：它明确说明了instruction-level perturbation可能导致整类任务失败，而且PDR公式可以直接借鉴到有标准答案的任务中。但它主要是classification tasks，不涉及开放式生成，也没有区分sampling noise。

### 5. Within-Model vs Between-Prompt Variability in Creative Tasks

这篇文章关注creative writing / divergent thinking任务中的输出方差来源。它的重点不是“扰动后是否错”，而是把prompt effect、model effect和within-model sampling variance分开。

prompt设计包括10种：

1. P1 baseline：直接要求列出plastic bottle的各种用途。
2. P2 one-shot example：加入一个例子。
3. P3 heuristic prompt：加入跨领域、发散思考等启发。
4. P4 anticipatory prompt：提示避免不想要的输出。
5. P5 zero-shot CoT：让模型step-by-step思考。
6. P6 persona prompt：让模型扮演最有创造力的人。
7. P7 paraphrasing：同义改写。
8. P8 formatting constraint：格式限制，例如不要标题或冒号。
9. P9 information order：改变信息呈现顺序。
10. P10 typo robustness：加入随机拼写错误。

输出评价准则有两类：

1. Originality：使用AUT自动评分系统，对每个idea给1–5分，response-level originality取所有有效idea的平均分。
2. Fluency：每个response中有效idea的数量。

分析方法是linear mixed-effects model / variance decomposition，将总方差分为model、prompt、model×prompt interaction、within-LLM sampling variance。文章最重要的结论是：within-LLM variance本身可达到10%–34%，因此单次生成会把sampling noise误认为prompt effect。

这篇文章对你的项目的启发是：如果你的实验使用temperature > 0，不能只比较一次原prompt输出和一次扰动prompt输出。必须对同一prompt重复生成，建立noise baseline，否则perturbation effect和sampling noise会混在一起。

## 对你的Proposal的直接建议

你的研究设计可以把这些文献分成三条线：

1. 扰动构造来源：主要参考PromptRobust和Enhancing LLM Robustness。前者给出character/word/sentence/semantic四层扰动taxonomy；后者强调instruction-level perturbation。
2. 稳定性评价来源：主要参考POSIX和What Did I Do Wrong。POSIX强调log-likelihood sensitivity；What Did I Do Wrong强调不依赖ground truth的sensitivity/consistency。
3. sampling noise控制来源：主要参考Within-Model vs Between-Prompt Variability。它说明同一prompt重复生成的随机性不可忽略。

你自己的方案可以这样定位：不是做adversarial attack，也不是只看classification accuracy，而是在自然prompt perturbation下，同时测semantic drift、task correctness，并用repeated sampling建立noise baseline。
