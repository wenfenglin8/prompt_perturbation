# RQ2 Factual QA LLM Equivalence Correctness

This run replaces only the `factual_qa` correctness labels with an LLM equivalence judge.
Math and code correctness are unchanged from the original PDR run.

- Judge model: `gpt-4o-mini`
- Judged factual outputs: `300`
- Factual case-level comparisons: `50`
- Factual cases with repeated correctness change: `2`
- Factual cases with harmful correctness drop: `2`

The judge accepts semantically equivalent short answers and longer answers that contain the correct answer without contradiction.
This is a sensitivity analysis for the strict normalized exact-match factual correctness used in the original run.
