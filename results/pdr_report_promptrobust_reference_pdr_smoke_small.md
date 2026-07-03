# PromptRobust-Aligned PDR Evaluation

This run aligns the small validation with PromptRobust / PromptBench as closely as the local setup allows:

- Datasets: `SQuAD V2` for factual QA and `MATH` for mathematical reasoning.
- Perturbation: character-level prompt perturbation applied to the instruction only.
- Evaluation criterion: Performance Drop Rate (PDR), using task correctness as performance.

## Aggregate Result

- Average clean single-sample correctness: `1.0000`
- Average perturbed single-sample correctness: `1.0000`
- Average uncorrected single-sample PDR: `0.0000`
- Average clean repeated correctness: `1.0000`
- Average perturbed repeated correctness: `1.0000`
- Average repeated-sampling PDR: `0.0000`

## Per-Item Metrics

| case | task | dataset | clean single | perturbed single | uncorrected PDR | clean mean | perturbed mean | repeated PDR | correctness noise |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| promptrobust_pdr_squad_01 | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_math_01 | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

## Interpretation

The uncorrected condition estimates PDR from one clean output and one perturbed output. The repeated-sampling condition keeps the same dataset, perturbation, model, decoding parameters, and PDR criterion, but estimates clean and perturbed performance from repeated generations. This is the apple-to-apple comparison needed to test whether single-generation PDR overstates or understates perturbation impact.