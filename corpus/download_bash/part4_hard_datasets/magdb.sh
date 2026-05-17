#!/usr/bin/env bash
set -euo pipefail

# dataset: MAGdb
# slug: magdb
# part: part4_hard_datasets
# size: per-study data.tar.gz archives; total size depends on matched studies
# file: downloads/magdb/<category>/<study-title>.tar.gz
# note: Downloads MAGdb per-study archives through an authenticated EGG_SESS cookie.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

if [ "$#" -gt 0 ]; then
  case "$1" in
    list|url|download)
      exec python3 "${ROOT_DIR}/scripts/magdb/download.py" "$@"
      ;;
  esac
fi

python3 "${ROOT_DIR}/scripts/magdb/download.py" download \
  --category all \
  --all-matches \
  --output-dir "${ROOT_DIR}/downloads/magdb" \
  --skip-existing \
  --resume \
  --retries 3 \
  --continue-on-error \
  "$@"
