param(
    [string]$EnvPrefix = "",
    [string]$AssetRoot = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

if ([string]::IsNullOrWhiteSpace($EnvPrefix)) {
    $EnvPrefix = Join-Path $RepoRoot ".conda\mammal"
}

if ([string]::IsNullOrWhiteSpace($AssetRoot)) {
    $AssetRoot = "F:\00_AI\BIO_MODELS"
}

$env:BIO_MODELS_ROOT = $AssetRoot
$env:HF_HOME = Join-Path $AssetRoot "hf_cache"
$env:HF_HUB_CACHE = Join-Path $AssetRoot "hf_cache\hub"
$env:TRANSFORMERS_CACHE = Join-Path $AssetRoot "hf_cache\transformers"
$env:TORCH_HOME = Join-Path $AssetRoot "torch_cache"
$env:MAMMAL_MODELS_DIR = Join-Path $AssetRoot "models"
$env:MAMMAL_DATA_DIR = Join-Path $AssetRoot "data"
$env:CLEARML_OFFLINE_MODE = "1"

New-Item -ItemType Directory -Force `
    -Path $env:BIO_MODELS_ROOT, $env:HF_HOME, $env:HF_HUB_CACHE, $env:TRANSFORMERS_CACHE, $env:TORCH_HOME, $env:MAMMAL_MODELS_DIR, $env:MAMMAL_DATA_DIR `
    | Out-Null

if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    throw "conda was not found on PATH. Install Miniconda/Anaconda or open a Conda-enabled PowerShell."
}

(& conda "shell.powershell" "hook") | Out-String | Invoke-Expression
conda activate $EnvPrefix

Write-Host "Activated MAMMAL environment: $EnvPrefix"
Write-Host "Asset root: $env:BIO_MODELS_ROOT"
Write-Host "HF cache: $env:HF_HUB_CACHE"
Write-Host "Models dir: $env:MAMMAL_MODELS_DIR"
Write-Host "Data dir: $env:MAMMAL_DATA_DIR"
