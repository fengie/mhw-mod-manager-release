# Project Plan — Canonical Work Ledger

This file is the repository's durable current-work ledger. It follows the ownership-aware project-plan guidance in `fengie/heaven-toolbox@main`.

## Operating rules

- Allowed statuses: `PLANNED`, `READY`, `ACTIVE`, `BLOCKED`, `DEFERRED`, `DONE`, `SUPERSEDED`.
- Nonterminal items record source/evidence, owner or `unclaimed`, acceptance criteria/goal, and one concrete next action.
- Checkboxes become complete only from canonical-main or exact referenced evidence.
- Update this ledger after material ownership/status/blocker changes, after integration, and before handoff.
- Do not fabricate roadmap items to make a quiet repository appear active.

## Current plans & progress

### RELEASE-001 — Artifact-only provenance and immutability contract

**Status:** ACTIVE  
**Owner:** issue #1 / branch `issue-1-artifact-provenance-contract`  
**Goal:** keep this public repository metadata-only while proving exact private-source-to-public-artifact provenance and preventing silent historical rewrites.

- [x] Define repository-local artifact-only agent/policy contract.
- [x] Add machine-readable provenance schema.
- [x] Seed an evidence-neutral append-only release index without inventing historical records.
- [x] Add strict release-index/tree verifier.
- [x] Add regressions for invalid/missing source SHA and artifact digest.
- [x] Add pull-request CI that enforces append-only provenance against the base branch.
- [x] Document bad-publication recovery separately from installed-client rollback.
- [ ] Wire canonical `fengie/mhw-mods` release publication to generate/submit provenance from exact verified release inputs.
- [ ] Pass exact candidate CI, merge to canonical `main`, verify remote main, and close issue #1.

**Execution-path note:** this ChatGPT session exposes authenticated GitHub but no callable Heaven/Agent Control local-runtime namespace, so local offload was unavailable. Candidate CI is the mechanical verification path.

**Next action:** open the policy PR and require exact-head CI; after that lands, add the producer-side MHW publication adapter under the MHW repository's own release ownership rules.
