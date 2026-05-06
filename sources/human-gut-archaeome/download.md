# Human Gut Archaeome Download Notes

The human gut archaeome genome catalogue is associated with the Nature Microbiology article "A catalogue of 1,167 genomes from the human gut archaeome."

Primary links:

- Article: `https://www.nature.com/articles/s41564-021-01020-9`
- EBI genome sets index: `https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/`
- Genome archive: `https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/archaea_gut-genomes.tar.gz`

## Core Genome Archive

| Asset | URL | Size | Notes |
| --- | --- | ---: | --- |
| Recovered archaeal genomes | `https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/archaea_gut-genomes.tar.gz` | 657 MiB | Bulk archive listed by the article data availability statement as recovered genomes in generic feature format. |

Download with resume support:

```bash
curl -L -C - -O https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/archaea_gut-genomes.tar.gz
```

Inspect the archive before extracting:

```bash
tar -tzf archaea_gut-genomes.tar.gz | head
```

Extract when ready:

```bash
tar -xzf archaea_gut-genomes.tar.gz
```

## Supplementary Files

Nature hosts the companion files as public static assets.

| Asset | URL | Size | Notes |
| --- | --- | ---: | --- |
| Supplementary Information | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-021-01020-9/MediaObjects/41564_2021_1020_MOESM1_ESM.pdf` | 1.05 MiB | Supplementary results, tables, and material. |
| Reporting Summary | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-021-01020-9/MediaObjects/41564_2021_1020_MOESM2_ESM.pdf` | 67 KiB | Nature reporting summary. |
| Peer Review Information | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-021-01020-9/MediaObjects/41564_2021_1020_MOESM3_ESM.pdf` | 1.43 MiB | Peer review file. |
| Supplementary Data 1 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-021-01020-9/MediaObjects/41564_2021_1020_MOESM4_ESM.zip` | 29.7 MiB | Unified human archaeal protein catalogue based on 50% identity clustering. |
| Supplementary Data 2 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-021-01020-9/MediaObjects/41564_2021_1020_MOESM5_ESM.zip` | 119 MiB | DIAMOND BLASTx mapped protein matrix used for downstream statistical analyses. |
| Supplementary Data 3 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-021-01020-9/MediaObjects/41564_2021_1020_MOESM6_ESM.txt` | 845 KiB | mcrA gene alignment for M. smithii and M. smithii_A. |
| Supplementary Data 4 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-021-01020-9/MediaObjects/41564_2021_1020_MOESM7_ESM.txt` | 18 KiB | Environmental and human archaeal 16S rRNA genes. |
| Supplementary Tables | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-021-01020-9/MediaObjects/41564_2021_1020_MOESM8_ESM.xlsx` | 5.70 MiB | Supplementary Tables 1-14; includes accession details for used genomes and metagenomes. |

Example targeted downloads:

```bash
curl -L -o human-gut-archaeome-supplementary-tables.xlsx 'https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-021-01020-9/MediaObjects/41564_2021_1020_MOESM8_ESM.xlsx'
curl -L -o human-gut-archaeome-protein-catalogue.zip 'https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-021-01020-9/MediaObjects/41564_2021_1020_MOESM4_ESM.zip'
```

## Verification and Caveats

- No `md5`, `sha256`, or separate checksum file was observed in the EBI `genome_sets` directory during curation.
- The EBI archive supports HTTP range requests, so `curl -C -` or `wget -c` is appropriate.
- The article states that all used genomes and metagenomes are publicly available from NCBI and MGnify, with accession details in Supplementary Table 1a-f.
- The study did not generate custom code according to the article code availability statement.

Checked on 2026-05-06.
