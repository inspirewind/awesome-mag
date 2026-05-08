# Gut Phage Database Download Notes

The Gut Phage Database (GPD) is available from a public EMBL-EBI static file index linked by the Wellcome Sanger Institute project page.

- Sanger page: `https://www.sanger.ac.uk/data/gut-phage-database/`
- EBI index: `https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/gut_phage_database/`
- EBI README: `https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/gut_phage_database/README.txt`

No source-specific helper script is needed. The files are direct HTTP(S) downloads and support range requests.

## Core Files

Base path: `https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/gut_phage_database/`

| Asset | File | Size | Notes |
| --- | --- | ---: | --- |
| Nucleotide sequences | `GPD_sequences.fa.gz` | 1.4G | Nucleotide sequences for 142,809 GPD viral clusters at 95% nucleotide identity. |
| Protein sequences | `GPD_proteome.faa.gz` | 928M | Protein-coding sequences for GPD. |
| Genome annotations | `GPD_annotations.tar.gz` | 1.9G | Archive of GFF annotation files. |
| Genome metadata | `GPD_metadata.tsv` | 50M | Uncompressed TSV with genome source, viral cluster, predicted phage taxon, host range, detection geography, CheckV fields, and novelty. |
| Protein orthology assignments | `GPD_proteome_orthology_assignment.txt.gz` | 67M | Functional annotation table for GPD proteins, including eggNOG, GO, EC, KEGG, CAZy, BiGG, and COG fields. |
| Protein clusters | `PCs_GPD.txt` | 105M | GPD proteome clusters; each line represents one protein cluster. |

## Companion Files

| Asset | File | Size | Notes |
| --- | --- | ---: | --- |
| Screened metagenome metadata | `GutMetagenomes_metadata.csv` | 2.1M | Metadata for the 28,060 human gut metagenomes screened for viral sequences. |
| Host co-occurrence analysis | `co_occurrence_analysis.txt` | 1.0M | Predicted host, metagenomic co-detection counts, and binomial-test significance. |
| Gubaphage clades | `Gubaphage_clades.tsv` | 20K | Viral predictions over 60 kb assigned to major Gubaphage clades. |
| Gubaphage genomes | `Gubaphage_genomes.fa` | 142M | Gubaphage genome sequences, added after the first GPD file release. |
| crAss-like family members | `crAss-family_members.tsv` | 69K | Viral predictions assigned to crAss-like genera. |
| crAss/Gubaphage tree | `crAss_gubaphage_phylo.nwk` | 12K | Newick phylogeny of crAssphage with Gubaphage. |

## Example Commands

Download the README and metadata first:

```bash
curl -L -O https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/gut_phage_database/README.txt
curl -L -C - -O https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/gut_phage_database/GPD_metadata.tsv
```

Download the main sequence files with resume support:

```bash
curl -L -C - -O https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/gut_phage_database/GPD_sequences.fa.gz
curl -L -C - -O https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/gut_phage_database/GPD_proteome.faa.gz
curl -L -C - -O https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/gut_phage_database/GPD_annotations.tar.gz
```

Inspect file headers before full downstream processing:

```bash
zcat GPD_sequences.fa.gz | head
head -n 2 GPD_metadata.tsv
tar -tzf GPD_annotations.tar.gz | head
```

## Verification and Caveats

- The EBI index did not show MD5 or SHA checksum files during curation.
- `GPD_metadata.tsv` is uncompressed despite many companion files being compressed.
- The Sanger project page includes a data-use statement requesting PI permission before publishing chromosome/genome-scale sequence, ORF, or gene analyses.
- This resource is a viral/phage genome catalogue, not a bacterial or archaeal MAG catalogue. It is included here as a human-gut metagenomic companion resource.

Checked on 2026-05-07.
