# Anammox Microbiota Catalog Download Notes

Primary links:

- Figshare landing page: `https://figshare.com/articles/dataset/A_comprehensive_catalog_encompassing_genes_and_genomes_reveals_the_core_community_and_functional_diversity_in_anammox_microbiota/25476583`
- Figshare DOI: `https://doi.org/10.6084/m9.figshare.25476583`
- DataCite DOI metadata: `https://api.datacite.org/dois/10.6084/m9.figshare.25476583`
- Download-all route: `https://figshare.com/ndownloader/articles/25476583/versions/1`
- Article: `https://www.sciencedirect.com/science/article/pii/S0043135424012557`
- Article DOI: `https://doi.org/10.1016/j.watres.2024.122356`
- PubMed: `https://pubmed.ncbi.nlm.nih.gov/39236503/`

## Figshare Dataset

The Figshare/DataCite record describes the dataset as the global gene and genome catalogs of anammox microbiota based on 236 metagenomes.

Observed metadata:

| Field | Value |
| --- | --- |
| DOI | `10.6084/m9.figshare.25476583` |
| Creator | Depeng Wang |
| Created | 2024-03-27 |
| Updated | 2024-03-27 |
| License | CC BY 4.0 |
| DataCite size | 8,120,727,476 bytes |

The practical manual route is:

1. Open the Figshare landing page in a browser.
2. Use the Figshare download button or the download-all route for article `25476583`, version `1`.
3. Record the downloaded archive name and checksum locally, because no checksum file was visible from the metadata endpoints checked during curation.

## Command-Line Caveat

The likely download-all URL is:

```text
https://figshare.com/ndownloader/articles/25476583/versions/1
```

During curation, command-line access was not reproducible from this environment:

| Endpoint | Observed behavior |
| --- | --- |
| `https://api.figshare.com/v2/articles/25476583` | HTTP 403 |
| `https://figshare.com/ndownloader/articles/25476583/versions/1` | HTTP 202 with `x-amzn-waf-action: challenge` |
| `https://ndownloader.figshare.com/articles/25476583/versions/1` | HTTP 502 |

Because of that, do not add a source-specific downloader that scrapes or bypasses Figshare protections. Browser-mediated download is the documented route for now.

## Article Context

The associated Water Research article reports:

| Metric | Value |
| --- | ---: |
| Total MAGs used for catalog construction | 7,474 |
| Strain-level MAGs in the Figshare data package | 1,768 |
| Species-level genomes in the article catalog | 1,376 |
| Average anammox microbiota coverage | 92.40% |
| Core genera | 64 |
| Core species | 44 |

The article's data availability statement says the raw files containing sequences of the gene catalog and 1,768 strain-level MAGs are stored in the Figshare link above. It also says BioProject accessions for newly generated raw metagenomes are listed in Table S1.

## Automation Decision

A source-specific `download.py` is not needed at this stage.

If automation is added later, it should:

- use Figshare's official API only when it returns stable file metadata without a WAF challenge;
- emit a manifest of file names, sizes, checksums if available, and download URLs;
- avoid downloading the full 8.12 GB archive by default;
- avoid attempting to bypass browser challenges.

## Verification

Checked on 2026-05-09:

- DataCite DOI metadata for `10.6084/m9.figshare.25476583` returned CC BY 4.0 licensing, 2024-03-27 create/update dates, and an 8,120,727,476 byte size.
- PubMed record `39236503` and Crossref metadata matched the Water Research article DOI, title, volume 266, article number 122356, online date 2024-08-29, and print date 2024-11-15.
- Command-line Figshare API/downloader access was blocked or challenged as described above.
