from __future__ import annotations

import copy
import json
import unittest
from unittest import mock

from scripts.verify_release_repo import PolicyError, _validate_index, _verify_append_only


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
    def test_fractional_utc_timestamp_is_accepted(self) -> None:
        release = copy.deepcopy(VALID_RELEASE)
        release["published_at_utc"] = "2026-10-03T13:00:00.123456Z"
        _validate_index({"schema_version": 1, "releases": [release]})

    def test_malformed_or_nonexistent_publication_timestamps_are_rejected(self) -> None:
        invalid = (
            "not-a-dateZ",
            "2026-02-30T13:00:00Z",
            "2026-10-03T25:00:00Z",
            "2026-10-03T13:60:00Z",
            "2026-10-03T13:00:00+00:00",
            "2026-10-03T13:00Z",
            "2026-10-03T13:00:00.1234567Z",
            "2026-10-03T13:00:00Z ",
        )
        for timestamp in invalid:
            with self.subTest(timestamp=timestamp):
                release = copy.deepcopy(VALID_RELEASE)
                release["published_at_utc"] = timestamp
                with self.assertRaises(PolicyError):
                    _validate_index({"schema_version": 1, "releases": [release]})

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



class ReleaseAppendOnlyTests(unittest.TestCase):
    def check_against_original(self, original: dict, candidate: dict) -> None:
        # The PR validator reads the trusted base index with git show.
        with mock.patch(
            "scripts.verify_release_repo._git",
            return_value=json.dumps(original),
        ) as git:
            _verify_append_only("origin/main", candidate)
            git.assert_called_once_with("show", "origin/main:release-index.json")

    def test_unchanged_existing_record_is_allowed(self) -> None:
        original = {"schema_version": 1, "releases": [copy.deepcopy(VALID_RELEASE)]}
        self.check_against_original(original, copy.deepcopy(original))

    def test_append_new_release_preserves_existing_record(self) -> None:
        original = {"schema_version": 1, "releases": [copy.deepcopy(VALID_RELEASE)]}
        extra = copy.deepcopy(VALID_RELEASE)
        extra.update(
            version="8.8.86",
            build=384,
            source_sha="c" * 40,
            tag="v8.8.86",
            published_at_utc="2026-10-04T13:00:00Z",
        )
        candidate = {"schema_version": 1, "releases": [copy.deepcopy(VALID_RELEASE), extra]}
        self.check_against_original(original, candidate)

    def test_modify_published_artifact_digest_fails_closed(self) -> None:
        original = {"schema_version": 1, "releases": [copy.deepcopy(VALID_RELEASE)]}
        changed = copy.deepcopy(original)
        changed["releases"][0]["artifacts"][0]["sha256"] = "d" * 64
        with self.assertRaisesRegex(PolicyError, "immutable release record modified"):
            self.check_against_original(original, changed)

    def test_remove_published_record_fails_closed(self) -> None:
        original = {"schema_version": 1, "releases": [copy.deepcopy(VALID_RELEASE)]}
        changed = {"schema_version": 1, "releases": []}
        with self.assertRaisesRegex(PolicyError, "immutable release record removed"):
            self.check_against_original(original, changed)


if __name__ == "__main__":
    unittest.main()
