# RQ2 Surface-Noise Dose-Response Reproduction

This folder contains the Python scripts needed to reproduce the RQ2 perturbation-strength experiment.

## Files

```text
rq2_perturbation_dose_response.py
reference_perturbations.py
promptrobust_reference_pdr_eval.py
four_task_similarity_sweep.py
rq2_semantic_correctness_analysis.py
```

## Dependencies

```powershell
pip install requests numpy datasets
```

## API Key

Set:

```powershell
$env:OPENAI_API_KEY="your_api_key"
```

Or place an `api.txt` file in this folder containing the API key.

## Dataset Requirement

The script expects local HuggingFace Arrow caches for:

```text
squad_v2
DigitalLearningGmbH/MATH-lighteval
openai/openai_humaneval
```

The current script reads fixed local cache paths under the user's HuggingFace cache directory.

## Reproduction Command

```powershell
python rq2_perturbation_dose_response.py --dataset-cases-per-task 2 --samples 3 --levels 0,1,2,4,8 --tasks factual_qa,math_reasoning,code_generation --sleep 0 --output-tag rq2_surface_noise_dose_response_2x3_cumulative --resume
```

Long-answer factual QA reproduction:

```powershell
python rq2_perturbation_dose_response.py --dataset-cases-per-task 5 --samples 3 --levels 0,1,2,4,8 --tasks long_factual_qa --sleep 0 --output-tag rq2_surface_noise_dose_response_longfact_5x3_cumulative --resume
```

Outputs are written to:

```text
results/
```
