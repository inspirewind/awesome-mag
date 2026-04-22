# MAGdb Notes

Verified on April 21, 2026 against the public website and frontend bundles.

## Summary

MAGdb is a MAG-focused portal hosted by Nanhu Laboratory:

- homepage: <https://magdb.nanhulab.ac.cn/>
- download page: <https://magdb.nanhulab.ac.cn/download>
- visible top-level download tabs: `Clinical`, `Environment`, `Animal`

## Publicly Exposed Client Details

The download page HTML exposes:

- `groupId = "68493799f13f19003f1e2dae"`
- `token = "Dyw639DrEpz3VdBS2wCshX"`

The frontend bundle uses the public token to fetch category workbooks:

- `MAG/Clinical.xlsx`
- `MAG/Environment.xlsx`
- `MAG/Animal.xlsx`

These workbooks are public and can be downloaded without authentication.

## Download URL Construction

The download UI assembles article archive URLs client-side with this pattern:

```text
/biobank/v1/getDirectoryByPath/620a0f2a40da9762bca509bc/group/preview/params%3D/HAMG_20240130/{index}_{Category}_result/{Title}/data.tar.gz
```

Example:

```text
https://magdb.nanhulab.ac.cn/biobank/v1/getDirectoryByPath/620a0f2a40da9762bca509bc/group/preview/params%3D/HAMG_20240130/1_Clinical_result/Bile%20salt%20hydrolase%20in%20non-enterotoxigenic%20Bacteroides%20potentiates%20colorectal%20cancer/data.tar.gz
```

One important implementation detail: the path must preserve the title string exactly as stored by MAGdb, including trailing spaces when they exist. For example, the environment title `Chemosynthetic and photosynthetic bacteria contribute differentially to primary production across a steep desert aridity gradient ` includes a trailing space in the workbook and therefore requires `%20` before `/data.tar.gz`.

## Authentication Behavior

- Unauthenticated requests to article archive URLs return a JSON error payload rather than a tarball.
- The observed unauthenticated response body was:

```json
{"statusCode":402,"errMsg":"没有登录"}
```

- The web UI enforces login before triggering the archive download.
- After a successful login, the frontend also posts the public `groupId` to `/biobank/v1/group`.

## Useful Source Fields

The `Clinical.xlsx` workbook header observed on April 21, 2026 was:

```text
Number
Year
Title
Short introduction
metagenome runs accession
high quality MAGs
Journal
DOI
```

These columns are enough to build a practical article index and derive the archive path from `Title`.
