# Release Publication Contract

`fengie/mhw-mod-manager-release` is a public metadata/provenance surface for releases produced from the private canonical product repository `fengie/mhw-mods`.

## Source of truth

Product code, tests, updater logic, version decisions, and release orchestration remain in `fengie/mhw-mods`. This repository must not contain a second copy of product source or be used to reconstruct unpublished private implementation.

Tracked Git content here is limited to release-policy documentation, schemas, bounded verification/publication tooling, CI, and machine-readable provenance.

## Artifact publication

Release executables, installers, archives, and libraries are published as immutable GitHub Release assets. Each indexed release record must identify:

- exact `fengie/mhw-mods` source SHA;
- product version and updater/build number;
- immutable release tag and channel;
- UTC publication timestamp;
- every published artifact filename, byte size, and SHA-256;
- optional public signing-metadata key identity when independent updater signing is enabled.

The source SHA and artifact digest are facts supplied by the verified release pipeline. Agents must not infer, truncate, or fabricate them.

## Append-only provenance

`release-index.json` is append-only after publication. Existing release records may not be changed or removed by an ordinary pull request. If a release is bad, publish a separately identified corrected/superseding release and document the recovery. Do not mutate old provenance so history appears clean.

The policy gate compares the proposed index with the target branch and fails if an existing release record is removed or changed.

## Secrets and signing

Only public verification metadata such as a signing key ID/public-key identity may appear here. Private signing keys, GitHub credentials, cookies, HMAC material, API tokens, certificate private keys, recovery secrets, and other credentials remain outside this repository.

## "Latest" state

Any future "latest" pointer must be generated from immutable release records. It is a convenience view, not the authority for artifact identity.

## Recovery boundary

A publication mistake and an installed-client update rollback are different operations:

- **bad publication:** stop promotion, preserve evidence, publish a corrected/superseding immutable release or explicitly revoke according to the signed-metadata design;
- **client rollback:** restore the client's prior known-good installation under the product updater's transactional rules.

Neither operation authorizes overwriting a previously indexed artifact or source identity in place.

## Verification

Run:

```text
python scripts/verify_release_repo.py
```

Pull-request CI additionally runs:

```text
python scripts/verify_release_repo.py --base-ref origin/<base>
```

The verifier rejects malformed provenance, non-exact source SHAs, invalid artifact digests, duplicate release identities, tracked MHW product/binary payloads, oversized tracked files, and modification/removal of existing release records.
