# ICRGGC Notes

- ICRGGC is the Integrated Chicken Reference Genomes and Gene Catalog hosted by the National Microbiology Data Center at `https://nmdc.cn/icrggc/`.
- The companion paper is Feng et al. 2021, "Metagenome-Assembled Genomes and Gene Catalog from the Chicken Gut Microbiome Aid in Deciphering Antibiotic Resistomes".
- The resource reports 12,339 strain-level MAGs from 1,978 species, including 893 novel species, 38 novel genera, and 9,845 novel strains.
- The gene catalog contains 16,565,684 genes; the ICRGGC homepage reports 68.2% eggNOG annotation coverage.
- The study integrates 799 public chicken fecal metagenomes and six newly generated chicken fecal metagenomes.
- The ICRGGC data table is backed by a public API at `https://nmdc.cn/icrggcapi/api/icrggc/page`.
- The download page links three top-level FTP files: `gc_del_reorder.fa.gz`, `cds_ra_reorder.txt.gz`, and `MAGs.tar.gz`.
- The FTP root also exposes `MAGs.tar.gz.bak_20220906`, with the same observed size as `MAGs.tar.gz`; it is not linked in the page download table.
- The `MAGs_list` FTP directory provides split MAG, gene catalog, and gene abundance files plus MD5 manifests for the split files.
- The Nature article's Data availability section points to Figshare DOI `10.6084/m9.figshare.15982089` for MAGs and DOI `10.6084/m9.figshare.15911964` for the gene catalog.
- The article reference list appears to contain a shortened MAG DOI text (`1592089`); use the Data availability DOI `15982089`.
- Figshare and NMDC provide overlapping data, but the MAG archive byte sizes differ: the Figshare download-all ZIP is about 7.8 GB, while NMDC `MAGs.tar.gz` is about 8.5 GB.
- Checked on 2026-05-08: the NMDC FTP file headers were reachable with `curl --disable-epsv -I`, and the ICRGGC API reported `totalElements: 12339`.

## Main Data Files

| Source | File | Size | Notes |
| --- | --- | --- | --- |
| NMDC FTP | `gc_del_reorder.fa.gz` | 4.3 GB | Gene catalog; matches the Figshare gene-catalog scale |
| NMDC FTP | `cds_ra_reorder.txt.gz` | 11.2 GB | Gene relative-abundance matrix |
| NMDC FTP | `MAGs.tar.gz` | 8.5 GB | Top-level MAG archive |
| Figshare | `15911964.zip` | 4.3 GB | Gene catalog download-all ZIP |
| Figshare | `15982089.zip` | 7.8 GB | MAG download-all ZIP |

## Split FTP Directories

| Directory | Contents | Checksum file |
| --- | --- | --- |
| `MAGs_list/Ref_genome/` | 13 MAG tarballs plus `MAGs_md5.txt` | `MAGs_md5.txt` |
| `MAGs_list/gc/` | 9 gene catalog FASTA parts plus `split.sh.gz` | `Gene_catalog_md5` |
| `MAGs_list/gc_abundance/` | 10 gene abundance table parts | `Gene_catalog_md5` |

## Raw Read Projects

The paper cites raw metagenomic sequencing data from:

- ENA `PRJEB22062`
- ENA `PRJEB33338`
- NCBI SRA `SRP144318`
- Genome Sequence Archive `CRA003773`
