# cFMD Download Notes

cFMD data are exposed through the GitHub repository:

```text
https://github.com/SegataLab/cFMD
```

Use GitHub for the lightweight inventory and metadata files. Use the upstream shell scripts for dataset-level MAG FASTA and functional-profile archives.

## Start With Metadata

| Asset | URL | Notes |
| --- | --- | --- |
| Dataset inventory | `https://raw.githubusercontent.com/SegataLab/cFMD/main/cFMD_datasets.tsv` | Current dataset list, cFMD version added, MetaRefSGB version, and publication references where available. |
| Sample metadata | `https://raw.githubusercontent.com/SegataLab/cFMD/main/cFMD_metadata.tsv` | Sample-level metadata, accessions, sequencing details, read/assembly statistics, and MAG counts. |
| Metadata rules | `https://raw.githubusercontent.com/SegataLab/cFMD/main/cFMD_metadata_rules.tsv` | Field-level rules for `cFMD_metadata.tsv`. |
| MAG list | `https://raw.githubusercontent.com/SegataLab/cFMD/main/cFMD_mags_list.tsv` | MAG IDs, source sample, SGB assignment, taxonomy, and quality statistics. |
| Per-dataset folders | `https://github.com/SegataLab/cFMD/tree/main/cFMD_data` | Dataset-specific metadata, MAG info, taxonomic profiles, and cheese metadata where available. |

## MAG Downloads

The upstream MAG downloader is:

```text
https://raw.githubusercontent.com/SegataLab/cFMD/refs/heads/main/download_mags.sh
```

Example:

```bash
wget "https://raw.githubusercontent.com/SegataLab/cFMD/refs/heads/main/download_mags.sh"
chmod +x download_mags.sh
./download_mags.sh LiZ_2019 YuY_2022
```

The script downloads `${DATASET}_mags.tar.gz` from Zenodo, extracts it into `${DATASET}_mags/`, then removes the tarball.

Known MAG archive records used by the current upstream script:

| Record | Scope | DOI |
| --- | --- | --- |
| `https://zenodo.org/records/17710367` | Initial cFMD MAG archives, patched for eukaryotic MAGs. | `10.5281/zenodo.17710367` |
| `https://zenodo.org/records/17709831` | cFMD v1.2.1 added datasets, patched for eukaryotic MAGs. | `10.5281/zenodo.17709831` |
| `https://zenodo.org/records/18456071` | cFMD v1.3.1 new cheese datasets. | `10.5281/zenodo.18456071` |

For v1.3.1, the checked MAG files are:

| File | Size | MD5 |
| --- | ---: | --- |
| `UNINA_SM_2025_mags.tar.gz` | 618.9 MB | `539dca2373e8daa7501169506b3a7782` |
| `YasirM_2023_mags.tar.gz` | 1.7 MB | `dc7a7ff0650ec5864fa8c9f133853b99` |

Direct URL pattern:

```text
https://zenodo.org/records/<record-id>/files/<DATASET>_mags.tar.gz?download=1
```

## Functional Profile Downloads

The upstream functional-profile downloader is:

```text
https://raw.githubusercontent.com/SegataLab/cFMD/refs/heads/main/download_functional_profiles.sh
```

Example:

```bash
wget "https://raw.githubusercontent.com/SegataLab/cFMD/refs/heads/main/download_functional_profiles.sh"
chmod +x download_functional_profiles.sh
./download_functional_profiles.sh LiZ_2019 YuY_2022
```

The script downloads `${DATASET}_functional_profiles.tar.gz` from Zenodo, extracts it into `${DATASET}_functional_profiles/`, then removes the tarball. The archives contain HUMAnN3 outputs: normalized UniRef90 gene families, pathway abundances, and pathway coverages.

Known functional-profile records used by the current upstream script:

| Record | Scope | DOI |
| --- | --- | --- |
| `https://zenodo.org/records/14871851` | Initial cFMD v1.0.0 functional profiles. | `10.5281/zenodo.14871851` |
| `https://zenodo.org/records/15609141` | cFMD v1.2.1 functional profiles for 26 added datasets. | `10.5281/zenodo.15609141` |
| `https://zenodo.org/records/18456455` | cFMD v1.3.1 new cheese dataset functional profiles. | `10.5281/zenodo.18456455` |

For v1.3.1, the checked functional-profile files are:

| File | Size | MD5 |
| --- | ---: | --- |
| `UNINA_SM_2025_functional_profiles.tar.gz` | 156.7 MB | `6967f597e7dd67a5974a17bcc1bfa58d` |
| `YasirM_2023_functional_profiles.tar.gz` | 655.7 KB | `d9875beefbc988da82a06af17b60d688` |

Direct URL pattern:

```text
https://zenodo.org/records/<record-id>/files/<DATASET>_functional_profiles.tar.gz?download=1
```

## Publication Data Bundle

The original Cell 2024 data bundle is still useful as a publication-era reference:

| Record | Files | DOI |
| --- | --- | --- |
| `https://zenodo.org/records/13285428` | `cFMD_humann.tar.gz` is 1.4 GB; `cFMD_mags.tar.gz` is 9.8 GB. | `10.5281/zenodo.13285428` |

## Practical Caveats

- Prefer reading `cFMD_datasets.tsv` and `cFMD_mags_list.tsv` before launching bulk downloads.
- The upstream scripts are dataset-name driven. They are useful for selected datasets, but they are not full manifest generators.
- Use resumable tools when downloading Zenodo archives manually.
- The cFMD GitHub repository is CC BY 4.0; keep original dataset and publication terms in mind when reusing data.
- The publication-era Cell 2024 Zenodo bundle and the current cFMD v1.3.1 GitHub release have different counts.
