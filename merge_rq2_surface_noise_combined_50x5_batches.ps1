$ErrorActionPreference = "Stop"

$tagBase = "rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16"
$metrics = @()
for ($batch = 1; $batch -le 5; $batch++) {
  $path = "results\${tagBase}_batch${batch}of5_metrics.csv"
  if (-not (Test-Path $path)) {
    throw "Missing metrics file: $path"
  }
  $metrics += $path
}

python plot_rq2_surface_noise_combined.py `
  --metrics $metrics `
  --tag $tagBase
