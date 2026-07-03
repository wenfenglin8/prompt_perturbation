# Sample Noise Pilot Report

- Suite: `reference_four_task`
- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Samples per original/perturbed prompt: `3`
- Decoding: temperature `0.7`, top_p `0.9`

## Aggregate Result

- Average uncorrected single-sample drift: `0.2392`
- Average raw perturbation drift: `0.2253`
- Average sample-noise baseline: `0.0616`
- Average noise-corrected drift: `0.1637`
- Estimated share of raw drift explainable by sampling noise: `27.4%`

Interpretation: raw prompt-perturbation drift overstates the perturbation effect whenever the noise baseline is non-trivial. The noise-corrected value estimates the part of the observed drift that remains after accounting for ordinary repeated-generation variability.

## Per-Item Metrics

| case | task | uncorrected single drift | noise baseline | raw drift | corrected drift | SNR | bootstrap P(raw>noise) |
|---|---:|---:|---:|---:|---:|---:|---:|
| ref_squad_v2_01 | factual_qa | 0.5556 | 0.0840 | 0.5286 | 0.4446 | 6.29 | 1.000 |
| ref_math_01 | math_reasoning | 0.0483 | 0.0443 | 0.0450 | 0.0007 | 1.02 | 1.000 |
| ref_humaneval_01 | code_generation | 0.2516 | 0.0322 | 0.2246 | 0.1924 | 6.98 | 1.000 |
| ref_alpaca_01 | open_ended_writing | 0.1014 | 0.0860 | 0.1030 | 0.0170 | 1.20 | 1.000 |

## Link to Haase et al.

Haase et al. argue that LLM evaluation based on a single generation conflates prompt effects with sampling variability. This pilot operationalizes that claim for prompt perturbation: first estimate within-prompt variability from repeated generations, then subtract that baseline from between-prompt drift. A perturbation should be treated as meaningful only when its between-version drift clearly exceeds the within-version noise baseline.