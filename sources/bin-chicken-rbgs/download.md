# Bin Chicken Rare Biosphere Genomes Download Notes

Zenodo exposes direct file URLs for all files in this record family. No repository script is needed.

## Recommended Records

Use the latest record for revised metadata:

- `https://zenodo.org/records/15220963`

Use explicit older record IDs for MAG sequence archives:

- aquatic MAGs: `https://zenodo.org/records/14890002`
- terrestrial, engineered, and host-associated MAGs: `https://zenodo.org/records/14915155`

The concept DOI `https://doi.org/10.5281/zenodo.14889982` currently resolves to the latest Zenodo version, which is metadata-only. For whole-dataset downloads, do not use the concept DOI as the only source of file URLs.

## Direct URLs

```text
https://zenodo.org/records/15220963/files/binchicken_RBGs_metadata.tar.gz?download=1
https://zenodo.org/records/14890002/files/binchicken_RBGs_aquatic.tar.gz?download=1
https://zenodo.org/records/14915155/files/binchicken_RBGs_terrestrial_engineered_host.tar.gz?download=1
```

## Example Commands

Download revised metadata:

```bash
curl -L -o binchicken_RBGs_metadata.tar.gz \
  "https://zenodo.org/records/15220963/files/binchicken_RBGs_metadata.tar.gz?download=1"
```

Download MAG archives:

```bash
curl -L -o binchicken_RBGs_aquatic.tar.gz \
  "https://zenodo.org/records/14890002/files/binchicken_RBGs_aquatic.tar.gz?download=1"

curl -L -o binchicken_RBGs_terrestrial_engineered_host.tar.gz \
  "https://zenodo.org/records/14915155/files/binchicken_RBGs_terrestrial_engineered_host.tar.gz?download=1"
```

Verify checksums:

```bash
md5sum binchicken_RBGs_metadata.tar.gz
md5sum binchicken_RBGs_aquatic.tar.gz
md5sum binchicken_RBGs_terrestrial_engineered_host.tar.gz
```

Expected MD5 values:

```text
e48d69228091604aa1bdfda215bbe24f  binchicken_RBGs_metadata.tar.gz
88a477f645d857c12d160d262e1ca383  binchicken_RBGs_aquatic.tar.gz
2fcd0dd7c4359e542ddeccf291f3102c  binchicken_RBGs_terrestrial_engineered_host.tar.gz
```

## Sizes

- revised metadata: 961.9 MB
- aquatic MAGs: 33.8 GB
- terrestrial, engineered, and host-associated MAGs: 33.5 GB

Use a resumable downloader such as `wget -c`, `curl -C -`, or `aria2c` for the two MAG archives.
