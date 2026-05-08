# RUG2 Rumen MAGs Notes

- Stewart et al. 2019 report a compendium of 4,941 rumen metagenome-assembled genomes from 283 cattle.
- The author data page labels the resource as RUG2 and links to public pages for 288 metagenome assemblies and 20,469 Illumina bins.
- The author landing page says 20,567 bins, while the detailed bins page title and text say 20,469 Illumina bins. Use 20,469 when referring specifically to the linked Illumina bins index.
- The final 4,941 RUGs are selected from the broader candidate-bin set; when downloading through ENA, treat binned metagenome records as a superset unless using the study tables to filter the final RUG set.
- Data availability is split across ENA and Edinburgh DataShare. ENA holds raw reads, primary assemblies, and RUG assemblies. DataShare holds predicted proteins, gene clusters, annotations, synteny, and associated data tables.
- The earlier Stewart et al. 2018 reads reused in the study are under ENA project `PRJEB21624`.
- The DataShare record lists `rug2.tar.gz` as 29.76 Gb and the bitstream returned a 31,958,778,104 byte `Content-Length`, but the landing page does not expose a checksum.
- During curation on 2026-05-08, the ENA Portal API returned example rows for raw reads, primary metagenome assemblies, and binned metagenome assemblies. The author metagenome assemblies CSV was reachable. The author bins page was reachable, but its linked CSV returned a 404 page.
- No automation script is currently justified because ENA provides TSV exports with FTP URLs and the companion archive is a single DataShare file.
