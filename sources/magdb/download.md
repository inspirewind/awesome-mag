# MAGdb Download Notes

## Website

- Homepage: <https://magdb.nanhulab.ac.cn/>
- Download page: <https://magdb.nanhulab.ac.cn/download>

## What Is Public

MAGdb publishes three public category workbooks that can be fetched directly with the token exposed in the download page:

- `Clinical.xlsx`
- `Environment.xlsx`
- `Animal.xlsx`

Those workbooks contain the article-level metadata used by the website download UI.

## What Is Not Public

The article archive links follow a predictable URL pattern, but the archive endpoint still expects an authenticated session. Without login, the endpoint returns a JSON login error instead of `data.tar.gz`.

## Automation Strategy

The script in `scripts/magdb/download.py` automates the site in two stages:

1. Fetch the public workbook for a selected category
2. Parse article metadata and construct the exact archive URL
3. Authenticate by reusing a browser `EGG_SESS` cookie
4. Download the selected `data.tar.gz` archive with the authenticated session

## Recommended Usage

- Use `list` when you want to inspect the current article inventory.
- Use `url` when you only need the generated archive URL.
- Use `download` when you have a fresh browser session cookie and want the tarball itself.
- For large batches, prefer `--skip-existing --resume --retries 3 --continue-on-error`.

See `scripts/magdb/README.md` for concrete command examples.
