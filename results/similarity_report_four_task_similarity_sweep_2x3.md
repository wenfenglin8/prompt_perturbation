# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `2`
- Samples per clean / perturbed prompt: `3`
- Perturbations: `character, word, sentence, semantic`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | character | 2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | SQuAD V2 | word | 2 | 0.0000 | 0.0420 | 0.0840 | 0.0420 |
| factual_qa | SQuAD V2 | sentence | 2 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| factual_qa | SQuAD V2 | semantic | 2 | 0.2897 | 0.0025 | 0.2914 | 0.2889 |
| math_reasoning | MATH | character | 2 | 0.0241 | 0.0262 | 0.0301 | 0.0038 |
| math_reasoning | MATH | word | 2 | 0.3033 | 0.0236 | 0.2946 | 0.2711 |
| math_reasoning | MATH | sentence | 2 | 0.0237 | 0.0317 | 0.0308 | 0.0000 |
| math_reasoning | MATH | semantic | 2 | 0.0683 | 0.0384 | 0.0523 | 0.0139 |
| code_generation | HumanEval | character | 2 | 0.0410 | 0.0178 | 0.0168 | 0.0000 |
| code_generation | HumanEval | word | 2 | 0.1281 | 0.0196 | 0.1247 | 0.1051 |
| code_generation | HumanEval | sentence | 2 | 0.0979 | 0.0384 | 0.0691 | 0.0316 |
| code_generation | HumanEval | semantic | 2 | 0.1356 | 0.0029 | 0.1385 | 0.1357 |
| open_ended_writing | Alpaca | character | 2 | 0.0149 | 0.0372 | 0.0313 | 0.0000 |
| open_ended_writing | Alpaca | word | 2 | 0.0158 | 0.0255 | 0.0296 | 0.0041 |
| open_ended_writing | Alpaca | sentence | 2 | 0.0994 | 0.0477 | 0.0897 | 0.0419 |
| open_ended_writing | Alpaca | semantic | 2 | 0.0376 | 0.0234 | 0.0373 | 0.0139 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | semantic | 0.2889 | 0.2914 |
| factual_qa | 2 | word | 0.0420 | 0.0840 |
| factual_qa | 3 | character | 0.0000 | 0.0000 |
| factual_qa | 4 | sentence | 0.0000 | 0.0000 |
| math_reasoning | 1 | word | 0.2711 | 0.2946 |
| math_reasoning | 2 | semantic | 0.0139 | 0.0523 |
| math_reasoning | 3 | character | 0.0038 | 0.0301 |
| math_reasoning | 4 | sentence | 0.0000 | 0.0308 |
| code_generation | 1 | semantic | 0.1357 | 0.1385 |
| code_generation | 2 | word | 0.1051 | 0.1247 |
| code_generation | 3 | sentence | 0.0316 | 0.0691 |
| code_generation | 4 | character | 0.0000 | 0.0168 |
| open_ended_writing | 1 | sentence | 0.0419 | 0.0897 |
| open_ended_writing | 2 | semantic | 0.0139 | 0.0373 |
| open_ended_writing | 3 | word | 0.0041 | 0.0296 |
| open_ended_writing | 4 | character | 0.0000 | 0.0313 |