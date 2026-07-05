$ErrorActionPreference = "Stop"

python -u rq2_perturbation_dose_response.py `
  --dataset-cases-per-task 24 `
  --samples 5 `
  --levels 0,2,4,8,16 `
  --tasks factual_qa,long_factual_qa,math_reasoning,code_generation `
  --long-factqa-set stress `
  --perturbation-family surface_noise `
  --sleep 0 `
  --output-tag rq2_surface_noise_combined_balanced_24x5_l0_2_4_8_16 `
  --resume

python plot_rq2_surface_noise_combined.py `
  --metrics results\rq2_surface_noise_combined_balanced_24x5_l0_2_4_8_16_metrics.csv `
  --tag rq2_surface_noise_combined_balanced_24x5_l0_2_4_8_16
