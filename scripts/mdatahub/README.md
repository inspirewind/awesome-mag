# Microbiome Datahub Helper

`download.py` lists and downloads Microbiome Datahub bulk, Zenodo, and targeted API assets without a browser.

It supports:

- listing the officially documented NIG bulk sequence files
- printing current Zenodo record file URLs, with optional live refresh through the Zenodo API
- constructing targeted API URLs for project metadata, genome/CDS/protein sequence ZIPs, and KEGG module JSON
- downloading selected assets with the Python standard library, or delegating to `curl`, `wget`, or `aria2c`

## Requirements

- Python 3.9 or newer
- No third-party Python dependencies

## Commands

- `list`: list known bulk and Zenodo files.
- `url`: print selected URLs.
- `download`: download selected files.

Static groups:

- `bulk`: NIG full-database sequence files.
- `zenodo`: metadata, Bac2Feature, module matrix, and module labels from Zenodo.
- `all`: both groups.

API assets:

- `project-metadata`
- `genome-metadata`
- `sequence-genome`
- `sequence-cds`
- `sequence-protein`
- `kegg-modules`

## Examples

List only NIG bulk files:

```bash
python3 scripts/mdatahub/download.py list --group bulk
```

Print all bulk URLs for `wget`:

```bash
python3 scripts/mdatahub/download.py url --group bulk --plain > mdatahub-bulk.urls
wget -c -i mdatahub-bulk.urls
```

Print current Zenodo URLs:

```bash
python3 scripts/mdatahub/download.py url --group zenodo --plain
```

Refresh Zenodo file metadata from the live API:

```bash
python3 scripts/mdatahub/download.py url --group zenodo --refresh-zenodo --json
```

Download Zenodo files:

```bash
python3 scripts/mdatahub/download.py download \
  --group zenodo \
  --output-dir /data/mdatahub
```

Use `aria2c` for large bulk files:

```bash
python3 scripts/mdatahub/download.py download \
  --group bulk \
  --downloader aria2c \
  --resume \
  --skip-existing \
  --continue-on-error \
  --output-dir /data/mdatahub
```

Print a genome sequence ZIP API URL:

```bash
python3 scripts/mdatahub/download.py url \
  --asset sequence-genome \
  --ids GCA_000208265.2,GCA_001735855.1 \
  --plain
```

Download KEGG module JSON for one genome:

```bash
python3 scripts/mdatahub/download.py download \
  --asset kegg-modules \
  --ids GCA_029762515.1 \
  --output-dir /data/mdatahub
```

## Notes

- Bulk URLs are taken from the official Microbiome Datahub documentation.
- The NIG bulk host was not reachable from the curation network on 2026-04-25; verify reachability from your own server before launching large downloads.
- The `genome-metadata` API is documented upstream, but tested examples returned HTTP 500 during curation on 2026-04-25.
