#!/usr/bin/env bash

download_one() {
  local slug="$1"
  local dataset="$2"
  local part="$3"
  local url="$4"
  local filename="$5"
  local size="$6"

  if [[ -z "${SCRIPT_DIR:-}" ]]; then
    echo "SCRIPT_DIR is not set by the caller" >&2
    return 2
  fi

  local root_dir
  root_dir="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

  local download_dir="${root_dir}/downloads/${slug}"
  local completed_dir="${root_dir}/corpus/completed"
  local target="${download_dir}/${filename}"
  local target_rel="downloads/${slug}/${filename}"
  local flag="${completed_dir}/${slug}.flag"

  mkdir -p "${download_dir}" "${completed_dir}"

  echo "Dataset: ${dataset}"
  echo "Part: ${part}"
  echo "URL: ${url}"
  echo "Output: ${target_rel}"
  echo "Expected size: ${size}"

  if [[ -s "${target}" ]]; then
    echo "Existing non-empty file found; skipping download."
  elif command -v aria2c >/dev/null 2>&1; then
    aria2c -c -x 4 -s 4 --allow-overwrite=true --auto-file-renaming=false \
      -d "${download_dir}" -o "${filename}" "${url}"
  elif command -v curl >/dev/null 2>&1; then
    curl -L -C - --fail --retry 3 --retry-delay 5 -o "${target}" "${url}"
  elif command -v wget >/dev/null 2>&1; then
    wget -c --tries=3 -O "${target}" "${url}"
  else
    echo "No downloader found. Install aria2c, curl, or wget." >&2
    return 127
  fi

  if [[ ! -s "${target}" ]]; then
    echo "Download target is missing or empty: ${target_rel}" >&2
    return 1
  fi

  {
    printf 'slug=%s\n' "${slug}"
    printf 'dataset=%s\n' "${dataset}"
    printf 'part=%s\n' "${part}"
    printf 'file=%s\n' "${filename}"
    printf 'path=%s\n' "${target_rel}"
    printf 'url=%s\n' "${url}"
    printf 'size=%s\n' "${size}"
    printf 'completed_at=%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  } > "${flag}"

  echo "Completed flag: corpus/completed/${slug}.flag"
}
