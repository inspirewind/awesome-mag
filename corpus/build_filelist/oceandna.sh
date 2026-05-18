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
import tarfile
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
TAR_ARCHIVE_SUFFIXES = (
    ".tar",
    ".tar.gz",
    ".tgz",
    ".tar.bz2",
    ".tbz2",
    ".tar.xz",
    ".txz",
)
ZIP_ARCHIVE_SUFFIXES = (".zip",)


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


def is_tar_archive(path: str) -> bool:
    return path.lower().endswith(TAR_ARCHIVE_SUFFIXES)


def is_zip_archive(path: str) -> bool:
    lower = path.lower()
    return lower.endswith(ZIP_ARCHIVE_SUFFIXES) and not is_fasta(lower)


def archive_label(path: str) -> str:
    name = Path(path).name
    lower = name.lower()
    for suffix in (
        ".tar.gz",
        ".tar.bz2",
        ".tar.xz",
        ".tgz",
        ".tbz2",
        ".txz",
        ".tar",
        ".zip",
    ):
        if lower.endswith(suffix):
            return name[: -len(suffix)]
    return Path(name).stem


def output_member_name(member_name: str) -> str:
    if member_name.lower().endswith(".bz2"):
        return member_name.rsplit(".", 1)[0]
    return member_name


def safe_target(root: Path, member_name: str) -> Path:
    target = (root / member_name).resolve()
    root_resolved = root.resolve()
    if target != root_resolved and not str(target).startswith(str(root_resolved) + os.sep):
        raise SystemExit(f"Unsafe archive member path: {member_name}")
    return target


def copy_fasta_member(source, source_name: str, target: Path, expected_size: int, state: dict[str, int]) -> None:
    if not force_extract and target.exists():
        if source_name.lower().endswith(".bz2"):
            if target.stat().st_size > 0:
                state["skipped"] += 1
                return
        elif target.stat().st_size == expected_size:
            state["skipped"] += 1
            return

    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(target.name + ".tmp")
    with source, tmp.open("wb") as out:
        if source_name.lower().endswith(".bz2"):
            with bz2.BZ2File(source) as decompressed:
                shutil.copyfileobj(decompressed, out, length=8 * 1024 * 1024)
        else:
            shutil.copyfileobj(source, out, length=8 * 1024 * 1024)
    tmp.replace(target)
    state["extracted"] += 1


def log_progress(archive_name: str, state: dict[str, int], started: float) -> None:
    if state["entries"] % log_every != 0:
        return
    elapsed = time.time() - started
    print(
        f"[scan] {archive_name}: entries={state['entries']}; "
        f"fastas={state['fastas']}; extracted={state['extracted']}; "
        f"skipped={state['skipped']}; elapsed={elapsed:.1f}s",
        flush=True,
    )


def process_zip_fastas(
    archive: zipfile.ZipFile,
    infos: list[zipfile.ZipInfo],
    *,
    archive_name: str,
    target_root: Path,
    summary,
    state: dict[str, int],
    started: float,
) -> None:
    for info in infos:
        state["entries"] += 1
        log_progress(archive_name, state, started)
        if info.is_dir() or not is_fasta(info.filename):
            continue

        state["fastas"] += 1
        state["fasta_bytes"] += info.file_size
        summary.write(f"{archive_name}!{info.filename}\t{info.compress_size}\t{info.file_size}\n")
        if inspect_only:
            continue

        target = safe_target(target_root, output_member_name(info.filename))
        source = archive.open(info)
        copy_fasta_member(source, info.filename, target, info.file_size, state)


def process_tar_fastas(
    fileobj,
    *,
    archive_name: str,
    target_root: Path,
    summary,
    state: dict[str, int],
    started: float,
) -> None:
    with tarfile.open(fileobj=fileobj, mode="r|*") as tar:
        for member in tar:
            state["entries"] += 1
            log_progress(archive_name, state, started)
            if not member.isfile() or not is_fasta(member.name):
                continue

            state["fastas"] += 1
            state["fasta_bytes"] += member.size
            summary.write(f"{archive_name}!{member.name}\t\t{member.size}\n")
            if inspect_only:
                continue

            source = tar.extractfile(member)
            if source is None:
                raise SystemExit(f"Could not extract tar member: {archive_name}!{member.name}")

            target = safe_target(target_root, output_member_name(member.name))
            copy_fasta_member(source, member.name, target, member.size, state)


def materialize_nested_zip(archive: zipfile.ZipFile, info: zipfile.ZipInfo, cache_dir: Path) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    target = cache_dir / Path(info.filename).name
    if not force_extract and target.exists() and target.stat().st_size == info.file_size:
        return target

    tmp = target.with_name(target.name + ".tmp")
    with archive.open(info) as source, tmp.open("wb") as out:
        shutil.copyfileobj(source, out, length=8 * 1024 * 1024)
    tmp.replace(target)
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

state = {"entries": 0, "fastas": 0, "fasta_bytes": 0, "extracted": 0, "skipped": 0}
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
        infos = archive.infolist()
        direct_fastas = [info for info in infos if not info.is_dir() and is_fasta(info.filename)]
        nested_tars = [info for info in infos if not info.is_dir() and is_tar_archive(info.filename)]
        nested_zips = [info for info in infos if not info.is_dir() and is_zip_archive(info.filename)]

        if direct_fastas:
            print(
                f"[scan] {zip_path.name}: found {len(direct_fastas)} direct FASTA member(s) in outer ZIP",
                flush=True,
            )
            process_zip_fastas(
                archive,
                infos,
                archive_name=zip_path.name,
                target_root=extract_dir,
                summary=summary,
                state=state,
                started=started,
            )
        elif nested_tars:
            print(
                f"[scan] {zip_path.name}: no direct FASTA members; "
                f"streaming {len(nested_tars)} nested tar archive(s)",
                flush=True,
            )
            for info in nested_tars:
                label = archive_label(info.filename)
                target_root = extract_dir / label
                print(
                    f"[scan] nested tar: {info.filename} "
                    f"({human_bytes(info.file_size)} uncompressed ZIP member bytes)",
                    flush=True,
                )
                with archive.open(info) as source:
                    process_tar_fastas(
                        source,
                        archive_name=info.filename,
                        target_root=target_root,
                        summary=summary,
                        state=state,
                        started=started,
                    )
        elif nested_zips:
            print(
                f"[scan] {zip_path.name}: no direct FASTA members; "
                f"materializing {len(nested_zips)} nested ZIP archive(s)",
                flush=True,
            )
            nested_cache_dir = download_dir / "nested_archives"
            for info in nested_zips:
                label = archive_label(info.filename)
                target_root = extract_dir / label
                print(
                    f"[scan] nested zip: {info.filename} "
                    f"({human_bytes(info.file_size)} uncompressed ZIP member bytes)",
                    flush=True,
                )
                nested_zip_path = materialize_nested_zip(archive, info, nested_cache_dir)
                with zipfile.ZipFile(nested_zip_path) as nested_archive:
                    nested_infos = nested_archive.infolist()
                    nested_direct_fastas = [
                        nested_info
                        for nested_info in nested_infos
                        if not nested_info.is_dir() and is_fasta(nested_info.filename)
                    ]
                    nested_tar_infos = [
                        nested_info
                        for nested_info in nested_infos
                        if not nested_info.is_dir() and is_tar_archive(nested_info.filename)
                    ]
                    if nested_direct_fastas:
                        process_zip_fastas(
                            nested_archive,
                            nested_infos,
                            archive_name=info.filename,
                            target_root=target_root,
                            summary=summary,
                            state=state,
                            started=started,
                        )
                    elif nested_tar_infos:
                        for nested_tar in nested_tar_infos:
                            nested_tar_label = archive_label(nested_tar.filename)
                            nested_tar_target_root = target_root / nested_tar_label
                            print(
                                f"[scan] nested tar: {info.filename}!{nested_tar.filename} "
                                f"({human_bytes(nested_tar.file_size)} uncompressed ZIP member bytes)",
                                flush=True,
                            )
                            with nested_archive.open(nested_tar) as source:
                                process_tar_fastas(
                                    source,
                                    archive_name=f"{info.filename}!{nested_tar.filename}",
                                    target_root=nested_tar_target_root,
                                    summary=summary,
                                    state=state,
                                    started=started,
                                )
                    else:
                        preview = "\n".join(
                            f"  {nested_info.file_size}\t{nested_info.filename}"
                            for nested_info in nested_infos[:40]
                        )
                        raise SystemExit(
                            "No FASTA or supported nested tar archive was found in "
                            f"nested ZIP {info.filename}. First members:\n{preview}"
                        )
        else:
            preview = "\n".join(
                f"  {info.file_size}\t{info.filename}" for info in infos[:40]
            )
            raise SystemExit(
                "No FASTA or supported nested tar archive was found in the "
                f"Figshare ZIP. First members:\n{preview}"
            )
except (zipfile.BadZipFile, tarfile.TarError, EOFError, OSError) as exc:
    raise SystemExit(
        f"Failed to read {zip_path}: {exc}. "
        "The ZIP is likely incomplete; rerun the OceanDNA download script to resume."
    ) from exc

nonrep_fastas = state["fastas"]
nonrep_fasta_bytes = state["fasta_bytes"]
extracted = state["extracted"]
skipped = state["skipped"]
entries = state["entries"]

if nonrep_fastas != expected_nonrep:
    raise SystemExit(
        f"Unexpected non-representative FASTA count: {nonrep_fastas} != {expected_nonrep}. "
        f"See {members_tsv} for the archive members that were recognized."
    )

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
