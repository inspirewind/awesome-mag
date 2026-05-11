# GROWdb Download Notes

This resource is associated with the Nature article "A functional microbiome catalogue crowdsourced from North American rivers."

Primary links:

- Article: `https://www.nature.com/articles/s41586-024-08240-z`
- Data availability section: `https://www.nature.com/articles/s41586-024-08240-z#data-availability`
- NCBI BioProject: `https://www.ncbi.nlm.nih.gov/bioproject/PRJNA946291`
- Zenodo concept record: `https://zenodo.org/records/8173286`
- GROWdb Explorer: `https://geocentroid.shinyapps.io/GROWdatabase/`
- KBase collection: `https://narrative.kbase.us/collections/GROW`
- NMDC portal: `https://data.microbiomedata.org/`

## Download Strategy

Use two primary bulk routes:

- NCBI BioProject `PRJNA946291` for reads and MAG assemblies.
- Zenodo records for article-level companion files and the global freshwater MAG comparison archive.

The Zenodo concept DOI `10.5281/zenodo.8173286` has multiple versions. Do not rely only on the latest record:

- `8173287` contains the core GROWdb v1 files: annotations, gene FASTA, expression tables, ARG files, and tree files.
- `11193259` is the latest data record and contains the global freshwater comparison archive and inventory only.

## Zenodo Core GROWdb v1 Files

Zenodo record `10.5281/zenodo.8173287` is released under Creative Commons Attribution 4.0 and contains 11 public files totaling about 1.6 GB.

| File | Size | MD5 | URL |
| --- | ---: | --- | --- |
| `annotations.tsv.zip` | 306.5 MB | `c502de99d68664709a734e2a31f6ce95` | `https://zenodo.org/records/8173287/files/annotations.tsv.zip?download=1` |
| `genes.fna.zip` | 1.2 GB | `acae8ca209d07ae8b7e8134e5925bc66` | `https://zenodo.org/records/8173287/files/genes.fna.zip?download=1` |
| `metabolism_summary.xlsx` | 22.8 MB | `1f9035abeec68c130eaa51263af15f2e` | `https://zenodo.org/records/8173287/files/metabolism_summary.xlsx?download=1` |
| `GENES_geTMM_norm.counts.rpk_edger_zenodo.csv` | 12.3 MB | `402ad772b153a51f4652f1875bb49af1` | `https://zenodo.org/records/8173287/files/GENES_geTMM_norm.counts.rpk_edger_zenodo.csv?download=1` |
| `BINS_norm.counts.rpk_edger.mean_atLeast20_zenodo.csv` | 205.8 KB | `8bf115775c2f5789ed39cf05857eb892` | `https://zenodo.org/records/8173287/files/BINS_norm.counts.rpk_edger.mean_atLeast20_zenodo.csv?download=1` |
| `ARGS_genes_rgi.txt` | 357.2 KB | `d73cf4ef7f3cfa6c5043f9592b42f673` | `https://zenodo.org/records/8173287/files/ARGS_genes_rgi.txt?download=1` |
| `AMR_expression_by_sample.csv` | 2.8 KB | `2355ba5ed8012c0467303dbb1eccb3b2` | `https://zenodo.org/records/8173287/files/AMR_expression_by_sample.csv?download=1` |
| `GROW_pmoA_amoA_tree.pdf` | 257.6 KB | `a204697773015c7349dce2889d5475df` | `https://zenodo.org/records/8173287/files/GROW_pmoA_amoA_tree.pdf?download=1` |
| `GROW_nxr:nar_tree.pdf` | 525.5 KB | `8691ad0ec5a200bad3ae45f062887649` | `https://zenodo.org/records/8173287/files/GROW_nxr:nar_tree.pdf?download=1` |
| `bipartitionsBranchLabels.amoA_pmoA_seqs_for_tree_aligned.faa_mode_low.renamed` | 10.3 KB | `9d848e93428500582e9198f3a8294b1a` | `https://zenodo.org/records/8173287/files/bipartitionsBranchLabels.amoA_pmoA_seqs_for_tree_aligned.faa_mode_low.renamed?download=1` |
| `bipartitionsBranchLabels.nxr-nar_seqs_for_tree_aligned.faa_mode_low.renamed` | 17.1 KB | `7e7b3cb619608c9a59e0488100be678c` | `https://zenodo.org/records/8173287/files/bipartitionsBranchLabels.nxr-nar_seqs_for_tree_aligned.faa_mode_low.renamed?download=1` |

Example targeted downloads:

```bash
curl -L -C - -o annotations.tsv.zip 'https://zenodo.org/records/8173287/files/annotations.tsv.zip?download=1'
curl -L -C - -o genes.fna.zip 'https://zenodo.org/records/8173287/files/genes.fna.zip?download=1'
curl -L -C - -o metabolism_summary.xlsx 'https://zenodo.org/records/8173287/files/metabolism_summary.xlsx?download=1'
```

Verify checksums after download:

```bash
md5sum annotations.tsv.zip genes.fna.zip metabolism_summary.xlsx
```

## Zenodo Global Freshwater MAG Files

Zenodo latest record `10.5281/zenodo.11193259` adds the global freshwater comparison files described by the article and record metadata.

| File | Size | MD5 | URL |
| --- | ---: | --- | --- |
| `5986_99ID_drep_global.tar.gz` | 3.9 GB | `2ed31a0b87c4d9ee5c86ed5aa92abe83` | `https://zenodo.org/records/11193259/files/5986_99ID_drep_global.tar.gz?download=1` |
| `GlobalMAG_Inventory.xlsx` | 919.4 KB | `9a8fae1cd54f600ecb71ac5723b36a06` | `https://zenodo.org/records/11193259/files/GlobalMAG_Inventory.xlsx?download=1` |

Download with resume support:

```bash
curl -L -C - -o 5986_99ID_drep_global.tar.gz 'https://zenodo.org/records/11193259/files/5986_99ID_drep_global.tar.gz?download=1'
curl -L -C - -o GlobalMAG_Inventory.xlsx 'https://zenodo.org/records/11193259/files/GlobalMAG_Inventory.xlsx?download=1'
```

Inspect before extraction:

```bash
tar -tzf 5986_99ID_drep_global.tar.gz | head
```

## NCBI Archive

The article states that all reads and MAGs are hosted at NCBI under BioProject `PRJNA946291`.

Useful entry points:

| Asset | URL | Notes |
| --- | --- | --- |
| BioProject | `https://www.ncbi.nlm.nih.gov/bioproject/PRJNA946291` | Primary NCBI project record. |
| SRA search | `https://www.ncbi.nlm.nih.gov/sra?term=PRJNA946291` | Raw sequencing records associated with the project. |
| Assembly search | `https://www.ncbi.nlm.nih.gov/assembly/?term=PRJNA946291` | MAG and assembly records associated with the project. |
| BioProject summary API | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=bioproject&id=946291&retmode=json` | Machine-readable project metadata. |

During curation, NCBI E-utilities reported the BioProject title as "Genome Resolved Open Watersheds database (GROWdb) Metagenome" and the organism name as "freshwater metagenome."

Example metadata checks:

```bash
curl -L 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=bioproject&id=946291&retmode=json'
curl -L 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=sra&term=PRJNA946291&retmode=json&retmax=0'
curl -L 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=assembly&term=PRJNA946291&retmode=json&retmax=0'
```

For bulk read retrieval, use NCBI tools such as `datasets`, `sra-tools`, or generated accession lists from the SRA Run Selector rather than scraping interactive NCBI pages.

## Interactive Platforms

| Platform | URL | Notes |
| --- | --- | --- |
| NMDC Data Portal | `https://data.microbiomedata.org/` | Searchable multi-omics data and sample metadata. |
| KBase GROW collection | `https://narrative.kbase.us/collections/GROW` | Public collection with samples, MAGs, annotations, and genome-scale metabolic models. |
| KBase narrative DOI | `https://doi.org/10.25982/109073.30/1895615` | Article-linked KBase narrative structure. |
| GROWdb Explorer | `https://geocentroid.shinyapps.io/GROWdatabase/` | Shiny interface for microbial, metabolite, and geospatial browsing. |

Treat these as discovery and analysis interfaces. Use NCBI and Zenodo for reproducible bulk retrieval.

## Nature Supplementary Files

The Nature page hosts article companion files as Springer static assets:

| Asset | URL | Notes |
| --- | --- | --- |
| Supplementary Information | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-024-08240-z/MediaObjects/41586_2024_8240_MOESM1_ESM.docx` | Supplementary notes and methods details. |
| Reporting Summary | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-024-08240-z/MediaObjects/41586_2024_8240_MOESM2_ESM.pdf` | Nature reporting summary. |
| Supplementary Data 1 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-024-08240-z/MediaObjects/41586_2024_8240_MOESM3_ESM.xlsx` | River microbiome literature, metagenome/metatranscriptome info, geospatial variables, and chloroplast contamination analysis. |
| Supplementary Data 2 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-024-08240-z/MediaObjects/41586_2024_8240_MOESM4_ESM.xlsx` | GROWdb MAG taxonomy, quality, novelty, abundance, core analyses, and global MAG analysis. |
| Supplementary Data 3 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-024-08240-z/MediaObjects/41586_2024_8240_MOESM5_ESM.xlsx` | DRAM annotation summaries, trait calls, ARG calls, and ARG expression. |
| Supplementary Data 4 | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-024-08240-z/MediaObjects/41586_2024_8240_MOESM6_ESM.xlsx` | Emerging contaminant genes, ARG tabs, carbon usage, and statistical test values. |

## Code Repositories

| Repository or record | URL | Notes |
| --- | --- | --- |
| Data generation and processing scripts | `https://github.com/jmikayla1991/Genome-Resolved-Open-Watersheds-database-GROWdb` | Article-linked GitHub repository; GitHub API did not expose a license during curation. |
| Data generation scripts Zenodo | `https://doi.org/10.5281/zenodo.11041178` | Archived `GROW v1.0.0` code record. |
| Geospatial analysis and GROWdb Explorer code | `https://github.com/rossyndicate/GROWdb` | Article-linked GitHub repository; GitHub API reported MIT license during curation. |
| Figure and data analysis Zenodo | `https://doi.org/10.5281/zenodo.11188634` | Archived figure-generation and data-analysis code record. |

## Automation Decision

A source-specific `download.py` is not needed. Public access is already available through:

- NCBI BioProject, SRA, and Assembly records
- Zenodo direct file URLs with MD5 checksums
- Springer static supplementary files
- NMDC, KBase, and Shiny interfaces for discovery or point-and-click analysis

If a helper is added later, it should generate a Zenodo URL/checksum manifest and NCBI accession reports. It should not download the 3.9 GB global MAG archive or 1.2 GB gene FASTA by default.

## Verification

Checked on 2026-05-09.

During curation:

- The Nature article reported 3,825 medium- and high-quality MAGs dereplicated to 2,093 MAGs at 99% identity.
- Zenodo API record `8173287` reported 11 files totaling about 1.6 GB.
- Zenodo API record `11193259` reported 2 files totaling about 3.9 GB.
- NCBI E-utilities returned BioProject `PRJNA946291` with project title "Genome Resolved Open Watersheds database (GROWdb) Metagenome."
- GitHub API reported `rossyndicate/GROWdb` as MIT licensed and `jmikayla1991/Genome-Resolved-Open-Watersheds-database-GROWdb` with no exposed license.
