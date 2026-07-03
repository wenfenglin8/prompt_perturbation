# Proposal Theoretical Strengthening Suggestions

## Core Diagnosis

The current proposal is not lacking theory entirely. Its issue is that the theoretical framing is still mostly expressed as:

```text
prompt perturbation changes outputs, so this study measures semantic drift and correctness drift.
```

That is enough for an empirical study, but the proposal would be stronger if it framed the experiment through robustness, invariance, and noise-corrected sensitivity.

The study should be reframed as:

```text
intent-preserving input perturbation -> output distribution shift -> possible correctness drift
```

## 1. Use "Prompt as Input Perturbation" as the Core Framework

The proposal already has this idea, but it should be made more theoretical.

Suggested wording:

> A prompt can be treated as an input representation of user intent. Prompt perturbations are input-space transformations that ideally preserve task intent but may alter the model's internal interpretation and output distribution.

中文解释：

> prompt 是用户意图的输入表征。perturbation 是对输入表征的扰动。理想情况下，它不改变任务意图，但可能改变模型内部解释和输出分布。

This reframes the study from simply "changing prompt wording" to studying:

```text
intent-preserving input perturbation and output distribution shift
```

This gives the project a clearer theoretical basis.

## 2. Elevate Sample Noise Correction into a Theoretical Contribution

Sample-noise correction should not be treated as only a technical detail. It can be framed as a conceptual contribution.

Suggested wording:

> Observed output variation contains at least two components: perturbation-induced variation and stochastic sampling variation. Without separating these components, prompt sensitivity may be overestimated.

Conceptual formula:

```text
observed drift = perturbation-induced drift + sampling noise
```

This supports the theoretical claim:

```text
prompt robustness should be measured relative to the model's own baseline variability
```

In other words, the study is not only asking whether outputs change. It is asking whether outputs change more than what would be expected from the model's natural sampling variability.

## 3. Use Robustness and Invariance Language

The proposal should connect prompt sensitivity to robustness and invariance.

Key framing:

- If two prompts express the same intent, an ideal model should preserve output invariance.
- If an intent-preserving perturbation changes semantic output or correctness, the model lacks robustness.
- Semantic drift measures output-level invariance.
- Correctness drift measures task-level functional robustness.

Suggested sentence:

> This study conceptualizes prompt robustness as the degree to which a model preserves semantic output and task correctness under intent-preserving prompt transformations.

This sentence is suitable for the Introduction or Conceptual Framework section.

## 4. Clarify the Theoretical Relationship Between RQ1 and RQ2

Currently, RQ1 and RQ2 may read like two parallel empirical questions. They should be presented as a connected theoretical sequence.

Suggested relationship:

```text
RQ1: Which perturbations break output invariance?
RQ2: Does broken output invariance transfer into task correctness changes?
```

More formal wording:

> RQ1 examines representational or output-level robustness, while RQ2 examines whether output-level instability has downstream functional consequences.

中文解释：

> RQ1 研究输出层面的稳定性，RQ2 研究这种输出不稳定是否进一步造成任务功能层面的正确性变化。

This makes the RQ structure much stronger.

## 5. Make the Literature Gap More Explicit

The current literature review mentions PromptBench, POSIX, Haase et al., and related work, but it should more explicitly synthesize the gap.

Suggested research gaps:

1. Existing prompt robustness work often focuses on adversarial or classification settings.
2. Existing sensitivity metrics often do not separate perturbation effects from sampling noise.
3. Few studies link semantic output drift to objective correctness change across task types.

Then state that this study addresses these gaps by combining:

```text
cross-task comparison
noise-corrected semantic drift
semantic drift + correctness drift linkage
```

This makes the theoretical contribution clearer than simply listing prior studies.

## 6. Keep Tornado Charts and ANOVA as Methods, Not Theory

Tornado charts, ANOVA, and Tukey HSD are useful, but they should not look like the theoretical core of the proposal.

Recommended positioning:

| Component | Role |
|---|---|
| Tornado charts | Visualization of relative perturbation effects |
| ANOVA / Tukey HSD | Exploratory statistical comparison across task and perturbation categories |
| Noise-corrected semantic drift | Core robustness metric |
| Correctness drift | Functional robustness outcome |

The theoretical center should remain:

```text
robustness / invariance / noise-corrected perturbation effect
```

## 7. Add a Conceptual Framework Section

The proposal would benefit from adding a short section before the Research Questions.

Suggested section:

```text
Conceptual Framework

This study is based on three concepts:

1. Intent-preserving prompt perturbation
2. Output invariance under perturbation
3. Noise-corrected prompt sensitivity

Observed output drift is treated as a combination of perturbation-induced drift and sampling noise. Therefore, prompt robustness should be evaluated by comparing perturbation-induced drift against the model's own repeated-sampling variability. The study further distinguishes semantic robustness from functional robustness: semantic robustness refers to the preservation of output meaning, while functional robustness refers to the preservation of task correctness.
```

中文版本：

```text
概念框架

本研究基于三个核心概念：

1. 保持意图不变的 prompt perturbation
2. perturbation 下的 output invariance
3. 经过 sample-noise correction 的 prompt sensitivity

本研究将 observed output drift 视为 perturbation-induced drift 和 sampling noise 的组合。因此，prompt robustness 不应只根据输出是否发生变化来衡量，而应与模型自身 repeated-sampling variability 进行比较。本研究进一步区分 semantic robustness 和 functional robustness：semantic robustness 指输出含义是否保持稳定，functional robustness 指任务正确性是否保持稳定。
```

## Recommended One-Sentence Reframing

The proposal can be reframed as:

> This study investigates LLM prompt robustness by treating prompt variation as intent-preserving input perturbation, measuring whether such perturbations break output invariance beyond the model's own sampling noise, and testing whether semantic instability transfers into functional correctness changes.

中文对应：

> 本研究将 prompt variation 视为保持意图不变的输入扰动，考察这些扰动是否会在超过模型自身 sampling noise 的程度上破坏 output invariance，并进一步检验 semantic instability 是否会传导为 functional correctness changes。

## Bottom Line

The proposal should move from:

```text
I change prompts and measure whether outputs change.
```

to:

```text
I study LLM robustness under intent-preserving input perturbations by separating perturbation-induced semantic drift from stochastic sampling noise and examining whether this drift predicts task-level correctness changes.
```

## 8. Add a Mathematical Problem Formulation

The proposal can be strengthened further by introducing a mathematical formulation of the problem.

The core theoretical question can be written as:

```text
How much does an intent-preserving prompt perturbation shift the model's output distribution,
after accounting for the model's own stochastic sampling noise?
```

This reframes the project as a quantitative robustness analysis rather than only an empirical prompt-comparison study.

### Prompt Perturbation as an Input Transformation

Let:

```text
p = original prompt
T_k(p) = the prompt after perturbation type k
M(p; s) = model output for prompt p under sampling randomness s
```

For the original prompt, repeated sampling gives:

```text
M(p; s_1), M(p; s_2), ..., M(p; s_n)
```

For the perturbed prompt, repeated sampling gives:

```text
M(T_k(p); s_1), M(T_k(p); s_2), ..., M(T_k(p); s_n)
```

The central question becomes:

```text
Does T_k shift the output distribution of M beyond what would be expected from sampling noise?
```

This gives the proposal a stronger mathematical description:

```text
intent-preserving input perturbation -> output distribution shift
```

### Semantic Distance

Define semantic distance between two outputs as:

```text
d(y_i, y_j) = 1 - cosine_similarity(embed(y_i), embed(y_j))
```

This transforms generated text into a measurable output space.

### Sample Noise

Original prompt sample noise:

```text
N_original = average pairwise distance among M(p; s_1), ..., M(p; s_n)
```

Perturbed prompt sample noise:

```text
N_perturbed = average pairwise distance among M(T_k(p); s_1), ..., M(T_k(p); s_n)
```

Combined sample-noise baseline:

```text
N = (N_original + N_perturbed) / 2
```

This estimates how much outputs vary even when the prompt is not changed.

### Raw Perturbation Drift

Raw drift is the average cross-distance between original and perturbed outputs:

```text
D_raw = average d(M(p; s_i), M(T_k(p); s_j)) for all i, j
```

This captures the observed difference between original-prompt outputs and perturbed-prompt outputs.

However, this observed drift includes both:

```text
perturbation-induced drift + sampling noise
```

### Noise-Corrected Drift

The core metric can be defined as:

```text
D_corrected = max(0, D_raw - N)
```

Interpretation:

```text
noise-corrected drift = observed cross-prompt drift - model's own sampling noise
```

This is the main mathematical tool for the proposal.

It allows the study to avoid overestimating prompt sensitivity by subtracting the model's natural repeated-sampling variability.

## 9. Reformulate RQ1 as Effect Decomposition

RQ1 can be written as an effect-decomposition problem:

```text
D_corrected ~ task + perturbation + task × perturbation
```

Or more formally:

```text
D_ijk = μ + α_i + β_j + (αβ)_ij + ε_ijk
```

where:

| Symbol | Meaning |
|---|---|
| `D_ijk` | noise-corrected drift for task i, perturbation j, case k |
| `μ` | grand mean |
| `α_i` | task effect |
| `β_j` | perturbation effect |
| `(αβ)_ij` | task × perturbation interaction |
| `ε_ijk` | residual case-level variation |

This gives Tornado Charts and ANOVA a clear theoretical role:

- Tornado charts visualize relative effect sizes.
- ANOVA tests whether task, perturbation, or their interaction explains variation in drift.
- Tukey HSD can be used as a post-hoc comparison between categories.

## 10. Reformulate RQ2 as Drift-to-Correctness Transfer

Define repeated-sampling correctness:

```text
C_original = mean correctness of outputs from p
C_perturbed = mean correctness of outputs from T_k(p)
```

Correctness drift:

```text
ΔC = |C_original - C_perturbed|
```

Harmful correctness drop:

```text
H = 1 if C_original > C_perturbed else 0
```

RQ2 can then be formulated as:

```text
Does D_corrected predict ΔC?
```

Or statistically:

```text
corr(D_corrected, ΔC) > 0
```

A regression-style formulation is:

```text
ΔC = γ_0 + γ_1 D_corrected + γ_2 task + γ_3 perturbation + ε
```

If:

```text
γ_1 > 0
```

then semantic drift can be interpreted as an indicator of correctness drift.

This creates a clear theoretical bridge:

```text
semantic instability -> functional correctness instability
```

## 11. Suggested Quantitative Tools

The proposal can introduce the following mathematical and statistical tools:

| Tool | Purpose |
|---|---|
| Output distribution shift | Treat prompt perturbation as a shift in model output distribution |
| Semantic embedding distance | Quantify text-output difference in embedding space |
| Noise-corrected drift | Separate perturbation-induced drift from sampling noise |
| Effect decomposition / ANOVA | Test task, perturbation, and interaction effects |
| Tukey HSD | Identify which task or perturbation groups differ after ANOVA |
| Spearman correlation | Test whether semantic drift ranks align with correctness drift ranks |
| Pearson correlation | Test linear association between semantic drift and correctness drift |
| Bootstrap confidence interval | Estimate stability of correlation results |
| Permutation test | Test whether observed association is stronger than random pairing |
| Tornado chart | Visualize relative perturbation effects |

## 12. Suggested Problem Formulation Text

The following paragraph can be added to the proposal:

```text
Problem Formulation

Let p denote an original prompt and T_k(p) denote an intent-preserving perturbation of type k. For a stochastic language model M, the output is represented as M(p; s), where s denotes sampling randomness. The observed difference between M(p; s) and M(T_k(p); s) contains both perturbation-induced variation and the model's intrinsic sampling variation. Therefore, this study defines prompt sensitivity as a noise-corrected semantic drift:

D_corrected = max(0, D_raw - N)

where D_raw is the average semantic distance between outputs generated from the original and perturbed prompts, and N is the average within-prompt sampling noise. This formulation allows the study to distinguish prompt-induced instability from natural stochastic variation. The study then examines whether D_corrected varies across task types and perturbation categories, and whether it predicts changes in task correctness.
```

中文概括：

```text
本研究将 prompt perturbation 建模为保持意图不变的输入扰动，将 LLM 输出视为随机变量。observed drift 同时包含 perturbation effect 和 sampling noise，因此需要用 noise-corrected drift 来估计真正由 prompt perturbation 引起的输出变化。随后通过 ANOVA 分析 task 和 perturbation 的效应，并通过相关分析检验 semantic drift 是否能指示 correctness drift。
```
