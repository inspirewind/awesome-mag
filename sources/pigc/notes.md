# PIGC Notes

PIGC (Pig Integrated Gene Catalog) is the pig gut microbial gene catalog and MAG resource from the Nature Communications paper "An expanded catalog of microbial genes and metagenome-assembled genomes from the pig gut microbiome".

The paper sequenced 500 pig gut samples from 8 countries and more than 40 breeds, then integrated prior PGC data for the gene catalog. It reports PIGC catalogs from 787 gut metagenomes with 48,697,887 PIGC100 genes, 17,237,052 PIGC90 genes, and 7,246,447 PIGC50 genes, plus 6,339 non-redundant MAGs clustered into 2,673 species-level genome bins. Of those SGBs, 2,309 were unknown based on the reference databases used in the paper.

The resource is in scope for Awesome MAG because it is a large animal-associated MAG and gene catalog with public CNGB/CNSA accessions, assembly FASTA files, raw metagenomic FASTQ links, supplementary tables, and code provenance. It belongs under animal-associated MAG resources.

The primary reproducible data route is the CNGBdb project `CNP0000824`. The project page reports 503 samples, 500 experiments, 500 runs, and 6,347 assemblies. The current public `metadata_CNP0000824_assembly.tsv` also has 6,347 assembly rows, while the paper-level dereplicated/non-redundant MAG count is 6,339. Keep both numbers: use 6,339 when describing the published non-redundant MAG catalog, and use 6,347 when describing current CNGBdb assembly files.

The official `data_download_links_CNP0000824_ftp.txt` manifest contains 7,347 links: 6,347 `assembly` FASTA links and 1,000 `experiment` FASTQ links. Filter on the first column when building MAG-only download lists.

The article data availability section also points to the PIGC code repository on GitHub and a Zenodo code archive. These are useful for methods provenance, but they are not the primary route for bulk genome or read downloads.

Checked on 2026-05-08.
