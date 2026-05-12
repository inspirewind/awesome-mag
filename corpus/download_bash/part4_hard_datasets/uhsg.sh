#!/usr/bin/env bash
set -euo pipefail

# dataset: UHSG
# slug: uhsg
# part: part4_hard_datasets
# size: 5,779 per-assembly FASTA files; total size not precomputed
# file: .download-complete
# note: Filters the CNSA manifest to assembly FASTA links only.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

python3 "${ROOT_DIR}/scripts/uhsg/download.py" \
  --root "${ROOT_DIR}" \
  "$@"
