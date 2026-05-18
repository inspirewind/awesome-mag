#!/usr/bin/env bash
set -euo pipefail

# dataset: RUG2 Rumen MAGs
# slug: rug2
# clustering: RabbitTClust
# input files: downloads/rug2/assemblies/*.fa.gz
# output filelist: corpus/cluster_inputs/rabbittclust/rug2.list
#
# The downloader filters ENA analysis records to binned metagenome assembly
# FASTA files. This is a public sequence superset of the 4,941 final RUGs.
# RabbitTClust can read gzip FASTA, so this builder writes direct paths without
# materializing decompressed copies.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
INSPECT_ONLY=0
GZIP_TEST=0
EXPECTED_FASTA_COUNT=20567
LOG_EVERY=1000

while [ "$#" -gt 0 ]; do
  case "$1" in
    --root)
      ROOT_DIR="$(cd "$2" && pwd)"
      shift 2
      ;;
    --inspect-only)
      INSPECT_ONLY=1
      shift
      ;;
    --gzip-test)
      GZIP_TEST=1
      shift
      ;;
    --expected-count)
      EXPECTED_FASTA_COUNT="$2"
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
export INSPECT_ONLY
export GZIP_TEST
export EXPECTED_FASTA_COUNT
export LOG_EVERY

python3 - <<'PY'
from __future__ import annotations

import gzip
import os
import time
from pathlib import Path


SLUG = "rug2"
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


def human_bytes(value: int) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    number = float(value)
    for unit in units:
        if number < 1024 or unit == units[-1]:
            return f"{number:.2f} {unit}"
        number /= 1024
    raise AssertionError("unreachable")


def is_fasta(path: Path) -> bool:
    return path.name.lower().endswith(FASTA_SUFFIXES)


def gzip_crc_test(path: Path) -> None:
    with gzip.open(path, "rb") as handle:
        for _ in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            pass


root = Path(os.environ["ROOT_DIR"]).expanduser().resolve()
inspect_only = os.environ.get("INSPECT_ONLY") == "1"
gzip_test = os.environ.get("GZIP_TEST") == "1"
expected_fasta_count = int(os.environ.get("EXPECTED_FASTA_COUNT", "20567"))
log_every = int(os.environ.get("LOG_EVERY", "1000"))

if expected_fasta_count < 0:
    raise SystemExit("--expected-count must be non-negative")
if log_every <= 0:
    raise SystemExit("--log-every must be positive")

download_dir = root / "downloads" / SLUG
assemblies_dir = download_dir / "assemblies"
manifest = download_dir / "manifest.tsv"
filelist_dir = root / "corpus" / "cluster_inputs" / "rabbittclust"
debug_dir = root / "corpus" / "cluster_inputs" / "debug"
filelist = filelist_dir / f"{SLUG}.list"
members_tsv = debug_dir / "rug2.members.tsv"

if not assemblies_dir.exists():
    raise SystemExit(f"Missing assemblies directory: {assemblies_dir}")

filelist_dir.mkdir(parents=True, exist_ok=True)
debug_dir.mkdir(parents=True, exist_ok=True)

started = time.time()
fastas = sorted(path for path in assemblies_dir.rglob("*") if path.is_file() and is_fasta(path))
zero_size = [path for path in fastas if path.stat().st_size == 0]
total_bytes = sum(path.stat().st_size for path in fastas)

if zero_size:
    preview = "\n".join(str(path) for path in zero_size[:10])
    raise SystemExit(f"{len(zero_size)} RUG2 FASTA files are zero-size:\n{preview}")

if expected_fasta_count and len(fastas) != expected_fasta_count:
    raise SystemExit(
        f"Unexpected RUG2 FASTA count: {len(fastas)} != {expected_fasta_count}. "
        "The server inventory previously showed 5,364 files, which means the ENA download was incomplete. "
        "Rerun corpus/download_bash/part4_hard_datasets/rug2.sh to resume, or pass --expected-count "
        "only after intentionally choosing a smaller subset."
    )

with members_tsv.open("w", encoding="utf-8") as summary:
    summary.write("path\tsize\n")
    for index, fasta in enumerate(fastas, start=1):
        if index % log_every == 0:
            elapsed = time.time() - started
            print(
                f"[scan] {SLUG}: files={index}; bytes={total_bytes} "
                f"({human_bytes(total_bytes)}); elapsed={elapsed:.1f}s",
                flush=True,
            )
        summary.write(f"{fasta.resolve()}\t{fasta.stat().st_size}\n")

if gzip_test:
    print(f"[gzip-test] {SLUG}: start; files={len(fastas)}", flush=True)
    for index, fasta in enumerate(fastas, start=1):
        if not fasta.name.lower().endswith(".gz"):
            continue
        try:
            gzip_crc_test(fasta)
        except OSError as exc:
            raise SystemExit(f"gzip integrity check failed for {fasta}: {exc}") from exc
        if index % log_every == 0:
            elapsed = time.time() - started
            print(f"[gzip-test] {SLUG}: checked={index}; elapsed={elapsed:.1f}s", flush=True)
    print(f"[gzip-test] {SLUG}: OK", flush=True)

elapsed = time.time() - started
print(
    f"[done] {SLUG}: fastas={len(fastas)}; bytes={total_bytes} "
    f"({human_bytes(total_bytes)}); elapsed={elapsed:.1f}s",
    flush=True,
)

if inspect_only:
    print(f"dataset: {SLUG}")
    print("mode: inspect-only")
    print(f"assemblies_dir: {assemblies_dir}")
    print(f"manifest: {manifest if manifest.exists() else 'missing'}")
    print(f"expected_filelist_entries: {expected_fasta_count}")
    print(f"observed_fasta_entries: {len(fastas)}")
    print(f"member_fasta_bytes: {total_bytes} ({human_bytes(total_bytes)})")
    print(f"gzip_test: {'yes' if gzip_test else 'no'}")
    print(f"members_tsv: {members_tsv}")
    raise SystemExit(0)

with filelist.open("w", encoding="utf-8") as handle:
    for fasta in fastas:
        handle.write(str(fasta.resolve()) + "\n")

print(f"dataset: {SLUG}")
print(f"assemblies_dir: {assemblies_dir}")
print(f"manifest: {manifest if manifest.exists() else 'missing'}")
print(f"filelist: {filelist}")
print(f"filelist_entries: {len(fastas)}")
print(f"member_fasta_bytes: {total_bytes} ({human_bytes(total_bytes)})")
print(f"gzip_test: {'yes' if gzip_test else 'no'}")
print(f"members_tsv: {members_tsv}")
print(f"first_entry: {fastas[0].resolve()}")
print(f"last_entry: {fastas[-1].resolve()}")
PY
