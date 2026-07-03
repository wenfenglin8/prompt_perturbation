# Sample Noise Pilot Report

- Suite: `posix_mmlu_bbh`
- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Samples per original/perturbed prompt: `3`
- Decoding: temperature `0.7`, top_p `0.9`

## Aggregate Result

- Average raw perturbation drift: `0.0349`
- Average sample-noise baseline: `0.0349`
- Average noise-corrected drift: `0.0000`
- Estimated share of raw drift explainable by sampling noise: `100.0%`

Interpretation: raw prompt-perturbation drift overstates the perturbation effect whenever the noise baseline is non-trivial. The noise-corrected value estimates the part of the observed drift that remains after accounting for ordinary repeated-generation variability.

## Per-Item Metrics

| case | task | noise baseline | raw drift | corrected drift | SNR | bootstrap P(raw>noise) |
|---|---:|---:|---:|---:|---:|---:|
| posix_mmlu_01 | mmlu_multiple_choice_reasoning | 0.0000 | 0.0000 | 0.0000 | 3089215745.33 | 1.000 |
| posix_mmlu_02 | mmlu_multiple_choice_reasoning | 0.0000 | 0.0000 | 0.0000 | inf | 0.000 |
| posix_bbh_logical_deduction_01 | bbh_logical_deduction | 0.0084 | 0.0084 | 0.0000 | 1.00 | 0.228 |
| posix_bbh_logical_deduction_02 | bbh_logical_deduction | 0.1314 | 0.1313 | 0.0000 | 1.00 | 0.554 |

## Link to Haase et al.

Haase et al. argue that LLM evaluation based on a single generation conflates prompt effects with sampling variability. This pilot operationalizes that claim for prompt perturbation: first estimate within-prompt variability from repeated generations, then subtract that baseline from between-prompt drift. A perturbation should be treated as meaningful only when its between-version drift clearly exceeds the within-version noise baseline.