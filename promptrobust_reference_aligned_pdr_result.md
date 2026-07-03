# PromptRobust-Aligned PDR Result

本次重新对齐用户要求：

```text
相同的数据集
相同的扰动方式
相同的输出评价准则
比较 correction 和 uncorrection 的性能差异
```

这里严格选择 **PromptRobust / PromptBench** 作为对齐参考，因为在五篇参考文献中，PromptRobust 同时提供：

1. 可用于本项目的任务数据集：SQuAD V2 和 MATH。
2. Prompt-level perturbation 方式：character-level perturbation。
3. 输出评价准则：Performance Drop Rate (PDR)。

## 为什么本次只跑 Factual QA 和 Math Reasoning

五篇参考文献中，只有 PromptRobust / PromptBench 同时覆盖了：

| 项目任务 | 数据集 | 扰动方式 | 评价准则 |
|---|---|---|---|
| Factual QA | SQuAD V2 | character-level prompt perturbation | PDR |
| Math reasoning | MATH / Mathematics | character-level prompt perturbation | PDR |

Code generation 的 HumanEval 不来自五篇参考文献。Open-ended writing 的 Alpaca 来自 POSIX，但 POSIX 的原始评价准则是 log-likelihood based POSIX，不是 PDR，且需要 token probability。因此，如果要求完全参考文献一致，本次小实验应先限制在 PromptRobust 对齐的 SQuAD V2 和 MATH 上。

## Dataset Access Check

`load_dataset('squad_v2')` 在当前环境中会尝试访问 HuggingFace Hub，网络受限时容易卡住。已确认本地缓存可用，并改为直接读取 Arrow 文件：

```text
SQuAD V2:
C:\Users\wenfeng.lin\.cache\huggingface\datasets\squad_v2\squad_v2\0.0.0\3ffb306f725f7d2ce8394bc1873b24868140c412\squad_v2-validation.arrow

MATH:
C:\Users\wenfeng.lin\.cache\huggingface\datasets\DigitalLearningGmbH___math-lighteval\default\0.0.0\0530c78699ea5e8eb5530600900e1f328b48acad\math-lighteval-test.arrow
```

本地读取方式：

```python
from datasets import Dataset
ds = Dataset.from_file(path_to_arrow)
```

SQuAD V2 字段：

```text
id, title, context, question, answers
```

MATH 字段：

```text
problem, level, solution, type
```

## Experiment Setup

| 项目 | 设置 |
|---|---|
| Reference paper | PromptRobust / PromptBench |
| Tasks | Factual QA; Math reasoning |
| Datasets | SQuAD V2; MATH |
| Perturbation | character-level prompt perturbation on instruction |
| Evaluation criterion | Performance Drop Rate (PDR) |
| Performance definition | SQuAD V2: answer correctness; MATH: final-answer correctness |
| Model | `gpt-4o-mini` |
| Samples per clean / perturbed prompt | 3 |
| Temperature | 0.7 |
| Top-p | 0.9 |
| Cases per task | 2 |

运行命令：

```powershell
python promptrobust_reference_pdr_eval.py --dataset-cases-per-task 2 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag promptrobust_reference_pdr
```

输出文件：

- `results/generations_promptrobust_reference_pdr.csv`
- `results/pdr_metrics_promptrobust_reference_pdr.csv`
- `results/pdr_metrics_promptrobust_reference_pdr.json`
- `results/pdr_report_promptrobust_reference_pdr.md`

## Evaluation Criterion

参考文献评价准则：

```text
Performance Drop Rate (PDR)
```

公式：

```text
PDR = (Performance_clean - Performance_perturbed) / Performance_clean
```

在本实验中：

```text
Factual QA performance = answer correctness
Math reasoning performance = final-answer correctness
```

## Correction vs Uncorrection

| 设置 | 计算方式 |
|---|---|
| Uncorrection | 每个 case 只用第 1 个 clean output 和第 1 个 perturbed output 计算 single-sample PDR |
| Correction / repeated-sampling estimate | 每个 clean / perturbed prompt 各生成 3 次，用 mean correctness 计算 repeated-sampling PDR |

注意：

这里保持了同一数据集、同一扰动方式、同一模型、同一 decoding 参数、同一 PDR 评价准则。区别只在于：

```text
single-generation estimate
vs.
repeated-sampling estimate
```

## Aggregate Result

| Metric | Value |
|---|---:|
| Average clean single-sample correctness | 0.7500 |
| Average perturbed single-sample correctness | 0.7500 |
| Average uncorrected single-sample PDR | 0.0000 |
| Average clean repeated correctness | 0.6667 |
| Average perturbed repeated correctness | 0.5833 |
| Average repeated-sampling PDR | 0.1250 |

## Per-Item Result

| Case | Task | Dataset | Clean single | Perturbed single | Uncorrected PDR | Clean mean | Perturbed mean | Repeated PDR |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `promptrobust_pdr_squad_01` | Factual QA | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 |
| `promptrobust_pdr_squad_02` | Factual QA | SQuAD V2 | 1 | 1 | 0.0000 | 0.6667 | 0.3333 | 0.5000 |
| `promptrobust_pdr_math_01` | Math reasoning | MATH | 1 | 1 | 0.0000 | 0.6667 | 0.6667 | 0.0000 |
| `promptrobust_pdr_math_02` | Math reasoning | MATH | 0 | 0 | 0.0000 | 0.3333 | 0.3333 | 0.0000 |

## Task-Level Summary

| Task | N | Clean single | Perturbed single | Uncorrected PDR | Clean mean | Perturbed mean | Repeated PDR |
|---|---:|---:|---:|---:|---:|---:|---:|
| Factual QA | 2 | 1.0000 | 1.0000 | 0.0000 | 0.8333 | 0.6667 | 0.2500 |
| Math reasoning | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 |

## Interpretation

The strict reference-aligned comparison gives a different lesson from the earlier semantic-drift pilot:

```text
Uncorrected single-sample PDR: 0.0000
Repeated-sampling PDR:        0.1250
```

In this small run, single-generation evaluation did not detect any performance drop. Repeated sampling found a performance drop in one SQuAD V2 case:

```text
clean mean correctness:     0.6667
perturbed mean correctness: 0.3333
PDR:                        0.5000
```

Therefore, sample-noise-aware repeated evaluation does not always reduce the estimated perturbation effect. It can also reveal an effect that a single clean / perturbed sample misses.

## Main Takeaway

Under strict PromptRobust alignment:

```text
same dataset: SQuAD V2 / MATH
same perturbation: character-level instruction perturbation
same evaluation criterion: PDR
```

the small pilot shows that repeated sampling changes the estimated perturbation effect:

```text
single-sample PDR = 0.0000
repeated-sampling PDR = 0.1250
```

This supports the broader project argument that single-generation prompt-perturbation evaluation can be unreliable. It may overestimate, underestimate, or miss perturbation effects depending on the sampled outputs.

## Limitations

This is a small validation run:

1. Only 2 SQuAD V2 cases and 2 MATH cases.
2. Only 3 repeated generations per clean / perturbed prompt.
3. Exact correctness matching is strict and may undercount semantically correct QA answers.
4. The character-level perturbation is PromptRobust-style but not a full reproduction of PromptRobust adversarial search.

Next step:

```text
Increase dataset-cases-per-task and samples per prompt version.
```
