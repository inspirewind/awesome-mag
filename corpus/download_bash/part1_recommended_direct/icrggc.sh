#!/usr/bin/env bash
set -euo pipefail

# dataset: ICRGGC
# slug: icrggc
# part: part1_recommended_direct
# size: 8.5 GB
# file: MAGs.tar.gz
# note: Single all-MAG archive; representative MAGs are split across multiple tar files.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "icrggc" \
  "ICRGGC" \
  "part1_recommended_direct" \
  "ftp://download.nmdc.cn/icrggc/MAGs.tar.gz" \
  "MAGs.tar.gz" \
  "8.5 GB"
