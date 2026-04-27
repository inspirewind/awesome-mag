#!/usr/bin/env python3
"""List, inspect, and download public Microbiome Datahub files."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path


BASE_URL = "https://mdatahub.org"
BULK_ROOT = "http://palaeo.nig.ac.jp/Resources/MDatahub/2025/"
ZENODO_RECORD_API = "https://zenodo.org/api/records/18073262"


@dataclass(frozen=True)
class Asset:
    asset_id: str
    group: str
    filename: str
    url: str
    description: str
    size: str = ""
    caveat: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


BULK_ASSETS = [
    Asset(
        asset_id="all-mag-dna",
        group="bulk",
        filename="20250810AllMAG.fasta.gz",
        url=urllib.parse.urljoin(BULK_ROOT, "20250810AllMAG.fasta.gz"),
        description="All MAG contig DNA sequences for 218,653 MAGs.",
        size="146 GB",
    ),
    Asset(
        asset_id="all-mag-contig-map",
        group="bulk",
        filename="20250810AllMAG.rm.tsv.gz",
        url=urllib.parse.urljoin(BULK_ROOT, "20250810AllMAG.rm.tsv.gz"),
        description="Contig to MAG GCA ID mapping table.",
        size="287 MB",
    ),
    Asset(
        asset_id="all-protein",
        group="bulk",
        filename="AllMergedMDatahubProtein.faa.gz",
        url=urllib.parse.urljoin(BULK_ROOT, "AllMergedMDatahubProtein.faa.gz"),
        description="All predicted protein sequences for 454,799,231 proteins.",
        size="79 GB",
    ),
    Asset(
        asset_id="all-protein-map",
        group="bulk",
        filename="AllMergedMDatahubProtein.rm.tsv.gz",
        url=urllib.parse.urljoin(BULK_ROOT, "AllMergedMDatahubProtein.rm.tsv.gz"),
        description="Protein to MAG GCA ID mapping table.",
        size="7 GB",
    ),
    Asset(
        asset_id="cluster40-reps",
        group="bulk",
        filename="cluster40Res_rep_seq.fasta.gz",
        url=urllib.parse.urljoin(BULK_ROOT, "cluster40Res_rep_seq.fasta.gz"),
        description="LinClust 40 percent protein cluster representative sequences.",
        size="11 GB",
    ),
    Asset(
        asset_id="cluster90-reps",
        group="bulk",
        filename="clusterRes_rep_seq.fasta.gz",
        url=urllib.parse.urljoin(BULK_ROOT, "clusterRes_rep_seq.fasta.gz"),
        description="LinClust 90 percent protein cluster representative sequences.",
        size="33 GB",
    ),
]


ZENODO_ASSETS = [
    Asset(
        asset_id="ModuleListName.tsv",
        group="zenodo",
        filename="ModuleListName.tsv",
        url="https://zenodo.org/api/records/18073262/files/ModuleListName.tsv/content",
        description="KEGG module labels from the Microbiome Datahub MAG dataset.",
        size="29006",
    ),
    Asset(
        asset_id="MicrobiomeDatahub_MAGData_20251228.xlsx",
        group="zenodo",
        filename="MicrobiomeDatahub_MAGData_20251228.xlsx",
        url="https://zenodo.org/api/records/18073262/files/MicrobiomeDatahub_MAGData_20251228.xlsx/content",
        description="Main MAG metadata workbook.",
        size="44184875",
    ),
    Asset(
        asset_id="MicrobiomeDatahub_MAGBac2Feature_20250827.xlsx",
        group="zenodo",
        filename="MicrobiomeDatahub_MAGBac2Feature_20250827.xlsx",
        url="https://zenodo.org/api/records/18073262/files/MicrobiomeDatahub_MAGBac2Feature_20250827.xlsx/content",
        description="Bac2Feature phenotype prediction workbook.",
        size="31316179",
    ),
    Asset(
        asset_id="MicrobiomeDatahubMAGModuleComposition.tsv.gz",
        group="zenodo",
        filename="MicrobiomeDatahubMAGModuleComposition.tsv.gz",
        url="https://zenodo.org/api/records/18073262/files/MicrobiomeDatahubMAGModuleComposition.tsv.gz/content",
        description="KEGG module composition matrix inferred from MBGD ortholog composition.",
        size="11664667",
    ),
]


API_ASSETS = {
    "project-metadata": {
        "path": "/api/dl/project/metadata/{ids}",
        "filename": "project_metadata.tsv",
        "description": "BioProject metadata TSV.",
    },
    "genome-metadata": {
        "path": "/api/dl/genome/metadata/{ids}",
        "filename": "genome_metadata.tsv",
        "description": "Genome metadata TSV.",
        "caveat": "Documented examples returned HTTP 500 during curation on 2026-04-25.",
    },
    "sequence-genome": {
        "path": "/api/dl/sequence/genome/{ids}",
        "filename": "sequence_genome.zip",
        "description": "Genome sequence ZIP.",
    },
    "sequence-cds": {
        "path": "/api/dl/sequence/cds/{ids}",
        "filename": "sequence_cds.zip",
        "description": "Protein-coding gene sequence ZIP.",
    },
    "sequence-protein": {
        "path": "/api/dl/sequence/protein/{ids}",
        "filename": "sequence_protein.zip",
        "description": "Protein sequence ZIP.",
    },
    "kegg-modules": {
        "path": "/api/genome/mbgd/{ids}",
        "filename": "kegg_modules.json",
        "description": "Per-genome KEGG module list JSON.",
    },
}


class DownloadError(RuntimeError):
    """Raised when a download cannot be completed."""


def normalize_ids(raw_ids: str) -> str:
    values = [value.strip() for value in raw_ids.split(",") if value.strip()]
    if not values:
        raise DownloadError("--ids must contain at least one identifier")
    return ",".join(values)


def api_asset(asset_id: str, raw_ids: str) -> Asset:
    spec = API_ASSETS[asset_id]
    ids = normalize_ids(raw_ids)
    encoded_ids = urllib.parse.quote(ids, safe=",._-")
    path = spec["path"].format(ids=encoded_ids)
    filename = str(spec["filename"])
    if asset_id == "kegg-modules":
        safe_ids = ids.replace(",", "_").replace("/", "_")
        filename = f"{safe_ids}.kegg_modules.json"
    return Asset(
        asset_id=asset_id,
        group="api",
        filename=filename,
        url=urllib.parse.urljoin(BASE_URL, path),
        description=str(spec["description"]),
        caveat=str(spec.get("caveat", "")),
    )


def fetch_zenodo_assets(record_api: str = ZENODO_RECORD_API) -> list[Asset]:
    try:
        with urllib.request.urlopen(record_api, timeout=60) as response:
            payload = json.load(response)
    except urllib.error.URLError as exc:
        raise DownloadError(f"Unable to fetch Zenodo record {record_api}: {exc}") from exc
    assets: list[Asset] = []
    for item in payload.get("files", []):
        key = item.get("key")
        links = item.get("links") or {}
        url = links.get("self")
        if not key or not url:
            continue
        assets.append(
            Asset(
                asset_id=key,
                group="zenodo",
                filename=key,
                url=url,
                description="Zenodo file from Microbiome Datahub MAG dataset.",
                size=str(item.get("size", "")),
            )
        )
    if not assets:
        raise DownloadError(f"No Zenodo files were found at {record_api}")
    return assets


def get_assets(
    group: str | None,
    include_zenodo: bool = True,
    refresh_zenodo: bool = False,
) -> list[Asset]:
    assets: list[Asset] = []
    if group in (None, "bulk"):
        assets.extend(BULK_ASSETS)
    if include_zenodo and group in (None, "zenodo"):
        if refresh_zenodo:
            assets.extend(fetch_zenodo_assets())
        else:
            assets.extend(ZENODO_ASSETS)
    return assets


def select_assets(args: argparse.Namespace) -> list[Asset]:
    if args.asset in API_ASSETS:
        if not args.ids:
            raise DownloadError(f"--ids is required for API asset '{args.asset}'")
        return [api_asset(args.asset, args.ids)]

    assets = get_assets(
        args.group,
        refresh_zenodo=getattr(args, "refresh_zenodo", False),
    )
    if args.asset != "all":
        assets = [asset for asset in assets if asset.asset_id == args.asset]
    if not assets:
        raise DownloadError("No matching assets were selected")
    return assets


def emit_assets(assets: list[Asset], *, json_output: bool, plain: bool) -> None:
    if json_output:
        print(json.dumps([asset.to_dict() for asset in assets], indent=2))
        return
    if plain:
        for asset in assets:
            print(asset.url)
        return
    print("asset_id\tgroup\tsize\tfilename\turl\tdescription")
    for asset in assets:
        print(
            "\t".join(
                [
                    asset.asset_id,
                    asset.group,
                    asset.size,
                    asset.filename,
                    asset.url,
                    asset.description,
                ]
            )
        )


def python_download(
    asset: Asset,
    destination: Path,
    *,
    resume: bool,
    no_progress: bool,
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    part = destination.with_name(destination.name + ".part")
    headers = {"User-Agent": "awesome-mag-mdatahub-helper/1.0"}
    mode = "wb"
    existing = 0
    if resume and part.exists():
        existing = part.stat().st_size
        if existing > 0:
            headers["Range"] = f"bytes={existing}-"
            mode = "ab"

    request = urllib.request.Request(asset.url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            if existing and response.status != 206:
                existing = 0
                mode = "wb"
            total = response.headers.get("Content-Length")
            expected = int(total) + existing if total and total.isdigit() else None
            if not no_progress:
                size_note = f" expected={expected}" if expected else ""
                print(f"START {asset.url} -> {destination}{size_note}", file=sys.stderr)
            done = existing
            last_report = time.monotonic()
            with part.open(mode) as handle:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    handle.write(chunk)
                    done += len(chunk)
                    now = time.monotonic()
                    if not no_progress and now - last_report >= 5:
                        print(f"PROGRESS {destination.name} {done} bytes", file=sys.stderr)
                        last_report = now
    except urllib.error.HTTPError as exc:
        raise DownloadError(f"HTTP {exc.code} while downloading {asset.url}") from exc
    except urllib.error.URLError as exc:
        raise DownloadError(f"Network error while downloading {asset.url}: {exc}") from exc

    part.replace(destination)


def external_download(
    asset: Asset,
    destination: Path,
    *,
    downloader: str,
    resume: bool,
) -> None:
    executable = shutil.which(downloader)
    if not executable:
        raise DownloadError(f"Downloader '{downloader}' was not found on PATH")

    destination.parent.mkdir(parents=True, exist_ok=True)
    if downloader == "curl":
        command = [executable, "-L", "-o", str(destination)]
        if resume:
            command.extend(["-C", "-"])
        command.append(asset.url)
    elif downloader == "wget":
        command = [executable, "-O", str(destination)]
        if resume:
            command.append("--continue")
        command.append(asset.url)
    elif downloader == "aria2c":
        command = [
            executable,
            "--out",
            destination.name,
            "--dir",
            str(destination.parent),
        ]
        if resume:
            command.append("--continue=true")
        command.append(asset.url)
    else:
        raise DownloadError(f"Unsupported downloader '{downloader}'")

    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise DownloadError(
            f"Downloader '{downloader}' failed with exit code {result.returncode}"
        )


def command_list(args: argparse.Namespace) -> int:
    assets = get_assets(
        None if args.group == "all" else args.group,
        refresh_zenodo=args.refresh_zenodo,
    )
    emit_assets(assets, json_output=args.json, plain=False)
    return 0


def command_url(args: argparse.Namespace) -> int:
    assets = select_assets(args)
    emit_assets(assets, json_output=args.json, plain=args.plain)
    return 0


def command_download(args: argparse.Namespace) -> int:
    if args.asset == "all" and args.group == "all":
        raise DownloadError(
            "Refusing to download every static asset by default; choose "
            "--group zenodo or --group bulk explicitly."
        )
    assets = select_assets(args)
    failures: list[str] = []
    output_dir = Path(args.output_dir)
    for asset in assets:
        destination = output_dir / asset.group / asset.filename
        if args.skip_existing and destination.exists() and destination.stat().st_size > 0:
            print(f"SKIP {destination}")
            continue
        try:
            if args.downloader == "python":
                python_download(
                    asset,
                    destination,
                    resume=args.resume,
                    no_progress=args.no_progress,
                )
            else:
                external_download(
                    asset,
                    destination,
                    downloader=args.downloader,
                    resume=args.resume,
                )
            print(f"OK {destination}")
        except DownloadError as exc:
            print(f"FAIL {asset.asset_id}: {exc}", file=sys.stderr)
            failures.append(asset.asset_id)
            if not args.continue_on_error:
                return 1
    return 1 if failures else 0


def add_selection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--group",
        choices=["all", "bulk", "zenodo"],
        default="all",
        help="Static asset group to select. Defaults to all.",
    )
    parser.add_argument(
        "--asset",
        default="all",
        help=(
            "Asset ID to select, or an API asset: "
            + ", ".join(sorted(API_ASSETS))
            + ". Defaults to all static assets in --group."
        ),
    )
    parser.add_argument(
        "--ids",
        help="Comma-separated BioProject or GCA identifiers for API assets.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List, inspect, and download public Microbiome Datahub files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List known bulk and Zenodo files.")
    list_parser.add_argument(
        "--group",
        choices=["all", "bulk", "zenodo"],
        default="all",
        help="Asset group to list. Defaults to all.",
    )
    list_parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    list_parser.add_argument(
        "--refresh-zenodo",
        action="store_true",
        help="Fetch the current Zenodo file list from the Zenodo API.",
    )
    list_parser.set_defaults(func=command_list)

    url_parser = subparsers.add_parser("url", help="Print selected URLs.")
    add_selection_args(url_parser)
    url_parser.add_argument("--plain", action="store_true", help="Print URLs only.")
    url_parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    url_parser.add_argument(
        "--refresh-zenodo",
        action="store_true",
        help="Fetch the current Zenodo file list from the Zenodo API.",
    )
    url_parser.set_defaults(func=command_url)

    download_parser = subparsers.add_parser("download", help="Download selected files.")
    add_selection_args(download_parser)
    download_parser.add_argument(
        "--output-dir",
        default="downloads/mdatahub",
        help="Directory for downloaded files. Defaults to downloads/mdatahub.",
    )
    download_parser.add_argument(
        "--downloader",
        choices=["python", "curl", "wget", "aria2c"],
        default="python",
        help="Downloader to use. Defaults to the built-in Python downloader.",
    )
    download_parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume partial downloads when supported.",
    )
    download_parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip files that already exist and are non-empty.",
    )
    download_parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue after a failed file.",
    )
    download_parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable progress messages for the built-in Python downloader.",
    )
    download_parser.add_argument(
        "--refresh-zenodo",
        action="store_true",
        help="Fetch the current Zenodo file list from the Zenodo API.",
    )
    download_parser.set_defaults(func=command_download)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except DownloadError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
