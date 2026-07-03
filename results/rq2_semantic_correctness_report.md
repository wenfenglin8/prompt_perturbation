# RQ2 Semantic Drift vs Correctness Change

## Question

RQ2 asks whether semantic drift predicts correctness changes for objective tasks.

This first implementation excludes open-ended writing and uses factual QA, math reasoning, and code generation only.

## Data Source

- Generations: `D:/pioneer_python/results/generations_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv`
- Correctness metrics: `D:/pioneer_python/results/pdr_metrics_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv`
- Embedding model: `text-embedding-3-small`
- Case-level comparisons: `150`

## Method

For each case, the script embeds the three original outputs and three perturbed outputs from the same PDR run.
It computes original sample noise, perturbed sample noise, raw cross-version drift, and noise-corrected drift.
The primary correctness-change variable is absolute repeated pass-rate change; PDR is reported as an auxiliary normalized metric.

This report also treats sample-noise correction as an explicit comparison factor, linking RQ1's noise-corrected drift design to RQ2's correctness-prediction question.

## Overall Result

| scope_type | scope_value | n | relationship | pearson | spearman | spearman_ci95_low | spearman_ci95_high | spearman_permutation_p_two_sided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overall | all | 150 | primary | 0.328 | 0.346 | 0.188 | 0.503 | 0.001 |

The primary overall relationship is positive: larger semantic drift tends to align with larger correctness change.

## Sample-Noise Correction Comparison

This section directly tests whether sample-noise corrected similarity drift is a better indicator of correctness drift than uncorrected similarity drift.
The target is the same in the main comparison: absolute repeated pass-rate change.

| drift_measure | correction_status | sampling_design | correctness_target | comparison_role | pearson | spearman | spearman_ci95_low | spearman_ci95_high | spearman_permutation_p_two_sided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| noise_corrected_drift | sample_noise_corrected | repeated_3x3 | abs_repeated_pass_rate_change | primary_rq2_measure | 0.328 | 0.346 | 0.188 | 0.503 | 0.001 |
| raw_perturbation_drift | uncorrected_raw_cross_drift | repeated_3x3 | abs_repeated_pass_rate_change | same_target_uncorrected_baseline | 0.298 | 0.375 | 0.243 | 0.500 | 0.001 |
| uncorrected_single_drift | uncorrected_single_pair | single_pair | abs_repeated_pass_rate_change | single_pair_to_repeated_target_baseline | 0.267 | 0.332 | 0.188 | 0.463 | 0.001 |
| uncorrected_single_drift | uncorrected_single_pair | single_pair | abs_single_pass_rate_change | single_pair_internal_baseline | 0.298 | 0.334 | 0.200 | 0.455 | 0.001 |

On the repeated-sampling correctness target, the sample-noise corrected measure has Spearman 0.346, while raw uncorrected cross-drift has Spearman 0.375.

## Sample-Noise Correction Gain

| baseline_type | correctness_drift_target | corrected_pearson | baseline_pearson | pearson_delta_corrected_minus_baseline | pearson_delta_ci95_low | pearson_delta_ci95_high | corrected_spearman | baseline_spearman | spearman_delta_corrected_minus_baseline | spearman_delta_ci95_low | spearman_delta_ci95_high | spearman_delta_permutation_p_greater | corrected_better_by_pearson | corrected_better_by_spearman |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uncorrected_raw_cross_drift | abs_repeated_pass_rate_change | 0.328 | 0.298 | 0.030 | -0.073 | 0.233 | 0.346 | 0.375 | -0.029 | -0.196 | 0.138 | 0.617 | 1 | 0 |
| uncorrected_single_pair | abs_repeated_pass_rate_change | 0.328 | 0.267 | 0.061 | -0.059 | 0.294 | 0.346 | 0.332 | 0.015 | -0.168 | 0.189 | 0.462 | 1 | 1 |

Against raw cross-drift, sample-noise correction changes Pearson by 0.030 and Spearman by -0.029.
Against the single-pair baseline, sample-noise correction changes Pearson by 0.061 and Spearman by 0.015.
In this first RQ2 run, correction improves Pearson association with correctness drift, especially relative to the single-pair baseline, but it does not improve Spearman rank association over raw repeated cross-drift.

## Correctness Degradation

The primary RQ2 target measures absolute correctness drift. To separate change from degradation, this section checks whether similarity drift indicates harmful correctness drops.

| relationship | x | y | n | pearson | spearman | spearman_ci95_low | spearman_ci95_high | spearman_permutation_p_two_sided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| harmful_drop_binary | noise_corrected_drift | harmful_correctness_drop | 150 | 0.247 | 0.306 | 0.145 | 0.463 | 0.001 |
| raw_harmful_drop_binary | raw_perturbation_drift | harmful_correctness_drop | 150 | 0.200 | 0.213 | 0.074 | 0.340 | 0.009 |

This distinguishes the question 'did correctness move?' from 'did correctness get worse?'.

## By Task

| scope_value | n | relationship | pearson | spearman | spearman_ci95_low | spearman_ci95_high |
| --- | --- | --- | --- | --- | --- | --- |
| code_generation | 50 | primary | 0.747 | 0.515 | 0.180 | 0.732 |
| factual_qa | 50 | primary | 0.006 | 0.224 | -0.162 | 0.535 |
| math_reasoning | 50 | primary | -0.060 | 0.232 | -0.044 | 0.507 |

## By Perturbation

| scope_value | n | relationship | pearson | spearman | spearman_ci95_low | spearman_ci95_high |
| --- | --- | --- | --- | --- | --- | --- |
| context_injection | 30 | primary | 0.656 | 0.467 | 0.055 | 0.776 |
| formatting | 30 | primary | 0.577 | 0.221 | -0.213 | 0.605 |
| paraphrase | 30 | primary | 0.119 | 0.112 | -0.233 | 0.471 |
| reordering | 30 | primary | 0.613 | 0.271 | -0.195 | 0.655 |
| surface_noise | 30 | primary | 0.436 | 0.608 | 0.245 | 0.876 |

## Case Inspection Preview

| inspection_category | rank | case_id | task | perturbation | noise_corrected_drift | raw_perturbation_drift | clean_mean_correctness | perturbed_mean_correctness | repeated_pass_rate_drop | abs_repeated_pass_rate_change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_corrected_drift_high_correctness_drift | 1 | promptrobust_pdr_formatting_humaneval_03 | code_generation | formatting | 0.3492243914049976 | 0.3492243914049977 | 1.0 | 0.0 | 1.0 | 1.0 |
| high_corrected_drift_high_correctness_drift | 2 | promptrobust_pdr_paraphrase_humaneval_04 | code_generation | paraphrase | 0.16976289069259254 | 0.16976289069259265 | 1.0 | 0.0 | 1.0 | 1.0 |
| high_corrected_drift_high_correctness_drift | 3 | promptrobust_pdr_formatting_humaneval_09 | code_generation | formatting | 0.12303028863511735 | 0.12326928112127196 | 1.0 | 0.0 | 1.0 | 1.0 |
| high_corrected_drift_no_correctness_drift | 1 | promptrobust_pdr_paraphrase_squad_08 | factual_qa | paraphrase | 0.41575019866255514 | 0.41575019866255525 | 0.0 | 0.0 | 0.0 | 0.0 |
| high_corrected_drift_no_correctness_drift | 2 | promptrobust_pdr_formatting_math_03 | math_reasoning | formatting | 0.10500771683898985 | 0.16746868786033084 | 0.0 | 0.0 | 0.0 | 0.0 |
| high_corrected_drift_no_correctness_drift | 3 | promptrobust_pdr_surface_noise_humaneval_01 | code_generation | surface_noise | 0.06829442710378233 | 0.07501916417337598 | 0.0 | 0.0 | 0.0 | 0.0 |
| low_corrected_drift_high_correctness_drift | 1 | promptrobust_pdr_surface_noise_math_08 | math_reasoning | surface_noise | 0.003139136698297092 | 0.00988948254185773 | 0.0 | 1.0 | -1.0 | 1.0 |
| low_corrected_drift_high_correctness_drift | 2 | promptrobust_pdr_surface_noise_math_06 | math_reasoning | surface_noise | 0.006822273898649509 | 0.01452136063797391 | 1.0 | 0.0 | 1.0 | 1.0 |
| low_corrected_drift_high_correctness_drift | 3 | promptrobust_pdr_surface_noise_humaneval_09 | code_generation | surface_noise | 0.10210039585583176 | 0.11758460084061814 | 1.0 | 0.0 | 1.0 | 1.0 |

The full inspection table lists high-drift/high-correctness-change cases, high-drift/no-change cases, low-drift/high-change cases, harmful drops, and correctness improvements.

## Task x Perturbation Means

| task | dataset | perturbation | n | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | mean_repeated_pass_rate_drop | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | HumanEval | context_injection | 10 | 0.012 | 0.133 | -0.067 | 0.100 | 0.300 |
| code_generation | HumanEval | formatting | 10 | 0.056 | 0.267 | 0.267 | 0.300 | 0.300 |
| code_generation | HumanEval | paraphrase | 10 | 0.020 | 0.167 | 0.033 | 0.100 | 0.200 |
| code_generation | HumanEval | reordering | 10 | 0.000 | 0.033 | -0.033 | 0.000 | 0.100 |
| code_generation | HumanEval | surface_noise | 10 | 0.018 | 0.100 | 0.100 | 0.100 | 0.100 |
| factual_qa | SQuAD V2 | context_injection | 10 | 0.003 | 0.100 | -0.100 | 0.000 | 0.200 |
| factual_qa | SQuAD V2 | formatting | 10 | 0.000 | 0.067 | 0.067 | 0.200 | 0.200 |
| factual_qa | SQuAD V2 | paraphrase | 10 | 0.042 | 0.067 | 0.067 | 0.200 | 0.200 |
| factual_qa | SQuAD V2 | reordering | 10 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| factual_qa | SQuAD V2 | surface_noise | 10 | 0.001 | 0.067 | 0.067 | 0.100 | 0.100 |
| math_reasoning | MATH | context_injection | 10 | 0.002 | 0.133 | 0.000 | 0.200 | 0.400 |
| math_reasoning | MATH | formatting | 10 | 0.011 | 0.233 | -0.233 | 0.000 | 0.400 |
| math_reasoning | MATH | paraphrase | 10 | 0.003 | 0.233 | 0.033 | 0.300 | 0.600 |
| math_reasoning | MATH | reordering | 10 | 0.002 | 0.233 | -0.033 | 0.200 | 0.600 |
| math_reasoning | MATH | surface_noise | 10 | 0.003 | 0.300 | -0.100 | 0.100 | 0.500 |

## Limitations

- This is a first RQ2 implementation over 150 case-level comparisons from the existing 10x3 PDR run.
- Correlations are descriptive and should not be interpreted as causal evidence.
- Correctness labels are task-specific, so pooled results should be read together with task-level results.
- Code correctness depends on the existing HumanEval execution/evaluation logic from the PDR run.

---

# RQ2 语义漂移与正确性变化

## 研究问题

RQ2 询问：对于有客观正确性标准的任务，semantic drift 是否能够预测 correctness change。

这一版实现排除了 open-ended writing，只使用 factual QA、math reasoning 和 code generation 三类任务。

## 数据来源

- Generations: `D:/pioneer_python/results/generations_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv`
- Correctness metrics: `D:/pioneer_python/results/pdr_metrics_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.csv`
- Embedding model: `text-embedding-3-small`
- Case-level comparisons: `150`

## 方法

对于每个 case，脚本使用同一次 PDR 运行中的三个 original outputs 和三个 perturbed outputs 计算 embedding。
然后计算 original sample noise、perturbed sample noise、raw cross-version drift，以及 noise-corrected drift。
主要 correctness-change 变量是 absolute repeated pass-rate change；PDR 作为辅助的归一化指标报告。

本报告还把 sample-noise correction 明确作为一个比较因素，用来把 RQ1 的 noise-corrected drift 设计和 RQ2 的 correctness-prediction 问题衔接起来。

## 总体结果

| scope_type | scope_value | n | relationship | pearson | spearman | spearman_ci95_low | spearman_ci95_high | spearman_permutation_p_two_sided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overall | all | 150 | primary | 0.328 | 0.346 | 0.188 | 0.503 | 0.001 |

主要总体关系是正向的：semantic drift 越大，通常 correctness change 也越大。

## Sample-Noise Correction 比较

这一节直接检验：sample-noise corrected similarity drift 是否比 uncorrected similarity drift 更能指示 correctness drift。
主比较中的目标变量相同，都是 absolute repeated pass-rate change。

| drift_measure | correction_status | sampling_design | correctness_target | comparison_role | pearson | spearman | spearman_ci95_low | spearman_ci95_high | spearman_permutation_p_two_sided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| noise_corrected_drift | sample_noise_corrected | repeated_3x3 | abs_repeated_pass_rate_change | primary_rq2_measure | 0.328 | 0.346 | 0.188 | 0.503 | 0.001 |
| raw_perturbation_drift | uncorrected_raw_cross_drift | repeated_3x3 | abs_repeated_pass_rate_change | same_target_uncorrected_baseline | 0.298 | 0.375 | 0.243 | 0.500 | 0.001 |
| uncorrected_single_drift | uncorrected_single_pair | single_pair | abs_repeated_pass_rate_change | single_pair_to_repeated_target_baseline | 0.267 | 0.332 | 0.188 | 0.463 | 0.001 |
| uncorrected_single_drift | uncorrected_single_pair | single_pair | abs_single_pass_rate_change | single_pair_internal_baseline | 0.298 | 0.334 | 0.200 | 0.455 | 0.001 |

在 repeated-sampling correctness target 上，sample-noise corrected measure 的 Spearman 为 0.346，而 raw uncorrected cross-drift 的 Spearman 为 0.375。

## Sample-Noise Correction 增益

| baseline_type | correctness_drift_target | corrected_pearson | baseline_pearson | pearson_delta_corrected_minus_baseline | pearson_delta_ci95_low | pearson_delta_ci95_high | corrected_spearman | baseline_spearman | spearman_delta_corrected_minus_baseline | spearman_delta_ci95_low | spearman_delta_ci95_high | spearman_delta_permutation_p_greater | corrected_better_by_pearson | corrected_better_by_spearman |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uncorrected_raw_cross_drift | abs_repeated_pass_rate_change | 0.328 | 0.298 | 0.030 | -0.073 | 0.233 | 0.346 | 0.375 | -0.029 | -0.196 | 0.138 | 0.617 | 1 | 0 |
| uncorrected_single_pair | abs_repeated_pass_rate_change | 0.328 | 0.267 | 0.061 | -0.059 | 0.294 | 0.346 | 0.332 | 0.015 | -0.168 | 0.189 | 0.462 | 1 | 1 |

相比 raw cross-drift，sample-noise correction 使 Pearson 变化 +0.030，使 Spearman 变化 -0.029。
相比 single-pair baseline，sample-noise correction 使 Pearson 变化 +0.061，使 Spearman 变化 +0.015。
在这第一版 RQ2 运行中，correction 提高了与 correctness drift 的 Pearson 关联，尤其是相对于 single-pair baseline；但它没有相对于 raw repeated cross-drift 提高 Spearman rank association。

## Correctness Degradation

RQ2 的主要目标变量衡量的是 absolute correctness drift。为了区分“correctness 是否变化”和“correctness 是否下降”，本节检查 similarity drift 是否指示 harmful correctness drop。

| relationship | x | y | n | pearson | spearman | spearman_ci95_low | spearman_ci95_high | spearman_permutation_p_two_sided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| harmful_drop_binary | noise_corrected_drift | harmful_correctness_drop | 150 | 0.247 | 0.306 | 0.145 | 0.463 | 0.001 |
| raw_harmful_drop_binary | raw_perturbation_drift | harmful_correctness_drop | 150 | 0.200 | 0.213 | 0.074 | 0.340 | 0.009 |

这一节区分了两个问题：“correctness 有没有变化？”以及“correctness 有没有变差？”。

## 按任务分组

| scope_value | n | relationship | pearson | spearman | spearman_ci95_low | spearman_ci95_high |
| --- | --- | --- | --- | --- | --- | --- |
| code_generation | 50 | primary | 0.747 | 0.515 | 0.180 | 0.732 |
| factual_qa | 50 | primary | 0.006 | 0.224 | -0.162 | 0.535 |
| math_reasoning | 50 | primary | -0.060 | 0.232 | -0.044 | 0.507 |

## 按 Perturbation 分组

| scope_value | n | relationship | pearson | spearman | spearman_ci95_low | spearman_ci95_high |
| --- | --- | --- | --- | --- | --- | --- |
| context_injection | 30 | primary | 0.656 | 0.467 | 0.055 | 0.776 |
| formatting | 30 | primary | 0.577 | 0.221 | -0.213 | 0.605 |
| paraphrase | 30 | primary | 0.119 | 0.112 | -0.233 | 0.471 |
| reordering | 30 | primary | 0.613 | 0.271 | -0.195 | 0.655 |
| surface_noise | 30 | primary | 0.436 | 0.608 | 0.245 | 0.876 |

## Case Inspection 预览

| inspection_category | rank | case_id | task | perturbation | noise_corrected_drift | raw_perturbation_drift | clean_mean_correctness | perturbed_mean_correctness | repeated_pass_rate_drop | abs_repeated_pass_rate_change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| high_corrected_drift_high_correctness_drift | 1 | promptrobust_pdr_formatting_humaneval_03 | code_generation | formatting | 0.3492243914049976 | 0.3492243914049977 | 1.0 | 0.0 | 1.0 | 1.0 |
| high_corrected_drift_high_correctness_drift | 2 | promptrobust_pdr_paraphrase_humaneval_04 | code_generation | paraphrase | 0.16976289069259254 | 0.16976289069259265 | 1.0 | 0.0 | 1.0 | 1.0 |
| high_corrected_drift_high_correctness_drift | 3 | promptrobust_pdr_formatting_humaneval_09 | code_generation | formatting | 0.12303028863511735 | 0.12326928112127196 | 1.0 | 0.0 | 1.0 | 1.0 |
| high_corrected_drift_no_correctness_drift | 1 | promptrobust_pdr_paraphrase_squad_08 | factual_qa | paraphrase | 0.41575019866255514 | 0.41575019866255525 | 0.0 | 0.0 | 0.0 | 0.0 |
| high_corrected_drift_no_correctness_drift | 2 | promptrobust_pdr_formatting_math_03 | math_reasoning | formatting | 0.10500771683898985 | 0.16746868786033084 | 0.0 | 0.0 | 0.0 | 0.0 |
| high_corrected_drift_no_correctness_drift | 3 | promptrobust_pdr_surface_noise_humaneval_01 | code_generation | surface_noise | 0.06829442710378233 | 0.07501916417337598 | 0.0 | 0.0 | 0.0 | 0.0 |
| low_corrected_drift_high_correctness_drift | 1 | promptrobust_pdr_surface_noise_math_08 | math_reasoning | surface_noise | 0.003139136698297092 | 0.00988948254185773 | 0.0 | 1.0 | -1.0 | 1.0 |
| low_corrected_drift_high_correctness_drift | 2 | promptrobust_pdr_surface_noise_math_06 | math_reasoning | surface_noise | 0.006822273898649509 | 0.01452136063797391 | 1.0 | 0.0 | 1.0 | 1.0 |
| low_corrected_drift_high_correctness_drift | 3 | promptrobust_pdr_surface_noise_humaneval_09 | code_generation | surface_noise | 0.10210039585583176 | 0.11758460084061814 | 1.0 | 0.0 | 1.0 | 1.0 |

完整 inspection 表列出了 high-drift/high-correctness-change cases、high-drift/no-change cases、low-drift/high-change cases、harmful drops，以及 correctness improvements。

## Task x Perturbation 均值

| task | dataset | perturbation | n | mean_noise_corrected_drift | mean_abs_repeated_pass_rate_change | mean_repeated_pass_rate_drop | share_harmful_correctness_drop | share_correctness_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code_generation | HumanEval | context_injection | 10 | 0.012 | 0.133 | -0.067 | 0.100 | 0.300 |
| code_generation | HumanEval | formatting | 10 | 0.056 | 0.267 | 0.267 | 0.300 | 0.300 |
| code_generation | HumanEval | paraphrase | 10 | 0.020 | 0.167 | 0.033 | 0.100 | 0.200 |
| code_generation | HumanEval | reordering | 10 | 0.000 | 0.033 | -0.033 | 0.000 | 0.100 |
| code_generation | HumanEval | surface_noise | 10 | 0.018 | 0.100 | 0.100 | 0.100 | 0.100 |
| factual_qa | SQuAD V2 | context_injection | 10 | 0.003 | 0.100 | -0.100 | 0.000 | 0.200 |
| factual_qa | SQuAD V2 | formatting | 10 | 0.000 | 0.067 | 0.067 | 0.200 | 0.200 |
| factual_qa | SQuAD V2 | paraphrase | 10 | 0.042 | 0.067 | 0.067 | 0.200 | 0.200 |
| factual_qa | SQuAD V2 | reordering | 10 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| factual_qa | SQuAD V2 | surface_noise | 10 | 0.001 | 0.067 | 0.067 | 0.100 | 0.100 |
| math_reasoning | MATH | context_injection | 10 | 0.002 | 0.133 | 0.000 | 0.200 | 0.400 |
| math_reasoning | MATH | formatting | 10 | 0.011 | 0.233 | -0.233 | 0.000 | 0.400 |
| math_reasoning | MATH | paraphrase | 10 | 0.003 | 0.233 | 0.033 | 0.300 | 0.600 |
| math_reasoning | MATH | reordering | 10 | 0.002 | 0.233 | -0.033 | 0.200 | 0.600 |
| math_reasoning | MATH | surface_noise | 10 | 0.003 | 0.300 | -0.100 | 0.100 | 0.500 |

## 局限性

- 这是基于现有 10x3 PDR run 的第一版 RQ2 实现，共 150 个 case-level comparisons。
- 相关性结果是描述性的，不应解释为因果证据。
- Correctness labels 是 task-specific 的，因此 pooled results 需要和 task-level results 一起解读。
- Code correctness 依赖现有 PDR run 中的 HumanEval execution/evaluation logic。
