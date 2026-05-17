# Meta320 Sheep and Goat Gut MAGs Notes

Verified on 2026-05-11 against the Microbiome article, Crossref DOI metadata, NCBI BioProject/SRA metadata, the GitHub repository, Springer supplementary file headers, and the Figshare download endpoint behavior.

Meta320 is a sheep and goat gut microbiome resource from the Microbiome article "Compendium of 5810 genomes of sheep and goat gut microbiomes provides new insights into the glycan and mucin utilization."

The resource is in scope for Awesome MAG because it provides a ruminant-focused animal gut MAG catalog, companion sheep/goat microbial gene catalogs, CAZyme and PUL analyses, host-specific MAG tables, raw SRA read access, and workflow scripts.

## Resource Profile

Paper- and repository-reported scale:

- 320 fecal samples, including 210 sheep and 110 goat samples
- 21 sheep and goat breeds from 32 farms
- More than 162 million sheep gut non-redundant predicted genes
- More than 82 million goat gut non-redundant predicted genes
- 49 million shared non-redundant predicted genes and 1,138 shared species
- 5,810 medium- and high-quality MAGs
- 2,661 MAGs representing unidentified species
- 91 bacterial taxa reported as specifically colonizing the sheep gut
- Supplementary tables for MAG abundance, CAZyme-predicted proteins, host-specific MAGs, and PULs

NCBI SRA runinfo for `PRJNA972320` reports 320 paired Illumina HiSeq 4000 metagenomic WGA runs, 3,444,597,693,300 bases, and about 1.05 TB in SRA file size.

## Data Availability

The article states that raw sequence reads are under NCBI project `PRJNA972320`, protein and ORF sequences for all MAGs are in a Figshare share, and workflow/scripts are in `https://github.com/bladrome/meta320_binning`.

The GitHub repository is small and contains an Org-mode workflow, `envs/`, and `pipeline/` scripts for preprocessing, assembly/binning, GTDB-Tk taxonomy, and functional annotation. It is useful for reproducibility context, but not a data host.

Springer supplementary files are important for curation because several MAG-level tables are not the same as the Figshare sequence archive:

- Additional file 8 / Table S13: relative abundance of the 5,810 MAGs
- Additional file 9 / Table S14: CAZyme-predicted proteins of the 5,810 MAGs
- Additional file 10 / Table S15: 91 sheep-specific MAGs and one goat-specific MAG
- Additional file 11 / Table S16: CAZyme-predicted proteins for the 92 host-specific MAGs
- Additional file 12 / Table S17: predicted PULs for the 92 host-specific MAGs

## Curation Caveats

- Use the article DOI page as the descriptive landing page.
- Use NCBI BioProject `PRJNA972320` or the SRA runinfo CSV as the reproducible route for raw reads.
- Use the Figshare share for the Meta320 MAG assemblies file. The observed browser-facing file endpoint `https://figshare.com/ndownloader/files/40441679?private_link=fe5fb3dd964a15844505` returned `HTTP/2 202` with `x-amzn-waf-action: challenge` during one curation check, but the official downloader-host endpoint `https://ndownloader.figshare.com/files/40441679?private_link=fe5fb3dd964a15844505` is now wrapped by `corpus/download_bash/part4_hard_datasets/meta320.sh` and should be validated on the target server.
- Use Springer static supplementary URLs for metadata/annotation tables; spot checks of Additional files 8, 9, and 12 returned HTTP 200.
- Do not add challenge-bypass logic. If the official downloader-host endpoint fails, use browser-mediated download or revisit the Figshare route. After a successful download, inspect the payload packaging and FASTA headers before building the RabbitTClust filelist.

Primary citation:

- Zhang K, He C, Wang L, Suo L, Guo M, Guo J, et al. Compendium of 5810 genomes of sheep and goat gut microbiomes provides new insights into the glycan and mucin utilization. Microbiome 12, 104 (2024). https://doi.org/10.1186/s40168-024-01806-z
