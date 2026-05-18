#!/usr/bin/env python3
"""Download QXLSG MAG genome FASTA files from the GWH assembly endpoint."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.corpus_download import DownloadError, DownloadItem, add_common_arguments, main_wrapper, run_manifest_workflow


SLUG = "qxlsg"
DATASET = "QXLSG"
SIZE = "5,866 per-MAG GWH genome FASTA files; total size not precomputed"
NOTE = "GWH BioProject PRJCA037687 assemblies filtered to DNA genome FASTA links; raw reads and Figshare/NODE companion routes are skipped."
GWH_API = "https://ngdc.cncb.ac.cn/gwh/gsa/ajax/getAssembliesListByBioProjectAccession/PRJCA037687"
EXPECTED_MAG_COUNT = 5_866
USER_AGENT = "awesome-mag/0.1 (+https://github.com/)"


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json, */*", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise DownloadError(f"GWH API request failed: {exc.code} {exc.reason}\n{body[:1000]}") from exc
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise DownloadError(f"GWH API request failed: {exc}") from exc


def extract_dna_link(record: dict) -> str:
    links = (
        record.get("downloadLinks", {})
        .get("downloadLinksList", [])
    )
    dna_links = [
        item.get("link", "").strip()
        for item in links
        if item.get("label", "").strip().upper() == "DNA" and item.get("link", "").strip()
    ]
    if not dna_links:
        dna_links = [item.get("link", "").strip() for item in links if item.get("link", "").strip()]
    if len(dna_links) != 1:
        accession = record.get("accession", "<unknown>")
        raise DownloadError(f"Expected exactly one DNA download link for {accession}; observed {len(dna_links)}")
    return dna_links[0]


def output_name(accession: str, url: str, seen: set[str]) -> str:
    leaf = Path(urlparse(url).path).name
    if not leaf:
        leaf = f"{accession}.genome.fasta.gz"
    if leaf not in seen:
        seen.add(leaf)
        return leaf
    stem = leaf
    suffix = ""
    for candidate_suffix in (".genome.fasta.gz", ".fasta.gz", ".fa.gz", ".fna.gz", ".gz"):
        if leaf.endswith(candidate_suffix):
            stem = leaf[: -len(candidate_suffix)]
            suffix = candidate_suffix
            break
    candidate = f"{stem}_{accession}{suffix}"
    if candidate in seen:
        raise DownloadError(f"Duplicate QXLSG output filename after accession disambiguation: {candidate}")
    seen.add(candidate)
    return candidate


def build_items(root: Path, records: list[dict]) -> tuple[list[DownloadItem], list[dict[str, str]]]:
    output_dir = root / "downloads" / SLUG / "assemblies"
    seen: set[str] = set()
    items: list[DownloadItem] = []
    rows: list[dict[str, str]] = []
    for record in records:
        accession = str(record.get("accession", "")).strip()
        if not accession:
            raise DownloadError("GWH assembly record is missing accession")
        url = extract_dna_link(record)
        name = output_name(accession, url, seen)
        output = output_dir / name
        items.append(DownloadItem(url=url, output=output))
        rows.append(
            {
                "accession": accession,
                "assembly_page": str(record.get("hyperlink", "") or ""),
                "url": url,
                "output": str(Path("assemblies") / name),
            }
        )
    return items, rows


def write_gwh_manifest(root: Path, rows: list[dict[str, str]]) -> None:
    path = root / "downloads" / SLUG / "gwh_assemblies_manifest.tsv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("accession", "assembly_page", "url", "output"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_arguments(parser, jobs=8, connections=2)
    parser.add_argument(
        "--expected-count",
        type=int,
        default=EXPECTED_MAG_COUNT,
        help="Expected number of GWH DNA FASTA links. Defaults to 5,866.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).expanduser().resolve()

    payload = fetch_json(GWH_API)
    records = payload.get("assembliesList", [])
    if not isinstance(records, list):
        raise DownloadError("GWH API response does not contain an assembliesList array.")
    response_count = payload.get("count")
    if response_count is not None and int(response_count) != len(records):
        raise DownloadError(f"GWH response count mismatch: count={response_count}, records={len(records)}")
    if args.expected_count and len(records) != args.expected_count:
        raise DownloadError(f"Unexpected QXLSG assembly count: {len(records)} != {args.expected_count}")

    items, rows = build_items(root, records)
    write_gwh_manifest(root, rows)
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
