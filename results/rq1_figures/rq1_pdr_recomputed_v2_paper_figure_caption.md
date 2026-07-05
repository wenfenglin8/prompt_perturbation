# RQ1 Recomputed V2 PDR Figure Caption

Suggested caption:

Figure X. Repaired PDR analysis for RQ1, excluding open-ended writing. Panel A reports corrected PDR by perturbation type and objective task, in percentage points; cell labels show the corrected PDR value and the within-task harmfulness rank. Panel B decomposes total perturbed loss into clean-prompt baseline loss and the additional perturbation-induced loss. After repairing the math and code evaluators, clean repeated performance is 0.9426 and perturbed repeated performance is 0.9395, yielding a small aggregate corrected PDR of 0.0031. The perturbation ranking is task-dependent: paraphrasing is consistently harmful, but reordering is most harmful for math reasoning while near-neutral or beneficial for the other tasks.

Values to mention in text:

- Factual QA highest corrected PDR: paraphrase `paraphrase` = `0.0072`.
- Math reasoning highest corrected PDR: reordering = `0.0240`.
- Code generation highest corrected PDR: paraphrase = `0.0200`.
- Aggregate corrected PDR: `0.0031`.

Files:

- main_png: `D:/pioneer_python/results/rq1_figures/rq1_pdr_recomputed_v2_task_dependent_ranking.png`
- main_pdf: `D:/pioneer_python/results/rq1_figures/rq1_pdr_recomputed_v2_task_dependent_ranking.pdf`
- bar_png: `D:/pioneer_python/results/rq1_figures/rq1_pdr_recomputed_v2_corrected_pdr_by_task_bars.png`
- bar_pdf: `D:/pioneer_python/results/rq1_figures/rq1_pdr_recomputed_v2_corrected_pdr_by_task_bars.pdf`
- grouped_csv: `D:/pioneer_python/results/rq1_figures/rq1_pdr_recomputed_v2_grouped_for_paper.csv`
