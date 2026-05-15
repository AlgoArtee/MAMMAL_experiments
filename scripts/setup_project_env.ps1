param(
    [switch]$WithMcp,
    [switch]$CpuOnly,
    [string]$AssetRoot = "F:\00_AI\BIO_MODELS"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$EnvPrefix = Join-Path $RepoRoot ".conda\mammal"

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [scriptblock]$Command
    )
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE"
    }
}

if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    throw "conda was not found on PATH. Install Miniconda/Anaconda or open a Conda-enabled PowerShell."
}

Set-Location $RepoRoot
New-Item -ItemType Directory -Force -Path $AssetRoot | Out-Null

if (-not (Test-Path $EnvPrefix)) {
    Invoke-Checked { conda create --prefix $EnvPrefix python=3.10 -y }
}

if ($CpuOnly) {
    Invoke-Checked { conda install --prefix $EnvPrefix pytorch cpuonly -c pytorch -y }
} else {
    Invoke-Checked { conda install --prefix $EnvPrefix pytorch pytorch-cuda=12.1 -c pytorch -c nvidia -y }
}

Invoke-Checked { conda install --prefix $EnvPrefix -c conda-forge rdkit pyarrow scikit-learn jupyter ipykernel -y }
Invoke-Checked { conda run --prefix $EnvPrefix python -m pip install --upgrade pip }
Invoke-Checked { conda run --prefix $EnvPrefix python -m pip install -e ".[examples]" }

if ($WithMcp) {
    Invoke-Checked { conda run --prefix $EnvPrefix python -m pip install -e ".\mammal_mcp[dev]" }
}

Invoke-Checked { conda run --prefix $EnvPrefix python -m ipykernel install --user --name mammal-project --display-name "MAMMAL project" }

Write-Host "Environment ready at $EnvPrefix"
Write-Host "Asset root ready at $AssetRoot"
Write-Host "Activate with: . .\scripts\activate_project_env.ps1"
