# Caprinae Gut MAG Catalog Download Notes

This resource is distributed across the Microbiology Spectrum article, CNCB BioProject/GSA records, ScienceDirect/Elsevier supplement files, and an authors' GitHub repository.

Primary links:

- Article: `https://journals.asm.org/doi/10.1128/spectrum.02211-22`
- DOI: `https://doi.org/10.1128/spectrum.02211-22`
- ScienceDirect mirror: `https://www.sciencedirect.com/org/science/article/pii/S2165049722010320`
- CNCB BioProject: `https://ngdc.cncb.ac.cn/bioproject/browse/PRJCA008889`
- GSA project: `https://ngdc.cncb.ac.cn/gsa/browse/CRA007205`
- GSA HTTPS directory: `https://download.cncb.ac.cn/gsa2/CRA007205/`
- GSA checksum file: `https://download.cncb.ac.cn/gsa2/CRA007205/md5sum.txt`
- GitHub code repository: `https://github.com/qb-lyu/caprinaeGut`

## Raw Reads

Raw metagenomic reads are public under CNCB BioProject `PRJCA008889` and GSA project `CRA007205`.

The GSA page reports:

| Field | Value |
| --- | --- |
| Project | `CRA007205` |
| BioProject | `PRJCA008889` |
| Runs | 30 |
| Sequence files | 60 |
| Reported file size | 1218.75 GB |
| Release date | 2022-10-21 |

Direct access routes:

| Route | URL | Notes |
| --- | --- | --- |
| GSA browser | `https://ngdc.cncb.ac.cn/gsa/browse/CRA007205` | Project page, run table, metadata export, and download routes. |
| HTTPS directory | `https://download.cncb.ac.cn/gsa2/CRA007205/` | Public Apache-style directory with run subfolders and `md5sum.txt`. |
| FTP directory | `ftp://download.big.ac.cn/gsa2/CRA007205` | GSA-listed FTP route. |
| Qtrans | `https://qtp.cncb.ac.cn/qtrans/v2/file?path=/gsa2/CRA007205` | Browser-oriented high-speed transfer route. |
| Aspera | `aspera01@download.cncb.ac.cn:/gsa2/CRA007205` | GSA page gives the command template and key download. |

Example targeted downloads:

```bash
curl -L -C - -O 'https://download.cncb.ac.cn/gsa2/CRA007205/md5sum.txt'
curl -L -C - -O 'https://download.cncb.ac.cn/gsa2/CRA007205/CRR516072/CRR516072_f1.fq.gz'
curl -L -C - -O 'https://download.cncb.ac.cn/gsa2/CRA007205/CRR516072/CRR516072_r2.fq.gz'
```

Verify downloaded FASTQ files against `md5sum.txt`.

Example first-run file metadata observed from the public directory:

| File | Size |
| --- | ---: |
| `CRR516072_f1.fq.gz` | 20,431,184,241 bytes |
| `CRR516072_r2.fq.gz` | 21,022,402,226 bytes |
| `CRR516072_sta.xml` | 1,347 bytes |

## Run Layout

The public GSA directory has one folder per run:

```text
CRR516072/
CRR516073/
...
CRR516101/
md5sum.txt
```

Each run folder follows the paired-read naming pattern:

```text
CRR516072_f1.fq.gz
CRR516072_r2.fq.gz
CRR516072_sta.xml
```

The `md5sum.txt` file contains 60 checksum entries, one for each FASTQ file.

## Supplementary Files

The ScienceDirect mirror exposes the article supplement files as direct `ars.els-cdn.com` URLs.

| File | Size | URL | Notes |
| --- | ---: | --- | --- |
| `spectrum.02211-22-s0001.xlsx` | 1.5 MB | `https://ars.els-cdn.com/content/image/1-s2.0-S2165049722010320-spectrum.02211-22-s0001.xlsx` | Workbook with sheets `ST1` through `ST9`. |
| `spectrum.02211-22-s0002.xlsx` | 689.5 KB | `https://ars.els-cdn.com/content/image/1-s2.0-S2165049722010320-spectrum.02211-22-s0002.xlsx` | Workbook with sheets `ST10` through `ST18`. |
| `spectrum.02211-22-s0003.pdf` | 681.2 KB | `https://ars.els-cdn.com/content/image/1-s2.0-S2165049722010320-spectrum.02211-22-s0003.pdf` | Supplementary figure PDF. |

Example:

```bash
curl -L -C - -o spectrum.02211-22-s0001.xlsx \
  'https://ars.els-cdn.com/content/image/1-s2.0-S2165049722010320-spectrum.02211-22-s0001.xlsx'
curl -L -C - -o spectrum.02211-22-s0002.xlsx \
  'https://ars.els-cdn.com/content/image/1-s2.0-S2165049722010320-spectrum.02211-22-s0002.xlsx'
curl -L -C - -o spectrum.02211-22-s0003.pdf \
  'https://ars.els-cdn.com/content/image/1-s2.0-S2165049722010320-spectrum.02211-22-s0003.pdf'
```

These files are useful for MAG-level metadata, annotations, and supplementary figures. They are not a replacement for a bulk MAG sequence archive.

## MAG Sequence Availability

The paper reports a catalog of 5,046 MAGs, including 1,933 high-quality and 3,113 medium-quality MAGs. However, the reproducible public endpoints checked here expose raw reads and supplementary tables, not a stable bulk MAG FASTA/protein archive.

Checked routes:

| Route | Result |
| --- | --- |
| GSA `CRA007205` public directory | 30 run folders, paired FASTQ files, and `md5sum.txt`. |
| CNCB GWH BioProject lookup for `PRJCA008889` | Returned `count: 0` assembly records during curation. |
| CNCB OMIX lookup for `PRJCA008889` | Returned `totalCount: 0` during curation. |
| GitHub `qb-lyu/caprinaeGut` | Code/figure repository, no release archive and no declared license. |

For analyses that require the MAG FASTA files themselves, use the article and supplement metadata to identify the resource, then check the article page in a browser or contact the corresponding authors.

## Workflow Repository

The authors' repository is:

```text
https://github.com/qb-lyu/caprinaeGut
```

GitHub API metadata observed during curation:

| Field | Value |
| --- | --- |
| Default branch | `master` |
| Main language | `R` |
| Declared license | none |
| Top-level contents | `README.md`, `figure1/` through `figure6/` |

The repository is useful for figure/workflow context but should not be treated as a bulk data source.

## Automation Decision

No source-specific script is needed for the README entry.

A future helper could safely:

- enumerate `https://download.cncb.ac.cn/gsa2/CRA007205/`
- emit a 60-file FASTQ manifest from the 30 run directories
- download `md5sum.txt`
- optionally download the small supplementary files

It should not download 1.2 TB of FASTQ files by default, and it should not try to infer or reconstruct a missing MAG sequence archive.

## Verification

Checked on 2026-05-11.

- Crossref DOI metadata reported the title, authors, Microbiology Spectrum volume 10 issue 6, article number `e02211-22`, PubMed ID `36321901`, and Creative Commons Attribution 4.0 article license.
- CNCB BioProject `PRJCA008889` reported 30 BioSample records, one GSA project, agricultural/metagenome scope, and the same DOI/PubMed publication.
- GSA `CRA007205` reported 60 files totaling 1218.75 GB and public HTTPS/FTP/Qtrans/Aspera routes.
- The GSA direct download directory exposed run folders `CRR516072` through `CRR516101` and `md5sum.txt`.
- ScienceDirect supplement URLs returned HTTP 200 with content lengths 1,553,086 bytes, 689,500 bytes, and 681,239 bytes.
- The ASM DOI page returned a Cloudflare challenge from command-line access, so supplement verification used the ScienceDirect mirror and CDN URLs.
