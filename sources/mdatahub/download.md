# Microbiome Datahub Download Notes

Microbiome Datahub has two practical command-line access paths:

- bulk direct files for whole-database DNA/protein sequence assets
- API endpoints for targeted project metadata, per-genome sequence ZIPs, and per-genome KEGG module JSON

Use bulk files first when the goal is all data. Use the API when you already have BioProject or GCA identifiers and want a smaller subset.

## Bulk Full-Database Downloads

The official bulk sequence root is:

- `http://palaeo.nig.ac.jp/Resources/MDatahub/2025/`

Officially documented bulk files:

| Asset | URL | Notes |
| --- | --- | --- |
| All MAG DNA contigs | `http://palaeo.nig.ac.jp/Resources/MDatahub/2025/20250810AllMAG.fasta.gz` | 146 GB; contains all contig sequences from 218,653 MAGs. |
| Contig to MAG map | `http://palaeo.nig.ac.jp/Resources/MDatahub/2025/20250810AllMAG.rm.tsv.gz` | 287 MB; maps contigs to MAG GCA IDs. |
| All MAG proteins | `http://palaeo.nig.ac.jp/Resources/MDatahub/2025/AllMergedMDatahubProtein.faa.gz` | 79 GB; contains 454,799,231 predicted protein sequences. |
| Protein to MAG map | `http://palaeo.nig.ac.jp/Resources/MDatahub/2025/AllMergedMDatahubProtein.rm.tsv.gz` | 7 GB; maps proteins to MAG GCA IDs. |
| 40% protein cluster representatives | `http://palaeo.nig.ac.jp/Resources/MDatahub/2025/cluster40Res_rep_seq.fasta.gz` | 11 GB; LinClust representative sequences for 69,769,482 clusters. |
| 90% protein cluster representatives | `http://palaeo.nig.ac.jp/Resources/MDatahub/2025/clusterRes_rep_seq.fasta.gz` | 33 GB; LinClust representative sequences for 192,557,564 clusters. |

Recommended resumable commands:

```bash
# List all known bulk URLs from this repository.
python3 scripts/mdatahub/download.py list --group bulk

# Write a wget input file, then download outside the repository.
python3 scripts/mdatahub/download.py url --group bulk --plain > mdatahub-bulk.urls
wget -c -i mdatahub-bulk.urls

# Or download one large file directly.
wget -c http://palaeo.nig.ac.jp/Resources/MDatahub/2025/20250810AllMAG.fasta.gz
```

During curation on 2026-04-25, the NIG bulk host did not respond from the current network. The URLs above come from the official Microbiome Datahub documentation; users should verify reachability from their server network before launching multi-day downloads.

## Zenodo Metadata And Matrix Files

Zenodo record:

- `https://zenodo.org/records/18073262`
- DOI: `https://doi.org/10.5281/zenodo.18073262`
- Concept DOI: `https://doi.org/10.5281/zenodo.16963985`

Current record files:

| File | Size | Notes |
| --- | ---: | --- |
| `MicrobiomeDatahub_MAGData_20251228.xlsx` | 44,184,875 bytes | Main MAG metadata workbook. |
| `MicrobiomeDatahub_MAGBac2Feature_20250827.xlsx` | 31,316,179 bytes | Bac2Feature phenotype prediction workbook. |
| `MicrobiomeDatahubMAGModuleComposition.tsv.gz` | 11,664,667 bytes | KEGG module composition matrix inferred from MBGD ortholog composition. |
| `ModuleListName.tsv` | 29,006 bytes | KEGG module labels. |

Command-line examples:

```bash
# Print latest-record Zenodo file URLs from the Zenodo API.
python3 scripts/mdatahub/download.py url --group zenodo --plain

# Download all current Zenodo files with the standard-library helper.
python3 scripts/mdatahub/download.py download --group zenodo --output-dir /data/mdatahub/zenodo

# Or use curl directly for a specific file.
curl -L -o MicrobiomeDatahub_MAGData_20251228.xlsx \
  https://zenodo.org/api/records/18073262/files/MicrobiomeDatahub_MAGData_20251228.xlsx/content
```

## Download API

The API manual is:

- `https://mdatahub.org/apimanual`
- raw documentation source: `https://raw.githubusercontent.com/microbiomedatahub/microbiome-datahub/main/docs/apimanual.md`

Documented endpoints:

| Purpose | URL pattern | Output |
| --- | --- | --- |
| Project metadata | `https://mdatahub.org/api/dl/project/metadata/<BIOPROJECT[,BIOPROJECT...]>` | TSV |
| Genome metadata | `https://mdatahub.org/api/dl/genome/metadata/<GCA[,GCA...]>` | TSV, but tested examples returned HTTP 500 on 2026-04-25. |
| Genome sequence | `https://mdatahub.org/api/dl/sequence/genome/<GCA[,GCA...]>` | ZIP |
| CDS sequence | `https://mdatahub.org/api/dl/sequence/cds/<GCA[,GCA...]>` | ZIP |
| Protein sequence | `https://mdatahub.org/api/dl/sequence/protein/<GCA[,GCA...]>` | ZIP |
| KEGG modules for one genome | `https://mdatahub.org/api/genome/mbgd/<GCA>` | JSON |

Examples:

```bash
# Project metadata TSV.
curl -L -o project_metadata.tsv \
  https://mdatahub.org/api/dl/project/metadata/PRJNA982417

# Multiple project metadata records.
curl -L -o project_metadata.tsv \
  https://mdatahub.org/api/dl/project/metadata/PRJNA982417,PRJNA981657,PRJNA981705

# One genome sequence ZIP.
curl -L -o sequence_genome.zip \
  https://mdatahub.org/api/dl/sequence/genome/GCA_000208265.2

# CDS and protein sequence ZIPs.
curl -L -o sequence_cds.zip \
  https://mdatahub.org/api/dl/sequence/cds/GCA_000208265.2
curl -L -o sequence_protein.zip \
  https://mdatahub.org/api/dl/sequence/protein/GCA_000208265.2

# KEGG module JSON for one genome.
curl -L -o GCA_029762515.1.kegg_modules.json \
  https://mdatahub.org/api/genome/mbgd/GCA_029762515.1
```

The helper script can build the API URLs without requiring a browser:

```bash
python3 scripts/mdatahub/download.py url \
  --asset sequence-genome \
  --ids GCA_000208265.2,GCA_001735855.1 \
  --plain

python3 scripts/mdatahub/download.py download \
  --asset kegg-modules \
  --ids GCA_029762515.1 \
  --output-dir /data/mdatahub/api
```
