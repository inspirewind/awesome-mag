# Human Gut Archaeome Notes

Verified on 2026-05-06 against the Nature Microbiology article page, the EBI genome sets index, and the linked Springer supplementary files.

Human Gut Archaeome is the genome catalogue from "A catalogue of 1,167 genomes from the human gut archaeome" by Chibani, Mahnert, Borrel, Almeida, Werner, Brugere, Gribaldo, Finn, Schmitz, and Moissl-Eichinger.

The resource is in scope for Awesome MAG because it provides a public, reusable archaeal genome catalogue derived from human gastrointestinal metagenomic resources and isolates, with the recovered genomes distributed as a bulk archive.

## Resource Profile

Paper-reported scale:

- 1,167 nonchimeric and nonredundant archaeal genomes from human gastrointestinal samples
- 608 high-quality genomes
- Samples spanning 24 countries and rural and urban populations
- 28,581 protein cluster representatives after clustering predicted genes across the catalogue
- Previously undescribed taxa reported at 3 genera, 15 species, and 52 strains
- 996 genomes assigned to Methanobrevibacter, about 85% of the catalogue
- 98 genomes did not match any known species

Taxonomic coverage reported in the article is dominated by Methanobacteriales and Methanomassiliicoccales, with smaller numbers from Methanomicrobiales and Halobacteriales. The paper also argues for splitting the Methanobrevibacter smithii clade into M. smithii and the candidate species Candidatus Methanobrevibacter intestini.

## Data Availability

The article data availability statement points recovered genomes to the EBI `genome_sets` static file index:

```text
https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/archaea_gut-genomes.tar.gz
```

The same statement says the genomes and metagenomes used in the study are public through NCBI and MGnify, with accession details in Supplementary Table 1a-f.

Companion files on the Nature page include:

- Supplementary Data 1: unified human archaeal protein catalogue
- Supplementary Data 2: DIAMOND BLASTx mapped protein matrix
- Supplementary Data 3: mcrA alignment
- Supplementary Data 4: environmental and human archaeal 16S rRNA genes
- Supplementary Tables 1-14

## Curation Caveats

- The EBI data root is a shared `genome_sets` directory rather than a dedicated project landing page. Keep the Nature article as the descriptive landing page and the EBI index as the operational download page.
- The main genome archive is listed as generic feature format; users who need raw nucleotide FASTA should inspect the archive contents before assuming file layout.
- No source-specific automation script is needed because the genome archive and supplementary files are direct public URLs.
- No checksum file was observed next to the genome archive in the EBI index.
- The article is open access under CC BY 4.0, but the EBI archive page does not expose a separate dataset license statement.
