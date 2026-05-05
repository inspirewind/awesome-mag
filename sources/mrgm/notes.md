# MRGM Notes

MRGM (Mouse Reference Gut Microbiome) is a mouse gut bacterial genome catalog from Insuk Lee's Network Biology Lab at Yonsei University / decodebiome. The public site reports 42,245 non-redundant genomes with completeness >=90% and contamination <=5%, spanning 1,524 bacterial species, plus sequence and functional information for about 1.7 million non-redundant proteins.

The resource is in scope for Awesome MAG because it is a large animal-associated MAG and genome catalog with public genome downloads, protein catalogs, 16S rRNA metadata, and custom Kraken2 / MetaPhlAn databases. It belongs under animal-associated MAG resources, and shares the decodebiome access pattern already used by HRGM and HROM.

Downloads use the same decodebiome pattern as HRGM and HROM: a PHP file browser (`listdir.php`) lists directories, while files are retrievable through direct HTTPS URLs. Direct directory access under `data/` returns 403, so automation should enumerate through `listdir.php` or known metadata-derived paths.

There is no formal data API, no published checksum manifest, and no Zenodo mirror found for MRGM during curation. The all-genomes directory has a 43 GB `genome.tar.gz` archive, but the non-redundant-genomes directory currently only exposes per-genome files and metadata. Its README mentions `genome.tar.gz`; the matching direct URL returned 404 when checked.

Primary citation:

- Kim N, Kim CY, Ma J, Yang S, Park DJ, Ha SJ, Belenky P, Lee I. MRGM: an enhanced catalog of mouse gut microbial genomes substantially broadening taxonomic and functional landscapes. Gut Microbes 16(1):2393791 (2024). https://doi.org/10.1080/19490976.2024.2393791

Raw metagenomic sequencing data for the in-house samples are available from NCBI SRA study `SRP335854`. The paper states that MRGM sequences and annotations are available from the decodebiome MRGM site.

Checked on 2026-05-06.
