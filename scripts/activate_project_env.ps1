param(
    [string]$EnvPrefix = "",
    [string]$AssetRoot = "",
    [string]$CondaExe = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$RoopCondaExe = "F:\00_AI\roop\roop-unleashed-main\installer\installer_files\conda\Scripts\conda.exe"

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

if ([string]::IsNullOrWhiteSpace($CondaExe)) {
    $CondaCommand = Get-Command conda -ErrorAction SilentlyContinue
    if ($CondaCommand) {
        $CondaExe = $CondaCommand.Source
    } elseif (Test-Path $RoopCondaExe) {
        $CondaExe = $RoopCondaExe
    } else {
        throw "conda was not found on PATH and fallback conda was not found at $RoopCondaExe."
    }
} elseif (-not (Test-Path $CondaExe)) {
    throw "Conda executable was not found at $CondaExe."
}

(& $CondaExe "shell.powershell" "hook") | Out-String | Invoke-Expression
conda activate $EnvPrefix

Write-Host "Activated MAMMAL environment: $EnvPrefix"
Write-Host "Conda executable: $CondaExe"
Write-Host "Asset root: $env:BIO_MODELS_ROOT"
Write-Host "HF cache: $env:HF_HUB_CACHE"
Write-Host "Models dir: $env:MAMMAL_MODELS_DIR"
Write-Host "Data dir: $env:MAMMAL_DATA_DIR"
