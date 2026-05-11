# OceanDNA MAG Catalog Notes

- OceanDNA is a marine prokaryotic MAG catalog from Nishimura and Yoshizawa, published as a Scientific Data descriptor in 2022.
- The catalog reconstructs 52,325 qualified MAGs from 2,057 published marine metagenomes, grouped into 8,466 species-level clusters across 59 phyla.
- The study includes 3,337 MAGs from deep sea below 1,000 m, 7,884 from low-oxygen zones below 90 umol O2 per kg water, and 7,752 from polar regions.
- Data Records split the sequence archive into 8,466 species representatives submitted as WGS entries under `PRJDB11811` and 43,859 non-representative genomes submitted as DDBJ analysis entries.
- The figshare collection is the best top-level genome-sequence landing page. The static Nature/Springer supplementary files are directly downloadable and cover source metagenomes, OceanDNA MAG metadata, published marine genomes, and UGCMP representatives.
- Supplementary File S3 is the key metadata table for the OceanDNA MAGs. It includes genome statistics, functional RNAs, genome quality, species clusters, species-representative flags, GTDB taxonomy, and source-metagenome metadata.
- The authors report 108 high-quality draft MAGs and 52,217 medium-quality draft MAGs by MIMAG criteria. They recommend manual quality control before downstream use because misassigned contigs may remain after automated refinement.
- The metagenome dataset is mainly water samples, plus sediment trap and biofilm samples. The Usage Notes explicitly caution that some marine environments, including sediments, hydrothermal vents, and coral reefs, were not included.
- MAGRE, the post-refinement module from the study, is available at `https://github.com/yosuken/MAGRE`.

## Citation

- Nishimura, Y. and Yoshizawa, S. The OceanDNA MAG catalog contains over 50,000 prokaryotic genomes originated from various marine environments. Scientific Data 9, 305 (2022). https://doi.org/10.1038/s41597-022-01392-5
