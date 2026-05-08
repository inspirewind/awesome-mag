# Glacier-fed Streams (GFS) MAGs Download Notes

This resource is associated with the Nature Microbiology article "Mapping the metagenomic diversity of the multi-kingdom glacier-fed stream microbiome."

Primary links:

- Article: `https://www.nature.com/articles/s41564-024-01874-9`
- Data availability section: `https://www.nature.com/articles/s41564-024-01874-9#data-availability`
- NCBI BioProject: `https://www.ncbi.nlm.nih.gov/bioproject/PRJNA781406`
- Zenodo record: `https://zenodo.org/records/13890040`
- Project website: `https://www.glacierstreams.ch/`

## NCBI Archive

The article data availability statement says that all raw sequencing data and MAGs are deposited under BioProject `PRJNA781406`.

Useful entry points:

| Asset | URL | Notes |
| --- | --- | --- |
| BioProject | `https://www.ncbi.nlm.nih.gov/bioproject/PRJNA781406` | Primary project record for the Vanishing Glaciers Project. |
| SRA search | `https://www.ncbi.nlm.nih.gov/sra?term=PRJNA781406` | Raw sequencing runs associated with the project. |
| Assembly search | `https://www.ncbi.nlm.nih.gov/assembly/?term=PRJNA781406` | Assembly and MAG records associated with the project. |
| BioProject summary API | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=bioproject&id=781406&retmode=json` | Machine-readable project metadata. |

During curation, NCBI E-utilities reported the BioProject title as "Vanishing Glaciers Project" and the description as "Investigating the microbiomes associated to glacier-fed streams around the world."

Example metadata checks:

```bash
curl -L 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=bioproject&id=781406&retmode=json'
curl -L 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=sra&term=PRJNA781406&retmode=json&retmax=0'
curl -L 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=assembly&term=PRJNA781406&retmode=json&retmax=0'
```

For bulk SRA retrieval, use NCBI tools such as `datasets`, `sra-tools`, or generated accession lists from the SRA Run Selector rather than scraping the browser pages.

## Zenodo Prokaryotic MAG Files

Zenodo record `10.5281/zenodo.13890040` is titled "MAGs from glacier-fed streams" and is released under Creative Commons Attribution 4.0. It contains three public files:

| File | Size | MD5 | URL |
| --- | ---: | --- | --- |
| `ProkaryoticMAGsContig.tar` | 3.2 GB | `92ce0436b073d4480cc4f841d9b6f5e4` | `https://zenodo.org/records/13890040/files/ProkaryoticMAGsContig.tar?download=1` |
| `ProkaryoticMAGsGff.tar` | 1.8 GB | `7d04f9d9f11b6df8510ada2e638636f8` | `https://zenodo.org/records/13890040/files/ProkaryoticMAGsGff.tar?download=1` |
| `ProkaryoticMAGsProtein.tar` | 597.9 MB | `5d3c9d2419345aa7196540ef58010ee7` | `https://zenodo.org/records/13890040/files/ProkaryoticMAGsProtein.tar?download=1` |

Download with resume support:

```bash
curl -L -C - -o ProkaryoticMAGsContig.tar 'https://zenodo.org/records/13890040/files/ProkaryoticMAGsContig.tar?download=1'
curl -L -C - -o ProkaryoticMAGsGff.tar 'https://zenodo.org/records/13890040/files/ProkaryoticMAGsGff.tar?download=1'
curl -L -C - -o ProkaryoticMAGsProtein.tar 'https://zenodo.org/records/13890040/files/ProkaryoticMAGsProtein.tar?download=1'
```

Verify checksums after download:

```bash
cat > md5.txt <<'EOF'
92ce0436b073d4480cc4f841d9b6f5e4  ProkaryoticMAGsContig.tar
7d04f9d9f11b6df8510ada2e638636f8  ProkaryoticMAGsGff.tar
5d3c9d2419345aa7196540ef58010ee7  ProkaryoticMAGsProtein.tar
EOF
md5sum -c md5.txt
```

Inspect before extracting:

```bash
tar -tf ProkaryoticMAGsContig.tar | head
tar -tf ProkaryoticMAGsGff.tar | head
tar -tf ProkaryoticMAGsProtein.tar | head
```

## Nature Supplementary Files

The Nature page hosts article companion files as Springer static assets:

| Asset | URL | Notes |
| --- | --- | --- |
| Reporting Summary | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM1_ESM.pdf` | Nature reporting summary. |
| Peer Review File | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM2_ESM.pdf` | Peer reviewer reports. |
| Supplementary Tables 1-6 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM3_ESM.xlsx` | General sample, metagenome, prokaryotic MAG, eukaryotic MAG, carotenoid gene, and interaction-gene tables. |

Example targeted downloads:

```bash
curl -L -o gfs-reporting-summary.pdf 'https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM1_ESM.pdf'
curl -L -o gfs-peer-review-file.pdf 'https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM2_ESM.pdf'
curl -L -o gfs-supplementary-tables.xlsx 'https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM3_ESM.xlsx'
```

## Nature Source Data Files

The Nature page also exposes figure source data files:

| Asset | URL |
| --- | --- |
| Source Data Fig. 1 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM4_ESM.xlsx` |
| Source Data Fig. 2 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM5_ESM.xlsx` |
| Source Data Fig. 3 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM6_ESM.xlsx` |
| Source Data Fig. 4 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM7_ESM.xlsx` |
| Source Data Fig. 5 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM8_ESM.xlsx` |
| Source Data Fig. 6 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM9_ESM.xlsx` |
| Source Data Extended Data Fig. 1 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM10_ESM.txt` |
| Source Data Extended Data Fig. 2 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM11_ESM.txt` |
| Source Data Extended Data Fig. 3 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM12_ESM.txt` |
| Source Data Extended Data Fig. 4 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM13_ESM.txt` |
| Source Data Extended Data Fig. 5 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM14_ESM.xlsx` |
| Source Data Extended Data Fig. 6 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM15_ESM.txt` |
| Source Data Extended Data Fig. 7 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM16_ESM.txt` |
| Source Data Extended Data Fig. 8 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM17_ESM.txt` |
| Source Data Extended Data Fig. 9 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01874-9/MediaObjects/41564_2024_1874_MOESM18_ESM.txt` |

## Code Repositories

The article code availability statement points to two GitHub repositories:

| Repository | URL | Notes |
| --- | --- | --- |
| MAG workflow code | `https://github.com/michoug/VanishingGlacierMAGs` | Python repository; GitHub API reported MIT license during curation. |
| R analysis code | `https://github.com/michoug/VanishingGlaciersRcode` | R code for the project; no license field was exposed by the GitHub API during curation. |

## Automation Decision

A source-specific `download.py` is not needed. The major access routes are public:

- NCBI BioProject/SRA/Assembly records for raw sequencing data and MAGs
- Zenodo direct file URLs with checksums for prokaryotic MAG contigs, GFF files, and protein files
- Springer static assets for reporting, supplementary tables, and source data files

If a helper is added later, it should generate accession manifests from NCBI E-utilities or the SRA Run Selector and should avoid scraping interactive NCBI pages.

## Verification and Caveats

- The article reports 156 sediment metagenomes collected from glacier-fed stream biofilms across 9 mountain ranges, yielding 2,855 bacterial MAGs.
- Zenodo describes the companion record as "MAGs from glacier-fed streams" and exposes three files totaling 5.2 GB.
- HTTP HEAD checks against the Zenodo direct file URLs returned a 504 gateway response during curation on 2026-05-08, so the Zenodo page metadata was used for file size and checksum recording.
- NCBI E-utilities reported 2,240 SRA records and 3,387 Assembly records matching `PRJNA781406` during curation on 2026-05-08; treat those as archive-level search counts, not as the article's metagenome count.

Checked on 2026-05-08.
