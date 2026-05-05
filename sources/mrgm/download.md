# MRGM Download Notes

MRGM data on the decodebiome site are publicly accessible via direct HTTPS with no authentication. Downloads are served through a PHP-based file browser; direct directory URLs under `data/` return 403, but direct file URLs work.

- Homepage: `https://www.decodebiome.org/MRGM/`
- Navigate page: `https://www.decodebiome.org/MRGM/navigate.html`
- File browser: `https://www.decodebiome.org/MRGM/listdir.php?directory=data`
- Genome catalog browser: `https://www.decodebiome.org/MRGM/listdir.php?directory=data/genome_catalog`
- Protein catalog browser: `https://www.decodebiome.org/MRGM/listdir.php?directory=data/protein_catalog`
- MRGM species browser: `https://www.decodebiome.org/MRGM/MRGM-Genomes.html`

No source-specific automation script is needed. The stable direct URLs and `listdir.php` pages are enough for `curl`, `wget`, or `aria2c` workflows.

## Genome Catalog

Base path: `https://www.decodebiome.org/MRGM/data/genome_catalog/`

| Asset | URL | Size |
| --- | --- | --- |
| Genome catalog README | `README.txt` | 332 B |
| Representative genome metadata | `MRGM_representative_genomes/MRGM_final_metadata.tsv` | 1 MB |
| Representative genome directory | `MRGM_representative_genomes/MRGM_Genomes-Sequences/` | 1,524 `.fna` files |
| All NC genomes metadata | `All_55893_genomes/Genomes_final_metadata.tsv` | 17 MB |
| All NC genomes archive | `All_55893_genomes/genome.tar.gz` | 43 GB |
| All NC genomes directory | `All_55893_genomes/Genomes/` | 55,893 `.fna.gz` files |
| Non-redundant NC genomes metadata | `Nonredundant_42245_genomes/Genomes_nonredundant_metadata.tsv` | 12 MB |
| Non-redundant NC genomes directory | `Nonredundant_42245_genomes/Genomes/` | 42,245 `.fna.gz` files |

Download the all-genomes archive:

```bash
curl -L -C - -o MRGM_all_55893_genomes.tar.gz \
  'https://www.decodebiome.org/MRGM/data/genome_catalog/All_55893_genomes/genome.tar.gz'
```

Download representative and non-redundant metadata:

```bash
curl -L -C - -o MRGM_final_metadata.tsv \
  'https://www.decodebiome.org/MRGM/data/genome_catalog/MRGM_representative_genomes/MRGM_final_metadata.tsv'

curl -L -C - -o Genomes_nonredundant_metadata.tsv \
  'https://www.decodebiome.org/MRGM/data/genome_catalog/Nonredundant_42245_genomes/Genomes_nonredundant_metadata.tsv'
```

Example representative genome download:

```bash
curl -L -C - -o MRGM_0001.fna \
  'https://www.decodebiome.org/MRGM/data/genome_catalog/MRGM_representative_genomes/MRGM_Genomes-Sequences/MRGM_0001.fna'
```

Example non-redundant genome download:

```bash
curl -L -C - -o GENOME00001.fna.gz \
  'https://www.decodebiome.org/MRGM/data/genome_catalog/Nonredundant_42245_genomes/Genomes/GENOME00001.fna.gz'
```

The non-redundant directory README mentions `genome.tar.gz`, but `https://www.decodebiome.org/MRGM/data/genome_catalog/Nonredundant_42245_genomes/genome.tar.gz` returned 404 when checked on 2026-05-06. Use the per-genome directory unless the site adds the archive later.

## 16S Sequences

Base path: `https://www.decodebiome.org/MRGM/data/genome_catalog/16S_sequence/`

| Asset | URL | Size |
| --- | --- | --- |
| 16S metadata | `16S_sequence_metadata.tsv` | 21 MB |
| README | `README.txt` | 364 B |

The article reports 16,020 predicted 16S rRNA sequences for 940 of 1,524 MRGM species. The metadata columns include MRGM name, direct/GTDB prediction source, barrnap version, rRNA type, sequence length, e-value, description, sequence, and taxonomy.

## Taxonomy Profiling Databases

Base path: `https://www.decodebiome.org/MRGM/data/genome_catalog/MRGM_custom_db/`

| Asset | URL | Size |
| --- | --- | --- |
| Kraken2 `database.kraken` | `MRGM_kraken2_customdb/database.kraken` | 16 GB |
| Kraken2 `hash.k2d` | `MRGM_kraken2_customdb/hash.k2d` | 9 GB |
| Kraken2 `taxo.k2d` | `MRGM_kraken2_customdb/taxo.k2d` | 174 KB |
| Kraken2 `names.dmp` | `MRGM_kraken2_customdb/taxonomy/names.dmp` | 121 KB |
| Kraken2 `nodes.dmp` | `MRGM_kraken2_customdb/taxonomy/nodes.dmp` | 53 KB |
| MetaPhlAn4 DB files | `MRGM_metaphlan_customdb/` | multi-file Bowtie2 + pkl database |

The Kraken2 directory also includes `database80mers`, `database90mers`, `database100mers`, and `database150mers` k-mer distribution and kraken files. The MetaPhlAn directory includes `MRGM_20221205.1.bt2l` through `.4.bt2l`, reverse index files, and `MRGM_20221205.pkl`.

Example Kraken2 file download:

```bash
curl -L -C - -o hash.k2d \
  'https://www.decodebiome.org/MRGM/data/genome_catalog/MRGM_custom_db/MRGM_kraken2_customdb/hash.k2d'
```

## Protein Catalog

Base path: `https://www.decodebiome.org/MRGM/data/protein_catalog/`

| Cluster | FASTA | Cluster info | Taxonomic map | Annotation files |
| --- | --- | --- | --- | --- |
| linclust-100 | `MRGM_linclust-100.Proteins.faa` (4 GB) | `MRGM_linclust-100.cluster_info.tsv` (2 GB) | `MRGM_linclust-100.taxonomic-map.tsv` (783 MB) | None listed |
| linclust-90 | `MRGM_linclust-90.Proteins.faa` (1 GB) | `MRGM_linclust-90.cluster_info.tsv` (2 GB) | `MRGM_linclust-90.taxonomic-map.tsv` (281 MB) | DeepGOPlus 1 GB; eggNOG-mapper 1 GB |
| linclust-80 | `MRGM_linclust-80.Proteins.faa` (949 MB) | `MRGM_linclust-80.cluster_info.tsv` (2 GB) | `MRGM_linclust-80.taxonomic-map.tsv` (213 MB) | None listed |
| linclust-50 | `MRGM_linclust-50.Proteins.faa` (409 MB) | `MRGM_linclust-50.cluster_info.tsv` (2 GB) | `MRGM_linclust-50.taxonomic-map.tsv` (122 MB) | None listed |

Example protein catalog download:

```bash
curl -L -C - -o MRGM_linclust-90.Proteins.faa \
  'https://www.decodebiome.org/MRGM/data/protein_catalog/MRGM_linclust-90.Proteins.faa'
```

## NCBI Accessions

| Resource | Accession | URL |
| --- | --- | --- |
| Raw metagenomic sequencing data | SRP335854 | https://trace.ncbi.nlm.nih.gov/Traces/sra/?study=SRP335854 |

## Automation Decision

No download script is needed. All listed files are accessible via direct HTTPS URLs with no authentication, cookies, or JavaScript requirements. For large files, use resumable downloads (`curl -C -`, `wget -c`, or `aria2c -c`).

## Caveats

- The site does not publish checksum files; verify large archive integrity with tools such as `tar -tzf` after download.
- Direct directory URLs such as `https://www.decodebiome.org/MRGM/data/protein_catalog/` return 403; use `listdir.php?directory=data/protein_catalog`.
- The all-genomes archive is 43 GB. The non-redundant genome archive mentioned by the README was not available when checked.
- The MRGM page and file-browser HTML reuse some HRGM2 titles and navigation labels; use the MRGM URL path and file names rather than page titles for curation.

Checked on 2026-05-06.
