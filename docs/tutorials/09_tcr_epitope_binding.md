# TCR-Epitope Binding

## Purpose

Predict binding between a T-cell receptor beta-chain sequence and an epitope sequence.

## Prerequisites

```powershell
. .\scripts\activate_project_env.ps1
python .\scripts\download_models.py --group finetuned
```

## Required models

- `ibm-research/biomed.omics.bl.sm.ma-ted-458m.tcr_epitope_bind`

## Required datasets

None for single-pair inference.

## Command

```powershell
python -m pytest mammal\examples\tests\test_tcr_epitope_binding_inference.py -s
```

## Expected output

The test prints a binding prediction for the example TCR beta-chain and epitope pair.

## Runtime notes

- The script defaults to CPU unless changed in code.
- TCR inputs should be amino acid sequences, not gene names.

## Troubleshooting

- Config mismatch warnings: the TCR loader allows config mismatch for backward compatibility.
- Slow first run: the fine-tuned model and tokenizer are being cached.
