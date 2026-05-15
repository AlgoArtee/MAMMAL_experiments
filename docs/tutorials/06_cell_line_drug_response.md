# Cell-Line Drug Response

## Purpose

Predict IC50-like drug response from a drug SMILES and cell-line gene-expression profile.

## Prerequisites

```powershell
. .\scripts\activate_project_env.ps1
python .\scripts\download_models.py --group core
```

## Required models

- `ibm/biomed.omics.bl.sm.ma-ted-458m`

## Required datasets

Fine-tuning uses TDC GDSC datasets. The config selects:

```yaml
dataset_name: GDSC2
```

Use `data/cell_line_drug_response` for any persistent downloaded or custom files.

## Fine-tune

```powershell
python mammal\main_finetune.py `
  --config-name config.yaml `
  --config-path mammal\examples\cell_line_drug_response `
  root=. `
  name=models/fine_tuned/cell_line_drug_response
```

## Inference by GDSC cell-line name

```powershell
python mammal\examples\cell_line_drug_response\main_infer.py `
  --model_path models/fine_tuned/cell_line_drug_response/best_epoch.ckpt `
  --cell_line_name "A549" `
  --drug_smiles "CC(=O)NCCC1=CNc2c1cc(OC)cc2" `
  --drug_name "example_drug"
```

## Inference from custom h5ad

```powershell
python mammal\examples\cell_line_drug_response\main_infer.py `
  --model_path models/fine_tuned/cell_line_drug_response/best_epoch.ckpt `
  --cell_line_h5ad_file data/cell_line_drug_response/example_cell_line.h5ad `
  --drug_smiles "CC(=O)NCCC1=CNc2c1cc(OC)cc2" `
  --drug_name "example_drug"
```

## Evaluation

```powershell
python mammal\main_finetune.py `
  --config-name config.yaml `
  --config-path mammal\examples\cell_line_drug_response `
  evaluate=True `
  model.pretrained_kwargs.pretrained_model_name_or_path=models/fine_tuned/cell_line_drug_response/best_epoch.ckpt
```

## Expected output

Inference prints a scalar response prediction.

## Runtime notes

- `dataset_name` can be changed to `GDSC1`.
- Use `task.data_module_kwargs.limit_samples=100` for a quick local dry run.

## Troubleshooting

- Missing GDSC cell line: use the custom `.h5ad` path workflow.
- Memory pressure: reduce `batch_size` and dataloader `num_workers`.
