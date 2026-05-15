# Environment Setup

## Purpose

Create a reproducible Python environment stored inside this project folder, while model and dataset assets live in `F:\00_AI\BIO_MODELS`.

## Prerequisites

- Windows PowerShell.
- Conda available on `PATH`.
- NVIDIA driver if you want GPU acceleration.

## Conda vs venv

Use Conda as the default. This repo depends on PyTorch, CUDA packages, RDKit, `anndata`, TDC, and other compiled scientific packages. On Windows, Conda gives the most reliable binary compatibility.

Use `venv` only as a fallback for CPU-only basic inference. It is not the supported default for the full tutorial set.

## Create the project-local environment

From the repo root:

```powershell
.\scripts\setup_project_env.ps1
```

For CPU-only setup:

```powershell
.\scripts\setup_project_env.ps1 -CpuOnly
```

For MCP dependencies too:

```powershell
.\scripts\setup_project_env.ps1 -WithMcp
```

The environment is created at:

```text
.conda/mammal
```

The default shared asset root is:

```text
F:\00_AI\BIO_MODELS
```

## Activate the environment

Dot-source the activation script so it can update the current shell:

```powershell
. .\scripts\activate_project_env.ps1
```

This sets:

```text
HF_HOME=F:\00_AI\BIO_MODELS\hf_cache
HF_HUB_CACHE=F:\00_AI\BIO_MODELS\hf_cache\hub
TRANSFORMERS_CACHE=F:\00_AI\BIO_MODELS\hf_cache\transformers
TORCH_HOME=F:\00_AI\BIO_MODELS\torch_cache
MAMMAL_MODELS_DIR=F:\00_AI\BIO_MODELS\models
MAMMAL_DATA_DIR=F:\00_AI\BIO_MODELS\data
CLEARML_OFFLINE_MODE=1
```

## Validate

```powershell
python --version
python .\scripts\smoke_test.py
```

Expected success:

- Python reports `3.10.x`.
- Imports for `torch`, `mammal`, `fuse`, and `transformers` succeed.
- `torch_cuda_available=True` on the GPU setup.

## Runtime notes

- Do not commit `.conda/` or copied assets.
- Keep all examples and tutorials in this same activated shell.
- If Conda activation fails, open an Anaconda/Miniconda PowerShell and rerun the activation command.

## Troubleshooting

- `conda was not found`: install Miniconda or add Conda to `PATH`.
- `torch_cuda_available=False`: confirm `nvidia-smi` works, then rerun setup without `-CpuOnly`.
- `ModuleNotFoundError`: rerun `pip install -e ".[examples]"` inside the activated environment.
