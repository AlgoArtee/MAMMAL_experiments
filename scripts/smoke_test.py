"""Small local smoke test for the project-local MAMMAL environment."""

from __future__ import annotations

import importlib
import sys


def require(module_name: str) -> None:
    importlib.import_module(module_name)
    print(f"ok: import {module_name}")


def main() -> None:
    print(sys.version)
    for module_name in ["torch", "mammal", "fuse", "transformers"]:
        require(module_name)

    import torch

    print(f"torch_cuda_available={torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"torch_cuda_device={torch.cuda.get_device_name(0)}")


if __name__ == "__main__":
    main()
