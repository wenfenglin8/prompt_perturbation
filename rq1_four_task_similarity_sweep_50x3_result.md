# RQ1 Four-Task Similarity Sweep 50x3 Result

Updated on 2026-07-03 after completing all 10 batches.

## RQ1

Current RQ1:

```text
After correcting for sample noise, do different perturbation types produce a
stable sensitivity ranking across factual QA, math reasoning, code generation,
and open-ended writing?
```

Short answer:

```text
No. The full 50x3 result shows that corrected perturbation sensitivity rankings
are task-dependent rather than stable across task types.
```

## Experiment Setup

| Item | Setting |
|---|---|
| Model | `gpt-4o-mini` |
| Embedding model | `text-embedding-3-small` |
| Cases per task | 50 |
| Samples per original / perturbed prompt | 3 |
| Tasks | factual QA, math reasoning, code generation, open-ended writing |
| Datasets | SQuAD V2, MATH, HumanEval, Alpaca |
| Perturbations | paraphrase, reordering, formatting, context injection, surface noise |
| Evaluation | embedding-based semantic drift |
| Correction | `max(0, raw_perturbation_drift - noise_baseline)` |
| Batches | 10 |

Total scale:

```text
4 tasks x 50 cases/task x 5 perturbations = 1000 metric rows
1000 case-perturbation comparisons x 2 prompt versions x 3 samples = 6000 generation rows
```

## Output Files

Merged output files:

```text
results/generations_four_task_similarity_sweep_50x3.csv
results/similarity_metrics_four_task_similarity_sweep_50x3.csv
results/similarity_grouped_four_task_similarity_sweep_50x3.csv
results/similarity_rankings_four_task_similarity_sweep_50x3.csv
results/similarity_summary_four_task_similarity_sweep_50x3.json
results/similarity_report_four_task_similarity_sweep_50x3.md
```

Completeness check:

```text
generation rows = 6000 / 6000
metric rows     = 1000 / 1000
completed batches = 10 / 10
```

## Overall Raw vs Corrected Drift

Across all 1000 metric rows:

| Metric | Mean | Std |
|---|---:|---:|
| raw perturbation drift | 0.060849 | 0.083388 |
| noise baseline | 0.045906 | 0.055732 |
| noise-corrected drift | 0.017669 | 0.061468 |
| uncorrected single-sample drift | 0.060273 | 0.097865 |

Sample-noise correction reduces the average apparent perturbation effect from
0.060849 to 0.017669.

```text
Share of raw drift removed by sample-noise correction = 70.96%
```

This supports the core methodological claim that single-sample or raw
original-vs-perturbed comparisons substantially overestimate perturbation-specific
semantic change.

## Task-Level Summary

| Task | N | Raw drift mean | Raw drift std | Noise baseline mean | Noise baseline std | Corrected drift mean | Corrected drift std | Share removed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| code generation | 250 | 0.055106 | 0.076633 | 0.034207 | 0.046559 | 0.023445 | 0.061950 | 57.45% |
| factual QA | 250 | 0.050660 | 0.114437 | 0.026297 | 0.063408 | 0.026823 | 0.094488 | 47.05% |
| math reasoning | 250 | 0.056676 | 0.053980 | 0.050905 | 0.034590 | 0.008600 | 0.030966 | 84.83% |
| open-ended writing | 250 | 0.080954 | 0.073858 | 0.072215 | 0.061912 | 0.011806 | 0.034633 | 85.42% |

Task-level interpretation:

- Factual QA has the highest average noise-corrected drift.
- Code generation is second highest.
- Math reasoning and open-ended writing have lower corrected drift because a large share of their raw drift is explained by within-prompt sample noise.
- Open-ended writing has the largest raw drift, but also a large noise baseline, so its corrected drift is modest.

## Perturbation-Level Summary

| Perturbation | N | Raw drift mean | Raw drift std | Noise baseline mean | Noise baseline std | Corrected drift mean | Corrected drift std | Share removed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| paraphrase | 200 | 0.071854 | 0.099022 | 0.047804 | 0.062266 | 0.026914 | 0.082874 | 62.54% |
| formatting | 200 | 0.066594 | 0.088138 | 0.046083 | 0.052522 | 0.022982 | 0.069478 | 65.49% |
| reordering | 200 | 0.059976 | 0.088857 | 0.047589 | 0.059932 | 0.015814 | 0.061213 | 73.63% |
| context injection | 200 | 0.051279 | 0.065610 | 0.041760 | 0.049943 | 0.011574 | 0.036158 | 77.43% |
| surface noise | 200 | 0.054542 | 0.069613 | 0.046294 | 0.053356 | 0.011059 | 0.044931 | 79.72% |

Overall corrected perturbation ranking:

```text
paraphrase > formatting > reordering > context_injection > surface_noise
```

However, this pooled ranking is not the main RQ1 answer, because RQ1 asks whether
the ranking remains stable across task types. The task-specific rankings below
show that it does not.

## Task-Specific Corrected Rankings

| Task | Rank 1 | Rank 2 | Rank 3 | Rank 4 | Rank 5 |
|---|---|---|---|---|---|
| factual QA | paraphrase | surface noise | formatting | reordering | context injection |
| math reasoning | reordering | formatting | context injection | paraphrase | surface noise |
| code generation | formatting | paraphrase | reordering | surface noise | context injection |
| open-ended writing | formatting | context injection | reordering | paraphrase | surface noise |

Corrected drift values:

| Task | Perturbation | N | Raw drift | Noise baseline | Corrected drift |
|---|---|---:|---:|---:|---:|
| factual QA | paraphrase | 50 | 0.0983 | 0.0373 | 0.0625 |
| factual QA | surface noise | 50 | 0.0381 | 0.0193 | 0.0202 |
| factual QA | formatting | 50 | 0.0437 | 0.0288 | 0.0185 |
| factual QA | reordering | 50 | 0.0400 | 0.0262 | 0.0175 |
| factual QA | context injection | 50 | 0.0332 | 0.0199 | 0.0153 |
| math reasoning | reordering | 50 | 0.0752 | 0.0575 | 0.0200 |
| math reasoning | formatting | 50 | 0.0530 | 0.0480 | 0.0073 |
| math reasoning | context injection | 50 | 0.0505 | 0.0473 | 0.0061 |
| math reasoning | paraphrase | 50 | 0.0512 | 0.0502 | 0.0048 |
| math reasoning | surface noise | 50 | 0.0534 | 0.0516 | 0.0048 |
| code generation | formatting | 50 | 0.0832 | 0.0393 | 0.0451 |
| code generation | paraphrase | 50 | 0.0644 | 0.0327 | 0.0338 |
| code generation | reordering | 50 | 0.0433 | 0.0300 | 0.0180 |
| code generation | surface noise | 50 | 0.0491 | 0.0367 | 0.0147 |
| code generation | context injection | 50 | 0.0355 | 0.0323 | 0.0057 |
| open-ended writing | formatting | 50 | 0.0865 | 0.0683 | 0.0210 |
| open-ended writing | context injection | 50 | 0.0859 | 0.0676 | 0.0192 |
| open-ended writing | reordering | 50 | 0.0813 | 0.0766 | 0.0077 |
| open-ended writing | paraphrase | 50 | 0.0735 | 0.0711 | 0.0066 |
| open-ended writing | surface noise | 50 | 0.0775 | 0.0775 | 0.0046 |

## RQ1 Interpretation

The full 50x3 result answers RQ1 negatively. After sample-noise correction, the
perturbation sensitivity ranking is not stable across factual QA, math reasoning,
code generation, and open-ended writing.

The strongest perturbation differs by task:

| Task | Most sensitive perturbation | Corrected drift |
|---|---|---:|
| factual QA | paraphrase | 0.0625 |
| math reasoning | reordering | 0.0200 |
| code generation | formatting | 0.0451 |
| open-ended writing | formatting | 0.0210 |

This means that prompt perturbation effects should not be treated as a single
global robustness property of the model. Instead, the effect depends on the task
and, as suggested by the large within-task variation, likely also on the specific
case or item.

## Methodological Implication

The experiment supports the need for repeated sampling. The raw drift and
single-sample drift are close in mean, but both are much larger than the
noise-corrected estimate:

```text
uncorrected single-sample drift mean = 0.060273
raw perturbation drift mean          = 0.060849
noise-corrected drift mean           = 0.017669
```

Therefore, comparing one original output with one perturbed output would have
overstated perturbation-specific drift by roughly the same amount as the raw
cross-prompt estimate. The repeated-sampling baseline is necessary to separate
prompt-perturbation effects from ordinary stochastic output variability.

## Proposal-Ready Wording

The full 50x3 four-task similarity sweep shows that raw semantic drift
substantially overestimates perturbation-specific output change. Across 1,000
task-perturbation-case comparisons, the mean raw drift was 0.0608, whereas the
mean noise-corrected drift was 0.0177, indicating that approximately 71% of the
apparent drift was attributable to within-prompt sample noise. After correction,
perturbation sensitivity rankings differed across tasks: factual QA was most
sensitive to paraphrasing, math reasoning to reordering, and both code generation
and open-ended writing to formatting changes. These results answer RQ1 negatively:
there is no stable perturbation sensitivity ranking shared across task types.
Instead, prompt perturbation effects are task-dependent and should be interpreted
after accounting for sample noise.

## Caveats

1. The metric is embedding-based semantic drift, not a direct correctness metric.
2. Each prompt version uses three repeated samples. This is enough to estimate a
   within-prompt baseline, but larger repeated-sampling counts would reduce
   uncertainty in the noise estimate.
3. The task-level ranking is now much more stable than earlier 2x3 and 5x3 pilots,
   but item-level heterogeneity remains important and should be analyzed separately.
