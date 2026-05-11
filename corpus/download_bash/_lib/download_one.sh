#!/usr/bin/env bash

local_file_size() {
  local path="$1"

  if stat -c '%s' "${path}" >/dev/null 2>&1; then
    stat -c '%s' "${path}"
  else
    stat -f '%z' "${path}"
  fi
}

remote_content_length() {
  local url="$1"

  if ! command -v curl >/dev/null 2>&1; then
    return 0
  fi

  curl -L -sS -I --fail "${url}" 2>/dev/null \
    | awk 'BEGIN { IGNORECASE = 1 } /^Content-Length:/ { value = $2 } END { gsub("\r", "", value); print value }' \
    || true
}

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
  local locks_dir="${root_dir}/corpus/.locks"
  local target="${download_dir}/${filename}"
  local target_rel="downloads/${slug}/${filename}"
  local flag="${completed_dir}/${slug}.flag"
  local lock_dir="${locks_dir}/${slug}.lock"

  mkdir -p "${download_dir}" "${completed_dir}" "${locks_dir}"

  while true; do
    if mkdir "${lock_dir}" 2>/dev/null; then
      printf '%s\n' "$$" > "${lock_dir}/pid"
      printf '%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" > "${lock_dir}/started_at"
      break
    fi

    local lock_pid
    lock_pid="$(cat "${lock_dir}/pid" 2>/dev/null || true)"
    if [[ -n "${lock_pid}" ]] && kill -0 "${lock_pid}" 2>/dev/null; then
      echo "Dataset is already downloading under pid ${lock_pid}; skipping duplicate run."
      return 0
    fi

    echo "Removing stale lock for ${slug}."
    rm -rf "${lock_dir}"
  done

  trap "rm -rf '${lock_dir}'" EXIT HUP INT TERM

  echo "Dataset: ${dataset}"
  echo "Part: ${part}"
  echo "URL: ${url}"
  echo "Output: ${target_rel}"
  echo "Expected size: ${size}"

  local remote_bytes
  remote_bytes="$(remote_content_length "${url}")"
  if [[ -n "${remote_bytes}" ]]; then
    echo "Remote bytes: ${remote_bytes}"
  else
    echo "Remote bytes: unavailable; downloader success will be used as the completion check."
  fi

  if [[ -f "${target}" && -n "${remote_bytes}" ]]; then
    local existing_bytes
    existing_bytes="$(local_file_size "${target}")"
    echo "Existing local bytes: ${existing_bytes}"

    if (( existing_bytes == remote_bytes )); then
      echo "Existing file size matches remote; skipping download."
    elif (( existing_bytes < remote_bytes )); then
      echo "Existing file is incomplete; resuming download."
      rm -f "${flag}"
      if command -v curl >/dev/null 2>&1; then
        curl -L -C - --fail --retry 3 --retry-delay 5 -o "${target}" "${url}"
      elif command -v aria2c >/dev/null 2>&1; then
        aria2c -c -x 4 -s 4 --allow-overwrite=true --auto-file-renaming=false \
          -d "${download_dir}" -o "${filename}" "${url}"
      elif command -v wget >/dev/null 2>&1; then
        wget -c --tries=3 -O "${target}" "${url}"
      else
        echo "No downloader found. Install aria2c, curl, or wget." >&2
        return 127
      fi
    else
      echo "Existing file is larger than remote; refusing to mark complete: ${target_rel}" >&2
      rm -f "${flag}"
      return 1
    fi
  elif [[ -f "${target}" ]]; then
    local existing_bytes
    existing_bytes="$(local_file_size "${target}")"
    echo "Existing local bytes: ${existing_bytes}"
    echo "Remote size is unavailable; attempting resume instead of trusting the existing file."
    rm -f "${flag}"
    if command -v curl >/dev/null 2>&1; then
      curl -L -C - --fail --retry 3 --retry-delay 5 -o "${target}" "${url}"
    elif command -v aria2c >/dev/null 2>&1; then
      aria2c -c -x 4 -s 4 --allow-overwrite=true --auto-file-renaming=false \
        -d "${download_dir}" -o "${filename}" "${url}"
    elif command -v wget >/dev/null 2>&1; then
      wget -c --tries=3 -O "${target}" "${url}"
    else
      echo "No downloader found. Install aria2c, curl, or wget." >&2
      return 127
    fi
  elif command -v aria2c >/dev/null 2>&1; then
    rm -f "${flag}"
    aria2c -c -x 4 -s 4 --allow-overwrite=true --auto-file-renaming=false \
      -d "${download_dir}" -o "${filename}" "${url}"
  elif command -v curl >/dev/null 2>&1; then
    rm -f "${flag}"
    curl -L -C - --fail --retry 3 --retry-delay 5 -o "${target}" "${url}"
  elif command -v wget >/dev/null 2>&1; then
    rm -f "${flag}"
    wget -c --tries=3 -O "${target}" "${url}"
  else
    echo "No downloader found. Install aria2c, curl, or wget." >&2
    return 127
  fi

  if [[ ! -s "${target}" ]]; then
    echo "Download target is missing or empty: ${target_rel}" >&2
    return 1
  fi

  local final_bytes
  final_bytes="$(local_file_size "${target}")"
  if [[ -n "${remote_bytes}" && "${final_bytes}" != "${remote_bytes}" ]]; then
    echo "Downloaded file size mismatch: local=${final_bytes}, remote=${remote_bytes}" >&2
    rm -f "${flag}"
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
    printf 'local_bytes=%s\n' "${final_bytes}"
    printf 'remote_bytes=%s\n' "${remote_bytes}"
    printf 'completed_at=%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  } > "${flag}"

  echo "Completed flag: corpus/completed/${slug}.flag"
}
