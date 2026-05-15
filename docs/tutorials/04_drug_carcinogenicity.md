# Drug Carcinogenicity

## Purpose

Fine-tune or run inference for binary carcinogenicity prediction from a SMILES string.

## Prerequisites

```powershell
. .\scripts\activate_project_env.ps1
python .\scripts\download_models.py --group core
```

## Required models

- `ibm/biomed.omics.bl.sm.ma-ted-458m`

## Required datasets

The example includes:

```text
mammal/examples/carcinogenicity/data/carcinogens_lagunin.tab
```

Copy it into the shared dataset root with:

```powershell
python .\scripts\download_datasets.py --group carcinogenicity
```

## Fine-tune

```powershell
python mammal\main_finetune.py `
  --config-name config.yaml `
  --config-path mammal\examples\carcinogenicity `
  name=carcinogenicity
```

## Inference

```powershell
python mammal\examples\carcinogenicity\main_infer.py `
  F:\00_AI\BIO_MODELS\models\fine_tuned\carcinogenicity `
  "CC(CCl)OC(C)CCl"
```

## Evaluation

```powershell
python mammal\main_finetune.py `
  --config-name config.yaml `
  --config-path mammal\examples\carcinogenicity `
  evaluate=True `
  model.pretrained_kwargs.pretrained_model_name_or_path=F:\00_AI\BIO_MODELS\models\fine_tuned\carcinogenicity\best_epoch.ckpt
```

## Expected output

Inference prints whether the SMILES is predicted carcinogenic and a score.

## Runtime notes

- This config adds `<CARCINOGENICITY>` as a special token.
- Use a short dry run before a full fine-tune.

## Troubleshooting

- Token mismatch after fine-tune: use the tokenizer saved next to the checkpoint.
- Path issues: run commands from the repository root.
