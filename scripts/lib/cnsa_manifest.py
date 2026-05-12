#!/usr/bin/env python3
"""Helpers for CNSA public_info manifests."""

from __future__ import annotations

import urllib.error
import urllib.request
from pathlib import Path

from lib.corpus_download import DownloadError, DownloadItem


USER_AGENT = "awesome-mag/0.1 (+https://github.com/)"


def fetch_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "text/plain, */*",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(request) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise DownloadError(f"Request failed: {exc.code} {exc.reason}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise DownloadError(f"Request failed: {exc.reason}") from exc


def unique_name(url: str, seen: set[str]) -> str:
    name = url.rstrip("/").rsplit("/", 1)[-1]
    if name not in seen:
        seen.add(name)
        return name
    stem, dot, suffix = name.partition(".")
    index = 2
    while True:
        candidate = f"{stem}_{index}{dot}{suffix}" if dot else f"{name}_{index}"
        if candidate not in seen:
            seen.add(candidate)
            return candidate
        index += 1


def assembly_items_from_manifest(
    *,
    manifest_url: str,
    output_dir: Path,
    alternate_ftp2: bool = False,
) -> list[DownloadItem]:
    text = fetch_text(manifest_url)
    seen: set[str] = set()
    items: list[DownloadItem] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) < 2 or fields[0] != "assembly":
            continue
        url = fields[1]
        if alternate_ftp2:
            url = url.replace("ftp://ftp.cngb.org/", "ftp://ftp2.cngb.org/", 1)
        name = unique_name(url, seen)
        items.append(DownloadItem(url=url, output=output_dir / "assemblies" / name))
    if not items:
        raise DownloadError(f"No assembly URLs found in CNSA manifest: {manifest_url}")
    return items
