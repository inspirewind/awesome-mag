# TPMC Notes

Verified on 2026-05-09 against the TPMC project page, CNCB-NGDC static download indexes, GSA accession `CRA011511`, BioProject `PRJCA017393`, and Crossref metadata for DOI `10.1038/s41467-024-45895-8`.

TPMC is the Tibetan Plateau Microbial Catalog from "A genome and gene catalog of the aquatic microbiomes of the Tibetan Plateau."

The resource is in scope for Awesome MAG because it provides a public, region-specific aquatic MAG catalog from high-altitude water ecosystems, with companion gene catalogs, BGC predictions, sample metadata, and raw metagenomes in GSA.

## Resource Profile

Paper- and site-reported scale:

- 498 Tibetan Plateau aquatic metagenomes across saline lakes, freshwater lakes, rivers, hot springs, wetlands, and glaciers
- 32,355 medium- and high-quality MAGs
- 10,723 representative genome-based species
- 2,024 high-quality MAGs
- 296,289,678 non-redundant TPMC genes
- 73,864 antiSMASH BGCs grouped with BiG-SCAPE
- 329,568,659 non-redundant TLGC genes built from the 498 TP samples plus 109 additional Chinese ladder-step samples

## Data Availability

The TPMC page exposes four static CNCB-NGDC catalog directories:

- `TPMC_genome_catalog/` for MAG FASTA archive and MAG summary metadata
- `TPMC_gene_catalog/` for representative nucleotide/protein sequences, clustering results, and functional annotations
- `TPMC_BGC/` for antiSMASH BGC GenBank files and summary metadata
- `TLGC_gene_catalog/` for the broader three-step ladder topography gene catalog

The page also links all 607 metagenomes to GSA accession `CRA011511`. The GSA page reports 1,214 files totaling 19,459.39 GB, with HTTPS, FTP, Qtrans, and Aspera access paths.

## Curation Caveats

- Use the TPMC page as the descriptive landing page and the CNCB static download directories as the reproducible catalog download route.
- The static catalog directories expose file sizes and modification dates, but no checksum files were found during curation.
- Several large TPMC gene files are plain `.fa` or `.tsv`, not compressed archives. Plan storage and transfer accordingly.
- The directory readmes use shortened names such as `TPMC_MAG.gz` and `TPMC_BGC.gz`, while the actual downloadable files are `TPMC_MAG.tar.gz` and `TPMC_BGC_73864.tar.gz`.
- Raw metagenomes are subject to GSA data release and utilization policies. The project page says the TPMC catalogs are free to use, while encouraging contact for planned analyses or publications that may overlap with project goals.

No source-specific automation script is needed for this resource.
