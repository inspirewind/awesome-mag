#!/usr/bin/env bash
set -euo pipefail

# dataset: HROM
# slug: hrom
# part: part2_large_or_caveated_direct
# size: 76.1 GB
# file: HROM_nonredundant_genomes.tar.gz
# note: Nonredundant genome archive; representative genomes are many individual files.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "hrom" \
  "HROM" \
  "part2_large_or_caveated_direct" \
  "https://www.decodebiome.org/HROM/data/genome_catalog/HROM_nonredundant_genomes.tar.gz" \
  "HROM_nonredundant_genomes.tar.gz" \
  "76.1 GB"
