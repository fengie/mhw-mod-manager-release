# mhw-mod-manager-release

> ⏱️ Last README update: `2026-10-05T22:15:24Z` _(auto-maintained)_

Public release metadata/provenance surface for **MHW Manual Mod Manager**.

Canonical product source is private and lives in `fengie/mhw-mods`. This repository is not a second product source tree.

## Contract

Tracked Git content is metadata-only: release policy, schemas, provenance index, CI, and bounded publication/verification tooling. Release binaries belong in immutable GitHub Release assets.

Every indexed release binds:
- exact `fengie/mhw-mods` source SHA;
- version/build/tag/channel;
- UTC publication time;
- artifact filename, byte size, and SHA-256;
- optional public signing-key identity.

Existing release records are append-only. Bad publications are superseded/recovered explicitly; old provenance is never silently rewritten.

See [RELEASE_CONTRACT.md](RELEASE_CONTRACT.md).

## Verification

```text
python -m unittest discover -s tests -v
python scripts/verify_release_repo.py
```

Pull-request CI also compares `release-index.json` with the base branch and rejects changes/removal of an existing immutable release record.

## Current plans & progress

Canonical ledger: [`_AGENT_CONTEXT/PROJECT_PLAN.md`](_AGENT_CONTEXT/PROJECT_PLAN.md)

Issue #1 owns the artifact/provenance contract rollout.
