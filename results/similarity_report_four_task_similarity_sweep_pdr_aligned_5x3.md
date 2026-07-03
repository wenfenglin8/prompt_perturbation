# Four-Task Similarity Sweep, PDR-Aligned Perturbations

- Batch count: `5`
- Tasks: `factual_qa, math_reasoning, code_generation, open_ended_writing`
- Datasets: `SQuAD V2, MATH, HumanEval, Alpaca`
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise`
- Perturbation alignment: same taxonomy as `pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md`, applied to instruction text only.
- Total generation rows: `600`
- Total metric rows: `100`

## Reference Alignment and Scope

This run is **reference-aligned**, but it is not a direct reproduction of one
single reference paper. The datasets, perturbation types, and correction method
come from the following mapping.

### Dataset Alignment

| task | dataset in this run | reference alignment | status |
|---|---|---|---|
| factual_qa | SQuAD V2 | PromptRobust / PromptBench | Directly aligned dataset family for factual QA |
| math_reasoning | MATH | PromptRobust / PromptBench | Directly aligned dataset family for mathematical reasoning |
| code_generation | HumanEval | External supplement | Not covered by the five reviewed prompt-perturbation papers; added to preserve the four-task project design |
| open_ended_writing | Alpaca | POSIX | Aligned with POSIX open-ended / instruction-following evaluation setting |

Important boundary:

```text
SQuAD V2 and MATH are aligned with PromptRobust / PromptBench.
Alpaca is aligned with POSIX.
HumanEval is an external supplement, not a dataset from the five reviewed papers.
```

Therefore, this experiment should not be described as using datasets from a
single paper. A precise description is:

```text
The four-task dataset selection combines PromptRobust / PromptBench-aligned datasets
for factual QA and mathematical reasoning, POSIX-aligned Alpaca examples for open-ended
writing, and HumanEval as an external code-generation supplement.
```

### Perturbation Alignment

The perturbation taxonomy in this run is the same as the three-task PDR
validation report:

```text
paraphrase
reordering
formatting
context_injection
surface_noise
```

The perturbations are applied to the **task instruction only**. The task content
itself is kept unchanged:

```text
SQuAD passage/question body: unchanged
MATH problem statement: unchanged
HumanEval function prompt/body: unchanged
Alpaca instruction content/input body: unchanged
```

The perturbation-reference mapping is:

| perturbation | implementation in this project | closest reference basis | note |
|---|---|---|---|
| paraphrase | LLM-generated intent-preserving rewrite of the instruction | PromptRobust / PromptBench prompt rephrasing; POSIX intent-aligned prompt variants | Directly matches the natural prompt-variation idea |
| reordering | LLM-generated semantically equivalent clause/order change | PromptRobust-style information-order perturbation; Haase et al. prompt order variation motivation | Implemented as a controlled project variant, not a verbatim algorithm from one paper |
| formatting | POSIX-style prompt template wrapper, e.g. `Question: ... Answer:` | POSIX template variation | Directly tied to POSIX prompt-template sensitivity |
| context_injection | Appends irrelevant context, `and false is not true` | PromptRobust-style sentence-level irrelevant-context perturbation | Natural non-adversarial context injection |
| surface_noise | Deterministic typo / character-level noise on non-essential instruction words | PromptRobust typo/noise perturbations; Haase et al. typo robustness motivation | Applied only to instruction words, not task facts or code body |

Thus, the perturbation scheme is best described as:

```text
a PDR-aligned, reference-informed natural perturbation taxonomy, combining
PromptRobust / PromptBench-style prompt perturbations, POSIX-style formatting
variation, and Haase et al.-motivated repeated-sampling correction.
```

It should **not** be described as an exact reproduction of PromptRobust's full
adversarial prompt-generation pipeline or of POSIX's likelihood-based Prompt
Sensitivity Index. This run uses embedding-based semantic drift and
sample-noise correction instead.

### Evaluation Alignment

The primary metric in this report is **Noise-Corrected Semantic Drift**:

```text
noise_corrected_drift = max(0, raw_perturbation_drift - noise_baseline)
```

Its reference basis is:

| component | reference basis |
|---|---|
| semantic similarity / semantic coherence between outputs | POSIX semantic coherence / response-similarity motivation |
| repeated generations and within-prompt sample-noise baseline | Haase et al. within-model / within-prompt variability |
| PDR-style perturbation taxonomy and auxiliary correctness framing | PromptRobust / PromptBench and related perturbed-instruction robustness work |

In short:

```text
Datasets:
SQuAD V2 and MATH -> PromptRobust / PromptBench
Alpaca -> POSIX
HumanEval -> external supplement

Perturbations:
PDR-aligned project taxonomy based on PromptRobust / PromptBench + POSIX,
with sample-noise correction motivated by Haase et al.
```

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | paraphrase | 5 | 0.0674 | 0.0201 | 0.0539 | 0.0338 |
| factual_qa | SQuAD V2 | reordering | 5 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | SQuAD V2 | formatting | 5 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | SQuAD V2 | context_injection | 5 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | SQuAD V2 | surface_noise | 5 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| math_reasoning | MATH | paraphrase | 5 | 0.0520 | 0.0467 | 0.0577 | 0.0121 |
| math_reasoning | MATH | reordering | 5 | 0.0618 | 0.0429 | 0.0457 | 0.0032 |
| math_reasoning | MATH | formatting | 5 | 0.0433 | 0.0613 | 0.0528 | 0.0011 |
| math_reasoning | MATH | context_injection | 5 | 0.0831 | 0.0532 | 0.0512 | 0.0018 |
| math_reasoning | MATH | surface_noise | 5 | 0.0328 | 0.0616 | 0.0547 | 0.0007 |
| code_generation | HumanEval | paraphrase | 5 | 0.0366 | 0.0077 | 0.0445 | 0.0369 |
| code_generation | HumanEval | reordering | 5 | 0.0782 | 0.0173 | 0.0638 | 0.0465 |
| code_generation | HumanEval | formatting | 5 | 0.0500 | 0.0186 | 0.0565 | 0.0382 |
| code_generation | HumanEval | context_injection | 5 | 0.0634 | 0.0266 | 0.0299 | 0.0051 |
| code_generation | HumanEval | surface_noise | 5 | 0.0403 | 0.0128 | 0.0457 | 0.0333 |
| open_ended_writing | Alpaca | paraphrase | 5 | 0.1375 | 0.0872 | 0.0889 | 0.0066 |
| open_ended_writing | Alpaca | reordering | 5 | 0.0516 | 0.0889 | 0.0916 | 0.0066 |
| open_ended_writing | Alpaca | formatting | 5 | 0.1479 | 0.0980 | 0.1523 | 0.0543 |
| open_ended_writing | Alpaca | context_injection | 5 | 0.0990 | 0.0719 | 0.0857 | 0.0161 |
| open_ended_writing | Alpaca | surface_noise | 5 | 0.1647 | 0.0618 | 0.1597 | 0.1016 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | paraphrase | 0.0338 | 0.0539 |
| factual_qa | 2 | reordering | 0.0000 | 0.0000 |
| factual_qa | 3 | context_injection | 0.0000 | 0.0000 |
| factual_qa | 4 | formatting | 0.0000 | 0.0000 |
| factual_qa | 5 | surface_noise | 0.0000 | 0.0000 |
| math_reasoning | 1 | paraphrase | 0.0121 | 0.0577 |
| math_reasoning | 2 | reordering | 0.0032 | 0.0457 |
| math_reasoning | 3 | context_injection | 0.0018 | 0.0512 |
| math_reasoning | 4 | formatting | 0.0011 | 0.0528 |
| math_reasoning | 5 | surface_noise | 0.0007 | 0.0547 |
| code_generation | 1 | reordering | 0.0465 | 0.0638 |
| code_generation | 2 | formatting | 0.0382 | 0.0565 |
| code_generation | 3 | paraphrase | 0.0369 | 0.0445 |
| code_generation | 4 | surface_noise | 0.0333 | 0.0457 |
| code_generation | 5 | context_injection | 0.0051 | 0.0299 |
| open_ended_writing | 1 | surface_noise | 0.1016 | 0.1597 |
| open_ended_writing | 2 | formatting | 0.0543 | 0.1523 |
| open_ended_writing | 3 | context_injection | 0.0161 | 0.0857 |
| open_ended_writing | 4 | paraphrase | 0.0066 | 0.0889 |
| open_ended_writing | 5 | reordering | 0.0066 | 0.0916 |

## Effect of Sample-Noise Correction

This experiment compares raw repeated-sampling similarity drift with the
noise-corrected drift:

```text
noise_corrected_drift = max(0, raw_perturbation_drift - noise_baseline)
```

Across all task-perturbation groups, sample-noise correction substantially
reduces the estimated perturbation effect:

```text
Average raw similarity drift:       0.0567
Average noise-corrected drift:      0.0199
Average reduction after correction: 0.0368
Share removed by sample noise:      64.9%
```

By task:

| task | average raw drift | average corrected drift | reduction | share removed by sample noise |
|---|---:|---:|---:|---:|
| factual_qa | 0.0108 | 0.0068 | 0.0040 | 37.3% |
| math_reasoning | 0.0524 | 0.0038 | 0.0486 | 92.8% |
| code_generation | 0.0481 | 0.0320 | 0.0161 | 33.4% |
| open_ended_writing | 0.1157 | 0.0370 | 0.0786 | 68.0% |

The strongest correction effect appears in **math_reasoning**. Its raw drift
is `0.0524`, but the corrected drift falls to `0.0038`, meaning that most of
the apparent perturbation-induced semantic drift is explainable by ordinary
repeated-generation variability.

Open-ended writing also shows a large reduction, from `0.1157` raw drift to
`0.0370` corrected drift. This is consistent with the expectation that
open-ended generation has a larger within-prompt variability baseline.

Code generation is less reduced by correction than math and open-ended writing.
Its average drift decreases from `0.0481` to `0.0320`, so a larger share of the
observed drift remains after accounting for sample noise.

Main interpretation:

```text
The uncorrected similarity drift substantially overestimates perturbation-induced output change.
After subtracting the within-prompt sample-noise baseline, the average drift decreases from
0.0567 to 0.0199, indicating that about 64.9% of the apparent perturbation effect can be
attributed to ordinary repeated-generation variability.
```

Therefore, sample-noise correction is necessary for this four-task similarity
analysis. Without correction, raw similarity drift can misattribute stochastic
generation variability to prompt-perturbation sensitivity, especially for math
reasoning and open-ended writing.
