#!/usr/bin/env bash
set -euo pipefail

# dataset: HRGM
# slug: hrgm
# part: part1_recommended_direct
# size: 3.5 GB
# file: HRGMv2_Rep_Genome.tar.gz
# note: Representative genome archive.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "hrgm" \
  "HRGM" \
  "part1_recommended_direct" \
  "https://www.decodebiome.org/HRGM/data/genome_catalog/HRGMv2_Genomes/HRGMv2_Rep_Genome.tar.gz" \
  "HRGMv2_Rep_Genome.tar.gz" \
  "3.5 GB"
