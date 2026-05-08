# Unified Human Gut Virome Download Notes

The Unified Human Gut Virome (UHGV) is available through a public NERSC static file index, an official JGI website download page, and a compact Zenodo v1.0 data record.

- Official website: `https://uhgv.jgi.doe.gov/`
- Official downloads page: `https://uhgv.jgi.doe.gov/downloads`
- NERSC index: `https://portal.nersc.gov/UHGV/`
- NERSC README: `https://portal.nersc.gov/UHGV/README.md`
- GitHub repository: `https://github.com/snayfach/UHGV`
- Zenodo v1.0 record: `https://zenodo.org/records/17402089`

No source-specific helper script is needed. The NERSC files are direct HTTP(S) downloads and support range requests. Use the Zenodo record when you want the smaller zstd-compressed core subset plus MD5 checksums.

## Recommended Starter Files

| Asset | URL | Size | Notes |
| --- | --- | ---: | --- |
| High-quality vOTU representative genomes | `https://portal.nersc.gov/UHGV/genome_catalogs/votus_hq_plus.fna.gz` | 701M | Recommended by the GitHub README for high-quality representative genomes. |
| vOTU metadata | `https://portal.nersc.gov/UHGV/metadata/votus_metadata.tsv` | 52M | Metadata for all 168,536 species-level vOTUs. |

## NERSC Core Genome Catalogs

Base path: `https://portal.nersc.gov/UHGV/genome_catalogs/`

| File | Size | Notes |
| --- | ---: | --- |
| `uhgv_full.fna.gz` | 6.5G | DNA FASTA for all full-tier UHGV genomes. |
| `uhgv_full.faa.gz` | 5.6G | Protein FASTA for all UHGV genomes. |
| `uhgv_mq_plus.fna.gz` | 5.1G | DNA FASTA for medium-quality-plus UHGV genomes. |
| `uhgv_mq_plus.faa.gz` | 3.8G | Protein FASTA for medium-quality-plus UHGV genomes. |
| `uhgv_hq_plus.fna.gz` | 3.0G | DNA FASTA for high-quality-plus UHGV genomes. |
| `uhgv_hq_plus.faa.gz` | 2.2G | Protein FASTA for high-quality-plus UHGV genomes. |
| `votus_full.fna.gz` | 1.3G | DNA FASTA for all species-level vOTU representatives. |
| `votus_full.faa.gz` | 1.0G | Protein FASTA for all species-level vOTU representatives. |
| `votus_mq_plus.fna.gz` | 1.0G | DNA FASTA for medium-quality-plus vOTU representatives. |
| `votus_mq_plus.faa.gz` | 796M | Protein FASTA for medium-quality-plus vOTU representatives. |
| `votus_hq_plus.fna.gz` | 701M | DNA FASTA for high-quality-plus vOTU representatives. |
| `votus_hq_plus.faa.gz` | 522M | Protein FASTA for high-quality-plus vOTU representatives. |
| `host_genomes.tar.gz` | 4.2G | Gut prokaryote genome sequences used for host prediction/read mapping. |
| `prokaryote_reps.fna.gz` | 4.3G | Prokaryotic representative FASTA used by profiling/index resources. |

## Metadata and Annotation Files

| File | URL | Size | Notes |
| --- | --- | ---: | --- |
| `uhgv_metadata.tsv` | `https://portal.nersc.gov/UHGV/metadata/uhgv_metadata.tsv` | 207M | Genome-level metadata for 873,995 UHGV genomes. |
| `votus_metadata.tsv` | `https://portal.nersc.gov/UHGV/metadata/votus_metadata.tsv` | 52M | Main vOTU metadata table. |
| `votus_metadata_extended.tsv` | `https://portal.nersc.gov/UHGV/metadata/votus_metadata_extended.tsv` | 129M | Extended species-level vOTU metadata. |
| `host_metadata.tsv` | `https://portal.nersc.gov/UHGV/metadata/host_metadata.tsv` | 131M | Host/prokaryote taxonomy and quality metadata. |
| `source_biosample_metadata.tsv` | `https://portal.nersc.gov/UHGV/metadata/source_biosample_metadata.tsv` | 5.3M | Biosample metadata for source samples. |
| `protein_annotations.tsv.gz` | `https://portal.nersc.gov/UHGV/annotations/protein_annotations.tsv.gz` | 329M | Functional annotations for proteins encoded by vOTU representatives. |
| `tRNAs.tsv.gz` | `https://portal.nersc.gov/UHGV/annotations/tRNAs.tsv.gz` | 1.4M | tRNAs predicted in vOTU representatives. |
| `DGRs.tsv.gz` | `https://portal.nersc.gov/UHGV/annotations/DGRs.tsv.gz` | 144K | Diversity-generating retroelements predicted in vOTU representatives. |

## Host Prediction, Phylogeny, and Profiling Files

| File | URL | Size | Notes |
| --- | --- | ---: | --- |
| `crispr_spacers.fna` | `https://portal.nersc.gov/UHGV/host_predictions/crispr_spacers.fna` | 428M | 5,318,089 CRISPR spacers. |
| `host_assignment_crispr.tsv` | `https://portal.nersc.gov/UHGV/host_predictions/host_assignment_crispr.tsv` | 311M | Host predictions from CRISPR spacer matches. |
| `host_assignment_kmers.tsv` | `https://portal.nersc.gov/UHGV/host_predictions/host_assignment_kmers.tsv` | 372M | Host predictions from PHIST k-mer matching. |
| `host_genomes_info.tsv` | `https://portal.nersc.gov/UHGV/host_predictions/host_genomes_info.tsv` | 128M | GTDB r207 taxonomy for UHGG, NCBI, and Hadza host genomes. |
| `phylogenetic_host_range_breadth.tsv` | `https://portal.nersc.gov/UHGV/host_predictions/phylogenetic_host_range_breadth.tsv` | 9.6M | Estimated phylogenetic host-range breadth. |
| `caudoviricetes_tree.nwk.gz` | `https://portal.nersc.gov/UHGV/phylogeny/caudoviricetes_tree.nwk.gz` | 3.4M | Caudoviricetes phylogeny. |
| `metagenomes_coverm.tsv.gz` | `https://portal.nersc.gov/UHGV/read_mapping/metagenomes_coverm.tsv.gz` | 2.7G | CoverM statistics for bulk metagenomes. |
| `viromes_coverm.tsv.gz` | `https://portal.nersc.gov/UHGV/read_mapping/viromes_coverm.tsv.gz` | 125M | CoverM statistics for viral-enriched metagenomes. |
| `relative_abundance.tsv` | `https://portal.nersc.gov/UHGV/read_mapping/relative_abundance.tsv` | 50M | Per-sample relative abundances of viruses and hosts. |
| `sample_metadata.tsv` | `https://portal.nersc.gov/UHGV/read_mapping/sample_metadata.tsv` | 584K | Metadata for read-mapping samples. |
| `study_metadata.tsv` | `https://portal.nersc.gov/UHGV/read_mapping/study_metadata.tsv` | 16K | Study-level sample metadata. |

## Protein Clusters and Structures

| File | URL | Size | Notes |
| --- | --- | ---: | --- |
| `protein_clusters.tsv` | `https://portal.nersc.gov/UHGV/protein_clusters/protein_clusters.tsv` | 232M | Protein-cluster summary table. |
| `cluster_membership.tsv.gz` | `https://portal.nersc.gov/UHGV/protein_clusters/cluster_membership.tsv.gz` | 217M | Cluster membership for UHGV proteins. |
| `cluster_taxonomy.tsv.gz` | `https://portal.nersc.gov/UHGV/protein_clusters/cluster_taxonomy.tsv.gz` | 64M | Consensus UHGV and ICTV taxonomy for each protein cluster. |
| `MSAs.tar.gz` | `https://portal.nersc.gov/UHGV/protein_clusters/MSAs.tar.gz` | 1.3G | Multiple sequence alignments of clusters with at least 15 members. |
| `msa_neff.tsv.gz` | `https://portal.nersc.gov/UHGV/protein_clusters/msa_neff.tsv.gz` | 1.0M | Effective sequence counts for MSAs. |
| `PDB.tar.gz` | `https://portal.nersc.gov/UHGV/structures/PDB.tar.gz` | 1.5G | UHGV predicted protein structures in PDB format. |
| `PDB_references.tar.gz` | `https://portal.nersc.gov/UHGV/structures/PDB_references.tar.gz` | 1.4G | Reference predicted structures for COG, HAMAP, NCBIfam, and Pfam entries. |
| `PDB_domains.tar.gz` | `https://portal.nersc.gov/UHGV/structures/PDB_domains.tar.gz` | 397M | PDB domain files. |
| `JSON.tar.gz` | `https://portal.nersc.gov/UHGV/structures/JSON.tar.gz` | 9.1G | JSON-format predicted structure output. |
| `domains.tsv` | `https://portal.nersc.gov/UHGV/structures/domains.tsv` | 2.6M | Domain segmentation table. |
| `structure_annotation.tsv.gz` | `https://portal.nersc.gov/UHGV/structures/structure_annotation.tsv.gz` | 2.4M | Structure annotation table. |
| `uhgv_structure_db.bca` | `https://portal.nersc.gov/UHGV/structures/uhgv_structure_db.bca` | 81M | Structure database file used by search tooling. |

## Zenodo Compact v1.0 Files

The Zenodo record provides the most relevant files in `.zst` format and includes MD5 checksums.

| File | URL | Size | MD5 |
| --- | --- | ---: | --- |
| `uhgv_full.fna.zst` | `https://zenodo.org/records/17402089/files/uhgv_full.fna.zst?download=1` | 1.5G | `6608f58dbd0e451c9a494ccf69cb3a35` |
| `uhgv_full.faa.zst` | `https://zenodo.org/records/17402089/files/uhgv_full.faa.zst?download=1` | 4.7G | `d2120a8c5f39e83092e087b551614142` |
| `votus_full.fna.zst` | `https://zenodo.org/records/17402089/files/votus_full.fna.zst?download=1` | 920M | `9ad996fea08c6087a452194f0c2f9d33` |
| `votus_full.faa.zst` | `https://zenodo.org/records/17402089/files/votus_full.faa.zst?download=1` | 975M | `1eff9626a8c3990a98d2b4ea58ff0596` |
| `uhgv_metadata.tsv.zst` | `https://zenodo.org/records/17402089/files/uhgv_metadata.tsv.zst?download=1` | 37M | `f897bdf92b8b93cf3941f6d2c3d55efb` |
| `votus_metadata_extended.tsv.zst` | `https://zenodo.org/records/17402089/files/votus_metadata_extended.tsv.zst?download=1` | 13M | `6702355349e933fb605e62a8bbaa50a9` |
| `source_biosample_metadata.tsv.zst` | `https://zenodo.org/records/17402089/files/source_biosample_metadata.tsv.zst?download=1` | 149K | `9934204a79cdac60ce9681a6233282b6` |
| `host_range_breadth.tsv.zst` | `https://zenodo.org/records/17402089/files/host_range_breadth.tsv.zst?download=1` | 479K | `25960f854fa411956ef1353213133bfc` |
| `read_mapping_relative_abundances.tsv.zst` | `https://zenodo.org/records/17402089/files/read_mapping_relative_abundances.tsv.zst?download=1` | 11M | `e6d9feb8e7e583076c2a8fa88ee354f1` |
| `read_mapping_sample_metadata.tsv.zst` | `https://zenodo.org/records/17402089/files/read_mapping_sample_metadata.tsv.zst?download=1` | 68K | `98df06e9bd17f6c0d1fd374fcea6763d` |
| `read_mapping_study_metadata.tsv.zst` | `https://zenodo.org/records/17402089/files/read_mapping_study_metadata.tsv.zst?download=1` | 5K | `be82bec4d0650b6af42ab7301c4d5332` |

## Example Commands

Download the recommended starter files:

```bash
curl -L -C - -O https://portal.nersc.gov/UHGV/genome_catalogs/votus_hq_plus.fna.gz
curl -L -C - -O https://portal.nersc.gov/UHGV/metadata/votus_metadata.tsv
```

Download the main full-tier genome and protein catalogs:

```bash
curl -L -C - -O https://portal.nersc.gov/UHGV/genome_catalogs/uhgv_full.fna.gz
curl -L -C - -O https://portal.nersc.gov/UHGV/genome_catalogs/uhgv_full.faa.gz
curl -L -C - -O https://portal.nersc.gov/UHGV/metadata/uhgv_metadata.tsv
```

Download the compact Zenodo subset and verify an MD5 checksum:

```bash
curl -L -C - -o uhgv_full.fna.zst "https://zenodo.org/records/17402089/files/uhgv_full.fna.zst?download=1"
echo "6608f58dbd0e451c9a494ccf69cb3a35  uhgv_full.fna.zst" | md5sum -c -
```

Inspect table columns before downstream processing:

```bash
zcat protein_annotations.tsv.gz | head -n 2
head -n 2 uhgv_metadata.tsv
head -n 2 votus_metadata.tsv
head -n 2 host_assignment_crispr.tsv
```

## Verification and Caveats

- The NERSC index did not show MD5 or SHA checksum files during curation.
- The Zenodo record is the better source when checksums are required, but it contains only a compact subset rather than every NERSC auxiliary file.
- The NERSC top-level `README.md` is older than the current GitHub README and Zenodo v1.0 record. Prefer the GitHub README and Zenodo record for current counts and file naming.
- The per-vOTU representative area under `votu_reps/` contains many sharded directories. Prefer the aggregate FASTA/FAA files in `genome_catalogs/` unless per-genome GFF or annotation files are specifically needed.
- This resource is a viral/phage genome catalogue, not a bacterial or archaeal MAG catalogue. It is included here as a human-gut metagenomic companion resource.

Checked on 2026-05-08.
