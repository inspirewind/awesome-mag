# RGMGC Download Notes

RGMGC data are split across the project website, NCBI, Figshare, and Springer:

- Website: `https://rummeta.njau.edu.cn/`
- RGMGC browse page: `https://rummeta.njau.edu.cn/rumment/browse/browsePage`
- Website download page: `https://rummeta.njau.edu.cn/rumment/resource/metagenomicsPage`
- Raw reads: NCBI BioProject `PRJNA657455`
- MAG assemblies: NCBI BioProject `PRJNA657473`
- MAG/USG protein and ORF sequence bundles: Figshare DOI `10.6084/m9.figshare.14176574`

## Website Gene Catalogs

The official website exposes direct download endpoints with this pattern:

```text
https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=<file_name>
```

Core integrated catalog files:

| Asset | URL | Observed size |
| --- | --- | ---: |
| RGMGC nucleotide gene catalog | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=RGMGC.geneSet.ffn.gz` | 30,144,505,627 bytes |
| RGMGC amino-acid gene catalog | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=RGMGC.geneSet.faa.gz` | 21,133,596,825 bytes |

Taxonomic subsets:

| Group | Nucleotide FASTA | Amino-acid FASTA |
| --- | --- | --- |
| Bovinae | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Bovinae.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Bovinae.geneSet.faa.gz` |
| Caprinae | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Caprinae.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Caprinae.geneSet.faa.gz` |
| Cervidae | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Cervidae.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Cervidae.geneSet.faa.gz` |

Species subsets:

| Species | Nucleotide FASTA | Amino-acid FASTA |
| --- | --- | --- |
| Dairy cattle | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Dairy_cattle.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Dairy_cattle.geneSet.faa.gz` |
| Water buffalo | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Water_buffalos.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Water_buffalos.geneSet.faa.gz` |
| Yak | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Yak.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Yak.geneSet.faa.gz` |
| Goat | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Goat.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Goat.geneSet.faa.gz` |
| Sheep | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Sheep.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Sheep.geneSet.faa.gz` |
| Roe deer | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Roe_deer.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Roe_deer.geneSet.faa.gz` |
| Water deer | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Water_deer.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Water_deer.geneSet.faa.gz` |

GIT-region subsets:

| Region | Nucleotide FASTA | Amino-acid FASTA |
| --- | --- | --- |
| Rumen | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Rumen.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Rumen.geneSet.faa.gz` |
| Reticulum | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Reticulum.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Reticulum.geneSet.faa.gz` |
| Omasum | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Omasum.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Omasum.geneSet.faa.gz` |
| Abomasum | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Abomasum.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Abomasum.geneSet.faa.gz` |
| Duodenum | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Duodenum.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Duodenum.geneSet.faa.gz` |
| Jejunum | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Jejunum.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Jejunum.geneSet.faa.gz` |
| Ileum | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Ileum.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Ileum.geneSet.faa.gz` |
| Cecum | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Cecum.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Cecum.geneSet.faa.gz` |
| Colon | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Colon.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Colon.geneSet.faa.gz` |
| Rectum | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Rectum.geneSet.ffn.gz` | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=Rectum.geneSet.faa.gz` |

Example:

```bash
curl -L -C - -o RGMGC.geneSet.ffn.gz \
  'https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=RGMGC.geneSet.ffn.gz'
```

## Website Profiles

| Asset | URL | Observed size |
| --- | --- | ---: |
| Gene abundance profile for 370 GIT samples | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=RGMGC.geneabundance.txt.gz` | 18,168,494,484 bytes |
| Phylum abundance profile | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=RGMGC.phylum.profile.xls.gz` | 268,769 bytes |
| Genus abundance profile | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=RGMGC.genus.profile.xls.gz` | not checked |
| KO abundance profile | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=RGMGC.KOs.profile.xls.gz` | not checked |
| COG abundance profile | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=RGMGC.COGs.profile.xls.gz` | not checked |
| CAZy family abundance profile | `https://rummeta.njau.edu.cn/rumment/download/downloadFile?file=RGMGC.cazy.profile.family.xls.gz` | not checked |

## Raw Reads

Raw metagenomic reads are under NCBI BioProject `PRJNA657455`.

Useful entry points:

| Asset | URL | Notes |
| --- | --- | --- |
| BioProject | `https://www.ncbi.nlm.nih.gov/bioproject/PRJNA657455` | Project page for the 370 GIT metagenomes. |
| SRA search | `https://www.ncbi.nlm.nih.gov/sra?term=PRJNA657455` | Browser search for related SRA records. |
| Runinfo CSV | `https://trace.ncbi.nlm.nih.gov/Traces/sra-db-be/runinfo?acc=PRJNA657455` | NCBI run manifest; ESearch reported 370 SRA records on 2026-05-11. |

Fetch the SRA run manifest:

```bash
curl -L -o rgmgc_PRJNA657455_runinfo.csv \
  'https://trace.ncbi.nlm.nih.gov/Traces/sra-db-be/runinfo?acc=PRJNA657455'
```

Then use SRA Toolkit on selected runs:

```bash
prefetch SRR12529399
fasterq-dump --split-files --threads 8 SRR12529399
```

## MAG Assemblies

MAG assemblies are under NCBI BioProject `PRJNA657473`.

Useful entry points:

| Asset | URL | Notes |
| --- | --- | --- |
| BioProject | `https://www.ncbi.nlm.nih.gov/bioproject/PRJNA657473` | Project page for MAG assemblies. |
| Assembly search | `https://www.ncbi.nlm.nih.gov/assembly/?term=PRJNA657473` | Browser search for related assemblies. |
| ESearch count | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=assembly&term=PRJNA657473%5BBioProject%5D&retmode=json` | Returned 10,373 assembly records on 2026-05-11. |
| Example assembly | `https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_017965065.1/` | Example assembly page observed during curation. |

With NCBI EDirect and Datasets CLI installed, export assembly accessions and download genome FASTA packages:

```bash
esearch -db assembly -query 'PRJNA657473[BioProject]' \
  | efetch -format docsum \
  | xtract -pattern DocumentSummary -element AssemblyAccession \
  > rgmgc_PRJNA657473_assemblies.txt

datasets download genome accession \
  --inputfile rgmgc_PRJNA657473_assemblies.txt \
  --include genome \
  --filename rgmgc_PRJNA657473_genomes.zip
```

The corpus workflow uses a dependency-light E-utilities helper instead of requiring
EDirect or NCBI Datasets CLI:

```bash
bash corpus/download_bash/part4_hard_datasets/rgmgc.sh --manifest-only
bash corpus/download_bash/part4_hard_datasets/rgmgc.sh --downloader aria2c --jobs 8 --connections 2
```

The helper enumerates `PRJNA657473[BioProject]` with ESearch, resolves each
Assembly document summary FTP path with ESummary, constructs the corresponding
`*_genomic.fna.gz` URL, and writes the audit table
`downloads/rgmgc/ncbi_assemblies_manifest.tsv`.

## Figshare Protein and ORF Bundles

The article data availability section points to Figshare DOI:

```text
https://doi.org/10.6084/m9.figshare.14176574
```

Figshare landing page:

```text
https://figshare.com/articles/dataset/An_integrated_gene_catalog_and_over_10_000_metagenome-assembled_genomes_from_the_gastrointestinal_microbiome_of_ruminants/14176574
```

The article describes these as protein and ORF sequences for all MAGs and unidentified species genomes. During curation, the Figshare web page was reachable, but direct Figshare API access from `curl` returned HTTP 403, so browser download is the practical route.

## Springer Article and Supplementary Files

Article and DOI:

- `https://link.springer.com/article/10.1186/s40168-021-01078-x`
- `https://doi.org/10.1186/s40168-021-01078-x`

The article page hosts supplementary files for figures, sample metadata, gene catalog summaries, MAG/USG statistics, annotation tables, CAZyme/PUL analyses, BGC summaries, and methane/feed-efficiency association tables. Use the article landing page as the stable reference rather than hard-coding every Springer `MOESM` URL unless a workflow needs a specific table.

## Automation Decision

A source-specific script is now provided for the MAG sequence payload:

- `corpus/download_bash/part4_hard_datasets/rgmgc.sh`
- `scripts/rgmgc/download.py`

The reproducible parts have stable public routes:

- RGMGC website direct `downloadFile?file=` endpoints for gene catalogs and profiles
- NCBI SRA runinfo CSV for raw reads
- NCBI Assembly/BioProject records for the 10,373 MAG assemblies, used by the corpus downloader
- Figshare DOI landing page for MAG/USG protein and ORF sequence bundles

Do not add automation to work around Figshare API or browser restrictions for the protein/ORF bundles. They are not the genome FASTA payload needed for MAG-level RabbitTClust clustering.

## Verification

Checked on 2026-05-11:

- RGMGC homepage, browse page, metagenomics page, and browse JSON endpoint loaded.
- RGMGC metagenomics page exposed direct links for integrated, taxonomic, species, regional, and profile downloads.
- RGMGC direct download HEAD checks returned `200 OK` for `RGMGC.geneSet.ffn.gz`, `RGMGC.geneSet.faa.gz`, `RGMGC.geneabundance.txt.gz`, and `RGMGC.phylum.profile.xls.gz`.
- RGMGC genomes page loaded but did not list genome links.
- NCBI ESearch reported 370 SRA records for `PRJNA657455`.
- NCBI ESearch reported 10,373 assembly records for `PRJNA657473`.
- NCBI example assembly `GCA_017965065.1` loaded in the Datasets genome page.
- Crossref DOI metadata confirmed Microbiome volume 9, article 137, published online 2021-06-12, with a 2022 correction DOI.

Checked on 2026-05-18:

- NCBI Assembly ESearch for `PRJNA657473[BioProject]` returned 10,373 records.
- `scripts/rgmgc/download.py --manifest-only` successfully resolved 10,373 GenBank FTP paths into `*_genomic.fna.gz` URLs.
