#!/usr/bin/env bash
set -euo pipefail

# dataset: Human Gut Archaeome
# slug: human-gut-archaeome
# clustering: RabbitTClust
# input archive: downloads/human-gut-archaeome/archaea_gut-genomes.tar.gz
# output filelist: corpus/cluster_inputs/rabbittclust/human-gut-archaeome.list
#
# The EBI archive stores recovered archaeal genomes in GFF/GFF3 format. Each
# GFF is one genome and can contain its nucleotide sequence in a trailing
# ##FASTA block. This builder materializes those FASTA blocks as one .fna file
# per genome so RabbitTClust receives genome-level FASTA paths.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
FORCE_EXTRACT=0
INSPECT_ONLY=0
SKIP_SIZE_CHECK=0
LOG_EVERY=200

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
    --skip-size-check)
      SKIP_SIZE_CHECK=1
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
export INSPECT_ONLY
export SKIP_SIZE_CHECK
export LOG_EVERY

python3 - <<'PY'
from __future__ import annotations

import bz2
import gzip
import os
import shutil
import tarfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import BinaryIO, Iterator


SLUG = "human-gut-archaeome"
ARCHIVE_NAME = "archaea_gut-genomes.tar.gz"
EXPECTED_ARCHIVE_BYTES = 688_991_120
EXPECTED_GENOME_COUNT = 1_167
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
GFF_SUFFIXES = (
    ".gff",
    ".gff3",
    ".gff.gz",
    ".gff3.gz",
    ".gff.bz2",
    ".gff3.bz2",
)


def human_bytes(value: int) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    number = float(value)
    for unit in units:
        if number < 1024 or unit == units[-1]:
            return f"{number:.2f} {unit}"
        number /= 1024
    raise AssertionError("unreachable")


def is_fasta_name(path: str) -> bool:
    return path.lower().endswith(FASTA_SUFFIXES)


def is_gff_name(path: str) -> bool:
    return path.lower().endswith(GFF_SUFFIXES)


def strip_compression_suffix(path: str) -> str:
    lower = path.lower()
    if lower.endswith(".gz") or lower.endswith(".bz2"):
        return path.rsplit(".", 1)[0]
    return path


def output_member_name(member_name: str) -> str:
    base = strip_compression_suffix(member_name)
    lower = base.lower()
    for suffix in (".gff3", ".gff"):
        if lower.endswith(suffix):
            return base[: -len(suffix)] + ".fna"
    return base


def is_plain_fasta(path: Path) -> bool:
    return path.name.lower().endswith((".fa", ".fasta", ".fna", ".fas"))


def safe_target(root: Path, member_name: str) -> Path:
    target = (root / member_name).resolve()
    root_resolved = root.resolve()
    if target != root_resolved and not str(target).startswith(str(root_resolved) + os.sep):
        raise SystemExit(f"Unsafe tar member path: {member_name}")
    return target


@contextmanager
def open_member_payload(member_name: str, source: BinaryIO) -> Iterator[BinaryIO]:
    lower = member_name.lower()
    if lower.endswith(".bz2"):
        with bz2.BZ2File(source) as handle:
            yield handle
    elif lower.endswith(".gz"):
        with gzip.GzipFile(fileobj=source) as handle:
            yield handle
    else:
        yield source


def extract_gff_fasta(payload: BinaryIO, output: BinaryIO | None = None) -> tuple[int, int, int]:
    """Copy the GFF ##FASTA section and return headers, bases, and FASTA lines."""
    in_fasta = False
    headers = 0
    bases = 0
    lines = 0

    for raw in payload:
        line = raw.rstrip(b"\r\n")
        if not in_fasta:
            if line.strip() == b"##FASTA":
                in_fasta = True
            continue
        if not line:
            continue
        if line.startswith(b">"):
            headers += 1
        else:
            bases += len(line)
        lines += 1
        if output is not None:
            output.write(line + b"\n")

    return headers, bases, lines


root = Path(os.environ["ROOT_DIR"]).expanduser().resolve()
force_extract = os.environ.get("FORCE_EXTRACT") == "1"
inspect_only = os.environ.get("INSPECT_ONLY") == "1"
skip_size_check = os.environ.get("SKIP_SIZE_CHECK") == "1"
log_every = int(os.environ.get("LOG_EVERY", "200"))

if log_every <= 0:
    raise SystemExit("--log-every must be positive")

download_dir = root / "downloads" / SLUG
archive_path = download_dir / ARCHIVE_NAME
extract_dir = download_dir / "extracted"
filelist_dir = root / "corpus" / "cluster_inputs" / "rabbittclust"
filelist = filelist_dir / f"{SLUG}.list"

if not archive_path.exists():
    raise SystemExit(f"Missing archive: {archive_path}")

archive_bytes = archive_path.stat().st_size
if archive_bytes == 0:
    raise SystemExit(f"Archive is empty: {archive_path}")

if not skip_size_check and archive_bytes != EXPECTED_ARCHIVE_BYTES:
    raise SystemExit(
        f"Archive size mismatch for {ARCHIVE_NAME}: "
        f"{archive_bytes} != {EXPECTED_ARCHIVE_BYTES}. "
        "Rerun the download script with resume support, or pass --skip-size-check only after manual verification."
    )

extract_dir.mkdir(parents=True, exist_ok=True)
filelist_dir.mkdir(parents=True, exist_ok=True)

entries = 0
direct_fasta_members = 0
gff_members = 0
gff_with_fasta = 0
gff_without_fasta = 0
sequence_sources = 0
member_bytes = 0
gff_fasta_bases = 0
extracted = 0
skipped = 0
targets_seen: set[str] = set()
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
                    f"direct_fastas={direct_fasta_members}; gff={gff_members}; "
                    f"gff_with_fasta={gff_with_fasta}; extracted={extracted}; "
                    f"skipped={skipped}; elapsed={elapsed:.1f}s",
                    flush=True,
                )

            if not member.isfile():
                continue

            is_fasta = is_fasta_name(member.name)
            is_gff = is_gff_name(member.name)
            if not is_fasta and not is_gff:
                continue

            member_bytes += member.size
            target_name = output_member_name(member.name)
            if target_name in targets_seen:
                raise SystemExit(f"Duplicate materialized target from archive members: {target_name}")
            targets_seen.add(target_name)

            if is_fasta:
                direct_fasta_members += 1
                sequence_sources += 1
                if inspect_only:
                    continue

                target = safe_target(extract_dir, target_name)
                if not force_extract and target.exists() and target.stat().st_size > 0:
                    skipped += 1
                    continue

                source = tar.extractfile(member)
                if source is None:
                    raise SystemExit(f"Could not extract tar member: {member.name}")

                target.parent.mkdir(parents=True, exist_ok=True)
                tmp = target.with_name(target.name + ".tmp")
                with source:
                    with open_member_payload(member.name, source) as payload:
                        with tmp.open("wb") as out:
                            shutil.copyfileobj(payload, out, length=1024 * 1024)
                tmp.replace(target)
                extracted += 1
                continue

            gff_members += 1
            target = safe_target(extract_dir, target_name)
            if not inspect_only and not force_extract and target.exists() and target.stat().st_size > 0:
                gff_with_fasta += 1
                sequence_sources += 1
                skipped += 1
                continue

            source = tar.extractfile(member)
            if source is None:
                raise SystemExit(f"Could not extract tar member: {member.name}")

            with source:
                with open_member_payload(member.name, source) as payload:
                    if inspect_only:
                        headers, bases, _ = extract_gff_fasta(payload)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        tmp = target.with_name(target.name + ".tmp")
                        with tmp.open("wb") as out:
                            headers, bases, _ = extract_gff_fasta(payload, out)
                        if headers == 0:
                            tmp.unlink(missing_ok=True)
                        else:
                            tmp.replace(target)

            if headers == 0:
                gff_without_fasta += 1
                continue

            gff_with_fasta += 1
            sequence_sources += 1
            gff_fasta_bases += bases
            if not inspect_only:
                extracted += 1
except (tarfile.TarError, EOFError, OSError) as exc:
    raise SystemExit(f"Failed to read {archive_path}: {exc}") from exc

if sequence_sources != EXPECTED_GENOME_COUNT:
    raise SystemExit(
        f"Unexpected genome sequence source count: "
        f"{sequence_sources} != {EXPECTED_GENOME_COUNT}. "
        f"direct_fastas={direct_fasta_members}; gff_with_fasta={gff_with_fasta}; "
        f"gff_without_fasta={gff_without_fasta}"
    )

elapsed = time.time() - started
print(
    f"[done] {ARCHIVE_NAME}: entries={entries}; sequence_sources={sequence_sources}; "
    f"direct_fastas={direct_fasta_members}; gff={gff_members}; "
    f"gff_with_fasta={gff_with_fasta}; gff_without_fasta={gff_without_fasta}; "
    f"member_bytes={member_bytes} ({human_bytes(member_bytes)}); "
    f"gff_fasta_bases={gff_fasta_bases}; extracted={extracted}; "
    f"skipped={skipped}; elapsed={elapsed:.1f}s",
    flush=True,
)

if inspect_only:
    print(f"dataset: {SLUG}")
    print("mode: inspect-only")
    print(f"archive: {archive_path}")
    print(f"archive_bytes: {archive_bytes}")
    print(f"expected_filelist_entries: {sequence_sources}")
    print(f"direct_fasta_members: {direct_fasta_members}")
    print(f"gff_members: {gff_members}")
    print(f"gff_with_fasta: {gff_with_fasta}")
    print(f"gff_without_fasta: {gff_without_fasta}")
    print(f"member_bytes: {member_bytes} ({human_bytes(member_bytes)})")
    print(f"gff_fasta_bases: {gff_fasta_bases}")
    print(f"extract_dir: {extract_dir}")
    raise SystemExit(0)

fastas = sorted(
    path
    for path in extract_dir.rglob("*")
    if path.is_file() and is_plain_fasta(path)
)

if len(fastas) != EXPECTED_GENOME_COUNT:
    raise SystemExit(f"Unexpected extracted FASTA count: {len(fastas)} != {EXPECTED_GENOME_COUNT}")

with filelist.open("w", encoding="utf-8") as handle:
    for fasta in fastas:
        handle.write(str(fasta.resolve()) + "\n")

materialized_bytes = sum(path.stat().st_size for path in fastas)
print(f"dataset: {SLUG}")
print(f"archive: {archive_path}")
print(f"archive_bytes: {archive_bytes}")
print(f"extract_dir: {extract_dir}")
print(f"filelist: {filelist}")
print(f"filelist_entries: {len(fastas)}")
print(f"member_bytes: {member_bytes} ({human_bytes(member_bytes)})")
print(f"gff_fasta_bases: {gff_fasta_bases}")
print(f"materialized_fasta_bytes: {materialized_bytes} ({human_bytes(materialized_bytes)})")
print(f"first_entry: {fastas[0].resolve()}")
print(f"last_entry: {fastas[-1].resolve()}")
PY
