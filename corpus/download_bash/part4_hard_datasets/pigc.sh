#!/usr/bin/env bash
set -euo pipefail

# dataset: PIGC
# slug: pigc
# part: part4_hard_datasets
# size: 6,339 MAG bin FASTA files; total size not precomputed
# file: .download-complete
# note: Filters the CNSA manifest to MAG bin FASTA links only; raw FASTQ and gene/protein catalog records are skipped.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

python3 "${ROOT_DIR}/scripts/pigc/download.py" \
  --root "${ROOT_DIR}" \
  "$@"
