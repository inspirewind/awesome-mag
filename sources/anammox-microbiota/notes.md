# Anammox Microbiota Catalog Notes

Verified on 2026-05-09 against the Figshare landing page, DataCite DOI metadata for `10.6084/m9.figshare.25476583`, PubMed record `39236503`, and Crossref metadata for `10.1016/j.watres.2024.122356`.

This resource is in scope for Awesome MAG because the associated Water Research article reports a genome-centric anammox microbiota catalog built from thousands of MAGs, with the Figshare dataset providing the companion gene and genome catalog files.

## Resource Profile

Reported scale:

- 236 metagenomes in the overall Figshare-described catalog.
- 193 metagenomic samples from 37 previous studies were used to construct the genome catalog, with 43 additional public samples used after catalog construction.
- 7,474 MAGs were used as the raw genome set.
- 1,768 strain-level MAGs are listed by the article's data availability statement as part of the Figshare data package.
- 1,376 species-level genomes form the main non-redundant genome catalog in the Water Research article title and abstract.
- Average coverage of anammox microbiota was reported as 92.40%.
- 64 core genera and 44 core species were identified, accounting for about 64.25% and 43.97% of anammox microbiota, respectively.
- The sample/system metadata described in the article covers 110 individual anammox systems, including 82 laboratory systems, 28 engineering systems, 80 coupling systems, and 30 single systems.

## Data Availability

The Figshare record is the primary landing page for the dataset:

- `https://figshare.com/articles/dataset/A_comprehensive_catalog_encompassing_genes_and_genomes_reveals_the_core_community_and_functional_diversity_in_anammox_microbiota/25476583`
- DOI: `10.6084/m9.figshare.25476583`

DataCite metadata reports:

- creator: Depeng Wang
- created and updated: 2024-03-27
- license: Creative Commons Attribution 4.0 International
- size: 8,120,727,476 bytes
- description: global gene and genome catalogs of anammox microbiota based on 236 metagenomes

The associated article is:

- "A comprehensive catalog encompassing 1376 species-level genomes reveals the core community and functional diversity of anammox microbiota"
- Water Research, volume 266, article 122356
- DOI: `10.1016/j.watres.2024.122356`
- PubMed: `39236503`

## Curation Caveats

- The Figshare title omits the `1376 species-level genomes` phrase used in the final article title. Use the Water Research title for publication metadata and the Figshare title for the data landing page.
- The Figshare dataset describes 236 metagenomes; the article abstract reports 7,474 MAGs and 1,376 candidate species/species-level genomes, while the data availability statement describes raw files containing the gene catalog and 1,768 strain-level MAGs.
- The article states that BioProject accessions for newly generated raw metagenomes are listed in Table S1. This entry records the Figshare catalog deposit rather than trying to reconstruct all raw-read accessions from supplementary tables.
- Command-line checks against `api.figshare.com` and `figshare.com/ndownloader` were blocked or challenged during curation. Do not build automation that attempts to bypass Figshare's WAF behavior.
- A source-specific download script is not needed unless a stable Figshare file-level API response is available. Browser download from the Figshare landing page is the most reliable documented route for now.
