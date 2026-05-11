# Caprinae Gut MAG Catalog Notes

Verified on 2026-05-11 against Crossref DOI metadata, the ScienceDirect article mirror and supplement links, CNCB BioProject `PRJCA008889`, GSA project `CRA007205`, the public GSA download directory, and the authors' GitHub repository `qb-lyu/caprinaeGut`.

This resource comes from the Microbiology Spectrum article "A Catalog of over 5,000 Metagenome-Assembled Microbial Genomes from the Caprinae Gut Microbiota."

The resource is in scope for Awesome MAG because it reports a ruminant gut genome catalog of 5,046 MAGs from ultra-deep fecal metagenomes, with SGB clustering and functional annotations including CAZymes, biosynthetic gene clusters, antimicrobial resistance genes, and virulence genes.

## Resource Profile

Paper- and archive-reported scale:

- 30 fecal metagenomes from Caprinae animals in six regions of China.
- Host coverage includes domestic sheep and goats plus wild Caprinae samples.
- The article reports more than 100 Gbp per sample and about 3.3 Tb of high-quality metagenomic data after quality control.
- GSA `CRA007205` reports 30 runs, 60 paired FASTQ files, and 1218.75 GB of public sequence files.
- The authors generated 22,882 raw bins and retained 5,046 medium- and high-quality MAGs.
- The retained MAG catalog includes 1,933 high-quality and 3,113 medium-quality genomes.
- The article reports average completeness of 86.3% and average contamination of 1.4%.
- MAG dereplication/species clustering produced 3,306 SGBs.
- 2,530 genomes were reported as uncultured candidate species.
- Functional annotation includes 7,973 KEGG orthologs, 342 KEGG modules, 960,735 CAZyme genes across 344 CAZy families, 69 ARGs, and 302 virulence genes.

## Data Availability

The most reproducible public bulk route is CNCB GSA:

- BioProject: `PRJCA008889`
- GSA project: `CRA007205`
- HTTPS directory: `https://download.cncb.ac.cn/gsa2/CRA007205/`
- FTP directory: `ftp://download.big.ac.cn/gsa2/CRA007205`
- Checksum file: `https://download.cncb.ac.cn/gsa2/CRA007205/md5sum.txt`

The GSA download directory contains one subdirectory per run from `CRR516072` through `CRR516101`. Each run directory contains paired FASTQ files and a small run XML file. The top-level `md5sum.txt` has 60 entries for the FASTQ files.

The ScienceDirect article mirror exposes direct public supplement links:

- `spectrum.02211-22-s0001.xlsx`: sheets `ST1` through `ST9`
- `spectrum.02211-22-s0002.xlsx`: sheets `ST10` through `ST18`
- `spectrum.02211-22-s0003.pdf`: supplementary figures

The authors' GitHub repository contains figure-related code and small workflow/context files, not a data archive.

## Curation Caveats

- Use the ASM DOI page as the canonical article landing page, but note that command-line access to `journals.asm.org` returned a Cloudflare challenge during curation.
- Use the ScienceDirect mirror and `ars.els-cdn.com` supplement URLs for reproducible supplement downloads.
- Use GSA/CNCB for raw read retrieval. The direct directory and `md5sum.txt` are easier to automate than the paginated GSA browser page.
- During curation, BioProject `PRJCA008889` did not return linked GWH assembly records through the CNCB GWH BioProject lookup API, and the public GSA directory exposed raw reads rather than MAG FASTA/protein archives.
- Treat the 5,046 MAG count as the paper-reported catalog size. For actual MAG sequence FASTA access, the current public routes identified here are insufficient; the article/supplement should be checked in a browser and authors contacted if needed.
- No source-specific automation script is needed now. A small helper could generate the 30-run/60-FASTQ URL manifest and checksum table from the public GSA directory.

Primary citation:

- Zhang X-X, Lv Q-B, Yan Q-L, Zhang Y, Guo R-C, Meng J-X, et al. A Catalog of over 5,000 Metagenome-Assembled Microbial Genomes from the Caprinae Gut Microbiota. Microbiology Spectrum 10:e02211-22 (2022). https://doi.org/10.1128/spectrum.02211-22
