# gcMeta Automation

`download.py` enumerates public gcMeta catalogue names and derives their public archive URLs.

It supports:

- listing all public catalogue entries exposed by gcMeta's public enumeration APIs
- locating entries by exact catalogue group, exact catalogue name, or substring
- printing direct archive, `.md5`, and metadata URLs
- downloading `total` and `species` bundles from the same URLs used by the page
- skipping existing files, retrying failures, and resuming `.part` files with Python, `curl`, `wget`, or `aria2c`

## Requirements

- Python 3.9 or newer
- No third-party Python dependencies

## How gcMeta Works

gcMeta exposes public catalogue enumeration endpoints that are enough to derive the direct archive URLs without reproducing the site's encrypted pagination flow:

- `https://gcmeta.wdcm.org/gcmetaapi/catalogue/catalogueTree`
- `https://gcmeta.wdcm.org/gcmetaapi/home/catalogueNameList`

Once a catalogue name is known, the actual file URL is public and direct:

```text
https://open.nmdc.cn/specail_data/gcmeta/Mags/Archive/<catalogue-name-with-spaces-replaced-by-underscores>/<file-name>
```

The script derives filenames using the same stable naming convention visible on the public download page:

- `*_all_MAGs.tar.gz`
- `*_all_MAGs.tar.gz.md5`
- `*_all_MAGs.metainfo.txt`
- `*_species-level_representative_MAGs.tar.gz`
- `*_species-level_representative_MAGs.tar.gz.md5`
- `*_species-level_representative_MAGs.metainfo.txt`

## Commands and Parameters

The script has three subcommands:

- `list`: enumerate catalogue entries and show the derived archive names.
- `url`: print direct URLs without downloading files.
- `download`: download selected files from the public `open.nmdc.cn` archive host.

Common selection parameters:

- `--catalogue NAME`: exact catalogue-name match, for example `Acid Habitat`.
- `--group NAME`: exact catalogue-group match, for example `Large Livestock`.
- `--contains TEXT`: substring match against catalogue group or catalogue name.
- `--all-matches`: allow multiple matches for `url` or `download`; without this flag, those commands require a single resolved entry.
- `--json`: emit JSON output for `list` and `url`, useful for piping into other tools.

Asset selection parameters:

- `--bundle total`: select only `*_all_MAGs.tar.gz`; this is the default.
- `--bundle species`: select only `*_species-level_representative_MAGs.tar.gz`.
- `--bundle both`: select both `total` and `species` bundles.
- `--include-md5`: also include the `.md5` sidecar file.
- `--include-metadata`: also include the `.metainfo.txt` metadata file.

Download parameters:

- `--output-dir DIR`: write files under this directory. The default is `downloads/gcmeta`.
- `--skip-existing`: skip a target file when it already exists and is non-empty.
- `--resume`: resume from an existing `.part` file when the selected downloader supports it.
- `--downloader python`: use the built-in Python downloader. This is the default and is dependency-free.
- `--downloader curl`: use `curl -C -` when `--resume` is enabled.
- `--downloader wget`: use `wget --continue` when `--resume` is enabled.
- `--downloader aria2c`: use `aria2c --continue=true` when `--resume` is enabled. The script keeps aria2c conservative with one connection per file.
- `--retries N`: retry each failed file `N` additional times.
- `--continue-on-error`: continue downloading other files after one file fails.
- `--no-progress`: disable per-file `START` and byte-count progress messages.

Download progress is shown on stderr so stdout remains usable for final status lines or shell redirection. The script reports catalogue resolution, selected entry count, a `START` line for each file, periodic byte progress, and then the existing `OK`, `SKIP`, or `FAIL` status.

The script always downloads into `<target>.part` first and only moves it into the final filename after a successful transfer. For robust resume on large archives, prefer `--resume --downloader curl`, `--resume --downloader wget`, or `--resume --downloader aria2c`.

## Examples

List all catalogue entries:

```bash
python3 scripts/gcmeta/download.py list
```

Find entries by substring:

```bash
python3 scripts/gcmeta/download.py list --contains "Acid Habitat"
```

Print the direct `total` archive URL for one exact catalogue:

```bash
python3 scripts/gcmeta/download.py url \
  --catalogue "Acid Habitat" \
  --bundle total
```

Print archive, `.md5`, and metadata URLs for every matching entry:

```bash
python3 scripts/gcmeta/download.py url \
  --contains "Gut" \
  --bundle both \
  --include-md5 \
  --include-metadata \
  --all-matches
```

Download one `species` bundle:

```bash
python3 scripts/gcmeta/download.py download \
  --catalogue "Acid Habitat" \
  --bundle species
```

Download both bundle types plus sidecar files for every match:

```bash
python3 scripts/gcmeta/download.py download \
  --group "Large Livestock" \
  --bundle both \
  --include-md5 \
  --include-metadata \
  --all-matches \
  --skip-existing \
  --resume \
  --retries 3 \
  --continue-on-error
```

Download only `*_all_MAGs.tar.gz` for every catalogue:

```bash
python3 scripts/gcmeta/download.py download \
  --bundle total \
  --all-matches \
  --skip-existing \
  --continue-on-error
```

Resume all `*_all_MAGs.tar.gz` downloads with `aria2c`:

```bash
python3 scripts/gcmeta/download.py download \
  --bundle total \
  --all-matches \
  --skip-existing \
  --continue-on-error \
  --resume \
  --downloader aria2c \
  --output-dir /mnt/HC5501/gcmeta/
```

Resume with `curl` instead:

```bash
python3 scripts/gcmeta/download.py download \
  --bundle total \
  --all-matches \
  --skip-existing \
  --continue-on-error \
  --resume \
  --downloader curl \
  --output-dir /mnt/HC5501/gcmeta/
```

Write downloads into a custom directory:

```bash
python3 scripts/gcmeta/download.py download \
  --catalogue "Acid Habitat" \
  --bundle total \
  --output-dir ./downloads/gcmeta
```

## Notes

- The script prefers public enumeration APIs over replaying gcMeta's encrypted pagination requests.
- The download files themselves are public once the catalogue name has been resolved.
- `--bundle total` corresponds to the `Total MAGs` tab.
- `--bundle species` corresponds to the `Species-level representative MAGs` tab.
- `.md5` and metadata files are optional sidecars; add them with `--include-md5` and `--include-metadata`.
- Output files are stored under `<output-dir>/<bundle>/<upstream-file-name>`.
