# Four-Task Similarity Sweep

- Model: `gpt-4o-mini`
- Embedding model: `text-embedding-3-small`
- Cases per task: `10`
- Samples per clean / perturbed prompt: `3`
- Perturbations: `character, word, sentence, semantic`

## Grouped Drift

| task | dataset | perturbation | n | uncorrected single drift | noise baseline | raw drift | corrected drift |
|---|---|---|---:|---:|---:|---:|---:|
| factual_qa | SQuAD V2 | character | 10 | 0.0453 | 0.0094 | 0.0542 | 0.0473 |
| factual_qa | SQuAD V2 | word | 10 | 0.0891 | 0.0372 | 0.0747 | 0.0375 |
| factual_qa | SQuAD V2 | sentence | 10 | 0.0451 | 0.0346 | 0.0300 | 0.0000 |
| factual_qa | SQuAD V2 | semantic | 10 | 0.2145 | 0.0139 | 0.1926 | 0.1788 |
| math_reasoning | MATH | character | 10 | 0.0696 | 0.0571 | 0.0594 | 0.0065 |
| math_reasoning | MATH | word | 10 | 0.3969 | 0.1386 | 0.3528 | 0.2142 |
| math_reasoning | MATH | sentence | 10 | 0.0465 | 0.0514 | 0.0519 | 0.0042 |
| math_reasoning | MATH | semantic | 10 | 0.0636 | 0.0447 | 0.0517 | 0.0077 |
| code_generation | HumanEval | character | 10 | 0.0343 | 0.0422 | 0.0541 | 0.0124 |
| code_generation | HumanEval | word | 10 | 0.1159 | 0.0278 | 0.1211 | 0.0951 |
| code_generation | HumanEval | sentence | 10 | 0.0396 | 0.0267 | 0.0598 | 0.0370 |
| code_generation | HumanEval | semantic | 10 | 0.1205 | 0.0318 | 0.1271 | 0.0953 |
| open_ended_writing | Alpaca | character | 10 | 0.1579 | 0.1336 | 0.1528 | 0.0308 |
| open_ended_writing | Alpaca | word | 10 | 0.1407 | 0.1049 | 0.1390 | 0.0408 |
| open_ended_writing | Alpaca | sentence | 10 | 0.1547 | 0.0845 | 0.1636 | 0.0793 |
| open_ended_writing | Alpaca | semantic | 10 | 0.0988 | 0.1151 | 0.1422 | 0.0274 |

## Corrected Sensitivity Ranking

| task | rank | perturbation | corrected drift | raw drift |
|---|---:|---|---:|---:|
| factual_qa | 1 | semantic | 0.1788 | 0.1926 |
| factual_qa | 2 | character | 0.0473 | 0.0542 |
| factual_qa | 3 | word | 0.0375 | 0.0747 |
| factual_qa | 4 | sentence | 0.0000 | 0.0300 |
| math_reasoning | 1 | word | 0.2142 | 0.3528 |
| math_reasoning | 2 | semantic | 0.0077 | 0.0517 |
| math_reasoning | 3 | character | 0.0065 | 0.0594 |
| math_reasoning | 4 | sentence | 0.0042 | 0.0519 |
| code_generation | 1 | semantic | 0.0953 | 0.1271 |
| code_generation | 2 | word | 0.0951 | 0.1211 |
| code_generation | 3 | sentence | 0.0370 | 0.0598 |
| code_generation | 4 | character | 0.0124 | 0.0541 |
| open_ended_writing | 1 | sentence | 0.0793 | 0.1636 |
| open_ended_writing | 2 | word | 0.0408 | 0.1390 |
| open_ended_writing | 3 | character | 0.0308 | 0.1528 |
| open_ended_writing | 4 | semantic | 0.0274 | 0.1422 |