# Meta320 Sheep and Goat Gut MAGs Download Notes

Meta320 data are distributed across the article, NCBI SRA, a Figshare share, Springer supplementary files, and the authors' GitHub workflow repository.

Primary links:

- Article: `https://link.springer.com/article/10.1186/s40168-024-01806-z`
- DOI: `https://doi.org/10.1186/s40168-024-01806-z`
- NCBI BioProject: `https://www.ncbi.nlm.nih.gov/bioproject/PRJNA972320`
- NCBI runinfo CSV: `https://trace.ncbi.nlm.nih.gov/Traces/sra-db-be/runinfo?acc=PRJNA972320`
- Figshare share: `https://figshare.com/s/fe5fb3dd964a15844505`
- GitHub workflow repository: `https://github.com/bladrome/meta320_binning`

## Raw Reads

Raw metagenomic reads are under NCBI BioProject `PRJNA972320` / SRA study `SRP438552`.

| Asset | URL | Notes |
| --- | --- | --- |
| BioProject | `https://www.ncbi.nlm.nih.gov/bioproject/PRJNA972320` | Public project titled "metagenomics of 320 goat and sheep". |
| Article reviewer dataview | `https://dataview.ncbi.nlm.nih.gov/object/PRJNA972320?reviewer=cbpvcbh5i6pfuqc3cfmv2ck30j` | Link listed by the article. |
| Runinfo CSV | `https://trace.ncbi.nlm.nih.gov/Traces/sra-db-be/runinfo?acc=PRJNA972320` | 320 SRA runs; about 1.05 TB SRA size at curation time. |
| Example run | `SRR24653945` | Paired Illumina HiSeq 4000 metagenomic WGA run. |

Fetch the run manifest:

```bash
curl -L -o meta320-runinfo.csv \
  'https://trace.ncbi.nlm.nih.gov/Traces/sra-db-be/runinfo?acc=PRJNA972320'
```

Download reads through SRA Toolkit:

```bash
prefetch SRR24653945
fasterq-dump --split-files --threads 8 SRR24653945
```

Or use the `download_path` column in the NCBI runinfo CSV if direct SRA object downloads are preferred. Example path observed for `SRR24653945`:

```text
https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos6/sra-pub-zq-40/SRR024/24653/SRR24653945/SRR24653945.lite.1
```

## MAG Assemblies

The Figshare share exposes a file titled "5,810 genomes of meta320", corresponding to the article's medium- and high-quality MAG set:

```text
https://figshare.com/s/fe5fb3dd964a15844505
```

The observed direct Figshare file endpoint:

```text
https://figshare.com/ndownloader/files/40441679?private_link=fe5fb3dd964a15844505
```

returned `HTTP/2 202` with `x-amzn-waf-action: challenge` during one curation check, but the same file can also be addressed through the official file downloader host:

```text
https://ndownloader.figshare.com/files/40441679?private_link=fe5fb3dd964a15844505
```

The repository now includes a thin download wrapper at `corpus/download_bash/part4_hard_datasets/meta320.sh`. It does not scrape or bypass Figshare protections; it only uses the public private-link file endpoint and should be validated on the target server before writing the filelist builder.

## Springer Supplementary Files

These files are direct static assets from Springer and are useful for metadata, annotation, and MAG-level curation.

| File | URL | Notes |
| --- | --- | --- |
| Additional file 1 / Figure S1-S9 | `https://static-content.springer.com/esm/art%3A10.1186%2Fs40168-024-01806-z/MediaObjects/40168_2024_1806_MOESM1_ESM.docx` | Pipeline and supplementary figures. |
| Additional file 2 / Table S1 | `https://static-content.springer.com/esm/art%3A10.1186%2Fs40168-024-01806-z/MediaObjects/40168_2024_1806_MOESM2_ESM.xls` | Background information on sheep and goat samples. |
| Additional file 3 / Table S2 | `https://static-content.springer.com/esm/art%3A10.1186%2Fs40168-024-01806-z/MediaObjects/40168_2024_1806_MOESM3_ESM.xls` | General features of the gene catalogs. |
| Additional file 4 / Table S3-S6 | `https://static-content.springer.com/esm/art%3A10.1186%2Fs40168-024-01806-z/MediaObjects/40168_2024_1806_MOESM4_ESM.xls` | Sheep core NR genes, species, CAZy families, and KEGG functions. |
| Additional file 5 / Table S7-S10 | `https://static-content.springer.com/esm/art%3A10.1186%2Fs40168-024-01806-z/MediaObjects/40168_2024_1806_MOESM5_ESM.xls` | Goat core NR genes, species, CAZy families, and KEGG functions. |
| Additional file 6 / Table S11 | `https://static-content.springer.com/esm/art%3A10.1186%2Fs40168-024-01806-z/MediaObjects/40168_2024_1806_MOESM6_ESM.xls` | Species found only in goat and sheep samples. |
| Additional file 7 / Table S12 | `https://static-content.springer.com/esm/art%3A10.1186%2Fs40168-024-01806-z/MediaObjects/40168_2024_1806_MOESM7_ESM.xls` | KEGG level-2 analysis of grazing and drylot goat groups. |
| Additional file 8 / Table S13 | `https://static-content.springer.com/esm/art%3A10.1186%2Fs40168-024-01806-z/MediaObjects/40168_2024_1806_MOESM8_ESM.xlsx` | Relative abundance of 5,810 medium- and high-quality MAGs. |
| Additional file 9 / Table S14 | `https://static-content.springer.com/esm/art%3A10.1186%2Fs40168-024-01806-z/MediaObjects/40168_2024_1806_MOESM9_ESM.xlsx` | CAZyme-predicted proteins of 5,810 medium- and high-quality MAGs. |
| Additional file 10 / Table S15 | `https://static-content.springer.com/esm/art%3A10.1186%2Fs40168-024-01806-z/MediaObjects/40168_2024_1806_MOESM10_ESM.xlsx` | 91 sheep-specific MAGs and one goat-specific MAG. |
| Additional file 11 / Table S16 | `https://static-content.springer.com/esm/art%3A10.1186%2Fs40168-024-01806-z/MediaObjects/40168_2024_1806_MOESM11_ESM.xlsx` | CAZyme-predicted proteins of the 92 host-specific MAGs. |
| Additional file 12 / Table S17 | `https://static-content.springer.com/esm/art%3A10.1186%2Fs40168-024-01806-z/MediaObjects/40168_2024_1806_MOESM12_ESM.xlsx` | Predicted PULs for the 92 host-specific MAGs. |

Example:

```bash
curl -L -C - -O \
  'https://static-content.springer.com/esm/art%3A10.1186%2Fs40168-024-01806-z/MediaObjects/40168_2024_1806_MOESM8_ESM.xlsx'
```

## Workflow Repository

The authors' repository is:

```text
https://github.com/bladrome/meta320_binning
```

It contains:

- `readme.org`: workflow notes
- `envs/`: conda/mamba environment files
- `pipeline/`: scripts for preprocessing, assembly/binning, taxonomy, and functional annotation

The pipeline mentions tools including metaWRAP, dRep, GTDB-Tk release 207, eggNOG-mapper, run_dbcan, PULpy, cd-hit, seqkit, and SRA-compatible read processing tools.

## Automation Decision

A thin source-specific download script is included because the Figshare share exposes one MAG assemblies file.

The reproducible parts are already covered by stable public endpoints:

- NCBI SRA runinfo CSV for raw-read manifests
- SRA Toolkit or runinfo `download_path` values for read transfer
- Springer static supplementary file URLs for table downloads

The Figshare MAG sequence endpoint should still be treated as network-sensitive. If the server receives an HTML challenge/error page instead of the binary file, use browser-mediated download or revisit the Figshare route rather than adding challenge-bypass logic. After a successful download, inspect the payload packaging and FASTA headers before building the RabbitTClust filelist.

## Verification

- Crossref DOI metadata checked on 2026-05-11.
- NCBI BioProject `PRJNA972320` and runinfo CSV checked on 2026-05-11.
- SRA runinfo reported 320 runs, 3,444,597,693,300 bases, and 1,075,195 MB.
- GitHub repository `bladrome/meta320_binning` checked on 2026-05-11.
- Springer Additional files 8, 9, and 12 returned HTTP 200 during curation.
- Figshare direct file endpoint returned `HTTP/2 202` with `x-amzn-waf-action: challenge` during curation.
