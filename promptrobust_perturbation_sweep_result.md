# PromptRobust-Aligned Perturbation Sweep Result

本次实验按用户要求做横向比较：

```text
相同数据集
相同评价准则
不同扰动方法
比较 uncorrection 和 sample-noise / repeated-sampling estimate 的差异
```

## 固定设置

| 项目 | 设置 |
|---|---|
| Reference paper | PromptRobust / PromptBench |
| Datasets | SQuAD V2; MATH |
| Tasks | Factual QA; Math reasoning |
| Evaluation criterion | Performance Drop Rate (PDR) |
| Performance definition | SQuAD V2: answer correctness; MATH: final-answer correctness |
| Model | `gpt-4o-mini` |
| Samples per clean / perturbed prompt | 3 |
| Temperature | 0.7 |
| Top-p | 0.9 |
| Cases per task | 2 |

## Perturbation Methods

| Perturbation | Reference source | Implementation in this run |
|---|---|---|
| Character-level | PromptRobust: TextBugger / DeepWordBug family | Typos inserted into instruction only |
| Word-level | PromptRobust: TextFooler / BertAttack family | Instruction-level wording replacement / rewrite |
| Sentence-level | PromptRobust: StressTest / CheckList family | Irrelevant sentence appended to instruction |
| Semantic-level | PromptRobust semantic-level prompts | Semantic paraphrase of instruction |

Note:

```text
This is PromptRobust-aligned rather than a full reproduction of PromptRobust's adversarial search pipeline.
The dataset family, perturbation family, and PDR criterion are aligned with PromptRobust.
```

## Run Command

```powershell
python promptrobust_reference_pdr_eval.py --dataset-cases-per-task 2 --samples 3 --temperature 0.7 --top-p 0.9 --perturbations all --output-tag promptrobust_perturbation_sweep_2x3
```

Output files:

- `results/generations_promptrobust_perturbation_sweep_2x3.csv`
- `results/pdr_metrics_promptrobust_perturbation_sweep_2x3.csv`
- `results/pdr_metrics_promptrobust_perturbation_sweep_2x3.json`
- `results/pdr_report_promptrobust_perturbation_sweep_2x3.md`

## Overall Result

| Metric | Value |
|---|---:|
| Average clean single-sample correctness | 0.3750 |
| Average perturbed single-sample correctness | 0.6250 |
| Dataset-level uncorrected single-sample PDR | -0.6667 |
| Average clean repeated correctness | 0.4375 |
| Average perturbed repeated correctness | 0.6250 |
| Dataset-level repeated-sampling PDR | -0.4286 |

Interpretation:

```text
Negative PDR means the perturbed prompt performed better than the clean prompt in this small run.
The magnitude changes after repeated sampling:
uncorrected PDR = -0.6667
repeated-sampling PDR = -0.4286
```

So even when perturbation does not hurt performance, single-sample evaluation still gives a different estimate from repeated-sampling evaluation.

## Horizontal Comparison Table

| Perturbation | Task | Dataset | Clean single perf | Perturbed single perf | Uncorrected PDR | Clean repeated perf | Perturbed repeated perf | Repeated-sampling PDR | Difference |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| Character | Factual QA | SQuAD V2 | 0.5000 | 1.0000 | -1.0000 | 0.6667 | 0.8333 | -0.2500 | -0.7500 |
| Character | Math reasoning | MATH | 0.0000 | 0.0000 | 0.0000 | 0.3333 | 0.3333 | 0.0000 | 0.0000 |
| Word-level | Factual QA | SQuAD V2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| Word-level | Math reasoning | MATH | 0.0000 | 1.0000 | 0.0000 | 0.1667 | 0.8333 | -4.0000 | 4.0000 |
| Sentence-level | Factual QA | SQuAD V2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| Sentence-level | Math reasoning | MATH | 0.5000 | 0.5000 | 0.0000 | 0.3333 | 0.5000 | -0.5000 | 0.5000 |
| Semantic-level | Factual QA | SQuAD V2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| Semantic-level | Math reasoning | MATH | 0.5000 | 1.0000 | -1.0000 | 0.5000 | 1.0000 | -1.0000 | 0.0000 |

Definitions:

```text
Difference = Uncorrected PDR - Repeated-sampling PDR
```

Interpretation:

- `Difference > 0`: uncorrected estimate is higher than repeated-sampling estimate.
- `Difference < 0`: uncorrected estimate is lower than repeated-sampling estimate.
- `Difference = 0`: both estimates agree.

## Main Observations

1. **Factual QA is mostly stable except character-level perturbation.**

   For word-level, sentence-level, and semantic-level perturbations, both uncorrected and repeated-sampling PDR are 0. Character-level perturbation shows perturbed prompts performing better in this small run, but the magnitude is smaller after repeated sampling.

2. **Math reasoning is more variable.**

   Word-level, sentence-level, and semantic-level perturbations often produced better repeated performance than clean prompts in this run. This gives negative PDR values.

3. **Single-sample evaluation can disagree with repeated-sampling evaluation.**

   The clearest case is word-level perturbation on math:

   ```text
   Uncorrected PDR:       0.0000
   Repeated-sampling PDR: -4.0000
   ```

   This happens because the single clean performance was 0, so single-sample PDR cannot represent the improvement seen under repeated sampling.

4. **The experiment supports the need for repeated sampling.**

   Even with the same dataset, same perturbation family, and same PDR criterion, a single clean / perturbed generation can give a misleading estimate.

## Similarity-Based Comparison on the Same Outputs

The same generated outputs were also evaluated with embedding-based similarity drift. This does **not** replace the PromptRobust PDR criterion; it is an auxiliary output-stability comparison using the same datasets and perturbation methods.

Source generations:

```text
results/generations_promptrobust_perturbation_sweep_2x3.csv
```

Similarity output files:

- `results/similarity_metrics_promptrobust_perturbation_sweep_2x3.csv`
- `results/similarity_grouped_promptrobust_perturbation_sweep_2x3.csv`
- `results/similarity_metrics_promptrobust_perturbation_sweep_2x3.json`

Similarity metric definitions:

```text
uncorrected single drift
= embedding distance between the first clean output and first perturbed output

raw perturbation drift
= average embedding distance across all clean-vs-perturbed output pairs

noise baseline
= average within-clean and within-perturbed output distance

noise-corrected drift
= max(0, raw perturbation drift - noise baseline)
```

### Similarity Drift Table

| Perturbation | Task | Dataset | Uncorrected single drift | Noise baseline | Raw drift | Noise-corrected drift |
|---|---|---|---:|---:|---:|---:|
| Character | Factual QA | SQuAD V2 | 0.0516 | 0.0344 | 0.0286 | 0.0000 |
| Character | Math reasoning | MATH | 0.0271 | 0.0181 | 0.0210 | 0.0029 |
| Word-level | Factual QA | SQuAD V2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Word-level | Math reasoning | MATH | 0.0646 | 0.0370 | 0.0422 | 0.0052 |
| Sentence-level | Factual QA | SQuAD V2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Sentence-level | Math reasoning | MATH | 0.0441 | 0.0276 | 0.0277 | 0.0005 |
| Semantic-level | Factual QA | SQuAD V2 | 0.1637 | 0.0025 | 0.1653 | 0.1628 |
| Semantic-level | Math reasoning | MATH | 0.0348 | 0.0346 | 0.0535 | 0.0199 |

### Similarity Interpretation

1. **Semantic-level perturbation creates the largest similarity drift for Factual QA.**

   ```text
   raw drift:              0.1653
   noise-corrected drift:  0.1628
   ```

   The drift remains after subtracting the within-prompt noise baseline.

2. **Math reasoning shows visible sample-noise effects.**

   For word-level and sentence-level perturbations, raw drift is reduced strongly after correction:

   ```text
   Word-level math raw drift:       0.0422
   Word-level math corrected drift: 0.0052

   Sentence-level math raw drift:       0.0277
   Sentence-level math corrected drift: 0.0005
   ```

3. **Some perturbations have near-zero similarity impact on Factual QA.**

   Word-level and sentence-level perturbations produced almost identical short answers in SQuAD V2, so embedding drift is effectively zero.

4. **The similarity results support the same methodological point.**

   Even when the same outputs are evaluated with similarity rather than PDR, the uncorrected single-output estimate and the noise-corrected estimate can differ substantially.

## Caveats

This is still a small validation run:

1. Only 2 cases per task.
2. Only 3 repeated generations per prompt version.
3. The perturbations are PromptRobust-style families, not a full reproduction of adversarial search.
4. Strict exact-match correctness may undercount semantically correct answers.
5. Negative PDR should be interpreted as perturbed performance exceeding clean performance, not as robustness failure.

## Recommended Next Run

If we want a more stable estimate, run:

```powershell
python promptrobust_reference_pdr_eval.py --dataset-cases-per-task 5 --samples 3 --temperature 0.7 --top-p 0.9 --perturbations all --output-tag promptrobust_perturbation_sweep_5x3
```

Expected cost:

```text
5 cases per task × 2 tasks × 4 perturbations × 2 prompt versions × 3 samples
= 240 model calls
```
