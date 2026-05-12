#!/usr/bin/env bash
set -euo pipefail

# dataset: SMAG
# slug: smag
# part: part4_hard_datasets
# size: 36.3 GiB split MAG archive
# file: .download-complete
# note: Downloads Zenodo mag.tar.gz.* parts and reassembles mag.tar.gz; companion files are skipped.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

python3 "${ROOT_DIR}/scripts/smag/download.py" \
  --root "${ROOT_DIR}" \
  "$@"
