# MAINFRAME MAMMAL

## Purpose

Run the MAINFRAME 2026 MAMMAL fine-tuning and inference workflows for WDR91 and PGK2 hit prediction.

## Prerequisites

```powershell
. .\scripts\activate_project_env.ps1
python .\scripts\download_models.py --group core --group mainframe-mammal
```

## Required models

- `ibm/biomed.omics.bl.sm.ma-ted-458m`
- `michalozeryflato/biomed.omics.bl.sm.ma-ted-458m.wdr91_asms`
- `michalozeryflato/biomed.omics.bl.sm.ma-ted-458m.pgk2_del_cdd`

## Required datasets

Download from `https://www.aircheck.ai/datasets`, tab `Datasets for Hands-on`.

Expected raw files:

```text
F:\00_AI\BIO_MODELS\data\mainframe\raw\DREAM_Challenge_1_TrainSet.parquet
F:\00_AI\BIO_MODELS\data\mainframe\raw\DREAM_Target2035_Challenge_test_data.csv
F:\00_AI\BIO_MODELS\data\mainframe\raw\PGK2_CDD.parquet
F:\00_AI\BIO_MODELS\data\mainframe\raw\PGK2_Creative.parquet
```

Expected processed files:

```text
F:\00_AI\BIO_MODELS\data\mainframe\wdr91\train.csv
F:\00_AI\BIO_MODELS\data\mainframe\wdr91\val.csv
F:\00_AI\BIO_MODELS\data\mainframe\wdr91\test.csv
F:\00_AI\BIO_MODELS\data\mainframe\wdr91_eval.csv
F:\00_AI\BIO_MODELS\data\mainframe\pgk2\train.csv
F:\00_AI\BIO_MODELS\data\mainframe\pgk2\val.csv
F:\00_AI\BIO_MODELS\data\mainframe\pgk2\test.csv
F:\00_AI\BIO_MODELS\data\mainframe\pgk2_creative.csv
```

Each processed file should have:

```text
smiles,label
```

## Run notebook as reference

Open:

```text
tutorials/MAINFRAME_2026/MAMMAL_finetune.ipynb
tutorials/MAINFRAME_2026/MAMMAL_inference.ipynb
```

Use the project paths above instead of `/content` or `/proj/...`.

## Suggested local output paths

```text
F:\00_AI\BIO_MODELS\models\fine_tuned\mainframe\mammal\wdr91
F:\00_AI\BIO_MODELS\models\fine_tuned\mainframe\mammal\pgk2
F:\00_AI\BIO_MODELS\tutorial_runs\mainframe\mammal
```

## Expected output

Fine-tuning writes checkpoints. Inference writes prediction CSVs for later analysis.

## Runtime notes

- Start with the notebook demo-size cells before full training.
- Keep raw Aircheck files under `F:\00_AI\BIO_MODELS\data\mainframe\raw`.

## Troubleshooting

- Column errors: normalize input files to `smiles,label`.
- Leakage risk: ensure PGK2 Creative compounds overlapping training are removed.
