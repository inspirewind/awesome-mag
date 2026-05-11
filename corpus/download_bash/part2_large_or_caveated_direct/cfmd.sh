#!/usr/bin/env bash
set -euo pipefail

# dataset: cFMD
# slug: cfmd
# part: part2_large_or_caveated_direct
# size: 9.8 GB
# file: cFMD_mags.tar.gz
# note: Initial Cell paper MAG archive; current cFMD release also has additional MAG archives.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "cfmd" \
  "cFMD" \
  "part2_large_or_caveated_direct" \
  "https://zenodo.org/records/13285428/files/cFMD_mags.tar.gz?download=1" \
  "cFMD_mags.tar.gz" \
  "9.8 GB"
