# OMDB Notes

Verified on 2026-05-09 against the OMDB About page, OMDB ocean repository pages, and the Sunagawa Lab v2.0 static download backend.

OMDB is the Ocean Microbiomics DataBase from the Sunagawa Lab. Version 2.0 was released on 2025-05-25 and is focused on genome-resolved ocean microbiome data.

The resource is in scope for Awesome MAG because it exposes reconstructed ocean microbial genomes with per-genome FASTA, gene nucleotide FASTA, protein FASTA, GFF, antiSMASH output links, and large derived gene/scaffold catalogs.

## Resource Profile

Site-reported OMDB v2.0 scale:

- 274,282 reconstructed genomes.
- 32,022 species-level units.
- 348 marine microbiome projects.
- 12,260 geo-referenced samples.
- 508,832,278 gene calls in the redundant nucleotide and amino-acid gene catalogs.

The browser covers studies, samples, genomes, genes, annotations, taxonomy, and map views. The same content can be accessed in bulk through the Sunagawa Lab static backend.

## Data Availability

The practical bulk entry point is `OMDBv2.0_data.tsv.gz`. It has one row per genome and columns for:

- genome ID
- sample ID
- study ID
- genome FASTA URL
- nucleotide gene FASTA URL
- amino-acid gene FASTA URL
- GFF URL
- antiSMASH tarball URL

During curation, the links TSV decompressed to 274,283 lines, which is 274,282 genome rows plus the header. This matches the headline genome count on the OMDB site.

The backend also exposes:

- a 1.5 TB `OMDv2.genomes.db.tar.gz` archive
- a 31 MB `OMDv2_GENO_all_genome_files` manifest
- nucleotide gene catalogs at redundant, NR100, and NR95 levels
- amino-acid gene catalogs at redundant, NR100, NR50, and NR30 levels
- scaffold catalogs at redundant and NR100 levels

## Curation Caveats

- Prefer the links TSV for reproducible selective download. It avoids recursive traversal of a very large nested directory tree.
- The whole-database archive uses the file prefix `OMDv2` rather than `OMDBv2.0`; record this literally.
- Catalog sequence files are large, ranging from about 2 GB to 150 GB, and cluster tables can also be several GB.
- The catalog directory lists MD5 sidecar files. Most tested MD5 sidecars were directly readable, but `OMDBv2.0_data.tsv.gz.md5` returned HTTP 403 during curation. The official download documentation itself reports the links TSV MD5 as `c1b5f14c9b7899f7300ccf41e62f8681`.
- OMDB states that all data are freely available under CC BY 4.0 and that citation information for OMDB will be provided separately.

No source-specific automation script is needed now. If one is added later, it should generate a URL manifest from `OMDBv2.0_data.tsv.gz` and require explicit user selection before downloading large genome or catalog files.
