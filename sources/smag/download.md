# SMAG Download Notes

Prefer the Zenodo record for reproducible access:

- Landing page: `https://zenodo.org/records/8223844`
- API record: `https://zenodo.org/api/records/8223844`
- Files API: `https://zenodo.org/api/records/8223844/files`
- DOI: `https://doi.org/10.5281/zenodo.8223844`

Zenodo records the dataset as open access under CC BY 4.0. The record includes the split `mag.tar.gz.*` main MAG archive, `SMAG_README.md`, `magvirus.fa`, `SNV_CATALOG.tar.gz`, supplementary tables, and a phylogenetic tree file.

## Main MAG Archive

The main MAG archive is split into 373 files with the `mag.tar.gz.*` prefix, totaling approximately 36.3 GiB in the Zenodo file metadata. Use the Zenodo files API to generate a current URL list instead of maintaining every part URL by hand.

Download all MAG archive parts with `wget`:

```bash
curl -sS https://zenodo.org/api/records/8223844/files \
  | jq -r '.entries[]
      | select(.key | startswith("mag.tar.gz."))
      | "https://zenodo.org/records/8223844/files/\(.key | @uri)?download=1"' \
  > smag-mag-parts.urls

wget -c --content-disposition -i smag-mag-parts.urls
```

Equivalent `aria2c` download:

```bash
curl -sS https://zenodo.org/api/records/8223844/files \
  | jq -r '.entries[]
      | select(.key | startswith("mag.tar.gz."))
      | .links.content + "\n  out=" + .key' \
  > smag-mag-parts.aria2

aria2c -c -x 4 -s 4 -i smag-mag-parts.aria2
```

Optionally write an MD5 manifest from Zenodo metadata and check every downloaded part:

```bash
curl -sS https://zenodo.org/api/records/8223844/files \
  | jq -r '.entries[]
      | select(.key | startswith("mag.tar.gz."))
      | "\(.checksum | sub("^md5:"; ""))  \(.key)"' \
  > smag-mag-parts.md5

md5sum -c smag-mag-parts.md5
```

After all parts are present, reassemble and unpack:

```bash
LC_ALL=C cat ./mag.tar.gz.* > mag.tar.gz
tar -xvf mag.tar.gz
```

The upstream README uses `tar -xjvf`; the command above leaves compression detection to `tar`, which is safer because the `.tar.gz` extension normally implies gzip rather than bzip2.

## Other Zenodo Direct Downloads

The following direct commands use the Zenodo record file URLs. Quote the URLs because the `?download=1` query string is interpreted by some shells.

Core companion files:

```bash
curl -L -C - -o SMAG_README.md \
  'https://zenodo.org/records/8223844/files/SMAG_README.md?download=1'

curl -L -C - -o magvirus.fa \
  'https://zenodo.org/records/8223844/files/magvirus.fa?download=1'

curl -L -C - -o SNV_CATALOG.tar.gz \
  'https://zenodo.org/records/8223844/files/SNV_CATALOG.tar.gz?download=1'

curl -L -C - -o RAxML_bestTree.mag20177prodigal_refined1.tre \
  'https://zenodo.org/records/8223844/files/RAxML_bestTree.mag20177prodigal_refined1.tre?download=1'
```

Supplementary tables:

```bash
curl -L -C - -o 'Supplementary Data 1.xlsx' \
  'https://zenodo.org/records/8223844/files/Supplementary%20Data%201.xlsx?download=1'

curl -L -C - -o 'Supplementary Data 2.xlsx' \
  'https://zenodo.org/records/8223844/files/Supplementary%20Data%202.xlsx?download=1'

curl -L -C - -o 'Supplementary Data 2 subgroup.xlsx' \
  'https://zenodo.org/records/8223844/files/Supplementary%20Data%202%20subgroup.xlsx?download=1'

curl -L -C - -o 'Supplementary Data 3.xlsx' \
  'https://zenodo.org/records/8223844/files/Supplementary%20Data%203.xlsx?download=1'

curl -L -C - -o 'Supplementary Data 4.xlsx' \
  'https://zenodo.org/records/8223844/files/Supplementary%20Data%204.xlsx?download=1'

curl -L -C - -o 'Supplementary Data 5.xlsx' \
  'https://zenodo.org/records/8223844/files/Supplementary%20Data%205.xlsx?download=1'

curl -L -C - -o 'Supplementary Data 6.xlsx' \
  'https://zenodo.org/records/8223844/files/Supplementary%20Data%206.xlsx?download=1'
```

Download every non-MAG companion file from the current Zenodo API metadata:

```bash
curl -sS https://zenodo.org/api/records/8223844/files \
  | jq -r '.entries[]
      | select((.key | startswith("mag.tar.gz.")) | not)
      | "https://zenodo.org/records/8223844/files/\(.key | @uri)?download=1"' \
  > smag-companion-files.urls

wget -c --content-disposition -i smag-companion-files.urls
```

## Mirror Checks

The project page lists CyVerse and China-region S3 mirrors. Treat these as secondary mirrors, not the primary reproducible endpoint.

Checked on 2026-04-27:

- `https://data.cyverse.org/dav-anon/iplant/home/lucyzju/Caiyu_SMAG_catalog_2023/MAGdrep.tar.gz` returned `307 Temporary Redirect` to `https://unblockme.cyverse.org/`.
- `https://data.cyverse.org/dav-anon/iplant/home/lucyzju/Caiyu_SMAG_catalog_2023/MAG.tar.gz` returned `307 Temporary Redirect` to `https://unblockme.cyverse.org/`.
- `https://bma-smag.s3.cn-northwest-1.amazonaws.com.cn/SMAG/MAG40039.tar.gz` returned `404 Not Found`.
- `https://bma-smag.s3.cn-northwest-1.amazonaws.com.cn/SMAG/magdrep.tar.gz` returned `404 Not Found`.

The project page says the SMAG web interface is under website maintenance, so avoid depending on it for automated access.

## Companion Resources

- Project page: `https://microbma.github.io/project/SMAG.html`
- GitHub repository: `https://github.com/Caiyulu-818/SMAG`
- Pipeline code: `https://github.com/Caiyulu-818/SMAG/tree/main/Pipeline`
- Figure scripts: `https://github.com/Caiyulu-818/SMAG/tree/main/scripts`
- Figshare source data: `https://doi.org/10.6084/m9.figshare.23298791`
