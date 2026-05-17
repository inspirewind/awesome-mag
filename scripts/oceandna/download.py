#!/usr/bin/env python3
"""Download OceanDNA MAG sequence payloads."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.corpus_download import DownloadError, DownloadItem, add_common_arguments, main_wrapper, run_manifest_workflow


SLUG = "oceandna"
DATASET = "OceanDNA MAG Catalog"
SIZE = "43,859 non-representative MAGs from Figshare plus 8,466 representative WGS FASTA files from ENA"
NOTE = (
    "Downloads Figshare article 15218454 for OceanDNA non-representative MAGs "
    "and ENA PRJDB11811 WGS FASTA files for species representatives."
)

NONREP_URL = "https://ndownloader.figshare.com/articles/15218454/versions/1"
NONREP_BYTES = 26_291_374_398
NONREP_OUTPUT = "non_representatives/oceandna_non_representatives_15218454.zip"

ENA_REPORT_URL = (
    "https://www.ebi.ac.uk/ena/portal/api/filereport?"
    "accession=PRJDB11811&result=wgs_set&"
    "fields=accession,wgs_set,set_fasta_ftp,description&format=tsv"
)
EXPECTED_REPRESENTATIVES = 8_466


def fetch_ena_rows() -> list[dict[str, str]]:
    request = Request(
        ENA_REPORT_URL,
        headers={"User-Agent": "awesome-mag/0.1 (+https://github.com/)"},
    )
    try:
        with urlopen(request, timeout=180) as response:
            text = response.read().decode("utf-8")
    except OSError as exc:
        raise DownloadError(f"Failed to fetch ENA WGS report for {SLUG}: {exc}") from exc

    rows = list(csv.DictReader(text.splitlines(), delimiter="\t"))
    if len(rows) != EXPECTED_REPRESENTATIVES:
        raise DownloadError(
            f"Unexpected ENA representative count: {len(rows)} != {EXPECTED_REPRESENTATIVES}"
        )

    missing = [row.get("accession", "") for row in rows if not row.get("set_fasta_ftp")]
    if missing:
        preview = ", ".join(missing[:10])
        raise DownloadError(f"{len(missing)} ENA rows are missing set_fasta_ftp values: {preview}")

    return rows


def normalize_ena_url(value: str) -> str:
    value = value.strip()
    if value.startswith(("http://", "https://", "ftp://")):
        return value
    if value.startswith("ftp.ebi.ac.uk/"):
        return "https://" + value
    raise DownloadError(f"Unexpected ENA FASTA URL format: {value}")


def representative_items(root: Path, rows: list[dict[str, str]]) -> list[DownloadItem]:
    output_dir = root / "downloads" / SLUG / "representatives"
    items: list[DownloadItem] = []
    for row in rows:
        url = normalize_ena_url(row["set_fasta_ftp"])
        name = Path(urlparse(url).path).name
        if not name:
            raise DownloadError(f"Could not determine output filename from ENA URL: {url}")
        items.append(DownloadItem(url=url, output=output_dir / name))
    return items


def write_representative_report(root: Path, rows: list[dict[str, str]]) -> None:
    report = root / "downloads" / SLUG / "representatives_manifest.tsv"
    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("accession", "wgs_set", "url", "output", "description"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            url = normalize_ena_url(row["set_fasta_ftp"])
            name = Path(urlparse(url).path).name
            writer.writerow(
                {
                    "accession": row.get("accession", ""),
                    "wgs_set": row.get("wgs_set", ""),
                    "url": url,
                    "output": f"representatives/{name}",
                    "description": row.get("description", ""),
                }
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_arguments(parser, jobs=8, connections=2)
    parser.add_argument(
        "--representatives-only",
        action="store_true",
        help="Download only the 8,466 ENA WGS representative FASTA files.",
    )
    parser.add_argument(
        "--nonrepresentatives-only",
        action="store_true",
        help="Download only the Figshare non-representative MAG ZIP.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.representatives_only and args.nonrepresentatives_only:
        raise DownloadError("Choose at most one of --representatives-only and --nonrepresentatives-only.")

    root = Path(args.root).expanduser().resolve()
    items: list[DownloadItem] = []

    if not args.representatives_only:
        items.append(
            DownloadItem(
                url=NONREP_URL,
                output=root / "downloads" / SLUG / NONREP_OUTPUT,
                bytes=NONREP_BYTES,
            )
        )

    if not args.nonrepresentatives_only:
        rows = fetch_ena_rows()
        write_representative_report(root, rows)
        items.extend(representative_items(root, rows))

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
