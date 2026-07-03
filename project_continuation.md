# Project Continuation Notes

Date: 2026-06-28

## Current Project

Project working title:

**Stability of Large Language Model Outputs Under Prompt Perturbation**

The project studies whether output differences after prompt perturbation are true perturbation effects or can be explained by ordinary repeated-generation variability, called sample noise in the current project notes.

Core operational idea:

```text
noise_corrected_drift = raw_perturbation_drift - sample_noise_baseline
```

The clipped version used in reports is:

```text
noise_corrected_drift_clipped = max(0, raw_perturbation_drift - sample_noise_baseline)
```

## Discussion Summary

### Haase et al. and Sample Noise

Paper discussed:

**Within-Model vs Between-Prompt Variability in Large Language Models for Creative Tasks**

Main interpretation:

Haase et al. already provide the key motivation for sample noise. Their central point is that repeated generations from the same model and same prompt can vary enough that single-sample prompt comparisons may confuse prompt effects with ordinary stochastic output variability.

How the paper relates to this project:

- Haase et al. use repeated generations and variance decomposition.
- They decompose output variability into model effects, prompt effects, model-prompt interaction, and within-LLM variability.
- Their within-LLM variability is the methodological basis for this project's sample-noise baseline.

### Does Haase et al. Analyze Prompt Perturbation?

Answer:

**Yes, partly, but not as a dedicated prompt perturbation study.**

Their prompt set includes prompt variants that resemble perturbations:

- P7: phrasing variation / paraphrase
- P8: formatting tweak / format constraint
- P9: information order change
- P10: random spelling errors / typo robustness

However, their main goal is not to rank perturbation types or test perturbation robustness across tasks. Their main goal is variance decomposition in a creative task.

This project's distinction:

- It uses Haase et al. to justify repeated sampling and sample-noise correction.
- It extends that idea to prompt perturbation evaluation.
- It asks whether specific perturbation types produce drift beyond the within-prompt sample-noise baseline.
- It plans to compare across task types and, where possible, relate semantic drift to correctness changes.

Suggested proposal wording:

```text
Haase et al. include several prompt variants that resemble prompt perturbations, such as phrasing changes, formatting constraints, information-order changes, and spelling errors. However, their main contribution is not a dedicated prompt-perturbation analysis, but a variance-decomposition framework showing that within-model sampling variability can be large enough to confound single-sample prompt comparisons. The present study extends this insight by using repeated generations to construct a sample-noise baseline and by testing whether specific prompt perturbation types produce output drift beyond that baseline across multiple task types.
```

## Existing Python Script

File:

`sample_noise_pilot.py`

The script already implements sample-noise calculation.

Important functions:

- `avg_pairwise_distance(vectors)`: calculates within-prompt sample noise using all pairwise distances among repeated outputs.
- `avg_cross_distance(a, b)`: calculates raw original-vs-perturbed drift using all original/perturbed output pairs.
- `bootstrap_probability_between_exceeds_noise(...)`: estimates how often between-prompt drift exceeds the resampled noise baseline.

Implemented suites:

- `proposal`: hand-written pilot cases for factual QA, math reasoning, code generation, and open-ended writing.
- `promptrobust`: PromptRobust-style SST-2 sentiment examples with prompt typos.
- `promptrobust_hard`: harder SST-2-style examples with more ambiguous reviews and stronger typo perturbation.

Main outputs:

- `results/generations*.csv`
- `results/noise_metrics*.csv`
- `results/noise_metrics*.json`
- `results/sample_noise_report*.md`

## Commands Run in This Session

### Proposal Pilot Rerun

Command:

```powershell
python sample_noise_pilot.py --case-ids code_01,writing_01 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag rerun
```

Output files:

- `results/generations_rerun.csv`
- `results/noise_metrics_rerun.csv`
- `results/noise_metrics_rerun.json`
- `results/sample_noise_report_rerun.md`

Result:

```text
Average raw perturbation drift:        0.1066
Average sample-noise baseline:         0.0524
Average noise-corrected drift:         0.0542
Share explainable by sample noise:     49.2%
```

Per case:

```text
code_01:
sample-noise baseline = 0.0362
raw drift             = 0.1120
corrected drift       = 0.0759

writing_01:
sample-noise baseline = 0.0687
raw drift             = 0.1012
corrected drift       = 0.0326
```

### PromptRobust Suite Rerun

Command:

```powershell
python sample_noise_pilot.py --suite promptrobust --samples 5 --temperature 0.7 --top-p 0.9 --output-tag promptrobust_rerun
```

Output files:

- `results/generations_promptrobust_rerun.csv`
- `results/noise_metrics_promptrobust_rerun.csv`
- `results/noise_metrics_promptrobust_rerun.json`
- `results/sample_noise_report_promptrobust_rerun.md`

Result:

```text
Average raw perturbation drift:    0.0000
Average sample-noise baseline:     0.0000
Average noise-corrected drift:     0.0000
```

Interpretation:

The ordinary PromptRobust-style SST-2 examples produced almost completely stable short-label outputs. Embedding drift is therefore near zero and not very informative for this classification setting.

### PromptRobust Hard Suite Rerun

Command:

```powershell
python sample_noise_pilot.py --suite promptrobust_hard --samples 8 --temperature 0.9 --top-p 0.95 --output-tag promptrobust_hard_rerun
```

Output files:

- `results/generations_promptrobust_hard_rerun.csv`
- `results/noise_metrics_promptrobust_hard_rerun.csv`
- `results/noise_metrics_promptrobust_hard_rerun.json`
- `results/sample_noise_report_promptrobust_hard_rerun.md`

Result:

```text
Average raw perturbation drift:    0.0211
Average sample-noise baseline:     0.0229
Average noise-corrected drift:     0.0000
Share explainable by sample noise: 108.6%
```

Per case summary:

```text
promptrobust_hard_sst2_01:
sample-noise baseline = 0.0916
raw drift             = 0.0844
corrected drift       = 0.0000

promptrobust_hard_sst2_02:
sample-noise baseline = 0.0000
raw drift             = 0.0000
corrected drift       = 0.0000

promptrobust_hard_sst2_03:
sample-noise baseline = 0.0000
raw drift             = 0.0000
corrected drift       = 0.0000

promptrobust_hard_sst2_04:
sample-noise baseline = 0.0000
raw drift             = 0.0000
corrected drift       = 0.0000
```

Interpretation:

The hard PromptRobust-style set produces some measurable drift, but the raw drift does not exceed the sample-noise baseline on average. Therefore, under the current metric, the prompt typo perturbation does not show a robust perturbation-specific effect beyond sample noise.

## Methodological Takeaways

1. The sample-noise baseline is already implemented and can be used as the project's main methodological contribution.
2. Haase et al. should be cited as the motivation for repeated sampling and within-prompt noise correction.
3. PromptRobust-style SST-2 classification outputs are often too short and stable for embedding drift to be informative.
4. For classification tasks, future analysis should add label-level metrics:
   - label flip rate,
   - correctness change,
   - optional explanation drift if prompts ask for a short explanation plus final label.
5. For code generation and open-ended writing, embedding drift is more informative because outputs are longer and more variable.

## Recommended Next Steps

1. Add label extraction and label flip rate to `sample_noise_pilot.py` for SST-2 / classification tasks.
2. Add a mode where classification prompts require:

```text
Give a one-sentence explanation, then answer with exactly one label: positive or negative.
```

This would make semantic drift measurable while still preserving correctness evaluation.

3. Expand from the current small PromptRobust-style hand-written cases to a larger subset of actual PromptRobust / SST-2 examples.
4. Keep reporting both:
   - semantic drift metrics,
   - task correctness or label stability metrics.

## Current Important Files

- `research.md`: broader research notes and literature positioning.
- `project_continuation.md`: this continuation record.
- `sample_noise_pilot.py`: Python implementation of sample-noise calculation.
- `results/sample_noise_report_rerun.md`: proposal pilot rerun result.
- `results/sample_noise_report_promptrobust_rerun.md`: PromptRobust-style SST-2 rerun result.
- `results/sample_noise_report_promptrobust_hard_rerun.md`: harder PromptRobust-style rerun result.

## 2026-06-29 Update: PromptRobust SQuAD V2 + MATH Run

The user asked to use the PromptRobust paper's relevant datasets for:

- factual QA: SQuAD V2
- math reasoning: Mathematics / MATH

The script was updated to add a new suite:

```text
promptrobust_squad_math
```

Implementation details:

- SQuAD V2 is loaded from HuggingFace as `squad_v2`.
- MATH is loaded from HuggingFace as `DigitalLearningGmbH/MATH-lighteval`, which provides MATH-style `problem`, `solution`, `level`, and `type` fields.
- The run uses real dataset samples, not hand-written examples.
- The prompt perturbation is PromptRobust-style character-level instruction noise: typos are injected into the instruction text while the task sample itself is kept unchanged.

Command run:

```powershell
python sample_noise_pilot.py --suite promptrobust_squad_math --dataset-cases-per-task 2 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag promptrobust_squad_math
```

Output files:

- `results/generations_promptrobust_squad_math.csv`
- `results/noise_metrics_promptrobust_squad_math.csv`
- `results/noise_metrics_promptrobust_squad_math.json`
- `results/sample_noise_report_promptrobust_squad_math.md`

Aggregate result:

```text
Average raw perturbation drift:        0.0119
Average sample-noise baseline:         0.0111
Average noise-corrected drift:         0.0007
Share explainable by sample noise:     93.9%
```

Per-case result:

```text
promptrobust_squad_v2_01:
sample-noise baseline = 0.0000
raw drift             = 0.0000
corrected drift       = 0.0000

promptrobust_squad_v2_02:
sample-noise baseline = 0.0000
raw drift             = 0.0000
corrected drift       = 0.0000

promptrobust_math_01:
sample-noise baseline = 0.0267
raw drift             = 0.0282
corrected drift       = 0.0016

promptrobust_math_02:
sample-noise baseline = 0.0178
raw drift             = 0.0192
corrected drift       = 0.0013
```

Interpretation:

On this small run, SQuAD V2 outputs were almost deterministic, so both sample noise and perturbation drift were effectively zero. MATH outputs had visible sample noise, but the raw perturbation drift was only slightly above the noise baseline. Overall, about 93.9% of raw drift was explainable by sample noise, leaving very small corrected drift.

Important caveat:

This run uses the same dataset families as PromptRobust for factual QA and math, and it uses PromptRobust-style character-level prompt perturbation. It does not reproduce the full PromptRobust adversarial prompt generation pipeline or full dataset scale.

## 2026-06-29 Update: Dataset Mapping Log

The dataset-mapping discussion was saved to:

```text
log_data_set.txt
```

Main conclusion:

- PromptRobust provides the best matches for factual QA and math reasoning through SQuAD V2 and MATH.
- POSIX provides the best match for open-ended writing / open-ended generation through Alpaca.
- None of the five current reference papers provides a strong code-generation dataset such as HumanEval or MBPP.

Recommended route:

```text
factual QA:          PromptRobust / SQuAD V2
math reasoning:      PromptRobust / MATH
code generation:     external HumanEval or MBPP
open-ended writing:  POSIX / Alpaca or self-designed prompts
```

## 2026-06-29 Update: POSIX MMLU + BBH Run

The user asked to use the POSIX-related MMLU / BBH datasets for factual QA / reasoning / multiple-choice reasoning and compute sample noise.

The script was updated to add a new suite:

```text
posix_mmlu_bbh
```

Implementation details:

- MMLU is loaded from HuggingFace as `cais/mmlu`, config `all`.
- BBH is loaded from HuggingFace as `maveriq/bigbenchhard`, config `logical_deduction_three_objects`.
- MMLU uses a multiple-choice template variation inspired by POSIX prompt-template perturbation.
- BBH uses a reasoning-instruction rephrasing perturbation.
- This is POSIX-style prompt variation, not a full reproduction of the POSIX likelihood-based metric.

Command run:

```powershell
python sample_noise_pilot.py --suite posix_mmlu_bbh --dataset-cases-per-task 2 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag posix_mmlu_bbh
```

Output files:

- `results/generations_posix_mmlu_bbh.csv`
- `results/noise_metrics_posix_mmlu_bbh.csv`
- `results/noise_metrics_posix_mmlu_bbh.json`
- `results/sample_noise_report_posix_mmlu_bbh.md`

Aggregate result:

```text
Average raw perturbation drift:        0.0349
Average sample-noise baseline:         0.0349
Average noise-corrected drift:         0.0000
Share explainable by sample noise:     100.0%
```

Per-case result:

```text
posix_mmlu_01:
sample-noise baseline = 0.0000
raw drift             = 0.0000
corrected drift       = 0.0000

posix_mmlu_02:
sample-noise baseline = 0.0000
raw drift             = 0.0000
corrected drift       = 0.0000

posix_bbh_logical_deduction_01:
sample-noise baseline = 0.0084
raw drift             = 0.0084
corrected drift       = 0.0000

posix_bbh_logical_deduction_02:
sample-noise baseline = 0.1314
raw drift             = 0.1313
corrected drift       = 0.0000
```

Interpretation:

On this small MMLU/BBH run, MMLU multiple-choice outputs were essentially deterministic. BBH logical-deduction outputs had measurable variability, especially one case with a high sample-noise baseline, but the raw original-vs-perturbed drift did not exceed the within-prompt noise baseline. Therefore, the corrected perturbation effect was zero in the aggregate report.

## 2026-06-29 End-of-Day Progress Summary

Today's main goal was to move beyond hand-written pilot cases and compute sample noise on datasets that are closer to the reference literature and the proposal's four-task design.

Completed work:

1. Confirmed dataset alignment across the five reference papers.

   Main conclusion:

   ```text
   factual QA:          PromptRobust / SQuAD V2
   math reasoning:      PromptRobust / MATH
   code generation:     external HumanEval or MBPP needed
   open-ended writing:  POSIX / Alpaca or self-designed prompts
   ```

   This mapping was saved to:

   ```text
   log_data_set.txt
   ```

2. Extended `sample_noise_pilot.py` with dataset-backed suites.

   New suite:

   ```text
   promptrobust_squad_math
   ```

   It loads:

   - SQuAD V2 from `squad_v2`
   - MATH from `DigitalLearningGmbH/MATH-lighteval`

   New suite:

   ```text
   posix_mmlu_bbh
   ```

   It loads:

   - MMLU from `cais/mmlu`, config `all`
   - BBH from `maveriq/bigbenchhard`, config `logical_deduction_three_objects`

3. Ran PromptRobust-style SQuAD V2 + MATH sample-noise experiment.

   Command:

   ```powershell
   python sample_noise_pilot.py --suite promptrobust_squad_math --dataset-cases-per-task 2 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag promptrobust_squad_math
   ```

   Aggregate result:

   ```text
   Average raw perturbation drift:        0.0119
   Average sample-noise baseline:         0.0111
   Average noise-corrected drift:         0.0007
   Share explainable by sample noise:     93.9%
   ```

   Interpretation:

   SQuAD V2 outputs were nearly deterministic. MATH outputs showed visible sample noise, but the perturbation-specific drift after correction was very small.

4. Ran POSIX-style MMLU + BBH sample-noise experiment.

   Command:

   ```powershell
   python sample_noise_pilot.py --suite posix_mmlu_bbh --dataset-cases-per-task 2 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag posix_mmlu_bbh
   ```

   Aggregate result:

   ```text
   Average raw perturbation drift:        0.0349
   Average sample-noise baseline:         0.0349
   Average noise-corrected drift:         0.0000
   Share explainable by sample noise:     100.0%
   ```

   Interpretation:

   MMLU multiple-choice outputs were essentially deterministic. BBH logical-deduction outputs had measurable natural variability, but raw drift did not exceed the sample-noise baseline.

Current overall finding:

Across the new dataset-backed runs, the same pattern holds: raw original-vs-perturbed drift can substantially overstate the effect of prompt perturbation. Once within-prompt sample noise is subtracted, the corrected perturbation effect is very small or zero in these small pilot samples.

Important caveat:

The current runs use very small dataset subsets:

```text
2 SQuAD V2 examples
2 MATH examples
2 MMLU examples
2 BBH examples
```

These are method-validation runs, not final statistical evidence. The next stage should increase the number of cases per task.

Files created or updated today:

- `sample_noise_pilot.py`
- `log_data_set.txt`
- `project_continuation.md`
- `results/sample_noise_report_promptrobust_squad_math.md`
- `results/noise_metrics_promptrobust_squad_math.json`
- `results/generations_promptrobust_squad_math.csv`
- `results/sample_noise_report_posix_mmlu_bbh.md`
- `results/noise_metrics_posix_mmlu_bbh.json`
- `results/generations_posix_mmlu_bbh.csv`

Suggested next steps for tomorrow:

1. Increase sample size per dataset-backed task, for example:

   ```text
   --dataset-cases-per-task 5 or 10
   ```

2. Add POSIX / Alpaca open-ended generation to cover the proposal's open-ended writing task more directly.

3. Add a code-generation dataset, preferably HumanEval or MBPP, because none of the five current reference papers covers code generation strongly.

4. Add task-specific correctness metrics:

   - SQuAD V2: answer match / semantic answer correctness
   - MATH: final answer extraction and exact match
   - MMLU / BBH: option-letter accuracy
   - code generation: unit tests once HumanEval or MBPP is added

5. Keep recording each run's command, output files, aggregate result, and interpretation in this file.

## 2026-06-29 Morning Discussion Update

The morning discussion focused on turning the literature review into a concrete experiment plan for comparing prompt-perturbation evaluation with and without sample-noise correction.

### Perturbation Scheme for the Four Project Tasks

Based on `project_perturbation_plan_by_task.md`, the project should use natural prompt perturbations rather than adversarial greedy-search attacks as the main experiment design.

Recommended perturbation types:

```text
P1 paraphrasing
P2 formatting changes
P3 information reordering
P4 surface noise such as typos or punctuation errors
P5 context injection / irrelevant sentence insertion
```

Task-specific constraints:

- Factual QA: perturb the instruction, not the passage, question entities, dates, or numbers.
- Math reasoning: perturb only the instruction template; do not perturb problem statements, formulas, variables, units, or numeric conditions.
- Code generation: perturb natural-language instruction only; do not perturb function signatures, examples, test-relevant constraints, or code blocks.
- Open-ended writing: all five perturbation types are usable because there is no single ground-truth answer, but repeated sampling is especially important.

Main framing:

```text
The project is not a direct adversarial-attack benchmark. It studies natural prompt perturbation under repeated sampling, then asks whether the observed between-prompt drift remains after subtracting within-prompt sample noise.
```

### Reference-Based Evaluation Criteria

Based on `reference_based_eval_criteria_by_task.md`, the project should present its evaluation criteria as adaptations of the five reference papers, not as newly invented metrics.

Reference-metric mapping:

```text
correctness -> PDR / APDR / Micro-F1
similarity  -> sensitivity / semantic coherence / response diversity / within-LLM variance
```

Recommended criteria by task:

| Task | Main criteria | Reference source |
|---|---|---|
| Factual QA | PDR based on answer correctness; sensitivity; semantic preservation | PromptRobust; Enhancing LLM Robustness; What Did I Do Wrong |
| Math reasoning | PDR based on final-answer correctness; sensitivity; semantic preservation | PromptRobust; Enhancing LLM Robustness |
| Code generation | PDR based on unit-test pass rate; sensitivity / consistency | PromptRobust-style PDR logic; What Did I Do Wrong |
| Open-ended writing | Sensitivity; semantic coherence; response diversity; originality / fluency where applicable | POSIX; Haase et al. |

The important methodological claim is:

```text
The contribution is not a new evaluation criterion. The contribution is an apple-to-apple comparison of existing reference criteria before and after sample-noise calibration.
```

### Dataset Selection

Based on `dataset_selection_for_noise_correction_comparison.md`, the dataset plan is:

| Task | Dataset | Source |
|---|---|---|
| Factual QA | SQuAD V2 | PromptRobust / PromptBench |
| Math reasoning | MATH / Mathematics | PromptRobust / PromptBench |
| Code generation | HumanEval | External supplement |
| Open-ended writing | Alpaca | POSIX |

Important limitation:

```text
None of the five reviewed papers provides a dedicated code-generation dataset. Therefore, HumanEval is added externally to retain the four-task design.
```

The comparison must hold fixed:

```text
same dataset
same clean prompt
same perturbed prompt
same perturbation type
same model
same decoding parameters
same evaluation criterion
```

The only methodological difference should be:

```text
without correction: single clean output vs single perturbed output
with correction: repeated clean outputs vs repeated perturbed outputs, with within-prompt sample noise estimated and subtracted
```

### Four-Task Smoke Validation

The script `sample_noise_pilot.py` was updated with a new suite:

```text
reference_four_task
```

This suite loads one small dataset-backed case per task:

- SQuAD V2 for factual QA
- MATH / Mathematics for math reasoning
- HumanEval for code generation
- Alpaca for open-ended writing

The script was also updated to report:

```text
uncorrected_single_drift
raw_perturbation_drift
noise_baseline
noise_corrected_drift
```

Command run:

```powershell
python sample_noise_pilot.py --suite reference_four_task --dataset-cases-per-task 1 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag reference_four_task_smoke
```

Output files:

- `results/generations_reference_four_task_smoke.csv`
- `results/noise_metrics_reference_four_task_smoke.csv`
- `results/noise_metrics_reference_four_task_smoke.json`
- `results/sample_noise_report_reference_four_task_smoke.md`
- `sample_noise_correction_validation.md`

Aggregate result:

```text
Average uncorrected single-sample drift: 0.2392
Average raw perturbation drift:          0.2253
Average sample-noise baseline:           0.0616
Average noise-corrected drift:           0.1637
Share explainable by sample noise:       27.4%
```

Per-task result:

| Case | Task | Dataset | Uncorrected single drift | Noise baseline | Raw drift | Corrected drift |
|---|---|---|---:|---:|---:|---:|
| `ref_squad_v2_01` | factual QA | SQuAD V2 | 0.5556 | 0.0840 | 0.5286 | 0.4446 |
| `ref_math_01` | math reasoning | MATH | 0.0483 | 0.0443 | 0.0450 | 0.0007 |
| `ref_humaneval_01` | code generation | HumanEval | 0.2516 | 0.0322 | 0.2246 | 0.1924 |
| `ref_alpaca_01` | open-ended writing | Alpaca | 0.1014 | 0.0860 | 0.1030 | 0.0170 |

Interpretation:

The smoke validation supports the core premise. Without sample-noise correction, raw prompt-perturbation drift can overestimate the perturbation effect. In this run, about 27.4% of the average raw drift was explainable by within-prompt sample noise.

Task-specific interpretation:

- SQuAD V2 and HumanEval still had substantial corrected drift, suggesting perturbation-specific output change in these examples.
- MATH had raw drift almost equal to the sample-noise baseline, so the corrected perturbation effect was nearly zero.
- Alpaca open-ended writing had high within-prompt variability, so most raw drift was explained by sample noise.

Important caveat:

This is only a method-validation smoke test:

- one example per task,
- three repeated generations per clean / perturbed prompt,
- similarity / semantic drift only,
- no task-specific correctness evaluation yet.

### Files Created or Updated This Morning

- `project_perturbation_plan_by_task.md`
- `reference_based_eval_criteria_by_task.md`
- `dataset_selection_for_noise_correction_comparison.md`
- `perturbation_methods_eval_criteria.md`
- `sample_noise_pilot.py`
- `sample_noise_correction_validation.md`
- `project_continuation.md`
- `results/generations_reference_four_task_smoke.csv`
- `results/noise_metrics_reference_four_task_smoke.csv`
- `results/noise_metrics_reference_four_task_smoke.json`
- `results/sample_noise_report_reference_four_task_smoke.md`

### Next Steps

1. Add task-specific correctness metrics:

   - SQuAD V2: answer match or semantic answer correctness.
   - MATH: final-answer extraction and exact match.
   - HumanEval: unit-test pass rate.
   - Alpaca: no single correctness target; keep semantic coherence, response diversity, sensitivity, and possibly fluency.

2. Increase scale:

   ```text
   --dataset-cases-per-task 5 or 10
   --samples 5 or more
   ```

3. Run each perturbation type separately:

   ```text
   paraphrase
   format change
   information reordering
   surface noise
   context injection
   ```

4. Compare for each metric:

   ```text
   uncorrected estimate
   vs.
   repeated-sampling / sample-noise-corrected estimate
   ```

## 2026-06-29 RQ1 Status Cleanup Update

This update records the latest RQ1 status alignment. No new model generations were run in this step. The work focused on cleaning the RQ1 completion summary so that the experimental structure is easier to review.

Updated file:

```text
rq1_completion_status.md
```

### Main Cleanup Decisions

1. Removed the duplicated row:

```text
multiple perturbation types on SQuAD + MATH
```

Reason:

This was an earlier partial experiment and overlapped with the later four-task multi-perturbation sweep. Keeping it as a separate completed item made the RQ1 status look more complete than the current main evidence actually supports.

2. Merged `uncorrected vs corrected comparison` into the four-task multi-perturbation result.

Reason:

The four-task similarity sweep already contains both:

```text
uncorrected raw drift
noise-corrected drift
```

Therefore, `uncorrected vs corrected comparison` is not a separate experiment. It is one analysis dimension inside the main four-task sweep.

3. Merged ranking-related duplicate rows into the main four-task sweep row.

The following were treated as analysis outputs of the same main experiment:

```text
perturbation ranking across four tasks
raw ranking vs corrected ranking
```

They are now summarized inside:

```text
four-task multi-perturbation similarity sweep
```

4. Reframed the cross-task paraphrase experiment as a preliminary validation.

The two cross-task experiments are now represented as one logical sequence:

| Stage | Role | File |
|---|---|---|
| cross-task paraphrase preliminary validation | Preliminary validation using one shared perturbation across four tasks | `cross_task_paraphrase_noise_correction.md` |
| four-task multi-perturbation similarity sweep | Main RQ1 similarity experiment using four perturbation types across four tasks | `rq1_four_task_similarity_sweep_5x3_result.md` |

### Current Interpretation

The project now treats the cross-task paraphrase run as a preliminary validation, not as a separate main experiment. It showed that a shared perturbation can have different corrected drift across Factual QA, Math reasoning, Code generation, and Open-ended writing.

The current RQ1 main experiment is:

```text
4 tasks × 4 perturbations × 5 cases/task × 3 samples/prompt
```

Main result file:

```text
rq1_four_task_similarity_sweep_5x3_result.md
```

Supporting result files:

```text
results/similarity_report_four_task_similarity_sweep_5x3.md
results/similarity_rankings_four_task_similarity_sweep_5x3.csv
sample_noise_correction_interpretation.md
```

Main conclusion:

Sample-noise correction can change the interpretation of prompt-perturbation sensitivity. In the 5x3 four-task sweep, corrected sensitivity ranking is task-dependent, and correction changes the ranking for some tasks, especially Math reasoning and Open-ended writing.

5x3 corrected ranking:

```text
Factual QA          semantic > word > sentence > character
Math reasoning      word > sentence > semantic > character
Code generation     semantic > word > character > sentence
Open-ended writing  character > sentence > word > semantic
```

### Current RQ1 Status After Cleanup

Completed / available evidence:

- sample-noise correction pipeline is implemented.
- preliminary cross-task paraphrase validation is complete.
- four-task multi-perturbation similarity sweep is complete at pilot-expanded scale.
- raw drift vs noise-corrected drift comparison is included in the main four-task sweep.
- corrected sensitivity ranking is available for all four tasks.
- PDR checks exist for Factual QA and Math reasoning.
- larger MATH PDR validation exists for paraphrase perturbation.

Still incomplete or requiring more evidence:

- HumanEval unit-test correctness is not yet integrated.
- Alpaca open-ended writing still mainly uses similarity; diversity/coherence/fluency are not systematically computed.
- The four-task similarity sweep is still small-scale: 5 cases/task and 3 samples/prompt.
- Larger-scale validation is still needed if the proposal requires benchmark-level evidence.
- Bootstrap ranking stability has not been run.
- Multi-model or multi-temperature validation has not been run.

Practical status:

```text
RQ1 pilot evidence is organized and internally consistent.
RQ1 is not yet benchmark-scale complete.
```

## 2026-06-29 End-of-Day RQ1 Progress Record

This section records the latest project status at the end of today's discussion. The main work was RQ1 status clarification, experiment de-duplication, and deciding which remaining simulations are necessary versus optional.

### Files Updated Today

```text
rq1_completion_status.md
project_continuation.md
```

Key result files referenced during the discussion:

```text
cross_task_paraphrase_noise_correction.md
rq1_four_task_similarity_sweep_5x3_result.md
results/similarity_report_four_task_similarity_sweep_5x3.md
results/similarity_rankings_four_task_similarity_sweep_5x3.csv
sample_noise_correction_interpretation.md
promptrobust_reference_aligned_pdr_result.md
math_paraphrase_pdr_25x3_analysis.md
```

### RQ1 Status Table Cleanup

The RQ1 status table was cleaned to avoid double-counting the same experiment under multiple names.

Removed from the completed section:

```text
multiple perturbation types on SQuAD + MATH
```

Reason:

This was an earlier partial experiment and overlapped with the later four-task multi-perturbation sweep. It should not be listed as a separate main completed RQ1 item.

Merged into the main four-task sweep row:

```text
uncorrected vs corrected comparison
perturbation ranking across four tasks
raw ranking vs corrected ranking
```

Reason:

These are not independent experiments. They are analysis dimensions of the same main experiment:

```text
four-task multi-perturbation similarity sweep
```

The main experiment already includes:

```text
raw drift / uncorrected estimate
sample-noise baseline
noise-corrected drift
corrected sensitivity ranking
raw ranking vs corrected ranking comparison
```

### Cross-Task Experiment Framing

The cross-task paraphrase experiment and the four-task multi-perturbation experiment were reframed as one logical sequence:

| Stage | Name in status | Role | Main file |
|---|---|---|---|
| 1 | cross-task paraphrase preliminary validation | Preliminary validation using one shared perturbation across all four tasks | `cross_task_paraphrase_noise_correction.md` |
| 2 | four-task multi-perturbation similarity sweep | Main RQ1 pilot-expanded experiment using four perturbation types across all four tasks | `rq1_four_task_similarity_sweep_5x3_result.md` |

Interpretation:

The paraphrase run is a preliminary validation, not a separate full RQ1 experiment. It showed that the same perturbation can produce different corrected drift across Factual QA, Math reasoning, Code generation, and Open-ended writing.

The main RQ1 similarity experiment is:

```text
4 tasks × 4 perturbations × 5 cases/task × 3 samples/prompt
```

It produced 480 model outputs:

```text
4 tasks × 5 cases/task × 4 perturbations × 2 prompt versions × 3 samples = 480 generations
```

Important clarification:

The current experiment has 480 generation outputs, but only 20 independent dataset cases:

```text
4 tasks × 5 cases/task = 20 dataset cases
```

Therefore, the current result is pilot-expanded evidence, not benchmark-scale evidence.

### Current Main RQ1 Result

Main result file:

```text
rq1_four_task_similarity_sweep_5x3_result.md
```

Supporting files:

```text
results/similarity_report_four_task_similarity_sweep_5x3.md
results/similarity_rankings_four_task_similarity_sweep_5x3.csv
sample_noise_correction_interpretation.md
```

Current corrected sensitivity ranking:

```text
Factual QA          semantic > word > sentence > character
Math reasoning      word > sentence > semantic > character
Code generation     semantic > word > character > sentence
Open-ended writing  character > sentence > word > semantic
```

Main interpretation:

Sample-noise correction changes the interpretation of perturbation sensitivity. In the current 5x3 four-task sweep, corrected ranking is task-dependent. Correction changes part of the ranking, especially for Math reasoning and Open-ended writing.

### Remaining Work Clarified

The unfinished items were rewritten in `rq1_completion_status.md` with more detailed explanations. They are now separated into three categories.

#### Main RQ1 Evidence Gaps

1. Larger four-task similarity sweep.

Current status:

```text
5 cases/task, 3 samples/prompt
```

Why it matters:

This supports pilot-level conclusions, but stable ranking claims need more cases. A larger sweep can test whether the current corrected ranking remains stable when the number of cases increases.

Suggested scale:

```text
10 cases/task or 25 cases/task
```

2. Ranking stability / bootstrap.

Why it matters:

The current ranking may be influenced by a small number of cases. Bootstrap does not require new model calls; it can resample the existing case-level metrics and estimate how often each perturbation becomes Rank 1 or Rank 2.

Input file:

```text
results/similarity_metrics_four_task_similarity_sweep_5x3.csv
```

#### Reference-Aligned Optional Supplements

1. Code generation correctness.

Current status:

HumanEval currently uses similarity drift only. Unit-test pass rate is not yet integrated.

Clarified interpretation:

This is not mandatory if RQ1 is limited to cross-task similarity / semantic drift. It becomes necessary if the proposal claims to evaluate task-performance impact or code-generation correctness.

2. Open-ended writing quality metrics.

Current status:

Alpaca currently mainly uses embedding similarity.

Clarified interpretation:

This is not mandatory if RQ1 uses similarity as the unified cross-task metric. It becomes important if the proposal claims to evaluate open-ended writing quality or strictly align with open-ended generation evaluation criteria from the references.

Candidate metrics:

```text
response diversity
semantic coherence
fluency
length stability
lexical diversity
```

#### Robustness Extensions

1. Multi-temperature comparison.

Purpose:

Check whether sample-noise correction depends on decoding randomness.

2. Multi-model comparison.

Purpose:

Check whether the finding is model-specific or more general.

Current decision:

These are useful robustness checks, but they should come after the single-model RQ1 main evidence is complete.

### SQuAD + MATH Larger PDR Sweep Plan

The user requested completing the following item:

```text
SQuAD + MATH larger PDR sweep across multiple perturbations
```

Target design:

```text
Tasks: Factual QA, Math reasoning
Datasets: SQuAD V2, MATH
Perturbations: character, word, sentence, semantic
Cases: 10 or 25 cases/task
Samples: 3 samples/prompt
Evaluation: task correctness and PDR
Comparison: uncorrected single-sample PDR vs repeated-sampling PDR
```

The script `promptrobust_reference_pdr_eval.py` already supports this design:

```text
--dataset-cases-per-task
--samples
--perturbations all
--tasks factual_qa,math_reasoning
```

A 10 cases/task run was attempted with:

```powershell
python promptrobust_reference_pdr_eval.py --dataset-cases-per-task 10 --samples 3 --temperature 0.7 --top-p 0.9 --perturbations all --tasks factual_qa,math_reasoning --output-tag squad_math_pdr_10x3_all_perturbations
```

Expected generation count:

```text
2 tasks × 10 cases/task × 4 perturbations × 2 prompt versions × 3 samples = 480 generations
```

Status:

The first attempt did not complete because the tool timed out after about 20 minutes before result files were written. A second attempt was started but was intentionally interrupted by the user when stopping for the day. No final result files were found for:

```text
*squad_math_pdr_10x3_all_perturbations*
```

Therefore, this experiment is planned but not completed. It should be rerun next time.

Suggested next run:

```powershell
python promptrobust_reference_pdr_eval.py --dataset-cases-per-task 10 --samples 3 --temperature 0.7 --top-p 0.9 --sleep 0 --perturbations all --tasks factual_qa,math_reasoning --output-tag squad_math_pdr_10x3_all_perturbations
```

If long runtime remains a problem, use one of these safer options:

```text
Option 1: run 5 cases/task first with all four perturbations.
Option 2: run one task at a time: factual_qa first, then math_reasoning.
Option 3: add checkpoint / incremental CSV writing to promptrobust_reference_pdr_eval.py before rerunning 10x3.
```

### End-of-Day Practical Status

Current status:

```text
RQ1 pilot evidence is organized and internally consistent.
The main four-task similarity sweep is complete at 5x3 scale.
The larger SQuAD + MATH PDR multi-perturbation sweep is planned but not completed.
RQ1 is still not benchmark-scale complete.
```

Recommended next step:

Before running another long PDR job, update `promptrobust_reference_pdr_eval.py` to write generations incrementally after each case. This avoids losing progress if the run is interrupted or times out.

## 2026-06-30 Progress Update

### Evaluation Criteria Decision

The five reference papers were re-checked specifically for whether any evaluation criterion can cover all four task types:

```text
factual QA
math reasoning
code generation
open-ended writing
```

Conclusion:

```text
No single reference evaluation criterion can be adopted unchanged for all four tasks.
```

Current evaluation decision:

```text
Primary cross-task metric:
Noise-Corrected Semantic Drift

Reference basis:
POSIX semantic coherence / response similarity
+
Haase et al. within-prompt sampling-noise correction

Auxiliary task-performance metric:
PDR / correctness drop

Applicable tasks:
factual QA
math reasoning
code generation

Not applicable:
open-ended writing
```

Notes written today:

```text
noise_corrected_semantic_drift_eval.md
proposal_similarity_vs_noise_corrected_drift.md
reference_eval_criteria_for_four_tasks.md
```

### PDR Expanded to Three Objective Tasks

The PDR evaluation was extended from two tasks to three tasks:

```text
factual_qa      -> SQuAD V2 exact short-answer correctness
math_reasoning  -> MATH final-answer correctness
code_generation -> HumanEval unit-test pass/fail
```

The implementation file updated today:

```text
promptrobust_reference_pdr_eval.py
```

Important correction:

```text
HumanEval correctness must be pass@1-style.
The model output is treated as a completion appended to the HumanEval prompt.
Standalone full-code outputs are accepted only as a fallback.
```

This fixed the earlier issue where function-body completions were being incorrectly treated as invalid standalone Python code.

### Three-Task 2x3 PDR Smoke Run

A 2 cases/task run was completed after fixing HumanEval evaluation:

```text
Tasks: factual_qa, math_reasoning, code_generation
Datasets: SQuAD V2, MATH, HumanEval
Perturbations: paraphrase, reordering, formatting, context_injection, surface_noise
Samples: 3 clean + 3 perturbed per case
```

Output files:

```text
results/pdr_report_three_task_pdr_humaneval_fixed_2x3_all_perturbations.md
results/pdr_metrics_three_task_pdr_humaneval_fixed_2x3_all_perturbations.csv
results/generations_three_task_pdr_humaneval_fixed_2x3_all_perturbations.csv
```

Key result:

```text
Uncorrected single-sample PDR: -0.1333
Repeated-sampling PDR:        -0.0426
```

Interpretation:

```text
The 2x3 smoke run showed that the single-sample estimate was more extreme than the repeated-sampling estimate.
Because the sample size was small, this was treated only as a sanity check.
```

### Three-Task 10x3 PDR Validation

The user requested increasing the dataset size to 10 cases/task.

The full 900-generation run timed out when attempted as one command, so the experiment was split into three task-specific runs:

```text
factual_qa      10 cases x 5 perturbations x 2 prompt versions x 3 samples = 300 generations
math_reasoning  10 cases x 5 perturbations x 2 prompt versions x 3 samples = 300 generations
code_generation 10 cases x 5 perturbations x 2 prompt versions x 3 samples = 300 generations
```

The three parts were then merged into one combined report.

Combined output files:

```text
results/pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md
results/pdr_metrics_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv
results/pdr_metrics_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.json
results/generations_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv
```

Task-specific output files:

```text
results/pdr_report_three_task_pdr_humaneval_fixed_10x3_factual_qa.md
results/pdr_report_three_task_pdr_humaneval_fixed_10x3_math_reasoning.md
results/pdr_report_three_task_pdr_humaneval_fixed_10x3_code_generation.md
```

### 10x3 Core Result

Aggregate result:

```text
Average clean single-sample correctness:     0.4867
Average perturbed single-sample correctness: 0.4533
Dataset-level uncorrected single-sample PDR: 0.0685

Average clean repeated correctness:          0.4778
Average perturbed repeated correctness:      0.4733
Dataset-level repeated-sampling PDR:         0.0093
```

Difference:

```text
uncorrected PDR - corrected/repeated PDR
= 0.0685 - 0.0093
= 0.0592
```

Interpretation:

```text
Uncorrected estimate:
perturbations appear to cause about 6.85% relative performance drop.

Repeated-sampling / sample-noise-aware estimate:
the estimated drop is only about 0.93%.

Therefore:
the uncorrected single-sample estimate overstates PDR by 0.0592,
or 5.92 percentage points.
```

By task:

```text
factual_qa:
uncorrected 0.0323 -> repeated 0.0319
almost unchanged

math_reasoning:
uncorrected 0.0000 -> repeated -0.1852
repeated sampling indicates perturbed prompts performed better on average

code_generation:
uncorrected 0.1818 -> repeated 0.1343
impact remains but is smaller after repeated sampling
```

### Perturbation Strength Interpretation

The current evidence suggests:

```text
After sample-noise-aware correction, the overall correctness drop is small.
```

Recommended wording:

```text
The current natural perturbations produce limited correctness degradation after accounting for sampling noise.
```

Avoid overclaiming:

```text
Do not simply say "the perturbations are too weak."
```

Reason:

```text
The perturbations are intentionally non-adversarial / natural everyday perturbations.
Semantic drift and correctness drop are different outcomes.
Task-specific effects still exist, especially for code generation.
```

This interpretation was added to:

```text
results/pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md
```

### Current Status After Today

Completed:

```text
1. Evaluation criteria from five references reviewed and documented.
2. Noise-Corrected Semantic Drift confirmed as consistent with the proposal's similarity + noise-baseline idea.
3. PDR selected as auxiliary metric for the first three objective tasks.
4. Code generation PDR corrected to HumanEval pass@1-style evaluation.
5. Three-task PDR comparison completed at 10 cases/task and 3 samples/prompt.
6. Core interpretation written into the combined Markdown report.
```

Next recommended steps:

```text
1. Decide whether to run the final proposal-scale setting:
   factual QA: 15-20 items
   math reasoning: 15-20 items
   code generation: 15 items

2. Consider adding incremental checkpointing to promptrobust_reference_pdr_eval.py
   before another long run.

3. Continue using semantic drift as the main four-task metric;
   use PDR only as auxiliary correctness validation for factual QA, math, and code.
```

## 2026-07-01 Progress Update: RQ2 Semantic Drift vs Correctness Change

### RQ2 Definition

RQ2 is currently framed as:

```text
For tasks with objective correctness, does semantic drift predict correctness changes?
```

Practical interpretation:

```text
When prompt perturbation causes a larger semantic / embedding-space output drift,
does the task correctness also tend to change more?
```

This differs from RQ1:

```text
RQ1: Which perturbation types produce noise-corrected semantic drift, and are rankings task-dependent?
RQ2: Does that semantic drift correspond to measurable correctness change?
```

### RQ2 Scope

RQ2 uses only tasks with objective correctness criteria:

```text
factual_qa      -> SQuAD V2 short-answer correctness
math_reasoning  -> MATH final-answer correctness
code_generation -> HumanEval pass@1-style unit-test correctness
```

Open-ended writing is excluded from the first RQ2 implementation because it does not have a single objective correctness label.

### Data Reused for RQ2

The RQ2 analysis reuses the completed three-task 10x3 PDR run:

```text
results/generations_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv
results/pdr_metrics_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv
```

Scale:

```text
3 tasks x 10 cases/task x 5 perturbations = 150 case-level comparisons
150 comparisons x 2 prompt versions x 3 samples = 900 generated outputs
```

This is methodologically important because semantic drift and correctness change are computed from the same generated outputs.

### RQ2 Implementation Files

Files added or updated:

```text
rq2_implementation_plan.md
rq2_semantic_correctness_analysis.py
rq2_factual_llm_judge_correctness.py
```

Main output files:

```text
results/rq2_semantic_correctness_report.md
results/rq2_semantic_correctness_interpretation.md
results/rq2_semantic_correctness_metrics.csv
results/rq2_semantic_correctness_grouped.csv
results/rq2_semantic_correctness_correlations.csv
results/rq2_semantic_correctness_case_inspection.csv
results/rq2_semantic_correctness_summary.json
```

Additional explanatory file:

```text
results/rq2_correlation_metrics_explanation.md
```

Proposal visual/statistical outputs:

```text
results/proposal_visual_stats/rq2_*.csv
results/proposal_visual_stats/rq2_*.png
```

These include ANOVA, Tukey, and tornado-style summaries for RQ2 correctness drift and harmful-drop patterns.

### RQ2 Method

For each case-level comparison, the script embeds:

```text
3 original outputs
3 perturbed outputs
```

It computes:

```text
original sample noise
perturbed sample noise
raw perturbation drift
noise-corrected drift
uncorrected single-pair drift
```

The primary correctness-change target is:

```text
abs_repeated_pass_rate_change
```

Reason:

```text
PDR can be unstable when clean correctness is near zero.
Repeated pass-rate change is a more direct case-level correctness-change variable.
```

Main relationship tested:

```text
X = noise_corrected_drift
Y = abs_repeated_pass_rate_change
```

### Main RQ2 Result with Exact-Match Factual QA

Main report:

```text
results/rq2_semantic_correctness_report.md
```

Overall result:

```text
Case-level comparisons: 150
Pearson:  0.328
Spearman: 0.346
Spearman 95% CI: [0.188, 0.503]
Permutation p: 0.001
```

Interpretation:

```text
Noise-corrected semantic drift is positively associated with correctness drift.
The relationship is statistically reliable but moderate in magnitude.
```

Recommended wording:

```text
Across objective tasks, noise-corrected semantic drift is positively associated
with correctness drift. The relationship is statistically reliable but moderate,
indicating that semantic drift can serve as an indicator of correctness change
but not as a strong deterministic predictor.
```

### Sample-Noise Correction Comparison for RQ2

The RQ2 analysis compared three drift measures:

```text
noise_corrected_drift
raw_perturbation_drift
uncorrected_single_drift
```

Primary target:

```text
abs_repeated_pass_rate_change
```

Comparison:

```text
noise_corrected_drift:
Pearson  = 0.328
Spearman = 0.346

raw_perturbation_drift:
Pearson  = 0.298
Spearman = 0.375

uncorrected_single_drift:
Pearson  = 0.267
Spearman = 0.332
```

Correction gain:

```text
corrected vs raw repeated cross-drift:
Pearson delta  = +0.030
Spearman delta = -0.029

corrected vs single-pair drift:
Pearson delta  = +0.061
Spearman delta = +0.015
```

Interpretation:

```text
Sample-noise correction improves the methodological cleanliness of the drift measure
and shows some Pearson-level gain, especially over the single-pair baseline.
However, this first RQ2 run does not show a stable rank-correlation improvement
over raw repeated cross-drift.
```

Therefore, avoid overclaiming:

```text
Do not claim that sample-noise correction always improves correctness prediction.
```

Stronger and safer claim:

```text
Sample-noise correction gives a cleaner perturbation-specific semantic drift measure.
In the current RQ2 run, it remains positively associated with correctness drift,
but the predictive advantage over uncorrected repeated drift is mixed.
```

### Harmful Correctness Drop Analysis

RQ2 also separates:

```text
correctness changed
```

from:

```text
correctness got worse
```

Harmful-drop relationship:

```text
noise_corrected_drift -> harmful_correctness_drop
```

Result:

```text
noise_corrected_drift:
Pearson  = 0.247
Spearman = 0.306
Spearman 95% CI: [0.145, 0.463]
Permutation p: 0.001

raw_perturbation_drift:
Pearson  = 0.200
Spearman = 0.213
Spearman 95% CI: [0.074, 0.340]
Permutation p: 0.009
```

Interpretation:

```text
Noise-corrected semantic drift is also associated with harmful correctness drops.
For this harmful-drop target, corrected drift is stronger than raw drift.
```

This is one of the clearest RQ2 links between sample-noise correction and correctness impact.

### RQ2 Task-Level Results

Task-level primary results:

```text
code_generation:
Pearson  = 0.747
Spearman = 0.515
Spearman 95% CI: [0.180, 0.732]

factual_qa:
Pearson  = 0.006
Spearman = 0.224
Spearman 95% CI: [-0.162, 0.535]

math_reasoning:
Pearson  = -0.060
Spearman = 0.232
Spearman 95% CI: [-0.044, 0.507]
```

Interpretation:

```text
RQ2 is task-dependent.
The strongest evidence is for code generation, where semantic drift is clearly
associated with HumanEval pass/fail changes.
Factual QA and math reasoning show weaker and less stable task-level relationships
at the current sample size.
```

### RQ2 Perturbation-Level Results

Perturbation-level Spearman results:

```text
surface_noise      0.608
context_injection  0.467
reordering         0.271
formatting         0.221
paraphrase         0.112
```

Interpretation:

```text
Surface noise and context injection show the clearest relationship between
semantic drift and correctness drift.
Paraphrase produces the weakest correctness-drift association, suggesting that
paraphrase may often change expression without changing task correctness.
```

### Case Inspection Findings

The RQ2 case inspection file:

```text
results/rq2_semantic_correctness_case_inspection.csv
```

It identifies several important case types:

```text
high corrected drift + high correctness drift
high corrected drift + no correctness drift
low corrected drift + high correctness drift
harmful correctness drops
correctness improvements
```

Important interpretation:

```text
Semantic drift is informative but imperfect.
Some outputs change substantially in embedding space while correctness remains unchanged.
Other cases show correctness changes even when corrected semantic drift is small.
This explains why the overall RQ2 relationship is reliable but moderate rather than strong.
```

### Factual QA LLM Equivalence Judge Sensitivity Analysis

Because exact-match factual QA correctness can be too strict, a sensitivity analysis replaced factual QA exact match with an LLM equivalence judge.

Script:

```text
rq2_factual_llm_judge_correctness.py
```

Main report:

```text
results/rq2_llm_fact_correctness_sensitivity.md
```

Full RQ2 report using LLM factual correctness:

```text
results/rq2_semantic_correctness_llm_fact_report.md
```

Other outputs:

```text
results/rq2_semantic_correctness_llm_fact_factual_judgments.csv
results/rq2_semantic_correctness_llm_fact_factual_pdr_metrics.csv
results/rq2_semantic_correctness_llm_fact_combined_pdr_metrics.csv
results/rq2_semantic_correctness_llm_fact_metrics.csv
results/rq2_semantic_correctness_llm_fact_grouped.csv
results/rq2_semantic_correctness_llm_fact_correlations.csv
results/rq2_semantic_correctness_llm_fact_case_inspection.csv
results/rq2_semantic_correctness_llm_fact_summary.json
```

Judge setup:

```text
Judge model: gpt-4o-mini
Factual outputs judged: 300
Factual case-level comparisons: 50
Original generations reused: yes
New answer generation: no
```

The judge was instructed to mark a factual answer correct if the candidate answer was semantically equivalent to at least one reference answer, including longer answers that contain the correct answer without contradiction.

### Difference Between Exact Match and LLM Factual Correctness

Comparison:

```text
Factual outputs judged: 300
Exact-match label differs from LLM label: 111
Exact-match 0 -> LLM 1: 111
Exact-match 1 -> LLM 0: 0
```

Interpretation:

```text
Strict exact match was conservative for factual QA.
The LLM equivalence judge accepted many outputs that were factually equivalent
or contained the correct answer in a longer response.
```

### RQ2 Result with LLM Factual Correctness

Overall relationship:

```text
noise_corrected_drift -> abs_repeated_pass_rate_change
```

Result:

```text
Pearson:  0.536
Spearman: 0.349
Spearman 95% CI: [0.187, 0.501]
Permutation p: 0.001
```

Comparison with exact-match factual correctness:

```text
Exact-match factual correctness:
Pearson  = 0.328
Spearman = 0.346

LLM-equivalence factual correctness:
Pearson  = 0.536
Spearman = 0.349
```

Interpretation:

```text
Replacing factual exact match with LLM equivalence correctness changes many
individual factual labels but does not materially change the overall RQ2 conclusion.
The overall Spearman relationship remains almost unchanged.
Pearson increases, suggesting a cleaner pooled linear relationship, but Spearman
should remain the preferred interpretation because correctness drift is discrete.
```

Recommended wording:

```text
Replacing strict exact-match factual QA correctness with an LLM equivalence judge
changes many individual factual labels but does not materially change the overall
RQ2 conclusion. Noise-corrected semantic drift remains a statistically reliable
but moderate indicator of correctness drift.
```

### Factual QA After LLM Equivalence Judging

With LLM equivalence correctness:

```text
Factual case-level comparisons: 50
Factual cases with repeated correctness change: 2
Factual cases with harmful correctness drop: 2
```

By perturbation:

```text
context_injection:
mean corrected drift = 0.003
mean abs repeated pass-rate change = 0.000

formatting:
mean corrected drift = 0.000
mean abs repeated pass-rate change = 0.000

paraphrase:
mean corrected drift = 0.042
mean abs repeated pass-rate change = 0.100

reordering:
mean corrected drift = 0.000
mean abs repeated pass-rate change = 0.000

surface_noise:
mean corrected drift = 0.001
mean abs repeated pass-rate change = 0.033
```

Interpretation:

```text
Under semantic equivalence judging, most factual QA perturbations do not change
factual correctness. Many exact-match factual errors were formatting or verbosity
artifacts rather than genuinely wrong answers.
```

Factual QA task-level caution:

```text
The factual QA Spearman relationship remains weak and uncertain.
Because only 2 of 50 factual comparisons show repeated correctness change after
LLM equivalence judging, the high factual Pearson should not be overinterpreted.
```

### Current RQ2 Status

Completed:

```text
1. RQ2 implementation plan written.
2. Semantic drift and correctness drift computed on the same 10x3 PDR generations.
3. Main RQ2 correlation analysis completed for three objective tasks.
4. Sample-noise corrected drift compared against raw repeated drift and single-pair drift.
5. Harmful correctness drop analysis completed.
6. Task-level and perturbation-level RQ2 summaries generated.
7. Case inspection table generated.
8. Factual QA exact-match sensitivity checked using LLM equivalence judging.
9. Proposal visual/statistical RQ2 outputs generated.
```

Current main conclusion:

```text
RQ2 has first-round evidence that semantic drift is a statistically reliable but
moderate indicator of correctness drift across objective tasks.
The relationship is strongest for code generation, weaker for factual QA and math.
Sample-noise correction is methodologically cleaner and is useful for harmful-drop
analysis, but its overall predictive advantage over raw repeated cross-drift is mixed.
```

Important caveats:

```text
1. Current RQ2 evidence is based on 150 case-level comparisons.
2. Correlations are descriptive, not causal.
3. Correctness labels are task-specific and should not be treated as perfectly comparable.
4. Spearman should be emphasized over Pearson because repeated correctness values are discrete.
5. Factual QA exact match is too strict; LLM equivalence judging is a useful sensitivity check.
6. Code-generation correctness depends on the HumanEval pass@1-style evaluation implementation.
```

Recommended next steps:

```text
1. Add this RQ2 result to the proposal / methodology narrative after RQ1.
2. Use Spearman as the primary RQ2 correlation statistic and Pearson as auxiliary.
3. Report both correctness change and harmful correctness drop.
4. Emphasize task dependence, especially the stronger code-generation result.
5. If more evidence is needed, scale the same RQ2 analysis to the final proposal-scale PDR run.
6. Consider adding logistic or threshold-based analysis for harmful correctness drop if the paper needs a predictive framing.
```

## 2026-07-02 Progress Update: RQ2 Surface-Noise Dose-Response Experiment

The user proposed a stronger RQ2 design:

```text
For one perturbation family, gradually increase perturbation strength and observe
whether output similarity decreases and correctness change increases.
```

This has now been implemented as a new script:

```text
rq2_perturbation_dose_response.py
```

### Algorithm

The first implemented perturbation family is:

```text
surface_noise
```

Strength is controlled by the number of corrupted words in the task instruction:

```text
0, 1, 2, 4, 8
```

The perturbation is cumulative:

```text
level 0: no typo
level 1: corrupt the first selected instruction word
level 2: keep level-1 corruption and corrupt one more selected word
level 3: keep prior corruptions and corrupt up to 4 selected words
level 4: keep prior corruptions and corrupt up to 8 selected words
```

Only the instruction is perturbed. The passage, math problem, and HumanEval function prompt are kept unchanged.

The script computes, for each base case and perturbation strength:

```text
mean_cross_similarity
mean_paired_similarity
raw_perturbation_drift
noise_corrected_drift
clean_mean_correctness
perturbed_mean_correctness
abs_repeated_pass_rate_change
repeated_pass_rate_drop
harmful_correctness_drop
correctness_changed
```

It also writes:

```text
by-level summaries
task-by-level summaries
overall and task-level correlations
within-case monotonicity checks
Markdown report
```

### Code Changes

Updated:

```text
reference_perturbations.py
```

Change:

```text
add_surface_noise(text, edits=4)
```

The default `edits=4` preserves the old behavior. Non-default edit counts support the new dose-response experiment.

Added:

```text
rq2_perturbation_dose_response.py
```

The script supports:

```text
--dataset-cases-per-task
--samples
--levels
--tasks
--output-tag
--resume
```

### Smoke Test

Command:

```powershell
python rq2_perturbation_dose_response.py --dataset-cases-per-task 1 --samples 1 --levels 0,1 --tasks factual_qa --sleep 0 --output-tag rq2_surface_noise_dose_response_smoke --resume
```

Output files:

```text
results/rq2_surface_noise_dose_response_smoke_generations.csv
results/rq2_surface_noise_dose_response_smoke_metrics.csv
results/rq2_surface_noise_dose_response_smoke_by_level.csv
results/rq2_surface_noise_dose_response_smoke_by_task_level.csv
results/rq2_surface_noise_dose_response_smoke_correlations.csv
results/rq2_surface_noise_dose_response_smoke_within_case_monotonicity.csv
results/rq2_surface_noise_dose_response_smoke_summary.json
results/rq2_surface_noise_dose_response_smoke_report.md
```

The smoke test completed successfully.

### Three-Task 2x3 Cumulative Dose-Response Pilot

Command:

```powershell
python rq2_perturbation_dose_response.py --dataset-cases-per-task 2 --samples 3 --levels 0,1,2,4,8 --tasks factual_qa,math_reasoning,code_generation --sleep 0 --output-tag rq2_surface_noise_dose_response_2x3_cumulative --resume
```

Scale:

```text
3 tasks x 2 cases/task x 5 strength levels = 30 case-level rows
3 samples per prompt version
90 generated outputs total
```

Output files:

```text
results/rq2_surface_noise_dose_response_2x3_cumulative_generations.csv
results/rq2_surface_noise_dose_response_2x3_cumulative_metrics.csv
results/rq2_surface_noise_dose_response_2x3_cumulative_by_level.csv
results/rq2_surface_noise_dose_response_2x3_cumulative_by_task_level.csv
results/rq2_surface_noise_dose_response_2x3_cumulative_correlations.csv
results/rq2_surface_noise_dose_response_2x3_cumulative_within_case_monotonicity.csv
results/rq2_surface_noise_dose_response_2x3_cumulative_summary.json
results/rq2_surface_noise_dose_response_2x3_cumulative_report.md
```

### Main Pilot Result

Mean by strength:

```text
edits 0:
mean similarity = 1.0000
mean corrected drift = 0.0000
mean abs correctness change = 0.0000

edits 1:
mean similarity = 0.9792
mean corrected drift = 0.0002
mean abs correctness change = 0.1111

edits 2:
mean similarity = 0.9787
mean corrected drift = 0.0001
mean abs correctness change = 0.0556

edits 4:
mean similarity = 0.9728
mean corrected drift = 0.0029
mean abs correctness change = 0.1667

edits 8:
mean similarity = 0.9707
mean corrected drift = 0.0036
mean abs correctness change = 0.1111
```

Correlation results:

```text
All levels:
strength_edits -> mean_cross_similarity:
Spearman = -0.5804

strength_edits -> abs_repeated_pass_rate_change:
Spearman = 0.2465

mean_cross_similarity -> abs_repeated_pass_rate_change:
Spearman = -0.6266

noise_corrected_drift -> abs_repeated_pass_rate_change:
Spearman = 0.4372
```

Nonzero perturbation levels only:

```text
mean_cross_similarity -> abs_repeated_pass_rate_change:
Spearman = -0.5929

noise_corrected_drift -> abs_repeated_pass_rate_change:
Spearman = 0.3772
```

Within-case monotonicity:

```text
Cases where strength-to-similarity Spearman is negative:
5 / 6

Cases where strength-to-absolute-correctness-change Spearman is positive:
2 / 6
```

### Interpretation

The cumulative surface-noise pilot supports the central RQ2 dose-response intuition at the pooled level:

```text
As perturbation strength increases, output similarity tends to decrease.
Lower output similarity is associated with larger correctness change.
The equivalent drift framing is also positive: larger noise-corrected drift is
associated with larger correctness change.
```

However, correctness change is not strictly monotonic by strength at this small pilot scale.

Important caution:

```text
This is a 2 cases/task pilot, not final statistical evidence.
The similarity dose-response pattern is clearer than the correctness dose-response pattern.
Correctness changes remain task-dependent and case-dependent.
```

Recommended wording:

```text
In a surface-noise dose-response pilot, increasing the number of corrupted
instruction words generally reduced output similarity. Across nonzero perturbation
levels, lower output similarity was associated with larger repeated-sampling
correctness change (Spearman = -0.593), and larger noise-corrected drift was
associated with larger correctness change (Spearman = 0.377). These results support
the RQ2 interpretation that semantic drift can indicate correctness instability,
while also showing that correctness degradation is not strictly monotonic at the
small pilot scale.
```

## 2026-07-02 Update: Larger RQ2 Surface-Noise Dose-Response Run

The user asked to increase the data size and add completion percentages to the run log.

Implemented:

```text
rq2_perturbation_dose_response.py now prints:
Progress completed/total (%) for generation requests
Metric progress completed/total (%) for case-level metric rows
```

The updated script was also copied into:

```text
rq2_dose_response_repro/
```

Command:

```powershell
python rq2_perturbation_dose_response.py --dataset-cases-per-task 5 --samples 3 --levels 0,1,2,4,8 --tasks factual_qa,math_reasoning,code_generation --sleep 0 --output-tag rq2_surface_noise_dose_response_5x3_cumulative --resume
```

Scale:

```text
3 tasks x 5 cases/task x 5 strength levels = 75 case-level rows
225 generation requests
```

The run completed:

```text
Progress 225/225 (100.0%) complete
Metric progress 75/75 (100.0%) complete
```

Output files:

```text
results/rq2_surface_noise_dose_response_5x3_cumulative_generations.csv
results/rq2_surface_noise_dose_response_5x3_cumulative_metrics.csv
results/rq2_surface_noise_dose_response_5x3_cumulative_by_level.csv
results/rq2_surface_noise_dose_response_5x3_cumulative_by_task_level.csv
results/rq2_surface_noise_dose_response_5x3_cumulative_correlations.csv
results/rq2_surface_noise_dose_response_5x3_cumulative_within_case_monotonicity.csv
results/rq2_surface_noise_dose_response_5x3_cumulative_summary.json
results/rq2_surface_noise_dose_response_5x3_cumulative_report.md
```

### Main 5x3 Result

Mean by perturbation strength:

```text
edits 0:
mean similarity = 1.0000
mean corrected drift = 0.0000
mean abs correctness change = 0.0000

edits 1:
mean similarity = 0.9700
mean corrected drift = 0.0019
mean abs correctness change = 0.1111

edits 2:
mean similarity = 0.9671
mean corrected drift = 0.0026
mean abs correctness change = 0.0889

edits 4:
mean similarity = 0.9603
mean corrected drift = 0.0051
mean abs correctness change = 0.1556

edits 8:
mean similarity = 0.9560
mean corrected drift = 0.0095
mean abs correctness change = 0.2000
```

Overall correlations:

```text
All levels:
strength_edits -> mean_cross_similarity:
Spearman = -0.5225

strength_edits -> abs_repeated_pass_rate_change:
Spearman = 0.3062

mean_cross_similarity -> abs_repeated_pass_rate_change:
Spearman = -0.3926

noise_corrected_drift -> abs_repeated_pass_rate_change:
Spearman = 0.0268
```

Nonzero perturbation levels only:

```text
mean_cross_similarity -> abs_repeated_pass_rate_change:
Spearman = -0.2829

noise_corrected_drift -> abs_repeated_pass_rate_change:
Spearman = -0.0363
```

Within-case monotonicity:

```text
Cases where strength-to-similarity Spearman is negative:
14 / 15

Cases where strength-to-absolute-correctness-change Spearman is positive:
6 / 15
```

### Interpretation

The larger 5x3 run gives stronger evidence that the surface-noise severity algorithm is working:

```text
As the number of corrupted instruction words increases, output similarity generally decreases.
```

The correctness-change pattern is present but weaker and less monotonic:

```text
All-level similarity-to-correctness-change Spearman = -0.3926
Nonzero-level similarity-to-correctness-change Spearman = -0.2829
```

Important update compared with the smaller 2x3 run:

```text
The 5x3 run supports the output-similarity version of the RQ2 claim more clearly
than the noise-corrected-drift version. Noise-corrected drift increases by level
on average, but its case-level rank association with correctness change is weak
in this larger pilot.
```

Recommended wording:

```text
In the 5x3 surface-noise dose-response experiment, increasing the number of
corrupted instruction words produced a clear decrease in output similarity
(strength-to-similarity Spearman = -0.523). Correctness change also tended to
increase with perturbation strength, but more weakly (Spearman = 0.306). Across
all levels, lower output similarity was associated with larger repeated-sampling
correctness change (Spearman = -0.393), while the association was weaker when
restricted to nonzero perturbation levels (Spearman = -0.283). These results
support the RQ2 claim that output similarity is informative about correctness
instability, but they also show that correctness changes are not strictly
monotonic and remain task- and case-dependent.
```

## 2026-07-02 Update: Long-Answer Factual QA Dose-Response Redesign

After inspecting the SQuAD factual QA dose-response results, the user correctly noted that short-answer factual QA is not well suited to the project's RQ2 similarity requirement.

Problem with SQuAD-style short factual QA:

```text
Outputs are often one phrase or one entity, such as "France", "Rollo", or "10th century".
Many generations are exactly identical across perturbation levels.
Embedding similarity is therefore dominated by short formatting/verbosity differences.
This can make stronger perturbation levels look more similar when they produce a more consistent short answer format.
```

A new task was added:

```text
long_factual_qa
```

Implementation:

```text
rq2_perturbation_dose_response.py
```

The task uses five built-in long-answer factual QA cases:

```text
Normans
Photosynthesis
Magna Carta
Apollo 11
Penicillin
```

Prompt design:

```text
Read the passage and answer the question in two to three complete sentences.
Include all key facts needed to answer the question accurately.
```

Correctness design:

```text
Each case defines required fact groups.
An output is correct if it includes at least one acceptable alias from every required fact group.
```

This avoids strict exact match and makes correctness more appropriate for longer factual answers.

Command:

```powershell
python rq2_perturbation_dose_response.py --dataset-cases-per-task 5 --samples 3 --levels 0,1,2,4,8 --tasks long_factual_qa --sleep 0 --output-tag rq2_surface_noise_dose_response_longfact_5x3_cumulative --resume
```

Scale:

```text
5 long factual QA cases x 5 strength levels x 3 samples = 75 generation requests
25 case-level metric rows
```

Completion:

```text
Progress 75/75 (100.0%) complete
Metric progress 25/25 (100.0%) complete
```

Output files:

```text
results/rq2_surface_noise_dose_response_longfact_5x3_cumulative_generations.csv
results/rq2_surface_noise_dose_response_longfact_5x3_cumulative_metrics.csv
results/rq2_surface_noise_dose_response_longfact_5x3_cumulative_by_level.csv
results/rq2_surface_noise_dose_response_longfact_5x3_cumulative_by_task_level.csv
results/rq2_surface_noise_dose_response_longfact_5x3_cumulative_correlations.csv
results/rq2_surface_noise_dose_response_longfact_5x3_cumulative_within_case_monotonicity.csv
results/rq2_surface_noise_dose_response_longfact_5x3_cumulative_summary.json
results/rq2_surface_noise_dose_response_longfact_5x3_cumulative_report.md
```

### Long-Answer Factual QA Result

Mean by strength:

```text
edits 0:
mean similarity = 1.0000
mean corrected drift = 0.0000
mean abs correctness change = 0.0000

edits 1:
mean similarity = 0.9739
mean corrected drift = 0.0000
mean abs correctness change = 0.1333

edits 2:
mean similarity = 0.9629
mean corrected drift = 0.0002
mean abs correctness change = 0.0667

edits 4:
mean similarity = 0.9763
mean corrected drift = 0.0000
mean abs correctness change = 0.1333

edits 8:
mean similarity = 0.9563
mean corrected drift = 0.0031
mean abs correctness change = 0.3333
```

Correlation results:

```text
All levels:
strength_edits -> mean_cross_similarity:
Spearman = -0.6142

strength_edits -> abs_repeated_pass_rate_change:
Spearman = 0.4593

mean_cross_similarity -> abs_repeated_pass_rate_change:
Spearman = -0.2342

noise_corrected_drift -> abs_repeated_pass_rate_change:
Spearman = 0.7295
```

Nonzero perturbation levels only:

```text
strength_edits -> mean_cross_similarity:
Spearman = -0.2404

strength_edits -> abs_repeated_pass_rate_change:
Spearman = 0.3004

mean_cross_similarity -> abs_repeated_pass_rate_change:
Spearman = 0.0017

noise_corrected_drift -> abs_repeated_pass_rate_change:
Spearman = 0.7239
```

Within-case monotonicity:

```text
Cases where strength-to-similarity Spearman is negative:
5 / 5

Cases where strength-to-absolute-correctness-change Spearman is positive:
4 / 5
```

### Interpretation

The redesigned long-answer factual QA task is better aligned with RQ2 than short-answer SQuAD.

Main finding:

```text
For long factual QA, increasing perturbation strength reduces output similarity at the within-case level in all five cases.
Correctness change increases with perturbation strength in four of five cases.
Noise-corrected drift is strongly associated with correctness change.
```

Important nuance:

```text
The by-level mean similarity is not perfectly monotonic because level 4 has a small aggregate rebound.
However, level 8 has the lowest mean similarity and largest correctness change.
The within-case monotonicity check is stronger than the simple level mean here.
```

Recommended wording:

```text
Because short-answer factual QA produced nearly identical outputs across perturbation levels,
we introduced a long-answer factual QA condition with two- to three-sentence answers and
required-fact correctness scoring. In this redesigned factual QA setting, perturbation strength
was negatively associated with output similarity in all five cases, and positively associated
with correctness change in four of five cases. At the aggregate level, strength was negatively
correlated with output similarity (Spearman = -0.614) and positively correlated with correctness
change (Spearman = 0.459). Noise-corrected drift showed a strong association with correctness
change (Spearman = 0.730 across all levels), supporting the RQ2 claim that larger perturbation-
specific semantic drift corresponds to greater correctness instability.
```

## 2026-07-03 RQ1 50x3 Sample-Noise Run Paused State

Status timestamp:

```text
2026-07-03 09:09:19 +08:00
```

Current experiment:

```text
Script: four_task_similarity_sweep.py
Model: gpt-4o-mini
Embedding model: text-embedding-3-small
Dataset cases per task: 50
Samples per prompt version: 3
Tasks: factual_qa, math_reasoning, code_generation, open_ended_writing
Perturbations: paraphrase, reordering, formatting, context_injection, surface_noise
Batch count: 10
```

The run was intentionally paused after batch 3/10 because network access needed to be disconnected.
Do not restart from batch 1 unless explicitly rerunning the experiment from scratch.

### Completed Batches

Completed:

```text
batch 1/10: four_task_similarity_sweep_50x3_batch1of10
batch 2/10: four_task_similarity_sweep_50x3_batch2of10
batch 3/10: four_task_similarity_sweep_50x3_batch3of10
```

Batch completeness check:

```text
batch 1: generations=600, metrics=100, grouped=4, rankings=4
batch 2: generations=600, metrics=100, grouped=4, rankings=4
batch 3: generations=600, metrics=100, grouped=4, rankings=4
```

Current cumulative progress:

```text
metric rows: 300 / 1000
generation rows: 1800 / 6000
completed batches: 1, 2, 3
next batch to run: 4
```

The completed batches currently cover these perturbation slices:

```text
batch 1: paraphrase
batch 2: reordering
batch 3: formatting
```

The remaining perturbations still need to be completed through later batch slices:

```text
context_injection
surface_noise
plus the complementary even/odd global slices implied by batch indices 4-10
```

### Output Files Already Written

```text
results/generations_four_task_similarity_sweep_50x3_batch1of10.csv
results/similarity_metrics_four_task_similarity_sweep_50x3_batch1of10.csv
results/similarity_grouped_four_task_similarity_sweep_50x3_batch1of10.csv
results/similarity_rankings_four_task_similarity_sweep_50x3_batch1of10.csv
results/similarity_report_four_task_similarity_sweep_50x3_batch1of10.md

results/generations_four_task_similarity_sweep_50x3_batch2of10.csv
results/similarity_metrics_four_task_similarity_sweep_50x3_batch2of10.csv
results/similarity_grouped_four_task_similarity_sweep_50x3_batch2of10.csv
results/similarity_rankings_four_task_similarity_sweep_50x3_batch2of10.csv
results/similarity_report_four_task_similarity_sweep_50x3_batch2of10.md

results/generations_four_task_similarity_sweep_50x3_batch3of10.csv
results/similarity_metrics_four_task_similarity_sweep_50x3_batch3of10.csv
results/similarity_grouped_four_task_similarity_sweep_50x3_batch3of10.csv
results/similarity_rankings_four_task_similarity_sweep_50x3_batch3of10.csv
results/similarity_report_four_task_similarity_sweep_50x3_batch3of10.md
```

### Current Interim Results

These results use only the first 300 metric rows, so they are interim results, not the final 50x3 conclusion.

Overall statistics:

```text
n = 300

noise_baseline:
mean = 0.047706
std = 0.058397
variance = 0.003410

raw_perturbation_drift:
mean = 0.072255
std = 0.100395
variance = 0.010079

noise_corrected_drift:
mean = 0.028305
std = 0.087777
variance = 0.007705

uncorrected_single_drift:
mean = 0.073690
std = 0.122281
variance = 0.014953
```

Sample-noise baseline by task:

```text
factual_qa:
n = 75
mean = 0.036157
std = 0.086040
variance = 0.007403

math_reasoning:
n = 75
mean = 0.051542
std = 0.029902
variance = 0.000894

code_generation:
n = 75
mean = 0.040254
std = 0.055961
variance = 0.003132

open_ended_writing:
n = 75
mean = 0.062872
std = 0.043716
variance = 0.001911
```

Sample-noise baseline by completed perturbation:

```text
paraphrase:
n = 100
mean = 0.046380
std = 0.064468
variance = 0.004156

reordering:
n = 100
mean = 0.051773
std = 0.058828
variance = 0.003461

formatting:
n = 100
mean = 0.044966
std = 0.051543
variance = 0.002657
```

Interim interpretation:

```text
The first 30% of the 50x3 run still supports the RQ1 motivation:
raw perturbation drift is much larger than the noise-corrected estimate.
Current raw drift mean is 0.072255, while corrected drift mean is 0.028305.
Open-ended writing currently has the highest task-level sample-noise mean,
and math reasoning has a relatively stable sample-noise baseline with low variance.
```

### Resume Command

Resume from batch 4/10:

```powershell
python four_task_similarity_sweep.py --model gpt-4o-mini --dataset-cases-per-task 50 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag four_task_similarity_sweep_50x3_batch4of10 --sleep 0 --batch-count 10 --batch-index 4 --resume
```

After batch 4 completes, continue with the same pattern by changing both `batch4of10` and `--batch-index 4`
to the next batch number.

After all 10 batches complete, merge them with:

```powershell
python merge_similarity_batches.py --batch-count 10 --batch-tag-prefix four_task_similarity_sweep_50x3 --output-tag four_task_similarity_sweep_50x3
```
