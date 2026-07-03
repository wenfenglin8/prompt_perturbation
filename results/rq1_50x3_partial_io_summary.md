# RQ1 50x3 Partial Run Input/Output Summary

Status:

```text
Paused after batch 3/10.
Completed data are partial results, not the final 50x3 run.
```

## What Was Run

Script:

```text
four_task_similarity_sweep.py
```

Purpose:

```text
Estimate sample noise and noise-corrected semantic drift using repeated generations
and embedding-based similarity distances.
```

This run measures semantic similarity / semantic drift, not correctness or PDR.

## Input Configuration

Generation model:

```text
gpt-4o-mini
```

Embedding model:

```text
text-embedding-3-small
```

Sampling parameters:

```text
temperature = 0.7
top_p = 0.9
samples per prompt version = 3
```

Dataset scale requested:

```text
50 cases per task
4 tasks
5 perturbations
2 prompt versions per case: original and perturbed
3 generations per prompt version
10 batches
```

Full planned scale:

```text
4 tasks x 50 cases/task x 5 perturbations x 2 prompt versions x 3 samples
= 6000 generation rows
= 1000 metric rows
```

Completed scale so far:

```text
3 batches completed
1800 generation rows
300 metric rows
```

Tasks and datasets:

| Task | Dataset |
|---|---|
| factual_qa | SQuAD V2 |
| math_reasoning | MATH |
| code_generation | HumanEval |
| open_ended_writing | Alpaca |

Perturbations planned:

```text
paraphrase
reordering
formatting
context_injection
surface_noise
```

Perturbations completed so far:

```text
batch 1/10: paraphrase slice
batch 2/10: reordering slice
batch 3/10: formatting slice
```

## Commands Used

Batch 1:

```powershell
python four_task_similarity_sweep.py --model gpt-4o-mini --dataset-cases-per-task 50 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag four_task_similarity_sweep_50x3_batch1of10 --sleep 0 --batch-count 10 --batch-index 1 --resume
```

Batch 2:

```powershell
python four_task_similarity_sweep.py --model gpt-4o-mini --dataset-cases-per-task 50 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag four_task_similarity_sweep_50x3_batch2of10 --sleep 0 --batch-count 10 --batch-index 2 --resume
```

Batch 3:

```powershell
python four_task_similarity_sweep.py --model gpt-4o-mini --dataset-cases-per-task 50 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag four_task_similarity_sweep_50x3_batch3of10 --sleep 0 --batch-count 10 --batch-index 3 --resume
```

Next command to continue:

```powershell
python four_task_similarity_sweep.py --model gpt-4o-mini --dataset-cases-per-task 50 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag four_task_similarity_sweep_50x3_batch4of10 --sleep 0 --batch-count 10 --batch-index 4 --resume
```

## Input Prompt Versions

For each task case and perturbation, the script sends two prompt versions:

```text
original: clean task instruction + task-specific body
perturbed: perturbed instruction + same task-specific body
```

Each prompt version is sampled three times.

Example structure:

```text
original prompt:
<clean instruction>

<dataset item body>

perturbed prompt:
<perturbed instruction>

<same dataset item body>
```

The dataset item body is held fixed between original and perturbed prompts.
Only the instruction text is perturbed.

## Output Files

Batch 1 outputs:

```text
results/generations_four_task_similarity_sweep_50x3_batch1of10.csv
results/similarity_metrics_four_task_similarity_sweep_50x3_batch1of10.csv
results/similarity_grouped_four_task_similarity_sweep_50x3_batch1of10.csv
results/similarity_rankings_four_task_similarity_sweep_50x3_batch1of10.csv
results/similarity_report_four_task_similarity_sweep_50x3_batch1of10.md
```

Batch 2 outputs:

```text
results/generations_four_task_similarity_sweep_50x3_batch2of10.csv
results/similarity_metrics_four_task_similarity_sweep_50x3_batch2of10.csv
results/similarity_grouped_four_task_similarity_sweep_50x3_batch2of10.csv
results/similarity_rankings_four_task_similarity_sweep_50x3_batch2of10.csv
results/similarity_report_four_task_similarity_sweep_50x3_batch2of10.md
```

Batch 3 outputs:

```text
results/generations_four_task_similarity_sweep_50x3_batch3of10.csv
results/similarity_metrics_four_task_similarity_sweep_50x3_batch3of10.csv
results/similarity_grouped_four_task_similarity_sweep_50x3_batch3of10.csv
results/similarity_rankings_four_task_similarity_sweep_50x3_batch3of10.csv
results/similarity_report_four_task_similarity_sweep_50x3_batch3of10.md
```

## Output File Meanings

`generations_*.csv` contains one row per generated output.

Important columns:

| Column | Meaning |
|---|---|
| case_id | Unique task/perturbation/dataset case ID |
| task | Task family |
| dataset | Dataset source |
| perturbation | Perturbation type |
| version | `original` or `perturbed` |
| sample_index | Repeated sample number |
| prompt | Prompt sent to the model |
| output | Model-generated response |

`similarity_metrics_*.csv` contains one row per task case and perturbation.

Important columns:

| Column | Meaning |
|---|---|
| uncorrected_single_drift | Distance between one original output and one perturbed output |
| original_noise | Average pairwise distance among the three original-prompt outputs |
| perturbed_noise | Average pairwise distance among the three perturbed-prompt outputs |
| noise_baseline | Average of `original_noise` and `perturbed_noise` |
| raw_perturbation_drift | Average cross-distance between original and perturbed outputs |
| noise_corrected_drift | `max(0, raw_perturbation_drift - noise_baseline)` |

`similarity_grouped_*.csv` aggregates metrics by task and perturbation within a batch.

`similarity_rankings_*.csv` ranks perturbations by noise-corrected drift within each task for that batch.

`similarity_report_*.md` is the human-readable batch report.

## Current Interim Statistics

The following statistics use only the first 300 metric rows.

Overall:

| Metric | Mean | Std | Variance |
|---|---:|---:|---:|
| noise_baseline | 0.047706 | 0.058397 | 0.003410 |
| raw_perturbation_drift | 0.072255 | 0.100395 | 0.010079 |
| noise_corrected_drift | 0.028305 | 0.087777 | 0.007705 |
| uncorrected_single_drift | 0.073690 | 0.122281 | 0.014953 |

Sample-noise baseline by task:

| Task | n | Mean | Std | Variance |
|---|---:|---:|---:|---:|
| factual_qa | 75 | 0.036157 | 0.086040 | 0.007403 |
| math_reasoning | 75 | 0.051542 | 0.029902 | 0.000894 |
| code_generation | 75 | 0.040254 | 0.055961 | 0.003132 |
| open_ended_writing | 75 | 0.062872 | 0.043716 | 0.001911 |

Sample-noise baseline by completed perturbation:

| Perturbation | n | Mean | Std | Variance |
|---|---:|---:|---:|---:|
| paraphrase | 100 | 0.046380 | 0.064468 | 0.004156 |
| reordering | 100 | 0.051773 | 0.058828 | 0.003461 |
| formatting | 100 | 0.044966 | 0.051543 | 0.002657 |

## Current Interpretation

The partial run shows that sample noise is non-negligible:

```text
mean raw perturbation drift = 0.072255
mean noise baseline = 0.047706
mean noise-corrected drift = 0.028305
```

This means a substantial part of observed raw semantic drift is explained by repeated-generation variability.

Because only 3/10 batches are complete, task-level and perturbation-level comparisons should be treated as interim trends.
The final RQ1 conclusion should be based on the merged 10-batch result.

---

# RQ1 50x3 阶段性运行输入/输出说明

状态：

```text
已在第 3/10 批之后暂停。
当前数据是阶段性结果，不是最终 50x3 完整运行结果。
```

## 实际运行内容

脚本：

```text
four_task_similarity_sweep.py
```

目的：

```text
通过 repeated generations 和 embedding-based similarity distance，
估计 sample noise 和 noise-corrected semantic drift。
```

这次运行测量的是语义相似度 / 语义漂移，不是 correctness，也不是 PDR。

## 输入配置

生成模型：

```text
gpt-4o-mini
```

Embedding 模型：

```text
text-embedding-3-small
```

采样参数：

```text
temperature = 0.7
top_p = 0.9
每个 prompt version 采样 3 次
```

请求的数据规模：

```text
每个 task 50 个 cases
4 个 tasks
5 类 perturbations
每个 case 有 2 个 prompt versions：original 和 perturbed
每个 prompt version 生成 3 次
总共分 10 批运行
```

完整计划规模：

```text
4 tasks x 50 cases/task x 5 perturbations x 2 prompt versions x 3 samples
= 6000 条 generation rows
= 1000 条 metric rows
```

目前已完成规模：

```text
已完成 3 批
1800 条 generation rows
300 条 metric rows
```

Tasks 和 datasets：

| Task | Dataset |
|---|---|
| factual_qa | SQuAD V2 |
| math_reasoning | MATH |
| code_generation | HumanEval |
| open_ended_writing | Alpaca |

计划运行的 perturbations：

```text
paraphrase
reordering
formatting
context_injection
surface_noise
```

目前已完成的 perturbation 部分：

```text
batch 1/10: paraphrase slice
batch 2/10: reordering slice
batch 3/10: formatting slice
```

## 已使用命令

第 1 批：

```powershell
python four_task_similarity_sweep.py --model gpt-4o-mini --dataset-cases-per-task 50 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag four_task_similarity_sweep_50x3_batch1of10 --sleep 0 --batch-count 10 --batch-index 1 --resume
```

第 2 批：

```powershell
python four_task_similarity_sweep.py --model gpt-4o-mini --dataset-cases-per-task 50 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag four_task_similarity_sweep_50x3_batch2of10 --sleep 0 --batch-count 10 --batch-index 2 --resume
```

第 3 批：

```powershell
python four_task_similarity_sweep.py --model gpt-4o-mini --dataset-cases-per-task 50 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag four_task_similarity_sweep_50x3_batch3of10 --sleep 0 --batch-count 10 --batch-index 3 --resume
```

下次继续运行的命令：

```powershell
python four_task_similarity_sweep.py --model gpt-4o-mini --dataset-cases-per-task 50 --samples 3 --temperature 0.7 --top-p 0.9 --output-tag four_task_similarity_sweep_50x3_batch4of10 --sleep 0 --batch-count 10 --batch-index 4 --resume
```

## 输入 Prompt Versions

对于每个 task case 和 perturbation，脚本会发送两个 prompt versions：

```text
original: 干净的 task instruction + task-specific body
perturbed: 被扰动后的 instruction + 同一个 task-specific body
```

每个 prompt version 会采样 3 次。

示例结构：

```text
original prompt:
<clean instruction>

<dataset item body>

perturbed prompt:
<perturbed instruction>

<same dataset item body>
```

original 和 perturbed 之间，dataset item body 保持不变。
只有 instruction text 被扰动。

## 输出文件

第 1 批输出：

```text
results/generations_four_task_similarity_sweep_50x3_batch1of10.csv
results/similarity_metrics_four_task_similarity_sweep_50x3_batch1of10.csv
results/similarity_grouped_four_task_similarity_sweep_50x3_batch1of10.csv
results/similarity_rankings_four_task_similarity_sweep_50x3_batch1of10.csv
results/similarity_report_four_task_similarity_sweep_50x3_batch1of10.md
```

第 2 批输出：

```text
results/generations_four_task_similarity_sweep_50x3_batch2of10.csv
results/similarity_metrics_four_task_similarity_sweep_50x3_batch2of10.csv
results/similarity_grouped_four_task_similarity_sweep_50x3_batch2of10.csv
results/similarity_rankings_four_task_similarity_sweep_50x3_batch2of10.csv
results/similarity_report_four_task_similarity_sweep_50x3_batch2of10.md
```

第 3 批输出：

```text
results/generations_four_task_similarity_sweep_50x3_batch3of10.csv
results/similarity_metrics_four_task_similarity_sweep_50x3_batch3of10.csv
results/similarity_grouped_four_task_similarity_sweep_50x3_batch3of10.csv
results/similarity_rankings_four_task_similarity_sweep_50x3_batch3of10.csv
results/similarity_report_four_task_similarity_sweep_50x3_batch3of10.md
```

## 输出文件含义

`generations_*.csv` 每一行是一条模型生成结果。

关键列：

| Column | Meaning |
|---|---|
| case_id | 唯一的 task / perturbation / dataset case ID |
| task | 任务类型 |
| dataset | 数据集来源 |
| perturbation | 扰动类型 |
| version | `original` 或 `perturbed` |
| sample_index | repeated sample 编号 |
| prompt | 发送给模型的 prompt |
| output | 模型生成的回答 |

`similarity_metrics_*.csv` 每一行对应一个 task case 和一个 perturbation。

关键列：

| Column | Meaning |
|---|---|
| uncorrected_single_drift | 一个 original output 和一个 perturbed output 之间的距离 |
| original_noise | 三个 original-prompt outputs 之间的平均 pairwise distance |
| perturbed_noise | 三个 perturbed-prompt outputs 之间的平均 pairwise distance |
| noise_baseline | `original_noise` 和 `perturbed_noise` 的平均值 |
| raw_perturbation_drift | original outputs 和 perturbed outputs 之间的平均 cross-distance |
| noise_corrected_drift | `max(0, raw_perturbation_drift - noise_baseline)` |

`similarity_grouped_*.csv` 会在每个 batch 内，按 task 和 perturbation 聚合指标。

`similarity_rankings_*.csv` 会在每个 batch 内，按每个 task 的 noise-corrected drift 对 perturbations 排名。

`similarity_report_*.md` 是每个 batch 的可读报告。

## 当前阶段性统计

以下统计只使用前 300 条 metric rows。

整体结果：

| Metric | Mean | Std | Variance |
|---|---:|---:|---:|
| noise_baseline | 0.047706 | 0.058397 | 0.003410 |
| raw_perturbation_drift | 0.072255 | 0.100395 | 0.010079 |
| noise_corrected_drift | 0.028305 | 0.087777 | 0.007705 |
| uncorrected_single_drift | 0.073690 | 0.122281 | 0.014953 |

按 task 统计 sample-noise baseline：

| Task | n | Mean | Std | Variance |
|---|---:|---:|---:|---:|
| factual_qa | 75 | 0.036157 | 0.086040 | 0.007403 |
| math_reasoning | 75 | 0.051542 | 0.029902 | 0.000894 |
| code_generation | 75 | 0.040254 | 0.055961 | 0.003132 |
| open_ended_writing | 75 | 0.062872 | 0.043716 | 0.001911 |

按已完成 perturbation 统计 sample-noise baseline：

| Perturbation | n | Mean | Std | Variance |
|---|---:|---:|---:|---:|
| paraphrase | 100 | 0.046380 | 0.064468 | 0.004156 |
| reordering | 100 | 0.051773 | 0.058828 | 0.003461 |
| formatting | 100 | 0.044966 | 0.051543 | 0.002657 |

## 当前解释

阶段性结果显示 sample noise 不是可以忽略的小误差：

```text
mean raw perturbation drift = 0.072255
mean noise baseline = 0.047706
mean noise-corrected drift = 0.028305
```

这说明 observed raw semantic drift 中有相当一部分可以由 repeated-generation variability 解释。

因为目前只完成了 3/10 批，所以 task-level 和 perturbation-level 的比较只能视为阶段性趋势。
最终 RQ1 结论应该基于 10 个 batch 合并后的完整结果。
