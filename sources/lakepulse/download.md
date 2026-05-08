# LakePulse MAG Catalogue Download Notes

This resource is associated with the Nature Microbiology article "A genome catalogue of lake bacterial diversity and its drivers at continental scale."

Primary links:

- Article: `https://www.nature.com/articles/s41564-023-01435-6`
- Data availability section: `https://www.nature.com/articles/s41564-023-01435-6#data-availability`
- Dryad record: `https://datadryad.org/dataset/doi:10.5061/dryad.zkh1893fs`
- ENA MAG project: `https://www.ebi.ac.uk/ena/browser/view/PRJEB62834`
- ENA raw-read project: `https://www.ebi.ac.uk/ena/browser/view/PRJEB29238`
- JGI GOLD study: `https://gold.jgi.doe.gov/study?id=Gs0136026`
- Code repository: `https://github.com/rebeccagarner/lakepulse_mags`

## Dryad Files

Dryad record `10.5061/dryad.zkh1893fs` is titled "The LakePulse Metagenome-Assembled Genome catalogue" and is released under CC0-1.0. Version 6 exposes 15 public files totaling approximately 64.3 GB.

Use the Dryad API file endpoints for direct downloads:

| File | Size | SHA-256 | URL |
| --- | ---: | --- | --- |
| `LakePulse_MAGs-contigs.zip` | 643.1 MB | `3094973e8a35ea317009c03dca1d19abd5201883258cc3bf3f549135556395f8` | `https://datadryad.org/api/v2/files/2471867/download` |
| `LakePulse_MAGs-aa.zip` | 383.9 MB | `7d60a752ca77da39dbedb56ce5bed2b05c5d288c98a82053be42c3377c4492f2` | `https://datadryad.org/api/v2/files/2471866/download` |
| `LakePulse_MAGs-gff.zip` | 66.2 MB | `00b0eda09043b82646ad8f9519b2f979478d85d5a5e397557d06a417177d61ec` | `https://datadryad.org/api/v2/files/2471865/download` |
| `AH_coassembly-contigs.fa.gz` | 4.2 GB | `e4d25adb9da5ecfc507bd75628422859590b3f050afa9da4dd4d32fe5b9a1d23` | `https://datadryad.org/api/v2/files/2473311/download` |
| `AM_coassembly-contigs.fa.gz` | 4.4 GB | `20dbe32911218b9d01eaccfc0297cc7a98b2c8b47195c21662622de647434971` | `https://datadryad.org/api/v2/files/2473314/download` |
| `BCTC_coassembly-contigs.fa.gz` | 4.7 GB | `b9b6029f09ce720222bddece9989b247ed7c28c317e549958c3dfa65aa3c3207` | `https://datadryad.org/api/v2/files/2473317/download` |
| `BP_coassembly-contigs.fa.gz` | 7.8 GB | `c3debb9bc8a22893475341a6ab700dea89dc6ae5de9e324e4adddebb666e7ac6` | `https://datadryad.org/api/v2/files/2473340/download` |
| `BS_coassembly-contigs.fa.gz` | 4.3 GB | `3a81b540a89b86dabc1b37621b5a27b2b35d6cf9ca61d2557daa7162ae785c72` | `https://datadryad.org/api/v2/files/2473387/download` |
| `MC_coassembly-contigs.fa.gz` | 6.1 GB | `1066673fcb3b25890c4e28be078b64c28445ef06d3c19360d969fe3f3cc2dd3b` | `https://datadryad.org/api/v2/files/2473674/download` |
| `MP_coassembly-contigs.fa.gz` | 4.3 GB | `0aa067575bf1c1bfa0a80e5c9838ec416084eae4eb86654d82ac03ebf3c2b91b` | `https://datadryad.org/api/v2/files/2473825/download` |
| `P_coassembly-contigs.fa.gz` | 9.8 GB | `d1e4d8cc7661b57559046d263e45bd692283dbf1d0d46965ec759af8216e39fc` | `https://datadryad.org/api/v2/files/2473895/download` |
| `PM_coassembly-contigs.fa.gz` | 6.2 GB | `89ab9839a82bd9dc794450bd12e6b7ffe638e958ee97062a1a424017fe67a72e` | `https://datadryad.org/api/v2/files/2473919/download` |
| `SAP_coassembly-contigs.fa.gz` | 5.2 GB | `17604406e3256fd4a36a361d01cb67d7e995e0927f843942218ddb2728ad91ab` | `https://datadryad.org/api/v2/files/2473971/download` |
| `TP_coassembly-contigs.fa.gz` | 5.9 GB | `ae387a01b86e2f365666835b701cf027ad255026791b4b1dd5900a0e0e0681bc` | `https://datadryad.org/api/v2/files/2473984/download` |
| `README.md` | 3.6 KB | `329320939f5d04efb8b2dd911bfda1fe4a0314425bc69143bd731f060e4e9958` | `https://datadryad.org/api/v2/files/2473990/download` |

Download examples:

```bash
curl -L -C - -o LakePulse_MAGs-contigs.zip 'https://datadryad.org/api/v2/files/2471867/download'
curl -L -C - -o LakePulse_MAGs-aa.zip 'https://datadryad.org/api/v2/files/2471866/download'
curl -L -C - -o LakePulse_MAGs-gff.zip 'https://datadryad.org/api/v2/files/2471865/download'
```

Verify checksums after download:

```bash
shasum -a 256 LakePulse_MAGs-contigs.zip
shasum -a 256 LakePulse_MAGs-aa.zip
shasum -a 256 LakePulse_MAGs-gff.zip
```

Inspect ZIP contents before extraction:

```bash
unzip -l LakePulse_MAGs-contigs.zip | head
unzip -l LakePulse_MAGs-aa.zip | head
unzip -l LakePulse_MAGs-gff.zip | head
```

## ENA Accessions

The article data availability statement separates the raw reads and the MAG deposit:

| Asset | Accession | URL | Notes |
| --- | --- | --- | --- |
| Raw metagenome reads | `PRJEB29238` | `https://www.ebi.ac.uk/ena/browser/view/PRJEB29238` | ENA reported 368 read-run rows during curation. |
| MAGs and associated records | `PRJEB62834` | `https://www.ebi.ac.uk/ena/browser/view/PRJEB62834` | ENA reported 1,008 assembly rows and 1,019 analysis rows during curation. |

Useful ENA API checks:

```bash
curl -L 'https://www.ebi.ac.uk/ena/browser/api/xml/PRJEB29238'
curl -L 'https://www.ebi.ac.uk/ena/browser/api/xml/PRJEB62834'
curl -L 'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJEB29238&result=read_run&fields=run_accession,fastq_ftp,fastq_md5,fastq_bytes&format=tsv'
curl -L 'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJEB62834&result=assembly&fields=assembly_accession,assembly_name,wgs_set,description,assembly_type,base_count,version&format=tsv'
curl -L 'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJEB62834&result=analysis&fields=analysis_accession,analysis_alias,generated_ftp,generated_md5,generated_bytes,analysis_type&format=tsv'
```

For bulk raw-read retrieval, generate accession manifests from ENA and use ENA-supported FTP/Aspera workflows rather than scraping browser pages.

## JGI GOLD

The article lists JGI GOLD study `Gs0136026` for co-assemblies and annotations:

- `https://gold.jgi.doe.gov/study?id=Gs0136026`

It also lists these analysis project accessions:

| Ecozone | GOLD analysis project |
| --- | --- |
| Boreal/Taiga Cordilleras | `Ga0495746` |
| Montane Cordillera | `Ga0495744` |
| Pacific Maritime | `Ga0495745` |
| Taiga Plains | `Ga0495743` |
| Semi-Arid Plateaux | `Ga0485099` |
| Boreal Plains | `Ga0485102` |
| Prairies | `Ga0485100` |
| Mixedwood Plains | `Ga0364548` |
| Boreal Shield | `Ga0373103` |
| Atlantic Highlands | `Ga0372599` |
| Atlantic Maritime | `Ga0372598` |

The GOLD study URL returned a generic error page during curation, so treat these as article-reported GOLD accessions and use Dryad for stable bulk co-assembly contig files.

## Nature Supplementary Files

The Nature page hosts companion files as Springer static assets:

| Asset | URL | Notes |
| --- | --- | --- |
| Reporting Summary | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-023-01435-6/MediaObjects/41564_2023_1435_MOESM1_ESM.pdf` | Nature reporting summary. |
| Supplementary Tables 1-4 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-023-01435-6/MediaObjects/41564_2023_1435_MOESM2_ESM.xlsx` | Metagenome information, MAG quality/taxonomy/file names, novel MAG counts, and GDM results. |
| Peer Review File | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-023-01435-6/MediaObjects/41564_2023_1435_MOESM3_ESM.pdf` | Peer reviewer reports. |

Source data files:

| Asset | URL |
| --- | --- |
| Source Data Fig. 1 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-023-01435-6/MediaObjects/41564_2023_1435_MOESM4_ESM.xlsx` |
| Source Data Fig. 2 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-023-01435-6/MediaObjects/41564_2023_1435_MOESM5_ESM.xlsx` |
| Source Data Fig. 3 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-023-01435-6/MediaObjects/41564_2023_1435_MOESM6_ESM.xlsx` |
| Source Data Fig. 4 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-023-01435-6/MediaObjects/41564_2023_1435_MOESM7_ESM.xlsx` |
| Source Data Fig. 5 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-023-01435-6/MediaObjects/41564_2023_1435_MOESM8_ESM.xlsx` |

## Automation Decision

A source-specific `download.py` is not needed. The direct Dryad API file endpoints, ENA report APIs, and Springer static assets are sufficient for reproducible access.

If a helper is added later, it should generate a Dryad URL/checksum manifest and ENA accession reports. It should not download the 64 GB Dryad file set by default.

## Verification

Checked on 2026-05-08.

During curation:

- Dryad API reported dataset id `112775`, version id `248470`, 15 files, and `64,292,409,479` bytes total storage.
- ENA `PRJEB29238` reported 368 read-run rows.
- ENA `PRJEB62834` reported 1,008 assembly rows and 1,019 analysis rows.
- GitHub API reported the `rebeccagarner/lakepulse_mags` repository as public and MIT-licensed.
