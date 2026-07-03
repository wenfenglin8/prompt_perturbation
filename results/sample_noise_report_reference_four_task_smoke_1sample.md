# Sample Noise Pilot Report

- Suite: `reference_four_task`
- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Samples per original/perturbed prompt: `1`
- Decoding: temperature `0.7`, top_p `0.9`

## Aggregate Result

- Average uncorrected single-sample drift: `0.2066`
- Average raw perturbation drift: `0.2066`
- Average sample-noise baseline: `0.0000`
- Average noise-corrected drift: `0.2066`
- Estimated share of raw drift explainable by sampling noise: `0.0%`

Interpretation: raw prompt-perturbation drift overstates the perturbation effect whenever the noise baseline is non-trivial. The noise-corrected value estimates the part of the observed drift that remains after accounting for ordinary repeated-generation variability.

## Per-Item Metrics

| case | task | uncorrected single drift | noise baseline | raw drift | corrected drift | SNR | bootstrap P(raw>noise) |
|---|---:|---:|---:|---:|---:|---:|---:|
| ref_squad_v2_01 | factual_qa | 0.4746 | 0.0000 | 0.4746 | 0.4746 | inf | 1.000 |
| ref_math_01 | math_reasoning | 0.0411 | 0.0000 | 0.0411 | 0.0411 | inf | 1.000 |
| ref_humaneval_01 | code_generation | 0.2110 | 0.0000 | 0.2110 | 0.2110 | inf | 1.000 |
| ref_alpaca_01 | open_ended_writing | 0.0996 | 0.0000 | 0.0996 | 0.0996 | inf | 1.000 |

## Link to Haase et al.

Haase et al. argue that LLM evaluation based on a single generation conflates prompt effects with sampling variability. This pilot operationalizes that claim for prompt perturbation: first estimate within-prompt variability from repeated generations, then subtract that baseline from between-prompt drift. A perturbation should be treated as meaningful only when its between-version drift clearly exceeds the within-version noise baseline.