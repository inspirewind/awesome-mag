# SPIRE Download Notes

SPIRE exposes a public downloads page:

- `https://spire.embl.de/downloads`

The static file host is:

- `https://swifter.embl.de/~fullam/spire/`

## Download Strategy

This repository does not use Python to download SPIRE data. The helper script only resolves and prints URLs so users can download with their preferred tools, such as `wget`, `curl`, `aria2c`, or an HPC transfer workflow.

For per-study static archives, use the official downloads page as the authoritative study list. It exposes 714 unique study names and four static archive classes per study:

- assemblies: `compiled/*_assemblies.tar`
- MAGs: `compiled/*_MAGs.tar`
- nucleotide gene calls: `genes_per_study/*_genecalls_fna.tar`
- protein gene calls: `genes_per_study/*_genecalls_faa.tar`

## Query Examples

Find ocean-related studies:

```bash
python3 scripts/spire/download.py list --contains ocean
```

Print all static URLs for those studies:

```bash
python3 scripts/spire/download.py url --contains ocean --plain
```

Use the URL list with `wget`:

```bash
python3 scripts/spire/download.py url --contains ocean --plain > spire-ocean.urls
wget -i spire-ocean.urls
```

Use the URL list with `aria2c`:

```bash
python3 scripts/spire/download.py url --contains ocean --aria2 > spire-ocean.aria2.txt
aria2c -i spire-ocean.aria2.txt
```

Print only MAG archive URLs:

```bash
python3 scripts/spire/download.py url --contains ocean --asset mags --plain
```

Print full-gene shard URLs from the hidden `genes/` directory:

```bash
python3 scripts/spire/download.py manifest --scope full-genes --plain
```

Enumerate all known files under `https://swifter.embl.de/~fullam/spire/`, including `.md5` sidecars:

```bash
python3 scripts/spire/download.py manifest \
  --scope all-spire \
  --include-md5-sidecars \
  --plain
```

## Caveats

- Dynamic profile TSV links live on `spire.embl.de`, not on the `swifter.embl.de` static file host.
- Use `--asset all` to include those profile endpoints in per-study URL output.
- The Apache indexes expose some page-hidden per-study tar files. Several are 10K placeholder archives and should not be treated as normal study packages without inspection.
- The `manifest` command intentionally enumerates index pages; it may include files not shown in the official downloads page.
