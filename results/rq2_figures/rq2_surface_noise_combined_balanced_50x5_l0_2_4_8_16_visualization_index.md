# RQ2 Surface Noise Combined Visualizations

Source files:

- `results\rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_batch1of5_metrics.csv`
- `results\rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_batch2of5_metrics.csv`
- `results\rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_batch3of5_metrics.csv`
- `results\rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_batch4of5_metrics.csv`
- `results\rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_batch5of5_metrics.csv`

Design:

- Perturbation family: `surface_noise`
- Tasks: `factual_qa, math_reasoning, code_generation, long_factual_qa`
- Cases per task: `{'code_generation': 50, 'factual_qa': 50, 'long_factual_qa': 50, 'math_reasoning': 50}`
- Samples per prompt version: `NA; see source experiment summary/report`
- Strength levels: `0, 2, 4, 8, 16` corrupted instruction words
- Combined case-level rows: `1000`

Generated files:

- `rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_by_level.csv`
- `rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_by_task_level.csv`
- `rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_overall_dose_response.png`
- `rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_similarity_by_task.png`
- `rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_correctness_change_by_task.png`
- `rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_similarity_vs_correctness_scatter.png`
- `rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16_corrected_drift_vs_correctness_scatter.png`

Key statistics:

- Strength vs mean cross similarity, Spearman: `-0.4800`
- Strength vs absolute repeated-pass-rate change, Spearman: `0.2659`
- Nonzero-level similarity vs absolute correctness change, Spearman: `-0.4460`
- Nonzero-level corrected drift vs absolute correctness change, Spearman: `0.3137`

Combined mean by strength:

|   strength_edits |        n |   mean_cross_similarity |   mean_noise_corrected_drift |   mean_abs_repeated_pass_rate_change |   share_harmful_correctness_drop |   share_correctness_changed |
|-----------------:|---------:|------------------------:|-----------------------------:|-------------------------------------:|---------------------------------:|----------------------------:|
|           0.0000 | 200.0000 |                  1.0000 |                       0.0000 |                               0.0000 |                           0.0000 |                      0.0000 |
|           2.0000 | 200.0000 |                  0.9611 |                       0.0070 |                               0.0781 |                           0.1500 |                      0.3900 |
|           4.0000 | 200.0000 |                  0.9581 |                       0.0109 |                               0.0889 |                           0.1700 |                      0.3750 |
|           8.0000 | 200.0000 |                  0.9565 |                       0.0125 |                               0.0984 |                           0.1900 |                      0.4150 |
|          16.0000 | 200.0000 |                  0.9534 |                       0.0131 |                               0.0964 |                           0.2250 |                      0.4300 |

Interpretation:

Combining LongFactQA with the three-task result keeps the expected surface-noise similarity trend: stronger surface noise lowers output similarity. The correctness movement remains modest and task-dependent, so this combined result is best treated as a contrast condition rather than the strongest RQ2 dose-response evidence.
