# Three-Task PDR Evaluation, 10 Cases Per Task

- Datasets: `HumanEval, MATH, SQuAD V2`.
- Tasks: `factual_qa, math_reasoning, code_generation`.
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise` applied to the instruction only.
- Samples: `3` generations per clean prompt and `3` generations per perturbed prompt.
- Evaluation criterion: Performance Drop Rate (PDR), using task correctness as performance.
- Code generation correctness: HumanEval pass@1-style unit-test pass/fail; completions are evaluated as HumanEval prompt + model completion, with standalone full-code outputs accepted as a fallback.

## Aggregate Result

- Average clean single-sample correctness: `0.4867`
- Average perturbed single-sample correctness: `0.4533`
- Dataset-level uncorrected single-sample PDR: `0.0685`
- Average clean repeated correctness: `0.4778`
- Average perturbed repeated correctness: `0.4733`
- Dataset-level repeated-sampling PDR: `0.0093`
- Difference, uncorrected minus repeated PDR: `0.0592`

## Core Result and Interpretation

本次将 case 数提高到 `10 cases/task` 后，整体结果如下：

```text
Average clean single-sample correctness:     0.4867
Average perturbed single-sample correctness: 0.4533
Uncorrected single-sample PDR:               0.0685

Average clean repeated correctness:          0.4778
Average perturbed repeated correctness:      0.4733
Repeated-sampling PDR:                       0.0093
```

解释：

```text
uncorrected 估计：扰动造成约 6.85% relative performance drop
repeated-sampling 后：扰动造成约 0.93% relative performance drop
```

也就是说，单次采样估计会明显高估 perturbation 对 correctness 的影响。使用 repeated sampling / sample-noise-aware 估计后，PDR 从 `0.0685` 降到 `0.0093`。

分任务看：

```text
factual_qa:      uncorrected 0.0323 -> repeated 0.0319，几乎不变
math_reasoning:  uncorrected 0.0000 -> repeated -0.1852，重复采样后反而显示 perturbed 更高
code_generation: uncorrected 0.1818 -> repeated 0.1343，影响仍在但变小
```

因此，这轮更大样本验证支持当前研究假设：

```text
如果只用单次生成，PDR 可能把 sampling randomness 误当成 perturbation effect；
repeated sampling 后，扰动造成的 correctness drop 明显收敛。
```

## By Task

| task | n | clean single | perturbed single | uncorrected PDR | clean repeated | perturbed repeated | repeated PDR | difference |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| factual_qa | 50 | 0.6200 | 0.6000 | 0.0323 | 0.6267 | 0.6067 | 0.0319 | 0.0003 |
| math_reasoning | 50 | 0.4000 | 0.4000 | 0.0000 | 0.3600 | 0.4267 | -0.1852 | 0.1852 |
| code_generation | 50 | 0.4400 | 0.3600 | 0.1818 | 0.4467 | 0.3867 | 0.1343 | 0.0475 |

## Grouped Result

| perturbation | task | n | clean single | perturbed single | uncorrected PDR | clean repeated | perturbed repeated | repeated PDR | difference | repeated pass-rate drop |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| paraphrase | factual_qa | 10 | 0.6000 | 0.6000 | 0.0000 | 0.6333 | 0.5667 | 0.1053 | -0.1053 | 0.0667 |
| paraphrase | math_reasoning | 10 | 0.4000 | 0.2000 | 0.5000 | 0.3333 | 0.3000 | 0.1000 | 0.4000 | 0.0333 |
| paraphrase | code_generation | 10 | 0.4000 | 0.4000 | 0.0000 | 0.4333 | 0.4000 | 0.0769 | -0.0769 | 0.0333 |
| reordering | factual_qa | 10 | 0.6000 | 0.6000 | 0.0000 | 0.6000 | 0.6000 | 0.0000 | 0.0000 | 0.0000 |
| reordering | math_reasoning | 10 | 0.5000 | 0.5000 | 0.0000 | 0.4000 | 0.4333 | -0.0833 | 0.0833 | -0.0333 |
| reordering | code_generation | 10 | 0.4000 | 0.5000 | -0.2500 | 0.4667 | 0.5000 | -0.0714 | -0.1786 | -0.0333 |
| formatting | factual_qa | 10 | 0.7000 | 0.6000 | 0.1429 | 0.6667 | 0.6000 | 0.1000 | 0.0429 | 0.0667 |
| formatting | math_reasoning | 10 | 0.3000 | 0.5000 | -0.6667 | 0.3333 | 0.5667 | -0.7000 | 0.0333 | -0.2333 |
| formatting | code_generation | 10 | 0.4000 | 0.1000 | 0.7500 | 0.4333 | 0.1667 | 0.6154 | 0.1346 | 0.2667 |
| context_injection | factual_qa | 10 | 0.6000 | 0.7000 | -0.1667 | 0.6333 | 0.7333 | -0.1579 | -0.0088 | -0.1000 |
| context_injection | math_reasoning | 10 | 0.3000 | 0.4000 | -0.3333 | 0.3667 | 0.3667 | 0.0000 | -0.3333 | 0.0000 |
| context_injection | code_generation | 10 | 0.5000 | 0.5000 | 0.0000 | 0.4333 | 0.5000 | -0.1538 | 0.1538 | -0.0667 |
| surface_noise | factual_qa | 10 | 0.6000 | 0.5000 | 0.1667 | 0.6000 | 0.5333 | 0.1111 | 0.0556 | 0.0667 |
| surface_noise | math_reasoning | 10 | 0.5000 | 0.4000 | 0.2000 | 0.3667 | 0.4667 | -0.2727 | 0.4727 | -0.1000 |
| surface_noise | code_generation | 10 | 0.5000 | 0.3000 | 0.4000 | 0.4667 | 0.3667 | 0.2143 | 0.1857 | 0.1000 |

## Interpretation

The uncorrected condition estimates PDR from one clean output and one perturbed output. The repeated-sampling condition estimates clean and perturbed performance from three generations each under the same dataset, perturbation, model, decoding parameters, and PDR criterion. The difference column shows how much the single-sample estimate changes after accounting for repeated-generation variability.

For code generation, PDR should be interpreted together with pass-rate drop because PDR is unstable when clean pass rate is near zero.

## Note on Perturbation Strength

基于当前 `10 cases/task, 3 samples/prompt` 的 PDR 结果：

```text
uncorrected PDR: 0.0685
corrected / repeated-sampling PDR: 0.0093
```

可以初步认为：

```text
当前这组 natural perturbations 对前三类任务的 correctness 影响整体较小。
```

更严谨的解释是：

```text
在单次 uncorrected 估计下，扰动看起来造成了约 6.85% 的相对性能下降；
但经过 repeated sampling / sample-noise-aware correction 后，估计的下降只有约 0.93%。
```

因此，uncorrected 估计比 corrected 估计高：

```text
0.0685 - 0.0093 = 0.0592
```

也就是：

```text
5.92 percentage points
```

这说明单次采样可能把 sampling randomness 误当成 perturbation effect，从而高估扰动对 correctness 的影响。

不过，不建议直接写：

```text
the perturbations are too weak
```

更合适的表述是：

```text
The current natural perturbations produce limited correctness degradation after accounting for sampling noise.
```

原因有三点：

1. 当前 perturbation 设计本来是 non-adversarial / natural everyday perturbation，不是 adversarial attack，因此不是为了最大化性能下降。
2. Semantic drift 和 correctness drop 是两个不同指标；扰动可能改变输出表达或语义相似度，但不一定导致答案错误。
3. 分任务效果不同。整体 corrected PDR 很小，但 code generation 仍然存在明显影响：

```text
code_generation repeated PDR = 0.1343
```

也就是说，code generation 在 corrected 后仍显示约 `13.43%` 的 relative performance drop。

可以在论文或报告中使用以下表述：

```text
After sample-noise-aware correction, the overall PDR decreases from 6.85% to 0.93%,
suggesting that the current natural perturbations have limited impact on task correctness overall.
However, this does not imply that the perturbations are ineffective, because the study focuses on natural prompt variation rather than adversarial degradation, and task-specific effects remain visible, especially for code generation.
```
