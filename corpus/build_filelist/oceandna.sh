#!/usr/bin/env bash
set -euo pipefail

# dataset: OceanDNA MAG Catalog
# slug: oceandna
# clustering: RabbitTClust
# input payloads:
#   downloads/oceandna/non_representatives/oceandna_non_representatives_15218454.zip
#   downloads/oceandna/representatives/*.fasta.gz
# output filelist: corpus/cluster_inputs/rabbittclust/oceandna.list
#
# OceanDNA has two MAG sequence routes: 43,859 non-representative MAGs in a
# Figshare ZIP and 8,466 species representatives as ENA WGS set FASTA files.
# The builder extracts only the ZIP-backed MAG files and points directly to
# ENA .fasta.gz files because RabbitTClust can read gzip FASTA.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
FORCE_EXTRACT=0
INSPECT_ONLY=0
ZIP_TEST=0
LOG_EVERY=5000
EXPECTED_NONREP_FASTA_COUNT=43859
EXPECTED_REP_FASTA_COUNT=8466

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
    --inspect-only)
      INSPECT_ONLY=1
      shift
      ;;
    --zip-test)
      ZIP_TEST=1
      shift
      ;;
    --expected-nonrep-count)
      EXPECTED_NONREP_FASTA_COUNT="$2"
      shift 2
      ;;
    --expected-rep-count)
      EXPECTED_REP_FASTA_COUNT="$2"
      shift 2
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
export INSPECT_ONLY
export ZIP_TEST
export LOG_EVERY
export EXPECTED_NONREP_FASTA_COUNT
export EXPECTED_REP_FASTA_COUNT

python3 - <<'PY'
from __future__ import annotations

import bz2
import os
import shutil
import time
import zipfile
from pathlib import Path


SLUG = "oceandna"
NONREP_ZIP = "non_representatives/oceandna_non_representatives_15218454.zip"
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
SUPPORTED_OUTPUT_SUFFIXES = (
    ".fa",
    ".fasta",
    ".fna",
    ".fas",
    ".fa.gz",
    ".fasta.gz",
    ".fna.gz",
    ".fas.gz",
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


def is_supported_fasta_path(path: Path) -> bool:
    return path.name.lower().endswith(SUPPORTED_OUTPUT_SUFFIXES)


def output_member_name(member_name: str) -> str:
    if member_name.lower().endswith(".bz2"):
        return member_name.rsplit(".", 1)[0]
    return member_name


def safe_target(root: Path, member_name: str) -> Path:
    target = (root / member_name).resolve()
    root_resolved = root.resolve()
    if target != root_resolved and not str(target).startswith(str(root_resolved) + os.sep):
        raise SystemExit(f"Unsafe ZIP member path: {member_name}")
    return target


root = Path(os.environ["ROOT_DIR"]).expanduser().resolve()
force_extract = os.environ.get("FORCE_EXTRACT") == "1"
inspect_only = os.environ.get("INSPECT_ONLY") == "1"
zip_test = os.environ.get("ZIP_TEST") == "1"
log_every = int(os.environ.get("LOG_EVERY", "5000"))
expected_nonrep = int(os.environ.get("EXPECTED_NONREP_FASTA_COUNT", "43859"))
expected_rep = int(os.environ.get("EXPECTED_REP_FASTA_COUNT", "8466"))
expected_total = expected_nonrep + expected_rep

if log_every <= 0:
    raise SystemExit("--log-every must be positive")
if expected_nonrep < 0 or expected_rep < 0:
    raise SystemExit("expected counts must be non-negative")

download_dir = root / "downloads" / SLUG
zip_path = download_dir / NONREP_ZIP
representatives_dir = download_dir / "representatives"
extract_dir = download_dir / "extracted" / "non_representatives"
filelist_dir = root / "corpus" / "cluster_inputs" / "rabbittclust"
debug_dir = root / "corpus" / "cluster_inputs" / "debug"
filelist = filelist_dir / f"{SLUG}.list"
members_tsv = debug_dir / "oceandna.non_representatives.members.tsv"

if not zip_path.exists():
    raise SystemExit(f"Missing non-representative ZIP: {zip_path}")
if not representatives_dir.exists():
    raise SystemExit(f"Missing representatives directory: {representatives_dir}")

zip_bytes = zip_path.stat().st_size
if zip_bytes == 0:
    raise SystemExit(f"Non-representative ZIP is empty: {zip_path}")

extract_dir.mkdir(parents=True, exist_ok=True)
filelist_dir.mkdir(parents=True, exist_ok=True)
debug_dir.mkdir(parents=True, exist_ok=True)

rep_fastas = sorted(
    path
    for path in representatives_dir.rglob("*")
    if path.is_file() and is_supported_fasta_path(path) and path.stat().st_size > 0
)
if len(rep_fastas) != expected_rep:
    raise SystemExit(f"Unexpected representative FASTA count: {len(rep_fastas)} != {expected_rep}")

entries = 0
nonrep_fastas = 0
nonrep_fasta_bytes = 0
extracted = 0
skipped = 0
started = time.time()

print(f"[scan] {zip_path.name}: start ({human_bytes(zip_bytes)})", flush=True)
try:
    with zipfile.ZipFile(zip_path) as archive, members_tsv.open("w", encoding="utf-8") as summary:
        if zip_test:
            print(f"[zip-test] {zip_path.name}: start", flush=True)
            bad_member = archive.testzip()
            if bad_member:
                raise SystemExit(f"ZIP integrity test failed at member: {bad_member}")
            print(f"[zip-test] {zip_path.name}: OK", flush=True)

        summary.write("member\tcompressed_size\tuncompressed_size\n")
        for info in archive.infolist():
            entries += 1
            if entries % log_every == 0:
                elapsed = time.time() - started
                print(
                    f"[scan] {zip_path.name}: entries={entries}; "
                    f"fastas={nonrep_fastas}; extracted={extracted}; "
                    f"skipped={skipped}; elapsed={elapsed:.1f}s",
                    flush=True,
                )

            if info.is_dir() or not is_fasta(info.filename):
                continue

            nonrep_fastas += 1
            nonrep_fasta_bytes += info.file_size
            summary.write(f"{info.filename}\t{info.compress_size}\t{info.file_size}\n")
            if inspect_only:
                continue

            target = safe_target(extract_dir, output_member_name(info.filename))
            if not force_extract and target.exists():
                if info.filename.lower().endswith(".bz2"):
                    if target.stat().st_size > 0:
                        skipped += 1
                        continue
                elif target.stat().st_size == info.file_size:
                    skipped += 1
                    continue

            target.parent.mkdir(parents=True, exist_ok=True)
            tmp = target.with_name(target.name + ".tmp")
            with archive.open(info) as source, tmp.open("wb") as out:
                if info.filename.lower().endswith(".bz2"):
                    with bz2.BZ2File(source) as decompressed:
                        shutil.copyfileobj(decompressed, out, length=8 * 1024 * 1024)
                else:
                    shutil.copyfileobj(source, out, length=8 * 1024 * 1024)
            tmp.replace(target)
            extracted += 1
except (zipfile.BadZipFile, EOFError, OSError) as exc:
    raise SystemExit(
        f"Failed to read {zip_path}: {exc}. "
        "The ZIP is likely incomplete; rerun the OceanDNA download script to resume."
    ) from exc

if nonrep_fastas != expected_nonrep:
    raise SystemExit(f"Unexpected non-representative FASTA count: {nonrep_fastas} != {expected_nonrep}")

elapsed = time.time() - started
print(
    f"[done] {zip_path.name}: entries={entries}; fastas={nonrep_fastas}; "
    f"fasta_bytes={nonrep_fasta_bytes} ({human_bytes(nonrep_fasta_bytes)}); "
    f"extracted={extracted}; skipped={skipped}; elapsed={elapsed:.1f}s",
    flush=True,
)

if inspect_only:
    print(f"dataset: {SLUG}")
    print("mode: inspect-only")
    print(f"nonrep_zip: {zip_path}")
    print(f"nonrep_zip_bytes: {zip_bytes}")
    print(f"nonrep_fasta_entries: {nonrep_fastas}")
    print(f"representative_fasta_entries: {len(rep_fastas)}")
    print(f"expected_filelist_entries: {expected_total}")
    print(f"nonrep_fasta_bytes: {nonrep_fasta_bytes} ({human_bytes(nonrep_fasta_bytes)})")
    print(f"representatives_dir: {representatives_dir}")
    print(f"extract_dir: {extract_dir}")
    print(f"members_tsv: {members_tsv}")
    raise SystemExit(0)

materialized_nonrep_fastas = sorted(
    path
    for path in extract_dir.rglob("*")
    if path.is_file() and is_supported_fasta_path(path)
)

if len(materialized_nonrep_fastas) != nonrep_fastas:
    raise SystemExit(
        f"Unexpected extracted non-representative FASTA count: "
        f"{len(materialized_nonrep_fastas)} != {nonrep_fastas}"
    )

fastas = sorted(rep_fastas + materialized_nonrep_fastas)
if len(fastas) != expected_total:
    raise SystemExit(f"Unexpected total filelist count: {len(fastas)} != {expected_total}")

with filelist.open("w", encoding="utf-8") as handle:
    for fasta in fastas:
        handle.write(str(fasta.resolve()) + "\n")

materialized_bytes = sum(path.stat().st_size for path in materialized_nonrep_fastas)
representative_bytes = sum(path.stat().st_size for path in rep_fastas)

print(f"dataset: {SLUG}")
print(f"nonrep_zip: {zip_path}")
print(f"nonrep_zip_bytes: {zip_bytes}")
print(f"representatives_dir: {representatives_dir}")
print(f"extract_dir: {extract_dir}")
print(f"members_tsv: {members_tsv}")
print(f"filelist: {filelist}")
print(f"filelist_entries: {len(fastas)}")
print(f"nonrep_fasta_entries: {len(materialized_nonrep_fastas)}")
print(f"representative_fasta_entries: {len(rep_fastas)}")
print(f"nonrep_fasta_bytes: {nonrep_fasta_bytes} ({human_bytes(nonrep_fasta_bytes)})")
print(f"materialized_nonrep_bytes: {materialized_bytes} ({human_bytes(materialized_bytes)})")
print(f"representative_bytes: {representative_bytes} ({human_bytes(representative_bytes)})")
print(f"first_entry: {fastas[0].resolve()}")
print(f"last_entry: {fastas[-1].resolve()}")
PY
