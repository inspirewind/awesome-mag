#!/usr/bin/env python3
"""List and download public gcMeta catalogue archives."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

CATALOGUE_TREE_API = "https://gcmeta.wdcm.org/gcmetaapi/catalogue/catalogueTree"
CATALOGUE_NAME_LIST_API = "https://gcmeta.wdcm.org/gcmetaapi/home/catalogueNameList"
ARCHIVE_BASE = "https://open.nmdc.cn/specail_data/gcmeta/Mags/Archive"
USER_AGENT = "awesome-mag/0.1 (+https://github.com/)"
PROGRESS_INTERVAL_SECONDS = 2.0

FIELD_MAP = {
    "total": {
        "archive": "total_file",
        "md5": "total_md5",
        "metadata": "total_metadata",
    },
    "species": {
        "archive": "species_file",
        "md5": "species_md5",
        "metadata": "species_metadata",
    },
}


class ApiError(Exception):
    """A failure while reading a public gcMeta enumeration API."""


class DownloadError(Exception):
    """A per-file download failure that may be retried or skipped."""


@dataclass(frozen=True)
class Entry:
    catalogue_group: str
    catalogue_name: str
    genome_num: int | None
    represent_species_num: int | None
    filesize_genome: int | None
    filesize_represent_species: int | None
    total_file: str
    total_md5: str
    total_metadata: str
    species_file: str
    species_md5: str
    species_metadata: str

    def file_name(self, bundle: str, artifact: str) -> str:
        return getattr(self, FIELD_MAP[bundle][artifact])

    def catalogue_stem(self) -> str:
        return "".join("_" if ch.isspace() else ch for ch in self.catalogue_name)

    def download_url(self, bundle: str, artifact: str) -> str:
        catalogue_dir = urllib.parse.quote(self.catalogue_stem(), safe="._,-()+")
        filename = urllib.parse.quote(self.file_name(bundle, artifact), safe="._,-()+")
        return f"{ARCHIVE_BASE}/{catalogue_dir}/{filename}"

    def to_dict(self) -> dict[str, object]:
        payload = {
            "catalogue_group": self.catalogue_group,
            "catalogue_name": self.catalogue_name,
            "catalogue_stem": self.catalogue_stem(),
            "genome_num": self.genome_num,
            "represent_species_num": self.represent_species_num,
            "filesize_genome_mb": self.filesize_genome,
            "filesize_represent_species_mb": self.filesize_represent_species,
            "total_file": self.total_file,
            "total_md5": self.total_md5,
            "total_metadata": self.total_metadata,
            "species_file": self.species_file,
            "species_md5": self.species_md5,
            "species_metadata": self.species_metadata,
        }
        for bundle in ("total", "species"):
            for artifact in ("archive", "md5", "metadata"):
                payload[f"{bundle}_{artifact}_url"] = self.download_url(bundle, artifact)
        return payload


def build_opener() -> urllib.request.OpenerDirector:
    return urllib.request.build_opener()


def request_bytes(
    opener: urllib.request.OpenerDirector,
    url: str,
    *,
    accept: str = "application/json, text/plain, */*",
) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with opener.open(req) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise ApiError(f"Request failed: {exc.code} {exc.reason}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise ApiError(f"Request failed: {exc.reason}") from exc


def parse_json_response(response: bytes, context: str) -> dict[str, object]:
    try:
        payload = json.loads(response.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ApiError(f"Unexpected non-JSON response while {context}.") from exc
    if not isinstance(payload, dict):
        raise ApiError(f"Unexpected JSON shape while {context}.")
    return payload


def extract_public_data(
    opener: urllib.request.OpenerDirector,
    url: str,
    *,
    description: str,
) -> object:
    payload = parse_json_response(request_bytes(opener, url), description)
    if payload.get("success") is False:
        message = payload.get("message") or payload.get("msg") or "Request failed."
        raise ApiError(str(message))
    status = payload.get("status")
    if status not in (None, 0):
        message = payload.get("message") or payload.get("msg") or "Request failed."
        raise ApiError(str(message))
    return payload.get("data")


def derived_entry(catalogue_group: str, catalogue_name: str) -> Entry:
    stem = "".join("_" if ch.isspace() else ch for ch in catalogue_name)
    total_archive = f"{stem}_all_MAGs.tar.gz"
    species_archive = f"{stem}_species-level_representative_MAGs.tar.gz"
    return Entry(
        catalogue_group=catalogue_group,
        catalogue_name=catalogue_name,
        genome_num=None,
        represent_species_num=None,
        filesize_genome=None,
        filesize_represent_species=None,
        total_file=total_archive,
        total_md5=f"{total_archive}.md5",
        total_metadata=f"{stem}_all_MAGs.metainfo.txt",
        species_file=species_archive,
        species_md5=f"{species_archive}.md5",
        species_metadata=f"{stem}_species-level_representative_MAGs.metainfo.txt",
    )


def fetch_catalogue_tree(
    opener: urllib.request.OpenerDirector,
) -> dict[str, tuple[str, str]]:
    data = extract_public_data(
        opener,
        CATALOGUE_TREE_API,
        description="reading the gcMeta catalogue tree",
    )
    if not isinstance(data, list):
        raise ApiError("gcMeta catalogue tree did not return a list.")

    grouped: dict[str, tuple[str, str]] = {}
    for node in data:
        if not isinstance(node, dict):
            continue
        fallback_group = str(node.get("name", "")).strip()
        children = node.get("children")
        if not isinstance(children, list):
            continue
        for child in children:
            if not isinstance(child, dict):
                continue
            name = str(child.get("name", "")).strip()
            if not name:
                continue
            group = str(child.get("catalogueGroup", "")).strip() or fallback_group
            grouped[name.casefold()] = (group, name)
    return grouped


def fetch_catalogue_names(opener: urllib.request.OpenerDirector) -> list[str]:
    data = extract_public_data(
        opener,
        CATALOGUE_NAME_LIST_API,
        description="reading the gcMeta catalogue name list",
    )
    if not isinstance(data, list):
        raise ApiError("gcMeta catalogue name list did not return a list.")

    names: list[str] = []
    seen: set[str] = set()
    for item in data:
        name = str(item).strip()
        if not name:
            continue
        key = name.casefold()
        if key in seen:
            continue
        seen.add(key)
        names.append(name)
    return names


def fetch_all_entries() -> list[Entry]:
    opener = build_opener()

    tree_entries: dict[str, tuple[str, str]] = {}
    flat_names: list[str] = []
    errors: list[str] = []

    try:
        tree_entries = fetch_catalogue_tree(opener)
    except ApiError as exc:
        errors.append(f"catalogueTree: {exc}")

    try:
        flat_names = fetch_catalogue_names(opener)
    except ApiError as exc:
        errors.append(f"catalogueNameList: {exc}")

    if not tree_entries and not flat_names:
        detail = "\n".join(f"- {message}" for message in errors) or "- no public API details"
        raise SystemExit(f"Unable to enumerate gcMeta catalogues from public APIs:\n{detail}")

    entries_by_key: dict[str, Entry] = {}
    for key, (group, name) in tree_entries.items():
        entries_by_key[key] = derived_entry(group, name)

    for name in flat_names:
        key = name.casefold()
        if key in entries_by_key:
            continue
        entries_by_key[key] = derived_entry("", name)

    entries = list(entries_by_key.values())
    entries.sort(
        key=lambda entry: (
            entry.catalogue_group == "",
            entry.catalogue_group.casefold(),
            entry.catalogue_name.casefold(),
        )
    )
    return entries


def select_entries(
    entries: list[Entry],
    *,
    group: str | None,
    catalogue: str | None,
    contains: str | None,
) -> list[Entry]:
    selected = entries
    if group:
        wanted = group.casefold()
        selected = [entry for entry in selected if entry.catalogue_group.casefold() == wanted]
    if catalogue:
        wanted = catalogue.casefold()
        selected = [entry for entry in selected if entry.catalogue_name.casefold() == wanted]
    if contains:
        wanted = contains.casefold()
        selected = [
            entry
            for entry in selected
            if wanted in entry.catalogue_name.casefold() or wanted in entry.catalogue_group.casefold()
        ]
    return selected


def ensure_match_constraints(entries: list[Entry], allow_many: bool) -> list[Entry]:
    if not entries:
        raise SystemExit("No matching gcMeta catalogue entries found.")
    if len(entries) > 1 and not allow_many:
        lines = ["Multiple gcMeta catalogue entries matched. Re-run with --all-matches or narrow the query:"]
        for entry in entries:
            if entry.catalogue_group:
                lines.append(f"- [{entry.catalogue_group}] {entry.catalogue_name}")
            else:
                lines.append(f"- {entry.catalogue_name}")
        raise SystemExit("\n".join(lines))
    return entries


def iter_requested_assets(
    bundle: str,
    *,
    include_md5: bool,
    include_metadata: bool,
) -> Iterable[tuple[str, str]]:
    bundles = ("total", "species") if bundle == "both" else (bundle,)
    artifacts = ["archive"]
    if include_md5:
        artifacts.append("md5")
    if include_metadata:
        artifacts.append("metadata")
    for item_bundle in bundles:
        for artifact in artifacts:
            yield (item_bundle, artifact)


def print_entries(entries: list[Entry], as_json: bool) -> None:
    if as_json:
        print(json.dumps([entry.to_dict() for entry in entries], ensure_ascii=False, indent=2))
        return

    for entry in entries:
        if entry.catalogue_group:
            print(f"[{entry.catalogue_group}] {entry.catalogue_name}")
        else:
            print(entry.catalogue_name)
        print(f"  Total archive:   {entry.total_file}")
        print(f"  Species archive: {entry.species_file}")


def print_urls(
    entries: list[Entry],
    *,
    bundle: str,
    include_md5: bool,
    include_metadata: bool,
    as_json: bool,
) -> None:
    rows: list[dict[str, str]] = []
    for entry in entries:
        for item_bundle, artifact in iter_requested_assets(
            bundle,
            include_md5=include_md5,
            include_metadata=include_metadata,
        ):
            rows.append(
                {
                    "catalogue_group": entry.catalogue_group,
                    "catalogue_name": entry.catalogue_name,
                    "bundle": item_bundle,
                    "artifact": artifact,
                    "file_name": entry.file_name(item_bundle, artifact),
                    "url": entry.download_url(item_bundle, artifact),
                }
            )

    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return

    for row in rows:
        label = f"[{row['catalogue_group']}] {row['catalogue_name']}"
        if not row["catalogue_group"]:
            label = row["catalogue_name"]
        print(f"{label} | {row['bundle']} {row['artifact']} | {row['url']}")


def temporary_destination(destination: Path) -> Path:
    return destination.with_suffix(destination.suffix + ".part")


def format_bytes(size: int | None) -> str:
    if size is None:
        return "unknown"
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} TiB"


def parse_content_length(response) -> int | None:
    value = response.headers.get("Content-Length")
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def render_progress(label: str, current: int, total: int | None) -> str:
    if total and total > 0:
        percent = min(current / total * 100, 100.0)
        return f"{label}: {percent:5.1f}% ({format_bytes(current)} / {format_bytes(total)})"
    return f"{label}: {format_bytes(current)}"


def emit_progress(label: str, current: int, total: int | None, *, final: bool = False) -> None:
    message = render_progress(label, current, total)
    if sys.stderr.isatty() and not final:
        sys.stderr.write(f"\r{message}")
        sys.stderr.flush()
        return
    if sys.stderr.isatty() and final:
        sys.stderr.write(f"\r{message}\n")
    else:
        sys.stderr.write(f"{message}\n")
    sys.stderr.flush()


def copy_response_to_file(
    response,
    handle,
    *,
    label: str,
    initial_bytes: int = 0,
    total_bytes: int | None = None,
    show_progress: bool = True,
) -> int:
    total = 0
    last_report = time.monotonic()
    if show_progress:
        emit_progress(label, initial_bytes, total_bytes)
    while True:
        chunk = response.read(1024 * 1024)
        if not chunk:
            break
        handle.write(chunk)
        total += len(chunk)
        now = time.monotonic()
        if show_progress and now - last_report >= PROGRESS_INTERVAL_SECONDS:
            emit_progress(label, initial_bytes + total, total_bytes)
            last_report = now
    if show_progress:
        emit_progress(label, initial_bytes + total, total_bytes, final=True)
    return total


def download_asset(
    opener: urllib.request.OpenerDirector,
    entry: Entry,
    bundle: str,
    artifact: str,
    output_dir: Path,
    *,
    skip_existing: bool = False,
    resume: bool = False,
    show_progress: bool = True,
) -> tuple[str, Path]:
    filename = entry.file_name(bundle, artifact)
    destination = output_dir / bundle / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = temporary_destination(destination)

    if skip_existing and destination.exists() and destination.stat().st_size > 0:
        return ("skipped", destination)

    range_start = 0
    mode = "wb"
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}

    if resume and partial.exists():
        range_start = partial.stat().st_size
        if range_start > 0:
            headers["Range"] = f"bytes={range_start}-"
            mode = "ab"

    label = f"{entry.catalogue_name} [{bundle} {artifact}]"
    if show_progress:
        print(f"START {label} -> {destination}", file=sys.stderr)

    req = urllib.request.Request(entry.download_url(bundle, artifact), headers=headers)
    try:
        with opener.open(req) as response:
            status = getattr(response, "status", 200)
            if status == 204:
                raise DownloadError(
                    f"gcMeta returned 204 No Content for '{entry.catalogue_name}' {bundle} {artifact}."
                )
            content_length = parse_content_length(response)
            if range_start and status != 206:
                range_start = 0
                mode = "wb"
            total_bytes = content_length + range_start if content_length is not None else None

            with partial.open(mode) as handle:
                bytes_written = copy_response_to_file(
                    response,
                    handle,
                    label=label,
                    initial_bytes=range_start,
                    total_bytes=total_bytes,
                    show_progress=show_progress,
                )
            if bytes_written == 0:
                raise DownloadError(
                    f"gcMeta returned an empty body for '{entry.catalogue_name}' {bundle} {artifact}."
                )
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise DownloadError(f"Download failed: {exc.code} {exc.reason}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise DownloadError(f"Download failed: {exc.reason}") from exc

    partial.replace(destination)
    return ("downloaded", destination)


def download_with_retries(
    opener: urllib.request.OpenerDirector,
    entry: Entry,
    bundle: str,
    artifact: str,
    output_dir: Path,
    *,
    skip_existing: bool,
    resume: bool,
    retries: int,
    show_progress: bool,
) -> tuple[str, Path]:
    attempts = retries + 1
    last_error: DownloadError | None = None
    for attempt in range(1, attempts + 1):
        try:
            return download_asset(
                opener,
                entry,
                bundle,
                artifact,
                output_dir,
                skip_existing=skip_existing,
                resume=resume,
                show_progress=show_progress,
            )
        except DownloadError as exc:
            last_error = exc
            if attempt >= attempts:
                break
            time.sleep(min(attempt, 3))
    assert last_error is not None
    raise last_error


def add_query_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--group", help="Match an exact gcMeta catalogue group.")
    parser.add_argument("--catalogue", help="Match an exact gcMeta catalogue name.")
    parser.add_argument(
        "--contains",
        help="Match catalogue entries whose group or name contains this substring.",
    )


def add_asset_arguments(parser: argparse.ArgumentParser, *, allow_both: bool = True) -> None:
    parser.add_argument(
        "--bundle",
        choices=["total", "species", "both"] if allow_both else ["total", "species"],
        default="total",
        help="Which gcMeta download tab to use. Defaults to total.",
    )
    parser.add_argument(
        "--include-md5",
        action="store_true",
        help="Include the .md5 sidecar file.",
    )
    parser.add_argument(
        "--include-metadata",
        action="store_true",
        help="Include the metadata text file.",
    )


def add_compatibility_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--page-size",
        type=int,
        default=None,
        help=argparse.SUPPRESS,
    )


def command_list(args: argparse.Namespace) -> int:
    entries = fetch_all_entries()
    matches = select_entries(
        entries,
        group=args.group,
        catalogue=args.catalogue,
        contains=args.contains,
    )
    print_entries(matches, args.json)
    return 0


def command_url(args: argparse.Namespace) -> int:
    entries = fetch_all_entries()
    matches = ensure_match_constraints(
        select_entries(
            entries,
            group=args.group,
            catalogue=args.catalogue,
            contains=args.contains,
        ),
        allow_many=args.all_matches,
    )
    print_urls(
        matches,
        bundle=args.bundle,
        include_md5=args.include_md5,
        include_metadata=args.include_metadata,
        as_json=args.json,
    )
    return 0


def command_download(args: argparse.Namespace) -> int:
    opener = build_opener()
    if not args.no_progress:
        print("Resolving gcMeta catalogues from public APIs...", file=sys.stderr)
    entries = fetch_all_entries()
    matches = ensure_match_constraints(
        select_entries(
            entries,
            group=args.group,
            catalogue=args.catalogue,
            contains=args.contains,
        ),
        allow_many=args.all_matches,
    )
    if not args.no_progress:
        print(f"Selected {len(matches)} catalogue entr{'y' if len(matches) == 1 else 'ies'}.", file=sys.stderr)

    output_dir = Path(args.output_dir).expanduser().resolve()
    failures: list[tuple[str, str]] = []
    for entry in matches:
        for bundle, artifact in iter_requested_assets(
            args.bundle,
            include_md5=args.include_md5,
            include_metadata=args.include_metadata,
        ):
            try:
                status, destination = download_with_retries(
                    opener,
                    entry,
                    bundle,
                    artifact,
                    output_dir,
                    skip_existing=args.skip_existing,
                    resume=args.resume,
                    retries=args.retries,
                    show_progress=not args.no_progress,
                )
                if status == "skipped":
                    print(f"SKIP {destination}")
                else:
                    print(f"OK   {destination}")
            except DownloadError as exc:
                message = str(exc)
                failures.append((entry.catalogue_name, message))
                print(
                    f"FAIL {entry.catalogue_group}: {entry.catalogue_name} [{bundle} {artifact}]",
                    file=sys.stderr,
                )
                print(message, file=sys.stderr)
                if not args.continue_on_error:
                    return 1

    if failures:
        print(f"Completed with {len(failures)} failed download(s).", file=sys.stderr)
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List, inspect, and download public gcMeta catalogue archives.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List gcMeta catalogue entries.")
    add_query_arguments(list_parser)
    list_parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    add_compatibility_arguments(list_parser)
    list_parser.set_defaults(func=command_list)

    url_parser = subparsers.add_parser("url", help="Print gcMeta archive URLs.")
    add_query_arguments(url_parser)
    add_asset_arguments(url_parser)
    url_parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    url_parser.add_argument(
        "--all-matches",
        action="store_true",
        help="Print every matched URL instead of requiring a single match.",
    )
    add_compatibility_arguments(url_parser)
    url_parser.set_defaults(func=command_url)

    download_parser = subparsers.add_parser("download", help="Download gcMeta public files.")
    add_query_arguments(download_parser)
    add_asset_arguments(download_parser)
    download_parser.add_argument(
        "--all-matches",
        action="store_true",
        help="Download every matched entry instead of requiring a single match.",
    )
    download_parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip target files that already exist and are non-empty.",
    )
    download_parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Keep downloading other files if one file fails.",
    )
    download_parser.add_argument(
        "--retries",
        type=int,
        default=0,
        help="Retry each failed download this many additional times. Defaults to 0.",
    )
    download_parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from an existing .part file when the server supports range requests.",
    )
    download_parser.add_argument(
        "--output-dir",
        default="downloads/gcmeta",
        help="Directory for downloaded gcMeta files. Defaults to downloads/gcmeta.",
    )
    download_parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable per-file download progress messages.",
    )
    add_compatibility_arguments(download_parser)
    download_parser.set_defaults(func=command_download)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
