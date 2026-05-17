#!/usr/bin/env bash
set -euo pipefail

# dataset: MAGdb
# slug: magdb
# clustering: RabbitTClust
# input archives: downloads/magdb/<category>/<study-title>.tar.gz
# output filelist: corpus/cluster_inputs/rabbittclust/magdb.list
#
# MAGdb is distributed as per-study data.tar.gz archives behind an authenticated
# browser session. This builder assumes those archives have already been
# downloaded with scripts/magdb/download.py and treats each nucleotide FASTA
# member inside each study archive as one MAG file.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
FORCE_EXTRACT=0
INSPECT_ONLY=0
EXPECTED_FASTA_COUNT=99672
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
    --inspect-only)
      INSPECT_ONLY=1
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
export FORCE_EXTRACT
export INSPECT_ONLY
export EXPECTED_FASTA_COUNT
export LOG_EVERY

python3 - <<'PY'
from __future__ import annotations

import bz2
import gzip
import os
import shutil
import tarfile
import time
from pathlib import Path


SLUG = "magdb"
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
ARCHIVE_SUFFIXES = (".tar.gz", ".tgz", ".tar")


def human_bytes(value: int) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    number = float(value)
    for unit in units:
        if number < 1024 or unit == units[-1]:
            return f"{number:.2f} {unit}"
        number /= 1024
    raise AssertionError("unreachable")


def is_archive(path: Path) -> bool:
    name = path.name.lower()
    return (
        name.endswith(ARCHIVE_SUFFIXES)
        and not name.endswith(".part")
        and ".part." not in name
    )


def archive_stem(path: Path) -> str:
    name = path.name
    lower = name.lower()
    for suffix in ARCHIVE_SUFFIXES:
        if lower.endswith(suffix):
            return name[: -len(suffix)]
    return path.stem


def is_fasta(path: str) -> bool:
    return path.lower().endswith(FASTA_SUFFIXES)


def output_member_name(member_name: str) -> str:
    lower = member_name.lower()
    if lower.endswith(".bz2") or lower.endswith(".gz"):
        return member_name.rsplit(".", 1)[0]
    return member_name


def is_plain_fasta(path: Path) -> bool:
    return path.name.lower().endswith((".fa", ".fasta", ".fna", ".fas"))


def safe_target(root: Path, member_name: str) -> Path:
    target = (root / member_name).resolve()
    root_resolved = root.resolve()
    if target != root_resolved and not str(target).startswith(str(root_resolved) + os.sep):
        raise SystemExit(f"Unsafe tar member path: {member_name}")
    return target


def archive_output_root(download_dir: Path, extract_dir: Path, archive_path: Path) -> Path:
    rel = archive_path.relative_to(download_dir)
    parent = rel.parent
    return extract_dir / parent / archive_stem(archive_path)


root = Path(os.environ["ROOT_DIR"]).expanduser().resolve()
force_extract = os.environ.get("FORCE_EXTRACT") == "1"
inspect_only = os.environ.get("INSPECT_ONLY") == "1"
expected_fasta_count = int(os.environ.get("EXPECTED_FASTA_COUNT", "99672"))
log_every = int(os.environ.get("LOG_EVERY", "1000"))

if expected_fasta_count < 0:
    raise SystemExit("--expected-count must be non-negative")
if log_every <= 0:
    raise SystemExit("--log-every must be positive")

download_dir = root / "downloads" / SLUG
extract_dir = download_dir / "extracted"
filelist_dir = root / "corpus" / "cluster_inputs" / "rabbittclust"
filelist = filelist_dir / f"{SLUG}.list"
debug_dir = root / "corpus" / "cluster_inputs" / "debug"
summary_tsv = debug_dir / "magdb.archives.tsv"

if not download_dir.exists():
    raise SystemExit(
        f"Missing MAGdb download directory: {download_dir}\n"
        "Download archives first with scripts/magdb/download.py."
    )

archives = sorted(
    path
    for path in download_dir.rglob("*")
    if path.is_file()
    and is_archive(path)
    and "extracted" not in path.relative_to(download_dir).parts
)

if not archives:
    raise SystemExit(
        f"No MAGdb study archives found under {download_dir}. "
        "Expected files like downloads/magdb/clinical/<study>.tar.gz."
    )

extract_dir.mkdir(parents=True, exist_ok=True)
filelist_dir.mkdir(parents=True, exist_ok=True)
debug_dir.mkdir(parents=True, exist_ok=True)

total_entries = 0
total_fastas = 0
total_fasta_bytes = 0
total_extracted = 0
total_skipped = 0
errors: list[str] = []
archive_roots: list[Path] = []
started_all = time.time()

with summary_tsv.open("w", encoding="utf-8") as summary:
    summary.write(
        "archive\tarchive_bytes\tentries\tfastas\tfasta_bytes\textracted\t"
        "skipped\telapsed_seconds\tstatus\n"
    )

    print(f"[discover] {SLUG}: archives={len(archives)}", flush=True)
    for archive_index, archive_path in enumerate(archives, start=1):
        rel_archive = archive_path.relative_to(download_dir)
        archive_bytes = archive_path.stat().st_size
        if archive_bytes == 0:
            message = f"{rel_archive}: archive is empty"
            errors.append(message)
            summary.write(f"{rel_archive}\t0\t0\t0\t0\t0\t0\t0.0\tempty\n")
            print(f"[error] {message}", flush=True)
            continue

        archive_root = archive_output_root(download_dir, extract_dir, archive_path)
        archive_roots.append(archive_root)
        entries = 0
        fasta_count = 0
        fasta_bytes = 0
        extracted = 0
        skipped = 0
        started = time.time()

        print(
            f"[scan] [{archive_index}/{len(archives)}] {rel_archive}: start "
            f"({human_bytes(archive_bytes)})",
            flush=True,
        )
        try:
            with tarfile.open(archive_path, mode="r|*") as tar:
                for member in tar:
                    entries += 1
                    if entries % log_every == 0:
                        elapsed = time.time() - started
                        print(
                            f"[scan] [{archive_index}/{len(archives)}] {rel_archive}: "
                            f"entries={entries}; fastas={fasta_count}; "
                            f"extracted={extracted}; skipped={skipped}; "
                            f"elapsed={elapsed:.1f}s",
                            flush=True,
                        )

                    if not member.isfile() or not is_fasta(member.name):
                        continue

                    fasta_count += 1
                    fasta_bytes += member.size
                    if inspect_only:
                        continue

                    target = safe_target(archive_root, output_member_name(member.name))
                    if not force_extract and target.exists() and target.stat().st_size > 0:
                        skipped += 1
                        continue

                    source = tar.extractfile(member)
                    if source is None:
                        raise OSError(f"Could not extract tar member: {member.name}")

                    target.parent.mkdir(parents=True, exist_ok=True)
                    tmp = target.with_name(target.name + ".tmp")
                    lower = member.name.lower()
                    with source, tmp.open("wb") as out:
                        if lower.endswith(".bz2"):
                            with bz2.BZ2File(source) as decompressed:
                                shutil.copyfileobj(decompressed, out, length=1024 * 1024)
                        elif lower.endswith(".gz"):
                            with gzip.GzipFile(fileobj=source) as decompressed:
                                shutil.copyfileobj(decompressed, out, length=1024 * 1024)
                        else:
                            shutil.copyfileobj(source, out, length=1024 * 1024)
                    tmp.replace(target)
                    extracted += 1
        except (tarfile.TarError, EOFError, OSError) as exc:
            elapsed = time.time() - started
            message = f"{rel_archive}: {exc}"
            errors.append(message)
            summary.write(
                f"{rel_archive}\t{archive_bytes}\t{entries}\t{fasta_count}\t"
                f"{fasta_bytes}\t{extracted}\t{skipped}\t{elapsed:.1f}\terror: {exc}\n"
            )
            print(f"[error] {message}", flush=True)
            if not inspect_only:
                raise SystemExit(
                    "MAGdb extraction stopped because a study archive could not be read. "
                    "Rerun inspect-only for the full error list."
                ) from exc
            continue

        elapsed = time.time() - started
        total_entries += entries
        total_fastas += fasta_count
        total_fasta_bytes += fasta_bytes
        total_extracted += extracted
        total_skipped += skipped
        summary.write(
            f"{rel_archive}\t{archive_bytes}\t{entries}\t{fasta_count}\t"
            f"{fasta_bytes}\t{extracted}\t{skipped}\t{elapsed:.1f}\tok\n"
        )
        print(
            f"[done] [{archive_index}/{len(archives)}] {rel_archive}: "
            f"entries={entries}; fastas={fasta_count}; "
            f"fasta_bytes={fasta_bytes} ({human_bytes(fasta_bytes)}); "
            f"extracted={extracted}; skipped={skipped}; elapsed={elapsed:.1f}s",
            flush=True,
        )

elapsed_all = time.time() - started_all

if inspect_only:
    print(f"dataset: {SLUG}")
    print("mode: inspect-only")
    print(f"download_dir: {download_dir}")
    print(f"archive_count: {len(archives)}")
    print(f"expected_filelist_entries: {expected_fasta_count}")
    print(f"observed_fasta_entries: {total_fastas}")
    print(f"member_fasta_bytes: {total_fasta_bytes} ({human_bytes(total_fasta_bytes)})")
    print(f"summary_tsv: {summary_tsv}")
    print(f"extract_dir: {extract_dir}")
    print(f"errors: {len(errors)}")
    if errors:
        for error in errors[:20]:
            print(f"error: {error}")
        if len(errors) > 20:
            print(f"error: ... {len(errors) - 20} more; see {summary_tsv}")
    if expected_fasta_count and total_fastas != expected_fasta_count:
        print(
            f"warning: observed_fasta_entries {total_fastas} != "
            f"expected_filelist_entries {expected_fasta_count}"
        )
    raise SystemExit(0 if not errors else 1)

if errors:
    raise SystemExit(f"Archive errors encountered; see {summary_tsv}")

if expected_fasta_count and total_fastas != expected_fasta_count:
    raise SystemExit(
        f"Unexpected MAGdb FASTA count: {total_fastas} != {expected_fasta_count}. "
        "Use --inspect-only to review downloaded package coverage, or pass "
        "--expected-count after explicitly choosing a subset."
    )

fastas = sorted(
    path
    for archive_root in archive_roots
    for path in archive_root.rglob("*")
    if path.is_file() and is_plain_fasta(path)
)

if len(fastas) != total_fastas:
    raise SystemExit(f"Unexpected extracted FASTA count: {len(fastas)} != {total_fastas}")

with filelist.open("w", encoding="utf-8") as handle:
    for fasta in fastas:
        handle.write(str(fasta.resolve()) + "\n")

materialized_bytes = sum(path.stat().st_size for path in fastas)
print(f"dataset: {SLUG}")
print(f"archive_count: {len(archives)}")
print(f"download_dir: {download_dir}")
print(f"extract_dir: {extract_dir}")
print(f"summary_tsv: {summary_tsv}")
print(f"filelist: {filelist}")
print(f"filelist_entries: {len(fastas)}")
print(f"member_fasta_bytes: {total_fasta_bytes} ({human_bytes(total_fasta_bytes)})")
print(f"materialized_fasta_bytes: {materialized_bytes} ({human_bytes(materialized_bytes)})")
print(f"elapsed_seconds: {elapsed_all:.1f}")
print(f"first_entry: {fastas[0].resolve()}")
print(f"last_entry: {fastas[-1].resolve()}")
PY
