# Proposal Visual and Statistical Analysis

This report checks the Proposal0.5 plan item about tornado charts, ANOVA, and Tukey HSD.

The tornado charts visualize relative perturbation effects. The ANOVA/Tukey analyses are exploratory because some dependent variables, especially correctness drift, are discrete and bounded.

## rq1_similarity_drift

- Dependent variable: `noise_corrected_drift`
- Rows: `100`
- Caution: Continuous embedding-distance metric; ANOVA is more defensible here than for discrete correctness outcomes, though sample size is still small.

### Tornado Charts

- By perturbation: `D:/pioneer_python/results/proposal_visual_stats/rq1_similarity_drift_tornado_by_perturbation.png`
- By task: `D:/pioneer_python/results/proposal_visual_stats/rq1_similarity_drift_tornado_by_task.png`
- By task x perturbation: `D:/pioneer_python/results/proposal_visual_stats/rq1_similarity_drift_tornado_by_task_perturbation.png`

### Top Perturbation Effects

| perturbation      |   mean |    std |   count |
|:------------------|-------:|-------:|--------:|
| surface_noise     | 0.0339 | 0.1115 |      20 |
| formatting        | 0.0234 | 0.0612 |      20 |
| paraphrase        | 0.0224 | 0.0416 |      20 |
| reordering        | 0.0141 | 0.0404 |      20 |
| context_injection | 0.0058 | 0.0145 |      20 |

### Top Task Effects

| task               |   mean |    std |   count |
|:-------------------|-------:|-------:|--------:|
| open_ended_writing | 0.0370 | 0.1035 |      25 |
| code_generation    | 0.0320 | 0.0616 |      25 |
| factual_qa         | 0.0068 | 0.0234 |      25 |
| math_reasoning     | 0.0038 | 0.0075 |      25 |

### ANOVA: task + perturbation + interaction

| effect                  |   sum_sq |       df |         F |    PR(>F) |
|:------------------------|---------:|---------:|----------:|----------:|
| C(task)                 |  0.02184 |  3.00000 |   1.82698 |   0.14890 |
| C(perturbation)         |  0.00897 |  4.00000 |   0.56276 |   0.69035 |
| C(task):C(perturbation) |  0.03485 | 12.00000 |   0.72897 |   0.71917 |
| Residual                |  0.31872 | 80.00000 | nan       | nan       |

### Tukey HSD Outputs

- Perturbation Tukey table: `D:/pioneer_python/results/proposal_visual_stats/rq1_similarity_drift_tukey_perturbation.csv`
- Task Tukey table: `D:/pioneer_python/results/proposal_visual_stats/rq1_similarity_drift_tukey_task.csv`
- Task x perturbation Tukey table: `D:/pioneer_python/results/proposal_visual_stats/rq1_similarity_drift_tukey_task_perturbation.csv`

## rq2_correctness_drift_exact_fact

- Dependent variable: `abs_repeated_pass_rate_change`
- Rows: `150`
- Caution: Correctness drift is discrete and bounded because each prompt version has three samples; treat ANOVA/Tukey as exploratory.

### Tornado Charts

- By perturbation: `D:/pioneer_python/results/proposal_visual_stats/rq2_correctness_drift_exact_fact_tornado_by_perturbation.png`
- By task: `D:/pioneer_python/results/proposal_visual_stats/rq2_correctness_drift_exact_fact_tornado_by_task.png`
- By task x perturbation: `D:/pioneer_python/results/proposal_visual_stats/rq2_correctness_drift_exact_fact_tornado_by_task_perturbation.png`

### Top Perturbation Effects

| perturbation      |   mean |    std |   count |
|:------------------|-------:|-------:|--------:|
| formatting        | 0.1889 | 0.3238 |      30 |
| surface_noise     | 0.1556 | 0.3244 |      30 |
| paraphrase        | 0.1556 | 0.2587 |      30 |
| context_injection | 0.1222 | 0.2050 |      30 |
| reordering        | 0.0889 | 0.1736 |      30 |

### Top Task Effects

| task            |   mean |    std |   count |
|:----------------|-------:|-------:|--------:|
| math_reasoning  | 0.2267 | 0.2731 |      50 |
| code_generation | 0.1400 | 0.3093 |      50 |
| factual_qa      | 0.0600 | 0.1606 |      50 |

### ANOVA: task + perturbation + interaction

| effect                  |   sum_sq |        df |         F |    PR(>F) |
|:------------------------|---------:|----------:|----------:|----------:|
| C(task)                 |  0.69481 |   2.00000 |   5.14756 |   0.00701 |
| C(perturbation)         |  0.17333 |   4.00000 |   0.64207 |   0.63341 |
| C(task):C(perturbation) |  0.32000 |   8.00000 |   0.59268 |   0.78261 |
| Residual                |  9.11111 | 135.00000 | nan       | nan       |

### Tukey HSD Outputs

- Perturbation Tukey table: `D:/pioneer_python/results/proposal_visual_stats/rq2_correctness_drift_exact_fact_tukey_perturbation.csv`
- Task Tukey table: `D:/pioneer_python/results/proposal_visual_stats/rq2_correctness_drift_exact_fact_tukey_task.csv`
- Task x perturbation Tukey table: `D:/pioneer_python/results/proposal_visual_stats/rq2_correctness_drift_exact_fact_tukey_task_perturbation.csv`

## rq2_harmful_drop_exact_fact

- Dependent variable: `harmful_correctness_drop`
- Rows: `150`
- Caution: Binary outcome; ANOVA is a rough exploratory comparison of group means, not a primary inference model.

### Tornado Charts

- By perturbation: `D:/pioneer_python/results/proposal_visual_stats/rq2_harmful_drop_exact_fact_tornado_by_perturbation.png`
- By task: `D:/pioneer_python/results/proposal_visual_stats/rq2_harmful_drop_exact_fact_tornado_by_task.png`
- By task x perturbation: `D:/pioneer_python/results/proposal_visual_stats/rq2_harmful_drop_exact_fact_tornado_by_task_perturbation.png`

### Top Perturbation Effects

| perturbation      |   mean |    std |   count |
|:------------------|-------:|-------:|--------:|
| paraphrase        | 0.2000 | 0.4068 |      30 |
| formatting        | 0.1667 | 0.3790 |      30 |
| surface_noise     | 0.1000 | 0.3051 |      30 |
| context_injection | 0.1000 | 0.3051 |      30 |
| reordering        | 0.0667 | 0.2537 |      30 |

### Top Task Effects

| task            |   mean |    std |   count |
|:----------------|-------:|-------:|--------:|
| math_reasoning  | 0.1600 | 0.3703 |      50 |
| code_generation | 0.1200 | 0.3283 |      50 |
| factual_qa      | 0.1000 | 0.3030 |      50 |

### ANOVA: task + perturbation + interaction

| effect                  |   sum_sq |        df |         F |    PR(>F) |
|:------------------------|---------:|----------:|----------:|----------:|
| C(task)                 |  0.09333 |   2.00000 |   0.41722 |   0.65972 |
| C(perturbation)         |  0.36000 |   4.00000 |   0.80464 |   0.52425 |
| C(task):C(perturbation) |  1.04000 |   8.00000 |   1.16225 |   0.32658 |
| Residual                | 15.10000 | 135.00000 | nan       | nan       |

### Tukey HSD Outputs

- Perturbation Tukey table: `D:/pioneer_python/results/proposal_visual_stats/rq2_harmful_drop_exact_fact_tukey_perturbation.csv`
- Task Tukey table: `D:/pioneer_python/results/proposal_visual_stats/rq2_harmful_drop_exact_fact_tukey_task.csv`
- Task x perturbation Tukey table: `D:/pioneer_python/results/proposal_visual_stats/rq2_harmful_drop_exact_fact_tukey_task_perturbation.csv`

## rq2_correctness_drift_llm_fact

- Dependent variable: `abs_repeated_pass_rate_change`
- Rows: `150`
- Caution: Sensitivity analysis using LLM-equivalence factual correctness; correctness drift remains discrete and bounded.

### Tornado Charts

- By perturbation: `D:/pioneer_python/results/proposal_visual_stats/rq2_correctness_drift_llm_fact_tornado_by_perturbation.png`
- By task: `D:/pioneer_python/results/proposal_visual_stats/rq2_correctness_drift_llm_fact_tornado_by_task.png`
- By task x perturbation: `D:/pioneer_python/results/proposal_visual_stats/rq2_correctness_drift_llm_fact_tornado_by_task_perturbation.png`

### Top Perturbation Effects

| perturbation      |   mean |    std |   count |
|:------------------|-------:|-------:|--------:|
| paraphrase        | 0.1667 | 0.3001 |      30 |
| formatting        | 0.1667 | 0.3246 |      30 |
| surface_noise     | 0.1444 | 0.3118 |      30 |
| context_injection | 0.0889 | 0.1736 |      30 |
| reordering        | 0.0889 | 0.1736 |      30 |

### Top Task Effects

| task            |   mean |    std |   count |
|:----------------|-------:|-------:|--------:|
| math_reasoning  | 0.2267 | 0.2731 |      50 |
| code_generation | 0.1400 | 0.3093 |      50 |
| factual_qa      | 0.0267 | 0.1482 |      50 |

### ANOVA: task + perturbation + interaction

| effect                  |   sum_sq |        df |         F |    PR(>F) |
|:------------------------|---------:|----------:|----------:|----------:|
| C(task)                 |  1.00593 |   2.00000 |   7.62921 |   0.00073 |
| C(perturbation)         |  0.18815 |   4.00000 |   0.71348 |   0.58409 |
| C(task):C(perturbation) |  0.32741 |   8.00000 |   0.62079 |   0.75923 |
| Residual                |  8.90000 | 135.00000 | nan       | nan       |

### Tukey HSD Outputs

- Perturbation Tukey table: `D:/pioneer_python/results/proposal_visual_stats/rq2_correctness_drift_llm_fact_tukey_perturbation.csv`
- Task Tukey table: `D:/pioneer_python/results/proposal_visual_stats/rq2_correctness_drift_llm_fact_tukey_task.csv`
- Task x perturbation Tukey table: `D:/pioneer_python/results/proposal_visual_stats/rq2_correctness_drift_llm_fact_tukey_task_perturbation.csv`
