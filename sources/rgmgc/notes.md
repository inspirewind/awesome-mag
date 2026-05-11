# RGMGC Notes

- RGMGC is the resource associated with Xie et al. 2021, "An integrated gene catalog and over 10,000 metagenome-assembled genomes from the gastrointestinal microbiome of ruminants."
- The study profiles 370 gastrointestinal tract content samples across seven ruminants: dairy cattle, water buffalo, yak, goat, sheep, roe deer, and water deer.
- Sampling spans ten GIT regions: rumen, reticulum, omasum, abomasum, duodenum, jejunum, ileum, cecum, colon, and rectum.
- The official website reports 154,335,274 non-redundant genes in the integrated ruminant GIT microbial reference gene catalog, with total gene length 100,332,734,514 bp, average gene length 650 bp, N50 768 bp, and GC content 47.5%.
- The paper and homepage report 10,373 nonredundant MAGs, including 8,745 novel uncultured bacterial and archaeal species. The homepage also says the site stores 28,543 Illumina bins from the study.
- The website's `RGMGC` browse page exposes gene-catalog summaries and a public JSON endpoint at `https://rummeta.njau.edu.cn/rumment/browse/getTableData`.
- The website's `METAGENOMICS` resource page is the useful direct-download page for nucleotide/amino-acid gene catalogs and gene/taxonomic/functional profiles.
- The website's `GENOMES` resource page loaded without download links during curation on 2026-05-11. For MAG sequence access, use NCBI BioProject `PRJNA657473`; for MAG and USG protein/ORF sequence bundles, use Figshare DOI `10.6084/m9.figshare.14176574`.
- The article has a correction record: `https://doi.org/10.1186/s40168-022-01426-5`.
- NCBI records list the legacy related-resource domain `http://www.rummeta.com`; the currently reachable official site from the user-provided URL is `https://rummeta.njau.edu.cn/`.

## Website Gene Counts

Selected counts from the official browse API:

| Group | Non-redundant genes |
| --- | ---: |
| RGMGC integrated catalog | 154,335,274 |
| Bovinae | 97,393,650 |
| Caprinae | 40,885,116 |
| Cervidae | 19,560,218 |
| Rumen | 53,037,993 |
| Reticulum | 31,307,361 |
| Omasum | 31,397,747 |
| Cecum | 36,326,606 |
| Colon | 31,690,262 |
| Rectum | 33,737,430 |

## Access Caveats

- The RGMGC website uses direct `downloadFile?file=` endpoints; no source-specific automation script is currently needed.
- Use resumable download tooling for the full gene catalogs. The website page does not show checksums or file sizes next to the links; HEAD checks on 2026-05-11 reported 30,144,505,627 bytes for `RGMGC.geneSet.ffn.gz` and 21,133,596,825 bytes for `RGMGC.geneSet.faa.gz`.
- The Figshare web page was visible during curation, but the Figshare API endpoint returned HTTP 403 to `curl`. Treat Figshare as browser-oriented unless a stable public API route is verified later.
- NCBI ESearch reported 370 SRA records for `PRJNA657455` and 10,373 assembly records for `PRJNA657473` on 2026-05-11.
