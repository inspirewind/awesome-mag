# Scripts

This directory contains automation helpers for sources that are difficult to download directly or that benefit from a reproducible command-line manifest.

Recommended future pattern:

```text
scripts/<slug>/
├── README.md
└── download.py
```

Keep scripts small, reproducible, and documented. If a source needs shared helpers later, add them under `scripts/shared/`.
