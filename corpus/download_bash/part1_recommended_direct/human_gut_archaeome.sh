#!/usr/bin/env bash
set -euo pipefail

# dataset: Human Gut Archaeome
# slug: human-gut-archaeome
# part: part1_recommended_direct
# size: 657 MiB
# file: archaea_gut-genomes.tar.gz
# note: Nonredundant archaeal gut genome archive.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../_lib/download_one.sh"

download_one \
  "human-gut-archaeome" \
  "Human Gut Archaeome" \
  "part1_recommended_direct" \
  "https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/archaea_gut-genomes.tar.gz" \
  "archaea_gut-genomes.tar.gz" \
  "657 MiB"
