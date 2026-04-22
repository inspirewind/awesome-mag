# MAGdb Automation

`download.py` automates the first MAGdb workflow in this repository.

It supports:

- listing article metadata from the public category workbooks
- locating entries by exact title or substring
- printing the generated `data.tar.gz` URL
- downloading one or more article archives through browser cookie reuse
- skipping already-downloaded files, retrying failures, and best-effort resume from `.part` files

## Requirements

- Python 3.9 or newer
- No third-party Python dependencies
- A MAGdb account only if you want to download protected archives

## Examples

List all clinical entries:

```bash
python3 scripts/magdb/download.py list --category clinical
```

Find matching entries by title fragment:

```bash
python3 scripts/magdb/download.py list --category clinical --contains "Bile salt hydrolase"
```

Print the generated archive URL without downloading:

```bash
python3 scripts/magdb/download.py url --category clinical --contains "Bile salt hydrolase"
```

Download using an authenticated browser session cookie without calling the login endpoint:

```bash
python3 scripts/magdb/download.py download \
  --category clinical \
  --contains "Bile salt hydrolase" \
  --cookie-prompt
```

Reuse a cookie stored in an environment variable so it does not end up in shell history:

```bash
export MAGDB_COOKIE='EGG_SESS=...'
python3 scripts/magdb/download.py download \
  --category all \
  --all-matches \
  --cookie-env MAGDB_COOKIE
```

Download every match returned by a substring query:

```bash
python3 scripts/magdb/download.py download \
  --category clinical \
  --contains "colorectal cancer" \
  --all-matches \
  --cookie-prompt
```

Resume an interrupted batch and skip files that already finished:

```bash
python3 scripts/magdb/download.py download \
  --category all \
  --all-matches \
  --cookie-prompt \
  --skip-existing \
  --resume \
  --retries 3 \
  --continue-on-error
```

Write downloads into a custom directory:

```bash
python3 scripts/magdb/download.py download \
  --category clinical \
  --contains "Bile salt hydrolase" \
  --cookie-prompt \
  --output-dir ./downloads/magdb
```

## Notes

- `list` and `url` only need the public workbook endpoints.
- `download` needs an authenticated MAGdb session supplied through one of the cookie options.
- `--cookie-prompt` and `--cookie-env` are safer than passing a long cookie directly on the command line.
- `--skip-existing` skips non-empty completed files at the final destination path.
- `--resume` uses a sibling `.part` file and sends a `Range` request when retrying an interrupted download.
- If the server ignores range requests, `--resume` falls back to re-downloading from the start.
- `--continue-on-error` keeps the batch moving and reports failures at the end.
- Output files are stored under `<output-dir>/<category>/<sanitized-title>.tar.gz`.
