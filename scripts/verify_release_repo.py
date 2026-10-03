from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

INDEX_PATH = Path("release-index.json")
MAX_TRACKED_FILE_BYTES = 2 * 1024 * 1024
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
VERSION = re.compile(r"^[0-9]+(?:\.[0-9]+){2,3}(?:[-+][0-9A-Za-z.-]+)?$")
FORBIDDEN_PRODUCT_SUFFIXES = {
    ".cs", ".xaml", ".csproj", ".sln", ".vcxproj", ".exe", ".dll", ".msi", ".zip"
}
ALLOWED_CHANNELS = {"stable", "beta", "preview", "internal"}


class PolicyError(RuntimeError):
    pass


def _git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise PolicyError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def _tracked_files() -> list[Path]:
    return [Path(line) for line in _git("ls-files").splitlines() if line.strip()]


def _load_index_bytes(data: bytes, source: str) -> dict[str, Any]:
    try:
        payload = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PolicyError(f"{source}: invalid UTF-8 JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise PolicyError(f"{source}: top-level value must be an object")
    return payload


def _load_index(path: Path = INDEX_PATH) -> dict[str, Any]:
    if not path.is_file():
        raise PolicyError(f"missing required {path}")
    return _load_index_bytes(path.read_bytes(), str(path))


def _require_keys(obj: dict[str, Any], required: set[str], source: str) -> None:
    missing = sorted(required - set(obj))
    if missing:
        raise PolicyError(f"{source}: missing required fields: {', '.join(missing)}")


def _validate_artifact(artifact: Any, source: str) -> None:
    if not isinstance(artifact, dict):
        raise PolicyError(f"{source}: artifact must be an object")
    _require_keys(artifact, {"name", "size_bytes", "sha256"}, source)
    name = artifact["name"]
    if not isinstance(name, str) or not name or "/" in name or "\\" in name:
        raise PolicyError(f"{source}: artifact name must be a plain filename")
    size = artifact["size_bytes"]
    if not isinstance(size, int) or isinstance(size, bool) or size < 0:
        raise PolicyError(f"{source}: size_bytes must be a nonnegative integer")
    digest = artifact["sha256"]
    if not isinstance(digest, str) or not SHA256.fullmatch(digest):
        raise PolicyError(f"{source}: sha256 must be 64 lowercase hex characters")
    if "signed_metadata_key_id" in artifact:
        key_id = artifact["signed_metadata_key_id"]
        if not isinstance(key_id, str) or not key_id.strip():
            raise PolicyError(f"{source}: signed_metadata_key_id must be nonblank")


def _validate_release(release: Any, index: int) -> str:
    source = f"release-index.json releases[{index}]"
    if not isinstance(release, dict):
        raise PolicyError(f"{source}: release must be an object")
    _require_keys(
        release,
        {
            "version",
            "build",
            "source_repository",
            "source_sha",
            "tag",
            "channel",
            "published_at_utc",
            "artifacts",
        },
        source,
    )
    if release["source_repository"] != "fengie/mhw-mods":
        raise PolicyError(f"{source}: source_repository must be fengie/mhw-mods")
    if not isinstance(release["source_sha"], str) or not SHA40.fullmatch(release["source_sha"]):
        raise PolicyError(f"{source}: source_sha must be an exact 40-char lowercase Git SHA")
    if not isinstance(release["version"], str) or not VERSION.fullmatch(release["version"]):
        raise PolicyError(f"{source}: version has unsupported format")
    if not isinstance(release["build"], int) or isinstance(release["build"], bool) or release["build"] < 0:
        raise PolicyError(f"{source}: build must be a nonnegative integer")
    if not isinstance(release["tag"], str) or not release["tag"].strip():
        raise PolicyError(f"{source}: tag must be nonblank")
    if release["channel"] not in ALLOWED_CHANNELS:
        raise PolicyError(f"{source}: unsupported channel {release['channel']!r}")
    if not isinstance(release["published_at_utc"], str) or not release["published_at_utc"].endswith("Z"):
        raise PolicyError(f"{source}: published_at_utc must be a UTC timestamp ending in Z")
    artifacts = release["artifacts"]
    if not isinstance(artifacts, list) or not artifacts:
        raise PolicyError(f"{source}: artifacts must be a non-empty array")
    names: set[str] = set()
    for artifact_index, artifact in enumerate(artifacts):
        _validate_artifact(artifact, f"{source}.artifacts[{artifact_index}]")
        if artifact["name"] in names:
            raise PolicyError(f"{source}: duplicate artifact name {artifact['name']!r}")
        names.add(artifact["name"])
    return f"{release['version']}|{release['build']}|{release['tag']}"


def _validate_index(payload: dict[str, Any]) -> None:
    _require_keys(payload, {"schema_version", "releases"}, "release-index.json")
    if payload["schema_version"] != 1:
        raise PolicyError("release-index.json: schema_version must be 1")
    releases = payload["releases"]
    if not isinstance(releases, list):
        raise PolicyError("release-index.json: releases must be an array")
    identities: set[str] = set()
    source_shas: set[str] = set()
    for index, release in enumerate(releases):
        identity = _validate_release(release, index)
        if identity in identities:
            raise PolicyError(f"release-index.json: duplicate release identity {identity}")
        identities.add(identity)
        source_sha = release["source_sha"]
        if source_sha in source_shas:
            raise PolicyError(
                "release-index.json: one source SHA may appear only once; "
                f"duplicate {source_sha}"
            )
        source_shas.add(source_sha)


def _release_map(payload: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for index, release in enumerate(payload.get("releases", [])):
        identity = _validate_release(release, index)
        result[identity] = release
    return result


def _verify_append_only(base_ref: str, current: dict[str, Any]) -> None:
    try:
        old_bytes = _git("show", f"{base_ref}:{INDEX_PATH.as_posix()}").encode("utf-8")
    except PolicyError as exc:
        if "does not exist" in str(exc) or "exists on disk, but not in" in str(exc):
            return
        raise
    old = _load_index_bytes(old_bytes, f"{base_ref}:{INDEX_PATH}")
    _validate_index(old)
    old_map = _release_map(old)
    current_map = _release_map(current)
    for identity, old_record in old_map.items():
        if identity not in current_map:
            raise PolicyError(f"immutable release record removed: {identity}")
        if current_map[identity] != old_record:
            raise PolicyError(f"immutable release record modified: {identity}")


def _verify_tracked_tree() -> None:
    for path in _tracked_files():
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix in FORBIDDEN_PRODUCT_SUFFIXES:
            raise PolicyError(
                f"tracked product/binary payload is forbidden in metadata repo: {path}"
            )
        size = path.stat().st_size
        if size > MAX_TRACKED_FILE_BYTES:
            raise PolicyError(
                f"tracked file exceeds {MAX_TRACKED_FILE_BYTES} bytes: {path} ({size})"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate MHW public release repository policy.")
    parser.add_argument(
        "--base-ref",
        help="Optional Git ref used to enforce append-only release-index semantics.",
    )
    args = parser.parse_args()

    try:
        payload = _load_index()
        _validate_index(payload)
        _verify_tracked_tree()
        if args.base_ref:
            _verify_append_only(args.base_ref, payload)
    except PolicyError as exc:
        print(f"release-repo policy: FAIL: {exc}", file=sys.stderr)
        return 1

    print(
        "release-repo policy: PASS "
        f"({len(payload['releases'])} immutable release records)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
