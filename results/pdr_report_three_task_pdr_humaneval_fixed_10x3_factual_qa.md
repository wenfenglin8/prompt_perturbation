# PromptRobust-Aligned PDR Evaluation

This run aligns the small validation with PromptRobust / PromptBench as closely as the local setup allows:

- Datasets: `SQuAD V2`.
- Tasks: `factual_qa`.
- Perturbations: `paraphrase, reordering, formatting, context_injection, surface_noise` applied to the instruction only.
- Evaluation criterion: Performance Drop Rate (PDR), using task correctness as performance.
- Code generation correctness: HumanEval pass@1-style unit-test pass/fail; completions are evaluated as HumanEval prompt + model completion, with standalone full-code outputs accepted as a fallback.

## Aggregate Result

- Average clean single-sample correctness: `0.6200`
- Average perturbed single-sample correctness: `0.6000`
- Dataset-level uncorrected single-sample PDR: `0.0323`
- Average clean repeated correctness: `0.6267`
- Average perturbed repeated correctness: `0.6067`
- Dataset-level repeated-sampling PDR: `0.0319`

## Grouped Result

| perturbation | task | n | clean single | perturbed single | uncorrected PDR | clean repeated | perturbed repeated | repeated PDR | difference |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| paraphrase | factual_qa | 10 | 0.6000 | 0.6000 | 0.0000 | 0.6333 | 0.5667 | 0.1053 | -0.1053 |
| reordering | factual_qa | 10 | 0.6000 | 0.6000 | 0.0000 | 0.6000 | 0.6000 | 0.0000 | 0.0000 |
| formatting | factual_qa | 10 | 0.7000 | 0.6000 | 0.1429 | 0.6667 | 0.6000 | 0.1000 | 0.0429 |
| context_injection | factual_qa | 10 | 0.6000 | 0.7000 | -0.1667 | 0.6333 | 0.7333 | -0.1579 | -0.0088 |
| surface_noise | factual_qa | 10 | 0.6000 | 0.5000 | 0.1667 | 0.6000 | 0.5333 | 0.1111 | 0.0556 |

## Per-Item Metrics

| case | perturbation | task | dataset | clean single | perturbed single | uncorrected PDR | clean mean | perturbed mean | repeated PDR | correctness noise |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| promptrobust_pdr_paraphrase_squad_01 | paraphrase | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_squad_01 | reordering | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_squad_01 | formatting | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_squad_01 | context_injection | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_squad_01 | surface_noise | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_squad_02 | paraphrase | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_squad_02 | reordering | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_squad_02 | formatting | factual_qa | SQuAD V2 | 1 | 0 | 1.0000 | 0.3333 | 0.0000 | 1.0000 | 0.2357 |
| promptrobust_pdr_context_injection_squad_02 | context_injection | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.6667 | 0.0000 | 0.2357 |
| promptrobust_pdr_surface_noise_squad_02 | surface_noise | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_squad_03 | paraphrase | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.3333 | 0.0000 | 1.0000 | 0.2357 |
| promptrobust_pdr_reordering_squad_03 | reordering | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_squad_03 | formatting | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.3333 | 0.0000 | 1.0000 | 0.2357 |
| promptrobust_pdr_context_injection_squad_03 | context_injection | factual_qa | SQuAD V2 | 0 | 1 | 0.0000 | 0.3333 | 0.6667 | -1.0000 | 0.4714 |
| promptrobust_pdr_surface_noise_squad_03 | surface_noise | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_squad_04 | paraphrase | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_squad_04 | reordering | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_squad_04 | formatting | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_squad_04 | context_injection | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_squad_04 | surface_noise | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_squad_05 | paraphrase | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_squad_05 | reordering | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_squad_05 | formatting | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_squad_05 | context_injection | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_squad_05 | surface_noise | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_squad_06 | paraphrase | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_squad_06 | reordering | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_squad_06 | formatting | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_squad_06 | context_injection | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_squad_06 | surface_noise | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_squad_07 | paraphrase | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_squad_07 | reordering | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_squad_07 | formatting | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_squad_07 | context_injection | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_squad_07 | surface_noise | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_squad_08 | paraphrase | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_squad_08 | reordering | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_squad_08 | formatting | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_squad_08 | context_injection | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_squad_08 | surface_noise | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_paraphrase_squad_09 | paraphrase | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 0.6667 | 0.3333 | 0.2357 |
| promptrobust_pdr_reordering_squad_09 | reordering | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_squad_09 | formatting | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_squad_09 | context_injection | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_squad_09 | surface_noise | factual_qa | SQuAD V2 | 1 | 0 | 1.0000 | 1.0000 | 0.3333 | 0.6667 | 0.2357 |
| promptrobust_pdr_paraphrase_squad_10 | paraphrase | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_reordering_squad_10 | reordering | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_formatting_squad_10 | formatting | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_context_injection_squad_10 | context_injection | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_surface_noise_squad_10 | surface_noise | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

## Interpretation

The uncorrected condition estimates PDR from one clean output and one perturbed output. The repeated-sampling condition keeps the same dataset, perturbation, model, decoding parameters, and PDR criterion, but estimates clean and perturbed performance from repeated generations. This is the apple-to-apple comparison needed to test whether single-generation PDR overstates or understates perturbation impact.