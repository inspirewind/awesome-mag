#!/usr/bin/env bash
set -euo pipefail

# dataset: SPIRE
# slug: spire
# part: part4_hard_datasets
# size: 714 per-study MAG tar archives; total size not precomputed
# file: .download-complete
# note: Downloads per-study *_MAGs.tar archives only.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

python3 "${ROOT_DIR}/scripts/spire/download.py" download \
  --root "${ROOT_DIR}" \
  --all-studies \
  "$@"
