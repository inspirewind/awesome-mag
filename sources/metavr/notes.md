# Meta-virus Resource Notes

- MetaVR is the successor to IMG/VR and is associated with the Nucleic Acids Research article "Meta-virus resource (MetaVR): expanding the frontiers of viral diversity with 24 million uncultivated virus genomes."
- The paper describes 24,435,662 uncultivated virus genomes (UViGs) organized into 12,705,385 vOTUs, plus 5,625 RefSeq viral genomes for context.
- Source data span 37,961 metagenomes, 8,694 metatranscriptomes, 99,377 isolate genomes, 1,452 SAGs, and 9,704 MAGs; the Downloads page lists a 162,534-row source dataset metadata file.
- MetaVR classifies UViGs as high-confidence or low-confidence. The paper reports 11,192,611 high-confidence UViGs and 13,243,051 low-confidence UViGs.
- Taxonomy was assigned for 23,668,185 UViGs and 12,271,957 vOTUs using ICTV, geNomad, and CAT/BAT.
- Host assignments are available for 7,833,811 UViGs and 4,321,235 vOTUs. The iPHoP-specific download covers 7,049,110 UViGs and 4,173,478 vOTUs.
- Protein data include 42,390,306 protein clusters. The Downloads page provides archives for representative protein-cluster MSAs and AlphaFold3 3D models for clusters with at least 100 members.
- The official entry points are the web portal, Downloads page, and API documentation:
  - `https://www.meta-virome.org/`
  - `https://www.meta-virome.org/Downloads`
  - `https://meta-virome.org/api/docs`
- The bulk URLs are not currently wget/curl-ready from the curation environment. A user-tested `wget -c` request for `IMGVR5_UViG.fna.gz` returned `403 Forbidden` on 2026-05-08, consistent with Cloudflare bot protection.
- Plain `curl` requests to documented API endpoints also returned Cloudflare challenge HTML rather than JSON during curation, so the API should not be treated as command-line reproducible without a provider-supported access method.
- This is a viral genome and virome companion resource rather than a bacterial or archaeal MAG catalogue.

## Data Layout

| File | Contents |
| --- | --- |
| `IMGVR5_UViG.fna.gz` | Nucleotide FASTA for all MetaVR UViGs. |
| `IMGVR5_UViG.tsv.gz` | UViG metadata table. |
| `IMGVR5_UViG.faa.gz` | Predicted protein FASTA for MetaVR UViGs. |
| `IMGVR5_PC_MSAs.tar.zst` | Representative protein-cluster multiple sequence alignments for clusters with at least 100 members. |
| `IMGVR5_PC_3Dmodels.tar.gz` | AlphaFold3-predicted 3D protein structures for representative protein clusters with at least 100 members. |
| `MetaVR_iPHoP_results.tsv.gz` | iPHoP host-classification results. |
| `Source_dataset_metadata.tsv.gz` | Source dataset metadata for metagenomes, metatranscriptomes, isolate genomes, SAGs, MAGs, and RefSeq genomes. |

## Checked Files

| File | Size | Last modified | Notes |
| --- | ---: | --- | --- |
| `IMGVR5_UViG.fna.gz` | ~77G | not captured | Main UViG nucleotide FASTA. |
| `IMGVR5_UViG.tsv.gz` | ~846M | not captured | Main UViG metadata table; 24,435,662 rows reported on the Downloads page. |
| `IMGVR5_UViG.faa.gz` | ~48.7G | not captured | Predicted protein FASTA. |
| `IMGVR5_PC_MSAs.tar.zst` | ~13.8G | not captured | Listed by the Downloads page, but the static URL returned 404 during curation on 2026-05-08; verify before bulk transfer. |
| `IMGVR5_PC_3Dmodels.tar.gz` | ~29.6G | not captured | AlphaFold3 protein-structure archive. |
| `MetaVR_iPHoP_results.tsv.gz` | ~921M | not captured | iPHoP host predictions. |
| `Source_dataset_metadata.tsv.gz` | ~22M | not captured | Source metadata; 162,534 rows reported on the Downloads page. |

## Curation Caveats

- The MetaVR site is protected by Cloudflare. Browser access to the Downloads page worked during curation, but CLI `HEAD` requests from the curation environment returned a Cloudflare challenge, `wget -c` against the main UViG FASTA returned `403 Forbidden`, and plain `curl` requests against documented API endpoints returned challenge HTML.
- The Downloads page did not list checksum files during curation.
- For reproducible bulk acquisition, prefer an official mirror, maintainer-provided transfer instructions, or a provider-supported endpoint rather than trying to evade the Cloudflare challenge.
- Treat low-confidence UViGs as discovery candidates with higher false-positive risk.
- The database-generation code is linked from the paper at `https://code.jgi.doe.gov/antoniop.camargo/metavr/`.

Checked on 2026-05-08.
