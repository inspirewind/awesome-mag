# GROWdb Notes

Verified on 2026-05-09 against the Nature article, Zenodo data records `10.5281/zenodo.8173287` and `10.5281/zenodo.11193259`, NCBI BioProject `PRJNA946291`, the KBase GROW collection, GROWdb Explorer, and the linked GitHub/Zenodo code records.

GROWdb is the Genome Resolved Open Watersheds database from "A functional microbiome catalogue crowdsourced from North American rivers."

The resource is in scope for Awesome MAG because it provides a public river surface-water MAG catalogue with metagenomic, metatranscriptomic, functional annotation, ARG, geospatial, and interactive exploration layers.

## Resource Profile

Paper-reported scale:

- More than 100 teams collected 163 samples at 106 river sites.
- Sampling covered 90% of United States watersheds, reported as 21 HUC-2 watersheds.
- The project generated about 3.8 Tb of metagenomic and metatranscriptomic sequence data.
- The dataset links microbiome data to up to 287 geochemical and geospatial variables.
- The authors recovered 3,825 medium- and high-quality MAGs and dereplicated them to 2,093 MAGs at 99% identity.
- GROWdb MAGs cover 27 phyla and include article-reported novelty across 10 families and 128 genera.

The global freshwater comparison in the article used 9,798 MAGs and the latest Zenodo version provides a 5,986-representative dereplicated MAG archive plus an inventory workbook.

## Data Availability

The Nature data availability statement separates access routes:

- NCBI BioProject `PRJNA946291` hosts reads and MAGs.
- Zenodo concept DOI `10.5281/zenodo.8173286` hosts article data, including MAG annotations, phylogenetic trees, ARG files, and expression tables.
- NMDC, KBase, and GROWdb Explorer provide searchable or interactive access.

The Zenodo concept DOI has an important version split:

- Record `8173287` contains the core GROWdb v1 annotation, gene sequence, expression, ARG, and tree files.
- Record `11193259` is the latest version and contains only the global freshwater comparison files: `5986_99ID_drep_global.tar.gz` and `GlobalMAG_Inventory.xlsx`.

Use both records for a complete curation view.

## Curation Caveats

- Treat the paper's 2,093 MAG count as the dereplicated river surface-water catalogue count; the 5,986 archive in Zenodo latest is a global freshwater comparison file set, not the same count.
- NCBI is the authoritative route for raw reads and MAG assemblies. Use NCBI tools or accession manifests instead of scraping browser pages.
- Zenodo is the best route for direct file downloads and checksum verification.
- GROWdb Explorer is useful for browsing microbial, metabolite, and geospatial data together, but it should not be treated as a bulk-download source.
- The main data-generation GitHub repository did not expose a license via the GitHub API during curation; the geospatial/explorer repository reported MIT.

No source-specific automation script is needed for this resource.
