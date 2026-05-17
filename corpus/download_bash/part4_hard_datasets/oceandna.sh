#!/usr/bin/env bash
set -euo pipefail

# dataset: OceanDNA MAG Catalog
# slug: oceandna
# part: part4_hard_datasets
# size: 43,859 non-representative MAGs plus 8,466 representative WGS FASTA files
# file: .download-complete
# note: Downloads Figshare article 15218454 and ENA PRJDB11811 WGS FASTA files.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

python3 "${ROOT_DIR}/scripts/oceandna/download.py" \
  --root "${ROOT_DIR}" \
  "$@"
