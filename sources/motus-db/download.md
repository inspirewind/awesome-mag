# mOTUs DB Download Notes

mOTUs DB has two different access paths:

- direct HTTP file downloads for full-database assets and metadata
- `motus-tool` for query-driven genome discovery and smaller targeted sequence downloads

Prefer the direct URLs when the goal is to obtain complete release-level files. Prefer `motus-tool` when the goal is to search by mOTU, taxonomy, function, or a list of genome identifiers.

## Full-Database Downloads

The public mOTUs 4.0 data root is:

- `https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/`

The most important full-database files are:

| Asset | URL | Notes |
| --- | --- | --- |
| All genome FASTA files | `https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/mOTUs4.genomes.tar` | Approximately 2.7 TB; use resumable download tooling. |
| Genome file manifest | `https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/genomes/genome_files` | Plain text relative paths for the per-genome `.fa.gz` files. |
| Genome metadata | `https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/mOTUs4.0_genome-metadata-20250702.alpha.tsv.gz` | Includes genome ID, quality metrics, GTDB taxonomy, mOTU, sample/study, environment, path, representative status. |
| Per-genome directory tree | `https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/genomes/` | Study/sample/genome directory hierarchy used by `PATH` fields. |
| Marker-gene DB | `https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/mOTUS-MGDB/current/db_mOTU.tar.gz` | mOTUs profiler reference DB; approximately 5.2 GB on the file host. |
| Marker-gene DB md5 | `https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/mOTUS-MGDB/current/db_mOTU.tar.gz.md5` | Sidecar checksum for the file-host copy. |

Recommended commands:

```bash
# All genome FASTA files, approximately 2.7 TB.
wget -c https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/mOTUs4.genomes.tar

# Full genome metadata.
wget -c https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/mOTUs4.0_genome-metadata-20250702.alpha.tsv.gz

# Per-genome file path manifest.
wget -c https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/genomes/genome_files

# Marker-gene database from the public file host.
wget -c https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/mOTUS-MGDB/current/db_mOTU.tar.gz
wget -c https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/mOTUS-MGDB/current/db_mOTU.tar.gz.md5
```

## Reconstructing Per-Genome URLs

The `mOTUs4.0_genome-metadata-20250702.alpha.tsv.gz` file contains a `PATH` column. A single genome sequence URL is:

```text
https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/genomes/<PATH>
```

Example:

```text
https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/genomes/ACIN21-1/ACIN21-1_SAMN05421555_METAG/ACIN21-1_SAMN05421555_MAG_00000001/ACIN21-1_SAMN05421555_MAG_00000001.fa.gz
```

This is useful when you already have genome identifiers or have filtered the full metadata locally.

## Supplementary Tables

Supplementary tables are available both from Zenodo and the public file host:

- Zenodo landing page: `https://zenodo.org/records/13325008`
- File-host directory: `https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/Supplementary_Tables/`

Files:

| File | Content |
| --- | --- |
| `Supplementary_Table_1.tsv.gz` | Genome to study/sample map for all genomes. |
| `Supplementary_Table_2.tsv.gz` | Non-MAG genome to source link map. |
| `Supplementary_Table_3.tsv.gz` | Metagenomic study overview with bioprojects, sample counts, MAG counts, and publications. |
| `Supplementary_Table_4.tsv.gz` | Sample to biosample/study/environment/source-link map. |
| `Supplementary_Table_5.tsv.gz` | Environment terms mapped to NCBI taxonomy IDs where available. |

Download example:

```bash
wget -c https://sunagawalab.ethz.ch/share/MOTUS/database/4.0/data/Supplementary_Tables/Supplementary_Table_1.tsv.gz
```

## motus-tool Downloads

Use `motus-tool` for smaller, targeted retrieval, especially when the selection is defined by:

- mOTU identifier
- genome identifier
- GTDB taxonomy or clade name
- KEGG, PFAM, or eggNOG functional annotation
- representative genomes only

Current installation pattern:

```bash
conda create -n mOTUs4 python=3.12 bwa=0.7.19 vsearch pip
conda activate mOTUs4
python -m pip install motus-tool
```

Download the marker-gene DB used by the tool:

```bash
motus downloadMGDB
```

Current `motus-tool` downloads the marker-gene DB from Zenodo:

```text
https://zenodo.org/records/17668622/files/db_mOTU.tar.gz?download=1
```

The `motus genomes` command also needs the annotation DB on first use. The current tool downloads:

```text
https://zenodo.org/records/17669279/files/mOTUsv4.0.annotation.db?download=1
```

This file is large, approximately 17.7 GB.

Query genome IDs by taxonomy or function:

```bash
# By mOTU ID.
motus genomes -i mOTUv4.0_001734 -o genomes_gilliamella_apis.tsv

# By exact taxonomy string.
motus genomes -i "Gilliamella apis" -o genomes_gilliamella_apis.tsv

# By KEGG identifiers, with taxonomy added to the output.
motus genomes -i K21722 K21723 K21724 -o genomes_caffeine_degradation.tsv -d TAXONOMY
```

Download the selected genome sequences:

```bash
motus download -i genomes_gilliamella_apis.tsv -o genome_sequences/
```

Download only representative genomes:

```bash
motus download -i genomes_gilliamella_apis.tsv -o genome_sequences/ -r
```

## Browser Downloads

The website is useful for browsing and for exporting metadata tables. Interactive genome sequence downloads are capped at 200 selected genomes. For larger genome-sequence batches, use one of:

- the full `mOTUs4.genomes.tar` archive
- direct URLs reconstructed from metadata `PATH`
- `motus genomes` plus `motus download`

## Version Notes

The user-facing download page inspected here is the v4.0.0a page and shows older commands such as:

```bash
python motus.py download -w Angelakisella -s Angelakisella.genomes -o Angelakisella_genomes_folder/
```

The current packaged tool uses:

```bash
motus genomes ...
motus download ...
motus downloadMGDB
```

Current mOTUs documentation also mentions v4.1 data, but the checked `database/4.1/data/genomes/` file-host path returned `401 Unauthorized`. This source entry therefore records the public v4.0 data root as the reproducible bulk-access endpoint.
