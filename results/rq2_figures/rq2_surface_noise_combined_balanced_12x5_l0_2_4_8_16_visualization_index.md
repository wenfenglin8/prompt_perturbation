# RQ2 Surface Noise Combined Visualizations

Source files:

- `results\rq2_surface_noise_combined_balanced_12x5_l0_2_4_8_16_metrics.csv`

Design:

- Perturbation family: `surface_noise`
- Tasks: `factual_qa, math_reasoning, code_generation, long_factual_qa`
- Cases per task: `{'code_generation': 12, 'factual_qa': 12, 'long_factual_qa': 12, 'math_reasoning': 12}`
- Samples per prompt version: `NA; see source experiment summary/report`
- Strength levels: `0, 2, 4, 8, 16` corrupted instruction words
- Combined case-level rows: `240`

Generated files:

- `rq2_surface_noise_combined_balanced_12x5_l0_2_4_8_16_by_level.csv`
- `rq2_surface_noise_combined_balanced_12x5_l0_2_4_8_16_by_task_level.csv`
- `rq2_surface_noise_combined_balanced_12x5_l0_2_4_8_16_overall_dose_response.png`
- `rq2_surface_noise_combined_balanced_12x5_l0_2_4_8_16_similarity_by_task.png`
- `rq2_surface_noise_combined_balanced_12x5_l0_2_4_8_16_correctness_change_by_task.png`
- `rq2_surface_noise_combined_balanced_12x5_l0_2_4_8_16_similarity_vs_correctness_scatter.png`
- `rq2_surface_noise_combined_balanced_12x5_l0_2_4_8_16_corrected_drift_vs_correctness_scatter.png`

Key statistics:

- Strength vs mean cross similarity, Spearman: `-0.4672`
- Strength vs absolute repeated-pass-rate change, Spearman: `0.2314`
- Nonzero-level similarity vs absolute correctness change, Spearman: `-0.2441`
- Nonzero-level corrected drift vs absolute correctness change, Spearman: `0.2066`

Combined mean by strength:

|   strength_edits |       n |   mean_cross_similarity |   mean_noise_corrected_drift |   mean_abs_repeated_pass_rate_change |   share_harmful_correctness_drop |   share_correctness_changed |
|-----------------:|--------:|------------------------:|-----------------------------:|-------------------------------------:|---------------------------------:|----------------------------:|
|           0.0000 | 48.0000 |                  1.0000 |                       0.0000 |                               0.0000 |                           0.0000 |                      0.0000 |
|           2.0000 | 48.0000 |                  0.9677 |                       0.0029 |                               0.0663 |                           0.1458 |                      0.2708 |
|           4.0000 | 48.0000 |                  0.9634 |                       0.0068 |                               0.0760 |                           0.2083 |                      0.2917 |
|           8.0000 | 48.0000 |                  0.9676 |                       0.0043 |                               0.0761 |                           0.2708 |                      0.3542 |
|          16.0000 | 48.0000 |                  0.9647 |                       0.0057 |                               0.0734 |                           0.2083 |                      0.3125 |

Interpretation:

Combining LongFactQA with the three-task result keeps the expected surface-noise similarity trend: stronger surface noise lowers output similarity. The correctness movement remains modest and task-dependent, so this combined result is best treated as a contrast condition rather than the strongest RQ2 dose-response evidence.
