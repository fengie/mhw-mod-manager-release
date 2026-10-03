# Agent Instructions — MHW Public Release Repository

This repository is the public **artifact/provenance publication surface** for the MHW Manual Mod Manager. Canonical product source, product planning, updater implementation, tests, and release engineering live in `fengie/mhw-mods`.

Before mutation, refresh current `fengie/heaven-toolbox@main` training and current `fengie/mhw-mods@main` release state. This repository must never become a second product source tree.

## Repository-local invariants

- Tracked Git content is metadata, policy, schemas, CI, and bounded publication tooling only.
- Release binaries belong in immutable GitHub Release assets, not in the tracked repository tree.
- Every indexed release must bind an exact 40-character `fengie/mhw-mods` source SHA to a version/build/tag/channel, publication time, and artifact SHA-256/size.
- Existing indexed release records are append-only. Ordinary changes may add records; they may not silently rewrite or delete published provenance.
- Private signing keys, release credentials, tokens, and other secrets never enter Git, issue text, logs, or provenance payloads.
- A bad publication is handled by an explicit superseding/recovery procedure; never normalize silent replacement of an immutable artifact.
- Run `python scripts/verify_release_repo.py` before delivery. Pull requests must also run append-only verification against their base branch.

See `RELEASE_CONTRACT.md` and `schemas/release-provenance.schema.json`.
