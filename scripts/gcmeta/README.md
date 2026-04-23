# gcMeta Automation

`download.py` enumerates public gcMeta catalogue names and derives their public archive URLs.

It supports:

- listing all public catalogue entries exposed by gcMeta's public enumeration APIs
- locating entries by exact catalogue group, exact catalogue name, or substring
- printing direct archive, `.md5`, and metadata URLs
- downloading `total` and `species` bundles from the same URLs used by the page
- skipping existing files, retrying failures, and best-effort resume from `.part` files

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
