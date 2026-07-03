# Sample Noise Pilot Report

- Suite: `promptrobust`
- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Samples per original/perturbed prompt: `5`
- Decoding: temperature `0.7`, top_p `0.9`

## Aggregate Result

- Average raw perturbation drift: `0.0000`
- Average sample-noise baseline: `0.0000`
- Average noise-corrected drift: `0.0000`
- Estimated share of raw drift explainable by sampling noise: `113.6%`

Interpretation: raw prompt-perturbation drift overstates the perturbation effect whenever the noise baseline is non-trivial. The noise-corrected value estimates the part of the observed drift that remains after accounting for ordinary repeated-generation variability.

## Per-Item Metrics

| case | task | noise baseline | raw drift | corrected drift | SNR | bootstrap P(raw>noise) |
|---|---:|---:|---:|---:|---:|---:|
| promptrobust_sst2_01 | sst2_sentiment | 0.0000 | 0.0000 | 0.0000 | 0.88 | 0.429 |
| promptrobust_sst2_02 | sst2_sentiment | 0.0000 | 0.0000 | 0.0000 | 1.00 | 0.000 |

## Link to Haase et al.

Haase et al. argue that LLM evaluation based on a single generation conflates prompt effects with sampling variability. This pilot operationalizes that claim for prompt perturbation: first estimate within-prompt variability from repeated generations, then subtract that baseline from between-prompt drift. A perturbation should be treated as meaningful only when its between-version drift clearly exceeds the within-version noise baseline.