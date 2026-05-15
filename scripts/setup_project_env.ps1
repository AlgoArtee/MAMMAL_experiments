param(
    [switch]$WithMcp,
    [switch]$CpuOnly
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$EnvPrefix = Join-Path $RepoRoot ".conda\mammal"

if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    throw "conda was not found on PATH. Install Miniconda/Anaconda or open a Conda-enabled PowerShell."
}

Set-Location $RepoRoot

if (-not (Test-Path $EnvPrefix)) {
    conda create --prefix $EnvPrefix python=3.10 -y
}

if ($CpuOnly) {
    conda install --prefix $EnvPrefix pytorch cpuonly -c pytorch -y
} else {
    conda install --prefix $EnvPrefix pytorch pytorch-cuda=12.1 -c pytorch -c nvidia -y
}

conda install --prefix $EnvPrefix -c conda-forge rdkit pyarrow scikit-learn jupyter ipykernel -y
conda run --prefix $EnvPrefix python -m pip install --upgrade pip
conda run --prefix $EnvPrefix python -m pip install -e ".[examples]"

if ($WithMcp) {
    conda run --prefix $EnvPrefix python -m pip install -e ".\mammal_mcp[dev]"
}

conda run --prefix $EnvPrefix python -m ipykernel install --user --name mammal-project --display-name "MAMMAL project"

Write-Host "Environment ready at $EnvPrefix"
Write-Host "Activate with: . .\scripts\activate_project_env.ps1"
