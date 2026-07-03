# Sample Noise Pilot Report

- Suite: `reference_four_task`
- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Samples per original/perturbed prompt: `3`
- Decoding: temperature `0.7`, top_p `0.9`

## Aggregate Result

- Average uncorrected single-sample drift: `0.1613`
- Average raw perturbation drift: `0.1284`
- Average sample-noise baseline: `0.0461`
- Average noise-corrected drift: `0.0825`
- Estimated share of raw drift explainable by sampling noise: `35.9%`

Interpretation: raw prompt-perturbation drift overstates the perturbation effect whenever the noise baseline is non-trivial. The noise-corrected value estimates the part of the observed drift that remains after accounting for ordinary repeated-generation variability.

## Per-Item Metrics

| case | task | uncorrected single drift | noise baseline | raw drift | corrected drift | SNR | bootstrap P(raw>noise) |
|---|---:|---:|---:|---:|---:|---:|---:|
| ref_squad_v2_01 | factual_qa | 0.5557 | 0.0840 | 0.5016 | 0.4176 | 5.97 | 1.000 |
| ref_squad_v2_02 | factual_qa | 0.3273 | 0.1133 | 0.1141 | 0.0008 | 1.01 | 0.761 |
| ref_math_01 | math_reasoning | 0.0331 | 0.0533 | 0.0560 | 0.0028 | 1.05 | 1.000 |
| ref_math_02 | math_reasoning | 0.0533 | 0.0416 | 0.0400 | 0.0000 | 0.96 | 0.890 |
| ref_humaneval_01 | code_generation | 0.2434 | 0.0214 | 0.2218 | 0.2004 | 10.36 | 1.000 |
| ref_humaneval_02 | code_generation | 0.0262 | 0.0073 | 0.0290 | 0.0217 | 3.97 | 1.000 |
| ref_alpaca_01 | open_ended_writing | 0.0512 | 0.0477 | 0.0643 | 0.0165 | 1.35 | 1.000 |
| ref_alpaca_02 | open_ended_writing | 0.0000 | 0.0000 | 0.0000 | 0.0000 | inf | 0.000 |

## Link to Haase et al.

Haase et al. argue that LLM evaluation based on a single generation conflates prompt effects with sampling variability. This pilot operationalizes that claim for prompt perturbation: first estimate within-prompt variability from repeated generations, then subtract that baseline from between-prompt drift. A perturbation should be treated as meaningful only when its between-version drift clearly exceeds the within-version noise baseline.