# Glacier-fed Streams (GFS) MAGs Notes

Verified on 2026-05-08 against the Nature Microbiology article page, Zenodo record `10.5281/zenodo.13890040`, NCBI E-utilities for BioProject `PRJNA781406`, and the linked GitHub repositories.

Glacier-fed Streams (GFS) MAGs is the Vanishing Glaciers Project genome resource from "Mapping the metagenomic diversity of the multi-kingdom glacier-fed stream microbiome."

The resource is in scope for Awesome MAG because it provides a public MAG catalogue from a freshwater cryosphere environment, with raw sequencing data and MAG assemblies in NCBI plus reusable prokaryotic MAG sequence and annotation archives on Zenodo.

## Resource Profile

Paper-reported scale:

- 1,034 glacier-fed streams surveyed globally
- 156 sediment metagenomes from stream biofilms
- 9 mountain ranges
- 2,855 bacterial MAGs reported in the article abstract
- Multi-kingdom microbiome scope, covering prokaryotes, algae, fungi, and viruses

The BioProject is titled "Vanishing Glaciers Project" and its NCBI summary describes it as an investigation of microbiomes associated with glacier-fed streams around the world.

## Data Availability

The article data availability statement lists:

- raw sequencing data and MAGs under NCBI BioProject `PRJNA781406`
- processed MAG companion files under Zenodo DOI `10.5281/zenodo.13890040`
- Supplementary Tables on the Nature page
- figure source data files on the Nature page
- custom code in `michoug/VanishingGlacierMAGs` and `michoug/VanishingGlaciersRcode`

The Zenodo record contains three prokaryotic MAG archives:

- `ProkaryoticMAGsContig.tar`
- `ProkaryoticMAGsGff.tar`
- `ProkaryoticMAGsProtein.tar`

## Curation Caveats

- Use the Nature article as the descriptive landing page, NCBI BioProject `PRJNA781406` as the accession-level archive, and Zenodo record `13890040` as the direct file-download entry point for prokaryotic MAG companion archives.
- The Zenodo file set is explicitly prokaryotic by filename. Users interested in algae, fungi, or viruses should start from the NCBI archive and Nature supplementary tables rather than assuming those are included in the three Zenodo tar files.
- The NCBI project has more archive records than the 156 metagenomes reported in the paper abstract. Keep the article counts and NCBI search counts separate.
- Zenodo direct HEAD requests returned a 504 gateway response during curation, so checksum and size values were taken from the Zenodo record page.
- The article page itself is not recorded as the dataset license authority; the Zenodo record is CC BY 4.0, and the GitHub repositories have separate licensing status.

No source-specific automation script is needed for this resource.
