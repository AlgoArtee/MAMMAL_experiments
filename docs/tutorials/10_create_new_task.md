# Create a New MAMMAL Task

## Purpose

Convert the advanced notebook into a command-line implementation checklist for a custom task.

## Prerequisites

```powershell
. .\scripts\activate_project_env.ps1
python .\scripts\download_models.py --group core
```

## Required models

- `ibm/biomed.omics.bl.sm.ma-ted-458m`

## Required datasets

Use your own dataset under:

```text
data/custom_task
```

For a first implementation, mirror the protein solubility task.

## Implementation steps

1. Create a package under `mammal/examples/<task_name>/`.
2. Implement a `MammalTask` subclass with:
   - `data_module()`
   - `data_preprocessing()`
   - `process_model_output()`
3. Implement a Lightning data module in `pl_data_module.py`.
4. Add `config.yaml` with:
   - `task._target_`
   - tokenizer path
   - `model.pretrained_kwargs.pretrained_model_name_or_path`
   - checkpoint output under `models/fine_tuned/<task_name>`
5. Add `main_infer.py` for single-sample inference.
6. Add at least one smoke test under `mammal/examples/tests/`.

## Dry-run command

```powershell
python mammal\main_finetune.py `
  --config-name config.yaml `
  --config-path mammal\examples\<task_name> `
  trainer.limit_train_batches=4 `
  trainer.limit_val_batches=4 `
  trainer.max_epochs=1
```

## Expected output

The dry run creates a small training output folder and reaches validation without data or tokenization errors.

## Runtime notes

- Use structured prompts, not free-form natural language prompts.
- Save tokenizer and config next to checkpoints so inference can reload them.

## Troubleshooting

- Token decode errors: inspect `process_model_output()` first.
- Batch collation errors: verify all token and attention-mask keys from `mammal.keys`.
