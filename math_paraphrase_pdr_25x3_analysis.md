# MATH Paraphrase PDR 25x3 Analysis

本文件保存刚才完成的 MATH-only 扩大实验结果，供 review 使用。

## 实验目的

之前 5-case MATH paraphrase PDR 结果显示：paraphrase 后 Math reasoning 的 correctness 反而提高。为了检查这是否只是小样本偶然现象，本次将 MATH 数据扩大 5 倍：

```text
5 MATH cases -> 25 MATH cases
```

本次只重新跑：

```text
Task: Math reasoning
Dataset: MATH
Perturbation: paraphrase / instruction rewording
Evaluation: PDR based on final-answer correctness
```

## 实验设置

| 项目 | 设置 |
|---|---|
| Task | Math reasoning |
| Dataset | MATH / Mathematics |
| Dataset source | PromptRobust / PromptBench |
| Perturbation | Paraphrase / instruction rewording |
| Evaluation criterion | PDR, Performance Drop Rate |
| Performance definition | final-answer correctness |
| Model | `gpt-4o-mini` |
| Samples per clean / perturbed prompt | 3 |
| Number of MATH cases | 25 |
| Temperature | 0.7 |
| Top-p | 0.9 |

运行命令：

```powershell
python promptrobust_reference_pdr_eval.py --tasks math_reasoning --dataset-cases-per-task 25 --samples 3 --temperature 0.7 --top-p 0.9 --perturbations paraphrase --output-tag math_paraphrase_pdr_25x3
```

总请求数：

```text
25 cases × 2 prompt versions × 3 samples = 150 model calls
```

脚本已加入进度显示，例如：

```text
Progress 75/150 (50.0%) complete
```

## 输出文件

| 文件 | 内容 |
|---|---|
| `results/generations_math_paraphrase_pdr_25x3.csv` | 所有 clean / perturbed generations 和 correctness |
| `results/pdr_metrics_math_paraphrase_pdr_25x3.csv` | 每个 case 的 PDR / correctness 指标 |
| `results/pdr_metrics_math_paraphrase_pdr_25x3.json` | JSON 格式完整指标 |
| `results/pdr_report_math_paraphrase_pdr_25x3.md` | 自动生成的实验报告 |

## 核心结果

| Metric | Value |
|---|---:|
| Clean single-sample correctness | 0.4000 |
| Perturbed single-sample correctness | 0.6000 |
| Uncorrected single-sample PDR | -0.5000 |
| Clean repeated correctness | 0.3600 |
| Perturbed repeated correctness | 0.5867 |
| Repeated-sampling PDR | -0.6296 |
| Average correctness sample noise | 0.1226 |

公式：

```text
PDR = (Performance_clean - Performance_perturbed) / Performance_clean
```

因为 perturbed performance 高于 clean performance，所以 PDR 为负数：

```text
Repeated-sampling PDR
= (0.3600 - 0.5867) / 0.3600
= -0.6296
```

## 结果解释

扩大到 25 条 MATH 后，之前的趋势没有反转：

```text
clean repeated correctness:     0.3600
perturbed repeated correctness: 0.5867
```

也就是说，在这个实验设置下，paraphrased instruction 比 clean instruction 更容易让模型答对 MATH final answer。

这说明当前 paraphrase perturbation 对 MATH 来说不是 harmful noise，而是可能更 reasoning-friendly。

Clean instruction:

```text
Solve the mathematics problem. Put the final answer only on the last line.
```

Paraphrased instruction:

```text
Work through the following math problem carefully.
Explain the reasoning, then state the final answer at the end.
```

第二个 instruction 更明确要求模型进行推理，因此可能提升 Math reasoning 表现。

## Correction vs Uncorrection

| Estimate | Clean performance | Perturbed performance | PDR |
|---|---:|---:|---:|
| Uncorrected single-sample | 0.4000 | 0.6000 | -0.5000 |
| Repeated-sampling | 0.3600 | 0.5867 | -0.6296 |

Interpretation:

```text
Both estimates agree that paraphrasing improves MATH correctness.
Repeated sampling changes the estimated magnitude:
uncorrected PDR = -0.5000
repeated PDR    = -0.6296
```

So sample-noise-aware repeated evaluation does not reverse the conclusion here, but it changes the estimated effect size.

## Per-Case Notes

The per-case results show substantial heterogeneity:

- Some cases are always correct under both clean and perturbed prompts.
- Some cases are always wrong under both.
- Several cases improve under the paraphrased prompt.
- A few cases get worse under paraphrasing.

This heterogeneity supports the need for repeated sampling and larger datasets when estimating prompt perturbation effects.

## Main Takeaway

For MATH reasoning under paraphrase perturbation:

```text
The perturbation improves final-answer correctness in this 25-case run.
Negative PDR should be interpreted as performance improvement under perturbed prompt, not as robustness failure.
```

This result is reasonable because the paraphrase is not a destructive perturbation. It changes the instruction into a more reasoning-oriented prompt.

## Implication for RQ1

For RQ1, this result means perturbation sensitivity is task- and perturbation-dependent:

```text
The same perturbation type can hurt one task, help another task, or mostly affect output similarity without hurting correctness.
```

In particular:

- For MATH, paraphrase may improve correctness.
- For harmful robustness testing on MATH, character-level typo, irrelevant sentence insertion, or stronger adversarial-style perturbations may be more appropriate.

## Limitations

1. This is still a moderate-scale validation, not a full benchmark.
2. Only 25 MATH cases were used.
3. Each prompt version was sampled 3 times.
4. Correctness depends on final-answer extraction and exact matching.
5. The perturbation is paraphrasing, not adversarial search.

## Recommended Follow-Up

Before treating this as a final result, consider:

1. Increase MATH cases further, for example 50 or 100.
2. Compare paraphrase against character-level and sentence-level perturbations on the same 25 cases.
3. Improve final-answer extraction for MATH.
4. Report both correctness PDR and similarity drift.
