"""Download datasets used by the project examples into the shared asset root."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

DEFAULT_ASSET_ROOT = Path(r"F:\00_AI\BIO_MODELS")
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_GROUPS = {
    "solubility",
    "carcinogenicity",
    "dti",
    "gdsc",
    "zheng68k",
    "mainframe",
}

SOLUBILITY_URL = "https://zenodo.org/api/records/1162886/files-archive"
ZHENG68K_MATRIX_URL = (
    "https://cf.10xgenomics.com/samples/cell-exp/1.1.0/"
    "fresh_68k_pbmc_donor_a/fresh_68k_pbmc_donor_a_filtered_gene_bc_matrices.tar.gz"
)
ZHENG68K_LABELS_URL = (
    "https://raw.githubusercontent.com/scverse/scanpy_usage/refs/heads/master/"
    "170503_zheng17/data/zheng17_bulk_lables.txt"
)


def download_file(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.stat().st_size > 0:
        print(f"exists: {destination}")
        return
    print(f"download: {url}")
    urllib.request.urlretrieve(url, destination)
    print(f"saved: {destination}")


def download_solubility(data_root: Path) -> None:
    target = data_root / "protein_solubility"
    raw_data_path = target / "sameerkhurana10-DSOL_rv0.2-20562ad" / "data"
    if raw_data_path.exists():
        print(f"exists: {raw_data_path}")
        return
    archive = target / "1162886.zip"
    download_file(SOLUBILITY_URL, archive)
    shutil.unpack_archive(archive, extract_dir=target)
    inner = target / "sameerkhurana10" / "DSOL_rv0.2-v0.3.zip"
    shutil.unpack_archive(inner, extract_dir=target)
    print(f"ready: {raw_data_path}")


def copy_carcinogenicity(data_root: Path) -> None:
    target = data_root / "carcinogenicity"
    target.mkdir(parents=True, exist_ok=True)
    src = (
        PROJECT_ROOT
        / "mammal"
        / "examples"
        / "carcinogenicity"
        / "data"
        / "carcinogens_lagunin.tab"
    )
    dst = target / src.name
    shutil.copy2(src, dst)
    print(f"copied: {dst}")


def download_dti(data_root: Path) -> None:
    from tdc.multi_pred.dti import DTI

    target = data_root / "tdc"
    target.mkdir(parents=True, exist_ok=True)
    data = DTI(name="BindingDB_Kd", path=str(target))
    data.harmonize_affinities(mode="max_affinity")
    data.convert_to_log(form="binding")
    split = data.get_split(method="cold_split", column_name=["Drug", "Target"])
    out = data_root / "dti_bindingdb_kd"
    out.mkdir(parents=True, exist_ok=True)
    for split_name, df in split.items():
        df.to_csv(out / f"{split_name}.csv", index=False)
    print(f"ready: {out}")


def download_gdsc(data_root: Path) -> None:
    from tdc.multi_pred import DrugRes

    target = data_root / "tdc"
    target.mkdir(parents=True, exist_ok=True)
    out = data_root / "cell_line_drug_response"
    out.mkdir(parents=True, exist_ok=True)
    for name in ["GDSC1", "GDSC2"]:
        data = DrugRes(name=name, path=str(target))
        split = data.get_split()
        dataset_out = out / name
        dataset_out.mkdir(parents=True, exist_ok=True)
        for split_name, df in split.items():
            df.to_pickle(dataset_out / f"{split_name}.pkl")
        genes = list(data.get_gene_symbols())
        (dataset_out / "gene_symbols.txt").write_text("\n".join(genes), encoding="utf-8")
        print(f"ready: {dataset_out}")


def download_zheng68k(data_root: Path, *, process: bool) -> None:
    target = data_root / "scrna_cell_type"
    target.mkdir(parents=True, exist_ok=True)
    matrix_archive = target / "fresh_68k_pbmc_donor_a_filtered_gene_bc_matrices.tar.gz"
    labels = target / "zheng17_bulk_lables.txt"
    download_file(ZHENG68K_MATRIX_URL, matrix_archive)
    download_file(ZHENG68K_LABELS_URL, labels)

    if not process:
        print(f"raw ready: {target}")
        return

    raw_h5ad = target / "Zheng_68k.h5ad"
    processed_h5ad = target / "Zheng_68k_preprocessed.h5ad"
    subprocess.run(
        [
            sys.executable,
            str(
                PROJECT_ROOT
                / "mammal"
                / "examples"
                / "scrna_cell_type"
                / "data"
                / "Zheng68k_to_anndata.py"
            ),
            "--data-dir",
            str(target),
            "--output-h5ad-file",
            str(raw_h5ad),
        ],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(
                PROJECT_ROOT
                / "mammal"
                / "examples"
                / "scrna_cell_type"
                / "data"
                / "process_h5ad_data.py"
            ),
            "--input-h5ad-file",
            str(raw_h5ad),
            "--output-h5ad-file",
            str(processed_h5ad),
        ],
        check=True,
    )
    print(f"ready: {processed_h5ad}")


def note_mainframe(data_root: Path) -> None:
    target = data_root / "mainframe" / "raw"
    target.mkdir(parents=True, exist_ok=True)
    readme = target / "README_MANUAL_DOWNLOAD.txt"
    readme.write_text(
        "\n".join(
            [
                "MAINFRAME datasets are published via https://www.aircheck.ai/datasets",
                "Open the 'Datasets for Hands-on' tab and place these files here:",
                "- DREAM_Challenge_1_TrainSet.parquet",
                "- DREAM_Target2035_Challenge_test_data.csv",
                "- PGK2_CDD.parquet",
                "- PGK2_Creative.parquet",
                "",
                "After placing the files, follow docs/tutorials/12_mainframe_mammal.md.",
            ]
        ),
        encoding="utf-8",
    )
    print(f"manual dataset note: {readme}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--group",
        action="append",
        choices=sorted(DATASET_GROUPS),
        help="Dataset group to download. Can be repeated. Defaults to all automatic groups.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Download all automatic datasets and create MAINFRAME manual-download note.",
    )
    parser.add_argument(
        "--asset-root",
        default=os.environ.get("BIO_MODELS_ROOT", str(DEFAULT_ASSET_ROOT)),
        help="Shared asset root. Defaults to BIO_MODELS_ROOT or F:\\00_AI\\BIO_MODELS.",
    )
    parser.add_argument(
        "--process-zheng68k",
        action="store_true",
        help="Build Zheng68k h5ad files after downloading raw files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    asset_root = Path(args.asset_root)
    data_root = Path(os.environ.get("MAMMAL_DATA_DIR", asset_root / "data"))
    data_root.mkdir(parents=True, exist_ok=True)

    groups = args.group or ["solubility", "carcinogenicity", "dti", "gdsc", "zheng68k"]
    if args.all:
        groups = ["solubility", "carcinogenicity", "dti", "gdsc", "zheng68k", "mainframe"]

    for group in groups:
        if group == "solubility":
            download_solubility(data_root)
        elif group == "carcinogenicity":
            copy_carcinogenicity(data_root)
        elif group == "dti":
            download_dti(data_root)
        elif group == "gdsc":
            download_gdsc(data_root)
        elif group == "zheng68k":
            download_zheng68k(data_root, process=args.process_zheng68k)
        elif group == "mainframe":
            note_mainframe(data_root)

    print(f"Done. Dataset root: {data_root}")


if __name__ == "__main__":
    main()
