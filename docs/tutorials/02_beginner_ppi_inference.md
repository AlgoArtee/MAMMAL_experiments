# Beginner PPI Inference

## Purpose

Run the simplest MAMMAL example: predict whether two protein sequences interact.

## Prerequisites

```powershell
. .\scripts\activate_project_env.ps1
python .\scripts\download_models.py --group core
```

## Required models

- `ibm/biomed.omics.bl.sm.ma-ted-458m`

## Required datasets

None.

## Command

Run the existing smoke-style test:

```powershell
python -m pytest mammal\examples\tests\test_simple_inference.py -s
```

## Expected output

The script prints a decoded generated output for the calmodulin/calcineurin protein pair.

## Runtime notes

- This is a sequence-to-sequence generation example using the base model.
- First run downloads the model if it is not already in `.hf_cache/hub`.

## Troubleshooting

- `CUDA out of memory`: run on CPU or close other GPU processes.
- `Couldn't find the checkpoint path nor download`: run the model downloader again.
