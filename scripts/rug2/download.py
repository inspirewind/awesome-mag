#!/usr/bin/env python3
"""Download RUG2 binned metagenome assembly FASTA files from ENA."""

from __future__ import annotations

import argparse
import csv
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.corpus_download import (
    DownloadError,
    DownloadItem,
    add_common_arguments,
    main_wrapper,
    parse_int,
    run_manifest_workflow,
)


SLUG = "rug2"
DATASET = "RUG2 Rumen MAGs"
EXPECTED_FASTA_COUNT = 20_567
SIZE = "20,567 ENA binned metagenome FASTA files; superset of the 4,941 final RUGs"
NOTE = "ENA analysis report filtered to binned metagenome assembly FASTA links; this is the public sequence superset, while raw reads and DataShare protein archive are skipped."
ENA_BINS_TSV = (
    "https://www.ebi.ac.uk/ena/portal/api/search?"
    "result=analysis&"
    "query=study_accession=%22PRJEB31266%22%20AND%20analysis_type=%22SEQUENCE_ASSEMBLY%22%20AND%20assembly_type=%22binned%20metagenome%22&"
    "fields=study_accession,analysis_accession,sample_accession,analysis_title,analysis_type,assembly_type,generated_ftp,generated_bytes,generated_md5,submitted_ftp,submitted_bytes,submitted_md5&"
    "format=tsv"
)
USER_AGENT = "awesome-mag/0.1 (+https://github.com/)"
BROKEN_SUBMITTED_ANALYSES = {
    # ENA still reports these submitted_ftp paths, but the files currently
    # return "resource not found". The generated_ftp contig.fa.gz files are
    # present and have ENA-provided md5/byte metadata.
    "ERZ1039161",
    "ERZ1039343",
    "ERZ1039465",
    "ERZ1061177",
    "ERZ1063851",
}


def fetch_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={"Accept": "text/tab-separated-values, text/plain, */*", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise DownloadError(f"ENA request failed: {exc.code} {exc.reason}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise DownloadError(f"ENA request failed: {exc.reason}") from exc


def with_scheme(url: str) -> str:
    if url.startswith(("ftp://", "http://", "https://")):
        return url
    return f"ftp://{url}"


def split_field(value: str) -> list[str]:
    if not value:
        return []
    return [item for item in value.split(";") if item]


def unique_output_name(analysis_accession: str, url: str, seen: set[str]) -> str:
    base = url.rstrip("/").rsplit("/", 1)[-1]
    candidate = f"{analysis_accession}_{base}" if analysis_accession else base
    if candidate not in seen:
        seen.add(candidate)
        return candidate
    index = 2
    while True:
        duplicate = f"{analysis_accession}_{index}_{base}" if analysis_accession else f"{index}_{base}"
        if duplicate not in seen:
            seen.add(duplicate)
            return duplicate
        index += 1


def build_items(root: Path) -> list[DownloadItem]:
    text = fetch_text(ENA_BINS_TSV)
    reader = csv.DictReader(text.splitlines(), delimiter="\t")
    output_dir = root / "downloads" / SLUG / "assemblies"
    seen: set[str] = set()
    items: list[DownloadItem] = []

    for row in reader:
        if row.get("assembly_type", "").casefold() != "binned metagenome":
            continue
        analysis = row.get("analysis_accession", "")
        submitted_urls = split_field(row.get("submitted_ftp", ""))
        generated_urls = split_field(row.get("generated_ftp", ""))

        if analysis in BROKEN_SUBMITTED_ANALYSES:
            if not generated_urls:
                raise DownloadError(f"{analysis} needs generated_ftp fallback, but ENA did not provide one.")
            urls = generated_urls
            md5s = split_field(row.get("generated_md5", ""))
            byte_values = split_field(row.get("generated_bytes", ""))
            output_name_urls = submitted_urls or generated_urls
        else:
            urls = submitted_urls or generated_urls
            if submitted_urls:
                md5s = split_field(row.get("submitted_md5", ""))
                byte_values = split_field(row.get("submitted_bytes", ""))
            else:
                md5s = split_field(row.get("generated_md5", ""))
                byte_values = split_field(row.get("generated_bytes", ""))
            output_name_urls = urls

        for index, raw_url in enumerate(urls):
            url = with_scheme(raw_url)
            output_source_url = with_scheme(output_name_urls[index]) if index < len(output_name_urls) else url
            output_name = unique_output_name(analysis, output_source_url, seen)
            md5 = md5s[index] if index < len(md5s) else ""
            size = parse_int(byte_values[index]) if index < len(byte_values) else None
            items.append(
                DownloadItem(
                    url=url,
                    output=output_dir / output_name,
                    md5=md5,
                    bytes=size,
                )
            )

    if not items:
        raise DownloadError("No RUG2 binned metagenome FASTA URLs were found in the ENA report.")
    return items


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_arguments(parser, jobs=4, connections=2)
    parser.add_argument(
        "--expected-count",
        type=int,
        default=EXPECTED_FASTA_COUNT,
        help="Expected number of ENA binned metagenome FASTA links. Defaults to 20,567.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    items = build_items(root)
    if args.expected_count and len(items) != args.expected_count:
        raise DownloadError(f"Unexpected RUG2 FASTA URL count: {len(items)} != {args.expected_count}")
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
