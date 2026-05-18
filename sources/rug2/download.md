# RUG2 Rumen MAGs Download Notes

RUG2 has three useful public access paths:

- ENA project accessions for raw reads, primary metagenome assemblies, and binned metagenome assemblies
- the Stewart et al. author pages for human-readable assembly/bin indexes
- Edinburgh DataShare for the large protein, cluster, annotation, synteny, and table archive

A source-specific corpus script is now provided to turn the ENA TSV report into a resumable MAG FASTA manifest:

```bash
bash corpus/download_bash/part4_hard_datasets/rug2.sh --manifest-only
bash corpus/download_bash/part4_hard_datasets/rug2.sh --downloader aria2c --jobs 4 --connections 2
```

The script downloads only the ENA `binned metagenome` assembly FASTA files under
`downloads/rug2/assemblies/`. It does not download raw reads, primary metagenome
assemblies, or the Edinburgh DataShare protein/annotation companion archive.

## ENA Accessions

The article data availability section names `PRJEB31266` as the primary ENA project for raw reads, primary assemblies, and RUGs. It also points to `PRJEB21624` for raw reads from the earlier Stewart et al. 2018 Illumina NextSeq rumen study.

| Asset | URL | Notes |
| --- | --- | --- |
| Primary ENA project | `https://www.ebi.ac.uk/ena/browser/view/PRJEB31266` | Raw reads, primary assemblies, and binned/RUG assembly records. |
| Previous-read ENA project | `https://www.ebi.ac.uk/ena/browser/view/PRJEB21624` | Reads reused from Stewart et al. 2018. |
| Raw read TSV | `https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJEB31266&result=read_run&fields=study_accession,sample_accession,experiment_accession,run_accession,fastq_ftp,fastq_md5,fastq_bytes&format=tsv` | Includes semicolon-separated FASTQ FTP URLs, MD5s, and byte counts. |
| Previous-read TSV | `https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJEB21624&result=read_run&fields=study_accession,sample_accession,experiment_accession,run_accession,fastq_ftp,fastq_md5,fastq_bytes&format=tsv` | Same fields for the earlier read project. |
| Sequence assembly TSV | `https://www.ebi.ac.uk/ena/portal/api/search?result=analysis&query=study_accession=%22PRJEB31266%22%20AND%20analysis_type=%22SEQUENCE_ASSEMBLY%22&fields=study_accession,analysis_accession,sample_accession,analysis_title,analysis_type,assembly_type,generated_ftp,submitted_ftp,submitted_bytes,submitted_md5&format=tsv` | Assemblies with current ENA FTP links. |

Recommended metadata exports:

```bash
curl -L -o PRJEB31266.read_run.tsv \
  "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJEB31266&result=read_run&fields=study_accession,sample_accession,experiment_accession,run_accession,fastq_ftp,fastq_md5,fastq_bytes&format=tsv"

curl -L -o PRJEB21624.read_run.tsv \
  "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJEB21624&result=read_run&fields=study_accession,sample_accession,experiment_accession,run_accession,fastq_ftp,fastq_md5,fastq_bytes&format=tsv"

curl -L -o PRJEB31266.sequence_assemblies.tsv \
  "https://www.ebi.ac.uk/ena/portal/api/search?result=analysis&query=study_accession=%22PRJEB31266%22%20AND%20analysis_type=%22SEQUENCE_ASSEMBLY%22&fields=study_accession,analysis_accession,sample_accession,analysis_title,analysis_type,assembly_type,generated_ftp,submitted_ftp,submitted_bytes,submitted_md5&format=tsv"
```

Use the TSVs to build URL lists for `wget` or `aria2c`. The `fastq_ftp`, `generated_ftp`, and `submitted_ftp` fields are semicolon-separated where multiple files exist.

Example single-file downloads from records verified during curation:

```bash
# One paired-end raw read run from PRJEB31266.
wget -c ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR320/005/ERR3201375/ERR3201375_1.fastq.gz
wget -c ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR320/005/ERR3201375/ERR3201375_2.fastq.gz

# One primary metagenome assembly.
wget -c ftp://ftp.sra.ebi.ac.uk/vol1/analysis/ERZ102/ERZ1024259/10676_0004_idba.fa.gz

# One binned metagenome assembly.
wget -c ftp://ftp.sra.ebi.ac.uk/vol1/analysis/ERZ103/ERZ1037592/10674_0001_idba_bin.100.fa.gz
```

## Author Index Pages

The author-maintained RUG2 page is:

- `https://vetgenomics.github.io/metagenomics/stewart2019/`

Useful subpages:

| Page | URL | Notes |
| --- | --- | --- |
| Metagenome assemblies | `https://vetgenomics.github.io/metagenomics/stewart2019/metagenome_assemblies/` | Lists 288 metagenome assemblies: 282 primary assemblies and 6 coassemblies. |
| Metagenome assemblies CSV | `https://vetgenomics.github.io/metagenomics/stewart2019/metagenome_assemblies.csv` | CSV with sample accession, sample name, assembler, assembly type, assembly accession, and FASTA URL. |
| Bins page | `https://vetgenomics.github.io/metagenomics/stewart2019/test/` | Lists 20,469 Illumina bins at least 50% complete and less than 10% contaminated. These are the bins from which the final 4,941 MAGs were selected. |

During curation on 2026-05-08, the metagenome assemblies CSV returned valid CSV. The bins page itself loaded, but its relative `bins_table_sorted_plus_urls.csv` link returned the site's 404 page from the current network. Use the HTML page or ENA analysis TSV if the CSV remains unavailable.

## Edinburgh DataShare Archive

The DataShare record is:

- DOI: `https://doi.org/10.7488/ds/2470`
- landing page: `https://datashare.ed.ac.uk/handle/10283/3224`
- file: `rug2.tar.gz`
- listed size: 29.76 Gb
- observed `Content-Length`: 31,958,778,104 bytes

The article describes this archive as containing predicted proteins, gene clusters, annotations of the RUGs and their synteny, and associated data tables.

Direct bitstream URL observed from the landing page:

```text
https://datashare.ed.ac.uk/bitstream/handle/10283/3224/rug2.tar.gz?isAllowed=y&sequence=1
```

Resumable download example:

```bash
curl -L -C - -o rug2.tar.gz \
  "https://datashare.ed.ac.uk/bitstream/handle/10283/3224/rug2.tar.gz?isAllowed=y&sequence=1"
```

During curation on 2026-05-08, the DataShare landing page loaded and the bitstream URL returned `200 OK`, `Content-Length: 31958778104`, and `Content-Disposition: attachment;filename="rug2.tar.gz"`. The HEAD response was slow, so use a resumable downloader for the full archive.

## Automation Decision

A source-specific script is provided for the MAG sequence payload:

- `corpus/download_bash/part4_hard_datasets/rug2.sh`
- `scripts/rug2/download.py`

The useful machine-readable paths are:

- ENA Portal API TSV reports
- stable ENA FTP paths in the TSV reports
- one DataShare bitstream URL
- one author-maintained CSV for the primary metagenome assemblies

The helper only turns ENA TSV fields into a plain URL manifest and does not scrape browser state.

## Verification

Checked on 2026-05-08:

- ENA read-run filereport for `PRJEB31266` returned FASTQ FTP paths.
- ENA read-run filereport for `PRJEB21624` returned FASTQ FTP paths.
- ENA analysis search for `PRJEB31266` returned `primary metagenome` and `binned metagenome` `SEQUENCE_ASSEMBLY` records with FTP paths and MD5s.
- `https://vetgenomics.github.io/metagenomics/stewart2019/metagenome_assemblies.csv` returned CSV.
- DataShare landing page listed `rug2.tar.gz` as 29.76 Gb; the bitstream URL returned HTTP 200 with a 31,958,778,104 byte `Content-Length`.

Checked on 2026-05-18:

- `scripts/rug2/download.py --manifest-only` returned 20,567 ENA binned metagenome FASTA entries.
