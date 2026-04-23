# SPIRE Notes

- SPIRE is hosted at `https://spire.embl.de/` and publishes its download landing page at `https://spire.embl.de/downloads`.
- Static files are served from `https://swifter.embl.de/~fullam/spire/`.
- The downloads page embeds a JavaScript `studyDownloadsData` object rather than loading the table from a separate JSON API.
- The embedded object currently contains 720 raw study blocks but 714 unique study names. The duplicate study blocks observed during curation were identical.
- Each page-listed study has four static archive URLs: assemblies, MAGs, gene-call FNA, and gene-call FAA.
- Dynamic profile links are not static files under `swifter.embl.de`; they are served by `https://spire.embl.de/download_motus3/<study>` and `https://spire.embl.de/download_spire_motus/<study>`.
- The `swifter.embl.de` host exposes Apache directory indexes, so additional files can be enumerated without browser automation.
- The `genes/` index is not shown on the downloads page and contains full-gene FASTA shards totaling multiple terabytes.
- `genes_per_study/`, `metadata/`, `representatives/`, and `spire_motus/` expose `.md5` sidecar files that are not all visible on the downloads page.
- Some extra per-study files exist in Apache indexes but are not listed by the official downloads page. Many of those extra tar files are only 10K and appear to be empty placeholder archives.
