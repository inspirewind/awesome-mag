#!/usr/bin/env bash
set -euo pipefail

# dataset: Bin Chicken Rare Biosphere Genomes
# slug: bin-chicken-rbgs
# part: part4_hard_datasets
# size: 33.8 GB + 33.5 GB
# file: .download-complete
# note: Downloads the two MAG sequence archives; metadata archive is intentionally skipped.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

python3 "${ROOT_DIR}/scripts/bin-chicken-rbgs/download.py" \
  --root "${ROOT_DIR}" \
  "$@"
