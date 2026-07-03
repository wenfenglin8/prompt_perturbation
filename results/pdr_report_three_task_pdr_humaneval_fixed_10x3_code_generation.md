# PromptRobust-Aligned PDR Evaluation

This run aligns the small validation with PromptRobust / PromptBench as closely as the local setup allows:

- Datasets: `HumanEval`.
- Tasks: `code_generation`.
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise` applied to the instruction only.
- Evaluation criterion: Performance Drop Rate (PDR), using task correctness as performance.
- Code generation correctness: HumanEval pass@1-style unit-test pass/fail; completions are evaluated as HumanEval prompt + model completion, with standalone full-code outputs accepted as a fallback.

## Aggregate Result

- Average clean single-sample correctness: `0.4400`
- Average perturbed single-sample correctness: `0.3600`
- Dataset-level uncorrected single-sample PDR: `0.1818`
- Average clean repeated correctness: `0.4467`
- Average perturbed repeated correctness: `0.3867`
- Dataset-level repeated-sampling PDR: `0.1343`

## Grouped Result

| perturbation | task | n | clean single | perturbed single | uncorrected PDR | clean repeated | perturbed repeated | repeated PDR | difference |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| paraphrase | code_generation | 10 | 0.4000 | 0.4000 | 0.0000 | 0.4333 | 0.4000 | 0.0769 | -0.0769 |
| reordering | code_generation | 10 | 0.4000 | 0.5000 | -0.2500 | 0.4667 | 0.5000 | -0.0714 | -0.1786 |
| formatting | code_generation | 10 | 0.4000 | 0.1000 | 0.7500 | 0.4333 | 0.1667 | 0.6154 | 0.1346 |
| context_injection | code_generation | 10 | 0.5000 | 0.5000 | 0.0000 | 0.4333 | 0.5000 | -0.1538 | 0.1538 |
| surface_noise | code_generation | 10 | 0.5000 | 0.3000 | 0.4000 | 0.4667 | 0.3667 | 0.2143 | 0.1857 |

## Per-Item Metrics

| case | perturbation | task | dataset | clean single | perturbed single | uncorrected PDR | clean mean | perturbed mean | repeated PDR | correctness noise |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| promptrobust_pdr_paraphrase_humaneval_01 | paraphrase | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_humaneval_01 | reordering | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_humaneval_01 | formatting | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_humaneval_01 | context_injection | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_humaneval_01 | surface_noise | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_humaneval_02 | paraphrase | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_humaneval_02 | reordering | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_humaneval_02 | formatting | code_generation | HumanEval | 1 | 0 | 1.0000 | 1.0000 | 0.3333 | 0.6667 | 0.2357 |
| promptrobust_pdr_context_injection_humaneval_02 | context_injection | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_humaneval_02 | surface_noise | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_humaneval_03 | paraphrase | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_humaneval_03 | reordering | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_humaneval_03 | formatting | code_generation | HumanEval | 1 | 0 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |
| promptrobust_pdr_context_injection_humaneval_03 | context_injection | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_humaneval_03 | surface_noise | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_humaneval_04 | paraphrase | code_generation | HumanEval | 1 | 0 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |
| promptrobust_pdr_reordering_humaneval_04 | reordering | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_humaneval_04 | formatting | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.3333 | 0.3333 | 0.0000 | 0.4714 |
| promptrobust_pdr_context_injection_humaneval_04 | context_injection | code_generation | HumanEval | 1 | 1 | 0.0000 | 0.6667 | 1.0000 | -0.5000 | 0.2357 |
| promptrobust_pdr_surface_noise_humaneval_04 | surface_noise | code_generation | HumanEval | 1 | 0 | 1.0000 | 0.6667 | 0.6667 | 0.0000 | 0.4714 |
| promptrobust_pdr_paraphrase_humaneval_05 | paraphrase | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_humaneval_05 | reordering | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_humaneval_05 | formatting | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_humaneval_05 | context_injection | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_humaneval_05 | surface_noise | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_humaneval_06 | paraphrase | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_humaneval_06 | reordering | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_humaneval_06 | formatting | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_humaneval_06 | context_injection | code_generation | HumanEval | 0 | 1 | 0.0000 | 0.0000 | 0.6667 | 0.0000 | 0.2357 |
| promptrobust_pdr_surface_noise_humaneval_06 | surface_noise | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_humaneval_07 | paraphrase | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_humaneval_07 | reordering | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_humaneval_07 | formatting | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_humaneval_07 | context_injection | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_humaneval_07 | surface_noise | code_generation | HumanEval | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_humaneval_08 | paraphrase | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_humaneval_08 | reordering | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_humaneval_08 | formatting | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_humaneval_08 | context_injection | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_humaneval_08 | surface_noise | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_humaneval_09 | paraphrase | code_generation | HumanEval | 0 | 1 | 0.0000 | 0.3333 | 1.0000 | -2.0000 | 0.2357 |
| promptrobust_pdr_reordering_humaneval_09 | reordering | code_generation | HumanEval | 0 | 1 | 0.0000 | 0.6667 | 1.0000 | -0.5000 | 0.2357 |
| promptrobust_pdr_formatting_humaneval_09 | formatting | code_generation | HumanEval | 1 | 0 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |
| promptrobust_pdr_context_injection_humaneval_09 | context_injection | code_generation | HumanEval | 1 | 0 | 1.0000 | 0.6667 | 0.3333 | 0.5000 | 0.4714 |
| promptrobust_pdr_surface_noise_humaneval_09 | surface_noise | code_generation | HumanEval | 1 | 0 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_humaneval_10 | paraphrase | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_humaneval_10 | reordering | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_humaneval_10 | formatting | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_humaneval_10 | context_injection | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_humaneval_10 | surface_noise | code_generation | HumanEval | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Interpretation

The uncorrected condition estimates PDR from one clean output and one perturbed output. The repeated-sampling condition keeps the same dataset, perturbation, model, decoding parameters, and PDR criterion, but estimates clean and perturbed performance from repeated generations. This is the apple-to-apple comparison needed to test whether single-generation PDR overstates or understates perturbation impact.