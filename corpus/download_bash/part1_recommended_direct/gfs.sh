#!/usr/bin/env bash
set -euo pipefail

# dataset: Glacier-fed Streams (GFS) MAGs
# slug: gfs
# part: part1_recommended_direct
# size: 3.2 GB
# file: ProkaryoticMAGsContig.tar
# note: Prokaryotic MAG contig archive.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "gfs" \
  "Glacier-fed Streams (GFS) MAGs" \
  "part1_recommended_direct" \
  "https://zenodo.org/records/13890040/files/ProkaryoticMAGsContig.tar?download=1" \
  "ProkaryoticMAGsContig.tar" \
  "3.2 GB"
