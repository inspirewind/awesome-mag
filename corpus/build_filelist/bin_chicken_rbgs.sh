#!/usr/bin/env bash
set -euo pipefail

# dataset: Bin Chicken Rare Biosphere Genomes
# slug: bin-chicken-rbgs
# clustering: RabbitTClust
# input archives:
#   downloads/bin-chicken-rbgs/binchicken_RBGs_aquatic.tar.gz
#   downloads/bin-chicken-rbgs/binchicken_RBGs_terrestrial_engineered_host.tar.gz
# output filelist: corpus/cluster_inputs/rabbittclust/bin-chicken-rbgs.list

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
FORCE_EXTRACT=0
VERIFY_MD5=0
INSPECT_ONLY=0
LOG_EVERY=5000

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
from dataclasses import dataclass
from pathlib import Path


SLUG = "bin-chicken-rbgs"
FASTA_SUFFIXES = (
    ".fa",
    ".fasta",
    ".fna",
    ".fas",
    ".fa.gz",
    ".fasta.gz",
    ".fna.gz",
    ".fas.gz",
)


@dataclass(frozen=True)
class ArchiveSpec:
    name: str
    label: str
    expected_bytes: int
    expected_md5: str
    expected_fastas: int


ARCHIVES = (
    ArchiveSpec(
        name="binchicken_RBGs_aquatic.tar.gz",
        label="aquatic",
        expected_bytes=33_823_795_732,
        expected_md5="88a477f645d857c12d160d262e1ca383",
        expected_fastas=44_481,
    ),
    ArchiveSpec(
        name="binchicken_RBGs_terrestrial_engineered_host.tar.gz",
        label="terrestrial_engineered_host",
        expected_bytes=33_499_575_163,
        expected_md5="2fcd0dd7c4359e542ddeccf291f3102c",
        expected_fastas=33_081,
    ),
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
    lower = path.lower()
    return lower.endswith(FASTA_SUFFIXES)


def md5sum(path: Path, *, log_every_bytes: int = 5 * 1024**3) -> str:
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
                print(
                    f"[md5] {path.name}: {human_bytes(seen)} read in {elapsed:.1f}s",
                    flush=True,
                )
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
log_every = int(os.environ.get("LOG_EVERY", "5000"))

download_dir = root / "downloads" / SLUG
extract_dir = download_dir / "extracted"
filelist_dir = root / "corpus" / "cluster_inputs" / "rabbittclust"
filelist = filelist_dir / f"{SLUG}.list"

if log_every <= 0:
    raise SystemExit("--log-every must be positive")

for spec in ARCHIVES:
    archive_path = download_dir / spec.name
    if not archive_path.exists():
        raise SystemExit(f"Missing archive: {archive_path}")
    observed_bytes = archive_path.stat().st_size
    if observed_bytes != spec.expected_bytes:
        raise SystemExit(
            f"Archive size mismatch for {spec.name}: "
            f"{observed_bytes} != {spec.expected_bytes}"
        )

    if verify_md5:
        print(f"[md5] verifying {archive_path}", flush=True)
        observed_md5 = md5sum(archive_path)
        if observed_md5 != spec.expected_md5:
            raise SystemExit(
                f"MD5 mismatch for {spec.name}: {observed_md5} != {spec.expected_md5}"
            )

extract_dir.mkdir(parents=True, exist_ok=True)
filelist_dir.mkdir(parents=True, exist_ok=True)

total_fastas = 0
total_uncompressed_fasta_bytes = 0

for spec in ARCHIVES:
    archive_path = download_dir / spec.name
    archive_extract_dir = extract_dir / spec.label
    archive_extract_dir.mkdir(parents=True, exist_ok=True)
    entries = 0
    fasta_count = 0
    fasta_bytes = 0
    extracted = 0
    skipped = 0
    started = time.time()

    print(f"[scan] {spec.name}: start", flush=True)
    try:
        with tarfile.open(archive_path, mode="r|gz") as tar:
            for member in tar:
                entries += 1
                if entries % log_every == 0:
                    elapsed = time.time() - started
                    print(
                        f"[scan] {spec.name}: entries={entries}; "
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

                target = safe_target(archive_extract_dir, member.name)
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

    if fasta_count != spec.expected_fastas:
        raise SystemExit(
            f"Unexpected FASTA count for {spec.name}: "
            f"{fasta_count} != {spec.expected_fastas}"
        )

    total_fastas += fasta_count
    total_uncompressed_fasta_bytes += fasta_bytes
    elapsed = time.time() - started
    print(
        f"[done] {spec.name}: entries={entries}; fastas={fasta_count}; "
        f"fasta_bytes={fasta_bytes} ({human_bytes(fasta_bytes)}); "
        f"extracted={extracted}; skipped={skipped}; elapsed={elapsed:.1f}s",
        flush=True,
    )

expected_total = sum(spec.expected_fastas for spec in ARCHIVES)
if total_fastas != expected_total:
    raise SystemExit(f"Unexpected total FASTA count: {total_fastas} != {expected_total}")

if inspect_only:
    print(f"dataset: {SLUG}")
    print(f"mode: inspect-only")
    print(f"archive_count: {len(ARCHIVES)}")
    print(f"expected_filelist_entries: {total_fastas}")
    print(
        f"uncompressed_fasta_bytes: {total_uncompressed_fasta_bytes} "
        f"({human_bytes(total_uncompressed_fasta_bytes)})"
    )
    print(f"extract_dir: {extract_dir}")
    raise SystemExit(0)

fastas: list[Path] = []
for spec in ARCHIVES:
    archive_extract_dir = extract_dir / spec.label
    fastas.extend(
        path
        for path in archive_extract_dir.rglob("*")
        if path.is_file() and is_fasta(path.name)
    )
fastas = sorted(fastas)

if len(fastas) != expected_total:
    raise SystemExit(f"Unexpected extracted FASTA count: {len(fastas)} != {expected_total}")

with filelist.open("w", encoding="utf-8") as handle:
    for fasta in fastas:
        handle.write(str(fasta.resolve()) + "\n")

print(f"dataset: {SLUG}")
print(f"archive_count: {len(ARCHIVES)}")
print(f"extract_dir: {extract_dir}")
print(f"filelist: {filelist}")
print(f"filelist_entries: {len(fastas)}")
print(f"uncompressed_fasta_bytes: {total_uncompressed_fasta_bytes} ({human_bytes(total_uncompressed_fasta_bytes)})")
print(f"first_entry: {fastas[0].resolve()}")
print(f"last_entry: {fastas[-1].resolve()}")
PY
