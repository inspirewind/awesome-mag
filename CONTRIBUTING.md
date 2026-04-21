# Contributing to Awesome MAG

## Principles

- Keep the main `README.md` readable first.
- Prefer stable upstream links over mirrors whenever possible.
- Separate curation content from automation code.
- Do not commit downloaded datasets, caches, or large derived outputs.

## Recommended Workflow

1. Add or update the source entry in `README.md`.
2. If the source needs more detail, create a folder under `sources/<slug>/`.
3. If the source needs automation, add a source-specific script under `scripts/<slug>/`.
4. Document unusual access constraints clearly.

## Naming

- Use lowercase kebab-case slugs such as `gtdb`, `uhgg`, or `ocean-mag-catalog`.
- Keep short descriptions factual and compact.
- Prefer consistent source names across README entries, folder names, and scripts.

## Minimum Source Information

Try to capture at least:

- source name
- homepage or landing page
- one-sentence description
- relevant biome or scope
- access mode
- license or usage terms when available

## Script Guidelines

- Keep dependencies minimal.
- Prefer transparent scripts over opaque browser recordings.
- Document required environment variables, cookies, or login assumptions.
- Add usage notes next to the script or in `scripts/<slug>/README.md`.
- Respect upstream terms of service and access restrictions.

## What Not to Add

- downloaded genome archives
- large metadata dumps
- generated tables that can be recreated from source metadata
- scripts with hard-coded personal credentials
