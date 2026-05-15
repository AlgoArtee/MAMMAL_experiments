"""Download MAMMAL and related Hugging Face models into the project cache."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from huggingface_hub import snapshot_download

PROJECT_ROOT = Path(__file__).resolve().parents[1]
HF_HOME = PROJECT_ROOT / ".hf_cache"
HF_HUB_CACHE = HF_HOME / "hub"
MODELS_DIR = PROJECT_ROOT / "models"

MODEL_GROUPS: dict[str, list[str]] = {
    "core": [
        "ibm/biomed.omics.bl.sm.ma-ted-458m",
    ],
    "finetuned": [
        "ibm/biomed.omics.bl.sm.ma-ted-458m.protein_solubility",
        "ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd",
        "ibm-research/biomed.omics.bl.sm.ma-ted-458m.tcr_epitope_bind",
    ],
    "molnet": [
        "ibm/biomed.omics.bl.sm.ma-ted-458m.moleculenet_bbbp",
        "ibm/biomed.omics.bl.sm.ma-ted-458m.moleculenet_clintox_tox",
        "ibm/biomed.omics.bl.sm.ma-ted-458m.moleculenet_clintox_fda",
    ],
    "mainframe-mammal": [
        "michalozeryflato/biomed.omics.bl.sm.ma-ted-458m.wdr91_asms",
        "michalozeryflato/biomed.omics.bl.sm.ma-ted-458m.pgk2_del_cdd",
    ],
    "mmelon": [
        "ibm-research/biomed.sm.mv-te-84m",
        "michalozeryflato/biomed.sm.mv-te-84m.wdr91_asms",
        "michalozeryflato/biomed.sm.mv-te-84m.pgk2_del_cdd",
    ],
}

MAMMAL_GROUPS = {"core", "finetuned", "molnet", "mainframe-mammal"}


def configure_project_cache() -> None:
    HF_HOME.mkdir(parents=True, exist_ok=True)
    HF_HUB_CACHE.mkdir(parents=True, exist_ok=True)
    (HF_HOME / "transformers").mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("HF_HOME", str(HF_HOME))
    os.environ.setdefault("HF_HUB_CACHE", str(HF_HUB_CACHE))
    os.environ.setdefault("TRANSFORMERS_CACHE", str(HF_HOME / "transformers"))
    os.environ.setdefault("TORCH_HOME", str(PROJECT_ROOT / ".torch_cache"))
    os.environ.setdefault("MAMMAL_MODELS_DIR", str(MODELS_DIR))
    os.environ.setdefault("MAMMAL_DATA_DIR", str(PROJECT_ROOT / "data"))


def selected_models(groups: list[str]) -> list[tuple[str, str]]:
    unknown = sorted(set(groups) - set(MODEL_GROUPS))
    if unknown:
        raise ValueError(f"Unknown group(s): {', '.join(unknown)}")

    models: list[tuple[str, str]] = []
    seen: set[str] = set()
    for group in groups:
        for repo_id in MODEL_GROUPS[group]:
            if repo_id not in seen:
                models.append((group, repo_id))
                seen.add(repo_id)
    return models


def download_mammal_model(repo_id: str, *, local_files_only: bool) -> None:
    from fuse.data.tokenizers.modular_tokenizer.op import ModularTokenizerOp

    from mammal.model import Mammal

    print(f"[mammal] {repo_id}")
    Mammal.from_pretrained(
        repo_id,
        cache_dir=str(HF_HUB_CACHE),
        local_files_only=local_files_only,
    )
    ModularTokenizerOp.from_pretrained(
        repo_id,
        cache_dir=str(HF_HUB_CACHE),
    )


def download_snapshot(repo_id: str, *, local_files_only: bool) -> None:
    print(f"[snapshot] {repo_id}")
    snapshot_download(
        repo_id=repo_id,
        cache_dir=str(HF_HUB_CACHE),
        local_files_only=local_files_only,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--group",
        action="append",
        choices=sorted(MODEL_GROUPS),
        help="Model group to download. Can be repeated. Defaults to core.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Download every known group, including optional MMELON models.",
    )
    parser.add_argument(
        "--local-files-only",
        action="store_true",
        help="Verify models are already present without network access.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_project_cache()

    if args.all:
        groups = list(MODEL_GROUPS)
    else:
        groups = args.group or ["core"]

    for group, repo_id in selected_models(groups):
        if group in MAMMAL_GROUPS:
            download_mammal_model(repo_id, local_files_only=args.local_files_only)
        else:
            download_snapshot(repo_id, local_files_only=args.local_files_only)

    print(f"Done. Hugging Face cache: {HF_HUB_CACHE}")


if __name__ == "__main__":
    main()
