#!/usr/bin/env bash
set -euo pipefail

# dataset: TPMC
# slug: tpmc
# part: part1_recommended_direct
# size: 24.8 GB
# file: TPMC_MAG.tar.gz
# note: TPMC genome catalog MAG archive.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "tpmc" \
  "TPMC" \
  "part1_recommended_direct" \
  "https://download.cncb.ac.cn/bigd/TPMC/TPMC_genome_catalog/TPMC_MAG.tar.gz" \
  "TPMC_MAG.tar.gz" \
  "24.8 GB"
