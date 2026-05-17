#!/usr/bin/env python3
"""Download the Anammox Microbiota Figshare dataset package.

The Figshare record mixes genome and gene catalog assets, so this helper does
not claim to produce a MAG-only corpus target. It downloads the official
Figshare files/package into downloads/anammox-microbiota for manual inspection
and subsequent per-dataset filelist construction.
"""

from __future__ import annotations

import argparse
import json
import os
import re
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
    main_wrapper,
    run_manifest_workflow,
)


SLUG = "anammox-microbiota"
DATASET = "Anammox Microbiota Catalog"
SIZE = "8.12 GB Figshare dataset package"
NOTE = (
    "Official Figshare files/package for the Anammox microbiota gene and genome "
    "catalog; inspect after download to select MAG sequence files."
)
ARTICLE_ID = "25476583"
VERSION = "1"
FIGSHARE_API = f"https://api.figshare.com/v2/articles/{ARTICLE_ID}"
FIGSHARE_FILES_API = f"https://api.figshare.com/v2/articles/{ARTICLE_ID}/files"
DOWNLOAD_ALL_URL = f"https://figshare.com/ndownloader/articles/{ARTICLE_ID}/versions/{VERSION}"
DEFAULT_USER_AGENT = "awesome-mag/0.1 (mailto:your-email@example.org; +https://github.com/)"


def load_token(*, env_name: str, token_file: str | None) -> str:
    if token_file:
        path = Path(token_file).expanduser()
        try:
            token = path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise DownloadError(f"Could not read Figshare token file: {path}") from exc
        if token:
            return token
    return os.environ.get(env_name, "").strip()


def request_headers(*, user_agent: str, token: str = "", accept: str = "application/json, */*") -> dict[str, str]:
    headers = {
        "Accept": accept,
        "User-Agent": user_agent,
    }
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def fetch_json(url: str, *, token: str, user_agent: str) -> object:
    request = urllib.request.Request(
        url,
        headers=request_headers(user_agent=user_agent, token=token),
    )
    try:
        with urllib.request.urlopen(request) as response:
            text = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise DownloadError(f"Figshare API request failed: {exc.code} {exc.reason}\n{body[:2000]}") from exc
    except urllib.error.URLError as exc:
        raise DownloadError(f"Figshare API request failed: {exc.reason}") from exc

    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise DownloadError(f"Figshare API returned non-JSON content:\n{text[:2000]}") from exc
    return payload


def safe_filename(name: str, fallback: str) -> str:
    name = name.strip() or fallback
    name = name.rsplit("/", 1)[-1]
    name = re.sub(r"[^A-Za-z0-9._,+@=-]+", "_", name)
    name = name.strip("._")
    return name or fallback


def clean_md5(value: object) -> str:
    if not value:
        return ""
    text = str(value).strip()
    if text.lower().startswith("md5:"):
        text = text.split(":", 1)[1]
    return text


def parse_int(value: object) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(str(value))
    except ValueError:
        return None


def file_download_url(entry: dict[str, object]) -> str:
    direct = entry.get("download_url")
    if direct:
        return str(direct)
    file_id = entry.get("id")
    if file_id:
        return f"https://ndownloader.figshare.com/files/{file_id}"
    return ""


def fetch_file_entries(
    *,
    files_api_url: str,
    article_api_url: str,
    token: str,
    user_agent: str,
) -> list[object]:
    errors: list[str] = []
    for label, url in (("files API", files_api_url), ("article metadata API", article_api_url)):
        try:
            payload = fetch_json(url, token=token, user_agent=user_agent)
        except DownloadError as exc:
            errors.append(f"{label} failed: {exc}")
            continue
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict) and isinstance(payload.get("files"), list):
            return payload["files"]  # type: ignore[index]
        errors.append(f"{label} response did not expose a files list.")
    raise DownloadError("\n".join(errors))


def build_api_items(
    root: Path,
    *,
    files_api_url: str,
    article_api_url: str,
    include_regex: str | None,
    token: str,
    user_agent: str,
) -> list[DownloadItem]:
    files = fetch_file_entries(
        files_api_url=files_api_url,
        article_api_url=article_api_url,
        token=token,
        user_agent=user_agent,
    )

    output_dir = root / "downloads" / SLUG / "figshare_files"
    pattern = re.compile(include_regex) if include_regex else None
    items: list[DownloadItem] = []
    seen_names: set[str] = set()

    for index, raw_entry in enumerate(files, start=1):
        if not isinstance(raw_entry, dict):
            continue
        name = safe_filename(str(raw_entry.get("name", "")), fallback=f"figshare_file_{index}")
        if pattern and not pattern.search(name):
            continue
        if name in seen_names:
            stem = Path(name).stem
            suffix = "".join(Path(name).suffixes)
            name = f"{stem}_{index}{suffix}"
        seen_names.add(name)

        url = file_download_url(raw_entry)
        if not url:
            continue
        items.append(
            DownloadItem(
                url=url,
                output=output_dir / name,
                md5=clean_md5(raw_entry.get("computed_md5") or raw_entry.get("supplied_md5")),
                bytes=parse_int(raw_entry.get("size")),
            )
        )

    if not items:
        if include_regex:
            raise DownloadError(f"No Figshare files matched --include-regex: {include_regex}")
        raise DownloadError("No downloadable files were exposed by the Figshare API.")
    return items


def build_download_all_item(root: Path) -> list[DownloadItem]:
    output = root / "downloads" / SLUG / f"figshare_{ARTICLE_ID}_v{VERSION}_download_all.zip"
    return [DownloadItem(url=DOWNLOAD_ALL_URL, output=output, bytes=8_120_727_476)]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_arguments(parser, jobs=2, connections=2, default_downloader="auto")
    parser.add_argument(
        "--api-url",
        default=FIGSHARE_API,
        help="Figshare public article metadata API URL. Defaults to the Anammox article API.",
    )
    parser.add_argument(
        "--files-api-url",
        default=FIGSHARE_FILES_API,
        help="Figshare public article files API URL. Defaults to the Anammox article files API.",
    )
    parser.add_argument(
        "--include-regex",
        default=None,
        help="Only download Figshare API files whose names match this Python regex.",
    )
    parser.add_argument(
        "--figshare-token-env",
        default="FIGSHARE_TOKEN",
        help="Environment variable containing a Figshare personal token. Defaults to FIGSHARE_TOKEN.",
    )
    parser.add_argument(
        "--figshare-token-file",
        default=None,
        help="Path to a file containing a Figshare personal token. Avoid committing this file.",
    )
    parser.add_argument(
        "--user-agent",
        default=DEFAULT_USER_AGENT,
        help=(
            "User-Agent sent to the Figshare API. Replace the mailto placeholder with "
            "a real contact address if your server policy allows it."
        ),
    )
    parser.add_argument(
        "--download-all-route",
        action="store_true",
        help="Skip file-level API enumeration and download the official Figshare download-all ZIP route.",
    )
    parser.add_argument(
        "--no-fallback-download-all",
        action="store_true",
        help="If the Figshare API fails, do not fall back to the official download-all URL.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    token = load_token(env_name=args.figshare_token_env, token_file=args.figshare_token_file)

    if args.download_all_route:
        items = build_download_all_item(root)
    else:
        try:
            items = build_api_items(
                root,
                files_api_url=args.files_api_url,
                article_api_url=args.api_url,
                include_regex=args.include_regex,
                token=token,
                user_agent=args.user_agent,
            )
        except DownloadError as exc:
            if args.no_fallback_download_all:
                raise
            print(f"Figshare file-level API failed; falling back to download-all route.\n{exc}", file=sys.stderr)
            items = build_download_all_item(root)

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
