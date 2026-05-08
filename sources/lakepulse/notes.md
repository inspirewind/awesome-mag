# LakePulse MAG Catalogue Notes

Verified on 2026-05-08 against the Nature Microbiology article page, Dryad dataset `10.5061/dryad.zkh1893fs`, ENA project records `PRJEB29238` and `PRJEB62834`, and the linked GitHub repository.

LakePulse is a continental-scale freshwater lake MAG resource from the article "A genome catalogue of lake bacterial diversity and its drivers at continental scale."

The resource is in scope for Awesome MAG because it provides a public bacterial MAG catalogue, co-assembly contigs, and companion annotations from Canadian lake surface-water metagenomes.

## Resource Profile

Paper-reported scale:

- 308 Canadian lakes across approximately 6.5 million km2
- 1,008 mostly novel bacterial genomospecies in the MAG catalogue
- MAG assemblage analyses linked to trophic state, watershed geomatics, soils, land use, agriculture, and human population density
- Supplementary Table 2 describes MAG quality, characteristics, taxonomy, associated filenames, marker-gene content, and TAD80 across 300 freshwater to oligosaline lakes

## Data Availability

The article data availability statement lists:

- raw metagenome reads under ENA study `PRJEB29238`
- metagenome co-assemblies and annotations under JGI GOLD study `Gs0136026`
- MAGs from co-assemblies and associated annotations in Dryad and under ENA study `PRJEB62834`
- scripts in `rebeccagarner/lakepulse_mags`

Dryad is the most direct bulk download route. It exposes 15 files in version 6:

- three MAG archives: contigs, amino-acid FASTA, and GFF
- eleven ecozone co-assembly contig FASTA gzip files
- one README

## Curation Caveats

- The Nature article abstract reports 308 lakes, while the supplementary table description says MAG details span 300 freshwater to oligosaline lakes. Keep those counts separate.
- ENA `PRJEB62834` is useful for accession-level MAG assembly records; Dryad is easier for bulk sequence and annotation retrieval.
- ENA reports 1,008 assembly rows for `PRJEB62834`, matching the reported catalogue scale. It also reports 1,019 analysis rows, which include co-assemblies in addition to MAG records.
- GOLD is an article-reported metadata and annotation entry point for the co-assemblies. The GOLD study URL returned a generic error page during curation, so do not treat GOLD as the primary bulk MAG download route unless a stable public file endpoint is identified.
- Dryad files are large. Use resumable downloads and verify SHA-256 checksums from the Dryad API.

No source-specific automation script is needed for this resource.
