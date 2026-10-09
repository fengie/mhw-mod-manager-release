# Agent instructions — Heaven public release archive / future Toolbox channel

**Canonical repository:** `fengie/heaven-toolbox-release` (renamed from `fengie/mhw-mod-manager-release`; GitHub repository ID 1395549117).
**This repository currently contains legacy MHW Release assets, not deployed Toolbox binaries.** Treat the existing MHW archive as immutable and ensure older updater clients remain compatible.

Before writing, refresh `fengie/heaven-toolbox@main` AGENTS/training/Git directive, this repo's current main/index, the active source product and release owners. Public availability never permits leaking private Toolbox source, tokens, signing keys, configuration or CI logs.

## Immutable provenance and release boundary

- `release-index.json` schema v1 contains historical MHW records whose literal `source_repository=fengie/mhw-mods` is part of a published historical record. **Do not rewrite those identities to new names** or erase history.
- Existing `updater-main-*` GitHub Releases and assets refer to MHW. **Never rebrand or replace them with Toolbox artifacts.**
- Future `toolbox-v*` publication is **blocked until** an independent signer / trusted CI producer and runtime consumption check are implemented, tests pass, and a reviewed new schema/validator explicitly supports product-separated provenance. The current verifier intentionally accepts only historical MHW source identity, and does NOT establish any Toolbox release publication capability.
- No direct unreviewed release uploads, tag overwrites, secret commits, private source mirroring, or unproven security attestation claims.
- Track release-configuration work separately from publishing; source merge != artifact publish != installed runtime. Verify main and named consumer compatibility.

Test `python -m unittest discover -s tests -v` and `python scripts/verify_release_repo.py --base-ref origin/main` on a real exact candidate checkout; CI is the trusted mechanical check. See `RELEASE_CONTRACT.md` and `_AGENT_CONTEXT/PROJECT_PLAN.md`.
