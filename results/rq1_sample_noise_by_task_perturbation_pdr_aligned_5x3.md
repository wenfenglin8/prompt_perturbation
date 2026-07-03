# RQ1 Sample Noise by Task and Perturbation

Source data:

```text
results/similarity_metrics_four_task_similarity_sweep_pdr_aligned_5x3.csv
```

Experiment scale:

```text
4 tasks x 5 cases/task x 5 perturbations x 2 prompt versions x 3 samples
= 600 generation rows
= 100 task-perturbation-case metric rows
```

Metric definition:

```text
sample_noise = noise_baseline
             = average(original_noise, perturbed_noise)
```

where `original_noise` is the average pairwise embedding distance among repeated
clean-prompt outputs, and `perturbed_noise` is the average pairwise embedding
distance among repeated perturbed-prompt outputs.

## Task by Perturbation Results

| Task | Perturbation | n | Mean sample noise | Std | Variance |
|---|---|---:|---:|---:|---:|
| factual_qa | paraphrase | 5 | 0.020128 | 0.036444 | 0.001328 |
| factual_qa | reordering | 5 | 0.000000 | 0.000000 | 0.000000 |
| factual_qa | formatting | 5 | 0.000000 | 0.000000 | 0.000000 |
| factual_qa | context_injection | 5 | 0.000000 | 0.000000 | 0.000000 |
| factual_qa | surface_noise | 5 | 0.000000 | 0.000000 | 0.000000 |
| math_reasoning | paraphrase | 5 | 0.046720 | 0.020800 | 0.000433 |
| math_reasoning | reordering | 5 | 0.042854 | 0.023815 | 0.000567 |
| math_reasoning | formatting | 5 | 0.061287 | 0.032832 | 0.001078 |
| math_reasoning | context_injection | 5 | 0.053210 | 0.029498 | 0.000870 |
| math_reasoning | surface_noise | 5 | 0.061613 | 0.043584 | 0.001900 |
| code_generation | paraphrase | 5 | 0.007657 | 0.012816 | 0.000164 |
| code_generation | reordering | 5 | 0.017336 | 0.022329 | 0.000499 |
| code_generation | formatting | 5 | 0.018572 | 0.021081 | 0.000444 |
| code_generation | context_injection | 5 | 0.026584 | 0.018843 | 0.000355 |
| code_generation | surface_noise | 5 | 0.012754 | 0.023261 | 0.000541 |
| open_ended_writing | paraphrase | 5 | 0.087233 | 0.099437 | 0.009888 |
| open_ended_writing | reordering | 5 | 0.088857 | 0.066385 | 0.004407 |
| open_ended_writing | formatting | 5 | 0.098028 | 0.105365 | 0.011102 |
| open_ended_writing | context_injection | 5 | 0.071900 | 0.068788 | 0.004732 |
| open_ended_writing | surface_noise | 5 | 0.061782 | 0.042485 | 0.001805 |

## Interpretation

Open-ended writing has the highest sample-noise baseline across perturbation
types. This means that repeated generations from the same prompt vary
substantially even before attributing any difference to prompt perturbation.

Math reasoning also shows noticeable sample noise across all five perturbation
modes, especially under `formatting` and `surface_noise`.

Code generation has lower but nonzero sample noise, with the largest mean under
`context_injection`.

Factual QA is nearly deterministic in this setting. Its sample noise is zero for
four perturbation modes and nonzero only under `paraphrase`.

Overall, the result supports the RQ1 motivation for sample-noise correction:
raw perturbation drift can include different amounts of repeated-generation
variability depending on both task type and perturbation mode.
