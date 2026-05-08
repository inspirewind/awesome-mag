# Unified Human Gut Virome Notes

- The Unified Human Gut Virome (UHGV) is a JGI/NERSC human gut viral genome resource built by integrating 12 independent gut virome datasets and processing them with a uniform pipeline.
- The current GitHub README and Zenodo v1.0 record describe 873,995 UHGV genomes and 168,536 species-level viral operational taxonomic units (vOTUs).
- UHGV provides three quality tiers: full genomes above 50% completeness or above 10 kb, medium-quality genomes above 50% completeness with confident viral prediction, and high-quality genomes above 90% completeness with confident viral prediction.
- The main operational download point is the NERSC static index at `https://portal.nersc.gov/UHGV/`. The official website points users to `https://uhgv.jgi.doe.gov/downloads`.
- Zenodo record `10.5281/zenodo.17402089` is the citable v1.0 data resource and provides a compact zstd subset with MD5 checksums.
- The NERSC top-level `README.md` appears older than the GitHub README: it lists 884,377 genomes and 171,338 vOTUs, while the current GitHub README and Zenodo record use 873,995 genomes and 168,536 vOTUs. Use the GitHub README/Zenodo counts for curation.
- This is a viral/phage genome catalogue, not a prokaryotic MAG catalogue. It belongs in this repository as a human-gut metagenomic companion resource, like GPD and MGV.

## Data Layout

| Area | Contents |
| --- | --- |
| `genome_catalogs/` | Full, medium-quality-plus, and high-quality-plus UHGV genome FASTA/protein FASTA files, vOTU representative FASTA/protein FASTA files, host genomes, and prokaryote representatives. |
| `metadata/` | Genome-level metadata, vOTU metadata, extended vOTU metadata, host metadata, and source biosample metadata. |
| `annotations/` | Protein annotations, predicted tRNAs, and diversity-generating retroelements for vOTU representatives. |
| `host_predictions/` | CRISPR spacers, CRISPR-based host assignments, PHIST k-mer host assignments, host genome taxonomy, and host-range breadth tables. |
| `protein_clusters/` | Protein cluster summaries, cluster membership, cluster taxonomy, multiple sequence alignments, and MSA effective sequence counts. |
| `structures/` | Predicted protein structures, reference structures, domain segmentation, structure annotations, and Foldseek-compatible structure database files. |
| `phylogeny/` | Caudoviricetes phylogenetic tree. |
| `read_mapping/` | CoverM read-mapping outputs, relative abundance table, sample metadata, study metadata, and Bowtie2 index directory. |
| `microdiversity/` | SNV and codon pN/pS tables derived from read mapping. |
| `votu_reps/` | Per-vOTU representative folders sharded from `UHGV-000/` through `UHGV-224/`; each representative can include `.fna`, `.faa`, `.gff`, eggNOG, and annotation tables. |

## Checked Files

| File | Size | Last modified | Notes |
| --- | ---: | --- | --- |
| `genome_catalogs/votus_hq_plus.fna.gz` | 701M | 2023-04-01 | GitHub README recommended high-quality representative genome FASTA. |
| `metadata/votus_metadata.tsv` | 52M | 2026-04-08 | GitHub README recommended vOTU metadata table. |
| `genome_catalogs/uhgv_full.fna.gz` | 6.5G | 2025-10-21 | DNA FASTA for all full-tier UHGV genomes. |
| `genome_catalogs/uhgv_full.faa.gz` | 5.6G | 2023-04-02 | Protein FASTA for all UHGV genomes. |
| `genome_catalogs/votus_full.fna.gz` | 1.3G | 2025-10-21 | DNA FASTA for all vOTU representatives. |
| `genome_catalogs/votus_full.faa.gz` | 1.0G | 2023-04-01 | Protein FASTA for all vOTU representatives. |
| `metadata/uhgv_metadata.tsv` | 207M | 2026-04-08 | Genome-level metadata for 873,995 UHGV genomes. |
| `metadata/votus_metadata_extended.tsv` | 129M | 2026-04-08 | Extended vOTU metadata. |
| `annotations/protein_annotations.tsv.gz` | 329M | 2025-11-02 | Protein annotations for vOTU representatives. |
| `host_predictions/crispr_spacers.fna` | 428M | 2022-12-10 | 5,318,089 CRISPR spacers. |
| `host_predictions/host_assignment_crispr.tsv` | 311M | 2023-04-01 | CRISPR-based host assignments. |
| `host_predictions/host_assignment_kmers.tsv` | 372M | 2023-04-01 | PHIST k-mer host assignments. |
| `protein_clusters/protein_clusters.tsv` | 232M | 2023-12-13 | Protein cluster summary table. |
| `protein_clusters/MSAs.tar.gz` | 1.3G | 2024-02-28 | Multiple sequence alignments for clusters with at least 15 members. |
| `structures/PDB.tar.gz` | 1.5G | 2024-02-28 | UHGV predicted protein structures. |
| `structures/JSON.tar.gz` | 9.1G | 2024-03-27 | JSON-format predicted structure output. |
| `phylogeny/caudoviricetes_tree.nwk.gz` | 3.4M | 2025-11-02 | Caudoviricetes tree. |
| `read_mapping/metagenomes_coverm.tsv.gz` | 2.7G | 2024-04-18 | CoverM statistics for bulk metagenomes. |
| `microdiversity/SNVs.tsv.zst` | 118M | 2025-11-02 | SNV table. |
| Zenodo `uhgv_full.fna.zst` | 1.5G | 2025-10-22 record update | Compact zstd DNA FASTA with MD5 checksum. |
| Zenodo `votus_full.fna.zst` | 920M | 2025-10-22 record update | Compact zstd vOTU representative DNA FASTA with MD5 checksum. |

Checked on 2026-05-08.
