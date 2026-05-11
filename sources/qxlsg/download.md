# QXLSG Download Notes

QXLSG is distributed across the article data-availability links plus NGDC archive records. The practical reproducible route is NGDC/GSA for reads and GWH for per-MAG genome FASTA files.

Primary links:

- Article: `https://www.sciencedirect.com/science/article/pii/S2211124725012549`
- DOI: `https://doi.org/10.1016/j.celrep.2025.116483`
- NGDC BioProject: `https://ngdc.cncb.ac.cn/bioproject/browse/PRJCA037687`
- GWH assembly listing API: `https://ngdc.cncb.ac.cn/gwh/gsa/ajax/getAssembliesListByBioProjectAccession/PRJCA037687`
- NODE homepage: `https://www.biosino.org/node/` with analysis accession `OEZ00021318`
- Figshare share: `https://figshare.com/s/74e7f72ed5eb1dd05a13`

## MAG Assemblies

The article lists NODE analysis `OEZ00021318` and Figshare for reconstructed MAGs. During curation, NGDC BioProject `PRJCA037687` also exposed the full 5,866 MAG set through GWH.

| Asset | URL | Notes |
| --- | --- | --- |
| GWH assemblies API | `https://ngdc.cncb.ac.cn/gwh/gsa/ajax/getAssembliesListByBioProjectAccession/PRJCA037687` | JSON endpoint returning `count: 5866`, each record's GWH accession, assembly page, and direct DNA download URL. |
| Example assembly page | `https://ngdc.cncb.ac.cn/gwh/Assembly/111872/show` | GWH page for `GWHHXZW00000000.1` / `adec_MAG_1`. |
| Example FASTA | `https://download.cncb.ac.cn/gwh/Others/metagenomes_adec_MAG_1_GWHHXZW00000000.1/GWHHXZW00000000.1.genome.fasta.gz` | 824,396 bytes; last modified 2026-03-20; byte-range supported. |
| NODE analysis | `OEZ00021318` | Article-listed MAG deposition accession; search from the NODE homepage if direct routing changes. |
| Figshare share | `https://figshare.com/s/74e7f72ed5eb1dd05a13` | Article-listed MAG deposition route; CLI checks returned an AWS WAF challenge during curation. |

Fetch the GWH JSON manifest:

```bash
curl -L -o qxlsg-gwh-assemblies.json https://ngdc.cncb.ac.cn/gwh/gsa/ajax/getAssembliesListByBioProjectAccession/PRJCA037687
```

Extracting the `downloadLinks.downloadLinksList[].link` values from that JSON yields the direct per-MAG `*.genome.fasta.gz` URLs.

## Raw Metagenomes

GSA accession: `CRA025489`

| Asset | URL | Notes |
| --- | --- | --- |
| GSA page | `https://ngdc.cncb.ac.cn/gsa/browse/CRA025489` | "Qinghai-Xizang Lake Genome catalog"; GSA reports 56 files and 1,350.97 GB. |
| HTTPS index | `https://download.cncb.ac.cn/gsa5/CRA025489/` | Static directory with 28 `CRR1838783`-`CRR1838810` run subdirectories plus `md5sum.txt`. |
| FTP index | `ftp://download.big.ac.cn/gsa5/CRA025489` | FTP alternative for large transfer clients. |
| Qtrans | `https://qtp.cncb.ac.cn/qtrans/v2/file?path=/gsa5/CRA025489` | GSA's recommended large-file transfer route. |
| MD5 list | `https://download.cncb.ac.cn/gsa5/CRA025489/md5sum.txt` | MD5 checksums for the 56 FASTQ files. |

Example run directory:

| File | Size | URL |
| --- | ---: | --- |
| `CRR1838810_r1.fq.gz` | 30,794,101,979 bytes | `https://download.cncb.ac.cn/gsa5/CRA025489/CRR1838810/CRR1838810_r1.fq.gz` |
| `CRR1838810_r2.fq.gz` | 32,038,466,211 bytes | `https://download.cncb.ac.cn/gsa5/CRA025489/CRR1838810/CRR1838810_r2.fq.gz` |
| `CRR1838810_sta.xml` | 2,631 bytes | `https://download.cncb.ac.cn/gsa5/CRA025489/CRR1838810/CRR1838810_sta.xml` |

Example:

```bash
curl -L -C - -O https://download.cncb.ac.cn/gsa5/CRA025489/md5sum.txt
curl -L -C - -O https://download.cncb.ac.cn/gsa5/CRA025489/CRR1838810/CRR1838810_r1.fq.gz
curl -L -C - -O https://download.cncb.ac.cn/gsa5/CRA025489/CRR1838810/CRR1838810_r2.fq.gz
```

## 16S Companion Reads

GSA accession: `CRA029668`

| Asset | URL | Notes |
| --- | --- | --- |
| GSA page | `https://ngdc.cncb.ac.cn/gsa/browse/CRA029668` | "Qinghai-Xizang Lake Microbial 16S rDNA sequencing"; GSA reports 56 files and less than 1 GB. |
| HTTPS index | `https://download.cncb.ac.cn/gsa5/CRA029668/` | Static directory with 28 `CRR2102888`-`CRR2102915` run subdirectories plus `md5sum.txt`. |
| FTP index | `ftp://download.big.ac.cn/gsa5/CRA029668` | FTP alternative. |
| Qtrans | `https://qtp.cncb.ac.cn/qtrans/v2/file?path=/gsa5/CRA029668` | GSA transfer route. |
| MD5 list | `https://download.cncb.ac.cn/gsa5/CRA029668/md5sum.txt` | MD5 checksums for the 56 FASTQ files. |

Example:

```bash
curl -L -C - -O https://download.cncb.ac.cn/gsa5/CRA029668/md5sum.txt
curl -L -C - -O https://download.cncb.ac.cn/gsa5/CRA029668/CRR2102915/CRR2102915_r1.fq.gz
curl -L -C - -O https://download.cncb.ac.cn/gsa5/CRA029668/CRR2102915/CRR2102915_r2.fq.gz
```

## Article Supplementary Files

The ScienceDirect article page lists supplementary datasets that are useful for curation and downstream annotation:

| File | Notes |
| --- | --- |
| `Document S1` | Figures S1-S12, PDF, about 2 MB. |
| `Dataset S1` | Sample information, data processing, and MAG information; sheets 1-4; about 1 MB. |
| `Dataset S2` | Functional details of QXLSG MAGs; sheets 1-7; about 10 MB. |
| `Dataset S3` | Salinity-adaptation genes of QXLSG MAGs; sheets 1-4; about 2 MB. |
| `Document S2` | Article plus supplemental information, PDF, about 9 MB. |

## Automation Decision

A source-specific `download.py` is not needed for the current awesome entry. GSA raw-read directories are static and checksum-backed, and GWH exposes the MAG FASTA URLs through a public JSON endpoint.

If a helper is added later, it should:

- fetch the GWH assemblies JSON for `PRJCA037687`;
- emit a TSV/JSON manifest with GWH accession, assembly page, MAG label, direct FASTA URL, file size if checked, and last-modified date if checked;
- avoid downloading all raw reads by default because `CRA025489` is about 1.35 TB;
- avoid trying to bypass the Figshare WAF challenge.

## Verification and Caveats

- The article, Crossref record, NGDC BioProject, GSA pages, GSA static indexes, and GWH assembly endpoint were checked on 2026-05-09.
- The GWH endpoint returned `count: 5866`, matching the article's MAG count.
- The BioProject page reports 5,894 BioSample records because it includes MAG assembly-linked BioSamples plus the original lake samples.
- GSA `CRA025489` and `CRA029668` each expose `md5sum.txt`.
- Figshare CLI access returned `HTTP/2 202` with `x-amzn-waf-action: challenge`; use browser access or the provider-listed NODE/GWH routes instead of scripting around that challenge.
