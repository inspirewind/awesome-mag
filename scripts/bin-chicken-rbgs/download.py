#!/usr/bin/env python3
"""Download Bin Chicken Rare Biosphere Genome MAG archives."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.corpus_download import DownloadItem, add_common_arguments, main_wrapper, run_manifest_workflow


SLUG = "bin-chicken-rbgs"
DATASET = "Bin Chicken Rare Biosphere Genomes"
SIZE = "33.8 GB + 33.5 GB"
NOTE = "Two MAG sequence archives from explicit Zenodo records; revised metadata is intentionally not downloaded."

FILES = (
    {
        "url": "https://zenodo.org/records/14890002/files/binchicken_RBGs_aquatic.tar.gz?download=1",
        "file": "binchicken_RBGs_aquatic.tar.gz",
        "bytes": 33823795732,
        "md5": "88a477f645d857c12d160d262e1ca383",
    },
    {
        "url": "https://zenodo.org/records/14915155/files/binchicken_RBGs_terrestrial_engineered_host.tar.gz?download=1",
        "file": "binchicken_RBGs_terrestrial_engineered_host.tar.gz",
        "bytes": 33499575163,
        "md5": "2fcd0dd7c4359e542ddeccf291f3102c",
    },
)


def build_items(root: Path) -> list[DownloadItem]:
    output_dir = root / "downloads" / SLUG
    return [
        DownloadItem(
            url=str(record["url"]),
            output=output_dir / str(record["file"]),
            md5=str(record["md5"]),
            bytes=int(record["bytes"]),
        )
        for record in FILES
    ]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_arguments(parser, jobs=2, connections=2, default_downloader="curl")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    return run_manifest_workflow(
        root=root,
        slug=SLUG,
        dataset=DATASET,
        size=SIZE,
        items=build_items(root),
        downloader=args.downloader,
        jobs=args.jobs,
        connections=args.connections,
        retries=args.retries,
        verify=args.verify_md5,
        note=NOTE,
        manifest_only=args.manifest_only,
    )


if __name__ == "__main__":
    raise SystemExit(main_wrapper(main))
