# ICRGGC Download Notes

ICRGGC has two practical access paths:

- NMDC/ICRGGC FTP files at `ftp://download.nmdc.cn/icrggc/`
- Figshare download-all ZIPs for the MAG and gene-catalog records

No repository script is needed because the main files have stable public URLs.

## NMDC FTP Files

| Asset | URL | Size | Notes |
| --- | --- | --- | --- |
| Gene catalog | `ftp://download.nmdc.cn/icrggc/gc_del_reorder.fa.gz` | 4.3 GB | Top-level gene catalog FASTA |
| Gene relative abundance | `ftp://download.nmdc.cn/icrggc/cds_ra_reorder.txt.gz` | 11.2 GB | Top-level abundance table |
| MAG archive | `ftp://download.nmdc.cn/icrggc/MAGs.tar.gz` | 8.5 GB | Top-level MAG archive |
| Split MAG directory | `ftp://download.nmdc.cn/icrggc/MAGs_list/Ref_genome/` | multiple files | Includes `MAGs_md5.txt` |
| Split gene catalog directory | `ftp://download.nmdc.cn/icrggc/MAGs_list/gc/` | multiple files | Includes `Gene_catalog_md5` |
| Split gene abundance directory | `ftp://download.nmdc.cn/icrggc/MAGs_list/gc_abundance/` | multiple files | Includes `Gene_catalog_md5` |

## Figshare Records

| Asset | DOI | Download-all URL | Size |
| --- | --- | --- | --- |
| MAGs | `10.6084/m9.figshare.15982089` | `https://ndownloader.figshare.com/articles/15982089/versions/1` | 7.8 GB |
| Gene catalog | `10.6084/m9.figshare.15911964` | `https://ndownloader.figshare.com/articles/15911964/versions/1` | 4.3 GB |
| Boxplot source data | `10.6084/m9.figshare.16871887` | Figshare landing page | 121 KB |

## Example Commands

Download the three top-level NMDC FTP files:

```bash
curl --disable-epsv -C - -O ftp://download.nmdc.cn/icrggc/gc_del_reorder.fa.gz
curl --disable-epsv -C - -O ftp://download.nmdc.cn/icrggc/cds_ra_reorder.txt.gz
curl --disable-epsv -C - -O ftp://download.nmdc.cn/icrggc/MAGs.tar.gz
```

List the split directories:

```bash
curl --disable-epsv --list-only ftp://download.nmdc.cn/icrggc/MAGs_list/Ref_genome/
curl --disable-epsv --list-only ftp://download.nmdc.cn/icrggc/MAGs_list/gc/
curl --disable-epsv --list-only ftp://download.nmdc.cn/icrggc/MAGs_list/gc_abundance/
```

Download split MAG files and their checksum manifest:

```bash
curl --disable-epsv -O ftp://download.nmdc.cn/icrggc/MAGs_list/Ref_genome/MAGs_md5.txt
for f in 1 2 3 4 5 6 10 11 12 13; do
  curl --disable-epsv -C - -O "ftp://download.nmdc.cn/icrggc/MAGs_list/Ref_genome/${f}.tar.gz"
done
curl --disable-epsv -C - -O ftp://download.nmdc.cn/icrggc/MAGs_list/Ref_genome/7_2.tar.gz
curl --disable-epsv -C - -O ftp://download.nmdc.cn/icrggc/MAGs_list/Ref_genome/8_2.tar.gz
curl --disable-epsv -C - -O ftp://download.nmdc.cn/icrggc/MAGs_list/Ref_genome/9_2.tar.gz
md5sum -c MAGs_md5.txt
```

Download Figshare ZIPs:

```bash
curl -L -o icrggc_mags_figshare_15982089.zip \
  https://ndownloader.figshare.com/articles/15982089/versions/1

curl -L -o icrggc_gene_catalog_figshare_15911964.zip \
  https://ndownloader.figshare.com/articles/15911964/versions/1
```

Query the ICRGGC MAG table API:

```bash
curl 'https://nmdc.cn/icrggcapi/api/icrggc/page?pageNo=1&pageSize=10&keyword='
```

The first page should report `totalElements: 12339`.

## Checksums For Split Files

The split FTP directories expose these checksum manifests:

```text
ftp://download.nmdc.cn/icrggc/MAGs_list/Ref_genome/MAGs_md5.txt
ftp://download.nmdc.cn/icrggc/MAGs_list/gc/Gene_catalog_md5
ftp://download.nmdc.cn/icrggc/MAGs_list/gc_abundance/Gene_catalog_md5
```

Use the split directories when you need per-part MD5 verification. The top-level FTP archives did not expose separate MD5 files on the ICRGGC download page when checked on 2026-05-08.

## Quirks

- Use `--disable-epsv` if FTP directory listing hangs or returns no output.
- The NMDC FTP `MAGs.tar.gz` file is larger than the Figshare `15982089.zip` archive, so pin the source in downstream manifests.
- Prefer the DOI `10.6084/m9.figshare.15982089` for the MAG Figshare record; the Nature reference list includes a shortened text form that should not be copied as the DOI.
