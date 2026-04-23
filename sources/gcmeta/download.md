# gcMeta Download Notes

gcMeta exposes a public `/download` page at:

- `https://gcmeta.wdcm.org/download`

The page shows two tabs per catalogue row:

- `Total MAGs`
- `Species-level representative MAGs`

Each row carries three downloadable files for each tab:

- archive
- `.md5`
- metadata text

## What the Frontend Actually Does

The page is not backed by a static HTML table. Instead, the frontend loads rows from:

- `https://gcmeta.wdcm.org/gcmetaapi/down/list`

One important quirk: a bare request returns the first page in plain JSON, but once pagination parameters such as `pageNum` and `pageSize` are present, the site expects the browser's own encrypted request format. That makes direct HTTP pagination needlessly brittle for this repository.

gcMeta also exposes public enumeration APIs that are simpler and sufficient for deriving the archive URLs:

- `https://gcmeta.wdcm.org/gcmetaapi/catalogue/catalogueTree`
- `https://gcmeta.wdcm.org/gcmetaapi/home/catalogueNameList`

The actual file download is much simpler than the list request. The page opens:

```text
https://open.nmdc.cn/specail_data/gcmeta/Mags/Archive/<catalogueName-with-whitespace-replaced-by-underscores>/<row-file-name>
```

The frontend only rewrites whitespace in the catalogue name. It does not create a task or require login for this page.

## Automation Strategy

For this repository, the reliable automation flow is:

1. Read public catalogue names from `catalogueTree` and `catalogueNameList`.
2. Keep the `catalogueGroup` when it is present in the tree.
3. Build the catalogue directory by replacing whitespace in `catalogueName` with `_`.
4. Derive the public archive, `.md5`, and metadata filenames from the stable naming template.
5. Download the selected files directly from `open.nmdc.cn`.

The companion script for this source is:

- `scripts/gcmeta/download.py`
