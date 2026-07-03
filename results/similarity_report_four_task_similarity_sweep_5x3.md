# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `5`
- Samples per clean / perturbed prompt: `3`
- Perturbations: `character, word, sentence, semantic`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | character | 5 | 0.0000 | 0.0168 | 0.0168 | 0.0000 |
| factual_qa | SQuAD V2 | word | 5 | 0.0674 | 0.0090 | 0.0594 | 0.0504 |
| factual_qa | SQuAD V2 | sentence | 5 | 0.0003 | 0.0000 | 0.0003 | 0.0003 |
| factual_qa | SQuAD V2 | semantic | 5 | 0.0890 | 0.0235 | 0.1276 | 0.1042 |
| math_reasoning | MATH | character | 5 | 0.0466 | 0.0559 | 0.0557 | 0.0029 |
| math_reasoning | MATH | word | 5 | 0.3901 | 0.1239 | 0.3174 | 0.1934 |
| math_reasoning | MATH | sentence | 5 | 0.0622 | 0.0404 | 0.0594 | 0.0226 |
| math_reasoning | MATH | semantic | 5 | 0.0584 | 0.0474 | 0.0654 | 0.0188 |
| code_generation | HumanEval | character | 5 | 0.0352 | 0.0069 | 0.0408 | 0.0340 |
| code_generation | HumanEval | word | 5 | 0.1262 | 0.0167 | 0.1143 | 0.0976 |
| code_generation | HumanEval | sentence | 5 | 0.0106 | 0.0162 | 0.0157 | 0.0000 |
| code_generation | HumanEval | semantic | 5 | 0.1310 | 0.0121 | 0.1218 | 0.1097 |
| open_ended_writing | Alpaca | character | 5 | 0.1738 | 0.0799 | 0.1803 | 0.1013 |
| open_ended_writing | Alpaca | word | 5 | 0.1158 | 0.0694 | 0.1478 | 0.0786 |
| open_ended_writing | Alpaca | sentence | 5 | 0.1724 | 0.1054 | 0.1857 | 0.0804 |
| open_ended_writing | Alpaca | semantic | 5 | 0.1643 | 0.0962 | 0.1393 | 0.0433 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | semantic | 0.1042 | 0.1276 |
| factual_qa | 2 | word | 0.0504 | 0.0594 |
| factual_qa | 3 | sentence | 0.0003 | 0.0003 |
| factual_qa | 4 | character | 0.0000 | 0.0168 |
| math_reasoning | 1 | word | 0.1934 | 0.3174 |
| math_reasoning | 2 | sentence | 0.0226 | 0.0594 |
| math_reasoning | 3 | semantic | 0.0188 | 0.0654 |
| math_reasoning | 4 | character | 0.0029 | 0.0557 |
| code_generation | 1 | semantic | 0.1097 | 0.1218 |
| code_generation | 2 | word | 0.0976 | 0.1143 |
| code_generation | 3 | character | 0.0340 | 0.0408 |
| code_generation | 4 | sentence | 0.0000 | 0.0157 |
| open_ended_writing | 1 | character | 0.1013 | 0.1803 |
| open_ended_writing | 2 | sentence | 0.0804 | 0.1857 |
| open_ended_writing | 3 | word | 0.0786 | 0.1478 |
| open_ended_writing | 4 | semantic | 0.0433 | 0.1393 |