# Model Cache and Downloads

## Purpose

Download model and tokenizer assets into the project-local Hugging Face cache.

## Prerequisites

Complete [environment setup](00_environment.md), then activate:

```powershell
. .\scripts\activate_project_env.ps1
```

## Cache layout

```text
.hf_cache/hub                 Hugging Face model snapshots
.hf_cache/transformers        Transformers cache
.torch_cache                  Torch cache
models/fine_tuned             Local fine-tune outputs
data                          Downloaded and processed datasets
```

## Download groups

Core MAMMAL:

```powershell
python .\scripts\download_models.py --group core
```

Fine-tuned inference models:

```powershell
python .\scripts\download_models.py --group finetuned
```

MolNet models:

```powershell
python .\scripts\download_models.py --group molnet
```

MAINFRAME MAMMAL models:

```powershell
python .\scripts\download_models.py --group mainframe-mammal
```

Optional MMELON models:

```powershell
python .\scripts\download_models.py --group mmelon
```

Everything:

```powershell
python .\scripts\download_models.py --all
```

## Offline verification

After a download, check that assets are available without network access:

```powershell
python .\scripts\download_models.py --group core --local-files-only
```

## Required models by tutorial

| Tutorial | Model group |
| --- | --- |
| Beginner PPI | `core` |
| Protein solubility | `core`, `finetuned` |
| Carcinogenicity | `core` |
| DTI BindingDB pKd | `core`, `finetuned` |
| Cell-line drug response | `core` |
| scRNA cell type | `core` |
| MolNet | `molnet` |
| TCR-epitope | `finetuned` |
| MCP server | `core`, `finetuned` as needed |
| MAINFRAME MAMMAL | `core`, `mainframe-mammal` |
| MAINFRAME MMELON | `mmelon` |

## Runtime notes

- The full set can require many GB of disk space.
- The downloader intentionally uses `.hf_cache/hub`.
- MCP now uses `HF_HUB_CACHE` too, so it does not create a second `mammal_mcp/model_cache`.

## Troubleshooting

- Certificate or network errors: rerun in a shell with working Hugging Face access.
- Private/gated model error: run `huggingface-cli login` in the active environment.
- Disk full: remove unused snapshots from `.hf_cache/hub`.
