# HRGM Download Notes

HRGM data on the decodebiome site is publicly accessible via direct HTTPS with no authentication. Downloads are served through a PHP-based file browser. HRGM2 also has an official GitHub code/data-description repository and Zenodo mirrors for the released datasets.

- Homepage: `https://www.decodebiome.org/HRGM/`
- File browser: `https://www.decodebiome.org/HRGM/listdir.php?directory=data`
- Metadata TSV: `https://www.decodebiome.org/HRGM/static/HRGMv2_metadata_for_web.tsv`
- HRGM1 legacy: `https://www.decodebiome.org/HRGM1/`
- HRGM2 code/data repository: `https://github.com/netbiolab/HRGM2`
- HRGM2 data DOI overview: `https://github.com/netbiolab/HRGM2/blob/main/DATA.md`

The HRGM2 Zenodo data records use CC0. The 2021 HRGM1 Genome Medicine publication is open access under CC BY 4.0.

## HRGM2 Bulk Genome Archives

Base path: `https://www.decodebiome.org/HRGM/data/genome_catalog/`

| Asset | URL | Size |
| --- | --- | --- |
| Representative genomes | `HRGMv2_Genomes/HRGMv2_Rep_Genome.tar.gz` | 3.5 GB |
| Pangenomes | `HRGMv2_Genomes/HRGMv2_Pangenomes.tar.gz` | 395 GB |
| Nonredundant genomes (all) | `Total_Genomes/Nonredundant_genomes.tar.gz` | 114 GB |
| Redundant genomes (all) | `Total_Genomes/Redundant_genomes.tar.gz` | 179 GB |
| GEMs | `GEMs/GEMs.tar.gz` | 34 GB |
| Defense systems | (see protein catalog below) | 377 MB |

### Index Files

The site provides TSV files mapping individual genome names to download URLs. These are essential for selective downloads:

| Index file | URL | Size |
| --- | --- | --- |
| Pangenome index | `HRGMv2_Genomes/Pangenome_download_link_info.tsv` | 537 KB |
| Total genomes index | `Total_Genomes/download_link_info.tsv` | 36 MB |
| GEM index | `GEMs/GEM_download_link_info.tsv` | 22 MB |
| CAZyme index | `download_link_info_cazyme.tsv` (under `data/protein_catalog/`) | 20 MB |

Download an index and extract specific genome URLs:

```bash
# Get the total genomes index
curl -L -o download_link_info.tsv \
  'https://www.decodebiome.org/HRGM/data/genome_catalog/Total_Genomes/download_link_info.tsv'

# Filter for specific genomes (column format depends on TSV structure)
awk -F'\t' '$1 ~ /HRGMv2_2040/ {print $NF}' download_link_info.tsv > subset.urls
wget -i subset.urls
```

### Metadata Files

Available at the genome catalog root:

| File | URL |
| --- | --- |
| Dereplication metadata | `Dereplication_genomes_metadata.tsv` |
| Cluster metadata | `HRGMv2_Cluster_metadata.tsv` |
| GTDB r220 results | `HRGMv2_gtdbr220_results.tsv` |
| README | `README.txt` |

### Example Bulk Downloads

Download representative genomes (smallest meaningful archive):

```bash
curl -L -C - -o HRGMv2_Rep_Genome.tar.gz \
  'https://www.decodebiome.org/HRGM/data/genome_catalog/HRGMv2_Genomes/HRGMv2_Rep_Genome.tar.gz'
```

Download the full nonredundant genome set with aria2c (resumable, multi-connection):

```bash
aria2c -c -x 4 -s 4 -d downloads/ \
  'https://www.decodebiome.org/HRGM/data/genome_catalog/Total_Genomes/Nonredundant_genomes.tar.gz'
```

Download metadata files:

```bash
curl -L -C - -o Dereplication_genomes_metadata.tsv \
  'https://www.decodebiome.org/HRGM/data/genome_catalog/Dereplication_genomes_metadata.tsv'

curl -L -C - -o HRGMv2_Cluster_metadata.tsv \
  'https://www.decodebiome.org/HRGM/data/genome_catalog/HRGMv2_Cluster_metadata.tsv'

curl -L -C - -o HRGMv2_gtdbr220_results.tsv \
  'https://www.decodebiome.org/HRGM/data/genome_catalog/HRGMv2_gtdbr220_results.tsv'
```

## Taxonomy Profiling Databases

Base path: `https://www.decodebiome.org/HRGM/data/genome_catalog/Taxonomy_Profiling/`

| Asset | URL | Size |
| --- | --- | --- |
| Kraken2 DB (representative) | `HRGMv2_kraken2_customdb/HRGMv2_Rep/` | multi-file directory; largest files include `hash.k2d` (16 GB) and `database.kraken` (2 GB) |
| Kraken2 DB (concatenated) | `HRGMv2_kraken2_customdb/HRGMv2_Concat/` | multi-file directory; largest files include `database.kraken` (82 GB) and `hash.k2d` (34 GB) |
| MetaPhlAn4 DB | `HRGMv2_metaphlan_customdb/HRGMv2_MetaPhlAn4_DB/` | ~2.2 GB |
| 16S rRNA library | `16S_rRNA/16S_rRNA_library.fasta` | 5 MB |

Browse each directory via `listdir.php` for individual file names.

## Protein Catalog

Base path: `https://www.decodebiome.org/HRGM/data/protein_catalog/`

Note: direct directory access returns 403; use `listdir.php?directory=data/protein_catalog` to browse.

| Directory | Content |
| --- | --- |
| `0.HRGMv2_Proteins/0.redundant_CDS` | All predicted CDS |
| `0.HRGMv2_Proteins/1.HRGMv2_Unique_Proteins` | Unique protein sequences |
| `0.HRGMv2_Proteins/2.HRGMv2_100_Proteins` | CD-HIT at 100% identity |
| `0.HRGMv2_Proteins/3.HRGMv2_95_Proteins` | CD-HIT at 95% identity |
| `0.HRGMv2_Proteins/4.HRGMv2_90_Proteins` | CD-HIT at 90% identity |
| `0.HRGMv2_Proteins/5.HRGMv2_70_Proteins` | CD-HIT at 70% identity |
| `0.HRGMv2_Proteins/6.HRGMv2_50_Proteins` | CD-HIT at 50% identity |
| `1.HRGMv2_Pangenomes/` | Pangenome eggNOG/RGI annotations |
| `2.HRGMv2_CAZymes/` | CAZyme annotations (dbCAN3) |
| `3.HRGMv2_Defense_systems.tar.gz` | Defense system annotations |

Download defense systems:

```bash
curl -L -C - -o HRGMv2_Defense_systems.tar.gz \
  'https://www.decodebiome.org/HRGM/data/protein_catalog/3.HRGMv2_Defense_systems.tar.gz'
```

## GEMs (Genome-Scale Metabolic Models)

Base path: `https://www.decodebiome.org/HRGM/data/genome_catalog/GEMs/`

| Asset | URL | Size |
| --- | --- | --- |
| GEM archive | `GEMs.tar.gz` | 34 GB |
| GEM index | `GEM_download_link_info.tsv` | 22 MB |

## HRGM1 Legacy Data

Base path: `https://www.decodebiome.org/HRGM1/data/genome_catalog/`

| Asset | URL | Size |
| --- | --- | --- |
| Genome sequences | `HRGM_Genomes/HRGM_Genome-Sequences.tar.gz` | 3 GB |
| KIJ genomes (FASTA) | `KIJ_Genomes/genome_fna.tar.gz` | 21 GB |
| KIJ genomes (CDS) | `KIJ_Genomes/cds_faa_fna.tar.gz` | 30 GB |
| Kraken2 DB | `HRGM_Genomes/HRGM_kraken2_customdb.tar.gz` | 17 GB |

Additional HRGM1 subdirectories: `16S_rRNA/`, `SNV/`, `all_genome_non-redundant/`, `all_genome_redundant/`, `antismash/`, `epitope/`, `prokka/`, `rgi/`.

## NCBI Accessions

| Resource | Accession | URL |
| --- | --- | --- |
| HRGM2 BioProject | PRJNA1227720 | https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1227720 |
| HRGM2 BioProject | PRJNA1227423 | https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1227423 |
| HRGM2 BioProject | PRJNA1226738 | https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1226738 |
| HRGM1 SRA study (raw reads) | SRP292575 | https://www.ncbi.nlm.nih.gov/sra/SRP292575 |
| HRGM1 BioProject (genomes) | PRJNA678426 | https://www.ncbi.nlm.nih.gov/bioproject/PRJNA678426 |
| HRGM1 BioProject (assembled) | PRJNA730993 | https://www.ncbi.nlm.nih.gov/bioproject/PRJNA730993 |

## Third-Party Resources

- gapseq metabolic models for 5,414 HRGM genomes (Waschina et al.): https://zenodo.org/records/8283247 (11.1 GB, CC BY 4.0)

## Automation Decision

No download script is needed. All files are accessible via direct HTTPS URLs with no authentication, cookies, or JavaScript requirements. The `listdir.php` browser and `download_link_info.tsv` index files provide sufficient URL discovery for `wget`/`curl`/`aria2c` workflows.

## Caveats

- The decodebiome server does not publish checksum files; Zenodo records provide MD5 checksums for mirrored HRGM2 data. For direct site downloads, consider verifying completeness with `tar -tzf`.
- The largest archives (Pangenomes: 395 GB, Redundant: 179 GB) require significant disk space and bandwidth.
- Kraken2 databases are multi-file directories; the table above names the largest files rather than a compressed archive size.
- Individual genome FASTA files are nested 3-4 levels deep (e.g., `HRGMv2_2040XX/HRGMv2_20402X/HRGMv2_20402.fna`); use index TSV files instead of guessing paths.
- The old URL `www.mbiomenet.org/HRGM/` cited in the 2021 paper is unreachable (DNS failure).

Checked on 2026-05-05.
