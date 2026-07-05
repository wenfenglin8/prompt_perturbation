# RQ1 PDR 50x5 Figure Caption

Suggested caption:

Figure X. Repeated-sampling PDR and within-condition sampling variability for the three objective tasks at 50 cases per task and 5 samples per prompt version. Panel A reports corrected PDR by perturbation and task, computed as the difference between perturbed-prompt loss and clean-prompt loss using repeated-sampling mean performance. Across all task-perturbation cells, clean repeated performance is 0.6279 and perturbed repeated performance is 0.6179, giving a small aggregate corrected PDR of 0.0100. Panel B separately reports within-condition correctness sample noise, whose overall mean is 0.0935; this quantity measures repeated-generation variability and should not be interpreted as additional performance loss.

Chinese note:

图中不要把 corrected PDR=0.0100 和 sample noise=0.0935 写成同一种 loss。左图是扰动后的平均性能损失，右图是同一条件下重复采样的 correctness 波动。

Files:

- PNG: `D:/pioneer_python/results/rq1_figures/rq1_pdr_newloss_50x5_effect_and_sample_noise.png`
- PDF: `D:/pioneer_python/results/rq1_figures/rq1_pdr_newloss_50x5_effect_and_sample_noise.pdf`
- Grouped data: `D:/pioneer_python/results/rq1_figures/rq1_pdr_newloss_50x5_grouped_for_figure.csv`

Task-level sample noise:

- Factual QA: `0.0020`
- Math: `0.2033`
- Code: `0.0751`
