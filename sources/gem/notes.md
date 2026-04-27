# GEM Notes

- GEM is the JGI Genomes from Earth's Microbiomes resource associated with "A genomic catalog of Earth's microbiomes."
- The project page reports 52,515 bacterial and archaeal MAGs reconstructed from more than 10,450 metagenomes across diverse microbiomes.
- The MAG catalogue meets medium-quality MIMAG criteria overall, with reported mean completeness of 83%, mean contamination of 1.3%, and 9,143 high-quality MAGs.
- The public NERSC data root is the most useful curation entry point: `https://portal.nersc.gov/GEM/`.
- The NERSC README describes companion data beyond genome sequences: OTU assignments, antiSMASH biosynthetic gene clusters, VirSorter prophage predictions, MMseqs2 protein clusters, and phylogenetic marker-gene trees.
- Data usage is permissive for the MAG bundle itself, but underlying metagenomes remain subject to JGI data release and utilization policies.
- During curation on 2026-04-27, the JGI Genome Portal page showed a banner saying the Genome Portal was reaching end of life at the end of April and would be replaced by the JGI Data Portal. The NERSC static file host was still publicly accessible.

## Data Layout

| Path | Contents |
| --- | --- |
| `genomes/` | MAG FASTA archives, individual genome FASTA files, predicted CDS/protein archives, and genome metadata. |
| `otus/` | Species-level OTU mapping, representative genomes, taxonomy, CheckM metrics, and representative OTU genome FASTA files. |
| `bgcs/` | Per-genome antiSMASH v5.1 GenBank outputs. |
| `prophages/` | VirSorter prophage predictions in FASTA and TSV form. |
| `protclusts/` | MMseqs2 protein cluster tables and representative protein sequences. |
| `tree/` | Marker-gene alignment and rooted/unrooted phylogenetic trees. |

## Checked Files

| File | Size | Notes |
| --- | ---: | --- |
| `genomes/genome_metadata.tsv` | 12.4 MB | Columns include genome ID, metagenome ID, genome length, contigs, N50, rRNA/tRNA counts, completeness, contamination, MIMAG quality, OTU ID, ecosystem fields, and coordinates. |
| `genomes/fna.tar` | 39.5 GB | Genome nucleotide FASTA tar archive for the 52,515 GEM MAGs. |
| `genomes/faa.tar` | 26.7 GB | Predicted protein FASTA tar archive. |
| `genomes/ffn.tar` | 39.3 GB | Predicted CDS nucleotide FASTA tar archive. |
| `otus/fna.tar` | 43.3 GB | Representative OTU genome FASTA tar archive. |
| `prophages/virsorter.fna` | 688 MB | VirSorter prophage nucleotide predictions. |
| `prophages/virsorter.tsv` | 2.1 MB | VirSorter prophage metadata table. |
| `protclusts/cluster_info.tsv` | 5.4 GB | Protein cluster information table. |
| `tree/multi_marker.rooted.tree` | 2.3 MB | Rooted tree based on universal single-copy marker genes. |
