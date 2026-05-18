#!/usr/bin/env bash
set -euo pipefail

# dataset: RGMGC
# slug: rgmgc
# part: part4_hard_datasets
# size: 10,373 per-MAG NCBI Assembly genome FASTA files; total size not precomputed
# file: .download-complete
# note: Enumerates NCBI BioProject PRJNA657473 assembly records and downloads genome FASTA files only.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

python3 "${ROOT_DIR}/scripts/rgmgc/download.py" \
  --root "${ROOT_DIR}" \
  "$@"
