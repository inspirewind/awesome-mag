#!/usr/bin/env bash
set -euo pipefail

# dataset: cFMD
# slug: cfmd
# clustering: RabbitTClust
# input archive: downloads/cfmd/cFMD_mags.tar.gz
# output filelist: corpus/cluster_inputs/rabbittclust/cfmd.list
#
# This builder covers the currently downloaded initial Cell paper MAG archive.
# Current cFMD v1.3.1 has additional MAG archives that should be handled
# separately if they are downloaded later.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
FORCE_EXTRACT=0
VERIFY_MD5=0
INSPECT_ONLY=0
LOG_EVERY=1000

while [ "$#" -gt 0 ]; do
  case "$1" in
    --root)
      ROOT_DIR="$(cd "$2" && pwd)"
      shift 2
      ;;
    --force-extract)
      FORCE_EXTRACT=1
      shift
      ;;
    --verify-md5)
      VERIFY_MD5=1
      shift
      ;;
    --inspect-only)
      INSPECT_ONLY=1
      shift
      ;;
    --log-every)
      LOG_EVERY="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

export ROOT_DIR
export FORCE_EXTRACT
export VERIFY_MD5
export INSPECT_ONLY
export LOG_EVERY

python3 - <<'PY'
from __future__ import annotations

import hashlib
import os
import shutil
import tarfile
import time
from pathlib import Path


SLUG = "cfmd"
ARCHIVE_NAME = "cFMD_mags.tar.gz"
EXPECTED_ARCHIVE_BYTES = 9_808_151_932
EXPECTED_MD5 = "691e4e35c8b2ccf104ea5336dd6a5c9d"
EXPECTED_FASTA_COUNT = 10_899
FASTA_SUFFIXES = (
    ".fa",
    ".fasta",
    ".fna",
    ".fas",
    ".fa.gz",
    ".fasta.gz",
    ".fna.gz",
    ".fas.gz",
    ".fa.bz2",
    ".fasta.bz2",
    ".fna.bz2",
    ".fas.bz2",
)


def human_bytes(value: int) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    number = float(value)
    for unit in units:
        if number < 1024 or unit == units[-1]:
            return f"{number:.2f} {unit}"
        number /= 1024
    raise AssertionError("unreachable")


def is_fasta(path: str) -> bool:
    return path.lower().endswith(FASTA_SUFFIXES)


def md5sum(path: Path, *, log_every_bytes: int = 2 * 1024**3) -> str:
    digest = hashlib.md5()
    seen = 0
    next_log = log_every_bytes
    started = time.time()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
            seen += len(chunk)
            if seen >= next_log:
                elapsed = time.time() - started
                print(f"[md5] {path.name}: {human_bytes(seen)} read in {elapsed:.1f}s", flush=True)
                next_log += log_every_bytes
    return digest.hexdigest()


def safe_target(root: Path, member_name: str) -> Path:
    target = (root / member_name).resolve()
    root_resolved = root.resolve()
    if target != root_resolved and not str(target).startswith(str(root_resolved) + os.sep):
        raise SystemExit(f"Unsafe tar member path: {member_name}")
    return target


root = Path(os.environ["ROOT_DIR"]).expanduser().resolve()
force_extract = os.environ.get("FORCE_EXTRACT") == "1"
verify_md5 = os.environ.get("VERIFY_MD5") == "1"
inspect_only = os.environ.get("INSPECT_ONLY") == "1"
log_every = int(os.environ.get("LOG_EVERY", "1000"))

if log_every <= 0:
    raise SystemExit("--log-every must be positive")

download_dir = root / "downloads" / SLUG
archive_path = download_dir / ARCHIVE_NAME
extract_dir = download_dir / "extracted"
filelist_dir = root / "corpus" / "cluster_inputs" / "rabbittclust"
filelist = filelist_dir / f"{SLUG}.list"

if not archive_path.exists():
    raise SystemExit(f"Missing archive: {archive_path}")

observed_bytes = archive_path.stat().st_size
if observed_bytes != EXPECTED_ARCHIVE_BYTES:
    raise SystemExit(
        f"Archive size mismatch for {ARCHIVE_NAME}: "
        f"{observed_bytes} != {EXPECTED_ARCHIVE_BYTES}"
    )

if verify_md5:
    print(f"[md5] verifying {archive_path}", flush=True)
    observed_md5 = md5sum(archive_path)
    if observed_md5 != EXPECTED_MD5:
        raise SystemExit(f"MD5 mismatch for {ARCHIVE_NAME}: {observed_md5} != {EXPECTED_MD5}")

extract_dir.mkdir(parents=True, exist_ok=True)
filelist_dir.mkdir(parents=True, exist_ok=True)

entries = 0
fasta_count = 0
fasta_bytes = 0
extracted = 0
skipped = 0
started = time.time()

print(f"[scan] {ARCHIVE_NAME}: start", flush=True)
try:
    with tarfile.open(archive_path, mode="r|gz") as tar:
        for member in tar:
            entries += 1
            if entries % log_every == 0:
                elapsed = time.time() - started
                print(
                    f"[scan] {ARCHIVE_NAME}: entries={entries}; "
                    f"fastas={fasta_count}; extracted={extracted}; "
                    f"skipped={skipped}; elapsed={elapsed:.1f}s",
                    flush=True,
                )

            if not member.isfile() or not is_fasta(member.name):
                continue

            fasta_count += 1
            fasta_bytes += member.size
            if inspect_only:
                continue

            target = safe_target(extract_dir, member.name)
            if (
                not force_extract
                and target.exists()
                and target.stat().st_size == member.size
            ):
                skipped += 1
                continue

            source = tar.extractfile(member)
            if source is None:
                raise SystemExit(f"Could not extract tar member: {member.name}")

            target.parent.mkdir(parents=True, exist_ok=True)
            tmp = target.with_name(target.name + ".tmp")
            with source, tmp.open("wb") as out:
                shutil.copyfileobj(source, out, length=1024 * 1024)
            tmp.replace(target)
            extracted += 1
except (tarfile.TarError, EOFError, OSError) as exc:
    raise SystemExit(f"Failed to read {archive_path}: {exc}") from exc

if fasta_count != EXPECTED_FASTA_COUNT:
    raise SystemExit(f"Unexpected FASTA count: {fasta_count} != {EXPECTED_FASTA_COUNT}")

elapsed = time.time() - started
print(
    f"[done] {ARCHIVE_NAME}: entries={entries}; fastas={fasta_count}; "
    f"fasta_bytes={fasta_bytes} ({human_bytes(fasta_bytes)}); "
    f"extracted={extracted}; skipped={skipped}; elapsed={elapsed:.1f}s",
    flush=True,
)

if inspect_only:
    print(f"dataset: {SLUG}")
    print("mode: inspect-only")
    print(f"archive: {archive_path}")
    print(f"archive_bytes: {observed_bytes}")
    print(f"expected_filelist_entries: {fasta_count}")
    print(f"uncompressed_fasta_bytes: {fasta_bytes} ({human_bytes(fasta_bytes)})")
    print(f"extract_dir: {extract_dir}")
    raise SystemExit(0)

fastas = sorted(
    path
    for path in extract_dir.rglob("*")
    if path.is_file() and is_fasta(path.name)
)

if len(fastas) != EXPECTED_FASTA_COUNT:
    raise SystemExit(f"Unexpected extracted FASTA count: {len(fastas)} != {EXPECTED_FASTA_COUNT}")

with filelist.open("w", encoding="utf-8") as handle:
    for fasta in fastas:
        handle.write(str(fasta.resolve()) + "\n")

print(f"dataset: {SLUG}")
print(f"archive: {archive_path}")
print(f"archive_bytes: {observed_bytes}")
print(f"extract_dir: {extract_dir}")
print(f"filelist: {filelist}")
print(f"filelist_entries: {len(fastas)}")
print(f"uncompressed_fasta_bytes: {fasta_bytes} ({human_bytes(fasta_bytes)})")
print(f"first_entry: {fastas[0].resolve()}")
print(f"last_entry: {fastas[-1].resolve()}")
PY
