# cFMD Notes

- cFMD is the Segata Lab curatedFoodMetagenomicData resource for food shotgun metagenomes.
- The current GitHub README reports cFMD v1.3.1 with 3,444 food metagenomes from 87 food metagenomic datasets, 14,904 MAGs, 1,153 prokaryotic SGBs, and 110 eukaryotic SGBs.
- The current version is not the same as the Cell 2024 paper release. The README points users to cFMD v1.1.0 for the Carlino et al. paper version.
- v1.3.1 focuses on cheese microbiomes: synchronization with MetaCheeseDB, two new cheese metagenomic datasets, 134 new samples, 839 new MAGs, and additional cheese metadata.
- GitHub stores lightweight cFMD-level TSV files and per-dataset folders. The large MAG FASTA and HUMAnN functional-profile archives are external Zenodo files reached through upstream shell scripts.
- The main `cFMD_metadata.tsv` key is `dataset_name` plus `sample_id`; food metadata are organized by category, type, and subtype.
- `cFMD_mags_list.tsv` is the key MAG-level inventory. It includes sample origin, SGB assignment, known/unknown status, taxonomy, genome size, contigs, N50, completeness, contamination, and GC content.
- Dataset-specific folders can include prokaryotic MAG info, eukaryotic MAG info, sample metadata, additional cheese metadata, and MetaPhlAn taxonomic profiles.
- The upstream `download_mags.sh` script maps dataset names to Zenodo records `17710367`, `17709831`, and `18456071` for initial-release, v1.2.1, and v1.3.1 MAG archives.
- The upstream `download_functional_profiles.sh` script maps dataset names to Zenodo records `14871851`, `15609141`, and `18456455` for initial-release, v1.2.1, and v1.3.1 functional-profile archives.
- Functional profiles are normalized UniRef90 gene families, pathway abundances, and pathway coverages generated with HUMAnN3.
- cFMD data generation uses SegataLab preprocessing, an assembly/MAG reconstruction pipeline, MetaPhlAn4, StrainPhlAn4, and HUMAnN3.
- Use the GitHub release/README counts for current cFMD curation. Use the Cell paper and Zenodo record `13285428` when documenting the original publication-scale release.

## Release History Pointers

| Version | Main curation note |
| --- | --- |
| v1.1.0 | Version associated with Carlino et al., Cell 2024. |
| v1.2.1 | Added publicly available food metagenomic datasets and reorganized data into dataset-specific folders. |
| v1.2.1 patch | Removed redundant `CM_UNINA_FFOOD` metagenomes and patched missing eukaryotic MAG archives. |
| v1.3.0 | Reprocessed older samples with updated MetaRefSGB and MetaPhlAn resources. |
| v1.3.1 | Added MetaCheeseDB-aligned cheese metadata plus two new cheese datasets. |
