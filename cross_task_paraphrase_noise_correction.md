# Cross-Task Paraphrase Perturbation: Sample-Noise Correction 验证

本次验证基于 `project_perturbation_plan_by_task.md`，从项目扰动方案中选择一个适合所有任务的 perturbation，并在四类任务数据集上比较：

```text
without sample-noise correction
vs.
with sample-noise correction
```

## 选择的扰动类型

本次选择：

```text
Paraphrasing / rewording
```

选择理由：

1. Paraphrasing 是四类任务都适用的自然 prompt perturbation。
2. 它可以保持 task intent 不变，只改变 instruction 的表达方式。
3. 对 factual QA，不需要修改 passage 或 question。
4. 对 math reasoning，不需要修改数字、公式、变量或题目条件。
5. 对 code generation，不需要修改 function signature、examples 或测试相关约束。
6. 对 open-ended writing，它是最自然的用户改写形式之一。

因此，paraphrasing 是最适合做 cross-task apple-to-apple 比较的扰动类型。

## 数据集

| Task | Dataset | Source |
|---|---|---|
| Factual QA | SQuAD V2 | PromptRobust / PromptBench |
| Math reasoning | MATH / Mathematics | PromptRobust / PromptBench |
| Code generation | HumanEval | External supplement |
| Open-ended writing | Alpaca | POSIX |

本次每类任务取 2 条样本，共 8 条样本。

## 实验设置

| Setting | Value |
|---|---|
| Suite | `reference_four_task` |
| Perturbation | Paraphrasing / instruction rewording |
| Model | `gpt-4o-mini` |
| Embedding model | `text-embedding-3-small` |
| Samples per clean / perturbed prompt | 3 |
| Temperature | 0.7 |
| Top-p | 0.9 |

运行命令：

```powershell
python sample_noise_pilot.py --suite reference_four_task --dataset-cases-per-task 2 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag cross_task_paraphrase
```

输出文件：

- `results/generations_cross_task_paraphrase.csv`
- `results/noise_metrics_cross_task_paraphrase.csv`
- `results/noise_metrics_cross_task_paraphrase.json`
- `results/sample_noise_report_cross_task_paraphrase.md`

## Overall Result

| Metric | Value |
|---|---:|
| Average uncorrected single-sample drift | 0.1613 |
| Average raw perturbation drift | 0.1284 |
| Average sample-noise baseline | 0.0461 |
| Average noise-corrected drift | 0.0825 |
| Share of raw drift explainable by sample noise | 35.9% |

Interpretation:

```text
Without sample-noise correction, the average drift estimate is 0.1284 using repeated cross-prompt drift, or 0.1613 using only a single clean / perturbed output pair. After subtracting the within-prompt sample-noise baseline, the estimated perturbation-specific drift decreases to 0.0825.
```

This means that, in this small cross-task run, about 35.9% of the raw paraphrase-induced drift can be explained by ordinary repeated-generation variability.

## Task-Level Average Results

| Task | N | Uncorrected single drift | Noise baseline | Raw drift | Corrected drift |
|---|---:|---:|---:|---:|---:|
| Factual QA | 2 | 0.4415 | 0.0987 | 0.3079 | 0.2092 |
| Math reasoning | 2 | 0.0432 | 0.0474 | 0.0480 | 0.0014 |
| Code generation | 2 | 0.1348 | 0.0144 | 0.1254 | 0.1111 |
| Open-ended writing | 2 | 0.0256 | 0.0239 | 0.0321 | 0.0083 |

## Per-Item Results

| Case | Task | Dataset | Uncorrected single drift | Noise baseline | Raw drift | Corrected drift |
|---|---|---|---:|---:|---:|---:|
| `ref_squad_v2_01` | Factual QA | SQuAD V2 | 0.5557 | 0.0840 | 0.5016 | 0.4176 |
| `ref_squad_v2_02` | Factual QA | SQuAD V2 | 0.3273 | 0.1133 | 0.1141 | 0.0008 |
| `ref_math_01` | Math reasoning | MATH | 0.0331 | 0.0533 | 0.0560 | 0.0028 |
| `ref_math_02` | Math reasoning | MATH | 0.0533 | 0.0416 | 0.0400 | 0.0000 |
| `ref_humaneval_01` | Code generation | HumanEval | 0.2434 | 0.0214 | 0.2218 | 0.2004 |
| `ref_humaneval_02` | Code generation | HumanEval | 0.0262 | 0.0073 | 0.0290 | 0.0217 |
| `ref_alpaca_01` | Open-ended writing | Alpaca | 0.0512 | 0.0477 | 0.0643 | 0.0165 |
| `ref_alpaca_02` | Open-ended writing | Alpaca | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Interpretation by Task

### Factual QA

Factual QA shows the largest uncorrected drift and still has substantial corrected drift on average:

```text
raw drift:       0.3079
corrected drift: 0.2092
```

However, the two examples behave differently. One SQuAD example retains a strong perturbation-specific drift after correction, while the other is almost fully explained by sample noise. This suggests that paraphrase sensitivity in QA may be item-dependent.

### Math Reasoning

Math reasoning shows the clearest effect of sample-noise correction:

```text
raw drift:       0.0480
corrected drift: 0.0014
```

The raw paraphrase drift is almost entirely explained by within-prompt variability. For these two MATH examples, uncorrected evaluation would overstate the paraphrase perturbation effect.

### Code Generation

Code generation retains a clear perturbation-specific drift:

```text
raw drift:       0.1254
corrected drift: 0.1111
```

The within-prompt noise baseline is small compared with the between-prompt drift. This suggests that paraphrasing the instruction can meaningfully change generated code outputs, at least in embedding space. The next step is to add HumanEval unit-test pass rate so this can be connected to correctness, not only similarity drift.

### Open-Ended Writing

Open-ended writing shows a moderate raw drift but much smaller corrected drift:

```text
raw drift:       0.0321
corrected drift: 0.0083
```

This matches the motivation from Haase et al.: open-ended generation has non-trivial within-prompt variability, so single-output comparisons can exaggerate prompt effects.

## Main Conclusion

For a cross-task paraphrase perturbation, sample-noise correction changes the interpretation:

```text
Average raw drift:       0.1284
Average corrected drift: 0.0825
Reduction:               35.9% of raw drift explained by sample noise
```

The effect is not uniform across tasks:

- **Math reasoning**: most raw drift disappears after correction.
- **Open-ended writing**: most raw drift is reduced after correction.
- **Factual QA**: corrected drift remains high for one example but not the other.
- **Code generation**: corrected drift remains high, suggesting paraphrase can change code outputs beyond sample noise.

## What This Validates

This run validates the project design:

```text
same dataset
same perturbation type: paraphrasing
same model and decoding settings
same similarity-based evaluation
comparison of uncorrected vs sample-noise-corrected estimates
```

It supports the claim that sample-noise correction provides a more conservative and more accurate estimate of prompt perturbation impact than single-generation or raw-drift evaluation.

## Limitations

This is still a small validation run:

1. Only 2 examples per task.
2. Only 3 generations per clean / perturbed prompt.
3. Current comparison uses similarity / semantic drift.
4. Task-specific correctness is not yet evaluated.
5. HumanEval outputs have not yet been run against unit tests.

The next experiment should add task-specific correctness:

| Task | Correctness metric |
|---|---|
| SQuAD V2 | answer correctness / semantic answer match |
| MATH | final-answer exact match |
| HumanEval | unit-test pass rate |
| Alpaca | no unique correctness; keep semantic coherence / response diversity |

## PDR Correctness Check for Factual QA and Math

Factual QA and Math reasoning both have objective correctness targets, so they can also be evaluated with the reference-paper PDR criterion:

```text
PDR = (Performance_clean - Performance_perturbed) / Performance_clean
```

where:

```text
Factual QA performance = SQuAD V2 answer correctness
Math reasoning performance = MATH final-answer correctness
```

This PDR check was run only for the two tasks where correctness is well-defined:

| Task | Dataset | Perturbation | Evaluation criterion | Evaluation source |
|---|---|---|---|---|
| Factual QA | SQuAD V2 | Paraphrasing / instruction rewording | PDR based on answer correctness | PromptRobust / PromptBench; Enhancing LLM Robustness |
| Math reasoning | MATH | Paraphrasing / instruction rewording | PDR based on final-answer correctness | PromptRobust / PromptBench; Enhancing LLM Robustness |

Run command:

```powershell
python promptrobust_reference_pdr_eval.py --dataset-cases-per-task 2 --samples 3 --temperature 0.7 --top-p 0.9 --perturbations paraphrase --output-tag cross_task_paraphrase_pdr
```

Output files:

- `results/generations_cross_task_paraphrase_pdr.csv`
- `results/pdr_metrics_cross_task_paraphrase_pdr.csv`
- `results/pdr_metrics_cross_task_paraphrase_pdr.json`
- `results/pdr_report_cross_task_paraphrase_pdr.md`

### PDR Result

| Task | N | Clean single perf | Perturbed single perf | Uncorrected PDR | Clean repeated perf | Perturbed repeated perf | Repeated-sampling PDR | Difference |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Factual QA | 2 | 0.5000 | 0.5000 | 0.0000 | 0.6667 | 0.5000 | 0.2500 | -0.2500 |
| Math reasoning | 2 | 0.0000 | 1.0000 | N/A | 0.0000 | 0.8333 | N/A | N/A |

For Factual QA:

```text
uncorrected PDR:        0.0000
repeated-sampling PDR:  0.2500
```

The single-sample estimate did not detect a performance drop, but repeated sampling found a 25% relative drop in answer correctness.

For Math reasoning, the clean prompt correctness was 0 in this tiny sample:

```text
clean repeated performance:     0.0000
perturbed repeated performance: 0.8333
```

Since PDR divides by clean performance, PDR is not meaningful when clean performance is zero. This case should be interpreted as:

```text
The paraphrased prompt performed better than the clean prompt on these two MATH examples, but PDR is undefined because clean baseline performance is zero.
```

### PDR Interpretation

This PDR check supports the same methodological point as the similarity-drift analysis:

```text
single-sample evaluation and repeated-sampling evaluation can give different conclusions.
```

For Factual QA, repeated sampling revealed a correctness drop that the single-sample estimate missed. For Math, the tiny sample is not suitable for PDR because clean performance was zero, so the next run should use more MATH examples or easier examples to obtain a nonzero clean baseline.

## Larger PDR Check: 5 Cases per Task

Because the 2-case PDR check had an unstable Math baseline, a larger run was performed:

```powershell
python promptrobust_reference_pdr_eval.py --dataset-cases-per-task 5 --samples 3 --temperature 0.7 --top-p 0.9 --perturbations paraphrase --output-tag cross_task_paraphrase_pdr_5x3
```

The script was also updated to print progress:

```text
Progress completed_requests / total_requests (percentage)
```

For this run:

```text
5 SQuAD cases + 5 MATH cases = 10 cases
2 prompt versions per case
3 samples per prompt version
total model calls = 60
```

Output files:

- `results/generations_cross_task_paraphrase_pdr_5x3.csv`
- `results/pdr_metrics_cross_task_paraphrase_pdr_5x3.csv`
- `results/pdr_metrics_cross_task_paraphrase_pdr_5x3.json`
- `results/pdr_report_cross_task_paraphrase_pdr_5x3.md`

### 5x3 Aggregate Result

| Metric | Value |
|---|---:|
| Average clean single-sample correctness | 0.5000 |
| Average perturbed single-sample correctness | 0.6000 |
| Dataset-level uncorrected single-sample PDR | -0.2000 |
| Average clean repeated correctness | 0.5000 |
| Average perturbed repeated correctness | 0.5667 |
| Dataset-level repeated-sampling PDR | -0.1333 |

### 5x3 Task-Level Result

| Task | N | Clean single perf | Perturbed single perf | Uncorrected PDR | Clean repeated perf | Perturbed repeated perf | Repeated-sampling PDR | Difference |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Factual QA | 5 | 0.6000 | 0.4000 | 0.3333 | 0.6000 | 0.4000 | 0.3333 | 0.0000 |
| Math reasoning | 5 | 0.4000 | 0.8000 | -1.0000 | 0.4000 | 0.7333 | -0.8333 | -0.1667 |

### 5x3 Interpretation

For **Factual QA**, the result is stable across single-sample and repeated-sampling estimates:

```text
uncorrected PDR:        0.3333
repeated-sampling PDR:  0.3333
```

In these 5 SQuAD cases, paraphrasing reduced answer correctness by about one third, and repeated sampling did not change that estimate.

For **Math reasoning**, paraphrasing improved correctness in this sample:

```text
uncorrected PDR:        -1.0000
repeated-sampling PDR:  -0.8333
```

Negative PDR means perturbed performance exceeded clean performance. Repeated sampling made the estimated improvement less extreme.

Overall, the larger PDR run is more interpretable than the 2-case run:

```text
Factual QA: paraphrase hurts correctness.
Math reasoning: paraphrase improves correctness in this small sample.
Repeated sampling can either confirm the single-sample result or moderate its magnitude.
```

## MATH-Only Larger PDR Check: 25 Cases

To check whether the MATH result changes with more data, the math reasoning subset was expanded 5x:

```powershell
python promptrobust_reference_pdr_eval.py --tasks math_reasoning --dataset-cases-per-task 25 --samples 3 --temperature 0.7 --top-p 0.9 --perturbations paraphrase --output-tag math_paraphrase_pdr_25x3
```

Progress reporting was added to the script. This run used:

```text
25 MATH cases
2 prompt versions per case
3 samples per prompt version
total model calls = 150
```

Output files:

- `results/generations_math_paraphrase_pdr_25x3.csv`
- `results/pdr_metrics_math_paraphrase_pdr_25x3.csv`
- `results/pdr_metrics_math_paraphrase_pdr_25x3.json`
- `results/pdr_report_math_paraphrase_pdr_25x3.md`

### 25x3 MATH Result

| Task | N | Clean single perf | Perturbed single perf | Uncorrected PDR | Clean repeated perf | Perturbed repeated perf | Repeated-sampling PDR | Difference |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Math reasoning | 25 | 0.4000 | 0.6000 | -0.5000 | 0.3600 | 0.5867 | -0.6296 | 0.1296 |

Average correctness sample noise:

```text
0.1226
```

### Interpretation of the 25x3 MATH Result

The larger MATH-only run confirms the earlier pattern:

```text
clean repeated performance:     0.3600
perturbed repeated performance: 0.5867
repeated-sampling PDR:          -0.6296
```

The paraphrased instruction still performs better than the clean instruction. This means the paraphrase perturbation is not acting as harmful noise for MATH. Instead, it likely makes the instruction more reasoning-friendly:

```text
Clean instruction:
Solve the mathematics problem. Put the final answer only on the last line.

Paraphrased instruction:
Work through the following math problem carefully. Explain the reasoning, then state the final answer at the end.
```

The paraphrased version encourages reasoning before the final answer, which can improve math correctness.

The difference between uncorrected and repeated-sampling PDR also changes:

```text
uncorrected PDR:       -0.5000
repeated-sampling PDR: -0.6296
difference:             0.1296
```

So repeated sampling does not reverse the conclusion, but it changes the estimated magnitude of the effect.

### Updated MATH Conclusion

With 25 MATH cases, the result is more stable:

```text
For MATH, paraphrasing improves final-answer correctness in this experiment.
Negative PDR should be interpreted as performance improvement under the perturbed prompt, not as robustness failure.
```

If the goal is to test harmful perturbation for math reasoning, a different perturbation type is more appropriate, such as:

- character-level typos,
- irrelevant sentence insertion,
- formatting constraints,
- or adversarial-style word-level perturbation.
