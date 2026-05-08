# Gut Phage Database Notes

- The Gut Phage Database (GPD) is a Wellcome Sanger Institute human gut bacteriophage resource associated with the Cell article "Massive expansion of human gut bacteriophage diversity."
- The Sanger page describes the database as 142,809 non-redundant gut phage genomes from 28,060 metagenomes.
- The publication describes mining 28,060 globally distributed human gut metagenomes plus 2,898 reference genomes of cultured gut bacteria, retaining viral genomes over 10 kb.
- The EBI README describes `GPD_sequences.fa.gz` as the nucleotide sequences of 142,809 viral clusters at 95% nucleotide identity.
- The main operational download entry point is the EBI static index: `https://ftp.ebi.ac.uk/pub/databases/metagenomics/genome_sets/gut_phage_database/`.
- Companion files include human gut metagenome metadata, predicted host co-occurrence results, Gubaphage clades/genomes, crAss-like family membership, and a crAss/Gubaphage Newick tree.
- Functional annotation is provided through `GPD_proteome_orthology_assignment.txt.gz`, with eggNOG ortholog, GO, EC, KEGG, CAZy, BiGG, COG, and free-text description fields.
- Sanger's data-use text should be preserved in downstream notes because the EBI directory itself does not state a dataset license or terms.

## Data Layout

| File | Contents |
| --- | --- |
| `GPD_sequences.fa.gz` | Nucleotide sequences of GPD viral genome representatives/clusters. |
| `GPD_proteome.faa.gz` | Predicted protein-coding sequences. |
| `GPD_annotations.tar.gz` | GFF annotation files for GPD genomes. |
| `GPD_metadata.tsv` | Genome metadata, host range, detection geography, CheckV quality fields, and novelty flag. |
| `GPD_proteome_orthology_assignment.txt.gz` | Functional annotation for GPD proteins. |
| `PCs_GPD.txt` | Protein clusters for the GPD proteome. |
| `GutMetagenomes_metadata.csv` | Metadata for screened human gut metagenomes. |
| `co_occurrence_analysis.txt` | Phage-host co-occurrence analysis results. |
| `Gubaphage_clades.tsv` | Major Gubaphage clade assignments for viral predictions over 60 kb. |
| `Gubaphage_genomes.fa` | Gubaphage genome sequences. |
| `crAss-family_members.tsv` | crAss-like genus membership assignments. |
| `crAss_gubaphage_phylo.nwk` | crAss/Gubaphage phylogeny in Newick format. |

## Checked Files

| File | Size | Last modified | Notes |
| --- | ---: | --- | --- |
| `GPD_sequences.fa.gz` | 1.4G | 2020-09-02 | Main nucleotide FASTA archive. |
| `GPD_proteome.faa.gz` | 928M | 2020-09-02 | Predicted protein FASTA archive. |
| `GPD_annotations.tar.gz` | 1.9G | 2020-10-29 | GFF annotation archive. |
| `GPD_metadata.tsv` | 50M | 2020-09-02 | Main metadata TSV; not gzip-compressed. |
| `GPD_proteome_orthology_assignment.txt.gz` | 67M | 2020-10-29 | Protein functional annotation table. |
| `PCs_GPD.txt` | 105M | 2020-10-29 | Protein cluster file. |
| `Gubaphage_genomes.fa` | 142M | 2021-05-29 | Gubaphage genomes. |
| `README.txt` | 4.2K | 2022-01-30 | File descriptions and column definitions. |

Checked on 2026-05-07.
