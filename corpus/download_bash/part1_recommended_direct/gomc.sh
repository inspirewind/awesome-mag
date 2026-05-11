#!/usr/bin/env bash
set -euo pipefail

# dataset: GOMC
# slug: gomc
# part: part1_recommended_direct
# size: 17.91 GB
# file: 24195.GOMC_genomes.tar.gz
# note: Species-level GOMC genome catalogue.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "gomc" \
  "GOMC" \
  "part1_recommended_direct" \
  "https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/24195.GOMC_genomes.tar.gz" \
  "24195.GOMC_genomes.tar.gz" \
  "17.91 GB"
