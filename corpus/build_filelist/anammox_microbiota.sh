#!/usr/bin/env bash
set -euo pipefail

# dataset: Anammox Microbiota Catalog
# slug: anammox-microbiota
# clustering: RabbitTClust
# input archive: downloads/anammox-microbiota/anammox_microbiota_figshare_45271516.zip
# output filelist: corpus/cluster_inputs/rabbittclust/anammox-microbiota.list

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SKIP_ZIP_TEST=0
FORCE_EXTRACT=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --root)
      ROOT_DIR="$(cd "$2" && pwd)"
      shift 2
      ;;
    --skip-zip-test)
      SKIP_ZIP_TEST=1
      shift
      ;;
    --force-extract)
      FORCE_EXTRACT=1
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

export ROOT_DIR
export SKIP_ZIP_TEST
export FORCE_EXTRACT

python3 - <<'PY'
from __future__ import annotations

import os
import shutil
import zipfile
from pathlib import Path

SLUG = "anammox-microbiota"
EXPECTED_ARCHIVE_BYTES = 1_865_155_640
EXPECTED_FASTA_COUNT = 1_768
ZIP_NAME = "anammox_microbiota_figshare_45271516.zip"

root = Path(os.environ["ROOT_DIR"]).expanduser().resolve()
skip_zip_test = os.environ.get("SKIP_ZIP_TEST") == "1"
force_extract = os.environ.get("FORCE_EXTRACT") == "1"

zip_path = root / "downloads" / SLUG / ZIP_NAME
extract_dir = root / "downloads" / SLUG / "extracted"
filelist_dir = root / "corpus" / "cluster_inputs" / "rabbittclust"
filelist = filelist_dir / f"{SLUG}.list"

if not zip_path.exists():
    raise SystemExit(f"Missing archive: {zip_path}")

archive_bytes = zip_path.stat().st_size
if archive_bytes != EXPECTED_ARCHIVE_BYTES:
    raise SystemExit(
        f"Archive size mismatch: {archive_bytes} != {EXPECTED_ARCHIVE_BYTES}; "
        "rerun corpus/download_bash/part4_hard_datasets/anammox_microbiota.sh first"
    )

extract_root = extract_dir.resolve()
extract_dir.mkdir(parents=True, exist_ok=True)
filelist_dir.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(zip_path) as zf:
    if not skip_zip_test:
        bad_member = zf.testzip()
        if bad_member is not None:
            raise SystemExit(f"ZIP integrity check failed at member: {bad_member}")

    fasta_members = [
        member
        for member in zf.infolist()
        if not member.is_dir() and member.filename.lower().endswith(".fa")
    ]
    if len(fasta_members) != EXPECTED_FASTA_COUNT:
        raise SystemExit(
            f"Unexpected FASTA count in ZIP: {len(fasta_members)} != {EXPECTED_FASTA_COUNT}"
        )

    extracted = 0
    skipped = 0
    for member in fasta_members:
        target = (extract_dir / member.filename).resolve()
        if not str(target).startswith(str(extract_root) + os.sep):
            raise SystemExit(f"Unsafe ZIP member path: {member.filename}")

        if (
            not force_extract
            and target.exists()
            and target.stat().st_size == member.file_size
        ):
            skipped += 1
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_name(target.name + ".tmp")
        with zf.open(member) as src, tmp.open("wb") as dst:
            shutil.copyfileobj(src, dst, length=1024 * 1024)
        tmp.replace(target)
        extracted += 1

fastas = sorted(extract_dir.rglob("*.fa"))
if len(fastas) != EXPECTED_FASTA_COUNT:
    raise SystemExit(
        f"Unexpected extracted FASTA count: {len(fastas)} != {EXPECTED_FASTA_COUNT}"
    )

with filelist.open("w", encoding="utf-8") as handle:
    for fasta in fastas:
        handle.write(str(fasta.resolve()) + "\n")

print(f"dataset: {SLUG}")
print(f"archive: {zip_path}")
print(f"archive_bytes: {archive_bytes}")
print(f"extract_dir: {extract_dir}")
print(f"extracted_files_this_run: {extracted}")
print(f"already_present_files: {skipped}")
print(f"filelist: {filelist}")
print(f"filelist_entries: {len(fastas)}")
print(f"first_entry: {fastas[0].resolve()}")
print(f"last_entry: {fastas[-1].resolve()}")
PY
