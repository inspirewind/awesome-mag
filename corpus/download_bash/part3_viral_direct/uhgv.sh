#!/usr/bin/env bash
set -euo pipefail

# dataset: Unified Human Gut Virome (UHGV)
# slug: uhgv
# part: part3_viral_direct
# size: 701 MB
# file: votus_hq_plus.fna.gz
# note: High-quality vOTU representative viral genomes.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "uhgv" \
  "Unified Human Gut Virome (UHGV)" \
  "part3_viral_direct" \
  "https://portal.nersc.gov/UHGV/genome_catalogs/votus_hq_plus.fna.gz" \
  "votus_hq_plus.fna.gz" \
  "701 MB"
