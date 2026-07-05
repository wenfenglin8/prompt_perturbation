# Why Code-Generation Points Are Dispersed in the Surface-Noise Scatter

## Figure

```text
results/rq2_figures/rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_similarity_vs_correctness_scatter.png
```

This figure plots nonzero surface-noise levels only:

```text
strength_edits = 2, 4, 8, 16
```

The x-axis is:

```text
mean_cross_similarity
```

The y-axis is:

```text
abs_repeated_pass_rate_change
```

That is:

```text
abs(clean_mean_correctness - perturbed_mean_correctness)
```

## Data Integrity Check

The combined 50x5 data were checked across the five batch metrics files.

```text
Total metric rows: 1000
Duplicate base_case_id + strength_edits rows: 0
Rows per task:
  code_generation    250
  factual_qa         250
  long_factual_qa    250
  math_reasoning     250
```

For nonzero perturbation levels:

```text
code_generation rows: 200
```

The code-generation scatter is therefore not caused by duplicate rows or an obvious batch-merge error.

## Main Reason

The code-generation points are dispersed mainly because HumanEval correctness is binary and format-sensitive.

For each prompt version, the experiment samples 5 outputs. Each HumanEval output either passes or fails unit tests:

```text
pass = 1.0
fail = 0.0
```

Therefore the repeated correctness mean can only take discrete values:

```text
0.0, 0.2, 0.4, 0.6, 0.8, 1.0
```

As a result, the y-axis value for code generation also tends to jump in discrete steps:

```text
0.0, 0.2, 0.4, 0.6, 0.8, 1.0
```

This makes code-generation points look more scattered than tasks with smoother or partial-credit scoring.

## Absolute Change Mixes Improvement and Harmful Drop

The plotted correctness change is an absolute value:

```text
abs_repeated_pass_rate_change
```

So it does not distinguish between:

```text
clean better than perturbed
perturbed better than clean
```

For code-generation nonzero rows, the direction counts were:

```text
unchanged: 127
improved under perturbed: 56
dropped under perturbed: 17
```

Among high-change rows:

```text
abs_repeated_pass_rate_change >= 0.4
```

the direction counts were:

```text
improved under perturbed: 37
dropped under perturbed: 9
unchanged: 0
```

Therefore many high-y code points are not harmful failures. They are cases where the perturbed prompt happened to produce more passing samples than the clean prompt.

## Why Code Is Especially Sensitive

HumanEval correctness depends on executable behavior and output formatting.

The evaluator tries to execute:

```text
HumanEval prompt prefix + model completion
```

and also accepts a standalone full-code output as a fallback.

Small changes in generation style can matter:

```text
function header repeated or omitted
markdown fences
extra explanation text
imports
indentation
edge-case handling
minor syntax mistakes
```

Surface noise only changes the instruction, not the HumanEval function prompt itself, but it can still change how the model formats or completes code. That makes pass/fail correctness more volatile.

## Embedding Similarity Is Not Functional Equivalence

The x-axis is based on embedding similarity between clean and perturbed outputs.

For code, embedding similarity is not the same as functional equivalence:

```text
Two code outputs can look semantically different but both pass tests.
Two code outputs can look semantically similar but one small bug can fail tests.
```

This weakens the visual alignment between semantic similarity and unit-test correctness at the individual-case level.

## Still Not Random Noise

Although the code points are visually dispersed, they still show a strong monotonic relationship:

```text
code_generation nonzero similarity vs correctness-change Spearman = -0.7385
```

This means:

```text
lower similarity is associated with larger correctness movement
```

So the code-generation cloud is not random. It is noisy and discrete, but directionally consistent with the RQ2 expectation.

## Recommended Interpretation

The broad dispersion of code-generation points is not a batch-merging or counting error. It mainly reflects the binary and format-sensitive nature of HumanEval pass/fail scoring under repeated sampling. Since the plotted correctness change is absolute, both harmful drops and improvements appear as large movements. Code outputs also have a weaker alignment between embedding similarity and functional equivalence, which further spreads the case-level scatter.

## Suggested Follow-Up Figure

Add a code-only scatter that separates direction:

```text
performance drop
performance improvement
unchanged
```

This would make it clear that many high-y code-generation points are improvements under perturbation rather than harmful robustness failures.
