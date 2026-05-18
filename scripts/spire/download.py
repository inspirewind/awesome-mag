#!/usr/bin/env python3
"""Resolve SPIRE download URLs without downloading files."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.corpus_download import (
    AlreadyRunning,
    DownloadError,
    DownloadItem,
    add_common_arguments,
    run_manifest_workflow,
)

DOWNLOADS_URL = "https://spire.embl.de/downloads"
SPIRE_SITE = "https://spire.embl.de"
SWIFTER_SPIRE_BASE = "https://swifter.embl.de/~fullam/spire/"
MARKER_GENES_BASE = "https://swifter.embl.de/~fullam/census_marker_genes/"
USER_AGENT = "awesome-mag/0.1 (+https://github.com/)"
DOWNLOAD_SLUG = "spire"
DOWNLOAD_DATASET = "SPIRE"
EXPECTED_MAG_ARCHIVE_COUNT = 714
DOWNLOAD_SIZE = "714 per-study MAG tar archives; total size not precomputed"
DOWNLOAD_NOTE = "SPIRE downloads page filtered to per-study *_MAGs.tar archives only."

STUDY_STATIC_ASSETS = ("assemblies", "mags", "fna", "faa")
STUDY_PROFILE_ASSETS = ("motus3-profile", "spire-motus-profile")
STUDY_ASSET_FIELDS = {
    "assemblies": ("assemblies_url", "assemblies_size", "assemblies_md5"),
    "mags": ("mags_url", "mags_size", "mags_md5"),
    "fna": ("fna_url", "fna_size", "fna_md5"),
    "faa": ("faa_url", "faa_size", "faa_md5"),
}

INDEX_SCOPES = {
    "root": (SWIFTER_SPIRE_BASE,),
    "metadata": (urllib.parse.urljoin(SWIFTER_SPIRE_BASE, "metadata/"),),
    "metadata-old": (urllib.parse.urljoin(SWIFTER_SPIRE_BASE, "metadata/old/"),),
    "study-compiled": (urllib.parse.urljoin(SWIFTER_SPIRE_BASE, "compiled/"),),
    "study-genes": (urllib.parse.urljoin(SWIFTER_SPIRE_BASE, "genes_per_study/"),),
    "representatives": (urllib.parse.urljoin(SWIFTER_SPIRE_BASE, "representatives/"),),
    "motus-db": (urllib.parse.urljoin(SWIFTER_SPIRE_BASE, "spire_motus/"),),
    "full-genes": (urllib.parse.urljoin(SWIFTER_SPIRE_BASE, "genes/"),),
    "marker-genes": (MARKER_GENES_BASE,),
}
INDEX_SCOPES["all-spire"] = (
    INDEX_SCOPES["root"]
    + INDEX_SCOPES["metadata"]
    + INDEX_SCOPES["metadata-old"]
    + INDEX_SCOPES["study-compiled"]
    + INDEX_SCOPES["study-genes"]
    + INDEX_SCOPES["representatives"]
    + INDEX_SCOPES["motus-db"]
    + INDEX_SCOPES["full-genes"]
)

STUDY_BLOCK_RE = re.compile(r'\n\s*"([^"]+)":\s*\{(.*?)\n\s*\},', re.S)
STUDY_FIELD_RE = re.compile(
    r'\n\s*([a-zA-Z0-9_]+):\s*(?:"([^"]*)"|(true|false))\s*,?'
)
INDEX_ROW_RE = re.compile(
    r'<a href="([^"]+)">.*?</a>\s*</td><td align="right">([^<]*)</td>'
    r'<td align="right">([^<]*)</td>',
    re.I,
)


class SourceError(Exception):
    """Raised when SPIRE URL enumeration fails."""


@dataclass(frozen=True)
class UrlRecord:
    category: str
    name: str
    asset: str
    url: str
    size: str = ""
    md5: str = ""
    modified: str = ""
    file_name: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "category": self.category,
            "name": self.name,
            "asset": self.asset,
            "url": self.url,
            "size": self.size,
            "md5": self.md5,
            "modified": self.modified,
            "file_name": self.output_name(),
        }

    def output_name(self) -> str:
        if self.file_name:
            return self.file_name
        path = urllib.parse.urlparse(self.url).path
        return urllib.parse.unquote(Path(path).name)


@dataclass(frozen=True)
class Study:
    name: str
    fields: dict[str, str]

    def to_dict(self) -> dict[str, str]:
        payload = {"study": self.name}
        payload.update(self.fields)
        return payload

    def static_record(self, asset: str) -> UrlRecord | None:
        url_field, size_field, md5_field = STUDY_ASSET_FIELDS[asset]
        url = self.fields.get(url_field, "")
        if not url:
            return None
        return UrlRecord(
            category="study",
            name=self.name,
            asset=asset,
            url=url,
            size=self.fields.get(size_field, ""),
            md5=self.fields.get(md5_field, ""),
        )

    def profile_record(self, asset: str) -> UrlRecord | None:
        if asset == "motus3-profile":
            if self.fields.get("has_motus3") != "true":
                return None
            rel = self.fields.get("motus3_url", "")
            suffix = "motus3_profile.tsv"
        elif asset == "spire-motus-profile":
            if self.fields.get("has_spire_motus") != "true":
                return None
            rel = self.fields.get("spire_motus_url", "")
            suffix = "spire_motus_profile.tsv"
        else:
            raise ValueError(asset)
        if not rel:
            return None
        return UrlRecord(
            category="study-profile",
            name=self.name,
            asset=asset,
            url=urllib.parse.urljoin(SPIRE_SITE, rel),
            file_name=f"{self.name}.{suffix}",
        )


def fetch_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "text/html, text/plain, */*",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(request) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SourceError(f"Request failed: {exc.code} {exc.reason}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise SourceError(f"Request failed: {exc.reason}") from exc


def load_downloads_html(path: str | None) -> str:
    if path:
        return Path(path).expanduser().read_text(encoding="utf-8")
    return fetch_text(DOWNLOADS_URL)


def parse_studies(html: str) -> list[Study]:
    match = re.search(r"var studyDownloadsData = \{(.*?)\n\};", html, re.S)
    if not match:
        raise SourceError("Unable to find studyDownloadsData in the SPIRE downloads page.")

    studies_by_name: dict[str, Study] = {}
    for block_match in STUDY_BLOCK_RE.finditer(match.group(1)):
        name = block_match.group(1)
        body = block_match.group(2)
        fields: dict[str, str] = {}
        for field_match in STUDY_FIELD_RE.finditer(body):
            value = field_match.group(2)
            if value is None:
                value = field_match.group(3) or ""
            fields[field_match.group(1)] = value

        study = Study(name=name, fields=fields)
        existing = studies_by_name.get(name)
        if existing is not None:
            if existing.fields != study.fields:
                print(f"WARNING duplicate SPIRE study differs: {name}", file=sys.stderr)
            continue
        studies_by_name[name] = study

    studies = sorted(studies_by_name.values(), key=lambda item: item.name.casefold())
    if not studies:
        raise SourceError("No SPIRE studies were parsed from the downloads page.")
    return studies


def select_studies(
    studies: list[Study],
    *,
    study_names: list[str] | None,
    contains: str | None,
    all_studies: bool,
) -> list[Study]:
    selected = studies if all_studies or not study_names else []
    if study_names:
        wanted = {name.casefold() for name in study_names}
        selected = [study for study in studies if study.name.casefold() in wanted]
    if contains:
        needle = contains.casefold()
        selected = [study for study in selected if needle in study.name.casefold()]
    return selected


def require_study_selector(args: argparse.Namespace) -> None:
    if args.all_studies or args.study or args.contains:
        return
    raise SystemExit("Select studies with --study, --contains, or --all-studies.")


def expand_study_assets(values: list[str]) -> list[str]:
    assets: list[str] = []
    for value in values:
        if value == "all-static":
            assets.extend(STUDY_STATIC_ASSETS)
        elif value == "all":
            assets.extend(STUDY_STATIC_ASSETS)
            assets.extend(STUDY_PROFILE_ASSETS)
        else:
            assets.append(value)

    deduped: list[str] = []
    seen: set[str] = set()
    for asset in assets:
        if asset in seen:
            continue
        seen.add(asset)
        deduped.append(asset)
    return deduped


def iter_study_url_records(
    studies: Iterable[Study],
    assets: Iterable[str],
    *,
    include_md5_sidecars: bool,
) -> Iterable[UrlRecord]:
    for study in studies:
        for asset in assets:
            if asset in STUDY_STATIC_ASSETS:
                record = study.static_record(asset)
                if record is None:
                    continue
                yield record
                if include_md5_sidecars and asset in ("fna", "faa"):
                    yield UrlRecord(
                        category="study-md5",
                        name=study.name,
                        asset=f"{asset}-md5",
                        url=f"{record.url}.md5",
                        file_name=f"{record.output_name()}.md5",
                    )
            elif asset in STUDY_PROFILE_ASSETS:
                record = study.profile_record(asset)
                if record is not None:
                    yield record
            else:
                raise ValueError(asset)


def print_studies(studies: list[Study], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps([study.to_dict() for study in studies], ensure_ascii=False, indent=2))
        return
    for study in studies:
        print(study.name)


def print_records(
    records: list[UrlRecord],
    *,
    as_json: bool,
    plain: bool,
    aria2: bool,
) -> None:
    if as_json:
        print(json.dumps([record.to_dict() for record in records], ensure_ascii=False, indent=2))
        return
    if aria2:
        for record in records:
            print(record.url)
            print(f"  out={record.output_name()}")
        return
    if plain:
        for record in records:
            print(record.url)
        return
    for record in records:
        parts = [record.name, record.asset]
        if record.size:
            parts.append(record.size)
        if record.md5:
            parts.append(f"MD5: {record.md5}")
        if record.modified:
            parts.append(f"modified: {record.modified}")
        parts.append(record.url)
        print(" | ".join(parts))


def parse_index_rows(base_url: str, html: str) -> list[UrlRecord]:
    records: list[UrlRecord] = []
    category = index_category(base_url)
    for match in INDEX_ROW_RE.finditer(html):
        href, modified, size = [value.strip() for value in match.groups()]
        if href.startswith("?C=") or href.startswith("/~fullam/") or href.endswith("/"):
            continue
        url = urllib.parse.urljoin(base_url, href)
        asset = "md5" if href.endswith(".md5") or ".md5_" in href else "file"
        records.append(
            UrlRecord(
                category=category,
                name=urllib.parse.unquote(href),
                asset=asset,
                url=url,
                size=size,
                modified=modified,
            )
        )
    return records


def index_category(base_url: str) -> str:
    if base_url == MARKER_GENES_BASE:
        return "marker-genes"
    relative = base_url.removeprefix(SWIFTER_SPIRE_BASE).strip("/")
    if not relative:
        return "root"
    return relative.replace("/", "-")


def iter_manifest_records(
    scope: str,
    *,
    include_md5_sidecars: bool,
) -> Iterable[UrlRecord]:
    for index_url in INDEX_SCOPES[scope]:
        records = parse_index_rows(index_url, fetch_text(index_url))
        for record in records:
            if record.asset == "md5" and not include_md5_sidecars:
                continue
            yield record


def command_list(args: argparse.Namespace) -> int:
    html = load_downloads_html(args.downloads_html)
    studies = parse_studies(html)
    matches = select_studies(
        studies,
        study_names=args.study,
        contains=args.contains,
        all_studies=True,
    )
    print_studies(matches, as_json=args.json)
    return 0


def command_url(args: argparse.Namespace) -> int:
    require_study_selector(args)
    html = load_downloads_html(args.downloads_html)
    studies = parse_studies(html)
    matches = select_studies(
        studies,
        study_names=args.study,
        contains=args.contains,
        all_studies=args.all_studies,
    )
    if not matches:
        raise SystemExit("No matching SPIRE studies found.")

    assets = expand_study_assets(args.asset or ["all-static"])
    records = list(
        iter_study_url_records(
            matches,
            assets,
            include_md5_sidecars=args.include_md5_sidecars,
        )
    )
    print_records(records, as_json=args.json, plain=args.plain, aria2=args.aria2)
    return 0


def command_manifest(args: argparse.Namespace) -> int:
    records = list(
        iter_manifest_records(
            args.scope,
            include_md5_sidecars=args.include_md5_sidecars,
        )
    )
    print_records(records, as_json=args.json, plain=args.plain, aria2=args.aria2)
    return 0


def records_to_download_items(records: list[UrlRecord], root: Path) -> list[DownloadItem]:
    output_dir = root / "downloads" / DOWNLOAD_SLUG / "mags"
    return [
        DownloadItem(
            url=record.url,
            output=output_dir / record.output_name(),
            md5=record.md5,
        )
        for record in records
    ]


def command_download(args: argparse.Namespace) -> int:
    html = load_downloads_html(args.downloads_html)
    studies = parse_studies(html)
    matches = select_studies(
        studies,
        study_names=args.study,
        contains=args.contains,
        all_studies=args.all_studies or (not args.study and not args.contains),
    )
    if not matches:
        raise SystemExit("No matching SPIRE studies found.")

    records = list(
        iter_study_url_records(
            matches,
            ["mags"],
            include_md5_sidecars=False,
        )
    )
    if not records:
        raise SystemExit("No SPIRE MAG archive URLs were found for the selected studies.")
    if args.expected_count and len(records) != args.expected_count:
        raise DownloadError(f"Unexpected SPIRE MAG archive URL count: {len(records)} != {args.expected_count}")

    root = Path(args.root).expanduser().resolve()
    return run_manifest_workflow(
        root=root,
        slug=DOWNLOAD_SLUG,
        dataset=DOWNLOAD_DATASET,
        size=DOWNLOAD_SIZE,
        items=records_to_download_items(records, root),
        downloader=args.downloader,
        jobs=args.jobs,
        connections=args.connections,
        retries=args.retries,
        verify=args.verify_md5,
        note=DOWNLOAD_NOTE,
        manifest_only=args.manifest_only,
    )


def add_study_selection_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--study",
        action="append",
        help="Exact SPIRE study name. Repeat to select multiple studies.",
    )
    parser.add_argument("--contains", help="Case-insensitive substring match on study name.")
    parser.add_argument(
        "--all-studies",
        action="store_true",
        help="Select all studies. Required for URL output without --study or --contains.",
    )


def add_output_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    parser.add_argument("--plain", action="store_true", help="Emit one URL per line.")
    parser.add_argument(
        "--aria2",
        action="store_true",
        help="Emit aria2 input format with an output filename for each URL.",
    )


def add_downloads_page_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--downloads-html",
        help="Read a cached SPIRE downloads HTML file instead of fetching the live page.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List SPIRE studies and print download URLs without downloading files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List SPIRE study names.")
    add_study_selection_arguments(list_parser)
    list_parser.set_defaults(all_studies=True)
    list_parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    add_downloads_page_argument(list_parser)
    list_parser.set_defaults(func=command_list)

    url_parser = subparsers.add_parser("url", help="Print SPIRE per-study URLs.")
    add_study_selection_arguments(url_parser)
    url_parser.add_argument(
        "--asset",
        action="append",
        choices=[
            "assemblies",
            "mags",
            "fna",
            "faa",
            "motus3-profile",
            "spire-motus-profile",
            "all-static",
            "all",
        ],
        help="Study asset to print. Repeatable. Defaults to all-static.",
    )
    url_parser.add_argument(
        "--include-md5-sidecars",
        action="store_true",
        help="Also print .md5 sidecar URLs where SPIRE exposes them.",
    )
    add_output_arguments(url_parser)
    add_downloads_page_argument(url_parser)
    url_parser.set_defaults(func=command_url)

    manifest_parser = subparsers.add_parser(
        "manifest",
        help="Print file URLs from SPIRE Apache index pages.",
    )
    manifest_parser.add_argument(
        "--scope",
        choices=sorted(INDEX_SCOPES),
        default="all-spire",
        help="Index scope to enumerate. Defaults to all-spire.",
    )
    manifest_parser.add_argument(
        "--include-md5-sidecars",
        action="store_true",
        help="Include .md5 files from index pages.",
    )
    add_output_arguments(manifest_parser)
    manifest_parser.set_defaults(func=command_manifest)

    download_parser = subparsers.add_parser(
        "download",
        help="Download SPIRE per-study MAG tar archives.",
    )
    add_study_selection_arguments(download_parser)
    add_common_arguments(download_parser, jobs=4, connections=2)
    download_parser.add_argument(
        "--expected-count",
        type=int,
        default=EXPECTED_MAG_ARCHIVE_COUNT,
        help="Expected number of page-listed SPIRE MAG tar archives. Defaults to 714.",
    )
    add_downloads_page_argument(download_parser)
    download_parser.set_defaults(func=command_download)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except AlreadyRunning:
        return 0
    except DownloadError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except SourceError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
