# RQ2 Surface Noise LongFactQA Stress Visualizations

Source files:

```text
results/rq2_surface_noise_dose_response_longfact_stress_5x3_by_level.csv
results/rq2_surface_noise_dose_response_longfact_stress_5x3_metrics.csv
```

Generated figures:

1. `rq2_surface_noise_longfact_overall_dose_response.png`
   - Strength-to-similarity plus performance movement / corrected drift / harmful-drop share.

2. `rq2_surface_noise_longfact_similarity_vs_correctness_scatter.png`
   - Case-level relationship between output similarity and correctness change for nonzero surface-noise levels.

3. `rq2_surface_noise_longfact_corrected_drift_vs_correctness_scatter.png`
   - Case-level relationship between noise-corrected drift and correctness change for nonzero surface-noise levels.

Main visual takeaway:

```text
Surface noise changes similarity slightly and lower similarity is associated with larger performance movement, but corrected drift does not show a clean positive relationship with correctness change. This supports using surface noise as a contrast condition rather than the main RQ2 dose-response evidence.
```
