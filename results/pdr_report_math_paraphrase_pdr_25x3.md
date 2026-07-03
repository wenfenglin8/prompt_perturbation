# PromptRobust-Aligned PDR Evaluation

This run aligns the small validation with PromptRobust / PromptBench as closely as the local setup allows:

- Datasets: `SQuAD V2` for factual QA and `MATH` for mathematical reasoning.
- Perturbations: `paraphrase` applied to the instruction only.
- Evaluation criterion: Performance Drop Rate (PDR), using task correctness as performance.

## Aggregate Result

- Average clean single-sample correctness: `0.4000`
- Average perturbed single-sample correctness: `0.6000`
- Dataset-level uncorrected single-sample PDR: `-0.5000`
- Average clean repeated correctness: `0.3600`
- Average perturbed repeated correctness: `0.5867`
- Dataset-level repeated-sampling PDR: `-0.6296`

## Grouped Result

| perturbation | task | n | clean single | perturbed single | uncorrected PDR | clean repeated | perturbed repeated | repeated PDR | difference |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| paraphrase | math_reasoning | 25 | 0.4000 | 0.6000 | -0.5000 | 0.3600 | 0.5867 | -0.6296 | 0.1296 |

## Per-Item Metrics

| case | perturbation | task | dataset | clean single | perturbed single | uncorrected PDR | clean mean | perturbed mean | repeated PDR | correctness noise |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| promptrobust_pdr_paraphrase_math_01 | paraphrase | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_02 | paraphrase | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.3333 | 1.0000 | -2.0000 | 0.2357 |
| promptrobust_pdr_paraphrase_math_03 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_04 | paraphrase | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_05 | paraphrase | math_reasoning | MATH | 1 | 1 | 0.0000 | 0.6667 | 1.0000 | -0.5000 | 0.2357 |
| promptrobust_pdr_paraphrase_math_06 | paraphrase | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 0.6667 | 0.3333 | 0.2357 |
| promptrobust_pdr_paraphrase_math_07 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_08 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_09 | paraphrase | math_reasoning | MATH | 1 | 0 | 1.0000 | 0.6667 | 0.3333 | 0.5000 | 0.4714 |
| promptrobust_pdr_paraphrase_math_10 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_11 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_12 | paraphrase | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_13 | paraphrase | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_14 | paraphrase | math_reasoning | MATH | 1 | 1 | 0.0000 | 0.3333 | 1.0000 | -2.0000 | 0.2357 |
| promptrobust_pdr_paraphrase_math_15 | paraphrase | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_16 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_17 | paraphrase | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_18 | paraphrase | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.3333 | 0.6667 | -1.0000 | 0.4714 |
| promptrobust_pdr_paraphrase_math_19 | paraphrase | math_reasoning | MATH | 1 | 0 | 1.0000 | 1.0000 | 0.3333 | 0.6667 | 0.2357 |
| promptrobust_pdr_paraphrase_math_20 | paraphrase | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_21 | paraphrase | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.3333 | 0.3333 | 0.0000 | 0.4714 |
| promptrobust_pdr_paraphrase_math_22 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.3333 | 0.0000 | 0.2357 |
| promptrobust_pdr_paraphrase_math_23 | paraphrase | math_reasoning | MATH | 1 | 1 | 0.0000 | 0.3333 | 1.0000 | -2.0000 | 0.2357 |
| promptrobust_pdr_paraphrase_math_24 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_25 | paraphrase | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |

## Interpretation

The uncorrected condition estimates PDR from one clean output and one perturbed output. The repeated-sampling condition keeps the same dataset, perturbation, model, decoding parameters, and PDR criterion, but estimates clean and perturbed performance from repeated generations. This is the apple-to-apple comparison needed to test whether single-generation PDR overstates or understates perturbation impact.