# RQ1 PDR Reproduction Specification

This document specifies the RQ1 PDR experiment so that another large language model or implementation team can reproduce it from scratch.

## 1. Research Question

RQ1:

After applying a repeated-sampling / noise-baseline correction, is the ranking of perturbation types consistent across task types, or is the ranking task-dependent?

For the PDR experiment, use objective tasks only:

- factual question answering
- mathematical reasoning
- code generation

Exclude open-ended writing because PDR requires task correctness or pass/fail evaluation, and no PDR evaluator was implemented for open-ended writing.

## 2. Goal Of The PDR Experiment

The goal is to separate:

1. Clean baseline loss:

   The model's baseline error under the original clean prompt.

2. Perturbation-induced loss:

   The additional performance loss after applying a prompt perturbation.

3. Repeated-generation variability:

   The natural variability in correctness caused by sampling the same model multiple times with the same prompt.

The key result is the corrected PDR:

```text
corrected_PDR = perturbed_loss - clean_loss
              = clean_repeated_performance - perturbed_repeated_performance
```

Positive corrected PDR means the perturbation reduced performance. Negative corrected PDR means the perturbed prompt performed slightly better than the clean prompt in repeated sampling.

## 3. Model And Sampling Setup

Use the same model for all clean and perturbed generations.

Current experiment settings:

```text
model: gpt-4o-mini
temperature: 0.7
top_p: 0.9
samples_per_prompt_version: 5
dataset_cases_per_task: 50
tasks: factual_qa, math_reasoning, code_generation
perturbations: paraphrase, reordering, formatting, context_injection, surface_noise
```

For each task, perturbation, and case:

```text
generate 5 outputs from the clean prompt
generate 5 outputs from the perturbed prompt
```

Total metric rows:

```text
3 tasks * 5 perturbations * 50 cases = 750 case-level rows
```

Total generation rows:

```text
750 rows * 2 prompt versions * 5 samples = 7500 generation rows
```

## 4. Datasets

### 4.1 Factual QA

Dataset:

```text
SQuAD V2
```

Use 50 cases.

Each case should contain:

- passage / context
- question
- one or more reference answers

Clean prompt template:

```text
Read the passage and answer the question. Answer with the exact short answer only.

Passage: {passage}

Question: {question}
```

### 4.2 Math Reasoning

Dataset:

```text
MATH-style benchmark
```

The current run used:

```text
DigitalLearningGmbH/MATH-lighteval
```

Use 50 cases.

Each case should contain:

- problem
- reference solution
- extractable final answer, preferably boxed

Clean prompt template:

```text
Solve the mathematics problem. Put the final answer only on the last line.

Problem: {problem}
```

### 4.3 Code Generation

Dataset:

```text
HumanEval
```

Use 50 cases.

Each case should contain:

- function prompt
- entry point
- unit tests
- canonical solution, optional for reporting

Clean prompt template:

```text
Complete the following Python function. Return only valid Python code, with no explanation.

{humaneval_prompt}
```

## 5. Perturbation Types

Apply perturbations only to the instruction portion of the prompt. Do not alter the task content that determines the answer.

Do not perturb:

- factual passages
- factual questions
- math problem statements
- numbers
- formulas
- code signatures
- examples
- unit-test-relevant constraints

### 5.1 Paraphrase

Rewrite the instruction with equivalent meaning.

Example:

```text
Clean:
Solve the mathematics problem. Put the final answer only on the last line.

Perturbed:
Resolve the mathematics problem. Place the final answer exclusively on the last line.
```

### 5.2 Reordering

Change the order of instruction clauses without changing meaning.

Example:

```text
Clean:
Read the passage and answer the question. Answer with the exact short answer only.

Perturbed:
Answer with the exact short answer only after reading the passage and question.
```

### 5.3 Formatting

Change presentation format while preserving meaning.

Example:

```text
Question: Solve the mathematics problem. Put the final answer only on the last line.
Answer:
```

### 5.4 Context Injection

Add an irrelevant or logically harmless sentence to the instruction.

Example:

```text
Solve the mathematics problem. Put the final answer only on the last line and false is not true.
```

### 5.5 Surface Noise

Add minor spelling / typo / punctuation noise to the instruction.

Example:

```text
Solve the matheematics prolem. Put the fnial answer onky on the last line.
```

## 6. Generation Output Schema

Save one row per generated output.

Recommended fields:

```text
case_id
task
dataset
perturbation
version
sample_idx
prompt
output
reference_answer
correct
performance_score
```

Where:

```text
version = original or perturbed
sample_idx = 0,1,2,3,4
```

## 7. Task Evaluation Metrics

### 7.1 Factual QA Scoring

Use a continuous score in [0,1].

Recommended:

```text
score = max(answer containment, token F1)
```

Normalize text before scoring:

- lowercase
- remove punctuation
- normalize whitespace
- optionally remove articles

If any reference answer is fully contained in the model output after normalization, score can be 1.

### 7.2 Math Reasoning Scoring

Use binary correctness:

```text
correct = 1 if model final answer is equivalent to reference final answer
correct = 0 otherwise
```

Required robust answer extraction:

1. Extract the last complete `\boxed{...}` expression.
2. Support nested LaTeX, especially:

   ```text
   \boxed{\frac{11}{2}}
   ```

3. If no boxed answer exists, extract the answer after final-answer phrases:

   ```text
   final answer is:
   answer:
   the answer is:
   ```

4. If the phrase is followed by a newline, extract the next nonempty math/content line.
5. Strip display math wrappers:

   ```text
   \[ ... \]
   \( ... \)
   ```

6. Normalize equivalent LaTeX:

   ```text
   \frac and \dfrac
   \left and \right
   whitespace
   commas
   dollar signs
   ```

7. Compare numeric equivalents:

   ```text
   5.5 == 11/2
   40.00 == 40
   1/2 == .5
   ```

8. Handle common interval and symbolic equivalences:

   ```text
   [-2, 7] == x \in [-2,7]
   [0, \infty) == [0,∞)
   7(x-3)(x+3) == 7(x+3)(x-3)
   ```

Known issue from the original run:

The original evaluator had many false negatives because it failed to extract answers such as:

```text
The final answer is:
402
```

and failed to compare:

```text
5.5 vs \frac{11}{2}
```

The reproduced experiment must fix these issues.

### 7.3 Code Generation Scoring

Use HumanEval-style unit-test pass/fail:

```text
correct = 1 if generated code passes all tests
correct = 0 otherwise
```

Important evaluator requirement:

Preserve indentation inside Markdown code fences.

The original evaluator produced false negatives for outputs like:

```python
```python
    return len(string)
```
```

because code-fence stripping removed indentation and caused:

```text
SyntaxError: 'return' outside function
IndentationError
```

Robust code evaluation should try at least:

1. HumanEval prompt prefix + raw fenced-code body, preserving indentation.
2. HumanEval prompt prefix + normalized body indented by four spaces.
3. Completion-only code, for outputs that include the full function.

Evaluate in a sandboxed subprocess with timeout.

## 8. Case-Level PDR Metrics

For each case and perturbation:

Clean scores:

```text
c_1, c_2, c_3, c_4, c_5
```

Perturbed scores:

```text
p_1, p_2, p_3, p_4, p_5
```

Compute:

```text
clean_single_correct = c_1
perturbed_single_correct = p_1

clean_mean_correctness = mean(c_1,...,c_5)
perturbed_mean_correctness = mean(p_1,...,p_5)

uncorrected_pdr_loss = 1 - clean_mean_correctness
perturbed_pdr_loss = 1 - perturbed_mean_correctness

corrected_pdr = perturbed_pdr_loss - uncorrected_pdr_loss
              = clean_mean_correctness - perturbed_mean_correctness
```

Interpretation:

```text
corrected_pdr > 0: perturbation caused additional loss
corrected_pdr = 0: no average performance change
corrected_pdr < 0: perturbed prompt performed better in repeated sampling
```

## 9. Correctness Sample Noise

To estimate sample noise for PDR/correctness, use pairwise correctness variability:

```text
correctness_sample_noise = average_{i<j} |score_i - score_j|
```

For binary correctness with 5 samples:

```text
[1,1,1,1,1] -> 0.0
[1,1,1,1,0] -> 0.4
[1,1,1,0,0] -> 0.6
[1,1,0,0,0] -> 0.6
[1,0,0,0,0] -> 0.4
[0,0,0,0,0] -> 0.0
```

This is the PDR analogue of semantic-similarity sample noise.

Do not interpret sample noise as additional loss. It measures repeated-generation instability.

## 10. Aggregate Reports

Produce a metrics CSV with one row per case-perturbation pair:

```text
case_id
task
dataset
perturbation
clean_single_correct
perturbed_single_correct
clean_mean_correctness
perturbed_mean_correctness
uncorrected_pdr_loss
perturbed_pdr_loss
corrected_pdr
correctness_sample_noise
```

Produce aggregate summaries:

### 10.1 Overall

```text
average clean single-sample performance
average perturbed single-sample performance
average clean repeated performance
average perturbed repeated performance
dataset-level uncorrected PDR loss
dataset-level perturbed PDR loss
dataset-level corrected PDR
```

### 10.2 By Task

For each task:

```text
clean repeated performance
perturbed repeated performance
clean baseline loss
perturbation-induced loss
mean correctness sample noise
```

### 10.3 By Perturbation And Task

For each perturbation-task cell:

```text
clean repeated performance
perturbed repeated performance
corrected PDR
```

Use this table to answer RQ1.

## 11. RQ1 Decision Rule

Rank perturbation types within each task by corrected PDR, descending:

```text
larger positive corrected PDR = more harmful
near zero = neutral
negative = perturbed prompt performed better than clean prompt
```

Then compare rankings across tasks.

If rankings are similar across tasks, conclude:

```text
perturbation ranking is relatively consistent across tasks
```

If rankings differ, conclude:

```text
perturbation ranking is task-dependent
```

Current repaired result:

```text
factual_qa:
paraphrase > formatting > context injection > reordering ≈ surface noise

math_reasoning:
reordering > paraphrase > surface noise > formatting > context injection

code_generation:
paraphrase > context injection > formatting ≈ surface noise > reordering
```

Current conclusion:

```text
The ranking is task-dependent. Paraphrasing is consistently harmful, but the full ranking changes across tasks.
```

## 12. Recommended Visualizations

Create at least two figures:

### 12.1 Task-Dependent Ranking Heatmap

Rows:

```text
five perturbation types
```

Columns:

```text
three objective tasks
```

Cell value:

```text
corrected PDR in percentage points
```

Cell annotation:

```text
value and within-task rank
```

### 12.2 Baseline Loss vs Perturbation-Induced Loss

For each task, plot:

```text
clean baseline loss
perturbation-induced loss
```

This prevents readers from attributing all perturbed loss to perturbation.

## 13. Required Quality Checks

Before reporting final results:

1. Manually inspect math false negatives.
2. Verify that correct math answers are not marked wrong due to LaTeX or numeric equivalence.
3. Manually inspect code false negatives.
4. Confirm Markdown code fences and indentation are handled correctly.
5. Report old and repaired results separately if evaluator repair changed many scores.
6. Do not use the old uncorrected report if evaluator bugs are found.

## 14. Expected Output Files

Recommended output paths:

```text
results/rq1_recomputed/rq1_pdr_50x5_recomputed_generation_scores.csv
results/rq1_recomputed/rq1_pdr_50x5_recomputed_metrics.csv
results/rq1_recomputed/rq1_pdr_50x5_recomputed_summary.json
results/rq1_recomputed/rq1_pdr_50x5_recomputed_report.md
results/rq1_figures/rq1_pdr_recomputed_task_dependent_ranking.png
results/rq1_figures/rq1_pdr_recomputed_task_dependent_ranking.pdf
results/rq1_figures/rq1_pdr_recomputed_analysis_en.md
results/rq1_figures/rq1_pdr_recomputed_analysis_zh.md
```

## 15. Recommended Paper Wording

After evaluator repair, PDR should be described as follows:

```text
The repaired PDR analysis decomposes performance loss into clean-prompt baseline loss and perturbation-induced loss. Clean baseline loss measures the model's task error under repeated clean-prompt sampling, while corrected PDR measures the additional loss under perturbed prompts. Excluding open-ended writing, the perturbation ranking is task-dependent: paraphrasing is consistently harmful across objective tasks, but reordering, formatting, context injection, and surface noise change their relative positions across tasks.
```

Important caveat:

```text
PDR measures correctness loss, not semantic similarity directly. It should therefore be interpreted as task-performance evidence alongside semantic-similarity drift analysis.
```
