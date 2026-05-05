# HROM Download Notes

HROM data on the decodebiome site are publicly accessible via direct HTTPS with no authentication. Downloads are served through a PHP-based file browser; direct directory URLs under `data/` return 403, but direct file URLs work.

- Homepage: `https://www.decodebiome.org/HROM/`
- Navigate page: `https://www.decodebiome.org/HROM/navigate.html`
- File browser: `https://www.decodebiome.org/HROM/listdir.php?directory=data`
- Genome catalog browser: `https://www.decodebiome.org/HROM/listdir.php?directory=data/genome_catalog`
- Protein catalog browser: `https://www.decodebiome.org/HROM/listdir.php?directory=data/protein_catalog`
- HROM species browser: `https://www.decodebiome.org/HROM/HROM-Genomes.html`

No source-specific automation script is needed. The stable direct URLs and `listdir.php` pages are enough for `curl`, `wget`, or `aria2c` workflows.

## Genome Catalog

Base path: `https://www.decodebiome.org/HROM/data/genome_catalog/`

| Asset | URL | Size |
| --- | --- | --- |
| Non-redundant genomes archive | `HROM_nonredundant_genomes.tar.gz` | 76.1 GB |
| Decontamination archive | `decontamination_HROM.tar.gz` | 12.6 GB |
| Species metadata | `HROM-Species-metadata.tsv` | 1.8 MB |
| Conspecific genomes metadata | `HROM_Conspecific-genomes-metadata.tsv` | 22.7 MB |
| README | `README.txt` | 973 B |

Download the full non-redundant genome archive:

```bash
curl -L -C - -o HROM_nonredundant_genomes.tar.gz \
  'https://www.decodebiome.org/HROM/data/genome_catalog/HROM_nonredundant_genomes.tar.gz'
```

Download metadata:

```bash
curl -L -C - -o HROM-Species-metadata.tsv \
  'https://www.decodebiome.org/HROM/data/genome_catalog/HROM-Species-metadata.tsv'

curl -L -C - -o HROM_Conspecific-genomes-metadata.tsv \
  'https://www.decodebiome.org/HROM/data/genome_catalog/HROM_Conspecific-genomes-metadata.tsv'
```

## Representative And Non-Redundant Genomes

Representative genomes are nested by genome-name prefixes. The web table uses this pattern:

```text
HROM_representative_genomes/HROM_Genome_0XXX/HROM_Genome_00XX/HROM_Genome_0001.fna
```

Example representative genome download:

```bash
curl -L -C - -o HROM_Genome_0001.fna \
  'https://www.decodebiome.org/HROM/data/genome_catalog/HROM_representative_genomes/HROM_Genome_0XXX/HROM_Genome_00XX/HROM_Genome_0001.fna'
```

Individual non-redundant genomes are grouped by HROM species directory:

```text
HROM_nonredundant_genomes/HROM_Genome_0023/HROM_Genome_0023_1.fna
```

Example conspecific genome download:

```bash
curl -L -C - -o HROM_Genome_0023_1.fna \
  'https://www.decodebiome.org/HROM/data/genome_catalog/HROM_nonredundant_genomes/HROM_Genome_0023/HROM_Genome_0023_1.fna'
```

## Species Pangenomes

Base browser: `https://www.decodebiome.org/HROM/listdir.php?directory=data/genome_catalog/HROM_species_pangenome`

Each species directory can contain:

| File | Example URL | Notes |
| --- | --- | --- |
| `gene_presence_absence.Rtab` | `HROM_species_pangenome/HROM_Genome_0002/gene_presence_absence.Rtab` | Gene presence/absence matrix |
| `pan_genome_reference.eggnog.annotation` | `HROM_species_pangenome/HROM_Genome_0002/pan_genome_reference.eggnog.annotation` | eggNOG annotation |
| `pan_genome_reference.fa` | `HROM_species_pangenome/HROM_Genome_0002/pan_genome_reference.fa` | Pangenome reference sequence |

## Taxonomy Profiling Databases

Base path: `https://www.decodebiome.org/HROM/data/genome_catalog/`

| Asset | URL | Size |
| --- | --- | --- |
| Kraken2 `database.kraken` | `HROM_kraken2_customdb/database.kraken` | 32.4 GB |
| Kraken2 `hash.k2d` | `HROM_kraken2_customdb/hash.k2d` | 11.6 GB |
| Kraken2 `seqid2taxid.map` | `HROM_kraken2_customdb/seqid2taxid.map` | 287.4 MB |
| MetaPhlAn4 DB files | `HROM_metaphlan_customdb/` | multi-file Bowtie2 + pkl database |
| 16S rRNA library | `HROM_16s_rRNA_sequences/16S_rRNA_library.fasta` | 15.5 MB |

The MetaPhlAn4 custom database includes `HROM_20221218.1.bt2l`, `HROM_20221218.2.bt2l`, `HROM_20221218.3.bt2l`, `HROM_20221218.4.bt2l`, reverse index files, and `HROM_20221218.pkl`.

## Protein Catalog

Base path: `https://www.decodebiome.org/HROM/data/protein_catalog/`

| Cluster | FASTA | Cluster info | Annotation files |
| --- | --- | --- | --- |
| HROP-100 | `HROP-100.faa` (28.0 GB) | `HROP-100_cluster_info.tsv` (12.3 GB) | `HROP-100_eggnog.mapper.tsv` (23.3 GB) |
| HROP-95 | `HROP-95.faa` (5.0 GB) | `HROP-95_cluster_info.tsv` (6.9 GB) | DeepGOPlus 5.0 GB; eggNOG 3.8 GB |
| HROP-90 | `HROP-90.faa` (2.8 GB) | `HROP-90_cluster_info.tsv` (6.4 GB) | DeepGOPlus 2.6 GB; eggNOG 2.0 GB |
| HROP-70 | `HROP-70.faa` (720.6 MB) | `HROP-70_cluster_info.tsv` (5.9 GB) | DeepGOPlus 645.2 MB; eggNOG 486.4 MB |
| HROP-50 | `HROP-50.faa` (521.8 MB) | `HROP-50_cluster_info.tsv` (5.8 GB) | DeepGOPlus 413.1 MB; eggNOG 300.1 MB |

Example protein catalog download:

```bash
curl -L -C - -o HROP-50.faa \
  'https://www.decodebiome.org/HROM/data/protein_catalog/HROP-50.faa'
```

## Caveats

- The site does not publish checksums; verify large archive integrity with tools such as `tar -tzf` after download.
- The largest genome and protein files are tens of GB; use resumable downloads.
- Direct directory URLs such as `https://www.decodebiome.org/HROM/data/protein_catalog/` return 403; use `listdir.php?directory=data/protein_catalog`.
- The HROM homepage citation text is stale as of 2026-05-05; the article is available at `https://doi.org/10.1016/j.chom.2025.10.013`.

Checked on 2026-05-05.
