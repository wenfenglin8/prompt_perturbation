# PromptRobust-Aligned PDR Evaluation

This run aligns the small validation with PromptRobust / PromptBench as closely as the local setup allows:

- Datasets: `SQuAD V2` for factual QA and `MATH` for mathematical reasoning.
- Perturbations: `paraphrase` applied to the instruction only.
- Evaluation criterion: Performance Drop Rate (PDR), using task correctness as performance.

## Aggregate Result

- Average clean single-sample correctness: `0.2500`
- Average perturbed single-sample correctness: `0.7500`
- Dataset-level uncorrected single-sample PDR: `-2.0000`
- Average clean repeated correctness: `0.3333`
- Average perturbed repeated correctness: `0.6667`
- Dataset-level repeated-sampling PDR: `-1.0000`

## Grouped Result

| perturbation | task | n | clean single | perturbed single | uncorrected PDR | clean repeated | perturbed repeated | repeated PDR | difference |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| paraphrase | factual_qa | 2 | 0.5000 | 0.5000 | 0.0000 | 0.6667 | 0.5000 | 0.2500 | -0.2500 |
| paraphrase | math_reasoning | 2 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.8333 | 0.0000 | 0.0000 |

## Per-Item Metrics

| case | perturbation | task | dataset | clean single | perturbed single | uncorrected PDR | clean mean | perturbed mean | repeated PDR | correctness noise |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| promptrobust_pdr_paraphrase_squad_01 | paraphrase | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_squad_02 | paraphrase | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.3333 | 0.0000 | 1.0000 | 0.2357 |
| promptrobust_pdr_paraphrase_math_01 | paraphrase | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.0000 | 0.6667 | 0.0000 | 0.2357 |
| promptrobust_pdr_paraphrase_math_02 | paraphrase | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |

## Interpretation

The uncorrected condition estimates PDR from one clean output and one perturbed output. The repeated-sampling condition keeps the same dataset, perturbation, model, decoding parameters, and PDR criterion, but estimates clean and perturbed performance from repeated generations. This is the apple-to-apple comparison needed to test whether single-generation PDR overstates or understates perturbation impact.