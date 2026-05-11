#!/usr/bin/env bash
set -euo pipefail

# dataset: GROWdb
# slug: growdb
# part: part2_large_or_caveated_direct
# size: 3.9 GB
# file: 5986_99ID_drep_global.tar.gz
# note: Global freshwater dereplicated MAG comparison set, not the core GROWdb-only MAG set.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "growdb" \
  "GROWdb" \
  "part2_large_or_caveated_direct" \
  "https://zenodo.org/records/11193259/files/5986_99ID_drep_global.tar.gz?download=1" \
  "5986_99ID_drep_global.tar.gz" \
  "3.9 GB"
