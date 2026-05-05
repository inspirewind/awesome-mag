# HROM Notes

HROM (Human Reference Oral Microbiome) is a human oral microbial genome catalog from Insuk Lee's Network Biology Lab at Yonsei University / decodebiome. The public site reports 72,641 high-quality genomes from 3,426 species and 8,492,076 non-redundant protein sequences with annotations.

The resource is in scope for Awesome MAG because it is a large human-associated MAG and genome catalog with public bulk downloads, per-species representative genomes, non-redundant genome archives, species pangenomes, protein catalogs, 16S rRNA sequences, and Kraken2 / MetaPhlAn4 custom databases. It belongs under human-associated MAG resources.

Downloads use the same decodebiome pattern as HRGM: a PHP file browser (`listdir.php`) lists directories, while files are retrievable through direct HTTPS URLs. Direct directory access under `data/` returns 403, so automation should enumerate through `listdir.php` or known metadata-derived paths.

There is no formal data API, no published checksum manifest, and no Zenodo mirror found for HROM during curation. No official GitHub code repository was found; the public article states that the assembly pipeline is described on the HROM web server.

The site homepage still lists the citation as "in preparation", but the matching publication is now available:

- Cha JH, Kim N, You JY, et al. A high-quality genomic catalog of the human oral microbiome broadens its phylogeny and clinical insights. Cell Host & Microbe (2025). https://doi.org/10.1016/j.chom.2025.10.013

Checked on 2026-05-05.
