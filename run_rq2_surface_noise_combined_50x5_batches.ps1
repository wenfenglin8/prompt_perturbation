$ErrorActionPreference = "Stop"

$tagBase = "rq2_surface_noise_combined_balanced_50x5_l0_2_4_8_16"
$python = (Get-Command python).Source
$root = Get-Location
$logDir = Join-Path $root "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

for ($batch = 1; $batch -le 5; $batch++) {
  $tag = "${tagBase}_batch${batch}of5"
  $outLog = Join-Path $logDir "${tag}.out.log"
  $errLog = Join-Path $logDir "${tag}.err.log"
  $argsList = @(
    "-u",
    "rq2_perturbation_dose_response.py",
    "--dataset-cases-per-task", "50",
    "--samples", "5",
    "--levels", "0,2,4,8,16",
    "--tasks", "factual_qa,long_factual_qa,math_reasoning,code_generation",
    "--long-factqa-set", "stress",
    "--perturbation-family", "surface_noise",
    "--sleep", "0",
    "--case-batch-count", "5",
    "--case-batch-index", "$batch",
    "--output-tag", $tag,
    "--resume"
  )
  $process = Start-Process `
    -FilePath $python `
    -ArgumentList $argsList `
    -WorkingDirectory $root `
    -RedirectStandardOutput $outLog `
    -RedirectStandardError $errLog `
    -WindowStyle Hidden `
    -PassThru
  Write-Host "Started $tag PID=$($process.Id)"
  Write-Host "  OUT: $outLog"
  Write-Host "  ERR: $errLog"
}

Write-Host ""
Write-Host "After all batches finish, run:"
Write-Host ".\merge_rq2_surface_noise_combined_50x5_batches.ps1"
