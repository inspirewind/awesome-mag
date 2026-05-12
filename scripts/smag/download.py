#!/usr/bin/env python3
"""Download and reassemble the split SMAG MAG archive from Zenodo."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.corpus_download import (
    DownloadError,
    DownloadItem,
    add_common_arguments,
    dataset_lock,
    download_items,
    main_wrapper,
    parse_int,
    relpath,
    verify_md5,
    write_completed_flag,
    write_manifest,
)


SLUG = "smag"
DATASET = "SMAG"
SIZE = "36.3 GiB split MAG archive"
NOTE = "Zenodo mag.tar.gz.* parts only; companion virus, SNV, tree, README, and supplementary files are skipped."
ZENODO_FILES_API = "https://zenodo.org/api/records/8223844/files"
USER_AGENT = "awesome-mag/0.1 (+https://github.com/)"


def fetch_json(url: str) -> dict[str, object]:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json, */*", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise DownloadError(f"Zenodo request failed: {exc.code} {exc.reason}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise DownloadError(f"Zenodo request failed: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise DownloadError("Zenodo files API returned non-JSON content.") from exc


def iter_file_entries(url: str) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    next_url: str | None = url
    seen_pages: set[str] = set()
    while next_url:
        if next_url in seen_pages:
            raise DownloadError(f"Zenodo pagination loop detected at {next_url}")
        seen_pages.add(next_url)
        payload = fetch_json(next_url)
        page_entries = payload.get("entries")
        if page_entries is None:
            page_entries = payload.get("files")
        if not isinstance(page_entries, list):
            raise DownloadError("Zenodo files API did not expose an entries/files list.")
        entries.extend(entry for entry in page_entries if isinstance(entry, dict))
        links = payload.get("links")
        next_url = links.get("next") if isinstance(links, dict) else None
    return entries


def entry_url(entry: dict[str, object], key: str) -> str:
    links = entry.get("links")
    if isinstance(links, dict):
        content = links.get("content") or links.get("self")
        if content:
            return str(content)
    quoted = urllib.parse.quote(key, safe="")
    return f"https://zenodo.org/records/8223844/files/{quoted}?download=1"


def build_part_items(root: Path) -> list[DownloadItem]:
    entries = iter_file_entries(ZENODO_FILES_API)
    output_dir = root / "downloads" / SLUG / "parts"
    items: list[DownloadItem] = []
    for entry in sorted(entries, key=lambda item: str(item.get("key", ""))):
        key = str(entry.get("key", ""))
        if not key.startswith("mag.tar.gz."):
            continue
        checksum = str(entry.get("checksum", ""))
        size = parse_int(entry.get("size")) or parse_int(entry.get("filesize"))
        items.append(
            DownloadItem(
                url=entry_url(entry, key),
                output=output_dir / key,
                md5=checksum,
                bytes=size,
            )
        )
    if not items:
        raise DownloadError("No SMAG mag.tar.gz.* parts were found in the Zenodo files API.")
    return items


def merge_parts(parts: list[DownloadItem], final_archive: Path) -> DownloadItem:
    known_sizes = [item.bytes for item in parts]
    total_bytes = sum(size for size in known_sizes if size is not None)
    expected_bytes = total_bytes if all(size is not None for size in known_sizes) else None

    if final_archive.exists() and expected_bytes is not None and final_archive.stat().st_size == expected_bytes:
        print(f"Existing reassembled archive matches expected size: {final_archive}")
        return DownloadItem(url="", output=final_archive, bytes=expected_bytes)

    final_archive.parent.mkdir(parents=True, exist_ok=True)
    partial = final_archive.with_suffix(final_archive.suffix + ".part")
    with partial.open("wb") as out_handle:
        for item in parts:
            with item.output.open("rb") as in_handle:
                for chunk in iter(lambda: in_handle.read(1024 * 1024), b""):
                    out_handle.write(chunk)
    partial.replace(final_archive)
    if expected_bytes is not None and final_archive.stat().st_size != expected_bytes:
        raise DownloadError(
            f"Reassembled archive size mismatch: {final_archive.stat().st_size} != {expected_bytes}"
        )
    return DownloadItem(url="", output=final_archive, bytes=expected_bytes)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_arguments(parser, jobs=4, connections=2)
    parser.add_argument(
        "--no-merge",
        action="store_true",
        help="Download parts but do not concatenate them into downloads/smag/mag.tar.gz.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    work_dir = root / "downloads" / SLUG
    manifest_path = work_dir / "manifest.tsv"
    marker_path = work_dir / ".download-complete"

    with dataset_lock(root, SLUG):
        parts = build_part_items(root)
        manifest_items = list(parts)
        final_item: DownloadItem | None = None
        if not args.no_merge:
            total = sum(item.bytes for item in parts if item.bytes is not None)
            expected = total if all(item.bytes is not None for item in parts) else None
            final_item = DownloadItem(url="", output=work_dir / "mag.tar.gz", bytes=expected)
            manifest_items.append(final_item)
        write_manifest(manifest_items, manifest_path, root)

        print(f"Dataset: {DATASET}")
        print("Part: part4_hard_datasets")
        print(f"Files: {len(manifest_items)}")
        print(f"Manifest: {relpath(manifest_path, root)}")
        print(f"Output: {relpath(work_dir, root)}")
        print(f"Expected size: {SIZE}")
        if args.manifest_only:
            print("Manifest-only mode; no data files downloaded.")
            return 0

        download_items(
            parts,
            downloader=args.downloader,
            work_dir=work_dir,
            jobs=args.jobs,
            connections=args.connections,
            retries=args.retries,
        )
        if args.verify_md5:
            verify_md5(parts)
        if final_item is not None:
            final_item = merge_parts(parts, final_item.output)
            write_manifest(parts + [final_item], manifest_path, root)
        write_completed_flag(
            root=root,
            slug=SLUG,
            dataset=DATASET,
            size=SIZE,
            manifest_path=manifest_path,
            marker_path=marker_path,
            note=NOTE,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main_wrapper(main))
