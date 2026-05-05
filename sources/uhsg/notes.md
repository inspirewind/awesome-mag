# UHSG Notes

Verified on 2026-05-06 against the publication metadata and the CNGB/CNSA public download directory.

UHSG (Unified Human Skin Genome) is a human skin MAG catalog from the Advanced Science article "Integrated Human Skin Bacteria Genome Catalog Reveals Extensive Unexplored Habitat-Specific Microbiome Diversity and Function."

The resource is in scope for Awesome MAG because it provides a public, accessioned genome catalog for the human skin microbiome rather than only raw metagenomic reads.

## Resource Profile

Paper-reported scale:

- 450 newly sequenced human facial samples
- 2,069 public human skin metagenomes integrated with the new data
- 5,779 MAGs in UHSG
- 813 prokaryotic species across 22 skin sites
- 470 reported novel species
- 1,385 reported new assembled genomes
- 1,220 reported putative novel secondary metabolites

The paper uses UHSG to analyze habitat-specific skin microbiome diversity and function, including metabolism, antimicrobial resistance, virulence-associated signals, and secondary metabolite biosynthetic potential.

## Data Availability

The article data availability statement points raw sequences and newly assembled genomes to CNGB Sequence Archive project `CNP0002131`.

Primary links:

- Article DOI: <https://doi.org/10.1002/advs.202300050>
- PubMed: <https://pubmed.ncbi.nlm.nih.gov/37548643/>
- PMC: <https://pmc.ncbi.nlm.nih.gov/articles/PMC10558695/>
- CNGBdb project: <https://db.cngb.org/data_resources/project/CNP0002131>
- CNSA public metadata directory: <https://ftp.cngb.org/pub/CNSA/data7/public_info/CNP0002131/>

## Public CNSA Files

The `public_info` directory exposes four useful files:

| File | Size | Last modified | Role |
| --- | ---: | --- | --- |
| `data_download_links_CNP0002131_ftp.txt` | 682.24 KB | 2025-06-24 10:55:12 | Plain-text manifest of assembly FASTA FTP URLs |
| `metadata_CNP0002131_assembly.tsv` | 1.27 MB | 2025-06-24 10:55:23 | Assembly-level metadata and MD5 checksums |
| `metadata_CNP0002131_experiment.tsv` | 122.79 KB | 2025-06-21 12:05:46 | WGS run accessions, FASTQ names, and FASTQ MD5 checksums |
| `metadata_CNP0002131_sample_Microbial_sample.tsv` | 132.11 KB | 2025-06-21 12:04:02 | Sample metadata for human skin metagenome samples |

Observed assembly metadata fields include `project_accession`, `sample_accession`, `assembly_accession`, `assembly_name`, `assembly_method`, `assembly_method_version`, `sequencing_technology`, `fasta_file_name`, `fasta_file_md5`, `total_size(bp)`, `sequences`, and `N50(bp)`.

Observed experiment metadata fields include `experiment_accession`, `run_accession`, `library_strategy`, `platform`, `instrument_model`, paired FASTQ file names, and paired FASTQ MD5 checksums.

## Curation Caveats

- UHSG is distributed through CNSA as per-assembly files; there is no observed single bulk UHSG archive.
- The manifest lines use `ftp://ftp.cngb.org/pub/CNSA/data5/CNP0002131/...` URLs.
- CNGB also exposes an alternate FTP host, `ftp2.cngb.org`, through its copy-download UI.
- Treat the CNGB/CNSA metadata files as the source of truth for MD5 checksums and accession mapping.
- The publication is open access under CC BY 4.0, but the CNSA project files do not expose an obvious separate dataset license in the public directory.
