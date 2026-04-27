# Microbiome Datahub Notes

- Microbiome Datahub is a National Institute of Genetics MAG-focused database that collects publicly available MAG DNA sequence data from INSDC and re-annotates genomes with DFAST and DFAST_QC.
- The public site reports Microbiome Datahub version 1.2 and a dataset update date of 2025-08-29.
- The site documentation says version 1 contains 218,653 MAGs. The Zenodo record description still says 214,427 MAGs, so curation should treat the site documentation and the dated filenames as the operational authority for the current sequence bulk set.
- Search interfaces cover project and genome metadata. Genome search supports environment, genome taxon, MAG completeness, host taxon, and Bac2Feature phenotype filters.
- Bulk DNA/protein sequence acquisition is not a single archive; it is a small fixed set of large files on the NIG download web server.
- Whole-database metadata, Bac2Feature phenotype predictions, KEGG module composition matrix, and module labels are distributed through Zenodo.
- Targeted access uses stateless URL APIs with comma-separated BioProject or GCA identifiers.
- During curation on 2026-04-25, `https://mdatahub.org/api/dl/project/metadata/PRJNA982417`, sequence download `HEAD` requests, and `https://mdatahub.org/api/genome/mbgd/GCA_029762515.1` worked from the command line.
- During the same curation pass, the documented genome metadata API examples returned HTTP 500 with `row[n].replace is not a function`; keep this caveat until rechecked upstream.
- The official bulk server is documented as `http://palaeo.nig.ac.jp/Resources/MDatahub/2025/`. It was not reachable from the current network during curation, but the raw project documentation lists the file names and sizes.
