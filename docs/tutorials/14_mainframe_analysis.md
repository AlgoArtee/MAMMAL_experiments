# MAINFRAME Analysis

## Purpose

Analyze prediction outputs from MAINFRAME MAMMAL and MMELON workflows.

## Prerequisites

```powershell
. .\scripts\activate_project_env.ps1
```

If RDKit was not installed during setup:

```powershell
conda install -c conda-forge rdkit -y
```

## Required models

None for analysis.

## Required datasets

Prediction CSVs from:

```text
F:\00_AI\BIO_MODELS\tutorial_runs\mainframe\mammal
F:\00_AI\BIO_MODELS\tutorial_runs\mainframe\mmelon
```

The notebook expects labels and prediction scores for ROC-AUC, PR-AUC, enrichment, and clustering.

## Run notebook

Open:

```text
tutorials/MAINFRAME_2026/data_and_predictions_analysis.ipynb
```

Use project-local paths instead of `/content` or `/proj/...`:

```text
DATA_DIR = r"F:\00_AI\BIO_MODELS\data\mainframe"
RUN_DIR = r"F:\00_AI\BIO_MODELS\tutorial_runs\mainframe"
```

## Expected output

The analysis produces classification metrics, enrichment-at-k tables, molecular clustering summaries, and comparison plots.

## Runtime notes

- Keep plots and generated tables under `F:\00_AI\BIO_MODELS\tutorial_runs\mainframe\analysis`.
- RDKit can be slow on large molecular sets; test with a subset first.

## Troubleshooting

- Missing columns: normalize prediction files to include `smiles`, `label`, and score columns.
- RDKit parse failures: inspect invalid SMILES and remove or correct them before clustering.
