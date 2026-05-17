# OceanDNA MAG Catalog Download Notes

OceanDNA is primarily a paper-backed dataset with three access routes:

- the Scientific Data article and static Springer supplementary files
- a Springer Nature figshare collection for genome sequences
- INSDC records under BioProject `PRJDB11811` / SRA study `DRP008400`

The article's Data Records section states that all OceanDNA MAG genome sequences are available at figshare. It also states that 8,466 species representatives were submitted as WGS entries under `PRJDB11811`, while 43,859 non-representatives were submitted as DDBJ analysis entries and are available only via DDBJ in addition to figshare.

## Primary Genome Collection

Use the figshare collection as the main human-facing landing page:

- DOI: `https://doi.org/10.6084/m9.figshare.c.5564844.v1`
- collection page: `https://springernature.figshare.com/collections/The_OceanDNA_MAG_catalog_contains_over_50_000_prokaryotic_genomes_originated_from_various_marine_environments/5564844/1`
- DataCite metadata: `https://api.datacite.org/dois/10.6084/m9.figshare.c.5564844.v1`

Plain command-line access to the generic figshare API can be unreliable from some environments, but the server-side probe on 2026-05-18 confirmed that the direct `ndownloader.figshare.com` article endpoint returns the non-representative MAG ZIP as `application/zip`.

## Supplementary Files

The article page exposes five static XLSX supplementary files plus a file-list workbook. These links were reachable by `curl` and returned `Accept-Ranges: bytes`.

| Label | File | Size | Notes |
| --- | --- | ---: | --- |
| File list | `41597_2022_1392_MOESM1_ESM.xlsx` | 9,619 bytes | Lists Supplementary Files S1-S6. |
| S1 | `41597_2022_1392_MOESM2_ESM.xlsx` | 634,453 bytes | 2,057 metagenomes with sample metadata and statistics. |
| S2 | figshare supplementary package | not checked | Eleven multiple alignments and HMMs of terL protein sequences from aquatic viral MAGs; listed in the file-list workbook but not exposed as a static article link. |
| S3 | `41597_2022_1392_MOESM3_ESM.xlsx` | 28,463,431 bytes | OceanDNA MAG genome statistics, functional RNAs, genome quality, and taxonomy. |
| S4 | `41597_2022_1392_MOESM4_ESM.xlsx` | 10,050 bytes | 15 publications of marine SAGs and MAGs. |
| S5 | `41597_2022_1392_MOESM5_ESM.xlsx` | 11,942,764 bytes | Published marine prokaryotic genomes with QS >= 50. |
| S6 | `41597_2022_1392_MOESM6_ESM.xlsx` | 6,324,330 bytes | Species representatives of UGCMP. |

Download the static supplementary workbooks:

```bash
curl -L -C - -O 'https://static-content.springer.com/esm/art%3A10.1038%2Fs41597-022-01392-5/MediaObjects/41597_2022_1392_MOESM1_ESM.xlsx'
curl -L -C - -O 'https://static-content.springer.com/esm/art%3A10.1038%2Fs41597-022-01392-5/MediaObjects/41597_2022_1392_MOESM2_ESM.xlsx'
curl -L -C - -O 'https://static-content.springer.com/esm/art%3A10.1038%2Fs41597-022-01392-5/MediaObjects/41597_2022_1392_MOESM3_ESM.xlsx'
curl -L -C - -O 'https://static-content.springer.com/esm/art%3A10.1038%2Fs41597-022-01392-5/MediaObjects/41597_2022_1392_MOESM4_ESM.xlsx'
curl -L -C - -O 'https://static-content.springer.com/esm/art%3A10.1038%2Fs41597-022-01392-5/MediaObjects/41597_2022_1392_MOESM5_ESM.xlsx'
curl -L -C - -O 'https://static-content.springer.com/esm/art%3A10.1038%2Fs41597-022-01392-5/MediaObjects/41597_2022_1392_MOESM6_ESM.xlsx'
```

The figshare supplementary-file record is useful when the static article page is missing S2:

- `https://doi.org/10.6084/m9.figshare.19416815.v1`
- `https://springernature.figshare.com/articles/dataset/Supplementary_Files_ver_Scientific_Data_/19416815/1`

DataCite reports that record as 70,341,596 bytes under CC0.

## INSDC Metadata

The ENA XML endpoint currently resolves the BioProject and SRA-study metadata:

```bash
curl -L -o PRJDB11811.xml \
  'https://www.ebi.ac.uk/ena/browser/api/xml/PRJDB11811'

curl -L -o DRP008400.xml \
  'https://www.ebi.ac.uk/ena/browser/api/xml/DRP008400'
```

The XML metadata confirms:

- title: `TPA_asm: The OceanDNA MAG catalog: 52,325 prokaryotic genomes reconstructed from various marine environments`
- 52,325 qualified genomes
- 8,466 prokaryotic species-level clusters
- 59 phyla
- QS >= 50 for all genomes
- `ENA-FIRST-PUBLIC` of `2022-04-21` for `PRJDB11811`
- `ENA-FIRST-PUBLIC` of `2022-04-10` and `ENA-LAST-UPDATE` of `2023-08-11` for `DRP008400`

The read-run file report returns nine tiny FASTQ records, so treat it as study metadata rather than the bulk MAG sequence route:

```bash
curl -L -o PRJDB11811-read-run-fastq.tsv \
  'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJDB11811&result=read_run&fields=run_accession,fastq_ftp,fastq_md5,fastq_bytes'
```

For bulk MAG sequence retrieval, combine the Figshare non-representative ZIP with ENA WGS representative FASTA files. The ENA `wgs_set` file report for `PRJDB11811` returns 8,466 representative FASTA URLs in the `set_fasta_ftp` field.

## Automation Decision

A source-specific downloader is implemented as `corpus/download_bash/part4_hard_datasets/oceandna.sh`. It downloads Figshare article `15218454` from the stable direct ndownloader endpoint and enumerates ENA `PRJDB11811` WGS FASTA files into `downloads/oceandna/representatives_manifest.tsv`.

## Verification

During curation on 2026-05-09:

- DataCite resolved `10.6084/m9.figshare.c.5564844.v1` as a CC BY 4.0 figshare collection supplementing the Scientific Data article.
- DataCite resolved `10.6084/m9.figshare.19416815.v1` as the CC0 Scientific Data supplementary-file dataset.
- The ENA XML API returned public `PRJDB11811` / `DRP008400` metadata with the same title and counts.
- The six static Springer supplementary URLs returned `200 OK`.
- On 2026-05-18, the server probe confirmed `https://ndownloader.figshare.com/articles/15218454/versions/1` returns a 26,291,374,398-byte ZIP for 43,859 non-representative MAGs, and the ENA `PRJDB11811` `wgs_set` report returns 8,466 representative FASTA URLs.
