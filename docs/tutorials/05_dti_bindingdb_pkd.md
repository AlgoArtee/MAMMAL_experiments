# DTI BindingDB pKd

## Purpose

Predict drug-target binding affinity using protein sequence plus drug SMILES.

## Prerequisites

```powershell
. .\scripts\activate_project_env.ps1
python .\scripts\download_models.py --group core --group finetuned
```

## Required models

- Fine-tuning: `ibm/biomed.omics.bl.sm.ma-ted-458m`
- Direct inference: `ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd`

## Required datasets

Fine-tuning uses TDC BindingDB DTI data and downloads through TDC. Store persistent data under:

```text
data/dti_bindingdb_kd
```

## Fine-tune

```powershell
python mammal\main_finetune.py `
  --config-name config.yaml `
  --config-path mammal\examples\dti_bindingdb_kd `
  root=. `
  name=models/fine_tuned/dti_bindingdb_kd
```

## Inference

Use the normalization constants from `config.yaml`:

```text
norm_y_mean=5.79384684128215
norm_y_std=1.33808027428196
```

```powershell
python mammal\examples\dti_bindingdb_kd\main_infer.py `
  models/fine_tuned/dti_bindingdb_kd `
  "NLMKRCTRGFRKLGKCTTLEEEKCKTLYPRGQCTCSDSKMNTHSCDCKSC" `
  "CC(=O)NCCC1=CNc2c1cc(OC)cc2" `
  5.79384684128215 `
  1.33808027428196
```

## Evaluation

```powershell
python mammal\main_finetune.py `
  --config-name config.yaml `
  --config-path mammal\examples\dti_bindingdb_kd `
  evaluate=True `
  model.pretrained_kwargs.pretrained_model_name_or_path=models/fine_tuned/dti_bindingdb_kd/best_epoch.ckpt
```

## Expected output

Inference prints a pKd-like scalar prediction after de-normalization.

## Runtime notes

- The default split is a Drug+Target cold split.
- Full training is large. Start with `trainer.limit_train_batches=8 trainer.limit_val_batches=8 trainer.max_epochs=1`.

## Troubleshooting

- TDC download errors: check internet access and TDC service availability.
- Very long targets: keep target length within the config maximum.
