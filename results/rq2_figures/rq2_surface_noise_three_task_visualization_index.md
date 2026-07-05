# RQ2 Surface Noise Three-Task Visualizations

Source data:

- `results/rq2_surface_noise_dose_response_from_kayley_5x3_report.md`
- `results/rq2_surface_noise_dose_response_from_kayley_5x3_by_level.csv`
- `results/rq2_surface_noise_dose_response_from_kayley_5x3_by_task_level.csv`
- `results/rq2_surface_noise_dose_response_from_kayley_5x3_metrics.csv`

Design:

- Perturbation family: `surface_noise`
- Tasks: `factual_qa`, `math_reasoning`, `code_generation`
- Cases per task: `5`
- Samples per prompt version: `3`
- Strength levels: `0`, `1`, `2`, `4`, `8` corrupted instruction words
- Case-level rows: `75`

Figures:

- `rq2_surface_noise_three_task_overall_dose_response.png`
- `rq2_surface_noise_three_task_similarity_by_task.png`
- `rq2_surface_noise_three_task_correctness_change_by_task.png`
- `rq2_surface_noise_three_task_similarity_vs_correctness_scatter.png`
- `rq2_surface_noise_three_task_corrected_drift_vs_correctness_scatter.png`

Key statistics from the source report:

- Strength vs mean cross similarity: Spearman `-0.4164`
- Strength vs absolute repeated-pass-rate change: Spearman `0.1903`
- Nonzero-level similarity vs absolute correctness change: Spearman `-0.4914`
- Nonzero-level noise-corrected drift vs absolute correctness change: Spearman `0.2622`

Interpretation:

The three-task surface-noise result shows that increasing surface noise generally lowers output similarity. The relationship to correctness movement is weaker than the context-injection stress result, but the nonzero-level similarity/correctness association is in the expected direction: lower similarity is associated with larger correctness movement.
