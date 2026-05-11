# Awesome MAG

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated list of metagenome-assembled genome (MAG) datasets, catalogs, and database websites, with reproducible download notes and lightweight automation helpers for sources that still require manual clicks or multi-step browser workflows.

## Scope

This repository is intended to collect:

- MAG datasets and genome catalogs
- MAG-oriented databases and project portals
- Download pages, mirrors, and release notes
- Access notes for sources that are difficult to fetch reproducibly
- Automation scripts for sources that are not easily downloadable from a single stable URL

This repository is not intended to:

- mirror large upstream datasets in Git
- replace official documentation from source websites
- host full analysis pipelines for assembly, binning, or annotation

## Why This Repository Exists

MAG resources are distributed across project websites, supplemental data pages, institutional portals, and database interfaces. Discovery is often easy; reproducible access is not. A useful `awesome` repository for MAG resources should therefore separate three concerns:

1. A human-readable curated index for quick discovery
2. Structured source metadata for consistent maintenance
3. Small source-specific scripts for awkward download flows

## Suggested Top-Level Sections

As the list grows, the main `README.md` should stay concise and group links by user intent. A practical structure is:

- General MAG catalogs and database portals
- Human-associated MAG resources
- Animal-associated MAG resources
- Marine and freshwater MAG resources
- Soil and terrestrial environment MAG resources
- Wastewater, engineered, and extreme-environment resources
- Integrated or multi-biome collections
- Metadata, annotation, and companion resources
- Download notes, mirrors, and access restrictions
- Deprecated, moved, or archived resources

## General MAG Catalogs and Database Portals

| Resource | Scope | Type | Access | Automation | Notes |
| --- | --- | --- | --- | --- | --- |
| [MAGdb](https://magdb.nanhulab.ac.cn/) | Clinical, Environment, Animal | Database portal | Public listings; cookie-gated archive downloads | [Download script](scripts/magdb/README.md) | Per-study `data.tar.gz`; 74 study packages downloaded; see [notes](sources/magdb/download.md) |
| [gcMeta](https://gcmeta.wdcm.org/) | Multi-biome catalogues | Database portal | Public catalogue APIs; public direct archive files | [Download script](scripts/gcmeta/README.md) | 50 catalogue bundles; public `catalogueTree` and `catalogueNameList` enumeration plus derived direct files on `open.nmdc.cn`; see [notes](sources/gcmeta/download.md) |
| [GEM](https://genome.jgi.doe.gov/portal/GEMs/GEMs.home.html) | Global multi-biome bacterial and archaeal MAGs | Static dataset portal | Public NERSC file indexes and direct archives | None | 52,515 MAGs; 39.5G genome FASTA tar, 26.7G protein tar, 39.3G CDS tar, metadata, OTU, BGC, prophage, protein-cluster, and tree files; see [notes](sources/gem/download.md) |
| [GOMC](https://db.cngb.org/maya/datasets/MDB0000002) | Global ocean microbial MAG/genome catalogue | Dataset portal and CNGBdb archive | Public direct bulk archives, MD5 file, and CNGB/CNSA accession files | None | 43,191 recovered MAGs, 24,195 GOMC genomes, 171.3G protein catalogue, supplementary files, and CNP0004049 accession archive; see [notes](sources/gomc/download.md) |
| [OMDB](https://omdb.microbiomics.io/about) | Ocean microbiome reconstructed genomes and gene/scaffold catalogs | Database portal and static file backend | Public browser, direct HTTPS manifests, and catalog files | None | 274,282 reconstructed genomes, 32,022 species-level units, 508.8M genes, links TSV for per-genome FASTA/GFF/antiSMASH files, plus 100G-scale catalogs; see [notes](sources/omdb/download.md) |
| [OceanDNA MAG Catalog](https://www.nature.com/articles/s41597-022-01392-5) | Global marine prokaryotic MAGs | Paper dataset, figshare collection, INSDC BioProject, and DDBJ analysis records | Figshare collection for genome sequences; public static supplementary XLSX files; WGS representatives under `PRJDB11811` | None | 52,325 qualified MAGs from 2,057 marine metagenomes, 8,466 species-level representatives, 43,859 DDBJ non-representative analysis entries, and S1-S6 supplementary workbooks; see [notes](sources/oceandna/download.md) |
| [Glacier-fed Streams (GFS) MAGs](https://www.nature.com/articles/s41564-024-01874-9) | Freshwater cryosphere stream biofilms | Paper dataset, NCBI BioProject, Zenodo record, and code repositories | Public NCBI accessions plus Zenodo files with MD5 checksums | None | 156 sediment metagenomes from 9 mountain ranges, 2,855 bacterial MAGs, prokaryotic contig/GFF/protein tar archives, supplementary tables, and source data files; see [notes](sources/gfs/download.md) |
| [LakePulse MAG Catalogue](https://www.nature.com/articles/s41564-023-01435-6) | Canadian freshwater and oligosaline lakes | Paper dataset, Dryad record, ENA project, JGI GOLD study, and code repository | Public Dryad files, ENA accessions, and GOLD metadata | None | 308 Canadian lakes, 1,008 bacterial MAG/genomospecies, MAG contig/protein/GFF ZIPs, 11 ecozone co-assembly contig files, and 64.3G Dryad v6 file set; see [notes](sources/lakepulse/download.md) |
| [GROWdb](https://www.nature.com/articles/s41586-024-08240-z) | North American river surface-water MAGs and multi-omics | Paper dataset, NCBI BioProject, Zenodo records, NMDC/KBase portals, and Shiny explorer | Public NCBI accessions, Zenodo direct files, and interactive portals | None | 3,825 medium/high-quality MAGs dereplicated to 2,093 river MAGs, annotation/gene/expression/ARG files, plus 5,986 global freshwater dereplicated MAG archive; see [notes](sources/growdb/download.md) |
| [cFMD](https://github.com/SegataLab/cFMD) | Food shotgun metagenomes, including fermented foods and cheese | GitHub dataset, Zenodo archive records, and paper dataset | Public GitHub TSV/profile files plus Zenodo MAG and HUMAnN archives | Official shell scripts | cFMD v1.3.1 has 3,444 food metagenomes from 87 datasets, 14,904 MAGs, 1,153 prokaryotic SGBs, 110 eukaryotic SGBs, and MetaCheeseDB-aligned cheese metadata; see [notes](sources/cfmd/download.md) |
| [TPMC](https://ngdc.cncb.ac.cn/tpmc) | Tibetan Plateau aquatic microbiome MAGs and genes | Dataset portal and GSA project archive | Public CNCB static catalog directories plus GSA raw metagenome project | None | 32,355 medium/high-quality MAGs from 498 aquatic metagenomes, 10,723 species representatives, 296.3M TPMC genes, 73,864 BGCs, and 329.6M TLGC genes; see [notes](sources/tpmc/download.md) |
| [QXLSG](https://www.sciencedirect.com/science/article/pii/S2211124725012549) | Qinghai-Xizang Plateau lake sediment MAGs across salinity gradients | Paper dataset, NGDC BioProject/GSA, GWH assemblies, NODE analysis, and Figshare share | Public NGDC GSA and GWH direct URLs; Figshare share is browser-challenged from CLI | None | 28 sediment samples from 10 lakes, 5,866 MAGs, 2,742 species-level genomes, 58.16M non-redundant genes, and 19,008 BGCs; see [notes](sources/qxlsg/download.md) |
| [Anammox Microbiota Catalog](https://figshare.com/articles/dataset/A_comprehensive_catalog_encompassing_genes_and_genomes_reveals_the_core_community_and_functional_diversity_in_anammox_microbiota/25476583) | Wastewater anammox microbiota MAG and gene catalog | Paper dataset and Figshare record | Public Figshare DOI and browser download; command-line API/downloader access may be WAF-challenged | None | 236 metagenomes, 7,474 MAGs, 1,768 strain-level MAGs, 1,376 species-level genomes, and gene catalog files; see [notes](sources/anammox-microbiota/download.md) |
| [SPIRE](https://spire.embl.de/) | Multi-biome MAGs and assemblies | Dataset portal | Public direct URLs; Apache indexes | [URL helper](scripts/spire/README.md) | 714 page-listed studies; script prints URLs only for use with `wget`, `aria2c`, or other tools; see [notes](sources/spire/download.md) |
| [mOTUs DB](https://motus-db.org/) | Multi-biome prokaryotic genomes and mOTUs | Database portal and tool-backed dataset | Public bulk 4.0 file host; targeted access through `motus-tool` | Official `motus-tool` | 2.7T all-genomes tar, full metadata, supplementary tables, and marker/annotation DBs; see [notes](sources/motus-db/download.md) |
| [Microbiome Datahub](https://mdatahub.org/) | Multi-biome MAG metadata, annotations, and sequences | Database portal and API-backed dataset | Public Zenodo metadata; public NIG bulk sequence files; targeted download API | [Download helper](scripts/mdatahub/README.md) | 218,653 MAGs in site docs; 146G all-contig FASTA, 79G all-protein FASTA, Zenodo metadata/matrix files, and targeted URL APIs; see [notes](sources/mdatahub/download.md) |
| [Bin Chicken Rare Biosphere Genomes](https://zenodo.org/records/15220963) | Multi-biome rare biosphere MAGs | Zenodo supplementary dataset | Public direct Zenodo files; latest record is metadata-only | None | 77,562 Bin Chicken-recovered genomes; MAG archives are earlier explicit Zenodo versions, while latest record is revised metadata; see [notes](sources/bin-chicken-rbgs/download.md) |
| [SMAG](https://microbma.github.io/project/SMAG.html) | Global soil MAGs | Project portal, Zenodo dataset, and code repository | Public Zenodo split archive; CyVerse and S3 mirrors have access friction | None | 40,039 soil MAG bins from 3,304 metagenomes, 21,077 SGBs, plus SNV and virus files; see [notes](sources/smag/download.md) |
| [HRGM](https://www.decodebiome.org/HRGM/) | Human gut MAGs | Dataset portal | Public direct HTTPS files via PHP file browser | None | 155,211 non-redundant genomes (HRGM2), 4,824 species, plus proteins, pangenomes, GEMs, CAZymes, Kraken2/MetaPhlAn DBs, and taxonomy profiling; see [notes](sources/hrgm/download.md) |
| [Human Gut Archaeome](https://www.nature.com/articles/s41564-021-01020-9) | Human gut archaeal MAGs and isolate genomes | Paper dataset and EBI static archive | Public EBI bulk archive and public Nature supplementary files | None | 1,167 nonredundant archaeal genomes, 608 high-quality genomes, 28,581 protein clusters, and Supplementary Tables 1-14; see [notes](sources/human-gut-archaeome/download.md) |
| [Gut Phage Database (GPD)](https://www.sanger.ac.uk/data/gut-phage-database/) | Human gut bacteriophage genomes | Project page and EBI static archive | Public EBI static index and direct files | None | 142,809 non-redundant gut phage genome representatives/clusters from 28,060 metagenomes, plus proteins, GFF annotations, metadata, host/co-occurrence, Gubaphage, and crAss-like files; see [notes](sources/gut-phage-database/download.md) |
| [Metagenomic Gut Virus Dataset (MGV)](https://portal.nersc.gov/MGV/) | Human gut DNA virus genomes | NERSC static dataset and code repository | Public NERSC static index and direct files | None | 189,680 50%+ complete viral genomes from 11,810 metagenomes, 54,118 vOTUs, 11.8M proteins, 459,375 protein clusters, host/DGR/CRISPR-spacer files, and phylogeny; see [notes](sources/mgv/download.md) |
| [Unified Human Gut Virome (UHGV)](https://uhgv.jgi.doe.gov/) | Human gut virus genomes | JGI website, NERSC static dataset, Zenodo record, and code repository | Public NERSC static index, direct files, and Zenodo v1.0 compact files with MD5 checksums | None | 873,995 viral genomes from 12 gut virome data sources, 168,536 species-level vOTUs, 37.4M proteins, host predictions, read-mapping, microdiversity, protein-cluster, structure, and classifier/profiling resources; see [notes](sources/uhgv/download.md) |
| [Meta-virus Resource (MetaVR)](https://www.meta-virome.org/) | Multi-biome uncultivated viral genomes | Database portal, API, and bulk dataset | Browser-visible portal/API; plain curl/wget API and bulk requests are Cloudflare-blocked | None | 24,435,662 UViGs, 12,705,385 vOTUs, 42.4M protein clusters, 748,927 AlphaFold3 structures, iPHoP host calls, and IMG source metadata; see [notes](sources/metavr/download.md) |
| [HROM](https://www.decodebiome.org/HROM/) | Human oral MAGs | Dataset portal | Public direct HTTPS files via PHP file browser | None | 72,641 high-quality oral genomes, 3,426 species, 8,492,076 non-redundant proteins, pangenomes, 16S rRNA library, and Kraken2/MetaPhlAn DBs; see [notes](sources/hrom/download.md) |
| [MRGM](https://www.decodebiome.org/MRGM/) | Mouse gut MAGs | Dataset portal | Public direct HTTPS files via PHP file browser | None | 42,245 non-redundant NC genomes, 1,524 species, 55,893 total NC genomes, 1.7 million non-redundant proteins, 16S sequences, and Kraken2/MetaPhlAn DBs; see [notes](sources/mrgm/download.md) |
| [PIGC](https://db.cngb.org/data_resources/project/CNP0000824) | Pig gut microbial gene catalog and MAGs | CNGBdb project archive and code-backed paper dataset | Public CNSA FTP manifest, metadata TSVs, per-assembly FASTA links, and paired FASTQ links | None | 6,339 non-redundant MAGs, 2,673 SGBs, 17,237,052 PIGC90 genes, 500 newly sequenced metagenomes, and 6,347 current CNGB assembly files; see [notes](sources/pigc/download.md) |
| [ICRGGC](https://nmdc.cn/icrggc/) | Chicken gut MAGs and gene catalog | NMDC database portal, FTP archive, and Figshare datasets | Public ICRGGC API, NMDC FTP files, and Figshare ZIPs | None | 12,339 chicken gut MAGs, 1,978 species, 16,565,684-gene catalog, gene abundance archive, and split FTP mirrors with MD5 lists; see [notes](sources/icrggc/download.md) |
| [RUG2 Rumen MAGs](https://www.nature.com/articles/s41587-019-0202-3) | Cattle rumen MAGs and companion annotations | Paper dataset, ENA project, and DataShare archive | Public ENA FASTQ/assembly FTP links plus DataShare archive | None | 4,941 RUGs from 283 cattle, 288 metagenome assemblies, 20,469 Illumina bins index, and 29.76G protein/annotation archive; see [notes](sources/rug2/download.md) |
| [RGMGC](https://rummeta.njau.edu.cn/) | Ruminant gastrointestinal microbial gene catalog and MAG compendium | Database portal, paper dataset, NCBI BioProjects, Figshare record, and Springer supplementary files | Public website gene-catalog downloads, NCBI SRA/Assembly records, and browser-oriented Figshare record | None | 370 GIT-content metagenomes from 7 ruminant species and 10 regions, 154,335,274 non-redundant genes, 10,373 MAGs, 8,745 novel uncultured candidate species, and 28,543 Illumina bins; see [notes](sources/rgmgc/download.md) |
| [Meta320 Sheep and Goat Gut MAGs](https://link.springer.com/article/10.1186/s40168-024-01806-z) | Sheep and goat gut microbial genes and MAGs | Paper dataset, NCBI BioProject/SRA, Figshare share, Springer supplementary files, and GitHub workflow | Public SRA runinfo/read deposits; browser-oriented Figshare MAG sequence share; direct Springer supplements | None | 320 fecal metagenomes from 21 breeds and 32 farms, 5,810 medium/high-quality MAGs, 2,661 unidentified species, 162M+ sheep and 82M+ goat non-redundant genes, CAZyme/PUL tables; see [notes](sources/meta320/download.md) |
| [Caprinae Gut MAG Catalog](https://journals.asm.org/doi/10.1128/spectrum.02211-22) | Caprinae gut MAGs from sheep, goats, Tibetan antelope, and Tibetan gazelle | Paper dataset, CNCB BioProject/GSA, ScienceDirect supplementary files, and GitHub code | Public GSA raw FASTQ directory and MD5 file; direct supplement XLSX/PDF files; MAG sequence bulk archive not found in public endpoints | None | 30 ultra-deep fecal metagenomes from six Chinese regions, 5,046 medium/high-quality MAGs, 3,306 SGBs, 2,530 uncultured candidate species, CAZyme/BGC/ARG/virulence annotations, and 1.2 TB of GSA raw reads; see [notes](sources/caprinae-gut-mags/download.md) |
| [UHSG](https://doi.org/10.1002/advs.202300050) | Human skin MAGs across 22 skin sites | CNSA project archive and genome catalog | Public CNSA FTP manifest, metadata TSVs, and per-assembly FASTA links | None | 5,779 MAGs, 813 prokaryotic species, 450 new facial samples plus 2,069 public skin metagenomes; see [notes](sources/uhsg/download.md) |

## Directory Design

### `README.md`

The main landing page for humans. In an `awesome` repository, this is the canonical entry point and should remain easy to scan. Keep descriptions short and avoid turning the front page into a raw data dump.

### `sources/`

Stores structured information for individual data sources when a one-line README entry is not enough. Over time, each source can grow into a dedicated folder such as:

```text
sources/<slug>/
├── metadata.yaml
├── notes.md
└── download.md
```

Recommended use:

- `metadata.yaml`: machine-readable source metadata
- `notes.md`: short curation notes, caveats, or history
- `download.md`: manual download steps, quirks, tokens, cookies, or browser requirements

### `scripts/`

Contains automation helpers for websites that require clicking through multiple pages, filling forms, resolving dynamic URLs, or replaying authenticated browser actions. Keep scripts source-specific and reproducible.

Example future layout:

```text
scripts/
├── shared/
└── <slug>/
    ├── README.md
    └── download.py
```

### `docs/`

Holds repository conventions that should not clutter the front page, such as style rules, source field definitions, and roadmap notes.

### `templates/`

Contains reusable starter files for adding new sources consistently.

## Suggested Entry Fields

Each source should eventually capture as many of the following fields as practical:

- name
- homepage
- short summary
- environment or biome
- source type
- release or version
- update date
- license or terms of use
- download method
- automation availability
- known access quirks

## Curation Rules

- Prefer original project or database pages over third-party mirrors.
- Record direct download URLs when they are stable, but keep the landing page as the primary reference.
- Call out access friction explicitly, such as login requirements, JavaScript-only buttons, request forms, or temporary tokens.
- Keep main-list descriptions brief and move detailed notes into `sources/` or `scripts/`.
- Do not commit downloaded datasets or large derived files.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Add a repository license for the curation text and scripts, while respecting the original licenses and terms attached to each upstream dataset or database.

## Disclaimer

This repository contains automated download scripts designed to simplify the retrieval of public data. Please note:

- **Compliance & Fair Use**: All scripts provided in this repository are simple wrappers that interact exclusively with publicly available APIs, direct download links, or standard web endpoints as intended by the data providers.
- **No Malicious Activity**: These scripts do not perform aggressive scraping, bypass access controls, or cause malicious intrusion to the host servers. They typically include built-in rate-limiting (e.g., delays between requests) to respect server workloads.
- **User Responsibility**: Users of these scripts are responsible for ensuring that their data retrieval complies with the specific terms of service, data usage policies, and licensing requirements of each respective database or dataset provider.
- **Takedown Requests**: If any database maintainer or data provider believes that a script in this repository infringes upon their rights or violates their policies, please open an issue. We will promptly review and remove the relevant scripts.
