# GOMC Notes

- GOMC is the Global Ocean Microbiome Catalogue associated with the Nature paper "Global marine microbial diversity and its potential in bioprospecting".
- The Microbiome Data Portal dataset page is the preferred human-facing landing page for browsing the catalogue and enzyme-discovery context, and its `get_download` API exposes the bulk file table.
- The preferred bulk-access path is `https://ftp.cngb.org/pub/SciRAID/microbiomics/MDB0000002/`, which contains compressed archives, directory views, supplementary files, and `md5.txt`.
- The paper and dataset summary report 43,191 newly recovered prokaryotic genomes and a unified catalogue of 24,195 species-level genomes.
- The main bulk archives are `43191.all_MAGs.tar.gz`, `24195.GOMC_genomes.tar.gz`, `GOPC.geneset.pep.fa.gz`, and `unprecedented_genome_size_MAGs.tar.gz`.
- The CNGBdb project page `CNP0004049` is a secondary accession/archive view for the 16,240 dereplicated newly reconstructed MAGs. Keep it for per-assembly metadata and CNSA accessions, not as the primary download route.
- The `CNP0004049` project statistics list 16,240 samples and 16,240 assemblies. Treat these as accession-level files for the dereplicated newly reconstructed MAGs.
- The GitHub repository `BGI-Qingdao/GOMC` contains analysis code for the paper. It is useful for methods provenance but is not the primary data download location.
- No source-specific `download.py` is needed: the dataset has direct HTTPS bulk links and a small JSON download-table API.
