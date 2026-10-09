# Public release contract — legacy MHW archive and proposed Toolbox product

**Owner:** `fengie/heaven-toolbox-release`. It retains the original `fengie/mhw-mod-manager-release` repository ID and GitHub Release assets.

## What is actually published

Historical `release-index.json` is immutable schema v1 for MHW builds from former `fengie/mhw-mods` source. All source SHAs, timestamps, version/build/tag/channel, artifact filenames, sizes and SHA-256 digests remain EXACT. The source was later renamed `fengie/Heaven-Mod_Manager`, but the original literal identity must not be falsified in the historic records. Existing MHW updater URLs that GitHub redirects **must be end-to-end tested against installed clients**, not assumed safe by source inspection.

No new Heaven Toolbox binary, release tag, or independent signing key is deployed here as part of this repair.

## Current policy gates

Tracked Git content is restricted to metadata, release contracts, schemas, CI, bounded Python verification, and project state. ZIP/DLL/EXE binary artifacts belong only in immutable GitHub Releases and are not checked into Git.

Current [verifier](scripts/verify_release_repo.py) validates MHW schema v1 and rejects unrecognized source repositories, malformed exact SHAs, duplicate identities, invalid timestamps or digests, tracked binary payloads, and mutation/deletion of an existing release index record. Keep this closed by default until the separately reviewed Toolbox v2 release contract is operational.

New Toolbox releases **must not** reuse MHW's `updater-main-*` tag namespace or download paths. Proposed exclusive namespace: `toolbox-v<semver>` and a separate product release-index partition with exact `fengie/heaven-toolbox` source SHA, cryptographically validated artifact evidence and version-to-installed-package identity. Signer secrets and credentials remain outside public Git repositories.

Before changing the allowlist/schema: add tests that forbid cross-product artifact substitution, MHW archive rewrite, hash mismatch, duplicate Toolbox tags, unverifiable signing metadata, and unintended non-Toolbox publication. Do not treat a metadata key *identifier* as a verified signature. Use a trusted release producer and an independently verifiable consumer/rollback check.

## Recovery / handling bad publications

Preserve historical release records. On a bad artifact: stop promotion, retain evidence, and issue a separately identified corrected/superseding release with verified identity or approved revocation; do not overwrite immutable artifacts or reassign a tag. Installed-client rollback is a separate transactional operation and must be tested independently.

**Critical pending work:** actual private Toolbox signed release producer + reviewer authorization + public metadata verifier + a tested installed consumer. Those are blocked and not "green" simply because this repository is public.
