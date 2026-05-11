#!/usr/bin/env bash
set -euo pipefail

# dataset: LakePulse MAG Catalogue
# slug: lakepulse
# part: part1_recommended_direct
# size: 643.1 MB
# file: LakePulse_MAGs-contigs.zip
# note: MAG contig archive.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "lakepulse" \
  "LakePulse MAG Catalogue" \
  "part1_recommended_direct" \
  "https://datadryad.org/api/v2/files/2471867/download" \
  "LakePulse_MAGs-contigs.zip" \
  "643.1 MB"
