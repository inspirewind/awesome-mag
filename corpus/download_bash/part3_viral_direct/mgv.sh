#!/usr/bin/env bash
set -euo pipefail

# dataset: Metagenomic Gut Virus Dataset (MGV)
# slug: mgv
# part: part3_viral_direct
# size: 2.4 GB
# file: mgv_votu_representatives.fna
# note: vOTU representative viral genomes.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "mgv" \
  "Metagenomic Gut Virus Dataset (MGV)" \
  "part3_viral_direct" \
  "https://portal.nersc.gov/MGV/MGV_v1.0_2021_07_08/mgv_votu_representatives.fna" \
  "mgv_votu_representatives.fna" \
  "2.4 GB"
