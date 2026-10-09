# Heaven Toolbox — public release channel

> ⏱️ Last README update: **October 9, 2026 · 6:45:59 PM EDT** _(repo-enforced)_

> Identity repaired October 9, 2026 (America/New_York). Repository `fengie/heaven-toolbox-release` was renamed from `fengie/mhw-mod-manager-release`; **renaming did not publish Toolbox binaries**.

## Current release status

| Channel | What exists | State |
| --- | --- | --- |
| **MHW legacy archive** | Existing `updater-main-*` release assets and append-only SHA-256/index data | Preserved; not rebranded or revoked |
| **Heaven Toolbox** | Private canonical source at [fengie/heaven-toolbox](https://github.com/fengie/heaven-toolbox) | **Not configured for signed artifact publication or installed-client verification** |
| **Heaven Mod Manager current source** | Public [fengie/Heaven-Mod_Manager](https://github.com/fengie/Heaven-Mod_Manager) | Product releases and client updater continue under their existing verified channels until explicitly migrated |

This is an artifact/provenance-only repository, not a second source tree. Old historical `source_repository=fengie/mhw-mods` values in [release-index.json](release-index.json) are intentionally **not** rewritten: they bind immutable released artifacts to their original source identity. Existing GitHub releases remain historical **MHW Mod Manager**, including tag `updater-main-480`.

## Future Toolbox publishing (not yet activated)

Prior to first Toolbox release: complete independently authenticated publication from exact `fengie/heaven-toolbox@main` CI, verifiable artifact signatures/attestations and digests, a **new product-separated schema/CI check** with negative cross-product fixtures, public verification keys only, and actual installed plugin/consumer rollback evidence. Do not use this release repository as a shortcut around protected Toolbox admission.

**Current verifier intentionally rejects new Toolbox records until that work is done.** See [RELEASE_CONTRACT.md](RELEASE_CONTRACT.md) and [current plan](_AGENT_CONTEXT/PROJECT_PLAN.md). No new artifacts are announced by this metadata repair.

## Existing verification

```text
python -m unittest discover -s tests -v
python scripts/verify_release_repo.py
```

PR policy checks existing provenance records append-only against main. Human-readable MHW historical timestamps live in [VERSION_TIMESTAMPS.md](VERSION_TIMESTAMPS.md).
