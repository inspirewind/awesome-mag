# Metagenomic Gut Virus Dataset Download Notes

The Metagenomic Gut Virus Dataset (MGV) is available from a public NERSC static file index linked by the Nature Microbiology paper's data availability statement and by the MGV code repository.

- NERSC landing page: `https://portal.nersc.gov/MGV/`
- Expanded file index: `https://portal.nersc.gov/MGV/MGV_v1.0_2021_07_08/`
- Dataset README: `https://portal.nersc.gov/MGV/MGV_v1.0_2021_07_08/README.txt`
- Code repository: `https://github.com/snayfach/MGV`

No source-specific helper script is needed. The files are direct HTTP(S) downloads and support range requests.

## Full Archive

| Asset | File | Size | Notes |
| --- | --- | ---: | --- |
| Full MGV v1.0 archive | `MGV_v1.0_2021_07_08.tar.gz` | 5.2G | Full archive corresponding to the expanded NERSC directory. |

## Core Files

Base path: `https://portal.nersc.gov/MGV/MGV_v1.0_2021_07_08/`

| Asset | File | Size | Notes |
| --- | --- | ---: | --- |
| Viral genomes | `mgv_contigs.fna` | 8.8G | FASTA of 189,680 non-identical viral genomes, all with greater than 50% estimated completeness. |
| vOTU representatives | `mgv_votu_representatives.fna` | 2.4G | Representative genomes for 54,118 viral operational taxonomic units; representatives were prioritized by circularity, lack of flanking host regions, and length. |
| Proteins | `mgv_proteins.faa` | 4.2G | FASTA of 11,837,198 proteins predicted with Prodigal `-p meta`. |
| Contig metadata | `mgv_contig_info.tsv` | 22M | Genome metadata including vOTU, CheckV quality/completeness, prophage flag, BACPHLIP lifestyle scores, GC, stop-codon readthrough, Baltimore class, and ICTV annotations. |
| Host assignments | `mgv_host_assignments.tsv` | 17M | Host links to UHGG genomes inferred from CRISPR spacer matches and near-identical 1 kb BLAST hits. |
| Protein cluster info | `mgv_pc_info.tsv` | 281M | MMseqs2 protein-clustering table for 11,837,198 proteins grouped into 459,375 clusters. |
| Protein cluster functions | `mgv_pc_functions.tsv` | 6.2M | Consensus protein-cluster functional annotations from Pfam, KEGG, TIGRFAM, and related databases. |
| Sample metadata | `mgv_sample_info.tsv` | 24M | Metadata for the 11,810 public human gut metagenomic samples used to build MGV. |
| DGR predictions | `mgv_dgrs.tsv` | 4.3M | Diversity-generating retroelements identified with DGRscan plus Pfam/HMMER reverse transcriptase detection. |
| UHGG CRISPR spacers | `uhgg_spacers.fna` | 165M | FASTA of 1,846,441 CRISPR spacers identified from UHGG genomes. |
| Caudovirales phylogeny | `caudovirales_phylogeny.tree` | 1.0M | Tree file for Caudovirales analyses in the study. |

## Example Commands

Download the README and metadata first:

```bash
curl -L -O https://portal.nersc.gov/MGV/MGV_v1.0_2021_07_08/README.txt
curl -L -C - -O https://portal.nersc.gov/MGV/MGV_v1.0_2021_07_08/mgv_contig_info.tsv
curl -L -C - -O https://portal.nersc.gov/MGV/MGV_v1.0_2021_07_08/mgv_sample_info.tsv
```

Download the main sequence files with resume support:

```bash
curl -L -C - -O https://portal.nersc.gov/MGV/MGV_v1.0_2021_07_08/mgv_contigs.fna
curl -L -C - -O https://portal.nersc.gov/MGV/MGV_v1.0_2021_07_08/mgv_votu_representatives.fna
curl -L -C - -O https://portal.nersc.gov/MGV/MGV_v1.0_2021_07_08/mgv_proteins.faa
```

Download the full archive instead of individual files:

```bash
curl -L -C - -O https://portal.nersc.gov/MGV/MGV_v1.0_2021_07_08.tar.gz
```

Inspect headers and table columns before downstream processing:

```bash
head -n 2 mgv_contig_info.tsv
head -n 2 mgv_host_assignments.tsv
head -n 2 mgv_pc_info.tsv
```

## Verification and Caveats

- The NERSC index did not show MD5 or SHA checksum files during curation.
- Files in the expanded directory are mostly uncompressed FASTA/TSV assets; plan storage and transfer accordingly.
- The NERSC README says all data are freely available to use without restrictions, but downstream users should cite the Nature Microbiology paper.
- The MGV GitHub README points to UHGV as an updated version of the database.
- This resource is a viral/phage genome catalogue, not a bacterial or archaeal MAG catalogue. It is included here as a human-gut metagenomic companion resource.

Checked on 2026-05-07.
