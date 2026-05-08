# Metagenomic Gut Virus Dataset Notes

- The Metagenomic Gut Virus Dataset (MGV) is the supporting dataset for the Nature Microbiology article "Metagenomic compendium of 189,680 DNA viruses from the human gut microbiome."
- The NERSC README describes MGV as 189,680 draft genomes of uncultivated viruses with greater than 50% estimated completeness assembled from 11,810 public human gut metagenomic samples.
- The dataset includes 54,118 candidate species/vOTUs, 11,837,198 predicted proteins, and 459,375 viral protein clusters.
- The main operational download entry point is the NERSC static index: `https://portal.nersc.gov/MGV/`.
- Users can download either the full `MGV_v1.0_2021_07_08.tar.gz` archive or selected files from the expanded `MGV_v1.0_2021_07_08/` directory.
- The official data usage policy says the data are freely available to use without restrictions; the MGV GitHub README asks users to cite the Nature Microbiology paper.
- The MGV GitHub README notes that UHGV is an updated version of the database: `https://github.com/snayfach/UHGV`.
- This is a human gut viral/phage genome catalogue rather than a prokaryotic MAG catalogue, so it should remain marked as a companion resource.

## Data Layout

| File | Contents |
| --- | --- |
| `mgv_contigs.fna` | FASTA of 189,680 non-identical viral genomes, all with greater than 50% estimated completeness. |
| `mgv_votu_representatives.fna` | Representative genomes for 54,118 viral operational taxonomic units. |
| `mgv_contig_info.tsv` | Genome metadata, CheckV quality/completeness, prophage flag, BACPHLIP lifestyle scores, GC, stop-codon readthrough, Baltimore class, and ICTV annotations. |
| `mgv_host_assignments.tsv` | Host assignments to UHGG genomes inferred from CRISPR spacer matches and near-identical 1 kb BLAST hits. |
| `mgv_proteins.faa` | FASTA of 11,837,198 predicted proteins. |
| `mgv_pc_info.tsv` | MMseqs2 protein cluster table for 459,375 clusters. |
| `mgv_pc_functions.tsv` | Consensus functional annotations for protein clusters. |
| `mgv_sample_info.tsv` | Metadata for the 11,810 public human gut metagenomic samples. |
| `mgv_dgrs.tsv` | Diversity-generating retroelement predictions. |
| `uhgg_spacers.fna` | FASTA of 1,846,441 CRISPR spacers identified from UHGG genomes. |
| `caudovirales_phylogeny.tree` | Caudovirales phylogeny tree file. |

## Checked Files

| File | Size | Last modified | Notes |
| --- | ---: | --- | --- |
| `MGV_v1.0_2021_07_08.tar.gz` | 5.2G | 2021-11-03 | Full MGV v1.0 archive. |
| `mgv_contigs.fna` | 8.8G | 2021-04-13 | Main viral genome FASTA. |
| `mgv_votu_representatives.fna` | 2.4G | 2021-10-18 | vOTU representative genome FASTA. |
| `mgv_proteins.faa` | 4.2G | 2021-04-14 | Predicted protein FASTA. |
| `mgv_contig_info.tsv` | 22M | 2021-11-02 | Main genome metadata table. |
| `mgv_host_assignments.tsv` | 17M | 2021-04-14 | Host assignment table. |
| `mgv_pc_info.tsv` | 281M | 2021-04-15 | Protein cluster membership table. |
| `mgv_pc_functions.tsv` | 6.2M | 2021-04-14 | Protein cluster function table. |
| `mgv_sample_info.tsv` | 24M | 2021-06-17 | Sample metadata table. |
| `mgv_dgrs.tsv` | 4.3M | 2021-04-14 | Diversity-generating retroelement table. |
| `uhgg_spacers.fna` | 165M | 2021-04-14 | UHGG CRISPR spacer FASTA. |
| `caudovirales_phylogeny.tree` | 1.0M | 2021-08-06 | Caudovirales phylogeny. |
| `README.txt` | 4.3K | 2021-10-18 | Dataset overview, data usage policy, and file descriptions. |

Checked on 2026-05-07.
