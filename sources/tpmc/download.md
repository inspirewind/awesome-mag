# TPMC Download Notes

TPMC is hosted by CNCB-NGDC as a public project page plus static download indexes. Core catalog assets are reachable with plain HTTPS URLs and support resumable downloads.

Primary links:

- Project page: `https://ngdc.cncb.ac.cn/tpmc`
- GSA project: `https://ngdc.cncb.ac.cn/gsa/browse/CRA011511`
- CNCB BioProject: `https://ngdc.cncb.ac.cn/bioproject/browse/PRJCA017393`
- Publication: `https://www.nature.com/articles/s41467-024-45895-8`

## Project and Raw Metagenomes

| Asset | URL | Notes |
| --- | --- | --- |
| TPMC project page | `https://ngdc.cncb.ac.cn/tpmc` | Descriptive landing page, data usage policy, and links to all catalog directories. |
| Sample metadata | `https://download.cncb.ac.cn/bigd/TPMC/meta_table.xlsx` | 172.5 KB; metadata for the 498 TPMC samples. |
| GSA accession `CRA011511` | `https://ngdc.cncb.ac.cn/gsa/browse/CRA011511` | Raw metagenomes; GSA reports 607 items, 1,214 files, and 19,459.39 GB. |
| GSA HTTPS files | `https://download.cncb.ac.cn/gsa2/CRA011511` | Raw sequence file index linked from the GSA page. |
| GSA FTP files | `ftp://download.big.ac.cn/gsa2/CRA011511` | FTP alternative for raw sequence files. |
| GSA Qtrans | `https://qtp.cncb.ac.cn/qtrans/v2/file?path=/gsa2/CRA011511` | GSA recommended transfer route. |

## TPMC Genome Catalog

Index: `https://download.cncb.ac.cn/bigd/TPMC/TPMC_genome_catalog/`

| File | Size | URL | Notes |
| --- | ---: | --- | --- |
| `TPMC_MAG.tar.gz` | 24.8 GB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_genome_catalog/TPMC_MAG.tar.gz` | Archive containing 32,355 MAGs. |
| `MAG_summary.xlsx` | 4.6 MB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_genome_catalog/MAG_summary.xlsx` | MAG quality, taxonomy, and OTU clustering metadata. |
| `readme` | 831 B | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_genome_catalog/readme` | Catalog description from CNCB-NGDC. |

Example:

```bash
curl -L -C - -O https://download.cncb.ac.cn/bigd/TPMC/TPMC_genome_catalog/TPMC_MAG.tar.gz
curl -L -C - -O https://download.cncb.ac.cn/bigd/TPMC/TPMC_genome_catalog/MAG_summary.xlsx
```

## TPMC Gene Catalog

Index: `https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/`

The TPMC gene catalog contains 296,289,678 non-redundant genes. The download directory exposes representative sequences, clustering outputs, and functional annotation tables.

| File | Size | URL |
| --- | ---: | --- |
| `non_redundant_gene_rep_seq_nucl.fa` | 236.5 GB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/non_redundant_gene_rep_seq_nucl.fa` |
| `non_redundant_gene_rep_seq_proteins.fa` | 105.3 GB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/non_redundant_gene_rep_seq_proteins.fa` |
| `non_redundant_gene_clusters.tsv` | 30.2 GB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/non_redundant_gene_clusters.tsv` |
| `non_redundant_gene_clusters_in_mag.tsv` | 7.5 GB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/non_redundant_gene_clusters_in_mag.tsv` |
| `non_redundant_gene_ann_nr.tsv` | 20.4 GB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/non_redundant_gene_ann_nr.tsv` |
| `non_redundant_gene_ann_uniref50.tsv` | 21.3 GB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/non_redundant_gene_ann_uniref50.tsv` |
| `non_redundant_gene_ann_swissprot.tsv` | 8.1 GB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/non_redundant_gene_ann_swissprot.tsv` |
| `non_redundant_gene_ann_eggnog.tsv` | 92.1 GB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/non_redundant_gene_ann_eggnog.tsv` |
| `non_redundant_gene_ann_rgi.tsv` | 47.8 MB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/non_redundant_gene_ann_rgi.tsv` |
| `non_redundant_gene_ann_vfdb.tsv` | 4.9 GB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/non_redundant_gene_ann_vfdb.tsv` |
| `readme` | 1.0 KB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/readme` |

Download selected files with resume support:

```bash
curl -L -C - -O https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/non_redundant_gene_rep_seq_nucl.fa
curl -L -C - -O https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/non_redundant_gene_rep_seq_proteins.fa
curl -L -C - -O https://download.cncb.ac.cn/bigd/TPMC/TPMC_gene_catalog/non_redundant_gene_clusters.tsv
```

## TPMC BGC Catalog

Index: `https://download.cncb.ac.cn/bigd/TPMC/TPMC_BGC/`

The BGC directory contains 73,864 antiSMASH-predicted BGC GenBank files and a summary spreadsheet. The project readme reports BiG-SCAPE grouping into Terpene, RiPPs, Others, PKSother, NRPS, PKSI, PKS-NRP_Hybrids, and Saccharides.

| File | Size | URL | Notes |
| --- | ---: | --- | --- |
| `TPMC_BGC_73864.tar.gz` | 954.6 MB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_BGC/TPMC_BGC_73864.tar.gz` | Archive of 73,864 BGC `.gbk` files. |
| `BGC_summary.xlsx` | 7.5 MB | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_BGC/BGC_summary.xlsx` | BGC summary metadata. |
| `readme` | 442 B | `https://download.cncb.ac.cn/bigd/TPMC/TPMC_BGC/readme` | BGC catalog description from CNCB-NGDC. |

Example:

```bash
curl -L -C - -O https://download.cncb.ac.cn/bigd/TPMC/TPMC_BGC/TPMC_BGC_73864.tar.gz
curl -L -C - -O https://download.cncb.ac.cn/bigd/TPMC/TPMC_BGC/BGC_summary.xlsx
```

## TLGC Gene Catalog

Index: `https://download.cncb.ac.cn/bigd/TPMC/TLGC_gene_catalog/`

The TLGC catalog combines the 498 Tibetan Plateau samples with 109 additional Chinese ladder-step samples for a 329,568,659-gene non-redundant catalog.

| File | Size | URL | Notes |
| --- | ---: | --- | --- |
| `TLGC_non_redundant_gene_rep_seq_nucl.fasta.gz` | 72.9 GB | `https://download.cncb.ac.cn/bigd/TPMC/TLGC_gene_catalog/TLGC_non_redundant_gene_rep_seq_nucl.fasta.gz` | Representative nucleotide sequences for the TLGC gene catalog. |
| `readme` | 445 B | `https://download.cncb.ac.cn/bigd/TPMC/TLGC_gene_catalog/readme` | TLGC catalog description from CNCB-NGDC. |

Example:

```bash
curl -L -C - -O https://download.cncb.ac.cn/bigd/TPMC/TLGC_gene_catalog/TLGC_non_redundant_gene_rep_seq_nucl.fasta.gz
```

## Automation Decision

A source-specific `download.py` is not needed. The catalog assets are stable, public static files with predictable direct URLs.

If a helper is added later, it should read the CNCB-NGDC static directory listings, emit a manifest with file sizes and modification dates, and avoid downloading the raw GSA project by default because it is about 19.5 TB.

## Verification and Caveats

- The TPMC homepage, GSA page, and static CNCB indexes were checked on 2026-05-09.
- The static catalog indexes did not expose checksum files during curation.
- The GSA page recommends FTP/Qtrans for large raw-sequence transfers because HTTP speed can be limited.
- The project page states that TPMC catalogs are free to use, but underlying metagenomes are protected by GSA data release and utilization policies.
- The directory readmes use shorter labels for some files; prefer the exact filenames listed in the static indexes.
