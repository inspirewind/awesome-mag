#!/usr/bin/env python3
"""Shared helpers for corpus MAG download scripts."""

from __future__ import annotations

import csv
import hashlib
import os
import shutil
import subprocess
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator


PART = "part4_hard_datasets"
DOWNLOADER_CHOICES = ("auto", "aria2c", "wget", "curl")


class AlreadyRunning(Exception):
    """Raised when another process holds the dataset lock."""


class DownloadError(Exception):
    """Raised when a corpus download workflow fails."""


@dataclass(frozen=True)
class DownloadItem:
    url: str
    output: Path
    md5: str = ""
    bytes: int | None = None


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def relpath(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def parse_int(value: object) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(str(value))
    except ValueError:
        return None


def clean_md5(value: str | None) -> str:
    if not value:
        return ""
    value = value.strip()
    if value.lower().startswith("md5:"):
        value = value.split(":", 1)[1]
    return value.lower()


def pid_is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


@contextmanager
def dataset_lock(root: Path, slug: str) -> Iterator[None]:
    locks_dir = root / "corpus" / ".locks"
    lock_dir = locks_dir / f"{slug}.lock"
    locks_dir.mkdir(parents=True, exist_ok=True)

    while True:
        try:
            lock_dir.mkdir()
        except FileExistsError:
            pid_file = lock_dir / "pid"
            try:
                pid = int(pid_file.read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                pid = 0
            if pid and pid_is_alive(pid):
                print(f"Dataset is already downloading under pid {pid}; skipping duplicate run.")
                raise AlreadyRunning
            print(f"Removing stale lock for {slug}.")
            shutil.rmtree(lock_dir, ignore_errors=True)
            continue

        (lock_dir / "pid").write_text(f"{os.getpid()}\n", encoding="utf-8")
        (lock_dir / "started_at").write_text(
            time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + "\n",
            encoding="utf-8",
        )
        break

    try:
        yield
    finally:
        shutil.rmtree(lock_dir, ignore_errors=True)


def choose_downloader(requested: str) -> str:
    if requested != "auto":
        if shutil.which(requested):
            return requested
        raise DownloadError(f"Downloader '{requested}' was not found on PATH.")

    for candidate in ("aria2c", "wget", "curl"):
        if shutil.which(candidate):
            return candidate
    raise DownloadError("No downloader found. Install aria2c, wget, or curl.")


def ensure_unique_outputs(items: Iterable[DownloadItem]) -> list[DownloadItem]:
    seen: set[Path] = set()
    normalized: list[DownloadItem] = []
    for item in items:
        output = item.output
        if output in seen:
            raise DownloadError(f"Duplicate output path in manifest: {output}")
        seen.add(output)
        normalized.append(item)
    return normalized


def write_manifest(items: list[DownloadItem], manifest_path: Path, root: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("url", "path", "md5", "bytes"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for item in items:
            writer.writerow(
                {
                    "url": item.url,
                    "path": relpath(item.output, root),
                    "md5": clean_md5(item.md5),
                    "bytes": "" if item.bytes is None else str(item.bytes),
                }
            )


def read_manifest_sizes(manifest_path: Path, root: Path) -> dict[Path, int]:
    sizes: dict[Path, int] = {}
    if not manifest_path.exists():
        return sizes
    with manifest_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            rel = row.get("path", "")
            size = parse_int(row.get("bytes"))
            if not rel or size is None:
                continue
            sizes[(root / rel).resolve()] = size
    return sizes


def hydrate_item_sizes(items: list[DownloadItem], manifest_path: Path, root: Path) -> list[DownloadItem]:
    previous_sizes = read_manifest_sizes(manifest_path, root)
    if not previous_sizes:
        return items
    hydrated: list[DownloadItem] = []
    for item in items:
        if item.bytes is not None:
            hydrated.append(item)
            continue
        previous_size = previous_sizes.get(item.output.resolve())
        if previous_size is None:
            hydrated.append(item)
        else:
            hydrated.append(
                DownloadItem(
                    url=item.url,
                    output=item.output,
                    md5=item.md5,
                    bytes=previous_size,
                )
            )
    return hydrated


def fill_observed_sizes(items: list[DownloadItem]) -> list[DownloadItem]:
    filled: list[DownloadItem] = []
    for item in items:
        if item.bytes is not None or not item.output.exists():
            filled.append(item)
            continue
        filled.append(
            DownloadItem(
                url=item.url,
                output=item.output,
                md5=item.md5,
                bytes=item.output.stat().st_size,
            )
        )
    return filled


def target_is_complete(item: DownloadItem, *, allow_unknown_size: bool = True) -> bool:
    if not item.output.exists() or item.output.stat().st_size == 0:
        return False
    if item.bytes is None:
        return allow_unknown_size
    if item.output.stat().st_size != item.bytes:
        return False
    return True


def inspect_targets(
    items: Iterable[DownloadItem],
    *,
    allow_unknown_size: bool,
) -> tuple[list[DownloadItem], list[str]]:
    missing: list[DownloadItem] = []
    errors: list[str] = []
    for item in items:
        if not item.url:
            continue
        if item.output.exists() and item.bytes is not None and item.output.stat().st_size > item.bytes:
            errors.append(
                f"{item.output} is larger than expected "
                f"({item.output.stat().st_size} > {item.bytes})"
            )
            continue
        if not target_is_complete(item, allow_unknown_size=allow_unknown_size):
            missing.append(item)
    return missing, errors


def write_aria2_input(items: Iterable[DownloadItem], aria2_path: Path) -> None:
    aria2_path.parent.mkdir(parents=True, exist_ok=True)
    with aria2_path.open("w", encoding="utf-8") as handle:
        for item in items:
            if not item.url:
                continue
            item.output.parent.mkdir(parents=True, exist_ok=True)
            handle.write(f"{item.url}\n")
            handle.write(f"  dir={item.output.parent}\n")
            handle.write(f"  out={item.output.name}\n")


def sanitized_aria2_env() -> dict[str, str]:
    env = os.environ.copy()
    for key in (
        "all_proxy",
        "ALL_PROXY",
        "http_proxy",
        "HTTP_PROXY",
        "https_proxy",
        "HTTPS_PROXY",
        "ftp_proxy",
        "FTP_PROXY",
    ):
        env.pop(key, None)
    return env


def run_command(cmd: list[str], *, env: dict[str, str] | None = None) -> None:
    print("+ " + " ".join(cmd), file=sys.stderr)
    try:
        subprocess.run(cmd, check=True, env=env)
    except subprocess.CalledProcessError as exc:
        raise DownloadError(f"Command failed with exit code {exc.returncode}: {' '.join(cmd)}") from exc


def download_with_aria2c(
    items: list[DownloadItem],
    work_dir: Path,
    *,
    jobs: int,
    connections: int,
    retries: int,
) -> None:
    aria2_path = work_dir / "_manifest.aria2"
    write_aria2_input(items, aria2_path)
    run_command(
        [
            "aria2c",
            "--no-conf=true",
            "--enable-rpc=false",
            "--user-agent=awesome-mag/0.1 (+https://github.com/)",
            "-c",
            "-j",
            str(jobs),
            "-x",
            str(connections),
            "-s",
            str(connections),
            "--allow-overwrite=true",
            "--auto-file-renaming=false",
            "--retry-wait=5",
            f"--max-tries={max(1, retries + 1)}",
            "-i",
            str(aria2_path),
        ],
        env=sanitized_aria2_env(),
    )


def download_with_loop(
    downloader: str,
    items: list[DownloadItem],
    *,
    retries: int,
) -> None:
    tries = max(1, retries + 1)
    for item in items:
        if not item.url or target_is_complete(item, allow_unknown_size=False):
            continue
        item.output.parent.mkdir(parents=True, exist_ok=True)
        if downloader == "wget":
            run_command(["wget", "-c", f"--tries={tries}", "-O", str(item.output), item.url])
        elif downloader == "curl":
            run_command(
                [
                    "curl",
                    "-L",
                    "-C",
                    "-",
                    "--fail",
                    "--retry",
                    str(retries),
                    "--retry-delay",
                    "5",
                    "-o",
                    str(item.output),
                    item.url,
                ]
            )
        else:
            raise DownloadError(f"Unsupported loop downloader: {downloader}")


def download_items(
    items: list[DownloadItem],
    *,
    downloader: str,
    work_dir: Path,
    jobs: int,
    connections: int,
    retries: int,
) -> None:
    items = ensure_unique_outputs(items)
    missing, errors = inspect_targets(items, allow_unknown_size=False)
    if errors:
        raise DownloadError("\n".join(errors))
    if not missing:
        print("All target files are already present.")
        return

    selected = choose_downloader(downloader)
    print(f"Downloading {len(missing)} file(s) with {selected}.")
    if selected == "aria2c":
        download_with_aria2c(
            missing,
            work_dir,
            jobs=jobs,
            connections=connections,
            retries=retries,
        )
    else:
        download_with_loop(selected, missing, retries=retries)

    missing, errors = inspect_targets(items, allow_unknown_size=True)
    if errors:
        raise DownloadError("\n".join(errors))
    if missing:
        preview = "\n".join(f"- {item.output}" for item in missing[:10])
        suffix = "" if len(missing) <= 10 else f"\n... {len(missing) - 10} more"
        raise DownloadError(f"{len(missing)} target file(s) are still incomplete:\n{preview}{suffix}")


def md5_file(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_md5(items: Iterable[DownloadItem]) -> None:
    failures: list[str] = []
    checked = 0
    for item in items:
        expected = clean_md5(item.md5)
        if not expected:
            continue
        checked += 1
        observed = md5_file(item.output)
        if observed != expected:
            failures.append(f"{item.output}: expected {expected}, observed {observed}")
    if failures:
        raise DownloadError("MD5 verification failed:\n" + "\n".join(failures[:20]))
    if checked:
        print(f"MD5 verification passed for {checked} file(s).")


def manifest_counts(manifest_path: Path, root: Path) -> tuple[int, int]:
    if not manifest_path.exists():
        return 0, 0
    expected = 0
    present = 0
    with manifest_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            rel = row.get("path", "")
            if not rel:
                continue
            expected += 1
            path = root / rel
            expected_bytes = parse_int(row.get("bytes"))
            if path.exists() and path.stat().st_size > 0:
                if expected_bytes is None or path.stat().st_size == expected_bytes:
                    present += 1
    return expected, present


def write_completed_flag(
    *,
    root: Path,
    slug: str,
    dataset: str,
    size: str,
    manifest_path: Path,
    marker_path: Path,
    note: str,
) -> None:
    completed_dir = root / "corpus" / "completed"
    completed_dir.mkdir(parents=True, exist_ok=True)
    marker_path.parent.mkdir(parents=True, exist_ok=True)
    expected, present = manifest_counts(manifest_path, root)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    marker_path.write_text(
        "\n".join(
            [
                f"slug={slug}",
                f"dataset={dataset}",
                f"part={PART}",
                f"manifest={relpath(manifest_path, root)}",
                f"file_count={expected}",
                f"present_count={present}",
                f"completed_at={now}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    flag_path = completed_dir / f"{slug}.flag"
    flag_path.write_text(
        "\n".join(
            [
                f"slug={slug}",
                f"dataset={dataset}",
                f"part={PART}",
                "file=.download-complete",
                f"path={relpath(marker_path, root)}",
                f"manifest={relpath(manifest_path, root)}",
                f"size={size}",
                f"file_count={expected}",
                f"present_count={present}",
                f"local_bytes={marker_path.stat().st_size}",
                "remote_bytes=",
                f"note={note}",
                f"completed_at={now}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Completed flag: corpus/completed/{slug}.flag")


def run_manifest_workflow(
    *,
    root: Path,
    slug: str,
    dataset: str,
    size: str,
    items: list[DownloadItem],
    downloader: str,
    jobs: int,
    connections: int,
    retries: int,
    verify: bool,
    note: str,
    manifest_only: bool = False,
) -> int:
    work_dir = root / "downloads" / slug
    manifest_path = work_dir / "manifest.tsv"
    marker_path = work_dir / ".download-complete"
    items = ensure_unique_outputs(items)

    with dataset_lock(root, slug):
        items = hydrate_item_sizes(items, manifest_path, root)
        write_manifest(items, manifest_path, root)
        print(f"Dataset: {dataset}")
        print(f"Part: {PART}")
        print(f"Files: {len(items)}")
        print(f"Manifest: {relpath(manifest_path, root)}")
        print(f"Output: {relpath(work_dir, root)}")
        print(f"Expected size: {size}")
        if manifest_only:
            print("Manifest-only mode; no data files downloaded.")
            return 0

        download_items(
            items,
            downloader=downloader,
            work_dir=work_dir,
            jobs=jobs,
            connections=connections,
            retries=retries,
        )
        items = fill_observed_sizes(items)
        write_manifest(items, manifest_path, root)
        if verify:
            verify_md5(items)
        write_completed_flag(
            root=root,
            slug=slug,
            dataset=dataset,
            size=size,
            manifest_path=manifest_path,
            marker_path=marker_path,
            note=note,
        )
    return 0


def add_common_arguments(
    parser,
    *,
    jobs: int = 4,
    connections: int = 2,
    default_downloader: str = "auto",
) -> None:
    parser.add_argument(
        "--root",
        default=str(repo_root()),
        help="Repository root. Defaults to the awesome-mag checkout root.",
    )
    parser.add_argument(
        "--downloader",
        choices=DOWNLOADER_CHOICES,
        default=default_downloader,
        help=(
            f"Transfer backend. Defaults to {default_downloader}. "
            "Use auto for aria2c, then wget, then curl."
        ),
    )
    parser.add_argument("--jobs", type=int, default=jobs, help="Parallel file jobs for aria2c.")
    parser.add_argument(
        "--connections",
        type=int,
        default=connections,
        help="Connections per file for aria2c.",
    )
    parser.add_argument("--retries", type=int, default=3, help="Retry count per file.")
    parser.add_argument(
        "--verify-md5",
        action="store_true",
        help="Verify MD5 checksums when the manifest provides them.",
    )
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Generate the URL manifest without downloading data files.",
    )


def main_wrapper(func, argv: list[str] | None = None) -> int:
    try:
        return func(argv)
    except AlreadyRunning:
        return 0
    except DownloadError as exc:
        print(str(exc), file=sys.stderr)
        return 1
