# PromptRobust-Aligned PDR Evaluation

This run aligns the small validation with PromptRobust / PromptBench as closely as the local setup allows:

- Datasets: `HumanEval, MATH, SQuAD V2`.
- Tasks: `factual_qa, math_reasoning, code_generation`.
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise` applied to the instruction only.
- Evaluation criterion: Performance Drop Rate (PDR), using task correctness as performance.
- Code generation correctness: HumanEval pass@1-style unit-test pass/fail. The model output is treated as a completion appended to the HumanEval prompt; standalone full-function outputs are also accepted.

## Aggregate Result

- Average clean single-sample correctness: `0.4667`
- Average perturbed single-sample correctness: `0.5333`
- Dataset-level uncorrected single-sample PDR: `-0.1429`
- Average clean repeated correctness: `0.5111`
- Average perturbed repeated correctness: `0.5556`
- Dataset-level repeated-sampling PDR: `-0.0870`

## Grouped Result

| perturbation | task | n | clean single | perturbed single | uncorrected PDR | clean repeated | perturbed repeated | repeated PDR | difference |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| paraphrase | factual_qa | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| paraphrase | math_reasoning | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| paraphrase | code_generation | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| reordering | factual_qa | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.6667 | -0.3333 | 0.3333 |
| reordering | math_reasoning | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| reordering | code_generation | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| formatting | factual_qa | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| formatting | math_reasoning | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.8333 | -0.6667 | 0.6667 |
| formatting | code_generation | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.1667 | 0.6667 | -0.6667 |
| context_injection | factual_qa | 2 | 0.5000 | 1.0000 | -1.0000 | 0.5000 | 0.8333 | -0.6667 | -0.3333 |
| context_injection | math_reasoning | 2 | 0.5000 | 0.0000 | 1.0000 | 0.6667 | 0.3333 | 0.5000 | 0.5000 |
| context_injection | code_generation | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| surface_noise | factual_qa | 2 | 0.5000 | 1.0000 | -1.0000 | 0.6667 | 0.8333 | -0.2500 | -0.7500 |
| surface_noise | math_reasoning | 2 | 0.0000 | 0.5000 | 0.0000 | 0.3333 | 0.6667 | -1.0000 | 1.0000 |
| surface_noise | code_generation | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |

## Per-Item Metrics

| case | perturbation | task | dataset | clean single | perturbed single | uncorrected PDR | clean mean | perturbed mean | repeated PDR | correctness noise |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| promptrobust_pdr_paraphrase_squad_01 | paraphrase | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_squad_01 | reordering | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_squad_01 | formatting | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_squad_01 | context_injection | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_squad_01 | surface_noise | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_squad_02 | paraphrase | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_squad_02 | reordering | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.3333 | 0.0000 | 0.2357 |
| promptrobust_pdr_formatting_squad_02 | formatting | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_squad_02 | context_injection | factual_qa | SQuAD V2 | 0 | 1 | 0.0000 | 0.0000 | 0.6667 | 0.0000 | 0.2357 |
| promptrobust_pdr_surface_noise_squad_02 | surface_noise | factual_qa | SQuAD V2 | 0 | 1 | 0.0000 | 0.3333 | 0.6667 | -1.0000 | 0.4714 |
| promptrobust_pdr_paraphrase_math_01 | paraphrase | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_math_01 | reordering | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 0.6667 | 0.3333 | 0.2357 |
| promptrobust_pdr_formatting_math_01 | formatting | math_reasoning | MATH | 1 | 1 | 0.0000 | 0.6667 | 1.0000 | -0.5000 | 0.2357 |
| promptrobust_pdr_context_injection_math_01 | context_injection | math_reasoning | MATH | 1 | 0 | 1.0000 | 1.0000 | 0.6667 | 0.3333 | 0.2357 |
| promptrobust_pdr_surface_noise_math_01 | surface_noise | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.6667 | 1.0000 | -0.5000 | 0.2357 |
| promptrobust_pdr_paraphrase_math_02 | paraphrase | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_math_02 | reordering | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.3333 | 0.0000 | 0.2357 |
| promptrobust_pdr_formatting_math_02 | formatting | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.3333 | 0.6667 | -1.0000 | 0.4714 |
| promptrobust_pdr_context_injection_math_02 | context_injection | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.3333 | 0.0000 | 1.0000 | 0.2357 |
| promptrobust_pdr_surface_noise_math_02 | surface_noise | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.3333 | 0.0000 | 0.2357 |
| promptrobust_pdr_paraphrase_humaneval_01 | paraphrase | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_humaneval_01 | reordering | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_humaneval_01 | formatting | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_humaneval_01 | context_injection | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_humaneval_01 | surface_noise | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_humaneval_02 | paraphrase | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_humaneval_02 | reordering | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_humaneval_02 | formatting | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 0.3333 | 0.6667 | 0.2357 |
| promptrobust_pdr_context_injection_humaneval_02 | context_injection | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_humaneval_02 | surface_noise | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

## Interpretation

The uncorrected condition estimates PDR from one clean output and one perturbed output. The repeated-sampling condition keeps the same dataset, perturbation, model, decoding parameters, and PDR criterion, but estimates clean and perturbed performance from repeated generations. This is the apple-to-apple comparison needed to test whether single-generation PDR overstates or understates perturbation impact.