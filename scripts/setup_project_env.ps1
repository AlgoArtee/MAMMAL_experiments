param(
    [switch]$WithMcp,
    [switch]$CpuOnly,
    [switch]$DisableCondaSslVerification,
    [string]$AssetRoot = "F:\00_AI\BIO_MODELS",
    [string]$CondaExe = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$EnvPrefix = Join-Path $RepoRoot ".conda\mammal"
$RoopCondaExe = "F:\00_AI\roop\roop-unleashed-main\installer\installer_files\conda\Scripts\conda.exe"

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

Set-Location $RepoRoot
New-Item -ItemType Directory -Force -Path $AssetRoot | Out-Null

if ($DisableCondaSslVerification) {
    $env:CONDA_SSL_VERIFY = "false"
}

if (-not (Test-Path $EnvPrefix)) {
    Invoke-Checked { & $CondaExe create --prefix $EnvPrefix python=3.10 -y }
}

if ($CpuOnly) {
    Invoke-Checked { & $CondaExe install --prefix $EnvPrefix pytorch cpuonly -c pytorch -y }
} else {
    Invoke-Checked { & $CondaExe install --prefix $EnvPrefix pytorch pytorch-cuda=12.1 -c pytorch -c nvidia -y }
}

Invoke-Checked { & $CondaExe install --prefix $EnvPrefix -c conda-forge rdkit pyarrow scikit-learn jupyter ipykernel -y }
Invoke-Checked { & $CondaExe run --prefix $EnvPrefix python -m pip install --upgrade pip }
Invoke-Checked { & $CondaExe run --prefix $EnvPrefix python -m pip install -e ".[examples]" }
Invoke-Checked { & $CondaExe run --prefix $EnvPrefix python -m pip install PyTDC==0.4.1 }

if ($WithMcp) {
    Invoke-Checked { & $CondaExe run --prefix $EnvPrefix python -m pip install -e ".\mammal_mcp[dev]" }
}

Invoke-Checked { & $CondaExe run --prefix $EnvPrefix python -m ipykernel install --user --name mammal-project --display-name "MAMMAL project" }

Write-Host "Environment ready at $EnvPrefix"
Write-Host "Asset root ready at $AssetRoot"
Write-Host "Conda executable: $CondaExe"
if ($DisableCondaSslVerification) {
    Write-Host "Conda SSL verification was disabled for this setup process."
}
Write-Host "Activate with: . .\scripts\activate_project_env.ps1"
