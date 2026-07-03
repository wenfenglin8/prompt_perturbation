# PromptRobust-Aligned PDR 5x3 Run Interpretation

本次扩大数据集验证实际已经完成，输出文件为：

- `results/generations_promptrobust_reference_pdr_5x3.csv`
- `results/pdr_metrics_promptrobust_reference_pdr_5x3.csv`
- `results/pdr_metrics_promptrobust_reference_pdr_5x3.json`
- `results/pdr_report_promptrobust_reference_pdr_5x3.md`

## 为什么运行慢

这次运行不是卡在 SQuAD 数据集访问。SQuAD 和 MATH 都已经改成直接读取本地 Arrow cache。

主要耗时来自模型 API 生成：

```text
5 SQuAD cases + 5 MATH cases = 10 cases
每个 case: clean prompt + perturbed prompt = 2 prompt versions
每个 prompt version: 3 repeated generations
总请求数 = 10 × 2 × 3 = 60 model calls
```

脚本目前是顺序请求，没有并发。因此运行时间主要由 60 次 API latency 累加决定。

## Reference Alignment

本次设置严格对齐 PromptRobust / PromptBench：

| 项目 | 设置 |
|---|---|
| Reference paper | PromptRobust / PromptBench |
| Dataset | SQuAD V2; MATH |
| Perturbation | character-level prompt perturbation on instruction |
| Evaluation criterion | Performance Drop Rate (PDR) |
| Performance | answer correctness / final-answer correctness |

## Dataset-Level PDR

PromptRobust-style PDR 应按整体 performance 计算：

```text
PDR = (Performance_clean - Performance_perturbed) / Performance_clean
```

因此，dataset-level PDR 比直接平均 per-item PDR 更合适。直接平均 per-item PDR 在 clean correctness 为 0 的 case 上会产生不稳定解释。

## Aggregate Result

根据 `results/pdr_metrics_promptrobust_reference_pdr_5x3.csv`：

| Estimate | Clean performance | Perturbed performance | PDR |
|---|---:|---:|---:|
| Uncorrected single-sample | 0.6000 | 0.5000 | 0.1667 |
| Repeated-sampling | 0.5667 | 0.6000 | -0.0588 |

Interpretation:

```text
The uncorrected single-sample estimate suggests a 16.67% performance drop.
The repeated-sampling estimate does not confirm this drop; perturbed mean performance is slightly higher than clean mean performance in this small run.
```

So in this larger 5x3 run, single-sample evaluation appears to **overestimate** the perturbation harm.

## Task-Level Result

| Task | N | Clean single | Perturbed single | Single-sample PDR | Clean mean | Perturbed mean | Repeated-sampling PDR |
|---|---:|---:|---:|---:|---:|---:|---:|
| Factual QA | 5 | 0.6000 | 0.6000 | 0.0000 | 0.6000 | 0.6667 | -0.1111 |
| Math reasoning | 5 | 0.6000 | 0.4000 | 0.3333 | 0.5333 | 0.5333 | 0.0000 |

Interpretation by task:

- **Factual QA**: single-sample PDR shows no drop. Repeated sampling shows perturbed performance slightly higher than clean performance in this small sample.
- **Math reasoning**: single-sample PDR suggests a 33.33% drop, but repeated sampling shows no performance drop.

## Main Takeaway

Under the strict reference-aligned setup:

```text
same dataset: SQuAD V2 / MATH
same perturbation: character-level prompt perturbation
same evaluation criterion: PDR
```

the 5x3 run shows that uncorrected single-sample evaluation can overestimate perturbation harm:

```text
uncorrected single-sample PDR: 0.1667
repeated-sampling PDR:       -0.0588
```

This supports the project argument that single-generation prompt-perturbation evaluation is unstable. Repeated sampling gives a more reliable estimate of the perturbation effect under the same reference criterion.

## Important Note

The script `promptrobust_reference_pdr_eval.py` has been updated so future reports compute **dataset-level PDR** in the aggregate section, avoiding misleading `-inf` values from per-item cases where clean performance is zero.
