# gcMeta Notes

- gcMeta is hosted under the World Data Centre for Microorganisms infrastructure and branded as the Global Catalogue of Metagenomics.
- The `/download` page is public and focuses on catalogue-level bundles rather than per-study archives.
- The paginated `down/list` API is harder than the file download itself because gcMeta encrypts paginated request parameters in the browser.
- This repository avoids that encrypted pagination layer by enumerating catalogue names from public APIs and deriving the public filenames directly.
- The archive host path contains the typo `specail_data`; the frontend uses that path directly, so automation should preserve it exactly.
