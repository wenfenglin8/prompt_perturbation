# PromptRobust-Aligned PDR Evaluation

This run aligns the small validation with PromptRobust / PromptBench as closely as the local setup allows:

- Datasets: `MATH`.
- Tasks: `math_reasoning`.
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise` applied to the instruction only.
- Evaluation criterion: Performance Drop Rate (PDR), using task correctness as performance.
- Code generation correctness: HumanEval pass@1-style unit-test pass/fail; completions are evaluated as HumanEval prompt + model completion, with standalone full-code outputs accepted as a fallback.

## Aggregate Result

- Average clean single-sample correctness: `0.4000`
- Average perturbed single-sample correctness: `0.4000`
- Dataset-level uncorrected single-sample PDR: `0.0000`
- Average clean repeated correctness: `0.3600`
- Average perturbed repeated correctness: `0.4267`
- Dataset-level repeated-sampling PDR: `-0.1852`

## Grouped Result

| perturbation | task | n | clean single | perturbed single | uncorrected PDR | clean repeated | perturbed repeated | repeated PDR | difference |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| paraphrase | math_reasoning | 10 | 0.4000 | 0.2000 | 0.5000 | 0.3333 | 0.3000 | 0.1000 | 0.4000 |
| reordering | math_reasoning | 10 | 0.5000 | 0.5000 | 0.0000 | 0.4000 | 0.4333 | -0.0833 | 0.0833 |
| formatting | math_reasoning | 10 | 0.3000 | 0.5000 | -0.6667 | 0.3333 | 0.5667 | -0.7000 | 0.0333 |
| context_injection | math_reasoning | 10 | 0.3000 | 0.4000 | -0.3333 | 0.3667 | 0.3667 | 0.0000 | -0.3333 |
| surface_noise | math_reasoning | 10 | 0.5000 | 0.4000 | 0.2000 | 0.3667 | 0.4667 | -0.2727 | 0.4727 |

## Per-Item Metrics

| case | perturbation | task | dataset | clean single | perturbed single | uncorrected PDR | clean mean | perturbed mean | repeated PDR | correctness noise |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| promptrobust_pdr_paraphrase_math_01 | paraphrase | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 0.6667 | 0.3333 | 0.2357 |
| promptrobust_pdr_reordering_math_01 | reordering | math_reasoning | MATH | 1 | 1 | 0.0000 | 0.6667 | 1.0000 | -0.5000 | 0.2357 |
| promptrobust_pdr_formatting_math_01 | formatting | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_math_01 | context_injection | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_math_01 | surface_noise | math_reasoning | MATH | 1 | 1 | 0.0000 | 0.6667 | 1.0000 | -0.5000 | 0.2357 |
| promptrobust_pdr_paraphrase_math_02 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.3333 | 0.0000 | 0.2357 |
| promptrobust_pdr_reordering_math_02 | reordering | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.3333 | 0.0000 | 0.2357 |
| promptrobust_pdr_formatting_math_02 | formatting | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.0000 | 0.6667 | 0.0000 | 0.2357 |
| promptrobust_pdr_context_injection_math_02 | context_injection | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_math_02 | surface_noise | math_reasoning | MATH | 1 | 0 | 1.0000 | 0.3333 | 0.3333 | 0.0000 | 0.4714 |
| promptrobust_pdr_paraphrase_math_03 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_math_03 | reordering | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_math_03 | formatting | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_math_03 | context_injection | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_math_03 | surface_noise | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_04 | paraphrase | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_math_04 | reordering | math_reasoning | MATH | 1 | 1 | 0.0000 | 0.6667 | 1.0000 | -0.5000 | 0.2357 |
| promptrobust_pdr_formatting_math_04 | formatting | math_reasoning | MATH | 1 | 1 | 0.0000 | 0.3333 | 1.0000 | -2.0000 | 0.2357 |
| promptrobust_pdr_context_injection_math_04 | context_injection | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 0.6667 | 0.3333 | 0.2357 |
| promptrobust_pdr_surface_noise_math_04 | surface_noise | math_reasoning | MATH | 1 | 1 | 0.0000 | 0.6667 | 1.0000 | -0.5000 | 0.2357 |
| promptrobust_pdr_paraphrase_math_05 | paraphrase | math_reasoning | MATH | 1 | 0 | 1.0000 | 0.3333 | 0.6667 | -1.0000 | 0.4714 |
| promptrobust_pdr_reordering_math_05 | reordering | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 0.3333 | 0.6667 | 0.2357 |
| promptrobust_pdr_formatting_math_05 | formatting | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.3333 | 1.0000 | -2.0000 | 0.2357 |
| promptrobust_pdr_context_injection_math_05 | context_injection | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.6667 | 1.0000 | -0.5000 | 0.2357 |
| promptrobust_pdr_surface_noise_math_05 | surface_noise | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.3333 | 0.0000 | 0.2357 |
| promptrobust_pdr_paraphrase_math_06 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.3333 | 0.0000 | 1.0000 | 0.2357 |
| promptrobust_pdr_reordering_math_06 | reordering | math_reasoning | MATH | 1 | 1 | 0.0000 | 0.6667 | 1.0000 | -0.5000 | 0.2357 |
| promptrobust_pdr_formatting_math_06 | formatting | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_math_06 | context_injection | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.3333 | 0.6667 | -1.0000 | 0.4714 |
| promptrobust_pdr_surface_noise_math_06 | surface_noise | math_reasoning | MATH | 1 | 0 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_07 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_math_07 | reordering | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_math_07 | formatting | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_math_07 | context_injection | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_math_07 | surface_noise | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_08 | paraphrase | math_reasoning | MATH | 1 | 0 | 1.0000 | 0.6667 | 0.0000 | 1.0000 | 0.2357 |
| promptrobust_pdr_reordering_math_08 | reordering | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.3333 | 0.0000 | 1.0000 | 0.2357 |
| promptrobust_pdr_formatting_math_08 | formatting | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.3333 | 0.3333 | 0.0000 | 0.4714 |
| promptrobust_pdr_context_injection_math_08 | context_injection | math_reasoning | MATH | 1 | 0 | 1.0000 | 0.3333 | 0.0000 | 1.0000 | 0.2357 |
| promptrobust_pdr_surface_noise_math_08 | surface_noise | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_09 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.3333 | 0.0000 | 0.2357 |
| promptrobust_pdr_reordering_math_09 | reordering | math_reasoning | MATH | 1 | 1 | 0.0000 | 0.6667 | 0.6667 | 0.0000 | 0.4714 |
| promptrobust_pdr_formatting_math_09 | formatting | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.3333 | 0.6667 | -1.0000 | 0.4714 |
| promptrobust_pdr_context_injection_math_09 | context_injection | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.3333 | 0.3333 | 0.0000 | 0.4714 |
| promptrobust_pdr_surface_noise_math_09 | surface_noise | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_math_10 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_math_10 | reordering | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_math_10 | formatting | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_math_10 | context_injection | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_math_10 | surface_noise | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Interpretation

The uncorrected condition estimates PDR from one clean output and one perturbed output. The repeated-sampling condition keeps the same dataset, perturbation, model, decoding parameters, and PDR criterion, but estimates clean and perturbed performance from repeated generations. This is the apple-to-apple comparison needed to test whether single-generation PDR overstates or understates perturbation impact.