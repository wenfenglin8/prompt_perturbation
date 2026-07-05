# RQ2 Surface Noise Combined Visualizations

Source files:

- `results\rq2_surface_noise_dose_response_from_kayley_5x3_metrics.csv`
- `results\rq2_surface_noise_dose_response_longfact_stress_5x3_metrics.csv`

Design:

- Perturbation family: `surface_noise`
- Cohorts combined: `three_task` + `longfact_stress`
- Tasks: `factual_qa`, `math_reasoning`, `code_generation`, `long_factual_qa`
- Cases per task: `5`
- Samples per prompt version: `3`
- Strength levels: `0`, `1`, `2`, `4`, `8` corrupted instruction words
- Combined case-level rows: `100`

Generated files:

- `rq2_surface_noise_combined_by_level.csv`
- `rq2_surface_noise_combined_by_task_level.csv`
- `rq2_surface_noise_combined_overall_dose_response.png`
- `rq2_surface_noise_combined_similarity_by_task.png`
- `rq2_surface_noise_combined_correctness_change_by_task.png`
- `rq2_surface_noise_combined_similarity_vs_correctness_scatter.png`
- `rq2_surface_noise_combined_corrected_drift_vs_correctness_scatter.png`

Key statistics:

- Strength vs mean cross similarity, Spearman: `-0.4373`
- Strength vs absolute repeated-pass-rate change, Spearman: `0.2120`
- Nonzero-level similarity vs absolute correctness change, Spearman: `-0.5332`
- Nonzero-level corrected drift vs absolute correctness change, Spearman: `0.1673`

Combined mean by strength:

|   strength_edits |       n |   mean_cross_similarity |   mean_noise_corrected_drift |   mean_abs_repeated_pass_rate_change |   share_harmful_correctness_drop |   share_correctness_changed |
|-----------------:|--------:|------------------------:|-----------------------------:|-------------------------------------:|---------------------------------:|----------------------------:|
|           0.0000 | 20.0000 |                  1.0000 |                       0.0000 |                               0.0000 |                           0.0000 |                      0.0000 |
|           1.0000 | 20.0000 |                  0.9756 |                       0.0011 |                               0.1042 |                           0.0500 |                      0.2500 |
|           2.0000 | 20.0000 |                  0.9771 |                       0.0006 |                               0.0732 |                           0.0500 |                      0.3000 |
|           4.0000 | 20.0000 |                  0.9714 |                       0.0014 |                               0.0524 |                           0.0500 |                      0.2000 |
|           8.0000 | 20.0000 |                  0.9702 |                       0.0045 |                               0.1211 |                           0.1000 |                      0.3500 |

Interpretation:

Combining LongFactQA with the three-task result keeps the expected surface-noise similarity trend: stronger surface noise lowers output similarity. The correctness movement remains modest and task-dependent, so this combined result is best treated as a contrast condition rather than the strongest RQ2 dose-response evidence.
