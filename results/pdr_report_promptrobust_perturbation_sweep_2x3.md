# PromptRobust-Aligned PDR Evaluation

This run aligns the small validation with PromptRobust / PromptBench as closely as the local setup allows:

- Datasets: `SQuAD V2` for factual QA and `MATH` for mathematical reasoning.
- Perturbations: `character, word, sentence, semantic` applied to the instruction only.
- Evaluation criterion: Performance Drop Rate (PDR), using task correctness as performance.

## Aggregate Result

- Average clean single-sample correctness: `0.3750`
- Average perturbed single-sample correctness: `0.6250`
- Dataset-level uncorrected single-sample PDR: `-0.6667`
- Average clean repeated correctness: `0.4375`
- Average perturbed repeated correctness: `0.6250`
- Dataset-level repeated-sampling PDR: `-0.4286`

## Grouped Result

| perturbation | task | n | clean single | perturbed single | uncorrected PDR | clean repeated | perturbed repeated | repeated PDR | difference |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| character | factual_qa | 2 | 0.5000 | 1.0000 | -1.0000 | 0.6667 | 0.8333 | -0.2500 | -0.7500 |
| character | math_reasoning | 2 | 0.0000 | 0.0000 | 0.0000 | 0.3333 | 0.3333 | 0.0000 | 0.0000 |
| word | factual_qa | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| word | math_reasoning | 2 | 0.0000 | 1.0000 | 0.0000 | 0.1667 | 0.8333 | -4.0000 | 4.0000 |
| sentence | factual_qa | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| sentence | math_reasoning | 2 | 0.5000 | 0.5000 | 0.0000 | 0.3333 | 0.5000 | -0.5000 | 0.5000 |
| semantic | factual_qa | 2 | 0.5000 | 0.5000 | 0.0000 | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| semantic | math_reasoning | 2 | 0.5000 | 1.0000 | -1.0000 | 0.5000 | 1.0000 | -1.0000 | 0.0000 |

## Per-Item Metrics

| case | perturbation | task | dataset | clean single | perturbed single | uncorrected PDR | clean mean | perturbed mean | repeated PDR | correctness noise |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| promptrobust_pdr_character_squad_01 | character | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_word_squad_01 | word | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_sentence_squad_01 | sentence | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_semantic_squad_01 | semantic | factual_qa | SQuAD V2 | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_character_squad_02 | character | factual_qa | SQuAD V2 | 0 | 1 | 0.0000 | 0.3333 | 0.6667 | -1.0000 | 0.4714 |
| promptrobust_pdr_word_squad_02 | word | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_sentence_squad_02 | sentence | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_semantic_squad_02 | semantic | factual_qa | SQuAD V2 | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_character_math_01 | character | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.6667 | 0.6667 | 0.0000 | 0.4714 |
| promptrobust_pdr_word_math_01 | word | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.3333 | 1.0000 | -2.0000 | 0.2357 |
| promptrobust_pdr_sentence_math_01 | sentence | math_reasoning | MATH | 1 | 1 | 0.0000 | 0.6667 | 1.0000 | -0.5000 | 0.2357 |
| promptrobust_pdr_semantic_math_01 | semantic | math_reasoning | MATH | 1 | 1 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_character_math_02 | character | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_word_math_02 | word | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.0000 | 0.6667 | 0.0000 | 0.2357 |
| promptrobust_pdr_sentence_math_02 | sentence | math_reasoning | MATH | 0 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| promptrobust_pdr_semantic_math_02 | semantic | math_reasoning | MATH | 0 | 1 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |

## Interpretation

The uncorrected condition estimates PDR from one clean output and one perturbed output. The repeated-sampling condition keeps the same dataset, perturbation, model, decoding parameters, and PDR criterion, but estimates clean and perturbed performance from repeated generations. This is the apple-to-apple comparison needed to test whether single-generation PDR overstates or understates perturbation impact.