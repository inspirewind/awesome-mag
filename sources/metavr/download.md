# Meta-virus Resource Download Notes

MetaVR bulk assets are listed on the official Downloads page:

- Portal: `https://www.meta-virome.org/`
- Downloads page: `https://www.meta-virome.org/Downloads`
- API documentation: `https://meta-virome.org/api/docs`
- Database-generation code: `https://code.jgi.doe.gov/antoniop.camargo/metavr/`

The Downloads page exposes bulk-file links, but these URLs are not currently reproducible with plain command-line downloaders. During curation, CLI `HEAD` requests returned a Cloudflare challenge, and a user-tested `wget -c` request for `IMGVR5_UViG.fna.gz` returned `403 Forbidden` on 2026-05-08. Plain `curl` requests to documented API endpoints also returned Cloudflare challenge HTML rather than JSON.

For reproducible workflows, treat MetaVR as browser-visible but not wget/curl-ready for API or bulk files unless the provider publishes an official mirror, allowlists the client environment, or changes the Cloudflare policy.

## Core Files

| Asset | File | Size | Notes |
| --- | --- | ---: | --- |
| UViG genomes | `IMGVR5_UViG.fna.gz` | ~77G | Nucleotide FASTA for 24,435,662 MetaVR UViGs. |
| UViG metadata | `IMGVR5_UViG.tsv.gz` | ~846M | Metadata table for 24,435,662 UViGs. |
| UViG proteins | `IMGVR5_UViG.faa.gz` | ~48.7G | Predicted protein FASTA. |
| Protein-cluster MSAs | `IMGVR5_PC_MSAs.tar.zst` | ~13.8G | Representative protein-cluster MSAs for clusters with at least 100 members; verify first because the static URL returned 404 during curation on 2026-05-08. |
| Protein-cluster 3D models | `IMGVR5_PC_3Dmodels.tar.gz` | ~29.6G | AlphaFold3-predicted 3D structures for representative protein clusters with at least 100 members. |
| iPHoP results | `MetaVR_iPHoP_results.tsv.gz` | ~921M | Host-classification results for MetaVR UViGs. |
| Source dataset metadata | `Source_dataset_metadata.tsv.gz` | ~22M | Metadata for 162,534 source datasets listed on the Downloads page. |

## Automation Status

Plain `wget`/`curl` API and bulk-download requests are blocked by Cloudflare as of 2026-05-08. Do not use a source-specific script that attempts to bypass the challenge. Practical options are:

- Download through the official browser flow if the site permits it.
- Use the documented MetaVR API only from environments or clients that the provider supports.
- Ask the MetaVR maintainers for a provider-supported bulk mirror, Globus endpoint, FTP/HTTPS host, signed URL, or allowlisted transfer method.
- Re-check the listed URLs later in case the provider changes the Cloudflare policy.

## Inspection Commands

Check compressed metadata and headers:

```bash
gzip -t IMGVR5_UViG.tsv.gz
zcat IMGVR5_UViG.tsv.gz | head -n 2
zcat Source_dataset_metadata.tsv.gz | head -n 2
zcat MetaVR_iPHoP_results.tsv.gz | head -n 2
```

Inspect sequence headers and archives:

```bash
zcat IMGVR5_UViG.fna.gz | head
zcat IMGVR5_UViG.faa.gz | head
tar --zstd -tf IMGVR5_PC_MSAs.tar.zst | head
tar -tzf IMGVR5_PC_3Dmodels.tar.gz | head
```

## Verification and Caveats

- The MetaVR site is Cloudflare-protected. If automated `curl` header checks or downloads receive an HTML challenge page, retry from a browser session or an environment accepted by the site.
- The Downloads page did not show MD5 or SHA checksum files during curation.
- The Protein Cluster MSA archive was listed on the Downloads page, but the static URL returned 404 during curation on 2026-05-08.
- The largest assets are tens of gigabytes compressed; stage metadata and host-prediction tables before scheduling sequence and structure downloads.
- This resource is a viral/virome catalogue, not a prokaryotic MAG catalogue. It is included here as a multi-biome companion resource.

Checked on 2026-05-08.
