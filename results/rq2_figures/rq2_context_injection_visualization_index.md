# RQ2 Context Injection Dose-Response Visualizations

Source files:

```text
results/rq2_context_injection_dose_response_three_task_stress_5x3_by_level.csv
results/rq2_context_injection_dose_response_three_task_stress_5x3_by_task_level.csv
results/rq2_context_injection_dose_response_three_task_stress_5x3_metrics.csv
```

Generated figures:

1. `rq2_context_injection_overall_dose_response.png`
   - Overall strength-to-similarity and strength-to-performance-change view.

2. `rq2_context_injection_similarity_by_task.png`
   - Task-level output similarity curves across injection strength.

3. `rq2_context_injection_correctness_change_by_task.png`
   - Task-level absolute performance-change curves across injection strength.

4. `rq2_context_injection_similarity_vs_correctness_scatter.png`
   - Case-level nonzero-strength relationship between output similarity and correctness change.

5. `rq2_context_injection_corrected_drift_vs_correctness_scatter.png`
   - Case-level nonzero-strength relationship between noise-corrected drift and correctness change.

Main visual takeaway:

```text
Context injection produces measurable semantic movement, and lower output similarity is associated with larger performance movement. The task-level pattern is strongest for long factual QA, weaker but directionally consistent for code generation, and unstable for math reasoning.
```
