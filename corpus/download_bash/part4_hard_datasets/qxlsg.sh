#!/usr/bin/env bash
set -euo pipefail

# dataset: QXLSG
# slug: qxlsg
# part: part4_hard_datasets
# size: 5,866 per-MAG GWH genome FASTA files; total size not precomputed
# file: .download-complete
# note: Enumerates GWH PRJCA037687 assembly records and downloads DNA genome FASTA files only.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

python3 "${ROOT_DIR}/scripts/qxlsg/download.py" \
  --root "${ROOT_DIR}" \
  "$@"
