# mOTUs DB Notes

- mOTUs DB is the genome database behind the mOTUs profiler and website.
- The public v4.0 genome collection contains 3,747,151 genomes according to the v4.0 download page and supplementary metadata.
- The marker-gene mOTUs profiling database contains 124,295 species-level mOTUs built from ten single-copy marker genes.
- Genome sequences can be downloaded as one large tar archive, as individual `.fa.gz` files through the `genomes/` directory tree, or through `motus-tool`.
- The full `mOTUs4.genomes.tar` archive is the closest thing to a direct all-genomes download and is approximately 2.7 TB.
- The metadata file `mOTUs4.0_genome-metadata-20250702.alpha.tsv.gz` is the most useful starting point for scripted selection because it includes the per-genome `PATH` field.
- `motus-tool` should be used for query-driven access by taxonomy, mOTU, genome ID, KEGG, PFAM, or eggNOG.
- `motus genomes` downloads a large annotation database on first use; plan for approximately 17.7 GB in addition to the marker-gene DB.
- The website supports interactive sequence download for small selections only, with a 200-genome limit.
- Official documentation has started to describe mOTUs 4.1, but the checked 4.1 bulk path was not public at the time of curation; this entry records the public 4.0 paths.
