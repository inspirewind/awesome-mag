#!/usr/bin/env bash
set -euo pipefail

# dataset: OMDB
# slug: omdb
# part: part2_large_or_caveated_direct
# size: 1.5 TB
# file: OMDv2.genomes.db.tar.gz
# note: Very large whole genome database archive.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "omdb" \
  "OMDB" \
  "part2_large_or_caveated_direct" \
  "https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/genomes/OMDv2.genomes.db.tar.gz" \
  "OMDv2.genomes.db.tar.gz" \
  "1.5 TB"
