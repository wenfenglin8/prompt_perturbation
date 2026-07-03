# Sample-Noise Correction 小样本验证结果

本次验证基于以下三个设计文件：

- `project_perturbation_plan_by_task.md`
- `reference_based_eval_criteria_by_task.md`
- `dataset_selection_for_noise_correction_comparison.md`

目标是用少量数据验证：在相同数据集、相同扰动方案、相同评价准则下，比较不做 sample-noise correction 和做 sample-noise correction 时，对 prompt perturbation 影响的估计是否不同。

## 实验设置

| 项目 | 设置 |
|---|---|
| Suite | `reference_four_task` |
| Model | `gpt-4o-mini` |
| Embedding model | `text-embedding-3-small` |
| Samples per clean / perturbed prompt | 3 |
| Temperature | 0.7 |
| Top-p | 0.9 |
| Evaluation focus | Similarity / semantic drift |
| Output files | `results/sample_noise_report_reference_four_task_smoke.md`, `results/noise_metrics_reference_four_task_smoke.json`, `results/generations_reference_four_task_smoke.csv` |

本次小样本验证每类任务各取 1 条样本：

| 任务 | 数据集 | 数据来源 |
|---|---|---|
| Factual QA | SQuAD V2 | PromptRobust / PromptBench |
| Math reasoning | MATH / Mathematics | PromptRobust / PromptBench |
| Code generation | HumanEval | 外部补充，因为 5 篇参考文献没有 code generation 数据集 |
| Open-ended writing | Alpaca | POSIX |

## 评价方式

本次验证先聚焦 similarity / semantic drift，因为现有脚本已经实现 embedding-based drift 和 within-prompt sample-noise baseline。

比较两种估计：

| 估计方式 | 含义 |
|---|---|
| Uncorrected single-sample drift | 只比较第 1 个 clean output 和第 1 个 perturbed output |
| Raw perturbation drift | 比较所有 clean outputs 和 perturbed outputs 的平均 cross-distance |
| Noise-corrected drift | `raw perturbation drift - within-prompt sample-noise baseline`，并裁剪到不小于 0 |

## 结果总览

| 指标 | 数值 |
|---|---:|
| Average uncorrected single-sample drift | 0.2392 |
| Average raw perturbation drift | 0.2253 |
| Average sample-noise baseline | 0.0616 |
| Average noise-corrected drift | 0.1637 |
| Share of raw drift explainable by sample noise | 27.4% |

整体上，sample-noise correction 将平均 drift 从 0.2253 降到 0.1637，说明不做 correction 会高估 prompt perturbation 的影响。在这个小样本中，约 27.4% 的 raw drift 可以由 repeated-generation sample noise 解释。

## 分任务结果

| Case | Task | Dataset | Uncorrected single drift | Noise baseline | Raw drift | Corrected drift | Interpretation |
|---|---|---|---:|---:|---:|---:|---|
| `ref_squad_v2_01` | Factual QA | SQuAD V2 | 0.5556 | 0.0840 | 0.5286 | 0.4446 | 扰动影响仍明显，但 correction 后估计降低 |
| `ref_math_01` | Math reasoning | MATH | 0.0483 | 0.0443 | 0.0450 | 0.0007 | raw drift 几乎完全可由 sample noise 解释 |
| `ref_humaneval_01` | Code generation | HumanEval | 0.2516 | 0.0322 | 0.2246 | 0.1924 | 扰动影响仍明显，但 correction 后估计降低 |
| `ref_alpaca_01` | Open-ended writing | Alpaca | 0.1014 | 0.0860 | 0.1030 | 0.0170 | 大部分 raw drift 可由 open-ended generation 的 sample noise 解释 |

## 初步解释

这次小样本验证支持项目的核心假设：

```text
single-generation 或 raw drift 可能高估 prompt perturbation effect；
repeated sampling 可以估计 within-prompt variability；
sample-noise correction 后，剩下的 drift 更接近 perturbation-specific effect。
```

不同任务的差异也很明显：

1. **Factual QA** 和 **Code generation** 在这个样本中 correction 后仍有较高 drift，说明 perturbation 可能确实改变了输出。
2. **Math reasoning** 的 raw drift 几乎等于 sample-noise baseline，说明 observed drift 主要来自 repeated generation variability，而不是 prompt perturbation。
3. **Open-ended writing** 的 sample-noise baseline 很高，符合 Haase et al. 的观点：开放式任务中同一 prompt 的自然输出差异不可忽略。

## 限制

这只是 method-validation，不是最终统计结论。限制包括：

1. 每类任务只有 1 条样本。
2. 每个 clean / perturbed prompt 只有 3 次生成。
3. 当前验证主要比较 similarity / semantic drift，尚未加入 task-specific correctness。
4. HumanEval 这里只比较输出 drift，尚未执行 unit tests。

下一步如果要比较 correctness，应在同一框架下加入：

| 任务 | Correctness criterion |
|---|---|
| SQuAD V2 | answer correctness / exact or semantic answer match |
| MATH | final-answer correctness |
| HumanEval | unit-test pass rate |
| Alpaca | 无唯一 correctness，继续使用 semantic coherence / response diversity / fluency |

## 当前可引用结论

```text
In a small four-task pilot using SQuAD V2, MATH, HumanEval, and Alpaca, the average raw prompt-perturbation drift was 0.2253. After estimating within-prompt variability from repeated generations and subtracting this sample-noise baseline, the average corrected drift decreased to 0.1637. This suggests that uncorrected single-generation or raw-drift evaluation can overestimate the effect of prompt perturbations, especially for math reasoning and open-ended writing, where much of the observed drift was explained by ordinary sampling variability.
```
