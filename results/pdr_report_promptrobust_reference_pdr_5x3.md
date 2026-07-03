# PromptRobust-Aligned PDR Evaluation

This run aligns the small validation with PromptRobust / PromptBench as closely as the local setup allows:

- Datasets: `SQuAD V2` for factual QA and `MATH` for mathematical reasoning.
- Perturbation: character-level prompt perturbation applied to the instruction only.
- Evaluation criterion: Performance Drop Rate (PDR), using task correctness as performance.

## Aggregate Result

- Average clean single-sample correctness: `0.6000`
- Average perturbed single-sample correctness: `0.5000`
- Average uncorrected single-sample PDR: `0.1000`
- Average clean repeated correctness: `0.5667`
- Average perturbed repeated correctness: `0.6000`
- Dataset-level repeated-sampling PDR: `-0.0588`

## Per-Item Metrics

| case | task | dataset | clean single | perturbed single | uncorrected PDR | clean mean | perturbed mean | repeated PDR | correctness noise |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| promptrobust_pdr_squad_01 | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_squad_02 | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.3333 | N/A | 0.2357 |
| promptrobust_pdr_squad_03 | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_squad_04 | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_squad_05 | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_math_01 | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_math_02 | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.3333 | 0.6667 | -1.0000 | 0.4714 |
| promptrobust_pdr_math_03 | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_math_04 | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_math_05 | math_reasoning | MATH | 1 | 0 | 1.0000 | 0.3333 | 0.0000 | 1.0000 | 0.2357 |

## Interpretation

The uncorrected condition estimates PDR from one clean output and one perturbed output. The repeated-sampling condition keeps the same dataset, perturbation, model, decoding parameters, and PDR criterion, but estimates clean and perturbed performance from repeated generations. Aggregate PDR should be computed at the dataset level as `(mean clean performance - mean perturbed performance) / mean clean performance`; per-item PDR is undefined when clean performance is zero.
