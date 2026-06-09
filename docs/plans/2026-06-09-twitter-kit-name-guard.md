# Twitter Kit Name Guard

status: completed

## Context

The Fabric configuration contains a list of kits. The credential helper should
only accept `KitInfo` credentials from the explicitly named Twitter kit, not from
an arbitrary or malformed kit dictionary that happens to contain credential-like
keys.

## Objectives

- Split Fabric credential parsing into a testable helper.
- Require `KitName == "Twitter"` before accepting Twitter `KitInfo` values.
- Add tests for unnamed and correctly named Twitter kit dictionaries.
- Extend the static baseline so the Twitter kit name guard remains visible
  without Xcode.
- Preserve local credential handling without adding background API calls,
  uploads, analytics, persistence, or outcome storage.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
