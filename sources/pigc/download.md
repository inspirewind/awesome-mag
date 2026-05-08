# PIGC Download Notes

PIGC data are publicly accessible through the CNGB/CNSA project archive:

- project page: `https://db.cngb.org/data_resources/project/CNP0000824`
- public metadata directory: `https://ftp.cngb.org/pub/CNSA/data7/public_info/CNP0000824/`
- download manifest: `https://ftp.cngb.org/pub/CNSA/data7/public_info/CNP0000824/data_download_links_CNP0000824_ftp.txt`
- assembly metadata: `https://ftp.cngb.org/pub/CNSA/data7/public_info/CNP0000824/metadata_CNP0000824_assembly.tsv`
- experiment metadata: `https://ftp.cngb.org/pub/CNSA/data7/public_info/CNP0000824/metadata_CNP0000824_experiment.tsv`
- sample metadata: `https://ftp.cngb.org/pub/CNSA/data7/public_info/CNP0000824/metadata_CNP0000824_sample_Metagenome_or_environmental_sample.tsv`

No source-specific automation script is needed. The official manifest and metadata TSVs are enough for `curl`, `wget`, or `aria2c` workflows.

## Public Info Files

| File | Rows observed | Size | Notes |
| --- | ---: | ---: | --- |
| `data_download_links_CNP0000824_ftp.txt` | 7,347 links | 727.04 KB | 6,347 assembly links and 1,000 experiment FASTQ links |
| `metadata_CNP0000824_assembly.tsv` | 6,347 rows | 1.65 MB | Assembly accession, sample accession, FASTA filename, MD5, taxonomy, and assembly metrics |
| `metadata_CNP0000824_experiment.tsv` | 500 rows | 156.14 KB | Paired-end FASTQ filenames and MD5s |
| `metadata_CNP0000824_sample_Metagenome_or_environmental_sample.tsv` | 502 rows | 48.33 KB | Pig feces sample metadata |

Download the metadata and manifest:

```bash
curl -L -C - -O 'https://ftp.cngb.org/pub/CNSA/data7/public_info/CNP0000824/data_download_links_CNP0000824_ftp.txt'
curl -L -C - -O 'https://ftp.cngb.org/pub/CNSA/data7/public_info/CNP0000824/metadata_CNP0000824_assembly.tsv'
curl -L -C - -O 'https://ftp.cngb.org/pub/CNSA/data7/public_info/CNP0000824/metadata_CNP0000824_experiment.tsv'
curl -L -C - -O 'https://ftp.cngb.org/pub/CNSA/data7/public_info/CNP0000824/metadata_CNP0000824_sample_Metagenome_or_environmental_sample.tsv'
```

## MAG Assemblies

The manifest is a two-column text file. Assembly links have the form:

```text
assembly ftp://ftp.cngb.org/pub/CNSA/data2/CNP0000824/<sample_accession>/<assembly_accession>/<fasta_file_name>
```

Example assembly URL:

```text
ftp://ftp.cngb.org/pub/CNSA/data2/CNP0000824/CNS0178608/CNA0009161/S53008A_bin_73.fa.gz
```

Create a MAG-only URL list:

```bash
awk '$1 == "assembly" {print $2}' data_download_links_CNP0000824_ftp.txt > pigc_assembly_urls.txt
```

Download with a resumable downloader:

```bash
aria2c -c -x 2 -s 2 -i pigc_assembly_urls.txt
```

Use conservative concurrency because this expands to thousands of small assembly files.

## Raw Metagenomic Reads

Experiment links in the same manifest are paired FASTQ files from the 500 metagenomic runs:

```text
experiment ftp://ftp.cngb.org/pub/CNSA/data2/CNP0000824/<sample_accession>/<experiment_accession>/<run_accession>/<fastq_file_name>
```

Example read URL:

```text
ftp://ftp.cngb.org/pub/CNSA/data2/CNP0000824/CNS0178788/CNX0143359/CNR0176314/QH616240FF5204_NDME10026_1.clean.fq.gz
```

Create a read-only URL list:

```bash
awk '$1 == "experiment" {print $2}' data_download_links_CNP0000824_ftp.txt > pigc_experiment_urls.txt
```

## Supplementary Data And Code

The Nature article provides supplementary tables and source data alongside the CNGBdb archive:

| Asset | URL |
| --- | --- |
| Supplementary Information | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-021-21295-0/MediaObjects/41467_2021_21295_MOESM1_ESM.pdf` |
| Supplementary Data 1 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-021-21295-0/MediaObjects/41467_2021_21295_MOESM4_ESM.xlsx` |
| Supplementary Data 2 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-021-21295-0/MediaObjects/41467_2021_21295_MOESM5_ESM.xlsx` |
| Supplementary Data 3 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-021-21295-0/MediaObjects/41467_2021_21295_MOESM6_ESM.xlsx` |
| Supplementary Data 4 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-021-21295-0/MediaObjects/41467_2021_21295_MOESM7_ESM.xlsx` |
| Supplementary Data 5 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-021-21295-0/MediaObjects/41467_2021_21295_MOESM8_ESM.xlsx` |
| Source Data | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-021-21295-0/MediaObjects/41467_2021_21295_MOESM10_ESM.zip` |
| Code repository | `https://github.com/zhouyunyan/PIGC` |
| Zenodo code archive | `https://zenodo.org/records/4381340` |

## Caveats

- The paper reports 6,339 non-redundant MAGs, whereas the current CNGBdb assembly metadata exposes 6,347 assembly rows. Treat the 6,339 count as the published catalog statistic and the 6,347 count as the current archive-level file count.
- The CNGBdb project page reports 503 samples, while the current public sample metadata file `metadata_CNP0000824_sample_Metagenome_or_environmental_sample.tsv` contains 502 data rows. Use the project page for portal-level statistics and the TSV for reproducible file-level workflows.
- The manifest uses `ftp://` URLs. Some modern environments disable FTP by default; if needed, use a downloader with FTP support or construct equivalent HTTPS URLs only after testing them.
- No checksum manifest was found beyond the MD5 columns embedded in the assembly and experiment metadata TSVs.

Checked on 2026-05-08.
