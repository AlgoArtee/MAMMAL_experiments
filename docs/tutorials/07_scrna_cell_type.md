# scRNA Cell Type

## Purpose

Fine-tune or run inference for cell-type annotation from single-cell gene expression.

## Prerequisites

```powershell
. .\scripts\activate_project_env.ps1
python .\scripts\download_models.py --group core
```

## Required models

- `ibm-research/biomed.omics.bl.sm.ma-ted-458m`

## Required datasets

The default config expects:

```text
mammal/examples/scrna_cell_type/data/Zheng_68k_preprocessed.h5ad
```

Prefer storing generated source data under:

```text
data/scrna_cell_type
```

## Prepare data

Use the scripts in the example data folder:

```powershell
python mammal\examples\scrna_cell_type\data\Zheng68k_to_anndata.py
python mammal\examples\scrna_cell_type\data\process_h5ad_data.py
```

If the scripts write to the example folder, keep generated `.h5ad` files untracked.

## Fine-tune

```powershell
python mammal\main_finetune.py `
  --config-name config.yaml `
  --config-path mammal\examples\scrna_cell_type `
  root=. `
  name=models/fine_tuned/scrna_cell_type
```

## Inference

```powershell
python mammal\examples\scrna_cell_type\scRNA_infer.py `
  --model_path models/fine_tuned/scrna_cell_type/best_epoch.ckpt `
  --tokenizer_path models/fine_tuned/scrna_cell_type/tokenizer `
  --data_path mammal\examples\scrna_cell_type\data\Zheng_68k_preprocessed.h5ad
```

## Expected output

Inference prints predicted cell-type labels for processed cells.

## Runtime notes

- The config uses ranked gene names and `cell-type` as the label column.
- Start with a small subset before full fine-tuning.

## Troubleshooting

- `h5ad` missing: run preprocessing or place the file at the configured path.
- Label errors: verify the `.obs` column named `cell-type` exists.
