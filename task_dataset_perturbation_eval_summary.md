# 四类任务的数据集、扰动方式与评价准则汇总

本文基于以下项目文件整理：

- `project_perturbation_plan_by_task.md`
- `reference_based_eval_criteria_by_task.md`
- `dataset_selection_for_noise_correction_comparison.md`
- `cross_task_paraphrase_noise_correction.md`

目标是明确四类任务在 cross-task prompt perturbation 验证中的设置：

```text
任务 / 数据集 / 数据集来源 / 扰动方式 / 评价准则 / 评价准则来源 / sample noise correction / uncorrection
```

## 总表

| 任务 | 数据集 | 数据集来源 | 扰动方式 | 评价准则 | 评价准则来源 | Uncorrection | Sample noise correction |
|---|---|---|---|---|---|---|---|
| Factual QA | SQuAD V2 | PromptRobust / PromptBench | Paraphrasing / instruction rewording | 当前验证：similarity / semantic drift；应接入：answer correctness based PDR | Semantic drift / sensitivity: POSIX, What Did I Do Wrong, Haase et al.; PDR: PromptRobust, Enhancing LLM Robustness | 单次 clean output 与单次 perturbed output 比较 drift；或 single-sample correctness drop | 对 clean / perturbed prompt 分别重复生成，估计 within-prompt sample noise，再计算 `raw drift - noise baseline`；correctness 可用 repeated mean correctness 计算 PDR |
| Math reasoning | MATH / Mathematics | PromptRobust / PromptBench | Paraphrasing / instruction rewording | 当前验证：similarity / semantic drift；应接入：final-answer correctness based PDR | Semantic drift / sensitivity: POSIX, What Did I Do Wrong, Haase et al.; PDR: PromptRobust, Enhancing LLM Robustness | 单次 clean output 与单次 perturbed output 比较 drift；或 single-sample final-answer correctness drop | 对 clean / perturbed prompt 分别重复生成，估计 within-prompt sample noise，再计算 `raw drift - noise baseline`；correctness 可用 repeated final-answer accuracy 计算 PDR |
| Code generation | HumanEval | 外部补充，因为 5 篇参考文献没有 code generation 数据集 | Paraphrasing / instruction rewording | 当前验证：similarity / semantic drift；应接入：unit-test pass rate based PDR | PDR framework: PromptRobust, Enhancing LLM Robustness; sensitivity / consistency: What Did I Do Wrong; sample variance: Haase et al. | 单次 clean code 与单次 perturbed code 比较 drift；或 single-sample pass/fail difference | 对 clean / perturbed prompt 分别重复生成，估计 within-prompt sample noise，再计算 `raw drift - noise baseline`；correctness 可用 repeated unit-test pass rate 计算 PDR |
| Open-ended writing | Alpaca | POSIX | Paraphrasing / instruction rewording | 当前验证：similarity / semantic drift；可接入：semantic coherence, response diversity, fluency | Semantic coherence / response diversity: POSIX; originality / fluency and within-LLM variance: Haase et al.; sensitivity: What Did I Do Wrong | 单次 clean output 与单次 perturbed output 比较 semantic drift / coherence / fluency | 对 clean / perturbed prompt 分别重复生成，估计 within-prompt sample noise，再判断 between-prompt drift 是否超过自然输出波动 |

## 当前 Cross-Task 验证实际采用的统一设置

当前已经完成的 cross-task 验证使用的是同一个扰动类型：

```text
Paraphrasing / instruction rewording
```

选择 paraphrasing 的原因是它适合所有四类任务：

- Factual QA：只改写 instruction，不改 passage / question。
- Math reasoning：只改写 instruction，不改数字、公式、变量和题目条件。
- Code generation：只改写自然语言 instruction，不改 function signature 和 examples。
- Open-ended writing：自然用户改写最常见，适合开放式生成。

当前已经跑通的评价准则是：

```text
similarity / semantic drift
```

具体计算方式：

```text
uncorrected_single_drift
= distance(first clean output, first perturbed output)

raw_perturbation_drift
= average distance(all clean outputs, all perturbed outputs)

noise_baseline
= average(within-clean output distance, within-perturbed output distance)

noise_corrected_drift
= max(0, raw_perturbation_drift - noise_baseline)
```

## 参考文献中的评价准则如何对应到项目

| 项目中的评价方向 | 对应参考文献准则 | 来源文献 | 适用任务 |
|---|---|---|---|
| Correctness degradation | PDR / APDR | PromptRobust; Enhancing LLM Robustness | Factual QA, Math reasoning, Code generation |
| Classification-style performance | Micro-F1 | What Did I Do Wrong | 主要适合分类任务；本项目四类任务不是主用 |
| Prompt sensitivity | Sensitivity | What Did I Do Wrong | 四类任务均可借鉴 |
| Output stability / distribution change | Response diversity, entropy, semantic coherence | POSIX | Open-ended writing; 也可辅助 QA / math / code |
| Instruction semantic preservation | Human semantic preservation check; embedding cosine similarity | PromptRobust; Enhancing LLM Robustness | 四类任务均需要，用于确认扰动没有改变任务 |
| Repeated generation variability | Within-LLM sampling variance / variance decomposition | Haase et al. | 四类任务均适用，是 sample-noise correction 的依据 |
| Open-ended quality | Originality, fluency | Haase et al. | Open-ended writing / creative generation |

## 按任务展开

### 1. Factual QA

| 字段 | 设置 |
|---|---|
| 任务 | Factual QA |
| 数据集 | SQuAD V2 |
| 数据集来源 | PromptRobust / PromptBench |
| 扰动方式 | Paraphrasing / instruction rewording |
| 当前评价准则 | Similarity / semantic drift |
| 当前评价准则来源 | POSIX 的 semantic coherence / sensitivity 思路；What Did I Do Wrong 的 sensitivity；Haase et al. 的 within-LLM variance |
| 应接入 correctness 准则 | Answer correctness based PDR |
| Correctness 准则来源 | PromptRobust / PromptBench; Enhancing LLM Robustness |
| Uncorrection | 单次 clean output vs 单次 perturbed output，计算 drift 或 correctness drop |
| Sample noise correction | clean / perturbed prompt 各重复生成 K 次，先估计 within-prompt noise，再判断 between-prompt drift 或 correctness drop 是否超过 noise baseline |

### 2. Math Reasoning

| 字段 | 设置 |
|---|---|
| 任务 | Math reasoning |
| 数据集 | MATH / Mathematics |
| 数据集来源 | PromptRobust / PromptBench |
| 扰动方式 | Paraphrasing / instruction rewording |
| 当前评价准则 | Similarity / semantic drift |
| 当前评价准则来源 | POSIX; What Did I Do Wrong; Haase et al. |
| 应接入 correctness 准则 | Final-answer correctness based PDR |
| Correctness 准则来源 | PromptRobust / PromptBench; Enhancing LLM Robustness |
| Uncorrection | 单次 clean output vs 单次 perturbed output，计算 drift 或 final-answer correctness drop |
| Sample noise correction | clean / perturbed prompt 各重复生成 K 次，估计 within-prompt noise；用 repeated final-answer accuracy 计算更稳定的 PDR |

### 3. Code Generation

| 字段 | 设置 |
|---|---|
| 任务 | Code generation |
| 数据集 | HumanEval |
| 数据集来源 | 外部补充；五篇参考文献没有 code generation 数据集 |
| 扰动方式 | Paraphrasing / instruction rewording |
| 当前评价准则 | Similarity / semantic drift |
| 当前评价准则来源 | POSIX / What Did I Do Wrong 的 sensitivity 思路；Haase et al. 的 repeated-sampling variance |
| 应接入 correctness 准则 | Unit-test pass rate based PDR |
| Correctness 准则来源 | PDR 框架来自 PromptRobust / PromptBench 和 Enhancing LLM Robustness；pass rate 是 code generation 的 task performance |
| Uncorrection | 单次 clean code vs 单次 perturbed code，比较 drift 或 pass/fail difference |
| Sample noise correction | clean / perturbed prompt 各重复生成 K 份代码，估计 within-prompt output variability；用 repeated unit-test pass rate 计算 PDR |

### 4. Open-Ended Writing

| 字段 | 设置 |
|---|---|
| 任务 | Open-ended writing / open-ended generation |
| 数据集 | Alpaca |
| 数据集来源 | POSIX |
| 扰动方式 | Paraphrasing / instruction rewording |
| 当前评价准则 | Similarity / semantic drift |
| 当前评价准则来源 | POSIX 的 semantic coherence / response diversity；What Did I Do Wrong 的 sensitivity；Haase et al. 的 within-LLM variance |
| 可接入质量准则 | Semantic coherence, response diversity, fluency |
| 质量准则来源 | POSIX; Haase et al. |
| Uncorrection | 单次 clean output vs 单次 perturbed output，比较 semantic drift / coherence / fluency |
| Sample noise correction | clean / perturbed prompt 各重复生成 K 次，估计 within-prompt variability；只有当 between-prompt drift 超过 within-prompt noise 时，才认为 perturbation effect 明显 |

## 当前 Cross-Task Paraphrase 验证结果

当前已经完成的小样本验证：

```powershell
python sample_noise_pilot.py --suite reference_four_task --dataset-cases-per-task 2 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag cross_task_paraphrase
```

输出文件：

- `results/generations_cross_task_paraphrase.csv`
- `results/noise_metrics_cross_task_paraphrase.csv`
- `results/noise_metrics_cross_task_paraphrase.json`
- `results/sample_noise_report_cross_task_paraphrase.md`
- `cross_task_paraphrase_noise_correction.md`

结果汇总：

| Metric | Value |
|---|---:|
| Average uncorrected single-sample drift | 0.1613 |
| Average raw perturbation drift | 0.1284 |
| Average sample-noise baseline | 0.0461 |
| Average noise-corrected drift | 0.0825 |
| Share of raw drift explainable by sample noise | 35.9% |

按任务结果：

| Task | Dataset | Raw drift | Corrected drift |
|---|---|---:|---:|
| Factual QA | SQuAD V2 | 0.3079 | 0.2092 |
| Math reasoning | MATH | 0.0480 | 0.0014 |
| Code generation | HumanEval | 0.1254 | 0.1111 |
| Open-ended writing | Alpaca | 0.0321 | 0.0083 |

## 结论

当前 cross-task 验证中，四类任务使用：

```text
same perturbation: paraphrasing
same model and decoding setting
same similarity / semantic drift evaluation
same correction formula
```

结论是：

```text
不做 sample-noise correction 会高估 prompt perturbation 的影响。
在本次小样本验证中，35.9% 的 raw drift 可以由 within-prompt sample noise 解释。
```

下一步需要接入 task-specific correctness：

| Task | 下一步 correctness 准则 |
|---|---|
| Factual QA | answer correctness / semantic answer match |
| Math reasoning | final-answer exact match |
| Code generation | HumanEval unit-test pass rate |
| Open-ended writing | 无唯一 correctness，继续使用 semantic coherence / response diversity / fluency |
