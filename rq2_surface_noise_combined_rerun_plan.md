# RQ2 Surface Noise Combined Rerun Plan

## Goal

Rerun the surface-noise dose-response experiment by combining:

- `factual_qa`
- `long_factual_qa`
- `math_reasoning`
- `code_generation`

The aim is to increase data volume while keeping the design balanced enough to support a clean comparison across LongFactQA and the three existing objective tasks.

## Current Status

The current `rq2_perturbation_dose_response.py` script already supports running all four tasks together:

```text
--tasks factual_qa,long_factual_qa,math_reasoning,code_generation
```

The LongFactQA stress-decoy set has been expanded and is sufficient for the doubled run:

```text
LONG_FACTQA_STRESS_CASES >= 24
```

Therefore, this run is balanced:

```text
--dataset-cases-per-task 50
```

```text
factual_qa       50 cases
long_factual_qa  50 cases
math_reasoning   50 cases
code_generation  50 cases
```

## Recommended Data Volume

The recommended next run is:

```text
4 tasks x 50 cases/task x 5 strength levels x 5 samples
= 200 base cases
= 1000 case-level metric rows
= 5000 generation requests
```

Strength levels:

```text
0, 2, 4, 8, 16 corrupted instruction words
```

This is a good balance between cost and stability. Surface noise has a weaker effect than context injection, so increasing the number of cases is more useful than only increasing repeated samples.

The current code has enough LongFactQA stress-decoy cases for this run, using explicit stress cases plus deterministic generated stress-decoy cases.

## Not Recommended As First Expansion

Do not prioritize:

```text
--samples 7
```

before increasing case count. For surface noise, the main weakness is limited task/case coverage rather than only repeated-sampling variance.

## No-Code-Change Balanced Run

With the current code and current LongFactQA stress set, the largest balanced run is:

```powershell
python rq2_perturbation_dose_response.py `
  --dataset-cases-per-task 5 `
  --samples 5 `
  --levels 0,2,4,8,16 `
  --tasks factual_qa,long_factual_qa,math_reasoning,code_generation `
  --long-factqa-set stress `
  --perturbation-family surface_noise `
  --sleep 0 `
  --output-tag rq2_surface_noise_combined_balanced_5x5_l0_2_4_8_16 `
  --resume
```

Expected data volume:

```text
4 tasks x 5 cases/task x 5 levels = 100 metric rows
20 base cases x 5 prompt versions x 5 samples = 500 generation requests
```

This is balanced, but it is only a modest increase over the current combined result.

## Recommended Run After Expanding LongFactQA

Run:

```powershell
python rq2_perturbation_dose_response.py `
  --dataset-cases-per-task 50 `
  --samples 5 `
  --levels 0,2,4,8,16 `
  --tasks factual_qa,long_factual_qa,math_reasoning,code_generation `
  --long-factqa-set stress `
  --perturbation-family surface_noise `
  --sleep 0 `
  --output-tag rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16 `
  --resume
```

Expected data volume:

```text
4 tasks x 50 cases/task x 5 levels = 1000 metric rows
200 base cases x 5 prompt versions x 5 samples = 5000 generation requests
```

This is the recommended version for reporting.

## Visualization Update Needed

The current combined plotting script:

```text
plot_rq2_surface_noise_combined.py
```

currently reads two fixed source files:

```text
results/rq2_surface_noise_dose_response_from_kayley_5x3_metrics.csv
results/rq2_surface_noise_dose_response_longfact_stress_5x3_metrics.csv
```

For the rerun, it should be updated to accept a direct metrics file:

```powershell
python plot_rq2_surface_noise_combined.py `
  --metrics results/rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_metrics.csv `
  --tag rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16
```

Recommended output files:

```text
results/rq2_figures/rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_by_level.csv
results/rq2_figures/rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_by_task_level.csv
results/rq2_figures/rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_overall_dose_response.png
results/rq2_figures/rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_similarity_by_task.png
results/rq2_figures/rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_correctness_change_by_task.png
results/rq2_figures/rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_similarity_vs_correctness_scatter.png
results/rq2_figures/rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_corrected_drift_vs_correctness_scatter.png
results/rq2_figures/rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_visualization_index.md
```

## Final Recommendation

Use the `50 cases/task`, `5 samples`, `5 levels` design:

```text
tasks = factual_qa,long_factual_qa,math_reasoning,code_generation
cases_per_task = 50
samples = 5
levels = 0,2,4,8,16
total_metric_rows = 1000
total_generation_requests = 5000
```

The current code has enough LongFactQA stress cases for this `50x5` run.
