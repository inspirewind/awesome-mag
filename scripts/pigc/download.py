#!/usr/bin/env python3
"""Download PIGC MAG assembly FASTA files from the CNSA manifest."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.cnsa_manifest import assembly_items_from_manifest
from lib.corpus_download import add_common_arguments, main_wrapper, run_manifest_workflow


SLUG = "pigc"
DATASET = "PIGC"
SIZE = "6,339 MAG bin FASTA files; total size not precomputed"
NOTE = "CNSA manifest filtered to MAG bin FASTA links only; experiment FASTQ and gene/protein catalog assembly records are skipped."
MANIFEST_URL = "https://ftp.cngb.org/pub/CNSA/data7/public_info/CNP0000824/data_download_links_CNP0000824_ftp.txt"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_arguments(parser, jobs=4, connections=2)
    parser.add_argument(
        "--ftp2",
        action="store_true",
        help="Use ftp2.cngb.org instead of ftp.cngb.org for assembly file URLs.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    items = assembly_items_from_manifest(
        manifest_url=MANIFEST_URL,
        output_dir=root / "downloads" / SLUG,
        alternate_ftp2=args.ftp2,
    )
    items = [item for item in items if "_bin_" in item.output.name]
    return run_manifest_workflow(
        root=root,
        slug=SLUG,
        dataset=DATASET,
        size=SIZE,
        items=items,
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
