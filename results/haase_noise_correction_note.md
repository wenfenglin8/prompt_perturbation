# Noise-Corrected Prompt Perturbation Evaluation

Reference used: Jennifer Haase et al., "Within-Model vs Between-Prompt Variability in Large Language Models for Creative Tasks" (`reference/Within-Model vs Between-Prompt Variability in Large Language Models for.pdf`).

## Claim Tested

Haase et al. argue that single-generation LLM evaluations can conflate true prompt effects with within-model sampling variability. To test this idea in the current prompt-perturbation project, I ran a small pilot on two generation-heavy tasks:

- `code_01`: Python code generation
- `writing_01`: open-ended explanatory writing

Each original prompt and its perturbed version was sampled 3 times using `gpt-4o-mini` with `temperature=0.7` and `top_p=0.9`. Output drift was measured with `text-embedding-3-small` cosine distance.

## Definitions

- Within-prompt sample noise: average pairwise embedding distance among repeated outputs from the same prompt.
- Noise baseline: average of original-prompt noise and perturbed-prompt noise.
- Raw perturbation drift: average embedding distance between outputs from the original and perturbed prompts.
- Noise-corrected drift: `raw perturbation drift - noise baseline`.

## Pilot Result

| case | task | noise baseline | raw drift | noise-corrected drift | noise share of raw drift |
|---|---:|---:|---:|---:|---:|
| `code_01` | code generation | 0.0554 | 0.0884 | 0.0330 | 62.7% |
| `writing_01` | open-ended writing | 0.0571 | 0.0880 | 0.0308 | 64.9% |
| average | - | 0.0563 | 0.0882 | 0.0319 | 63.8% |

## Interpretation

The raw prompt-perturbation drift suggests an average output change of `0.0882`. However, repeated generations from the same prompt already vary by `0.0563` on average. After subtracting this sample-noise baseline, the estimated perturbation-specific drift falls to `0.0319`.

This supports Haase et al.'s methodological warning in the setting of prompt perturbation: if we evaluate only one output per prompt, much of the observed difference may be ordinary sampling variability rather than a true effect of prompt wording. In this pilot, about `63.8%` of the raw drift is explainable by sample noise. Therefore, noise correction gives a more accurate estimate of prompt perturbation impact by isolating the part of drift that exceeds normal within-prompt variability.

## Practical Conclusion for the Proposal

For the full experiment, each original and perturbed prompt should be sampled multiple times under fixed decoding parameters. A perturbation should be considered meaningfully destabilizing only when its between-prompt drift is larger than the within-prompt sample-noise baseline.
