#!/usr/bin/env bash
set -euo pipefail

# dataset: Gut Phage Database (GPD)
# slug: gut-phage-database
# part: part3_viral_direct
# size: 1.4 GB
# file: GPD_sequences.fa.gz
# note: Viral genome nucleotide sequences.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "gut-phage-database" \
  "Gut Phage Database (GPD)" \
  "part3_viral_direct" \
  "https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/gut_phage_database/GPD_sequences.fa.gz" \
  "GPD_sequences.fa.gz" \
  "1.4 GB"
