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

## Current Entries

### General MAG Catalogs and Database Portals

| Resource | Scope | Type | Access | Automation | Notes |
| --- | --- | --- | --- | --- | --- |
| [MAGdb](https://magdb.nanhulab.ac.cn/) | Clinical, Environment, Animal | Database portal | Public listings; cookie-gated archive downloads | [Download script](scripts/magdb/README.md) | Per-study `data.tar.gz`; 74 study packages downloaded; see [notes](sources/magdb/download.md) |
| [gcMeta](https://gcmeta.wdcm.org/) | Multi-biome catalogues | Database portal | Public catalogue APIs; public direct archive files | [Download script](scripts/gcmeta/README.md) | 50 catalogue bundles; public `catalogueTree` and `catalogueNameList` enumeration plus derived direct files on `open.nmdc.cn`; see [notes](sources/gcmeta/download.md) |

## Repository Layout

```text
awesome-mag/
├── README.md
├── CONTRIBUTING.md
├── docs/
│   └── README.md
├── sources/
│   ├── README.md
│   ├── gcmeta/
│   │   ├── download.md
│   │   ├── metadata.yaml
│   │   └── notes.md
│   └── magdb/
│       ├── download.md
│       ├── metadata.yaml
│       └── notes.md
├── scripts/
│   ├── README.md
│   ├── gcmeta/
│   │   ├── README.md
│   │   └── download.py
│   └── magdb/
│       ├── README.md
│       └── download.py
└── templates/
    └── source.template.yaml
```

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

## How `awesome` Repositories Usually Stay Maintainable

In practice, strong `awesome` repositories follow a few simple rules:

- the main list is curated and human-readable
- entries are grouped by clear categories rather than chronology
- each entry has a short, consistent description
- detailed operational notes live outside the front page
- contribution rules are explicit
- bulk data and generated artifacts are kept out of Git

For this project specifically, that means:

- `README.md` should remain the discovery layer
- `sources/` should hold deeper structured metadata
- `scripts/` should hold automation, not curation prose
- downloaded data should stay outside the repository

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
