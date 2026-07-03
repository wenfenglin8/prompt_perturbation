# RQ1 Sample Noise by Task and Perturbation, 10x3

Source data:

```text
results/similarity_metrics_four_task_similarity_sweep_pdr_aligned_10x3.csv
```

Experiment scale:

```text
4 tasks x 10 cases/task x 5 perturbations x 2 prompt versions x 3 samples
= 1200 generation rows
= 200 task-perturbation-case metric rows
```

Metric definition:

```text
sample_noise = noise_baseline
             = average(original_noise, perturbed_noise)
```

where `original_noise` is the average pairwise embedding distance among repeated
clean-prompt outputs, and `perturbed_noise` is the average pairwise embedding
distance among repeated perturbed-prompt outputs.

## Overall Result

| n | Mean sample noise | Std | Variance |
|---:|---:|---:|---:|
| 200 | 0.054593 | 0.067311 | 0.004531 |

## By Task

| Task | n | Mean sample noise | Std | Variance |
|---|---:|---:|---:|---:|
| factual_qa | 50 | 0.024689 | 0.045594 | 0.002079 |
| math_reasoning | 50 | 0.049934 | 0.027109 | 0.000735 |
| code_generation | 50 | 0.032547 | 0.045973 | 0.002114 |
| open_ended_writing | 50 | 0.111203 | 0.093661 | 0.008772 |

## Task by Perturbation Results

| Task | Perturbation | n | Mean sample noise | Std | Variance |
|---|---|---:|---:|---:|---:|
| factual_qa | paraphrase | 10 | 0.034908 | 0.056954 | 0.003244 |
| factual_qa | reordering | 10 | 0.017905 | 0.044268 | 0.001960 |
| factual_qa | formatting | 10 | 0.019024 | 0.043906 | 0.001928 |
| factual_qa | context_injection | 10 | 0.026297 | 0.046280 | 0.002142 |
| factual_qa | surface_noise | 10 | 0.025313 | 0.042884 | 0.001839 |
| math_reasoning | paraphrase | 10 | 0.044179 | 0.020593 | 0.000424 |
| math_reasoning | reordering | 10 | 0.054645 | 0.027781 | 0.000772 |
| math_reasoning | formatting | 10 | 0.047005 | 0.024541 | 0.000602 |
| math_reasoning | context_injection | 10 | 0.052615 | 0.032711 | 0.001070 |
| math_reasoning | surface_noise | 10 | 0.051228 | 0.032438 | 0.001052 |
| code_generation | paraphrase | 10 | 0.031307 | 0.051618 | 0.002664 |
| code_generation | reordering | 10 | 0.036827 | 0.039713 | 0.001577 |
| code_generation | formatting | 10 | 0.031320 | 0.052097 | 0.002714 |
| code_generation | context_injection | 10 | 0.027240 | 0.047450 | 0.002252 |
| code_generation | surface_noise | 10 | 0.036041 | 0.047236 | 0.002231 |
| open_ended_writing | paraphrase | 10 | 0.126156 | 0.116060 | 0.013470 |
| open_ended_writing | reordering | 10 | 0.103590 | 0.088314 | 0.007799 |
| open_ended_writing | formatting | 10 | 0.101710 | 0.077161 | 0.005954 |
| open_ended_writing | context_injection | 10 | 0.122026 | 0.109796 | 0.012055 |
| open_ended_writing | surface_noise | 10 | 0.102534 | 0.088634 | 0.007856 |

## Interpretation

The expanded 10x3 simulation gives a more stable estimate of sample noise than
the earlier 5x3 run. The overall mean sample-noise baseline is `0.054593`.

Open-ended writing has the largest sample-noise baseline across all perturbation
modes, with a task-level mean of `0.111203`. This confirms that repeated
generations from the same writing prompt vary substantially even before
attributing any difference to prompt perturbation.

Math reasoning has the second-highest task-level mean sample noise at `0.049934`,
but its standard deviation is lower than factual QA, code generation, and
open-ended writing. This suggests that math reasoning has a relatively consistent
moderate sample-noise baseline across perturbation modes and cases.

Code generation has a lower task-level mean sample noise of `0.032547`, while
factual QA has the lowest mean at `0.024689`. Compared with the 5x3 run, factual
QA no longer appears completely deterministic after increasing the number of
cases from 5 to 10.

Across task-perturbation groups, the highest mean sample noise appears in
open-ended writing under `paraphrase` (`0.126156`) and `context_injection`
(`0.122026`). The lowest mean sample noise appears in factual QA under
`reordering` (`0.017905`) and `formatting` (`0.019024`).

Overall, the 10x3 result strengthens the RQ1 motivation for sample-noise
correction: the amount of repeated-generation variability differs substantially
by task and remains non-negligible for several perturbation modes.
