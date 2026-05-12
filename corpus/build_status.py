#!/usr/bin/env python3
"""Report corpus download completion from corpus/completed flags."""

from __future__ import annotations

import os
import csv
from pathlib import Path


CORPUS_DIR = Path(__file__).resolve().parent
ROOT_DIR = CORPUS_DIR.parent
DOWNLOAD_BASH_DIR = CORPUS_DIR / "download_bash"
COMPLETED_DIR = CORPUS_DIR / "completed"
LOCKS_DIR = CORPUS_DIR / ".locks"


def parse_metadata(path: Path) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("#"):
            continue
        payload = line[1:].strip()
        if ":" not in payload:
            continue
        key, value = payload.split(":", 1)
        metadata[key.strip().lower()] = value.strip()
    return metadata


def parse_flag(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()
    return data


def int_value(value: str | None) -> int | None:
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def manifest_counts(path: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0

    expected = 0
    present = 0
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            rel_path = row.get("path", "")
            if not rel_path:
                continue
            expected += 1
            data_path = ROOT_DIR / rel_path
            expected_bytes = int_value(row.get("bytes"))
            if not data_path.exists() or data_path.stat().st_size == 0:
                continue
            if expected_bytes is not None and data_path.stat().st_size != expected_bytes:
                continue
            present += 1
    return expected, present


def lock_status(slug: str) -> str | None:
    pid_file = LOCKS_DIR / f"{slug}.lock" / "pid"
    if not pid_file.exists():
        return None

    pid = int_value(pid_file.read_text(encoding="utf-8", errors="replace").strip())
    if pid is None:
        return "stale-lock"

    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return "stale-lock"
    except PermissionError:
        return "running"
    return "running"


def has_data_files(path: Path) -> bool:
    if not path.exists():
        return False
    ignored = {"manifest.tsv", "_manifest.aria2", ".download-complete"}
    for child in path.rglob("*"):
        if not child.is_file():
            continue
        if child.name in ignored:
            continue
        if child.name.startswith("."):
            continue
        return True
    return False


def discover_scripts() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for script in sorted(DOWNLOAD_BASH_DIR.glob("*/*.sh")):
        if script.parent.name.startswith("_"):
            continue
        metadata = parse_metadata(script)
        slug = metadata.get("slug") or script.stem
        rows.append(
            {
                "slug": slug,
                "dataset": metadata.get("dataset", slug),
                "part": metadata.get("part", script.parent.name),
                "size": metadata.get("size", ""),
                "file": metadata.get("file", ""),
                "script": str(script.relative_to(ROOT_DIR)),
            }
        )
    return rows


def status_for(row: dict[str, str]) -> tuple[str, str]:
    locked = lock_status(row["slug"])
    if locked is not None:
        return locked, ""

    flag_path = COMPLETED_DIR / f"{row['slug']}.flag"
    flag = parse_flag(flag_path)
    download_dir = ROOT_DIR / "downloads" / row["slug"]
    default_path = download_dir / row["file"]

    if not flag:
        if default_path.exists() or has_data_files(download_dir):
            return "partial", ""
        return "pending", ""

    rel_path = flag.get("path", "")
    data_path = ROOT_DIR / rel_path if rel_path else default_path
    if not data_path.exists():
        return "flag-only", flag.get("completed_at", "")

    manifest_rel = flag.get("manifest", "")
    if manifest_rel:
        manifest_path = ROOT_DIR / manifest_rel
        expected, present = manifest_counts(manifest_path)
        if expected == 0:
            return "flag-only", flag.get("completed_at", "")
        if present == expected:
            return "done", flag.get("completed_at", "")
        if present == 0:
            return "pending", flag.get("completed_at", "")
        return "incomplete", flag.get("completed_at", "")

    current_bytes = data_path.stat().st_size
    remote_bytes = int_value(flag.get("remote_bytes"))
    flagged_local_bytes = int_value(flag.get("local_bytes"))

    if remote_bytes is not None:
        if current_bytes == remote_bytes:
            return "done", flag.get("completed_at", "")
        if current_bytes < remote_bytes:
            return "incomplete", flag.get("completed_at", "")
        return "size-mismatch", flag.get("completed_at", "")

    if flagged_local_bytes is not None and current_bytes != flagged_local_bytes:
        return "changed", flag.get("completed_at", "")

    return "flag-unverified", flag.get("completed_at", "")


def print_table(rows: list[dict[str, str]]) -> None:
    total = len(rows)
    statuses = [status_for(row)[0] for row in rows]
    counts = {status: statuses.count(status) for status in sorted(set(statuses))}
    summary = "  ".join(f"{status}: {count}" for status, count in counts.items())

    print("# Corpus Build Status")
    print()
    print(f"Scripts: {total}  {summary}")
    print()
    print("| Part | Dataset | Slug | Size | Status | Completed At | Script |")
    print("| --- | --- | --- | --- | --- | --- | --- |")

    for row in sorted(rows, key=lambda item: (item["part"], item["dataset"].casefold())):
        status, completed_at = status_for(row)
        print(
            "| {part} | {dataset} | `{slug}` | {size} | {status} | {completed_at} | `{script}` |".format(
                part=row["part"],
                dataset=row["dataset"],
                slug=row["slug"],
                size=row["size"],
                status=status,
                completed_at=completed_at,
                script=row["script"],
            )
        )


def main() -> int:
    rows = discover_scripts()
    print_table(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
