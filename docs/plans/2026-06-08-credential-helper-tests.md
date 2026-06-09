# Credential Helper Tests Plan

status: completed

## Context

`TweetShakeHasConfiguredCredentialValue` is the local guard that decides whether
Fabric/TwitterKit startup can proceed. It rejects missing, blank, unresolved
build-setting, and replacement-placeholder values, and it accepts trimmed local
credential values.

## Objectives

- Enable app code testability for the unit-test target.
- Replace generated XCTest placeholders with focused credential helper tests.
- Cover missing, blank, unresolved build-setting, replacement-placeholder, and
  trimmed local credential values.
- Keep real Twitter/Fabric credentials out of git and out of tests.
- Extend the static baseline so credential helper tests remain visible without
  Xcode.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
