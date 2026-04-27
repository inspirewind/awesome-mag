# GEM Download Notes

GEM data are available from the public NERSC static file host:

```text
https://portal.nersc.gov/GEM/
```

The JGI Genome Portal page is useful for project context and release metadata, but the NERSC root is the reproducible download entry point.

## Core Genome Files

| Asset | URL | Notes |
| --- | --- | --- |
| Dataset README | `https://portal.nersc.gov/GEM/README.md` | Upstream layout and data usage summary. |
| Genome metadata | `https://portal.nersc.gov/GEM/genomes/genome_metadata.tsv` | 12.4 MB TSV; best starting point for filtering by quality, OTU, ecosystem, habitat, and coordinates. |
| Genome nucleotide FASTA archive | `https://portal.nersc.gov/GEM/genomes/fna.tar` | 39.5 GB tar archive. |
| Predicted protein FASTA archive | `https://portal.nersc.gov/GEM/genomes/faa.tar` | 26.7 GB tar archive. |
| Predicted CDS nucleotide FASTA archive | `https://portal.nersc.gov/GEM/genomes/ffn.tar` | 39.3 GB tar archive. |
| Individual genome FASTA files | `https://portal.nersc.gov/GEM/genomes/fna/` | Apache-style directory with one `.fna.gz` file per MAG. |

## Companion Data

| Asset | URL | Notes |
| --- | --- | --- |
| OTU data | `https://portal.nersc.gov/GEM/otus/` | OTU mappings, taxonomy, representatives, CheckM metrics, and representative genome FASTA files. |
| BGC data | `https://portal.nersc.gov/GEM/bgcs/` | antiSMASH v5.1 GenBank files. |
| Prophage data | `https://portal.nersc.gov/GEM/prophages/` | VirSorter FASTA and TSV files for putative prophages. |
| Protein clusters | `https://portal.nersc.gov/GEM/protclusts/` | MMseqs2 cluster tables and representative protein sequences. |
| Marker-gene trees | `https://portal.nersc.gov/GEM/tree/` | Marker alignment plus rooted, unrooted, and midpoint trees. |

## Example Commands

Download the metadata first:

```bash
curl -L -O https://portal.nersc.gov/GEM/genomes/genome_metadata.tsv
```

Download the full genome archive with resume support:

```bash
curl -L -C - -O https://portal.nersc.gov/GEM/genomes/fna.tar
```

Download one individual MAG FASTA when the genome ID is known:

```bash
curl -L -O https://portal.nersc.gov/GEM/genomes/fna/3300025516_6.fna.gz
```

## Curation Caveats

- Use resumable download tooling for the tar archives; the largest checked files are roughly 26-43 GB each.
- The NERSC indexes are public and stable enough for direct URL construction, so no source-specific helper script is currently needed.
- The JGI Genome Portal displayed a migration/end-of-life banner on 2026-04-27. If the JGI landing page moves, keep the NERSC root and README as the operational download references.
- The MAG bundle is free to use, but the underlying metagenomes remain subject to JGI data release and utilization policies.
