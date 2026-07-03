# RQ1 Four-Task Similarity Sweep 5x3 Result

本实验是在之前 2x3 pilot matrix 基础上扩大数据量后的结果。

## Experiment Setup

| Item | Setting |
|---|---|
| Model | `gpt-4o-mini` |
| Embedding model | `text-embedding-3-small` |
| Cases per task | 5 |
| Samples per clean / perturbed prompt | 3 |
| Tasks | factual QA, math reasoning, code generation, open-ended writing |
| Datasets | SQuAD V2, MATH, HumanEval, Alpaca |
| Perturbations | character, word, sentence, semantic |
| Evaluation | embedding-based similarity / semantic drift |
| Correction | `max(0, raw drift - noise baseline)` |

Run command:

```powershell
python four_task_similarity_sweep.py --dataset-cases-per-task 5 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag four_task_similarity_sweep_5x3
```

Total generation calls:

```text
4 tasks × 5 cases × 4 perturbations × 2 prompt versions × 3 samples = 480
```

## Output Files

| File | Content |
|---|---|
| `results/generations_four_task_similarity_sweep_5x3.csv` | All generated outputs |
| `results/similarity_metrics_four_task_similarity_sweep_5x3.csv` | Per-case metrics |
| `results/similarity_grouped_four_task_similarity_sweep_5x3.csv` | Task × perturbation grouped metrics |
| `results/similarity_rankings_four_task_similarity_sweep_5x3.csv` | Corrected ranking per task |
| `results/similarity_summary_four_task_similarity_sweep_5x3.json` | Full structured result |
| `results/similarity_report_four_task_similarity_sweep_5x3.md` | Auto-generated report |

## Grouped Drift Result

| Task | Dataset | Perturbation | N | Uncorrected single drift | Noise baseline | Raw drift | Corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| Factual QA | SQuAD V2 | character | 5 | 0.0000 | 0.0168 | 0.0168 | 0.0000 |
| Factual QA | SQuAD V2 | word | 5 | 0.0674 | 0.0090 | 0.0594 | 0.0504 |
| Factual QA | SQuAD V2 | sentence | 5 | 0.0003 | 0.0000 | 0.0003 | 0.0003 |
| Factual QA | SQuAD V2 | semantic | 5 | 0.0890 | 0.0235 | 0.1276 | 0.1042 |
| Math reasoning | MATH | character | 5 | 0.0466 | 0.0559 | 0.0557 | 0.0029 |
| Math reasoning | MATH | word | 5 | 0.3901 | 0.1239 | 0.3174 | 0.1934 |
| Math reasoning | MATH | sentence | 5 | 0.0622 | 0.0404 | 0.0594 | 0.0226 |
| Math reasoning | MATH | semantic | 5 | 0.0584 | 0.0474 | 0.0654 | 0.0188 |
| Code generation | HumanEval | character | 5 | 0.0352 | 0.0069 | 0.0408 | 0.0340 |
| Code generation | HumanEval | word | 5 | 0.1262 | 0.0167 | 0.1143 | 0.0976 |
| Code generation | HumanEval | sentence | 5 | 0.0106 | 0.0162 | 0.0157 | 0.0000 |
| Code generation | HumanEval | semantic | 5 | 0.1310 | 0.0121 | 0.1218 | 0.1097 |
| Open-ended writing | Alpaca | character | 5 | 0.1738 | 0.0799 | 0.1803 | 0.1013 |
| Open-ended writing | Alpaca | word | 5 | 0.1158 | 0.0694 | 0.1478 | 0.0786 |
| Open-ended writing | Alpaca | sentence | 5 | 0.1724 | 0.1054 | 0.1857 | 0.0804 |
| Open-ended writing | Alpaca | semantic | 5 | 0.1643 | 0.0962 | 0.1393 | 0.0433 |

## Corrected Sensitivity Ranking

| Task | Rank 1 | Rank 2 | Rank 3 | Rank 4 |
|---|---|---|---|---|
| Factual QA | semantic (0.1042) | word (0.0504) | sentence (0.0003) | character (0.0000) |
| Math reasoning | word (0.1934) | sentence (0.0226) | semantic (0.0188) | character (0.0029) |
| Code generation | semantic (0.1097) | word (0.0976) | character (0.0340) | sentence (0.0000) |
| Open-ended writing | character (0.1013) | sentence (0.0804) | word (0.0786) | semantic (0.0433) |

## Raw vs Corrected Sensitivity Ranking

To test whether sample-noise correction changes the perturbation ranking, we compare:

```text
Raw ranking
= ranking by raw perturbation drift

Corrected ranking
= ranking by noise-corrected drift
```

| Task | Raw drift ranking | Corrected drift ranking | Changed? |
|---|---|---|---|
| Factual QA | semantic > word > character > sentence | semantic > word > sentence > character | small change |
| Math reasoning | word > semantic > sentence > character | word > sentence > semantic > character | yes |
| Code generation | semantic > word > character > sentence | semantic > word > character > sentence | no |
| Open-ended writing | sentence > character > word > semantic | character > sentence > word > semantic | yes |

### Interpretation

Sample-noise correction changes the sensitivity ranking for some tasks.

For **Factual QA**, the top two perturbations are stable:

```text
semantic > word
```

Only the low-impact perturbations change order:

```text
raw:       character > sentence
corrected: sentence > character
```

For **Math reasoning**, the strongest perturbation remains stable:

```text
word
```

But correction changes the middle ranking:

```text
raw:       semantic > sentence
corrected: sentence > semantic
```

This suggests that part of the semantic and sentence-level raw drift is affected by within-prompt variability.

For **Code generation**, the ranking is unchanged:

```text
semantic > word > character > sentence
```

This suggests that, in this run, code-generation similarity ranking is relatively stable under sample-noise correction.

For **Open-ended writing**, the top perturbation changes:

```text
raw:       sentence
corrected: character
```

This is important because open-ended writing has larger within-prompt variability. The raw drift ranking is therefore more likely to be influenced by sample noise.

### Main Takeaway

The comparison shows that sample-noise correction does not only reduce drift values. It can also change the interpretation of which perturbation type is most influential.

In this 5x3 run:

```text
ranking changed for Math reasoning and Open-ended writing;
ranking stayed mostly stable for Factual QA and Code generation.
```

This directly supports RQ1:

```text
sample-noise correction can change prompt-perturbation sensitivity rankings, and the effect is task-dependent.
```

## Comparison With 2x3 Pilot

| Task | 2x3 Rank 1 | 5x3 Rank 1 | Stable? |
|---|---|---|---|
| Factual QA | semantic | semantic | yes |
| Math reasoning | word | word | yes |
| Code generation | semantic | semantic | yes |
| Open-ended writing | sentence | character | no |

The top perturbation remains stable for factual QA, math reasoning, and code generation. Open-ended writing changes from sentence-level to character-level as the top corrected drift, suggesting that this task is more sensitive to sample selection and generation variability.

## Main RQ1 Finding

The 5x3 run strengthens the pilot RQ1 conclusion:

```text
Corrected perturbation sensitivity rankings are task-dependent.
```

Each task has a different strongest perturbation after sample-noise correction:

| Task | Most sensitive perturbation | Corrected drift |
|---|---|---:|
| Factual QA | semantic | 0.1042 |
| Math reasoning | word | 0.1934 |
| Code generation | semantic | 0.1097 |
| Open-ended writing | character | 0.1013 |

## Effect of Sample-Noise Correction

Sample-noise correction changes several raw-drift interpretations:

| Task | Perturbation | Raw drift | Noise baseline | Corrected drift | Interpretation |
|---|---|---:|---:|---:|---|
| Factual QA | character | 0.0168 | 0.0168 | 0.0000 | raw drift fully explained by noise |
| Math reasoning | character | 0.0557 | 0.0559 | 0.0029 | most raw drift explained by noise |
| Code generation | sentence | 0.0157 | 0.0162 | 0.0000 | raw drift fully explained by noise |
| Open-ended writing | semantic | 0.1393 | 0.0962 | 0.0433 | large raw drift reduced substantially |

This supports the sample-noise correction argument:

```text
raw perturbation drift can overstate perturbation-specific effects.
```

## Task-Level Interpretation

### Factual QA

Factual QA is most sensitive to semantic perturbation:

```text
semantic corrected drift = 0.1042
word corrected drift     = 0.0504
```

Character-level perturbation disappears after correction.

### Math Reasoning

Math reasoning is most sensitive to word-level instruction rewrite:

```text
word corrected drift = 0.1934
```

This is consistent with the 2x3 pilot where word-level perturbation was also the strongest for MATH.

### Code Generation

Code generation is most sensitive to semantic and word-level instruction rewrites:

```text
semantic corrected drift = 0.1097
word corrected drift     = 0.0976
```

Sentence-level perturbation has almost no corrected drift.

### Open-Ended Writing

Open-ended writing has the largest noise baselines and a less stable ranking:

```text
character corrected drift = 0.1013
sentence corrected drift  = 0.0804
word corrected drift      = 0.0786
semantic corrected drift  = 0.0433
```

The differences between the top three perturbations are not large, so this task needs more samples before making a strong ranking claim.

## Current RQ1 Status

After this run:

```text
RQ1 pilot matrix is complete and expanded from 2 cases/task to 5 cases/task.
```

Remaining gaps for benchmark-scale evidence:

1. Increase cases per task beyond 5.
2. Add HumanEval unit-test pass rate for code correctness.
3. Add Alpaca quality metrics beyond embedding drift.
4. Repeat with another model if needed.

## Short Summary

```text
The expanded 5x3 four-task similarity sweep confirms that corrected sensitivity rankings differ across tasks. Semantic perturbation is strongest for factual QA and code generation, word-level perturbation is strongest for math reasoning, and open-ended writing remains more variable with character/sentence/word perturbations close together. Sample-noise correction removes or substantially reduces several raw drift effects, supporting the need for repeated sampling.
```
