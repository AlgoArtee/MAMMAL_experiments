# Protein Solubility

## Purpose

Fine-tune or run inference for binary protein solubility prediction.

## Prerequisites

```powershell
. .\scripts\activate_project_env.ps1
python .\scripts\download_models.py --group core --group finetuned
```

## Required models

- Fine-tuning: `ibm/biomed.omics.bl.sm.ma-ted-458m`
- Direct inference: `ibm/biomed.omics.bl.sm.ma-ted-458m.protein_solubility`

## Required datasets

Fine-tuning downloads the solubility dataset into `example_solubility_data` by default. For local consistency, prefer overriding data paths into `data/protein_solubility` when extending the config.

## Fine-tune

```powershell
python mammal\main_finetune.py `
  --config-name config.yaml `
  --config-path mammal\examples\protein_solubility `
  root=. `
  name=models/fine_tuned/protein_solubility
```

## Inference with a fine-tuned checkpoint

```powershell
python mammal\examples\protein_solubility\main_infer.py `
  models/fine_tuned/protein_solubility `
  "MSSKLLLAGLDIERVLAEKNFYKEWDTWIIEAMNVGDEEVDRIKEFKEDEIFEEAK"
```

## Inference with the hosted fine-tuned model

```powershell
python mammal\examples\protein_solubility\main_infer.py `
  ibm/biomed.omics.bl.sm.ma-ted-458m.protein_solubility `
  "MSSKLLLAGLDIERVLAEKNFYKEWDTWIIEAMNVGDEEVDRIKEFKEDEIFEEAK"
```

## Evaluation

```powershell
python mammal\main_finetune.py `
  --config-name config.yaml `
  --config-path mammal\examples\protein_solubility `
  evaluate=True `
  model.pretrained_kwargs.pretrained_model_name_or_path=models/fine_tuned/protein_solubility/best_epoch.ckpt
```

## Expected output

Inference prints a class prediction and score. Training writes checkpoints under `models/fine_tuned/protein_solubility`.

## Runtime notes

- Full fine-tuning is GPU-heavy. Start by adding `trainer.limit_train_batches=8 trainer.limit_val_batches=8 trainer.max_epochs=1` for a dry run.

## Troubleshooting

- Dataset download fails: check network access to Zenodo.
- Missing checkpoint: verify `best_epoch.ckpt` exists under the selected output directory.
