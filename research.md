# Pioneer Research Notes

## Project Direction

Working title: **Stability of Large Language Model Outputs Under Prompt Perturbation**.

Core idea: treat the prompt as the input, the LLM response as the output, and natural prompt changes as perturbations. The project asks whether output changes after prompt perturbation are real perturbation effects or ordinary stochastic variation from repeated generation.

Current proposal frames the study around three questions:

1. After correcting for sample noise, do different perturbation types produce a stable sensitivity ranking across factual QA, math reasoning, code generation, and open-ended writing?
2. For tasks with objective correctness, does semantic drift predict correctness changes?
3. Exploratory: are the sensitivity patterns consistent across an open-source model and a commercial API model?

Planned perturbation types:

- Paraphrasing
- Information reordering
- Formatting changes
- Context injection
- Surface noise such as typos or punctuation errors

Planned noise correction:

- Generate multiple outputs for each original and perturbed prompt.
- Estimate within-prompt sample noise from repeated generations under fixed decoding parameters.
- Compare between-prompt drift against that baseline.
- Treat a perturbation as meaningful only when its drift clearly exceeds the noise baseline.

## Key Question: Does Haase et al. Analyze Prompt Perturbation?

Reference: Jennifer Haase et al., **"Within-Model vs Between-Prompt Variability in Large Language Models for Creative Tasks"**.

Short answer: **yes, but not in exactly the same way as this project**.

Haase et al. do analyze prompt variation, including minor prompt changes that look close to prompt perturbations. Their prompt set includes:

- A direct baseline prompt.
- Strategic prompt variants: one-shot example, heuristic/domain prompt, anticipatory prompt, zero-shot chain-of-thought, and creative persona.
- Minor prompt variations: phrasing change, formatting tweak, information order change, and random spelling errors.

So the paper does include prompt-level manipulations such as paraphrasing, format constraint, information order, and typo robustness. These overlap strongly with this project's perturbation categories.

However, Haase et al.'s main research goal is **variance decomposition** in a creative task. They ask how much output variability is explained by model choice, prompt strategy, model-prompt interaction, and within-model stochasticity. They do not primarily ask whether a specific perturbation type creates a statistically significant output drift after subtracting a sample-noise baseline. They also focus on a single creative task, the Alternative Uses Task for a plastic bottle, rather than comparing multiple task types or linking drift to task correctness.

Best interpretation for this project:

- Haase et al. provide the methodological motivation for **sample noise**.
- They show that repeated generations under the same model-prompt condition can vary enough to confound single-sample prompt comparisons.
- Their prompt variants demonstrate that prompt wording and structure matter, but their analysis is not a dedicated cross-task, noise-corrected perturbation benchmark.
- This project extends their warning into a practical perturbation-evaluation method.

## How Haase et al. Supports This Project

Important conceptual claim:

- A prompt should not be treated as a deterministic program.
- A prompt shapes a distribution of likely outputs.
- Single-generation evaluations can conflate prompt effects with within-prompt sampling variability.

Useful empirical details from Haase et al.:

- They generated repeated outputs for each model-prompt pair.
- They decomposed variance into prompt, model, model-prompt interaction, and within-LLM variance.
- They report that within-LLM variance is non-trivial, roughly in the 10-34% range depending on outcome.
- For originality, prompt strategy explains substantial variance.
- For fluency, model choice and within-LLM variance dominate more strongly.

Useful mechanism distinction:

- Persona and heuristic prompts can elicit higher originality, especially in some models.
- Format constraints can reduce diversity by narrowing the output space.
- Minor variations such as phrasing, information order, and typos are closer to this project's prompt perturbations, but in Haase et al. they are analyzed as part of a broader prompt-strategy comparison.

## Literature Roles

### PromptRobust

Role in proposal: perturbation construction and robustness benchmark precedent.

PromptRobust evaluates robustness to prompt-level adversarial perturbations across tasks, models, and datasets. It is useful for defining attack or perturbation categories such as typos, synonym changes, sentence-level changes, and semantic changes. Its limitation for this project is that it focuses on adversarial robustness and does not isolate sampling noise through repeated generations.

### POSIX

Role in proposal: task-dependent prompt sensitivity.

POSIX motivates the possibility that prompt sensitivity is not uniform across tasks. This supports RQ1: the ranking of perturbation types may depend on whether the task is factual QA, math, code, or open-ended writing.

### What Did I Do Wrong?

Role in proposal: sensitivity and consistency metrics.

This paper provides a diagnostic framing for prompt sensitivity and consistency, especially in classification settings. It is useful for thinking about robustness beyond accuracy. Its limitation is that it is less directly suited to non-deterministic open-ended generation unless adapted with repeated sampling.

### Enhancing LLM Robustness to Perturbed Instructions

Role in proposal: everyday instruction perturbations.

This paper is useful because it studies perturbed instructions rather than only perturbed task samples. It supports the proposal's focus on natural, everyday prompt changes. Its limitation is that it is still more classification-oriented than the proposed cross-task semantic-drift design.

## Current Pilot Results

### Code and Open-Ended Writing Pilot

File: `results/sample_noise_report.md`

Setup:

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Samples per original/perturbed prompt: 3
- Decoding: temperature 0.7, top_p 0.9

Aggregate result:

- Average raw perturbation drift: 0.0882
- Average sample-noise baseline: 0.0563
- Average noise-corrected drift: 0.0319
- Estimated share of raw drift explainable by sample noise: 63.8%

Interpretation:

The pilot supports the core premise. A large part of the raw original-vs-perturbed difference can be explained by ordinary repeated-generation variability. The perturbation effect remains positive, but it is much smaller after correction.

### PromptRobust SST-2 Pilot

File: `results/sample_noise_report_promptrobust_sst2.md`

Setup:

- Suite: `promptrobust`
- Model: `gpt-4o-mini`
- Samples per original/perturbed prompt: 5
- Decoding: temperature 0.7, top_p 0.9

Result:

- Raw drift and sample-noise baseline are both effectively 0 for the tested items.

Interpretation:

For simple sentiment classification cases, the model outputs may be too stable or too short for embedding drift to reveal meaningful variation. This suggests that binary classification outputs need a task-specific metric, such as label flip rate or probability/logit-based uncertainty if available, rather than relying only on embedding distance between short labels.

### Hard SST-2 Pilot

File: `results/sample_noise_report_promptrobust_hard_sst2.md`

Setup:

- Suite: `promptrobust_hard`
- Model: `gpt-4o-mini`
- Samples per original/perturbed prompt: 8
- Decoding: temperature 0.9, top_p 0.95

Aggregate result:

- Average raw perturbation drift: 0.0084
- Average sample-noise baseline: 0.0084
- Average noise-corrected drift: 0.0000
- Estimated share of raw drift explainable by sample noise: 100.0%

Interpretation:

Even with harder sentiment examples and higher decoding randomness, the measured perturbation drift does not exceed the sample-noise baseline. For classification tasks, correctness or label stability may be the main outcome, while semantic drift is more informative for code and open-ended writing.

## Methodological Implications

1. The proposal's noise-baseline design is justified.
2. Haase et al. should be cited as the source motivating repeated sampling and sample-noise correction, not as a direct prior version of this exact perturbation study.
3. The project should distinguish between:
   - within-prompt sample noise,
   - between-prompt perturbation drift,
   - task correctness change.
4. Different tasks may need different primary metrics:
   - factual QA: answer match plus semantic similarity,
   - math: final-answer correctness plus reasoning/output drift,
   - code: unit-test pass/fail plus code embedding or edit distance,
   - open-ended writing: semantic similarity and possibly length/style/diversity metrics.
5. For classification tasks, short label outputs can make embedding drift uninformative. The project should either ask models for short explanations before labels or use label flip rate as the main metric.

## Implemented Python Pilot

File: `sample_noise_pilot.py`

The current Python script already implements the sample-noise calculation. It is not only a proposal-level idea.

Implemented suites:

- `proposal`: small hand-written pilot cases for factual QA, math, code generation, and open-ended writing.
- `promptrobust`: simple SST-2-style prompt typo cases.
- `promptrobust_hard`: harder SST-2-style cases with more ambiguous reviews and stronger typo perturbations.

Implemented calculation:

`corrected_drift = max(0, raw_between_prompt_drift - within_prompt_noise_baseline)`

For each item and perturbation type:

- Estimate the original prompt's within-prompt distance.
- Estimate the perturbed prompt's within-prompt distance.
- Average them to form the noise baseline.
- Estimate raw drift between original and perturbed outputs.
- Report corrected drift, signal-to-noise ratio, and a bootstrap test for whether raw drift exceeds noise.

The script computes cosine distance as `1 - cosine similarity` over normalized embeddings from `text-embedding-3-small`. The main helper functions are:

- `avg_pairwise_distance`: computes within-prompt sample noise from all pairs of repeated outputs under the same prompt.
- `avg_cross_distance`: computes raw original-vs-perturbed drift from all cross-pairs.
- `bootstrap_probability_between_exceeds_noise`: estimates how often between-prompt drift exceeds the resampled within-prompt noise baseline.

The script writes:

- `results/generations*.csv`: all generated outputs.
- `results/noise_metrics*.csv`: per-case numeric metrics.
- `results/noise_metrics*.json`: full structured metrics.
- `results/sample_noise_report*.md`: readable summary report.

This turns Haase et al.'s conceptual warning into the operational contribution of the Pioneer project.
