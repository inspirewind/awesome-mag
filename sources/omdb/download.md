# OMDB Download Notes

Primary links:

- About page: `https://omdb.microbiomics.io/about`
- Ocean repository browser: `https://omdb.microbiomics.io/repository/ocean/`
- Download documentation: `https://omdb.microbiomics.io/repository/ocean/suppl_info`
- Static catalog backend: `https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/`
- Static genome backend: `https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/genomes/`

## Download Strategy

Use the small links TSV first for targeted genome-level retrieval:

- `OMDBv2.0_data.tsv.gz`
- URL: `https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_data.tsv.gz`
- MD5 reported by OMDB documentation: `c1b5f14c9b7899f7300ccf41e62f8681`
- Rows checked during curation: 274,283 including header, 274,282 genome rows.

The TSV columns are:

| Column | Meaning |
| --- | --- |
| `GENOME` | OMDB genome identifier. |
| `SAMPLE` | Source sample identifier. |
| `STUDY` | Source study/project identifier. |
| `GENOME_FILE` | Genome FASTA gzip URL. |
| `GENES_NT_FILE` | Predicted nucleotide gene FASTA gzip URL. |
| `GENES_AA_FILE` | Predicted protein FASTA gzip URL. |
| `GENES_GFF_FILE` | Gene annotation GFF gzip URL. |
| `ANTISMASH_FILE` | antiSMASH result tarball URL. |

Recommended manifest setup:

```bash
curl -L -O https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_data.tsv.gz
md5sum OMDBv2.0_data.tsv.gz
gzip -dc OMDBv2.0_data.tsv.gz | head
```

Download one genome FASTA from the manifest:

```bash
genome_id=GARB21-1_SAMN12799101_MAG_00000001
gzip -dc OMDBv2.0_data.tsv.gz \
  | awk -F '\t' -v genome="$genome_id" 'NR > 1 && $1 == genome {print $4}' \
  | xargs -n 1 curl -L -O
```

Download all files listed for one genome:

```bash
genome_id=GARB21-1_SAMN12799101_MAG_00000001
gzip -dc OMDBv2.0_data.tsv.gz \
  | awk -F '\t' -v genome="$genome_id" 'NR > 1 && $1 == genome {for (i=4; i<=8; i++) print $i}' \
  | xargs -n 1 curl -L -O
```

## Genome Archive And Manifests

The genome backend also exposes large whole-database files:

| File | Size | MD5 | URL |
| --- | ---: | --- | --- |
| `OMDv2.genomes.db.tar.gz` | 1.5 TB | `2f254920c9cb72c683d3faf1283ea01a` | `https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/genomes/OMDv2.genomes.db.tar.gz` |
| `OMDv2_GENO_all_genome_files` | 31 MB | not listed in the index | `https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/genomes/OMDv2_GENO_all_genome_files` |

The 1.5 TB archive should not be the default path for most curation work. Prefer the links TSV unless the goal is a full local mirror.

## Catalog Downloads

OMDB publishes nucleotide gene, amino-acid gene, and scaffold catalogs. Each catalog has a sequence file and a cluster table.

### Nucleotide Gene Catalogs

| Catalog | Entries | Threshold | Sequences | Clusters |
| --- | ---: | --- | --- | --- |
| `OMDBv2.0_NT_G_R` | 508,832,278 | none | `OMDBv2.0_NT_G_R.fna.gz` (128 GB) | `OMDBv2.0_NT_G_R.cluster.tsv.gz` (about 5 GB) |
| `OMDBv2.0_NT_G_NR100` | 325,384,975 | 100% | `OMDBv2.0_NT_G_NR100.fna.gz` (88 GB) | `OMDBv2.0_NT_G_NR100.cluster.tsv.gz` (about 4 GB) |
| `OMDBv2.0_NT_G_NR95` | 103,044,829 | 95% | `OMDBv2.0_NT_G_NR95.fna.gz` (27 GB) | `OMDBv2.0_NT_G_NR95.cluster.tsv.gz` (about 3 GB) |

URL pattern:

```text
https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/<CATALOG>/<FILE>
```

Example:

```bash
curl -L -O https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_NT_G_NR95/OMDBv2.0_NT_G_NR95.fna.gz
curl -L -O https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_NT_G_NR95/OMDBv2.0_NT_G_NR95.fna.gz.md5
```

### Amino-Acid Gene Catalogs

| Catalog | Entries | Threshold | Sequences | Clusters |
| --- | ---: | --- | --- | --- |
| `OMDBv2.0_AA_G_R` | 508,832,278 | none | `OMDBv2.0_AA_G_R.faa.gz` (88 GB) | `OMDBv2.0_AA_G_R.cluster.tsv.gz` (about 5 GB) |
| `OMDBv2.0_AA_G_NR100` | 249,518,434 | 100% | `OMDBv2.0_AA_G_NR100.faa.gz` (46 GB) | `OMDBv2.0_AA_G_NR100.cluster.tsv.gz` (about 4 GB) |
| `OMDBv2.0_AA_G_NR50` | 28,862,112 | 50% | `OMDBv2.0_AA_G_NR50.faa.gz` (4 GB) | `OMDBv2.0_AA_G_NR50.cluster.tsv.gz` (about 4 GB) |
| `OMDBv2.0_AA_G_NR30` | 18,342,415 | 30% | `OMDBv2.0_AA_G_NR30.faa.gz` (2 GB) | `OMDBv2.0_AA_G_NR30.cluster.tsv.gz` (about 4 GB) |

Example:

```bash
curl -L -O https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_AA_G_NR50/OMDBv2.0_AA_G_NR50.faa.gz
curl -L -O https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_AA_G_NR50/OMDBv2.0_AA_G_NR50.cluster.tsv.gz
```

### Scaffold Catalogs

| Catalog | Entries | Threshold | Sequences | Clusters |
| --- | ---: | --- | --- | --- |
| `OMDBv2.0_SC_G_R` | 69,280,421 | none | `OMDBv2.0_SC_G_R.fa.gz` (150 GB) | `OMDBv2.0_SC_G_R.cluster.tsv.gz` (about 1 GB) |
| `OMDBv2.0_SC_G_NR100` | 68,726,394 | 100% | `OMDBv2.0_SC_G_NR100.fa.gz` (145 GB) | `OMDBv2.0_SC_G_NR100.cluster.tsv.gz` (about 1 GB) |

Example:

```bash
curl -L -O https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_SC_G_NR100/OMDBv2.0_SC_G_NR100.fa.gz
curl -L -O https://sunagawalab.ethz.ch/share/microbiomics/ocean/db/2.0/data/catalogs/OMDBv2.0_SC_G_NR100/OMDBv2.0_SC_G_NR100.cluster.tsv.gz
```

## Automation Decision

A source-specific downloader is not needed for this repository yet because the official backend already provides:

- one compact genome-level URL manifest
- direct HTTPS links for per-genome files
- predictable catalog directory paths
- MD5 sidecars for large catalog and archive files

If a helper is added later, it should only parse `OMDBv2.0_data.tsv.gz`, filter by genome/sample/study ID, and emit URL manifests by default. It should not download the 1.5 TB archive or the 100 GB-scale catalogs unless explicitly requested.

## Verification

Checked on 2026-05-09.

During curation:

- The OMDB About page reported v2.0, 274,282 reconstructed genomes, 32,022 species-level units, 348 projects, 12,260 geo-referenced samples, and CC BY 4.0 terms.
- The official download documentation reported `OMDBv2.0_data.tsv.gz` as the command-line entry point and listed MD5 `c1b5f14c9b7899f7300ccf41e62f8681`.
- Streaming `OMDBv2.0_data.tsv.gz` returned columns `GENOME`, `SAMPLE`, `STUDY`, `GENOME_FILE`, `GENES_NT_FILE`, `GENES_AA_FILE`, `GENES_GFF_FILE`, and `ANTISMASH_FILE`.
- The links TSV contained 274,283 lines including the header.
- The genome backend listed `OMDv2.genomes.db.tar.gz` as a 1.5 TB archive and its MD5 sidecar returned `2f254920c9cb72c683d3faf1283ea01a`.
