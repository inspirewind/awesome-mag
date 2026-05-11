# QXLSG Notes

Verified on 2026-05-09 against the Cell Reports article, Crossref metadata for DOI `10.1016/j.celrep.2025.116483`, NGDC BioProject `PRJCA037687`, GSA accessions `CRA025489` and `CRA029668`, the GWH BioProject assembly endpoint, and the Figshare share header behavior.

QXLSG is the Qinghai-Xizang Lake Sediment Genome catalog from "A deep metagenomic atlas of Qinghai-Xizang Plateau lakes reveals their microbial diversity and salinity adaptation mechanisms."

The resource is in scope for Awesome MAG because it provides a public high-altitude lake-sediment MAG catalog across a broad salinity gradient, with companion gene/BGC analyses and raw metagenome deposits.

## Resource Profile

Paper- and archive-reported scale:

- 28 sediment samples from ten salinity-gradient Qinghai-Xizang Plateau lakes
- 3.28 Tb raw metagenomic data
- 43,092 raw reconstructed bins before quality filtering
- 5,866 medium-quality-or-better MAGs, including 1,028 high-quality MAGs
- 1,888 co-assembly MAGs and 3,978 single-lake MAGs
- 2,742 species-level genomes after dereplication, including 656 high-quality MAGs and nine complete genomes
- 80.78% of species-level genomes reported as undescribed taxa
- 58,163,874 non-redundant protein-coding genes
- 19,008 antiSMASH-predicted biosynthetic gene clusters

## Data Availability

The article states that metagenomic and 16S raw data are deposited under NGDC BioProject `PRJCA037687`, and reconstructed MAGs are available through NODE analysis `OEZ00021318` and the Figshare share `https://figshare.com/s/74e7f72ed5eb1dd05a13`.

During curation, the NGDC BioProject page also exposed:

- GSA accession `CRA025489` for "Qinghai-Xizang Lake Genome catalog": 28 metagenome runs, 56 FASTQ files, 1,350.97 GB reported by GSA, static HTTPS/FTP/Qtrans paths, and `md5sum.txt`.
- GSA accession `CRA029668` for "Qinghai-Xizang Lake Microbial 16S rDNA sequencing": 28 16S runs, 56 FASTQ files, less than 1 GB reported by GSA, static HTTPS/FTP/Qtrans paths, and `md5sum.txt`.
- A GWH assembly endpoint returning 5,866 per-MAG records with direct `*.genome.fasta.gz` URLs. Example: `GWHHXZW00000000.1` maps to `metagenomes_adec_MAG_1_GWHHXZW00000000.1/GWHHXZW00000000.1.genome.fasta.gz`.

## Curation Caveats

- Prefer the Cell Reports article as the descriptive landing page and NGDC BioProject `PRJCA037687` as the archive landing page.
- Use GWH for reproducible direct MAG FASTA URLs when per-MAG downloads are acceptable. No single public bulk MAG archive was found during curation.
- Use GSA `CRA025489` for raw metagenomic reads and `CRA029668` for 16S reads; both expose MD5 files.
- Figshare share access should not be treated as command-line reproducible from this environment. A CLI HEAD request returned `HTTP/2 202` with `x-amzn-waf-action: challenge`.
- NODE analysis `OEZ00021318` is listed by the article, but a stable direct download URL was not identified during curation. Record the accession and search it from the NODE homepage if needed.
- GWH per-MAG FASTA files have byte-range support based on curation-time header checks.

No source-specific automation script is required for the README entry. A helper could be useful later to read the GWH BioProject assembly JSON and emit a per-MAG manifest, but the data are already exposed through a public endpoint.
