# HRGM Notes

HRGM (Human Reference Gut Microbiome) is a comprehensive human gut prokaryotic genome catalog from Insuk Lee's lab at Yonsei University (Network Biology Lab / decodebiome). Two versions exist:

- **HRGM1** (published 2021): 232,098 non-redundant genomes representing 5,414 species, incorporating 29,082 newly assembled genomes from 845 fecal samples across Korea, India, and Japan combined with existing public genomes (UHGG).
- **HRGM2** (current; primary article published Dec 2025, issue date 2026): 155,211 non-redundant near-complete genomes representing 4,824 prokaryotic species across 41 countries, served at the primary site.

The resource is in scope for Awesome MAG because it is a major human gut MAG catalog with a public web portal, bulk genome downloads, protein catalogs, pangenomes, GEMs, taxonomy profiling databases, and a peer-reviewed publication. It belongs under human-associated MAG resources.

The site serves HRGM2 by default at `/HRGM/` and preserves HRGM1 at `/HRGM1/`. Downloads use a PHP-based file browser (`listdir.php`) that exposes Apache-style directory listings. All files are accessible via direct HTTPS with no authentication, login, or cookie requirements.

An official HRGM2 code and data-description repository exists at `https://github.com/netbiolab/HRGM2`. There is no formal data API; programmatic access is through the `listdir.php` directory browser and `genomeinfo.php` per-genome endpoint, plus direct HTTPS and Zenodo downloads. The old URL from the HRGM1 publication (`www.mbiomenet.org/HRGM/`) is unreachable.

HRGM2 data are also mirrored through Zenodo records listed in the official HRGM2 GitHub `DATA.md`. Those HRGM2 Zenodo records use CC0. A third-party Zenodo record (Waschina et al.) provides gapseq metabolic reconstructions derived from HRGM1 genomes under CC BY 4.0.

Primary citations:

- Ma J, Kim N, Cha JH, et al. A human gut metagenome-assembled genome catalogue spanning 41 countries supports genome-scale metabolic models. Nature Microbiology 11, 317-334 (2026). https://doi.org/10.1038/s41564-025-02206-1
- Kim CY, Lee M, Yang S, Kim K, Yong D, Kim HR, Lee I. Human reference gut microbiome catalog including newly assembled genomes from under-represented Asian metagenomes. Genome Medicine 13, 134 (2021). https://doi.org/10.1186/s13073-021-00950-7
