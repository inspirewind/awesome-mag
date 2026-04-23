# SPIRE URL Helper

`download.py` resolves SPIRE file URLs and prints them for external download tools. It does not download data.

It supports:

- listing the 714 unique studies exposed by `studyDownloadsData`
- searching studies by exact name or substring
- printing per-study archive URLs for assemblies, MAGs, nucleotide gene calls, and protein gene calls
- optionally printing dynamic profile endpoints for mOTUs3 and SPIRE mOTUs TSV files
- enumerating file URLs from the public Apache indexes under `https://swifter.embl.de/~fullam/spire/`

## Requirements

- Python 3.9 or newer
- No third-party Python dependencies

## Commands

- `list`: list SPIRE study names.
- `url`: print URLs for selected studies.
- `manifest`: enumerate URLs from SPIRE Apache index pages.

Study asset choices:

- `assemblies`: `compiled/*_assemblies.tar`
- `mags`: `compiled/*_MAGs.tar`
- `fna`: `genes_per_study/*_genecalls_fna.tar`
- `faa`: `genes_per_study/*_genecalls_faa.tar`
- `all-static`: all four static per-study archive types, used by default
- `all`: all static assets plus dynamic mOTUs profile endpoints

Manifest scopes:

- `all-spire`: known file indexes under `https://swifter.embl.de/~fullam/spire/`
- `metadata`
- `metadata-old`
- `study-compiled`
- `study-genes`
- `representatives`
- `motus-db`
- `full-genes`
- `root`
- `marker-genes`: page-linked marker genes outside the `/spire/` directory

## Examples

List ocean-related studies:

```bash
python3 scripts/spire/download.py list --contains ocean
```

Print all static archive URLs for ocean-related studies, one URL per line:

```bash
python3 scripts/spire/download.py url --contains ocean --plain
```

Write URLs for use with `wget`:

```bash
python3 scripts/spire/download.py url --contains ocean --plain > spire-ocean.urls
wget -i spire-ocean.urls
```

Write URLs for use with `aria2c`:

```bash
python3 scripts/spire/download.py url --contains ocean --aria2 > spire-ocean.aria2.txt
aria2c -i spire-ocean.aria2.txt
```

Print only MAG archive URLs for one study:

```bash
python3 scripts/spire/download.py url \
  --study Zhao_2015_lake \
  --asset mags \
  --plain
```

Print static archives plus mOTUs profile endpoints:

```bash
python3 scripts/spire/download.py url \
  --study Zhao_2015_lake \
  --asset all \
  --json
```

Print all full-gene shard URLs from the hidden `genes/` index:

```bash
python3 scripts/spire/download.py manifest --scope full-genes --plain
```

Print all known `/spire/` index file URLs, including `.md5` sidecars:

```bash
python3 scripts/spire/download.py manifest \
  --scope all-spire \
  --include-md5-sidecars \
  --plain
```

## Notes

- The `url` command uses the official downloads page as the authority for the 714 public studies.
- The `manifest` command reads Apache index pages and can expose files not listed on the downloads page.
- Dynamic profile endpoints live under `https://spire.embl.de/download_*`, not under the `swifter.embl.de` file host.
- Use `--downloads-html PATH` with `list` or `url` to parse a cached copy of the downloads page.
