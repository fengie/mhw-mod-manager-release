from __future__ import annotations

import copy
import unittest

from scripts.verify_release_repo import PolicyError, _validate_index


VALID_RELEASE = {
    "version": "8.8.85",
    "build": 383,
    "source_repository": "fengie/mhw-mods",
    "source_sha": "a" * 40,
    "tag": "v8.8.85",
    "channel": "stable",
    "published_at_utc": "2026-10-03T13:00:00Z",
    "artifacts": [
        {
            "name": "MhwModManager.exe",
            "size_bytes": 123,
            "sha256": "b" * 64,
        }
    ],
}


class ReleasePolicyTests(unittest.TestCase):
    def test_valid_release_is_accepted(self) -> None:
        _validate_index({"schema_version": 1, "releases": [VALID_RELEASE]})

    def test_missing_exact_source_sha_is_rejected(self) -> None:
        payload = copy.deepcopy(VALID_RELEASE)
        payload["source_sha"] = "deadbeef"
        with self.assertRaises(PolicyError):
            _validate_index({"schema_version": 1, "releases": [payload]})

    def test_bad_artifact_digest_is_rejected(self) -> None:
        payload = copy.deepcopy(VALID_RELEASE)
        payload["artifacts"][0]["sha256"] = "not-a-digest"
        with self.assertRaises(PolicyError):
            _validate_index({"schema_version": 1, "releases": [payload]})

    def test_duplicate_release_identity_is_rejected(self) -> None:
        with self.assertRaises(PolicyError):
            _validate_index({
                "schema_version": 1,
                "releases": [VALID_RELEASE, copy.deepcopy(VALID_RELEASE)],
            })


if __name__ == "__main__":
    unittest.main()
