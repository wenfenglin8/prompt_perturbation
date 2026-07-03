# RQ1 Experiment Completion Status

## 2026-07-01 Latest RQ1 Completion Update

### Current Completion Judgment

Current RQ1 status:

```text
RQ1 is complete at pilot-expanded / proposal-evidence scale.
RQ1 is not yet complete at benchmark-scale.
```

The main RQ1 evidence has now been updated from the older
`character / word / sentence / semantic` perturbation taxonomy to the
PDR-aligned five-perturbation taxonomy:

```text
paraphrase
reordering
formatting
context_injection
surface_noise
```

The latest main RQ1 similarity experiment is:

```text
4 tasks x 5 cases/task x 5 perturbations x 2 prompt versions x 3 samples
= 600 generation rows
= 100 task-perturbation-case metric rows
```

Main result file:

```text
results/similarity_report_four_task_similarity_sweep_pdr_aligned_5x3.md
```

Supporting files:

```text
results/generations_four_task_similarity_sweep_pdr_aligned_5x3.csv
results/similarity_metrics_four_task_similarity_sweep_pdr_aligned_5x3.csv
results/similarity_grouped_four_task_similarity_sweep_pdr_aligned_5x3.csv
results/similarity_rankings_four_task_similarity_sweep_pdr_aligned_5x3.csv
results/similarity_summary_four_task_similarity_sweep_pdr_aligned_5x3.json
```

The run was executed in five saved batches:

```text
batch 1/5: paraphrase
batch 2/5: reordering
batch 3/5: formatting
batch 4/5: context_injection
batch 5/5: surface_noise
```

### Reference Alignment Status

The latest four-task similarity sweep is aligned with the same perturbation
implementation used by the three-task PDR report:

```text
results/pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md
```

Both experiments use the same shared implementation:

```text
reference_perturbations.py
```

Important boundary:

```text
The perturbation categories are reference-informed / literature-aligned,
but the concrete perturbation generation algorithms are project-specific implementations.
They are not an exact reproduction of PromptRobust's official adversarial pipeline.
```

Dataset reference alignment:

| Task | Dataset | Reference alignment |
|---|---|---|
| factual_qa | SQuAD V2 | PromptRobust / PromptBench |
| math_reasoning | MATH | PromptRobust / PromptBench |
| code_generation | HumanEval | External supplement, because the reviewed prompt-perturbation papers do not provide a dedicated code-generation benchmark |
| open_ended_writing | Alpaca | POSIX |

Perturbation reference alignment:

| Perturbation | Status |
|---|---|
| paraphrase | Reference-informed; aligned with PromptRobust / PromptBench prompt rephrasing and POSIX intent-aligned prompt variants |
| reordering | Reference-informed; aligned with information-order / instruction-order perturbation ideas |
| formatting | Reference-informed; closest to POSIX-style template / formatting variation |
| context_injection | Reference-informed; aligned with irrelevant-context / sentence-level perturbation ideas |
| surface_noise | Reference-informed; aligned with typo / character-level noise perturbations |

### Latest RQ1 Similarity Result

Corrected sensitivity ranking from the PDR-aligned 5x3 four-task sweep:

| Task | Corrected sensitivity ranking |
|---|---|
| factual_qa | paraphrase > reordering > context_injection > formatting > surface_noise |
| math_reasoning | paraphrase > reordering > context_injection > formatting > surface_noise |
| code_generation | reordering > formatting > paraphrase > surface_noise > context_injection |
| open_ended_writing | surface_noise > formatting > context_injection > paraphrase > reordering |

Core RQ1 interpretation:

```text
Corrected perturbation sensitivity ranking is task-dependent.
The strongest perturbation differs across tasks after sample-noise correction.
```

This directly supports the RQ1 claim at pilot-expanded scale.

### Raw vs Noise-Corrected Similarity Difference

Across all task-perturbation groups in the latest PDR-aligned similarity sweep:

```text
Average raw similarity drift:       0.0567
Average noise-corrected drift:      0.0199
Average reduction after correction: 0.0368
Share removed by sample noise:      64.9%
```

By task:

| Task | Average raw drift | Average corrected drift | Share removed by sample noise |
|---|---:|---:|---:|
| factual_qa | 0.0108 | 0.0068 | 37.3% |
| math_reasoning | 0.0524 | 0.0038 | 92.8% |
| code_generation | 0.0481 | 0.0320 | 33.4% |
| open_ended_writing | 0.1157 | 0.0370 | 68.0% |

Interpretation:

```text
Uncorrected similarity drift substantially overestimates perturbation-induced output change.
After subtracting the within-prompt sample-noise baseline, the average drift decreases
from 0.0567 to 0.0199, indicating that about 64.9% of the apparent perturbation effect
can be attributed to ordinary repeated-generation variability.
```

### Auxiliary PDR Evidence

The auxiliary objective-task PDR validation is also complete at 10 cases/task
for three objective tasks:

```text
factual_qa
math_reasoning
code_generation
```

Main PDR report:

```text
results/pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md
```

Core PDR result:

```text
Average clean single-sample correctness:     0.4867
Average perturbed single-sample correctness: 0.4533
Dataset-level uncorrected single-sample PDR: 0.0685

Average clean repeated correctness:          0.4778
Average perturbed repeated correctness:      0.4733
Dataset-level repeated-sampling PDR:         0.0093
```

Interpretation:

```text
Single-sample PDR estimates a 6.85% relative performance drop.
Repeated-sampling PDR estimates only a 0.93% relative performance drop.
The single-sample estimate overstates the PDR by 5.92 percentage points.
```

This supports the broader RQ1 methodology: apparent perturbation effects can be
inflated when repeated-generation sample noise is not considered.

### What Is Now Completed

Completed / available:

| Component | Current status | Main evidence |
|---|---|---|
| sample-noise correction pipeline | Completed | `four_task_similarity_sweep.py`; `sample_noise_pilot.py` |
| PDR-aligned perturbation taxonomy | Completed | `reference_perturbations.py` |
| four-task multi-perturbation similarity sweep | Completed at 5 cases/task, 3 samples/prompt | `results/similarity_report_four_task_similarity_sweep_pdr_aligned_5x3.md` |
| raw drift vs noise-corrected drift comparison | Completed | `results/similarity_report_four_task_similarity_sweep_pdr_aligned_5x3.md` |
| corrected sensitivity ranking across four tasks | Completed | `results/similarity_rankings_four_task_similarity_sweep_pdr_aligned_5x3.csv` |
| objective-task PDR auxiliary validation | Completed at 10 cases/task for factual QA, math, and code | `results/pdr_report_three_task_pdr_humaneval_fixed_10x3_all_perturbations_combined.md` |
| reference-alignment limitation note | Completed | `official_code_alignment_limitations.md` |

### What Still Remains

Still incomplete / optional before making a strong benchmark-level claim:

| Missing / optional item | Status | Why it matters | Requires new model calls? |
|---|---|---|---:|
| Larger four-task similarity sweep | Not complete | Current main four-task sweep is 5 cases/task; stronger ranking-stability claims need 10-25 cases/task | Yes |
| Bootstrap ranking stability | Not complete | Can test whether current rankings are driven by a few cases | No |
| Reference-faithful official-code subset | Optional | Would make a narrower SQuAD V2 + MATH comparison closer to PromptRobust / PromptBench official settings | Likely yes |
| Multi-temperature check | Optional | Tests whether sample-noise correction changes under different decoding randomness | Yes |
| Multi-model check | Optional | Needed only for cross-model generality claims | Yes |
| Open-ended writing auxiliary quality metrics | Optional | Current writing evidence uses embedding drift, not diversity/coherence/fluency metrics | Maybe |

### Updated Bottom Line

Current best RQ1 status statement:

```text
The RQ1 methodology and main pilot-expanded evidence are complete. The latest
four-task similarity sweep uses a PDR-aligned five-perturbation taxonomy across
SQuAD V2, MATH, HumanEval, and Alpaca, with 5 cases per task and 3 repeated
samples per prompt version. Results show that sample-noise correction reduces
average drift from 0.0567 to 0.0199 and changes the interpretation of
perturbation sensitivity. Corrected sensitivity rankings are task-dependent:
paraphrase is strongest for factual QA and math reasoning, reordering is
strongest for code generation, and surface_noise is strongest for open-ended
writing. However, the evidence remains pilot-expanded rather than benchmark-scale
because each task currently uses 5 cases. A larger sample or bootstrap stability
analysis is needed before making a strong benchmark-level claim about stable
sensitivity rankings.
```

本文整理当前 RQ1 的实验完成度，方便 review。

## RQ1 原始问题

当前 proposal / research notes 中的 RQ1 是：

```text
After correcting for sample noise, do different perturbation types produce a stable sensitivity ranking across factual QA, math reasoning, code generation, and open-ended writing?
```

这个问题包含三个关键要求：

1. **Different perturbation types**
   需要比较多种 prompt perturbation。

2. **Across four task types**
   需要覆盖 factual QA、math reasoning、code generation、open-ended writing。

3. **After correcting for sample noise**
   需要比较 uncorrected estimate 和 sample-noise-corrected / repeated-sampling estimate。

## 当前结论

目前不能说 RQ1 已经 benchmark-scale 完整完成。

更准确的状态是：

```text
RQ1 的方法链路已经打通；
4 tasks × 4 perturbation types 的 pilot matrix 已经完成；
但 benchmark-scale RQ1 还没有完成，因为每个 task 当前只有少量样本。
```

## 已完成的数据和实验

### 1. Cross-task paraphrase validation

文件：

- `cross_task_paraphrase_noise_correction.md`
- `results/sample_noise_report_cross_task_paraphrase.md`
- `results/noise_metrics_cross_task_paraphrase.json`
- `results/generations_cross_task_paraphrase.csv`

覆盖：

| 维度 | 覆盖情况 |
|---|---|
| Tasks | factual QA, math reasoning, code generation, open-ended writing |
| Datasets | SQuAD V2, MATH, HumanEval, Alpaca |
| Perturbation | paraphrasing / instruction rewording |
| Evaluation | similarity / semantic drift |
| Correction | raw drift vs noise-corrected drift |

核心结果：

| Task | Dataset | Raw drift | Corrected drift |
|---|---|---:|---:|
| Factual QA | SQuAD V2 | 0.3079 | 0.2092 |
| Math reasoning | MATH | 0.0480 | 0.0014 |
| Code generation | HumanEval | 0.1254 | 0.1111 |
| Open-ended writing | Alpaca | 0.0321 | 0.0083 |

说明：

```text
这是一个 perturbation across four tasks 的实验。
它支持 RQ1 的 cross-task 部分，但只覆盖了 paraphrasing 这一种扰动。
```

### 2. PromptRobust-style perturbation sweep on SQuAD V2 and MATH

文件：

- `promptrobust_perturbation_sweep_result.md`
- `results/pdr_report_promptrobust_perturbation_sweep_2x3.md`
- `results/pdr_metrics_promptrobust_perturbation_sweep_2x3.csv`
- `results/generations_promptrobust_perturbation_sweep_2x3.csv`
- `results/similarity_grouped_promptrobust_perturbation_sweep_2x3.csv`

覆盖：

| 维度 | 覆盖情况 |
|---|---|
| Tasks | factual QA, math reasoning |
| Datasets | SQuAD V2, MATH |
| Perturbations | character, word, sentence, semantic |
| Evaluation | PDR correctness + similarity drift |
| Correction | single-sample vs repeated-sampling PDR; raw vs corrected similarity drift |

PDR 横向结果：

| Perturbation | Task | Uncorrected PDR | Repeated-sampling PDR |
|---|---|---:|---:|
| Character | Factual QA | -1.0000 | -0.2500 |
| Character | Math | 0.0000 | 0.0000 |
| Word-level | Factual QA | 0.0000 | 0.0000 |
| Word-level | Math | 0.0000 | -4.0000 |
| Sentence-level | Factual QA | 0.0000 | 0.0000 |
| Sentence-level | Math | 0.0000 | -0.5000 |
| Semantic-level | Factual QA | 0.0000 | 0.0000 |
| Semantic-level | Math | -1.0000 | -1.0000 |

Similarity 横向结果：

| Perturbation | Task | Raw drift | Corrected drift |
|---|---|---:|---:|
| Character | Factual QA | 0.0286 | 0.0000 |
| Character | Math | 0.0210 | 0.0029 |
| Word-level | Factual QA | 0.0000 | 0.0000 |
| Word-level | Math | 0.0422 | 0.0052 |
| Sentence-level | Factual QA | 0.0000 | 0.0000 |
| Sentence-level | Math | 0.0277 | 0.0005 |
| Semantic-level | Factual QA | 0.1653 | 0.1628 |
| Semantic-level | Math | 0.0535 | 0.0199 |

说明：

```text
这是 multiple perturbation types 的横向实验。
它支持 RQ1 的 perturbation-ranking 部分，但目前只覆盖 factual QA 和 math reasoning。
```

### 3. Factual QA and Math PDR correctness check for paraphrase

文件：

- `cross_task_paraphrase_noise_correction.md`
- `results/pdr_report_cross_task_paraphrase_pdr_5x3.md`
- `results/pdr_metrics_cross_task_paraphrase_pdr_5x3.csv`
- `results/generations_cross_task_paraphrase_pdr_5x3.csv`

覆盖：

| 维度 | 覆盖情况 |
|---|---|
| Tasks | factual QA, math reasoning |
| Datasets | SQuAD V2, MATH |
| Perturbation | paraphrase |
| Evaluation | PDR correctness |
| Correction | single-sample PDR vs repeated-sampling PDR |

5x3 结果：

| Task | N | Uncorrected PDR | Repeated-sampling PDR |
|---|---:|---:|---:|
| Factual QA | 5 | 0.3333 | 0.3333 |
| Math reasoning | 5 | -1.0000 | -0.8333 |

说明：

```text
Factual QA 中 paraphrase 降低 correctness。
Math reasoning 中 paraphrase 提升 correctness。
这说明 perturbation effect 是 task-dependent 的。
```

### 4. MATH-only larger paraphrase PDR check

文件：

- `math_paraphrase_pdr_25x3_analysis.md`
- `results/pdr_report_math_paraphrase_pdr_25x3.md`
- `results/pdr_metrics_math_paraphrase_pdr_25x3.csv`
- `results/generations_math_paraphrase_pdr_25x3.csv`

覆盖：

| 维度 | 覆盖情况 |
|---|---|
| Task | math reasoning |
| Dataset | MATH |
| Perturbation | paraphrase |
| Evaluation | PDR correctness |
| Correction | single-sample PDR vs repeated-sampling PDR |
| Scale | 25 MATH cases, 3 samples per prompt version |

结果：

| Estimate | Clean performance | Perturbed performance | PDR |
|---|---:|---:|---:|
| Uncorrected single-sample | 0.4000 | 0.6000 | -0.5000 |
| Repeated-sampling | 0.3600 | 0.5867 | -0.6296 |

说明：

```text
扩大到 25 条 MATH 后，paraphrase 仍然提升 final-answer correctness。
这说明 paraphrase 对 MATH 不是 harmful noise，而可能是 reasoning-friendly instruction.
```

### 5. Four-task similarity sweep

文件：

- `rq1_four_task_similarity_sweep_result.md`
- `results/similarity_report_four_task_similarity_sweep_2x3.md`
- `results/similarity_grouped_four_task_similarity_sweep_2x3.csv`
- `results/similarity_rankings_four_task_similarity_sweep_2x3.csv`
- `results/generations_four_task_similarity_sweep_2x3.csv`

覆盖：

| 维度 | 覆盖情况 |
|---|---|
| Tasks | factual QA, math reasoning, code generation, open-ended writing |
| Datasets | SQuAD V2, MATH, HumanEval, Alpaca |
| Perturbations | character, word, sentence, semantic |
| Evaluation | embedding-based similarity / semantic drift |
| Correction | raw drift vs noise-corrected drift |
| Scale | 2 cases per task, 3 samples per prompt version |

Corrected sensitivity ranking:

| Task | Rank 1 | Rank 2 | Rank 3 | Rank 4 |
|---|---|---|---|---|
| Factual QA | semantic | word | character | sentence |
| Math reasoning | word | semantic | character | sentence |
| Code generation | semantic | word | sentence | character |
| Open-ended writing | sentence | semantic | word | character |

说明：

```text
这是目前最直接回答 RQ1 的 pilot matrix。
结果显示 corrected perturbation sensitivity ranking 不同任务之间并不稳定。
```

### 6. Expanded four-task similarity sweep, 5 cases per task

文件：

- `rq1_four_task_similarity_sweep_5x3_result.md`
- `results/similarity_report_four_task_similarity_sweep_5x3.md`
- `results/similarity_grouped_four_task_similarity_sweep_5x3.csv`
- `results/similarity_rankings_four_task_similarity_sweep_5x3.csv`
- `results/generations_four_task_similarity_sweep_5x3.csv`

覆盖：

| 维度 | 覆盖情况 |
|---|---|
| Tasks | factual QA, math reasoning, code generation, open-ended writing |
| Datasets | SQuAD V2, MATH, HumanEval, Alpaca |
| Perturbations | character, word, sentence, semantic |
| Evaluation | embedding-based similarity / semantic drift |
| Correction | raw drift vs noise-corrected drift |
| Scale | 5 cases per task, 3 samples per prompt version |

Corrected sensitivity ranking:

| Task | Rank 1 | Rank 2 | Rank 3 | Rank 4 |
|---|---|---|---|---|
| Factual QA | semantic | word | sentence | character |
| Math reasoning | word | sentence | semantic | character |
| Code generation | semantic | word | character | sentence |
| Open-ended writing | character | sentence | word | semantic |

说明：

```text
这是当前 RQ1 的主 pilot result。
相比 2x3 版本，5x3 版本在 factual QA、math reasoning、code generation 上保持相同的 top perturbation。
open-ended writing 的 top perturbation 从 sentence 变为 character，说明开放式写作的 ranking 更不稳定，需要更多样本。
```

## RQ1 完成度判断

### 已完成部分

| RQ1 组成部分 | 当前状态 | 对应 MD / 结果文件 | 得到的结论 |
|---|---|---|---|
| sample-noise correction pipeline | 已完成 | `sample_noise_correction_validation.md`; `sample_noise_pilot.py`; `four_task_similarity_sweep.py` | 已实现 repeated sampling、within-prompt noise baseline、raw drift、noise-corrected drift。可以在同一批 clean / perturbed outputs 上比较 uncorrected 和 corrected estimate。 |
| cross-task paraphrase preliminary validation | 已完成 | `cross_task_paraphrase_noise_correction.md` | 这是 four-task perturbation evaluation 的 preliminary validation。固定 paraphrasing / instruction rewording 这一种共同扰动，覆盖 SQuAD V2、MATH、HumanEval、Alpaca 四类任务。结果显示同一种 perturbation 在不同任务上的 corrected drift 不同，说明 perturbation effect 是 task-dependent，并支持后续扩展到多扰动主实验。 |
| four-task multi-perturbation similarity sweep | pilot 已完成并扩大 | `rq1_four_task_similarity_sweep_5x3_result.md`; `results/similarity_report_four_task_similarity_sweep_5x3.md`; `results/similarity_rankings_four_task_similarity_sweep_5x3.csv`; `sample_noise_correction_interpretation.md` | 这是当前 RQ1 主实验。已完成 4 tasks × 4 perturbations × 5 cases/task × 3 samples/prompt 的 similarity sweep。该实验同时包含 uncorrected raw drift 与 noise-corrected drift 比较。结果显示 corrected sensitivity ranking 是 task-dependent，且 correction 会改变部分 ranking：Factual QA 小变化，Math 有变化，Code 无变化，Open-ended writing 有变化。5x3 corrected ranking：Factual QA = semantic > word > sentence > character；Math = word > sentence > semantic > character；Code = semantic > word > character > sentence；Writing = character > sentence > word > semantic。 |
| objective-task PDR check | 已完成 | `promptrobust_reference_aligned_pdr_result.md`; `cross_task_paraphrase_noise_correction.md` | 对 Factual QA 和 Math reasoning，可以用 PDR based on correctness。Factual QA 中 paraphrase 可降低 correctness；Math 中 paraphrase 反而可能提高 correctness，说明 perturbation 不一定是 harmful noise。 |
| MATH larger PDR validation | 已完成 | `math_paraphrase_pdr_25x3_analysis.md`; `results/pdr_report_math_paraphrase_pdr_25x3.md` | 扩大到 25 条 MATH 后，paraphrase 仍提升 final-answer correctness：clean repeated performance = 0.3600，perturbed repeated performance = 0.5867，repeated PDR = -0.6296。 |

### 未完成或需要补充部分

| 需要补充的部分 | 当前状态 | 为什么需要补 | 建议下一步 | 是否需要新模型调用 |
|---|---|---|---|---:|
| 更大规模 four-task similarity sweep | 未完成 benchmark-scale | 当前主结果是 5 cases/task，本质上是 pilot-expanded evidence，不是 benchmark-scale evidence。RQ1 要讨论的是不同 task / perturbation 的 sensitivity ranking 是否稳定；如果每个 task 只有 5 个 case，ranking 可能受个别样本影响。扩大样本量可以检验现在的 corrected ranking 是否还能保持，例如 Math 是否仍然是 word > sentence > semantic > character，Writing 是否仍然是 character / sentence 最敏感。 | 将当前 5 cases/task 扩大到 10 或 25 cases/task。10 cases/task 是低成本增强版；25 cases/task 更适合写成主实验结果。 | 是 |
| ranking stability / bootstrap | 未完成 | 这个不是新增数据实验，而是对已有 5x3 结果做稳定性检验。当前已经有 480 个 generation outputs，但只有 20 个 dataset cases。bootstrap 可以回答：当前 ranking 是不是由少数 case 偶然造成的？例如反复重采样 case 后，semantic perturbation 在 Factual QA 中成为 Rank 1 的概率是多少。它适合补充在结果分析里，说明 ranking 的可信度。 | 直接对 `results/similarity_metrics_four_task_similarity_sweep_5x3.csv` 做 case-level bootstrap，估计每个 task 下各 perturbation 成为 Rank 1 / Rank 2 的概率。 | 否 |
| code generation correctness | 可选补充 / 未完成 | 如果 RQ1 只限定为 cross-task similarity / semantic drift，那么 HumanEval unit-test pass rate 不是必须项；当前 similarity sweep 已经覆盖 Code generation。若 RQ1 声称评价 perturbation 对 task performance 或 correctness 的影响，那么 code generation 只看 embedding similarity 不够，因为 HumanEval 的标准评价准则是 unit-test pass/fail。补这个可以让 Code generation 与参考 benchmark 的 correctness evaluation 对齐。 | 若 proposal 需要 correctness evidence，则用 HumanEval outputs 跑本地 unit tests，计算 clean pass rate、perturbed pass rate、uncorrected PDR、repeated-sampling PDR。若 RQ1 只保留 semantic drift 主线，可把它写为 limitation / future work。 | 不一定，需要本地执行测试；若复用已有 outputs，通常不需要新模型调用 |
| open-ended writing quality metrics | 可选补充 / 未完成 | 如果 RQ1 只做统一的 similarity / semantic drift 比较，那么 Alpaca 当前结果可以用于 apple-to-apple cross-task comparison。若 RQ1 声称评价 open-ended writing quality，或者要严格贴近开放生成类参考文献，则 embedding similarity 不足以覆盖 response diversity、semantic coherence、fluency 等质量维度。补这些指标可以说明 sample-noise correction 不只影响语义漂移，也可能影响开放生成质量解释。 | 主线不一定要补。若要增强 writing task，可先加低成本 proxy：length stability、distinct-n / lexical diversity、embedding coherence；如 proposal 需要更强 quality evaluation，再加 LLM judge 评估 coherence / fluency。 | 可能；proxy 不需要新模型调用，LLM judge 需要 |
| SQuAD + MATH larger PDR sweep across multiple perturbations | 部分完成 | Factual QA 和 Math reasoning 是有明确正确答案的 objective tasks。当前已有 PDR 检查和 MATH larger paraphrase validation，但 PDR 还没有像 similarity sweep 一样系统覆盖 character / word / sentence / semantic 四种扰动和较大样本量。如果论文希望同时报告 semantic drift 和 correctness degradation，这部分会增强说服力。 | 对 SQuAD V2 和 MATH 用 character / word / sentence / semantic 跑 10 或 25 cases/task，输出 clean correctness、perturbed correctness、uncorrected PDR、repeated-sampling PDR。 | 是 |
| multi-temperature comparison | 可选 robustness check / 未完成 | sample noise 与 decoding randomness 强相关。当前 RQ1 主结果固定在 temperature 0.7，因此结论严格来说是在该 decoding setting 下成立。如果 reviewer 问 sample-noise correction 是否只在某个 temperature 下有效，需要 temperature 对比来回答。 | 选择 0.0 / 0.7 / 1.0 做小规模复验。0.0 可作为低 sample-noise 对照，1.0 可作为高 sample-noise 对照。 | 是 |
| multi-model comparison | 可选 robustness check / 未完成 | 当前结果是单模型设置，因此结论主要是 method-level pilot evidence。如果 proposal 要声称方法具有跨模型普适性，需要至少再加入一个模型。否则应把结论限定为当前模型和 decoding setting 下的发现。 | 先完成单模型 RQ1 主线。若时间允许，再用另一个 API 模型或本地开源模型复验较小的 four-task subset。 | 是 |

## 当前可以支持的 RQ1 初步结论

目前数据可以支持以下 pilot-level 结论：

1. **sample-noise correction 会改变 perturbation effect 的估计。**

   在 similarity drift 和 PDR correctness 下，single-sample estimate 与 repeated-sampling estimate 都可能不同。

2. **perturbation effect 是 task-dependent 的。**

   同一个 paraphrase perturbation 在 Factual QA 中可能降低 correctness，在 MATH 中反而提高 correctness。

3. **不同 perturbation 的 sensitivity pattern 不同。**

   在 SQuAD + MATH sweep 中，semantic-level perturbation 对 Factual QA 的 similarity drift 最大；math reasoning 中 word/sentence raw drift 很大程度被 sample noise 吸收。

4. **single-generation evaluation 不稳定。**

   它可能高估、低估，甚至漏掉 perturbation effect。

## 为什么还不能说 RQ1 完成

RQ1 的关键词是：

```text
different perturbation types
across factual QA, math reasoning, code generation, and open-ended writing
stable sensitivity ranking
```

现在 pilot 版本已经完成：

```text
4 tasks × multiple perturbation types × corrected ranking
```

但 benchmark-scale 版本仍然缺更强的证据层级：

主线缺口：

- 更大的每任务样本数。当前 5 cases/task 可以支持 pilot-level conclusion，但不足以强声明 stable sensitivity ranking。
- ranking stability / bootstrap。当前 ranking 已经算出，但还需要检查这些 ranking 是否由少数 case 驱动。

reference-aligned 补充项：

- HumanEval unit-test pass rate。若 RQ1 只讨论 semantic drift，这不是必须项；若讨论 code-generation correctness 或 task-performance impact，则需要补。
- Alpaca response diversity / semantic coherence / fluency。若 RQ1 只做统一 similarity 比较，这不是必须项；若讨论 open-ended writing quality，则需要补。

robustness 扩展项：

- 多 temperature 比较。用于检查 sample-noise correction 是否依赖 decoding randomness。
- 多模型比较。用于检查结论是否只适用于当前模型。

## 建议下一步补齐的实验

### 已完成实验：four-task similarity sweep

已经用 similarity / semantic drift 补齐 pilot RQ1 matrix：

| Task | Dataset | Perturbations | Evaluation |
|---|---|---|---|
| Factual QA | SQuAD V2 | character, word, sentence, semantic | corrected similarity drift |
| Math reasoning | MATH | character, word, sentence, semantic | corrected similarity drift |
| Code generation | HumanEval | character, word, sentence, semantic | corrected similarity drift |
| Open-ended writing | Alpaca | character, word, sentence, semantic | corrected similarity drift |

已输出：

```text
Task × Perturbation × raw drift × noise baseline × corrected drift
```

并根据 corrected drift 排序，得到每个 task 的 perturbation sensitivity ranking。

### 后续增强实验

1. HumanEval correctness:

   ```text
   unit-test pass rate based PDR
   ```

2. Alpaca quality metrics:

   ```text
   response diversity
   semantic coherence
   fluency / length stability
   ```

3. Larger sample size:

   ```text
   at least 10-25 cases per task
   at least 3-5 repeated generations per prompt version
   ```

## Bottom Line

当前 RQ1 的状态：

```text
Pilot matrix complete and expanded to 5 cases per task.
Benchmark-scale RQ1 not yet complete.
```

可以写进 proposal / progress report 的表述：

```text
The current experiments validate the RQ1 methodology and now include a pilot four-task by multi-perturbation similarity matrix. The corrected sensitivity rankings differ across tasks, suggesting that perturbation sensitivity is task-dependent. However, this remains a pilot-scale result because each task currently uses only two examples in the full matrix; benchmark-scale evidence will require more cases per task and task-specific correctness metrics for code generation and open-ended writing.
```

## Current Overall Status for Review

This section summarizes what is complete and what remains before treating RQ1 as fully supported.

### Completed

| Module | Status | Main file |
|---|---|---|
| Four-task similarity sweep | Completed at 5 cases/task | `rq1_four_task_similarity_sweep_5x3_result.md` |
| Raw drift vs corrected drift | Completed | `rq1_four_task_similarity_sweep_5x3_result.md` |
| Corrected sensitivity ranking | Completed | `results/similarity_rankings_four_task_similarity_sweep_5x3.csv` |
| Raw ranking vs corrected ranking | Completed | `rq1_four_task_similarity_sweep_5x3_result.md` |
| Cross-task paraphrase validation | Completed | `cross_task_paraphrase_noise_correction.md` |
| MATH paraphrase PDR expanded check | Completed at 25 MATH cases | `math_paraphrase_pdr_25x3_analysis.md` |
| SQuAD + MATH PDR correctness pilot | Completed | `promptrobust_reference_aligned_pdr_result.md` |
| Perturbation sweep on SQuAD + MATH | Completed | `promptrobust_perturbation_sweep_result.md` |

### Still Missing

| Priority | Missing simulation / analysis | Why it matters | Requires new model calls? |
|---|---|---|---:|
| P0 | Expand four-task similarity sweep to 10 or 25 cases/task | Current 5 cases/task is still small; RQ1 asks about stable ranking | Yes |
| P0 | Confirm whether corrected ranking stays stable at larger scale | This directly tests RQ1's "stable sensitivity ranking" language | Yes |
| P1 | Bootstrap ranking stability on current 5x3 result | Checks whether the observed ranking is driven by a few samples | No |
| P1 | HumanEval unit-test correctness | Code generation currently has similarity drift but not pass-rate correctness | No new generations if using existing outputs; local test execution needed |
| P1 | Alpaca open-ended quality metrics | Writing currently has embedding similarity only, not diversity/coherence/fluency | Maybe |
| P2 | Larger PDR sweep for SQuAD + MATH across multiple perturbations | Strengthens correctness-based evidence for objective-answer tasks | Yes |
| P2 | Multi-temperature comparison | Tests whether sample noise grows under higher sampling randomness | Yes |
| P3 | Multi-model comparison | Needed only if proposal keeps cross-model consistency as a research question | Yes |

### Recommended Next Order

Recommended sequence:

1. **Bootstrap current 5x3 ranking stability.**

   Use:

   ```text
   results/similarity_metrics_four_task_similarity_sweep_5x3.csv
   ```

   This does not require new API calls. It would estimate how often each perturbation becomes Rank 1 under resampling.

2. **If ranking is unstable, expand four-task similarity sweep.**

   Suggested next scale:

   ```text
   10 cases/task
   ```

   Expected generation calls:

   ```text
   4 tasks × 10 cases × 4 perturbations × 2 prompt versions × 3 samples = 960
   ```

3. **Add HumanEval correctness.**

   Use existing HumanEval generations where possible and run unit tests locally to compute pass rate.

4. **Add open-ended writing auxiliary metrics.**

   Candidate metrics:

   ```text
   response length change
   response diversity
   semantic coherence proxy
   fluency proxy
   ```

### Current Best RQ1 Statement

The current evidence supports this statement:

```text
The RQ1 pilot matrix is complete. Across four tasks and four perturbation types, sample-noise-corrected sensitivity rankings differ by task. Correction also changes some rankings compared with raw drift, especially for math reasoning and open-ended writing. However, the current result is still pilot-scale because the full four-task matrix uses 5 cases per task. A larger sample or bootstrap stability analysis is needed before making a strong benchmark-level claim about ranking stability.
```
