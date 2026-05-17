#!/usr/bin/env bash
set -euo pipefail

# dataset: Anammox Microbiota Catalog
# slug: anammox-microbiota
# part: part4_hard_datasets
# size: 1.87 GB Figshare Strain_level_MAGs.zip
# file: .download-complete
# note: Direct Figshare file download for the strain-level MAG archive.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

SLUG="anammox-microbiota"
DATASET="Anammox Microbiota Catalog"
PART="part4_hard_datasets"
URL="https://ndownloader.figshare.com/files/45271516"
EXPECTED_BYTES="1865155640"
OUT_DIR="${ROOT_DIR}/downloads/${SLUG}"
OUT_FILE="${OUT_DIR}/anammox_microbiota_figshare_45271516.zip"
MANIFEST="${OUT_DIR}/manifest.tsv"
MARKER="${OUT_DIR}/.download-complete"
COMPLETED_DIR="${ROOT_DIR}/corpus/completed"
LOCK_DIR="${ROOT_DIR}/corpus/.locks/${SLUG}.lock"
MANIFEST_ONLY=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --root)
      ROOT_DIR="$(cd "$2" && pwd)"
      OUT_DIR="${ROOT_DIR}/downloads/${SLUG}"
      OUT_FILE="${OUT_DIR}/anammox_microbiota_figshare_45271516.zip"
      MANIFEST="${OUT_DIR}/manifest.tsv"
      MARKER="${OUT_DIR}/.download-complete"
      COMPLETED_DIR="${ROOT_DIR}/corpus/completed"
      LOCK_DIR="${ROOT_DIR}/corpus/.locks/${SLUG}.lock"
      shift 2
      ;;
    --manifest-only)
      MANIFEST_ONLY=1
      shift
      ;;
    --downloader|--jobs|--connections|--retries)
      echo "Ignoring $1 for ${SLUG}; this script always uses wget."
      shift 2
      ;;
    --verify-md5)
      echo "Ignoring --verify-md5 for ${SLUG}; no upstream MD5 is available."
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

file_size_bytes() {
  if stat -c%s "$1" >/dev/null 2>&1; then
    stat -c%s "$1"
  else
    stat -f%z "$1"
  fi
}

relpath() {
  case "$1" in
    "${ROOT_DIR}"/*) printf '%s\n' "${1#"${ROOT_DIR}/"}" ;;
    *) printf '%s\n' "$1" ;;
  esac
}

write_manifest() {
  mkdir -p "${OUT_DIR}"
  {
    printf "url\tpath\tmd5\tbytes\n"
    printf "%s\t%s\t\t%s\n" "${URL}" "$(relpath "${OUT_FILE}")" "${EXPECTED_BYTES}"
  } > "${MANIFEST}"
}

acquire_lock() {
  mkdir -p "$(dirname "${LOCK_DIR}")"
  if mkdir "${LOCK_DIR}" 2>/dev/null; then
    printf '%s\n' "$$" > "${LOCK_DIR}/pid"
    return
  fi

  if [ -f "${LOCK_DIR}/pid" ]; then
    lock_pid="$(tr -d '[:space:]' < "${LOCK_DIR}/pid")"
    if [ -n "${lock_pid}" ] && kill -0 "${lock_pid}" 2>/dev/null; then
      echo "Dataset ${SLUG} is already downloading under pid ${lock_pid}; skipping duplicate run." >&2
      exit 1
    fi
  fi

  echo "Removing stale lock for ${SLUG}."
  rm -rf "${LOCK_DIR}"
  mkdir "${LOCK_DIR}"
  printf '%s\n' "$$" > "${LOCK_DIR}/pid"
}

write_completed_flag() {
  local now
  local actual_bytes
  now="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  actual_bytes="$(file_size_bytes "${OUT_FILE}")"
  mkdir -p "${COMPLETED_DIR}"

  {
    printf "slug=%s\n" "${SLUG}"
    printf "dataset=%s\n" "${DATASET}"
    printf "part=%s\n" "${PART}"
    printf "manifest=%s\n" "$(relpath "${MANIFEST}")"
    printf "archive=%s\n" "$(relpath "${OUT_FILE}")"
    printf "file_count=1\n"
    printf "present_count=1\n"
    printf "local_bytes=%s\n" "${actual_bytes}"
    printf "remote_bytes=%s\n" "${EXPECTED_BYTES}"
    printf "completed_at=%s\n" "${now}"
  } > "${MARKER}"

  {
    printf "slug=%s\n" "${SLUG}"
    printf "dataset=%s\n" "${DATASET}"
    printf "part=%s\n" "${PART}"
    printf "file=.download-complete\n"
    printf "path=%s\n" "$(relpath "${MARKER}")"
    printf "manifest=%s\n" "$(relpath "${MANIFEST}")"
    printf "archive=%s\n" "$(relpath "${OUT_FILE}")"
    printf "size=1.87 GB Figshare Strain_level_MAGs.zip\n"
    printf "file_count=1\n"
    printf "present_count=1\n"
    printf "local_bytes=%s\n" "${actual_bytes}"
    printf "remote_bytes=%s\n" "${EXPECTED_BYTES}"
    printf "note=Direct Figshare file download for the strain-level MAG archive.\n"
    printf "completed_at=%s\n" "${now}"
  } > "${COMPLETED_DIR}/${SLUG}.flag"
}

if ! command -v wget >/dev/null 2>&1; then
  echo "wget was not found on PATH." >&2
  exit 1
fi

acquire_lock
trap 'rm -rf "${LOCK_DIR}"' EXIT

write_manifest

echo "Dataset: ${DATASET}"
echo "Part: ${PART}"
echo "Files: 1"
echo "Manifest: $(relpath "${MANIFEST}")"
echo "Output: $(relpath "${OUT_DIR}")"
echo "Expected size: 1.87 GB Figshare Strain_level_MAGs.zip"
echo "URL: ${URL}"

if [ "${MANIFEST_ONLY}" -eq 1 ]; then
  echo "Manifest-only mode; no data file downloaded."
  exit 0
fi

mkdir -p "${OUT_DIR}"

if [ -f "${OUT_FILE}" ]; then
  current_bytes="$(file_size_bytes "${OUT_FILE}")"
  if [ "${current_bytes}" = "${EXPECTED_BYTES}" ]; then
    echo "Already complete: $(relpath "${OUT_FILE}") (${current_bytes} bytes)"
    write_completed_flag
    echo "Completed flag: corpus/completed/${SLUG}.flag"
    exit 0
  fi
  echo "Existing file size is ${current_bytes} bytes; expected ${EXPECTED_BYTES}. Resuming with wget -c."
fi

wget -c \
  --tries=5 \
  --waitretry=10 \
  --timeout=60 \
  --read-timeout=60 \
  -O "${OUT_FILE}" \
  "${URL}"

actual_bytes="$(file_size_bytes "${OUT_FILE}")"
if [ "${actual_bytes}" != "${EXPECTED_BYTES}" ]; then
  echo "Downloaded size mismatch for $(relpath "${OUT_FILE}"): ${actual_bytes} != ${EXPECTED_BYTES}" >&2
  echo "Keep the partial file in place and rerun this script to resume." >&2
  exit 1
fi

write_completed_flag
echo "Completed flag: corpus/completed/${SLUG}.flag"
