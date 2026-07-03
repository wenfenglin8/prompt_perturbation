# Sample Noise Pilot Report

- Suite: `proposal`
- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Samples per original/perturbed prompt: `3`
- Decoding: temperature `0.7`, top_p `0.9`

## Aggregate Result

- Average raw perturbation drift: `0.1066`
- Average sample-noise baseline: `0.0524`
- Average noise-corrected drift: `0.0542`
- Estimated share of raw drift explainable by sampling noise: `49.2%`

Interpretation: raw prompt-perturbation drift overstates the perturbation effect whenever the noise baseline is non-trivial. The noise-corrected value estimates the part of the observed drift that remains after accounting for ordinary repeated-generation variability.

## Per-Item Metrics

| case | task | noise baseline | raw drift | corrected drift | SNR | bootstrap P(raw>noise) |
|---|---:|---:|---:|---:|---:|---:|
| code_01 | code_generation | 0.0362 | 0.1120 | 0.0759 | 3.10 | 1.000 |
| writing_01 | open_ended_writing | 0.0687 | 0.1012 | 0.0326 | 1.47 | 1.000 |

## Link to Haase et al.

Haase et al. argue that LLM evaluation based on a single generation conflates prompt effects with sampling variability. This pilot operationalizes that claim for prompt perturbation: first estimate within-prompt variability from repeated generations, then subtract that baseline from between-prompt drift. A perturbation should be treated as meaningful only when its between-version drift clearly exceeds the within-version noise baseline.