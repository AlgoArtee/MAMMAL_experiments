# MCP Server

## Purpose

Run MAMMAL as an MCP server for agent integrations.

## Prerequisites

```powershell
.\scripts\setup_project_env.ps1 -WithMcp
. .\scripts\activate_project_env.ps1
```

## Required models

Depends on enabled `.env` flags:

- `PROTEIN_PROTEIN_INTERACTION=true`: core model
- `PROTEIN_SOLUBILITY=true`: protein solubility fine-tuned model
- `DRUG_TARGET_BINDING=true` or `DRUG_TARGET_BINDING_FASTA=true`: DTI fine-tuned model
- `TCR_EPITOPE_BINDING=true`: TCR fine-tuned model

## Required datasets

None for basic server startup. The UniProt lookup tool requires internet access.

## Configure

```powershell
Copy-Item mammal_mcp\.env.example mammal_mcp\.env
notepad mammal_mcp\.env
```

Enable only the tools you need. For a first run:

```text
PROTEIN_PROTEIN_INTERACTION=true
PROTEIN_SOLUBILITY=false
TCR_EPITOPE_BINDING=false
DRUG_TARGET_BINDING=false
DRUG_TARGET_BINDING_FASTA=false
STREAMABLE_HTTP=false
SSE=false
PORT=8001
```

## Pre-download enabled models

```powershell
python .\scripts\download_models.py --group core
```

Add `--group finetuned` if you enable fine-tuned tasks.

## Run STDIO server

```powershell
Set-Location mammal_mcp
python server.py
```

## Run Streamable HTTP

Set in `mammal_mcp/.env`:

```text
STREAMABLE_HTTP=true
PORT=8001
```

Then:

```powershell
Set-Location mammal_mcp
python server.py
```

## Expected output

Startup logs include `Assets loaded`. The server uses `F:\00_AI\BIO_MODELS\hf_cache\hub` through `HF_HUB_CACHE`, not `mammal_mcp/model_cache`.

## Runtime notes

- Do not enable every model unless you have enough RAM/VRAM.
- Restart the server after changing `.env`.

## Troubleshooting

- `Assets loaded` never appears: a model is still downloading or failed to download.
- Duplicate cache appears: verify you activated with `scripts/activate_project_env.ps1`.
