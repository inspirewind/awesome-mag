#!/usr/bin/env bash
set -euo pipefail

# dataset: Anammox Microbiota Catalog
# slug: anammox-microbiota
# part: part4_hard_datasets
# size: 8.12 GB Figshare dataset package
# file: .download-complete
# note: Uses the official Figshare public API when available; falls back to the official download-all URL for later MAG sequence inspection.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

python3 "${ROOT_DIR}/scripts/anammox-microbiota/download.py" \
  --root "${ROOT_DIR}" \
  "$@"
