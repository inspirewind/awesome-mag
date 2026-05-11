#!/usr/bin/env bash
set -euo pipefail

# dataset: mOTUs DB
# slug: motus-db
# part: part2_large_or_caveated_direct
# size: 2.7 TB
# file: mOTUs4.genomes.tar
# note: Extremely large full genome archive.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "motus-db" \
  "mOTUs DB" \
  "part2_large_or_caveated_direct" \
  "https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/mOTUs4.genomes.tar" \
  "mOTUs4.genomes.tar" \
  "2.7 TB"
