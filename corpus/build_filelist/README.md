# Cluster Filelist Build Tracking

This directory contains the manual, dataset-specific builders used after downloads have completed. Each builder should preserve genome-level boundaries: one bacterial or archaeal MAG FASTA path per line for RabbitTClust, and viral genome inputs for vclust.

## Current workflow

1. Collect dataset metadata and identify the correct MAG or viral genome sequence payload.
2. Download with the scripts under `corpus/download_bash/`.
3. Verify local integrity and packaging.
4. Build dataset-specific filelists with scripts in this directory.
5. Submit clustering jobs with RabbitTClust for bacterial/archaeal MAGs, and vclust for viral datasets.

Filelists should use absolute paths. Archive-backed datasets should be extracted into `downloads/<slug>/extracted/` or another dataset-specific materialized directory before the filelist is written.

## Implemented builders

| Dataset | Slug | Builder | Cluster tool | Output | Status |
| --- | --- | --- | --- | --- | --- |
| Anammox Microbiota Catalog | `anammox-microbiota` | `anammox_microbiota.sh` | RabbitTClust | `corpus/cluster_inputs/rabbittclust/anammox-microbiota.list` | ZIP verified; 1,768 strain-level MAG FASTA files; builder implemented. |

Run the Anammox builder from the repository root:

```bash
bash corpus/build_filelist/anammox_microbiota.sh
```

The Anammox builder checks that `downloads/anammox-microbiota/anammox_microbiota_figshare_45271516.zip` is exactly `1,865,155,640` bytes, validates the ZIP unless `--skip-zip-test` is passed, extracts `Strain_level_MAGs/*.fa`, and writes one absolute FASTA path per line.

## Dataset tracking

| Dataset | Slug | Payload status | Integrity status | Filelist status | Cluster tool | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Anammox Microbiota Catalog | `anammox-microbiota` | Downloaded `Strain_level_MAGs.zip` from Figshare file `45271516`. | Verified ZIP OK; 1,768 `.fa` members. | Implemented. | RabbitTClust | Each `.fa` is one strain-level MAG. |
| Bin Chicken Rare Biosphere Genomes | `bin-chicken-rbgs` | Two large MAG tarballs downloaded on the server. | Pending manual recheck. | Pending. | RabbitTClust | Archive members appear to be one FASTA per MAG. |
| cFMD | `cfmd` | `cFMD_mags.tar.gz` present on the server. | Pending manual recheck. | Pending. | RabbitTClust | Archive members appear to be MAG FASTA files. |
| Glacier-fed Streams MAGs | `gfs` | `ProkaryoticMAGsContig.tar` present on the server. | Pending manual recheck. | Pending. | RabbitTClust | Archive members appear to be MAG FASTA files. |
| GROWdb global dereplicated set | `growdb` | `5986_99ID_drep_global.tar.gz` present on the server. | Pending manual recheck. | Pending. | RabbitTClust | This is the 99% dereplicated global comparison set. |
| Gut Phage Database | `gut-phage-database` | Single `GPD_sequences.fa.gz` present on the server. | Pending manual recheck. | Pending. | vclust | Viral dataset; do not send to RabbitTClust. |
| HRGM | `hrgm` | `HRGMv2_Rep_Genome.tar.gz` present on the server. | Pending manual recheck. | Pending. | RabbitTClust | Representative genome archive. |
| HROM | `hrom` | `HROM_nonredundant_genomes.tar.gz` present on the server. | Needs recheck. | Pending. | RabbitTClust | Previous archive scan hit gzip EOF; verify before extracting. |
| Human Gut Archaeome | `human-gut-archaeome` | `archaea_gut-genomes.tar.gz` present on the server. | Pending manual recheck. | Pending. | RabbitTClust | Archaeal MAG/genome archive. |
| ICRGGC | `icrggc` | `MAGs.tar.gz` present on the server. | Pending manual recheck. | Pending. | RabbitTClust | MAG archive. |
| LakePulse MAG Catalogue | `lakepulse` | Server directory was empty in the last inventory. | Not downloaded. | Blocked. | RabbitTClust | Re-run download before validation. |
| Metagenomic Gut Virus catalogue | `mgv` | Single `mgv_votu_representatives.fna` present on the server. | Pending manual recheck. | Pending. | vclust | Viral dataset; one representative viral genome record per vOTU. |
| mOTUs DB | `motus-db` | Very large `mOTUs4.genomes.tar` present on the server. | Pending manual recheck. | Pending. | RabbitTClust | 2.5 TB archive; use careful tar listing before extraction. |
| MRGM | `mrgm` | `MRGM_All_55893_genomes.tar.gz` present on the server. | Pending manual recheck. | Pending. | RabbitTClust | MAG/genome archive. |
| OMDB | `omdb` | Very large `OMDv2.genomes.db.tar.gz` present on the server. | Pending manual recheck. | Pending. | RabbitTClust | Exclude gene and FetchMG FASTA files when building MAG filelist. |
| PIGC | `pigc` | 6,339 per-MAG `.fa.gz` files downloaded. | Pending manual recheck. | Pending. | RabbitTClust | Direct filelist builder can point to `.fa.gz` files. |
| RUG2 Rumen MAGs | `rug2` | 5,364 per-assembly `.fa.gz` files downloaded. | Pending manual recheck. | Pending. | RabbitTClust | ENA binned metagenome sequence superset. |
| SMAG | `smag` | Reassembled `mag.tar.gz` and split parts present on the server. | Pending manual recheck. | Pending. | RabbitTClust | Use `mag.tar.gz`; ignore split parts and companion `.fa`. |
| SPIRE | `spire` | 68 local study tarballs in the last inventory. | Incomplete. | Blocked. | RabbitTClust | Manifest had 714 rows; one local tar was zero-size. |
| TPMC | `tpmc` | `TPMC_MAG.tar.gz` present on the server. | Pending manual recheck. | Pending. | RabbitTClust | MAG archive. |
| UHGV | `uhgv` | Single `votus_hq_plus.fna.gz` present on the server. | Pending manual recheck. | Pending. | vclust | Viral dataset; do not send to RabbitTClust. |
| UHSG | `uhsg` | 5,779 per-MAG `.fa.gz` files downloaded. | Pending manual recheck. | Pending. | RabbitTClust | Direct filelist builder can point to `.fa.gz` files. |

## Builder conventions

- Use absolute paths in filelists.
- Keep one genome per line at the MAG or viral genome level.
- Do not split bacterial/archaeal MAG FASTA files by contig.
- Keep viral datasets out of RabbitTClust inputs.
- Validate archive integrity before writing a completed filelist.
- Make builders idempotent so interrupted extraction can be resumed safely.
