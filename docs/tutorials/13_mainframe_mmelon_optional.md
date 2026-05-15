# MAINFRAME MMELON Optional

## Purpose

Run the optional MMELON workflows from the MAINFRAME tutorial folder. MMELON is external to the core MAMMAL package.

## Prerequisites

```powershell
. .\scripts\activate_project_env.ps1
python .\scripts\download_models.py --group mmelon
```

Install the external package as described in the notebook:

```powershell
python -m pip install git+https://github.com/jmorrone/biomed-multi-view.git
```

## Required models

- `ibm-research/biomed.sm.mv-te-84m`
- `michalozeryflato/biomed.sm.mv-te-84m.wdr91_asms`
- `michalozeryflato/biomed.sm.mv-te-84m.pgk2_del_cdd`

## Required datasets

Use the same processed MAINFRAME files from [MAINFRAME MAMMAL](12_mainframe_mammal.md).

## Run notebooks

Open:

```text
tutorials/MAINFRAME_2026/MMELON_finetuning.ipynb
tutorials/MAINFRAME_2026/MMELON_inference.ipynb
```

Use project paths:

```text
data/mainframe
models/fine_tuned/mainframe/mmelon
tutorial_runs/mainframe/mmelon
```

## Expected output

Fine-tuning writes MMELON checkpoints. Inference writes prediction CSVs compatible with the analysis tutorial.

## Runtime notes

- MMELON may require PyTorch Geometric packages pinned to the installed PyTorch/CUDA version.
- Keep this optional path separate from core MAMMAL validation.

## Troubleshooting

- PyG install errors: follow the wheel URL matching your Torch and CUDA versions.
- Import errors for `bmfm_sm`: reinstall `biomed-multi-view` in the active Conda env.
