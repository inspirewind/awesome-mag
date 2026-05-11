#!/usr/bin/env bash
set -euo pipefail

# dataset: MRGM
# slug: mrgm
# part: part2_large_or_caveated_direct
# size: 43 GB
# file: MRGM_All_55893_genomes.tar.gz
# note: All near-complete genome archive; representative genomes are many individual files.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "mrgm" \
  "MRGM" \
  "part2_large_or_caveated_direct" \
  "https://www.decodebiome.org/MRGM/data/genome_catalog/All_55893_genomes/genome.tar.gz" \
  "MRGM_All_55893_genomes.tar.gz" \
  "43 GB"
