"""Download MAMMAL and related Hugging Face models into the shared asset cache."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from huggingface_hub import set_client_factory, snapshot_download
from huggingface_hub import constants as hf_constants

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ASSET_ROOT = Path(r"F:\00_AI\BIO_MODELS")
ASSET_ROOT = Path(os.environ.get("BIO_MODELS_ROOT", DEFAULT_ASSET_ROOT))
HF_HOME = Path(os.environ.get("HF_HOME", ASSET_ROOT / "hf_cache"))
HF_HUB_CACHE = Path(os.environ.get("HF_HUB_CACHE", HF_HOME / "hub"))
MODELS_DIR = Path(os.environ.get("MAMMAL_MODELS_DIR", ASSET_ROOT / "models"))

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


def configure_project_cache(asset_root: Path) -> None:
    global ASSET_ROOT, HF_HOME, HF_HUB_CACHE, MODELS_DIR

    ASSET_ROOT = asset_root
    HF_HOME = Path(os.environ.get("HF_HOME", ASSET_ROOT / "hf_cache"))
    HF_HUB_CACHE = Path(os.environ.get("HF_HUB_CACHE", HF_HOME / "hub"))
    MODELS_DIR = Path(os.environ.get("MAMMAL_MODELS_DIR", ASSET_ROOT / "models"))

    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    HF_HOME.mkdir(parents=True, exist_ok=True)
    HF_HUB_CACHE.mkdir(parents=True, exist_ok=True)
    (HF_HOME / "transformers").mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("BIO_MODELS_ROOT", str(ASSET_ROOT))
    os.environ["HF_HOME"] = str(HF_HOME)
    os.environ["HF_HUB_CACHE"] = str(HF_HUB_CACHE)
    os.environ.setdefault("TRANSFORMERS_CACHE", str(HF_HOME / "transformers"))
    os.environ.setdefault("TORCH_HOME", str(ASSET_ROOT / "torch_cache"))
    os.environ["MAMMAL_MODELS_DIR"] = str(MODELS_DIR)
    os.environ.setdefault("MAMMAL_DATA_DIR", str(ASSET_ROOT / "data"))


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


def download_snapshot(repo_id: str, *, local_files_only: bool) -> None:
    print(f"[snapshot] {repo_id}")
    snapshot_download(
        repo_id=repo_id,
        cache_dir=str(HF_HUB_CACHE),
        local_files_only=local_files_only,
    )


def disable_ssl_verification() -> None:
    import httpx

    set_client_factory(lambda: httpx.Client(follow_redirects=True, verify=False))


def disable_cache_symlinks() -> None:
    os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"
    hf_constants.HF_HUB_DISABLE_SYMLINKS = True


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
    parser.add_argument(
        "--asset-root",
        default=str(ASSET_ROOT),
        help="Shared asset root. Defaults to BIO_MODELS_ROOT or F:\\00_AI\\BIO_MODELS.",
    )
    parser.add_argument(
        "--validate-mammal-load",
        action="store_true",
        help="After snapshot download, try Mammal.from_pretrained and tokenizer loading for MAMMAL groups.",
    )
    parser.add_argument(
        "--disable-ssl-verification",
        action="store_true",
        help="Use only on machines whose Python CA store cannot verify Hugging Face TLS certificates.",
    )
    parser.add_argument(
        "--allow-cache-symlinks",
        action="store_true",
        help="Allow Hugging Face cache symlinks. On Windows this usually requires Developer Mode or Administrator rights.",
    )
    return parser.parse_args()


def validate_mammal_load(repo_id: str) -> None:
    from fuse.data.tokenizers.modular_tokenizer.op import ModularTokenizerOp

    from mammal.model import Mammal

    Mammal.from_pretrained(repo_id, cache_dir=str(HF_HUB_CACHE), local_files_only=True)
    ModularTokenizerOp.from_pretrained(repo_id, cache_dir=str(HF_HUB_CACHE))


def main() -> None:
    args = parse_args()
    configure_project_cache(Path(args.asset_root))
    if not args.allow_cache_symlinks:
        disable_cache_symlinks()
    if args.disable_ssl_verification:
        disable_ssl_verification()

    if args.all:
        groups = list(MODEL_GROUPS)
    else:
        groups = args.group or ["core"]

    for group, repo_id in selected_models(groups):
        download_snapshot(repo_id, local_files_only=args.local_files_only)
        if args.validate_mammal_load and group in MAMMAL_GROUPS:
            validate_mammal_load(repo_id)

    print(f"Done. Hugging Face cache: {HF_HUB_CACHE}")


if __name__ == "__main__":
    main()
