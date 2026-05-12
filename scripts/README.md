# Scripts

This directory contains automation helpers for sources that are difficult to download directly or that benefit from a reproducible command-line manifest.

Recommended future pattern:

```text
scripts/<slug>/
├── README.md
└── download.py
```

Keep scripts small, reproducible, and documented. Shared helpers live under `scripts/lib/`.

Current corpus download helpers:

- `bin-chicken-rbgs/download.py`: two Zenodo MAG archives.
- `pigc/download.py`: CNSA manifest filtered to MAG assembly FASTA.
- `rug2/download.py`: ENA binned metagenome assembly FASTA.
- `smag/download.py`: Zenodo split MAG archive download and merge.
- `spire/download.py`: SPIRE URL helper plus `download` subcommand for per-study MAG tar files.
- `uhsg/download.py`: CNSA manifest filtered to MAG assembly FASTA.
