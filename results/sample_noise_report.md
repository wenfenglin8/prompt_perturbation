# Sample Noise Pilot Report

- Suite: `proposal`
- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Samples per original/perturbed prompt: `4`
- Decoding: temperature `0.7`, top_p `0.9`

## Aggregate Result

- Average raw perturbation drift: `0.1353`
- Average sample-noise baseline: `0.0209`
- Average noise-corrected drift: `0.1144`
- Estimated share of raw drift explainable by sampling noise: `15.4%`

Interpretation: raw prompt-perturbation drift overstates the perturbation effect whenever the noise baseline is non-trivial. The noise-corrected value estimates the part of the observed drift that remains after accounting for ordinary repeated-generation variability.

## Per-Item Metrics

| case | task | noise baseline | raw drift | corrected drift | SNR | bootstrap P(raw>noise) |
|---|---:|---:|---:|---:|---:|---:|
| fact_01 | factual_qa | 0.0000 | 0.0585 | 0.0585 | inf | 1.000 |
| fact_02 | factual_qa | 0.0000 | 0.1475 | 0.1475 | inf | 1.000 |
| math_01 | math_reasoning | 0.0317 | 0.0351 | 0.0034 | 1.11 | 1.000 |
| math_02 | math_reasoning | 0.0000 | 0.3375 | 0.3375 | 3039841285373432.00 | 1.000 |
| code_01 | code_generation | 0.0341 | 0.1249 | 0.0908 | 3.66 | 1.000 |
| writing_01 | open_ended_writing | 0.0595 | 0.1081 | 0.0486 | 1.82 | 1.000 |

## Link to Haase et al.

Haase et al. argue that LLM evaluation based on a single generation conflates prompt effects with sampling variability. This pilot operationalizes that claim for prompt perturbation: first estimate within-prompt variability from repeated generations, then subtract that baseline from between-prompt drift. A perturbation should be treated as meaningful only when its between-version drift clearly exceeds the within-version noise baseline.