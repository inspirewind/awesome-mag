#!/usr/bin/env bash
set -euo pipefail

# dataset: RUG2 Rumen MAGs
# slug: rug2
# part: part4_hard_datasets
# size: 20,567 ENA binned metagenome FASTA files; superset of the 4,941 final RUGs
# file: .download-complete
# note: Filters ENA analysis records to binned metagenome assemblies; raw reads and DataShare companion archive are skipped.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

python3 "${ROOT_DIR}/scripts/rug2/download.py" \
  --root "${ROOT_DIR}" \
  "$@"
