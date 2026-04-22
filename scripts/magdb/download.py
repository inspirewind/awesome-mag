#!/usr/bin/env python3
"""Automate article discovery and downloads from MAGdb."""

from __future__ import annotations

import argparse
import getpass
import http.cookiejar
import http.cookies
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

BASE_URL = "https://magdb.nanhulab.ac.cn"
ROOT_ID = "620a0f2a40da9762bca509bc"
PUBLIC_TOKEN = "Dyw639DrEpz3VdBS2wCshX"
GROUP_ID = "68493799f13f19003f1e2dae"
RELEASE_DIR = "HAMG_20240130"
USER_AGENT = "awesome-mag/0.1 (+https://github.com/)"
XML_NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


class DownloadError(Exception):
    """A per-file download failure that may be retried or skipped."""


@dataclass(frozen=True)
class Category:
    key: str
    label: str
    index: int

    @property
    def workbook_url(self) -> str:
        return (
            f"{BASE_URL}/biobank/v1/getDirectoryByPath/{ROOT_ID}/group/preview/"
            f"params%3D/MAG/{self.label}.xlsx?token={PUBLIC_TOKEN}"
        )

    @property
    def result_dir(self) -> str:
        return f"{self.index}_{self.label}_result"


@dataclass(frozen=True)
class Entry:
    category: Category
    number: str
    year: str
    raw_title: str
    title: str
    short_introduction: str
    metagenome_runs_accession: str
    high_quality_mags: str
    journal: str
    doi: str

    @property
    def archive_url(self) -> str:
        quoted_title = urllib.parse.quote(self.raw_title, safe="")
        return (
            f"{BASE_URL}/biobank/v1/getDirectoryByPath/{ROOT_ID}/group/preview/"
            f"params%3D/{RELEASE_DIR}/{self.category.result_dir}/{quoted_title}/data.tar.gz"
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "category": self.category.key,
            "number": self.number,
            "year": self.year,
            "raw_title": self.raw_title,
            "title": self.title,
            "short_introduction": self.short_introduction,
            "metagenome_runs_accession": self.metagenome_runs_accession,
            "high_quality_mags": self.high_quality_mags,
            "journal": self.journal,
            "doi": self.doi,
            "archive_url": self.archive_url,
        }


CATEGORIES = {
    "clinical": Category(key="clinical", label="Clinical", index=1),
    "environment": Category(key="environment", label="Environment", index=2),
    "animal": Category(key="animal", label="Animal", index=3),
}


def build_opener() -> urllib.request.OpenerDirector:
    cookie_jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))


def normalize_header(value: str) -> str:
    value = re.sub(r"\s+", " ", value.strip().lower())
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def column_index(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha())
    index = 0
    for char in letters:
        index = index * 26 + (ord(char.upper()) - ord("A") + 1)
    return index - 1


def shared_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        raw = archive.read("xl/sharedStrings.xml")
    except KeyError:
        return []

    root = ET.fromstring(raw)
    values: list[str] = []
    for item in root.findall("a:si", XML_NS):
        text = "".join(node.text or "" for node in item.iterfind(".//a:t", XML_NS))
        values.append(text)
    return values


def cell_text(cell: ET.Element, strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.iterfind(".//a:t", XML_NS))

    value = cell.find("a:v", XML_NS)
    if value is None or value.text is None:
        return ""
    if cell_type == "s":
        return strings[int(value.text)]
    return value.text


def parse_workbook(data: bytes) -> list[dict[str, str]]:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        strings = shared_strings(archive)
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))

    rows: list[dict[int, str]] = []
    for row in sheet.findall("a:sheetData/a:row", XML_NS):
        row_values: dict[int, str] = {}
        for cell in row.findall("a:c", XML_NS):
            ref = cell.attrib.get("r", "")
            row_values[column_index(ref)] = cell_text(cell, strings)
        rows.append(row_values)

    if not rows:
        return []

    header_row = rows[0]
    last_column = max(header_row)
    headers = [normalize_header(header_row.get(index, "")) for index in range(last_column + 1)]

    parsed_rows: list[dict[str, str]] = []
    for row in rows[1:]:
        values: dict[str, str] = {}
        for index, header in enumerate(headers):
            if not header:
                continue
            values[header] = row.get(index, "")
        if any(value.strip() for value in values.values()):
            parsed_rows.append(values)
    return parsed_rows


def request(
    opener: urllib.request.OpenerDirector,
    url: str,
    *,
    method: str = "GET",
    payload: dict | None = None,
) -> bytes:
    data = None
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": USER_AGENT,
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with opener.open(req) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Request failed: {exc.code} {exc.reason}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Request failed: {exc.reason}") from exc


def parse_json_response(response: bytes, context: str) -> dict:
    try:
        return json.loads(response.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Unexpected non-JSON response while {context}.") from exc


def normalize_cookie_header(raw_cookie: str) -> str:
    value = raw_cookie.strip()
    value = re.sub(r"^\s*cookie\s*:?\s*", "", value, flags=re.IGNORECASE | re.DOTALL)

    parsed = http.cookies.SimpleCookie()
    parsed.load(value)
    if parsed:
        return "; ".join(f"{morsel.key}={morsel.value}" for morsel in parsed.values())

    if "=" not in value:
        raise SystemExit(
            "Invalid cookie input. Provide a full Cookie header or at least EGG_SESS=<value>."
        )
    return value


def configure_cookie_auth(opener: urllib.request.OpenerDirector, raw_cookie: str) -> None:
    cookie_header = normalize_cookie_header(raw_cookie)
    filtered = [(name, value) for name, value in opener.addheaders if name.lower() != "cookie"]
    filtered.append(("Cookie", cookie_header))
    opener.addheaders = filtered


def verify_authenticated_session(opener: urllib.request.OpenerDirector) -> None:
    response = request(opener, f"{BASE_URL}/biobank/v1/getMyself")
    data = parse_json_response(response, "verifying the MAGdb session")
    if data.get("statusCode") == 402 or data.get("errMsg") == "没有登录":
        raise SystemExit(
            "MAGdb session is not authenticated. Provide a fresh EGG_SESS cookie."
        )


def activate_group_session(opener: urllib.request.OpenerDirector) -> None:
    request(
        opener,
        f"{BASE_URL}/biobank/v1/group",
        method="POST",
        payload={"_id": GROUP_ID},
    )


def fetch_entries(
    opener: urllib.request.OpenerDirector, category: Category
) -> list[Entry]:
    data = request(opener, category.workbook_url)
    rows = parse_workbook(data)
    entries: list[Entry] = []
    for row in rows:
        raw_title = row.get("title", "")
        entries.append(
            Entry(
                category=category,
                number=row.get("number", "").strip(),
                year=row.get("year", "").strip(),
                raw_title=raw_title,
                title=raw_title.strip(),
                short_introduction=row.get("short_introduction", "").strip(),
                metagenome_runs_accession=row.get("metagenome_runs_accession", "").strip(),
                high_quality_mags=row.get("high_quality_mags", "").strip(),
                journal=row.get("journal", "").strip(),
                doi=row.get("doi", "").strip(),
            )
        )
    return entries


def iter_categories(name: str | None) -> Iterable[Category]:
    if not name or name == "all":
        return CATEGORIES.values()
    return [CATEGORIES[name]]


def select_entries(entries: list[Entry], title: str | None, contains: str | None) -> list[Entry]:
    if title:
        wanted = title.casefold()
        return [entry for entry in entries if entry.title.casefold() == wanted]
    if contains:
        wanted = contains.casefold()
        return [entry for entry in entries if wanted in entry.title.casefold()]
    return entries


def ensure_match_constraints(entries: list[Entry], allow_many: bool) -> list[Entry]:
    if not entries:
        raise SystemExit("No matching MAGdb entries found.")
    if len(entries) > 1 and not allow_many:
        message = ["Multiple MAGdb entries matched. Re-run with --all-matches or narrow the query:"]
        for entry in entries:
            message.append(f"- [{entry.category.key}] {entry.title} ({entry.year})")
        raise SystemExit("\n".join(message))
    return entries


def print_entries(entries: list[Entry], as_json: bool) -> None:
    if as_json:
        print(json.dumps([entry.to_dict() for entry in entries], ensure_ascii=False, indent=2))
        return

    for entry in entries:
        print(f"[{entry.category.key}] {entry.number}. {entry.title} ({entry.year})")
        print(f"  Journal: {entry.journal}")
        print(f"  MAGs: {entry.high_quality_mags} | Runs: {entry.metagenome_runs_accession}")
        if entry.doi:
            print(f"  DOI: {entry.doi}")
        print(f"  URL: {entry.archive_url}")


def resolve_cookie_auth(args: argparse.Namespace) -> str | None:
    if args.cookie:
        return args.cookie
    if args.cookie_file:
        return Path(args.cookie_file).expanduser().read_text(encoding="utf-8").strip()
    if args.cookie_env:
        value = os.environ.get(args.cookie_env, "").strip()
        if not value:
            raise SystemExit(f"Environment variable '{args.cookie_env}' is empty or not set.")
        return value
    if args.cookie_prompt:
        return getpass.getpass(
            "MAGdb cookie (paste EGG_SESS=... or a full Cookie header): "
        ).strip()
    return None


def safe_filename(text: str) -> str:
    cleaned = re.sub(r"[^\w.-]+", "_", text.strip(), flags=re.UNICODE)
    cleaned = cleaned.strip("._")
    return cleaned or "magdb-download"


def temporary_destination(destination: Path) -> Path:
    return destination.with_suffix(destination.suffix + ".part")


def copy_response_to_file(response, handle) -> int:
    total = 0
    while True:
        chunk = response.read(1024 * 1024)
        if not chunk:
            break
        handle.write(chunk)
        total += len(chunk)
    return total


def download_entry(
    opener: urllib.request.OpenerDirector,
    entry: Entry,
    output_dir: Path,
    *,
    skip_existing: bool = False,
    resume: bool = False,
) -> tuple[str, Path]:
    destination = output_dir / entry.category.key / f"{safe_filename(entry.title)}.tar.gz"
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

    req = urllib.request.Request(
        entry.archive_url,
        headers=headers,
    )
    try:
        with opener.open(req) as response:
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                body = response.read().decode("utf-8", errors="replace")
                raise DownloadError(
                    f"MAGdb returned JSON instead of an archive for '{entry.title}'.\n{body}"
                )

            status = getattr(response, "status", 200)
            if status == 204:
                raise DownloadError(f"MAGdb returned 204 No Content for '{entry.title}'.")
            if range_start and status != 206:
                range_start = 0
                mode = "wb"

            if mode == "wb":
                partial.parent.mkdir(parents=True, exist_ok=True)

            with partial.open(mode) as handle:
                bytes_written = copy_response_to_file(response, handle)
            if bytes_written == 0:
                raise DownloadError(f"MAGdb returned an empty body for '{entry.title}'.")
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
    output_dir: Path,
    *,
    skip_existing: bool,
    resume: bool,
    retries: int,
) -> tuple[str, Path]:
    attempts = retries + 1
    last_error: DownloadError | None = None
    for attempt in range(1, attempts + 1):
        try:
            return download_entry(
                opener,
                entry,
                output_dir,
                skip_existing=skip_existing,
                resume=resume,
            )
        except DownloadError as exc:
            last_error = exc
            if attempt >= attempts:
                break
            time.sleep(min(attempt, 3))
    assert last_error is not None
    raise last_error


def add_query_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--category",
        choices=["all", *CATEGORIES],
        default="all",
        help="MAGdb category to search. Defaults to all categories.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--title", help="Match an exact MAGdb title.")
    group.add_argument("--contains", help="Match entries whose titles contain this text.")


def command_list(args: argparse.Namespace) -> int:
    opener = build_opener()
    entries: list[Entry] = []
    for category in iter_categories(args.category):
        entries.extend(fetch_entries(opener, category))
    entries = select_entries(entries, args.title, args.contains)
    print_entries(entries, args.json)
    return 0


def command_url(args: argparse.Namespace) -> int:
    opener = build_opener()
    entries: list[Entry] = []
    for category in iter_categories(args.category):
        entries.extend(fetch_entries(opener, category))
    matches = ensure_match_constraints(
        select_entries(entries, args.title, args.contains),
        allow_many=args.all_matches,
    )
    for entry in matches:
        print(entry.archive_url)
    return 0


def command_download(args: argparse.Namespace) -> int:
    opener = build_opener()
    entries: list[Entry] = []
    for category in iter_categories(args.category):
        entries.extend(fetch_entries(opener, category))
    matches = ensure_match_constraints(
        select_entries(entries, args.title, args.contains),
        allow_many=args.all_matches,
    )

    cookie_auth = resolve_cookie_auth(args)
    if cookie_auth:
        configure_cookie_auth(opener, cookie_auth)
        verify_authenticated_session(opener)
        activate_group_session(opener)
    else:
        raise SystemExit(
            "Authentication is required for downloads. Use one of the cookie options."
        )

    output_dir = Path(args.output_dir).expanduser().resolve()
    failures: list[tuple[Entry, str]] = []
    for entry in matches:
        try:
            status, destination = download_with_retries(
                opener,
                entry,
                output_dir,
                skip_existing=args.skip_existing,
                resume=args.resume,
                retries=args.retries,
            )
            if status == "skipped":
                print(f"SKIP {destination}")
            else:
                print(f"OK   {destination}")
        except DownloadError as exc:
            message = str(exc)
            failures.append((entry, message))
            print(f"FAIL {entry.category.key}: {entry.title}", file=sys.stderr)
            print(message, file=sys.stderr)
            if not args.continue_on_error:
                return 1

    if failures:
        print(
            f"Completed with {len(failures)} failed download(s).",
            file=sys.stderr,
        )
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List, inspect, and download MAGdb article archives.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List MAGdb entries.")
    add_query_arguments(list_parser)
    list_parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    list_parser.set_defaults(func=command_list)

    url_parser = subparsers.add_parser("url", help="Print MAGdb archive URLs.")
    add_query_arguments(url_parser)
    url_parser.add_argument(
        "--all-matches",
        action="store_true",
        help="Print every matched URL instead of requiring a single match.",
    )
    url_parser.set_defaults(func=command_url)

    download_parser = subparsers.add_parser(
        "download",
        help="Download MAGdb archives with an authenticated browser cookie.",
    )
    add_query_arguments(download_parser)
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
        help="Keep downloading other entries if one entry fails.",
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
    auth_group = download_parser.add_mutually_exclusive_group(required=True)
    auth_group.add_argument(
        "--cookie",
        help="Cookie string from the browser, such as EGG_SESS=... or a full Cookie header.",
    )
    auth_group.add_argument(
        "--cookie-file",
        help="Read the cookie string from a local text file.",
    )
    auth_group.add_argument(
        "--cookie-env",
        help="Read the cookie string from an environment variable.",
    )
    auth_group.add_argument(
        "--cookie-prompt",
        action="store_true",
        help="Prompt securely for a cookie string instead of putting it in shell history.",
    )
    download_parser.add_argument(
        "--output-dir",
        default="downloads/magdb",
        help="Directory for downloaded archives. Defaults to downloads/magdb.",
    )
    download_parser.set_defaults(func=command_download)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if getattr(args, "retries", 0) < 0:
        parser.error("--retries must be 0 or greater.")
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
