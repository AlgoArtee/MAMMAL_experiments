# MolNet Inference

## Purpose

Run hosted fine-tuned MolNet models for BBBP, ClinTox toxicity, and ClinTox FDA approval.

## Prerequisites

```powershell
. .\scripts\activate_project_env.ps1
python .\scripts\download_models.py --group molnet
```

## Required models

- `ibm/biomed.omics.bl.sm.ma-ted-458m.moleculenet_bbbp`
- `ibm/biomed.omics.bl.sm.ma-ted-458m.moleculenet_clintox_tox`
- `ibm/biomed.omics.bl.sm.ma-ted-458m.moleculenet_clintox_fda`

## Required datasets

None for single-SMILES inference.

## Commands

```powershell
python mammal\examples\molnet\molnet_infer.py BBBP "C(Cl)Cl" --device cpu
python mammal\examples\molnet\molnet_infer.py TOXICITY "C(Cl)Cl" --device cpu
python mammal\examples\molnet\molnet_infer.py FDA_APPR "C(Cl)Cl" --device cpu
```

## Expected output

Each command prints a binary prediction and score for the SMILES string.

## Runtime notes

- Valid task names are `BBBP`, `TOXICITY`, and `FDA_APPR`.
- Use `--device cuda` only after the GPU smoke test succeeds.

## Troubleshooting

- Invalid task name: use one of the three exact task names above.
- Model download repeats: verify `HF_HUB_CACHE` points to `.hf_cache/hub`.
