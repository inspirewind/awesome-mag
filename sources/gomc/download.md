# GOMC Download Notes

GOMC has a proper bulk download table on the Microbiome Data Portal page:

- dataset page: `https://db.cngb.org/maya/datasets/MDB0000002`
- download API: `https://db.cngb.org/maya/api/get_download?dataset_id=MDB0000002&page=1&per_page=100&sort=default`
- bulk directory: `https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/`

Use the MDB0000002 bulk directory for normal downloads. The `CNP0004049` CNSA project remains useful for accession-level metadata and per-assembly files, but it is not the primary bulk route.

## Bulk Files

The `get_download` API currently returns 8 public items:

| File | Description | Size | URL |
| --- | --- | ---: | --- |
| `md5.txt` | MD5 checksums for the compressed bulk files | 245B | `https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/md5.txt` |
| `Supplementary_Data/` | Supplementary data directory | directory | `https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/Supplementary_Data/` |
| `43191.all_MAGs.tar.gz` | 43,191 MAGs recovered in the study | 30.80GB | `https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/43191.all_MAGs.tar.gz` |
| `43191.all_MAGs/` | Directory view of the recovered MAG files | directory | `https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/43191.all_MAGs/` |
| `24195.GOMC_genomes.tar.gz` | Global ocean microbiome genome catalogue sequences | 17.91GB | `https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/24195.GOMC_genomes.tar.gz` |
| `24195.GOMC_genomes/` | Directory view of the GOMC genome catalogue files | directory | `https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/24195.GOMC_genomes/` |
| `GOPC.geneset.pep.fa.gz` | Global ocean microbiome protein catalogue sequences | 171.33GB | `https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/GOPC.geneset.pep.fa.gz` |
| `unprecedented_genome_size_MAGs.tar.gz` | Three large bacterial genomes | 15.57MB | `https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/unprecedented_genome_size_MAGs.tar.gz` |

Download examples:

```bash
wget -c https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/md5.txt
wget -c https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/43191.all_MAGs.tar.gz
wget -c https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/24195.GOMC_genomes.tar.gz
wget -c https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/GOPC.geneset.pep.fa.gz
wget -c https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/unprecedented_genome_size_MAGs.tar.gz
```

The files support byte ranges, so `wget -c`, `curl -C -`, or `aria2c -c` are appropriate. Use conservative concurrency for the large protein catalogue.

## Checksums

`md5.txt` contains:

```text
683212865e370f9529928fc5d97d0eae  GOPC.geneset.pep.fa.gz
a37afc2813860ea26cd84d0ac6c128d7  24195.GOMC_genomes.tar.gz
1649313bc82b6f87100fd0140babff78  43191.all_MAGs.tar.gz
ac8aec9d23aa9d42edfbd42cdd224f8a  unprecedented_genome_size_MAGs.tar.gz
```

Verification example:

```bash
md5sum -c md5.txt
```

## Supplementary Data

The supplementary directory is:

- `https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/Supplementary_Data/`

Files observed in that directory:

| File | Size |
| --- | ---: |
| `Environmental_factors_vs_microbial_community_variation.pdf` | 6.04MB |
| `GOMC_large_bacterial_genomes.pdf` | 2.94MB |
| `SmallRNA.CL100176085_L01_25.fq.gz` | 4.70MB |
| `UMAP_biogeographical_distribution.pdf` | 44.47MB |

## CNP0004049 Accession Archive

The CNGBdb project page is:

- `https://db.cngb.org/data_resources/project/CNP0004049`

Its public metadata directory is:

- `https://ftp.cngb.org/pub/CNSA/data7/public_info/CNP0004049/`

Useful files there:

| File | Notes |
| --- | --- |
| `data_download_links_CNP0004049_ftp.txt` | Plain-text manifest of 16,240 CNSA assembly FASTA URLs. |
| `metadata_CNP0004049_assembly.tsv` | Assembly metadata including sample accession, assembly accession, FASTA file name, MD5, size, contig count, and N50. |
| `metadata_CNP0004049_sample_Metagenome_or_environmental_sample.tsv` | Sample metadata including location, collection date, organism, and representative count descriptions. |

Use these files when CNSA accessions or per-assembly metadata matter. For normal GOMC sequence retrieval, prefer the MDB0000002 bulk archives above.

## Automation Decision

A source-specific `download.py` is not needed. The dataset already provides:

- a public JSON download table through `get_download`
- stable direct HTTPS URLs
- directory indexes for the bulk folders
- a checksum file

If a helper is added later, it should only mirror the API response into a URL list for `wget` or `aria2c`; it should not scrape browser state or replay clicks.

## Verification

During curation, the `get_download` API returned 8 public entries. HTTP HEAD checks on the four compressed bulk files returned `200 OK` and `Accept-Ranges: bytes`.

Observed compressed file sizes:

| File | Content-Length |
| --- | ---: |
| `43191.all_MAGs.tar.gz` | 33,068,644,897 bytes |
| `24195.GOMC_genomes.tar.gz` | 19,227,227,555 bytes |
| `GOPC.geneset.pep.fa.gz` | 183,959,496,042 bytes |
| `unprecedented_genome_size_MAGs.tar.gz` | 16,325,042 bytes |
