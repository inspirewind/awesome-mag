#!/usr/bin/env bash
set -euo pipefail

# dataset: GEM
# slug: gem
# part: part1_recommended_direct
# size: 43.3 GB
# file: fna.tar
# note: OTU representative genome FASTA archive.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "gem" \
  "GEM" \
  "part1_recommended_direct" \
  "https://portal.nersc.gov/GEM/otus/fna.tar" \
  "fna.tar" \
  "43.3 GB"
