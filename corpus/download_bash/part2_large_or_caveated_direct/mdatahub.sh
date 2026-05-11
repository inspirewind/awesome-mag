#!/usr/bin/env bash
set -euo pipefail

# dataset: Microbiome Datahub
# slug: mdatahub
# part: part2_large_or_caveated_direct
# size: 146 GB
# file: 20250810AllMAG.fasta.gz
# note: All MAG contig DNA sequences; verify NIG host reachability from the target server.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "mdatahub" \
  "Microbiome Datahub" \
  "part2_large_or_caveated_direct" \
  "http://palaeo.nig.ac.jp/Resources/MDatahub/2025/20250810AllMAG.fasta.gz" \
  "20250810AllMAG.fasta.gz" \
  "146 GB"
